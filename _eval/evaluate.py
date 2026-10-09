#!/usr/bin/env python3
"""
Pipeline workspace — eval.

Three layers:
  structure   — pure filesystem/markdown analysis, plus output lineage. Zero tokens. Fast.
  legibility  — a local model executes stages; checks mechanics only. Free.
  behaviour   — runs stages headless against each case (synthetic fixtures + frozen real runs)
                and grades the output. Costs tokens. Case dirs: `case_roots` in checks.json.

Every run follows one pipeline (the `Pipeline:` line in its CLAUDE.md), whose blank method lives in
_templates/<pipeline>/. What it enforces lives in checks.json, not here. Rubrics live in
rubrics/<pipeline>/. Run it with ./eval from the workspace root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_tools"))
import local as local_mod  # noqa: E402
import manifest as manifest_mod  # noqa: E402
import prd_digest as prd_digest_mod  # noqa: E402  (process tool; the eval only checks its output)
import prd_checks as prd_checks_mod  # noqa: E402

EVAL_DIR = Path(__file__).resolve().parent
ROOT = EVAL_DIR.parent
REPORT_DIR = EVAL_DIR / "report"
SCRATCH = ROOT / "_eval-scratch"

STAGE_RE = re.compile(r"^\d{2}_[a-z0-9-]+$")
RUN_RE = re.compile(r"^\d+-[a-z0-9-]+$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
OUTFILE_RE = re.compile(r"[A-Za-z0-9_.<>/-]+\.(?:md|ya?ml|html)$")

SEV_ORDER = {"fail": 0, "warn": 1, "info": 2, "pass": 3}


# ───────────────────────────────────────────────────────────── findings

@dataclass
class Finding:
    check: str
    severity: str
    layer: str
    message: str
    scope: str = ""          # e.g. "01-<slug> / 02_explore"
    file: str = ""           # workspace-relative
    line: int = 0
    detail: str = ""
    ignored: bool = False


class Results:
    def __init__(self, spec: dict):
        self.spec = spec
        self.findings: list[Finding] = []
        self.counts = {"fail": 0, "warn": 0, "info": 0, "pass": 0}
        self.passed_checks: dict[str, int] = {}

    def add(self, check: str, message: str, *, layer: str = "structure",
            scope: str = "", file: str = "", line: int = 0, detail: str = "",
            severity: str | None = None) -> None:
        sev = severity or self.spec["severities"].get(check, "warn")
        ig = self.spec.get("ignore", {})
        ignored = check in ig.get("check_ids", []) or any(
            p and p in file for p in ig.get("paths", [])
        )
        self.counts[sev] += 1
        self.findings.append(Finding(check, sev, layer, message, scope, file, line, detail, ignored))

    def ok(self, check: str) -> None:
        """Record a silent pass, for the coverage count."""
        self.passed_checks[check] = self.passed_checks.get(check, 0) + 1
        self.counts["pass"] += 1

    @property
    def blocking(self) -> int:
        return sum(1 for f in self.findings if f.severity == "fail" and not f.ignored)


# ───────────────────────────────────────────────────────────── markdown helpers

def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def sections(text: str) -> dict[str, tuple[int, str]]:
    """Split markdown on '## ' headings -> {heading: (line_no, body)}."""
    out: dict[str, tuple[int, str]] = {}
    current, buf, start = None, [], 0
    for i, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            if current is not None:
                out[current] = (start, "\n".join(buf))
            current, buf, start = line[3:].strip(), [], i
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = (start, "\n".join(buf))
    return out


def find_line(text: str, needle: str) -> int:
    for i, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return i
    return 0


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def norm(text: str) -> str:
    return "\n".join(l.rstrip() for l in text.strip().splitlines())


def digest(text: str) -> str:
    return hashlib.sha256(norm(text).encode()).hexdigest()[:12]


def looks_like_path(token: str) -> bool:
    return "/" in token or token.endswith((".md", ".html", ".yaml", ".yml"))


def paths_in(body: str) -> list[str]:
    return [t for t in BACKTICK_RE.findall(body) if looks_like_path(t)]


def split_inputs(body: str) -> tuple[list[str], list[str]]:
    """Return (named inputs, do-not-load paths) from an Inputs section body."""
    named, forbidden = [], []
    for line in body.splitlines():
        target = forbidden if re.search(r"do\s*not\s*load", line, re.I) else named
        target.extend(paths_in(line))
    return named, forbidden


# ───────────────────────────────────────────────────────────── discovery

TYPES = ("core", "live", "optional")
IDENTITY_RE = r"\*\*{field}:\*\*\s*(.+)"


def templates_root(spec: dict) -> Path:
    return ROOT / spec.get("templates_dir", "_templates")


def pipeline_spec(spec: dict, name: str) -> dict:
    return spec.get("pipelines", {}).get(name, {})


def template_dir(spec: dict, name: str) -> Path:
    return templates_root(spec) / name


def template_folders(spec: dict) -> list[Path]:
    root = templates_root(spec)
    return sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []


def template_stages(spec: dict, name: str) -> list[str]:
    tdir = template_dir(spec, name)
    if not tdir.is_dir():
        return []
    return sorted(p.name for p in tdir.iterdir() if p.is_dir() and STAGE_RE.match(p.name))


def identity_field(run: Path, field_name: str) -> str:
    """Value of a `- **Field:** value` line in a run's CLAUDE.md, backticks stripped. "" if absent."""
    m = re.search(IDENTITY_RE.format(field=re.escape(field_name)), read(run / "CLAUDE.md"))
    return m.group(1).strip().strip("`").strip() if m else ""


def pipeline_of(run: Path, spec: dict) -> str:
    """A run's pipeline. Runs made before pipelines existed have no line and are the default."""
    return identity_field(run, "Pipeline") or spec.get("default_pipeline", "discovery")


def upstream_of(run: Path) -> str:
    """Workspace-relative upstream path, or "" for none / unfilled."""
    value = identity_field(run, "Upstream")
    if not value or value.lower() in ("none", "-", "n/a") or "<" in value:
        return ""
    return value.removeprefix("./")


def all_terminal_folders(spec: dict) -> list[str]:
    seen: list[str] = []
    for p in spec.get("pipelines", {}).values():
        seen += [t for t in p.get("terminal_folders", []) if t not in seen]
    return seen


def runs() -> list[Path]:
    return sorted(p for p in ROOT.iterdir()
                  if p.is_dir() and RUN_RE.match(p.name)
                  and any(c.is_dir() and STAGE_RE.match(c.name) for c in p.iterdir()))


def stages_of(run: Path) -> list[str]:
    return sorted(p.name for p in run.iterdir() if p.is_dir() and STAGE_RE.match(p.name))


# ───────────────────────────────────────────────────────────── structural checks

def check_walk(r: Results) -> None:
    """Entry points exist, and the root route table points at real files."""
    entrypoints = list(r.spec["entrypoints"])
    for name in r.spec.get("pipelines", {}):
        tdir = rel(template_dir(r.spec, name))
        entrypoints += [f"{tdir}/CLAUDE.md", f"{tdir}/CONTEXT.md"]
    for ep in entrypoints:
        if (ROOT / ep).exists():
            r.ok("walk.entrypoint-missing")
        else:
            r.add("walk.entrypoint-missing", f"entry point missing: {ep}",
                  scope="workspace", file=ep)

    claude = read(ROOT / "CLAUDE.md")
    for token in paths_in(claude):
        if token.startswith(tuple(r.spec["external_path_prefixes"])) or "*" in token:
            continue
        candidate = token.rstrip("/")
        # route table rows name either a concrete file or a run-relative pattern.
        # "<" is a placeholder; a space or a leading "./" means it's a command, not a path.
        if "<" in candidate or " " in candidate or candidate.startswith("./"):
            continue
        if (ROOT / candidate).exists():
            r.ok("walk.route-target-missing")
        elif candidate.startswith(("09", "10", "_")) or "/" not in candidate:
            r.ok("walk.route-target-missing")  # generic reference, not a path claim
        else:
            r.add("walk.route-target-missing",
                  f"root CLAUDE.md routes to something that does not exist: {candidate}",
                  scope="workspace", file="CLAUDE.md",
                  line=find_line(claude, candidate))


def check_shared_references(r: Results) -> None:
    """Every _shared/<file> named anywhere in the workspace resolves."""
    for md in sorted(ROOT.rglob("*.md")):
        if "_eval" in md.parts or "_eval-scratch" in md.parts:
            continue
        text = read(md)
        for token in set(BACKTICK_RE.findall(text)):
            m = re.search(r"_shared/([A-Za-z0-9_.-]+\.(?:md|ya?ml))$", token)
            if not m:
                continue
            if (ROOT / "_shared" / m.group(1)).exists():
                r.ok("shared.dangling-reference")
            else:
                r.add("shared.dangling-reference",
                      f"references _shared/{m.group(1)}, which does not exist",
                      scope=rel(md.parent), file=rel(md), line=find_line(text, token))


def check_templates(r: Results) -> None:
    """Every template folder is a registered pipeline, and its running-order table is complete."""
    registered = r.spec.get("pipelines", {})
    folders = {p.name: p for p in template_folders(r.spec)}
    for name, tdir in folders.items():
        if name not in registered:
            r.add("pipeline.unregistered",
                  f"_templates/{name} has no entry under `pipelines` in _eval/checks.json",
                  scope=f"pipeline {name}", file=rel(tdir),
                  detail="Register its canonical_outputs, optional_stages, terminal_folders and "
                         "behaviour_stages. See AUTHORING.md.")
    for name in registered:
        if name not in folders:
            r.add("pipeline.unregistered",
                  f"checks.json registers pipeline {name}, but {rel(template_dir(r.spec, name))} does not exist",
                  scope=f"pipeline {name}", file="_eval/checks.json")
            continue
        check_running_order(r, name)


def check_running_order(r: Results, name: str) -> None:
    """The template's CONTEXT.md table gives every stage a type; optional rows match checks.json."""
    tdir = template_dir(r.spec, name)
    path = tdir / "CONTEXT.md"
    text = read(path)
    scope = f"pipeline {name}"
    typed: dict[str, str] = {}
    for line in text.splitlines():
        cells = [c.strip().strip("`") for c in line.split("|")]
        stage = next((c for c in cells if STAGE_RE.match(c)), None)
        kind = next((c for c in cells if c in TYPES), None)
        if stage and kind and stage not in typed:
            typed[stage] = kind
    stages = template_stages(r.spec, name)
    for stage in stages:
        if stage in typed:
            r.ok("pipeline.running-order")
        else:
            r.add("pipeline.running-order",
                  f"{stage} has no row with a type (core / live / optional) in the running-order table",
                  scope=scope, file=rel(path),
                  detail="`work` reads the running order to choose the next step. A stage missing "
                         "from it is never proposed.")
    for stage in typed:
        if stage not in stages:
            r.add("pipeline.running-order",
                  f"running-order table lists {stage}, which is not a stage folder in this template",
                  scope=scope, file=rel(path), line=find_line(text, stage))
    declared = set(pipeline_spec(r.spec, name).get("optional_stages", []))
    tabled = {s for s, k in typed.items() if k == "optional"}
    if declared != tabled:
        r.add("pipeline.running-order",
              f"optional stages disagree — table: {sorted(tabled)}, checks.json: {sorted(declared)}",
              scope=scope, file=rel(path))
    else:
        r.ok("pipeline.running-order")


def check_run_shape(r: Results, run: Path, tmpl_stages: list[str], pipeline: str) -> None:
    present = stages_of(run)
    optional = set(pipeline_spec(r.spec, pipeline).get("optional_stages", []))
    for stage in tmpl_stages:
        if stage in present:
            r.ok("run.stage-missing")
        elif stage in optional:
            r.add("run.optional-stage-absent", f"optional stage not instantiated: {stage}",
                  scope=run.name, file=rel(run))
        else:
            r.add("run.stage-missing", f"stage folder missing: {stage}",
                  scope=run.name, file=rel(run))
    for stage in present:
        if stage not in tmpl_stages:
            r.add("run.extra-stage",
                  f"stage {stage} exists in this run but not in _templates/{pipeline} — method and instance have diverged",
                  scope=run.name, file=rel(run / stage))

    for folder in [run] + [run / s for s in present]:
        if not (folder / "CONTEXT.md").exists():
            r.add("contract.missing-section", "no CONTEXT.md — nothing tells an agent what to do here",
                  scope=f"{run.name} / {folder.name}" if folder != run else run.name,
                  file=rel(folder))


def check_identity(r: Results, run: Path) -> None:
    path = run / "CLAUDE.md"
    text = read(path)
    if not text:
        r.add("identity.placeholder", "run has no CLAUDE.md — it has no identity",
              scope=run.name, file=rel(path))
        return

    hit = False
    for token in r.spec["placeholder_tokens"]:
        if token in text:
            hit = True
            r.add("identity.placeholder",
                  f"unfilled placeholder {token!r} — stages will run on a blank identity",
                  scope=run.name, file=rel(path), line=find_line(text, token))
    if not hit:
        r.ok("identity.placeholder")

    pipeline = pipeline_of(run, r.spec)
    if pipeline in r.spec.get("pipelines", {}):
        r.ok("identity.pipeline-unknown")
    else:
        r.add("identity.pipeline-unknown",
              f"Pipeline: {pipeline} — no such pipeline in _templates/ and checks.json",
              scope=run.name, file=rel(path), line=find_line(text, "Pipeline:"))

    upstream = upstream_of(run)
    if upstream:
        target = ROOT / upstream
        up_run = ROOT / upstream.split("/")[0]
        if target.is_file():
            r.ok("identity.upstream-missing")
        elif up_run.is_dir() and up_run != run:
            r.add("identity.upstream-not-run",
                  f"Upstream {upstream} does not exist yet — that stage has not run",
                  scope=run.name, file=rel(path), line=find_line(text, "Upstream:"))
        else:
            r.add("identity.upstream-missing",
                  f"Upstream {upstream} does not resolve — no such run or file",
                  scope=run.name, file=rel(path), line=find_line(text, "Upstream:"),
                  detail="Upstream is workspace-relative, e.g. `03-checkout-release/04_prd/output/prd.md`.")

    heading = r.spec["empty_promise_heading"]
    secs = sections(text)
    if heading in secs:
        line_no, body = secs[heading]
        substantive = [l for l in body.splitlines()
                       if l.strip() and not l.strip().startswith(">")]
        if not substantive:
            r.add("identity.empty-promise",
                  f"'{heading}' is present but empty — four stage contracts point here. "
                  "Fill it or delete the heading.",
                  scope=run.name, file=rel(path), line=line_no)
        else:
            r.ok("identity.empty-promise")
    else:
        r.ok("identity.empty-promise")


def check_pipeline_table(r: Results, run: Path, canonical: dict) -> None:
    """The run's CONTEXT.md stage table must agree with the canonical output map."""
    path = run / "CONTEXT.md"
    text = read(path)
    if not text:
        return
    seen = {}
    for i, line in enumerate(text.splitlines(), start=1):
        cells = [c.strip() for c in line.split("|")]
        stages = [c.strip("`") for c in cells if STAGE_RE.match(c.strip("`"))]
        if not stages:
            continue
        files = [c.strip("`") for c in cells if OUTFILE_RE.match(c.strip("`"))]
        if files:
            seen[stages[0]] = (i, files)

    for stage, (line_no, files) in seen.items():
        expected = canonical.get(stage, [])
        literal = [f for f in expected if "<" not in f]
        if not literal:
            continue
        if set(files) & set(literal):
            r.ok("contract.table-mismatch")
        else:
            r.add("contract.table-mismatch",
                  f"pipeline table says {stage} produces {files}, canonical map says {literal}",
                  scope=run.name, file=rel(path), line=line_no,
                  detail="Fix the table, or update canonical_outputs in _eval/checks.json if the "
                         "change is intended.")


def check_stage_contract(r: Results, run: Path, stage: str, canonical: dict,
                         tmpl_stages: list[str], base: Path | None = None) -> None:
    """
    `base` is where the contract's relative paths resolve from. A run sits at the workspace root, so
    for a run it is the run itself. A template sits one level deeper, in _templates/, but its
    contracts are written for the place they will be copied to — so it is checked as if it were a
    run at the root.
    """
    base = base or run
    scope = f"{run.name} / {stage}" if base == run else f"_templates/{run.name} / {stage}"
    path = run / stage / "CONTEXT.md"
    text = read(path)
    if not text:
        return
    secs = sections(text)

    # required sections
    for want in r.spec["required_sections"]:
        if any(h.lower().startswith(want.lower()) for h in secs):
            r.ok("contract.missing-section")
        else:
            r.add("contract.missing-section", f"no '## {want}' section",
                  scope=scope, file=rel(path),
                  detail="Every stage contract needs Inputs, Process, Outputs and a Human check. "
                         "A stage with no Outputs section leaves nothing behind.")

    inputs_body = next((b for h, (_, b) in secs.items() if h.lower().startswith("inputs")), "")
    outputs_key = next((h for h in secs if h.lower().startswith("outputs")), None)
    named, forbidden = split_inputs(inputs_body)

    # always-loaded references
    for must in r.spec["always_loaded"]:
        leaf = Path(must).name
        if any(leaf in n for n in named):
            r.ok("contract.always-loaded-missing")
        else:
            r.add("contract.always-loaded-missing",
                  f"Inputs does not name {must}, which every stage is supposed to load",
                  scope=scope, file=rel(path), line=secs.get("Inputs", (0, ""))[0])

    # input paths resolve
    for token in named:
        if token.startswith(tuple(r.spec["external_path_prefixes"])):
            r.add("contract.external-path", f"input points outside the workspace: {token}",
                  scope=scope, file=rel(path), line=find_line(text, token))
            continue
        if not token.startswith(("../", "_shared/")):
            continue
        target = (base / stage / token).resolve()
        if base != run and target.is_relative_to(base.resolve()):
            target = run / target.relative_to(base.resolve())  # inside the template itself
        if target.exists():
            r.ok("contract.input-unresolved")
            continue
        # a missing output file is normal; a missing stage folder is not
        m = re.match(r"\.\./(\d{2}_[a-z0-9-]+)/", token)
        if m:
            if m.group(1) not in tmpl_stages:
                r.add("contract.input-stage-missing",
                      f"input names stage {m.group(1)}, which is not a stage in this pipeline's template",
                      scope=scope, file=rel(path), line=find_line(text, token))
            elif (run / m.group(1)).exists():
                r.add("contract.upstream-not-run",
                      f"{token} not present — {m.group(1)} has not run",
                      scope=scope, file=rel(path), line=find_line(text, token))
            else:
                r.add("contract.input-stage-missing",
                      f"input names {m.group(1)}, which this run does not have",
                      scope=scope, file=rel(path), line=find_line(text, token))
        else:
            r.add("contract.input-unresolved", f"input path does not resolve: {token}",
                  scope=scope, file=rel(path), line=find_line(text, token))

    # Do NOT load must not contradict Inputs
    for bad in forbidden:
        stem = bad.rstrip("/")
        if any(n.startswith(stem) for n in named):
            r.add("contract.do-not-load-conflict",
                  f"{stem} appears in both Inputs and 'Do NOT load'",
                  scope=scope, file=rel(path), line=find_line(text, bad))
        else:
            r.ok("contract.do-not-load-conflict")

    # downstream agreement: an input citing another stage's output must use that stage's real filename
    for token in named:
        m = re.match(r"\.\./(\d{2}_[a-z0-9-]+)/output/([A-Za-z0-9_.-]+\.[a-z]+)$", token)
        if not m:
            continue
        up_stage, filename = m.group(1), m.group(2)
        expected = [f for f in canonical.get(up_stage, []) if "<" not in f]
        if not expected:
            continue
        if filename in expected:
            r.ok("contract.downstream-disagree")
        else:
            r.add("contract.downstream-disagree",
                  f"expects {up_stage}/output/{filename}, but {up_stage} produces {expected}",
                  scope=scope, file=rel(path), line=find_line(text, token),
                  detail="This is the break that silently stalls a pipeline: the upstream stage "
                         "writes one filename and the downstream contract asks for another.")

    # declared outputs
    if outputs_key is None:
        return
    line_no, out_body = secs[outputs_key]
    # a declared output is a filename this stage writes into its own output/ folder.
    # "../" paths are shared-layer appends; "." paths are destinations in another repo.
    declared = sorted({t for t in BACKTICK_RE.findall(out_body)
                       if OUTFILE_RE.match(t) and not t.startswith(("../", "."))})

    if not declared:
        r.add("contract.no-output-declared",
              "Outputs section names no file — a stage that leaves nothing behind breaks the chain",
              scope=scope, file=rel(path), line=line_no)
        return

    for want in canonical.get(stage, []):
        if want in declared or want in out_body:
            r.ok("contract.output-mismatch")
        else:
            r.add("contract.output-mismatch",
                  f"canonical output {want} is not declared in this stage's Outputs section",
                  scope=scope, file=rel(path), line=line_no,
                  detail=f"Declared here: {declared}")
    for got in declared:
        if got not in canonical.get(stage, []):
            r.add("contract.output-mismatch",
                  f"declares output {got}, which is not in the canonical map for {stage}",
                  scope=scope, file=rel(path), line=line_no,
                  detail="Either the contract drifted, or canonical_outputs in _eval/checks.json "
                         "needs updating.")


def check_drift(r: Results, run: Path, stage: str, pipeline: str) -> None:
    live = run / stage / "CONTEXT.md"
    tmpl = template_dir(r.spec, pipeline) / stage / "CONTEXT.md"
    if not (live.exists() and tmpl.exists()):
        return
    a, b = read(live), read(tmpl)
    if digest(a) == digest(b):
        r.ok("drift.template")
        return
    la, lb = norm(a).splitlines(), norm(b).splitlines()
    added = len([l for l in la if l not in lb])
    removed = len([l for l in lb if l not in la])
    r.add("drift.template",
          f"stage contract differs from _templates/{pipeline} (+{added} / -{removed} lines)",
          scope=f"{run.name} / {stage}", file=rel(live),
          detail="The workspace rule is: change the method in the template, never in a live run. "
                 "Port the change back, or accept it here.")


def check_order(r: Results, run: Path, stage: str, canonical: dict) -> None:
    """If this stage has produced output, its named upstream inputs should exist too."""
    outdir = run / stage / "output"
    produced = [p for p in outdir.iterdir() if p.is_file()] if outdir.is_dir() else []
    if not produced:
        return
    text = read(run / stage / "CONTEXT.md")
    named, _ = split_inputs(next((b for h, (_, b) in sections(text).items()
                                  if h.lower().startswith("inputs")), ""))
    missing = []
    for token in named:
        m = re.match(r"\.\./(\d{2}_[a-z0-9-]+)/output/([A-Za-z0-9_.-]+\.[a-z]+)$", token)
        if m and not (run / stage / token).exists():
            if "if complete" in text.split(token)[0].splitlines()[-1].lower():
                continue
            missing.append(token.replace("../", ""))
    if missing:
        r.add("order.out-of-sequence",
              f"{stage} has output, but these named inputs were never produced: {', '.join(missing)}",
              scope=f"{run.name} / {stage}", file=rel(run / stage),
              detail="Legal if deliberate (08 has an explicit carve-out). Suspicious otherwise — "
                     "the stage worked from something other than its declared inputs.")
    else:
        r.ok("order.out-of-sequence")


def check_terminals(r: Results) -> None:
    for name in all_terminal_folders(r.spec):
        folder = ROOT / name
        if not folder.is_dir():
            r.add("run.stage-missing", f"terminal folder missing: {name}",
                  scope="workspace", file=name)
            continue
        for required in ("CLAUDE.md", "CONTEXT.md"):
            if (folder / required).exists():
                r.ok("walk.entrypoint-missing")
            else:
                r.add("walk.entrypoint-missing", f"{name} has no {required}",
                      scope=name, file=f"{name}/{required}")


def check_engine_manifest(r: Results) -> None:
    """Engine files are read-only in an instance. Only runs where engine.manifest exists."""
    if not (ROOT / manifest_mod.MANIFEST).is_file():
        return
    problems = manifest_mod.check(ROOT)
    for rel_path, problem in problems:
        r.add("engine.edited", f"engine file {problem}: {rel_path}",
              scope="engine", file=rel_path,
              detail="In an instance: revert it (git checkout) and make the fix upstream in the engine, "
                     "then ./pull-engine.sh the new tag. In the engine itself: run "
                     "`python3 _eval/manifest.py build` before tagging.")
    if not problems:
        r.ok("engine.edited")


# ───────────────────────────────────────────────────────────── lineage

UPSTREAM_OUTPUT_RE = re.compile(r"^\.\./(\d{2}_[a-z0-9-]+)/output/([A-Za-z0-9_.-]+\.[a-z]+)$")
MTIME_SLACK = 2.0  # seconds; a checkout writes files in some order, so near-ties are not evidence


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def output_files(stage_dir: Path) -> list[Path]:
    out = stage_dir / "output"
    if not out.is_dir():
        return []
    return sorted(p for p in out.rglob("*")
                  if p.is_file() and p.name not in (".DS_Store", ".gitkeep"))


def stage_inputs(run: Path, stage: str) -> list[Path]:
    """
    The working files a stage output was built from: the same-run upstream outputs its contract
    names, plus the run's Upstream file when the contract's Inputs mention it. A contract that
    names the PRD digest reads the digest beside the Upstream file instead, when there is one.
    """
    text = read(run / stage / "CONTEXT.md")
    body = next((b for h, (_, b) in sections(text).items() if h.lower().startswith("inputs")), "")
    named, _ = split_inputs(body)
    found = []
    for token in named:
        if UPSTREAM_OUTPUT_RE.match(token):
            p = (run / stage / token).resolve()
            if p.is_file():
                found.append(p)
    upstream = upstream_of(run)
    if upstream and re.search(r"\bupstream\b", body, re.I) and (ROOT / upstream).is_file():
        target = (ROOT / upstream).resolve()
        digest_name = prd_digest_mod.config()["output"]
        if digest_name in body and target.with_name(digest_name).is_file():
            target = target.with_name(digest_name)
        found.append(target)
    return found


def matches_accept(key: str, accept: list[str]) -> bool:
    for a in accept:
        a = a.strip("/")
        if a and (key == a or key.startswith(a + "/")):
            return True
    return False


def check_lineage(r: Results, accept: list[str]) -> None:
    """
    Flag a stage output whose inputs changed after it was built.

    The ledger (checks.json `lineage_file`) records, per stage output, a hash of the output and of
    every input as they were when the output was first seen. Hashes, not timestamps, because a git
    checkout resets every timestamp. While the output is unchanged, any input whose hash moved makes
    the output stale. Re-running the stage or editing its output re-baselines it; so does
    `./eval --accept <run>[/<stage>]` once a person has checked it still holds.

    First sight has no recorded history, so it falls back to timestamps once: an input newer than
    the output is recorded as unknown, and stays stale until the output changes or is accepted.
    """
    ledger_path = ROOT / r.spec.get("lineage_file", "_eval/lineage.json")
    try:
        ledger = json.loads(read(ledger_path) or "{}")
    except json.JSONDecodeError:
        ledger = {}
    entries: dict = ledger.get("entries", {})
    before = json.dumps(entries, sort_keys=True)
    live_keys = set()

    for run in runs():
        for stage in stages_of(run):
            outs = output_files(run / stage)
            if not outs:
                continue
            key = f"{run.name}/{stage}"
            live_keys.add(key)
            out_hash = hashlib.sha256("".join(file_hash(p) for p in outs).encode()).hexdigest()[:16]
            inputs = {rel(p): file_hash(p) for p in stage_inputs(run, stage)}
            entry = entries.get(key)

            if entry is None or entry.get("output") != out_hash or matches_accept(key, accept):
                recorded = dict(inputs)
                if entry is None and not matches_accept(key, accept):
                    oldest_out = min(p.stat().st_mtime for p in outs)
                    for name in inputs:
                        if (ROOT / name).stat().st_mtime > oldest_out + MTIME_SLACK:
                            recorded[name] = "?"  # newer than the output on first sight
                entries[key] = {"output": out_hash, "inputs": recorded}
                entry = entries[key]

            stale = []
            for name, h in inputs.items():
                was = entry["inputs"].get(name)
                if was is None:
                    entry["inputs"][name] = h  # input appeared after the output; nothing to compare
                elif was != h:
                    stale.append(name)
            if stale:
                r.add("lineage.stale",
                      f"{stage} output was built on an older version of {', '.join(stale)}",
                      scope=run.name, file=rel(run / stage / "output"),
                      detail="Re-run the stage, or edit its output to match. If you have checked "
                             f"it still holds: ./eval --accept {key}")
            else:
                r.ok("lineage.stale")

    for gone in set(entries) - live_keys:
        del entries[gone]
    if json.dumps(entries, sort_keys=True) != before and (entries or ledger_path.exists()):
        ledger_path.write_text(json.dumps({"version": 1, "entries": entries},
                                          indent=1, sort_keys=True) + "\n", encoding="utf-8")


def run_structure(r: Results, accept: list[str] | None = None) -> None:
    check_engine_manifest(r)
    check_walk(r)
    check_shared_references(r)
    check_terminals(r)
    check_templates(r)

    # each template is checked as a run for contract purposes, resolved as if it sat at the root
    for tdir in template_folders(r.spec):
        name = tdir.name
        if name not in r.spec.get("pipelines", {}):
            continue
        canonical = pipeline_spec(r.spec, name).get("canonical_outputs", {})
        stages = template_stages(r.spec, name)
        check_pipeline_table(r, tdir, canonical)
        for stage in stages_of(tdir):
            check_stage_contract(r, tdir, stage, canonical, stages, base=ROOT / name)

    for run in runs():
        pipeline = pipeline_of(run, r.spec)
        check_identity(r, run)
        if pipeline not in r.spec.get("pipelines", {}):
            continue  # identity.pipeline-unknown already says why; nothing to compare against
        canonical = pipeline_spec(r.spec, pipeline).get("canonical_outputs", {})
        stages = template_stages(r.spec, pipeline)
        check_run_shape(r, run, stages, pipeline)
        check_pipeline_table(r, run, canonical)
        for stage in stages_of(run):
            check_stage_contract(r, run, stage, canonical, stages)
            check_drift(r, run, stage, pipeline)
            check_order(r, run, stage, canonical)

    check_prd_digests(r)
    check_lineage(r, accept or [])


def check_prd_digests(r: Results) -> None:
    """
    A release PRD's digest must match the PRD it was built from: feature runs read the digest, not
    the PRD. Also re-digests the engine's synthetic fixture and compares it with the expected file,
    so a parser change that alters the output is caught. Making the digest is `./digest`, not this.
    """
    cfg = prd_digest_mod.config()
    fixture = ROOT / r.spec.get("prd_digest_fixture", "")
    if r.spec.get("prd_digest_fixture") and (fixture / "prd.md").is_file() \
            and (fixture / "expected-digest.md").is_file():
        got = prd_digest_mod.build(read(fixture / "prd.md"), prd_digest_mod.load_config(house=False))
        if norm(got) == norm(read(fixture / "expected-digest.md")):
            r.ok("prd.digest-fixture")
        else:
            r.add("prd.digest-fixture", "the digest of the synthetic fixture PRD no longer matches "
                  "expected-digest.md", file=rel(fixture),
                  detail="The parser changed. If the new output is right, regenerate it: "
                         f"./digest --file {rel(fixture / 'prd.md')} --generic "
                         f"--out {rel(fixture / 'expected-digest.md')}")

    for run in runs():
        src = run / cfg["stage"] / "output" / cfg["source"]
        if not src.is_file():
            continue
        out = src.with_name(cfg["output"])
        fix = f"./digest {run.name}"
        if not out.is_file():
            r.add("prd.digest-missing", f"{cfg['stage']} has {cfg['source']} but no {cfg['output']}",
                  scope=run.name, file=rel(src.parent),
                  detail=f"Feature runs read the digest, not the PRD. Run: {fix}")
        elif prd_digest_mod.is_stale(src, out):
            r.add("prd.digest-stale", f"digest stale — {cfg['source']} changed after {cfg['output']} "
                  "was written", scope=run.name, file=rel(out), detail=f"Run: {fix}")
        else:
            r.ok("prd.digest-stale")


# ───────────────────────────────────────────────────────────── PRD checks

def run_prd(r: Results, only: Path | None = None) -> None:
    """
    `./eval prd [run]`: the mechanical half of the Ready bar, on each release and feature PRD.
    Pointers land, IDs are unique and exist, values come from the house lists, no template text
    survives. `warn` while the PRD's Status is Draft, `fail` once it says Ready. Checks are in
    `prd_checks.py`; which file each pipeline's PRD is, in checks.json `prd_checks`.
    """
    cfg = prd_digest_mod.config()
    pc = r.spec.get("prd_checks", {})
    docs = pc.get("documents", {})
    allowed = prd_checks_mod.house(cfg)
    missing = [k for k in prd_checks_mod.VOCAB if k not in allowed]
    if missing:
        r.add("prd.vocab-missing", "no house value list for " + ", ".join(missing)
              + " — those vocabulary checks were skipped", layer="prd", file=cfg["rules_file"],
              detail="Add the keys to the ```prd-rules block, as comma-separated lists.")
    ready_rx = re.compile(pc.get("ready_status", r"^ready\b"), re.I)
    exempt = set(pc.get("ready_exempt", []))

    prds = {run: run / docs[pipeline_of(run, r.spec)] for run in runs()
            if pipeline_of(run, r.spec) in docs}
    prds = {run: path for run, path in prds.items() if path.is_file()}
    checked = 0
    for run, path in prds.items():
        if only is not None and run != only:
            continue
        upstream = ROOT / upstream_of(run) if upstream_of(run) else None
        parent = read(upstream) if upstream and upstream.is_file() else ""
        children = [read(p) for c, p in prds.items()
                    if upstream_of(c) and (ROOT / upstream_of(c)).resolve() == path.resolve()]
        status, issues = prd_checks_mod.check(
            read(path), cfg, allowed,
            parent_digest=prd_digest_mod.build(parent, cfg) if parent else None,
            parent_name=upstream_of(run), children=children)
        ready = bool(ready_rx.search(status))
        for i in issues:
            sev = r.spec["severities"].get(i.check, "warn")
            if ready and sev == "warn" and i.check not in exempt:
                sev = "fail"
            r.add(i.check, i.message, layer="prd", scope=run.name, file=rel(path), line=i.line,
                  detail=i.detail, severity=sev)
        if not issues:
            r.ok("prd.checks")
        checked += 1
    if not checked:
        r.add("prd.none", "no PRD to check" + (f" in {only.name}" if only else ""), layer="prd",
              severity="info")


# ───────────────────────────────────────────────────────────── behavioural layer

def claude_cli() -> str | None:
    return shutil.which("claude")


DEFAULT_CASE_ROOTS = ["_eval/fixtures", "_eval/cases"]


def is_case(path: Path) -> bool:
    """A case is a folder holding run/ (identity) and/or seed/ (upstream outputs per stage)."""
    return (path / "run").is_dir() or (path / "seed").is_dir()


def case_dirs(spec: dict, only: list[str] | None = None) -> list[Path]:
    """
    Behaviour cases, from checks.json `case_roots` (workspace-relative). Each root is either a case
    itself or a folder of cases. Engine fixtures are synthetic; instance cases are frozen real runs.
    `only` filters by case folder name or workspace-relative path.
    """
    found: list[Path] = []
    for root in spec.get("case_roots") or DEFAULT_CASE_ROOTS:
        p = ROOT / root
        if not p.is_dir():
            continue
        if is_case(p):
            found.append(p)
        else:
            found += sorted(c for c in p.iterdir() if c.is_dir() and is_case(c))
    if only:
        found = [c for c in found if c.name in only or rel(c) in only]
    return found


def case_pipeline(case: Path, spec: dict) -> str:
    return pipeline_of(case / "run", spec)


def case_stages(case: Path, spec: dict, requested: list[str]) -> list[str]:
    """The stages to test for one case: those requested that its pipeline has, else its defaults."""
    pipeline = case_pipeline(case, spec)
    if requested:
        return [s for s in requested if s in template_stages(spec, pipeline)]
    return list(pipeline_spec(spec, pipeline).get("behaviour_stages", []))


def build_scratch(stage: str, spec: dict, case: Path) -> Path:
    """Materialise a throwaway run containing the case identity and seeded upstream outputs."""
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    shutil.copytree(template_dir(spec, case_pipeline(case, spec)), SCRATCH)
    for name in ("CLAUDE.md", "CONTEXT.md"):
        src = case / "run" / name
        if src.exists():
            shutil.copy(src, SCRATCH / name)
    seed = case / "seed"
    if seed.is_dir():
        for stage_dir in seed.iterdir():
            if not stage_dir.is_dir():
                continue
            dest = SCRATCH / stage_dir.name / "output"
            dest.mkdir(parents=True, exist_ok=True)
            for f in stage_dir.iterdir():
                if f.is_file():
                    shutil.copy(f, dest / f.name)
    # the stage under test starts empty
    target = SCRATCH / stage / "output"
    if target.is_dir():
        for f in target.iterdir():
            if f.is_file():
                f.unlink()
    return SCRATCH


def stream_reads(raw: str) -> list[str]:
    """Pull file paths the agent read out of stream-json output."""
    hits: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue
        blocks = (evt.get("message") or {}).get("content") or []
        if isinstance(blocks, str):
            continue
        for block in blocks:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            inp = block.get("input") or {}
            for key in ("file_path", "path", "pattern", "command", "notebook_path"):
                val = inp.get(key)
                if isinstance(val, str):
                    hits.append(val)
    return hits


def invoke(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timed out after {timeout}s"
    except FileNotFoundError as e:
        return 127, "", str(e)


def grade(rubric_md: str, produced: str, cli: str, timeout: int) -> tuple[list[dict], str]:
    prompt = (
        "You are grading one stage output from a product-discovery pipeline against a rubric.\n"
        "Be strict. A plausible-sounding document that does not meet a criterion fails it.\n\n"
        "=== RUBRIC ===\n" + rubric_md +
        "\n\n=== OUTPUT UNDER TEST ===\n" + produced[:60000] +
        "\n\n=== RESPOND ===\n"
        "Reply with JSON only, no prose, no code fence:\n"
        '{"checks":[{"id":"<rubric id>","verdict":"pass|fail","evidence":"<one sentence, quote the output>"}]}'
    )
    code, out, err = invoke([cli, "-p", prompt, "--output-format", "json"], ROOT, timeout)
    if code != 0:
        return [], err or out or f"grader exited {code}"
    try:
        body = json.loads(out)
        text = body.get("result", out) if isinstance(body, dict) else out
    except json.JSONDecodeError:
        text = out
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return [], "grader did not return JSON"
    try:
        return json.loads(m.group(0)).get("checks", []), ""
    except json.JSONDecodeError as e:
        return [], f"unparseable grader JSON: {e}"


def grade_stage(r: Results, pipeline: str, stage: str, produced: str, scope: str, cli: str | None,
                grader: str, timeout: int, layer: str = "behaviour") -> None:
    """
    Route each rubric criterion to a grader.

    Criteria tagged '{local}' in the rubric are mechanical enough for a small local model.
    The rest are judgement calls and go to the strong model. `grader` picks the policy:
      auto   — local does its share, the strong model does the rest (default)
      local  — local only; judgement criteria are reported ungraded rather than guessed at
      claude — everything to the strong model
    """
    rubric = EVAL_DIR / "rubrics" / pipeline / f"{stage}.md"
    rubric_rel = f"rubrics/{pipeline}/{stage}.md"
    if not rubric.exists():
        r.add("behaviour.error", f"no rubric at {rubric_rel} — output quality not graded",
              layer=layer, scope=scope, severity="info")
        return

    local_ids, strong_ids, local_md, strong_md = local_mod.split_rubric(read(rubric))
    cfg = {**local_mod.DEFAULTS, **r.spec.get("local", {})}
    verdicts: list[tuple[dict, str]] = []

    if grader in ("auto", "local") and local_ids:
        checks, err = local_mod.grade_local(cfg, local_md, produced, local_ids)
        if err:
            r.add("behaviour.error", f"local grader: {err}", layer=layer, scope=scope,
                  severity="warn" if grader == "auto" else "fail",
                  detail="Run `./eval doctor` to check the local model. With --grader auto the "
                         "strong model can still cover these criteria.")
            if grader == "auto":
                strong_ids = sorted(set(strong_ids) | set(local_ids))
                strong_md = read(rubric)
        else:
            verdicts += [(c, cfg.get("grader_model") or cfg.get("model", "local"))
                         for c in checks]

    if grader == "local":
        for cid in strong_ids:
            r.add("behaviour.rubric-ungraded",
                  f"{cid} — judgement criterion, not graded locally",
                  layer=layer, scope=scope, file=rubric_rel,
                  detail="Tag it {local} in the rubric if you think a small model can judge it, "
                         "or run ./eval all to have the strong model grade it.")
    elif strong_ids:
        if not cli:
            r.add("behaviour.error", "no `claude` CLI, so judgement criteria went ungraded",
                  layer=layer, scope=scope)
        else:
            md = strong_md if grader == "auto" else read(rubric)
            checks, err = grade(md, produced, cli, timeout)
            if err:
                r.add("behaviour.error", f"strong grader: {err}", layer=layer, scope=scope)
            else:
                verdicts += [(c, "claude") for c in checks]

    for c, who in verdicts:
        verdict = str(c.get("verdict", "")).lower()
        if verdict == "pass":
            r.ok("behaviour.rubric")
        elif verdict == "unknown":
            r.add("behaviour.rubric-ungraded",
                  f"{c.get('id', '?')} — {c.get('evidence', 'no verdict returned')}",
                  layer=layer, scope=scope, file=rubric_rel)
        else:
            r.add("behaviour.rubric", f"{c.get('id', '?')} — {c.get('evidence', '')}",
                  layer=layer, scope=scope, file=rubric_rel,
                  detail=f"graded by: {who}")


def run_behaviour(r: Results, requested: list[str], do_grade: bool, timeout: int,
                  keep: bool, grader: str = "auto", cases: list[Path] | None = None) -> None:
    """`requested` filters stages; empty means each case's pipeline's behaviour_stages."""
    cli = claude_cli()
    if not cli:
        r.add("behaviour.error",
              "the `claude` CLI is not on PATH, so no stage could be run headless",
              layer="behaviour", scope="workspace",
              detail="Install it (npm i -g @anthropic-ai/claude-code) and re-run, or use "
                     "`./eval behaviour --manual` to print a run sheet you can work through by hand.")
        return

    cases = cases if cases is not None else case_dirs(r.spec)
    if not cases:
        r.add("behaviour.error", "no eval cases found — check `case_roots` in _eval/checks.json",
              layer="behaviour", scope="workspace")
        return
    pairs = [(c, s) for c in cases for s in case_stages(c, r.spec, requested)]
    if not pairs:
        r.add("behaviour.error", "no stage to test — no case's pipeline has the requested stages",
              layer="behaviour", scope="workspace", severity="warn")
    for case, stage in pairs:
        scope = f"{rel(case)} / {stage}"
        pipeline = case_pipeline(case, r.spec)
        canonical = pipeline_spec(r.spec, pipeline).get("canonical_outputs", {})
        build_scratch(stage, r.spec, case)
        contract = read(SCRATCH / stage / "CONTEXT.md")
        named, forbidden = split_inputs(
            next((b for h, (_, b) in sections(contract).items()
                  if h.lower().startswith("inputs")), ""))

        t0 = time.time()
        code, out, err = invoke(
            [cli, "-p", f"work {SCRATCH.name}/{stage}",
             "--permission-mode", "acceptEdits",
             "--output-format", "stream-json", "--verbose"],
            ROOT, timeout)
        elapsed = round(time.time() - t0, 1)

        if code != 0:
            r.add("behaviour.error", f"headless run failed (exit {code}) after {elapsed}s",
                  layer="behaviour", scope=scope, detail=(err or out)[-1500:])
            continue

        reads = stream_reads(out)

        # mechanics 1 — declared output written and not empty
        wanted = [f for f in canonical.get(stage, []) if "<" not in f]
        produced_text = ""
        for filename in wanted:
            path = SCRATCH / stage / "output" / filename
            if not path.exists():
                r.add("behaviour.output-missing",
                      f"stage ran for {elapsed}s but never wrote output/{filename}",
                      layer="behaviour", scope=scope,
                      detail="The stage contract's Outputs section is not being honoured.")
                continue
            body = read(path)
            if len(body.strip()) < 200:
                r.add("behaviour.output-empty",
                      f"output/{filename} is {len(body.strip())} chars — effectively empty",
                      layer="behaviour", scope=scope)
            else:
                r.ok("behaviour.output-missing")
                produced_text += f"\n\n---- {filename} ----\n{body}"

        # mechanics 2 — forbidden stages not read
        for bad in forbidden:
            stem = bad.strip("/").replace("../", "")
            if not stem:
                continue
            # note: exclude the eval's own tooling dir, but NOT _eval-scratch, which is the run
            offenders = [x for x in reads if stem in x and "/_eval/" not in x]
            if offenders:
                r.add("behaviour.forbidden-read",
                      f"contract says do not load {stem}, but the run touched it",
                      layer="behaviour", scope=scope,
                      detail="\n".join(sorted(set(offenders))[:8]))
            else:
                r.ok("behaviour.forbidden-read")

        # mechanics 3 — named inputs actually read
        for token in named:
            leaf = Path(token).name
            if not leaf.endswith(".md"):
                continue
            if not (SCRATCH / stage / token).exists():
                continue
            if any(leaf in x for x in reads):
                r.ok("behaviour.input-not-read")
            else:
                r.add("behaviour.input-not-read",
                      f"named input {leaf} was never read",
                      layer="behaviour", scope=scope,
                      detail="Either the contract names an input the stage does not need, or the "
                             "stage is working from less than it claims to.")

        # judgement — rubric
        if do_grade and produced_text.strip():
            grade_stage(r, pipeline, stage, produced_text, scope, cli, grader, timeout)

    if SCRATCH.exists() and not keep:
        shutil.rmtree(SCRATCH)


def run_legibility(r: Results, requested: list[str], keep: bool) -> None:
    """
    Is each contract mechanically unambiguous? A small local model runs the stage; we check only
    whether it could find its inputs, honour its exclusions, and write the declared output.

    Mechanics only, deliberately. The local model is not asked to grade what it just wrote —
    self-marking is not evidence. Rubric grading belongs to the behavioural layer, where the stage
    was run by a different model.

    This is not a cheap behavioural run. It says nothing about quality of thinking. Findings are
    warnings, because a local model failing is ambiguous evidence — the transcript is attached so
    you can tell whether the contract or the model was at fault.
    """
    cfg = {**local_mod.DEFAULTS, **r.spec.get("local", {})}
    if not cfg.get("model"):
        r.add("legibility.error", "no local model configured — run `./eval doctor` first",
              layer="legibility", scope="workspace", severity="fail")
        return

    cases = case_dirs(r.spec)
    if not cases:
        r.add("legibility.error", "no eval cases found — check `case_roots` in _eval/checks.json",
              layer="legibility", scope="workspace", severity="fail")
        return
    # legibility tests the contract, not the thinking — one case per pipeline is enough
    first: dict[str, Path] = {}
    for c in cases:
        first.setdefault(case_pipeline(c, r.spec), c)
    pairs = [(c, s) for c in first.values() for s in case_stages(c, r.spec, requested)]
    for case, stage in pairs:
        pipeline = case_pipeline(case, r.spec)
        canonical = pipeline_spec(r.spec, pipeline).get("canonical_outputs", {})
        scope = f"legibility / {pipeline} / {stage}"

        build_scratch(stage, r.spec, case)
        contract = read(SCRATCH / stage / "CONTEXT.md")
        named, forbidden = split_inputs(
            next((b for h, (_, b) in sections(contract).items()
                  if h.lower().startswith("inputs")), ""))

        t0 = time.time()
        res = local_mod.run_stage(cfg, ROOT, f"{SCRATCH.name}/{stage}")
        elapsed = round(time.time() - t0, 1)
        tail = "\n".join(res["transcript"][-14:])

        if res["error"]:
            r.add("legibility.error", f"local run failed: {res['error']}",
                  layer="legibility", scope=scope, severity="fail", detail=tail)
            continue

        if res["stalled"]:
            r.add("legibility.stalled",
                  f"hit the {cfg['max_turns']}-turn cap after {elapsed}s without finishing",
                  layer="legibility", scope=scope, detail=tail)

        # did it write the declared output, in the declared place?
        wanted = [f for f in canonical.get(stage, []) if "<" not in f]
        expected_dir = (SCRATCH / stage / "output").resolve()
        produced_text = ""
        for filename in wanted:
            path = expected_dir / filename
            if path.exists():
                body = read(path)
                if len(body.strip()) < 200:
                    r.add("legibility.output-thin",
                          f"wrote output/{filename} but only {len(body.strip())} chars",
                          layer="legibility", scope=scope,
                          detail="Enough to show the path was understood; too little to grade.")
                else:
                    r.ok("legibility.output-missing")
                    produced_text += f"\n\n---- {filename} ----\n{body}"
                continue

            stray = [w for w in res["writes"] if Path(w).name == filename]
            if stray:
                r.add("legibility.wrong-path",
                      f"wrote {filename} to the wrong place — the contract's output path is ambiguous",
                      layer="legibility", scope=scope,
                      detail="wrote: " + "\n".join(stray) + f"\nexpected: {rel(expected_dir)}/")
            else:
                r.add("legibility.output-missing",
                      f"never wrote output/{filename} ({res['turns']} turns, {elapsed}s)",
                      layer="legibility", scope=scope,
                      detail=(tail or "no tool calls at all") +
                             "\n\nIf the transcript shows it hunting for inputs, the contract's "
                             "Inputs paths are unclear. If it never called a tool, that is the "
                             "model, not the contract.")

        # exclusions honoured?
        for bad in forbidden:
            stem = bad.strip("/").replace("../", "")
            if not stem:
                continue
            offenders = [x for x in res["reads"] if stem in x and "/_eval/" not in x]
            if offenders:
                r.add("legibility.forbidden-read",
                      f"read {stem}, which the contract excludes — the exclusion is not landing",
                      layer="legibility", scope=scope,
                      detail="\n".join(sorted(set(offenders))[:8]))
            else:
                r.ok("legibility.forbidden-read")

        # inputs findable?
        for token in named:
            leaf = Path(token).name
            if not leaf.endswith(".md") or not (SCRATCH / stage / token).exists():
                continue
            if any(leaf in x for x in res["reads"]):
                r.ok("legibility.input-not-read")
            else:
                r.add("legibility.input-not-read",
                      f"never found named input {leaf}",
                      layer="legibility", scope=scope,
                      detail="Check the relative path in the Inputs list resolves from the stage "
                             "folder as written.")

        if produced_text.strip():
            r.add("legibility.ok",
                  f"contract executed cleanly by {cfg['model']} in {res['turns']} turns "
                  f"({elapsed}s) — mechanically unambiguous",
                  layer="legibility", scope=scope,
                  detail="Not a quality signal. Run ./eval behaviour to judge the thinking.")

    if SCRATCH.exists() and not keep:
        shutil.rmtree(SCRATCH)


def doctor(spec: dict) -> int:
    cfg = {**local_mod.DEFAULTS, **spec.get("local", {})}
    print()
    print(paint("  local model check", "bold"))
    print(f"  {paint(cfg['base_url'], 'dim')}\n")

    info = local_mod.probe(cfg)
    if not info["reachable"]:
        print(f"  {paint('✗', 'fail')} Ollama unreachable")
        for n in info["notes"]:
            print(f"    {n}")
        print(f"\n  Start it with {paint('ollama serve', 'bold')}, then re-run.\n")
        return 1

    print(f"  {paint('✓', 'pass')} reachable · {len(info['models'])} model(s) installed")
    for m in info["models"]:
        mark = paint("→", "pass") if m == info["chosen"] else " "
        print(f"    {mark} {m}")
    if not info["chosen"]:
        print(f"\n  {paint('✗', 'fail')} no usable model\n")
        return 1

    rows = [("JSON mode (needed for grading)", info["json"]),
            ("tool calling (needed for legibility)", info["tools"])]
    print()
    for label, ok in rows:
        icon = paint("✓", "pass") if ok else paint("✗", "fail")
        print(f"  {icon} {label}")
    if info.get("declared_capabilities"):
        print(f"    {paint('declared: ' + ', '.join(info['declared_capabilities']), 'dim')}")
    for n in info["notes"]:
        print(f"    {paint(n, 'dim')}")

    # persist the choice
    path = EVAL_DIR / "checks.json"
    raw = json.loads(read(path))
    raw.setdefault("local", {})
    raw["local"]["model"] = info["chosen"]
    raw["local"]["grader_model"] = info["chosen"]
    path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")

    print(f"\n  saved to _eval/checks.json → local.model = {paint(info['chosen'], 'bold')}")
    print()
    if info["json"]:
        print(f"  {paint('./eval all --grader auto', 'bold')}   local grades the mechanical "
              f"criteria, Claude the judgement ones")
    if info["tools"]:
        print(f"  {paint('./eval legibility', 'bold')}          free — are the contracts "
              f"unambiguous enough to execute?")
    if not info["tools"]:
        print(f"  {paint('note', 'warn')}: this model did not emit a tool call, so the "
              f"legibility tier will not work.")
        print(f"        Try a larger tag: {paint('ollama pull qwen2.5:14b', 'bold')}")
    print()
    return 0


def manual_sheet(spec: dict, requested: list[str], cases: list[Path] | None = None) -> Path:
    cases = cases if cases is not None else case_dirs(spec)
    lines = ["# Behavioural eval — manual run sheet", "",
             "The `claude` CLI was not available, so run these by hand.",
             "Fresh session per stage, always from the workspace root.", ""]
    for case_path, stage in ((c, s) for c in cases for s in case_stages(c, spec, requested)):
        case = rel(case_path)
        pipeline = case_pipeline(case_path, spec)
        tdir = rel(template_dir(spec, pipeline))
        outputs = pipeline_spec(spec, pipeline).get("canonical_outputs", {}).get(stage, [])
        rubric = EVAL_DIR / "rubrics" / pipeline / f"{stage}.md"
        lines += [f"## {pipeline} / {stage} — case `{case}`", "",
                  f"1. `cp -R {tdir} _eval-scratch` then copy `{case}/run/CLAUDE.md` over it,",
                  f"   and seed upstream outputs from `{case}/seed/`.",
                  f"2. New session, from the root: `work _eval-scratch/{stage}`",
                  f"3. Expect `_eval-scratch/{stage}/output/{', '.join(outputs)}`", ""]
        if rubric.exists():
            lines += ["Grade against:", "", read(rubric), ""]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "manual-run-sheet.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ───────────────────────────────────────────────────────────── report

def load_history() -> list[dict]:
    path = REPORT_DIR / "history.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def write_report(r: Results, layers: list[str], duration: float) -> tuple[Path, dict | None]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    history = load_history()
    previous = next((h for h in reversed(history) if h.get("layers") == layers), None)

    payload = {
        "generated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "root": ROOT.name,
        "layers": layers,
        "duration": round(duration, 2),
        "counts": r.counts,
        "blocking": r.blocking,
        "findings": [asdict(f) for f in r.findings],
        "coverage": r.passed_checks,
    }

    (REPORT_DIR / "results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with (REPORT_DIR / "history.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({k: payload[k] for k in
                             ("generated", "layers", "counts", "blocking", "duration")}) + "\n")

    html = HTML_TEMPLATE.replace("__PAYLOAD__", json.dumps(payload)) \
                        .replace("__PREVIOUS__", json.dumps(previous)) \
                        .replace("__HISTORY__", json.dumps(history[-20:]))
    path = REPORT_DIR / "index.html"
    path.write_text(html, encoding="utf-8")
    return path, previous


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Workspace eval</title>
<style>
:root{
  --bg:#fbfaf8; --panel:#fff; --ink:#16161a; --muted:#6c6c78; --line:#e6e3dd;
  --fail:#c0392b; --warn:#b5761b; --info:#4a6f9c; --pass:#2f7d4f;
  --fail-bg:#fdf1ef; --warn-bg:#fdf7ec; --info-bg:#f1f5fa; --pass-bg:#f0f7f2;
  --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#141416; --panel:#1c1c1f; --ink:#ececee; --muted:#9a9aa6; --line:#2e2e33;
  --fail:#ff7b6b; --warn:#e3ad52; --info:#84b0e0; --pass:#6ec78f;
  --fail-bg:#2a1c1a; --warn-bg:#26200f; --info-bg:#17202b; --pass-bg:#152018;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.5 ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
.wrap{max-width:1000px;margin:0 auto;padding:32px 16px 80px}
h1{font-size:22px;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:13px;margin-bottom:24px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:8px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}
.card .n{font-size:26px;font-weight:650;letter-spacing:-.02em;line-height:1}
.card .l{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin-top:6px}
.card.fail .n{color:var(--fail)}.card.warn .n{color:var(--warn)}
.card.info .n{color:var(--info)}.card.pass .n{color:var(--pass)}
.delta{font-size:11px;margin-top:4px;color:var(--muted)}
.verdict{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--pass);
  border-radius:10px;padding:14px 16px;margin:14px 0 22px;font-weight:550}
.verdict.bad{border-left-color:var(--fail)}
.verdict small{display:block;font-weight:400;color:var(--muted);margin-top:4px;font-size:12.5px}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:18px}
button.chip{font:inherit;font-size:12.5px;padding:5px 11px;border-radius:999px;cursor:pointer;
  border:1px solid var(--line);background:var(--panel);color:var(--muted)}
button.chip[aria-pressed="true"]{border-color:currentColor;font-weight:600}
button.chip.fail[aria-pressed="true"]{color:var(--fail);background:var(--fail-bg)}
button.chip.warn[aria-pressed="true"]{color:var(--warn);background:var(--warn-bg)}
button.chip.info[aria-pressed="true"]{color:var(--info);background:var(--info-bg)}
input[type=search]{flex:1;min-width:180px;font:inherit;font-size:13px;padding:6px 11px;
  border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}
.group{background:var(--panel);border:1px solid var(--line);border-radius:10px;margin-bottom:12px;
  overflow:hidden}
.group>summary{cursor:pointer;padding:12px 16px;font-weight:600;font-size:14px;display:flex;
  justify-content:space-between;gap:10px;align-items:center;list-style:none}
.group>summary::-webkit-details-marker{display:none}
.group>summary::before{content:"▸";color:var(--muted);font-size:11px;margin-right:2px}
.group[open]>summary::before{content:"▾"}
.gname{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pills{display:flex;gap:5px;flex-shrink:0}
.pill{font-size:11px;font-weight:650;padding:2px 7px;border-radius:5px}
.pill.fail{color:var(--fail);background:var(--fail-bg)}
.pill.warn{color:var(--warn);background:var(--warn-bg)}
.pill.info{color:var(--info);background:var(--info-bg)}
.f{border-top:1px solid var(--line);padding:12px 16px 12px 20px;border-left:3px solid transparent}
.f.fail{border-left-color:var(--fail)}.f.warn{border-left-color:var(--warn)}
.f.info{border-left-color:var(--info)}
.f.ignored{opacity:.55}
.fh{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.cid{font:12px var(--mono);color:var(--muted)}
.msg{flex:1;min-width:200px;font-size:14px}
.loc{font:11.5px var(--mono);color:var(--muted);margin-top:5px;word-break:break-all}
.det{font-size:13px;color:var(--muted);margin-top:7px;padding-left:10px;
  border-left:2px solid var(--line);white-space:pre-wrap;font-family:var(--mono);font-size:12px}
.empty{text-align:center;color:var(--muted);padding:44px 16px;font-size:14px}
.trend{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;
  margin-top:26px}
.trend h2{font-size:13px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:0 0 12px}
.trend table{width:100%;border-collapse:collapse;font-size:12.5px}
.trend td,.trend th{text-align:left;padding:4px 8px 4px 0;border-bottom:1px solid var(--line)}
.trend th{color:var(--muted);font-weight:500;font-size:11px;text-transform:uppercase;letter-spacing:.05em}
.trend td:first-child{font-family:var(--mono);font-size:11.5px;color:var(--muted)}
footer{color:var(--muted);font-size:12px;margin-top:26px;line-height:1.7}
code{font:12px var(--mono);background:var(--info-bg);padding:1px 5px;border-radius:4px}
</style></head><body><div class="wrap">
<h1>Workspace eval</h1>
<div class="sub" id="sub"></div>
<div class="cards" id="cards"></div>
<div class="verdict" id="verdict"></div>
<div class="bar">
  <button class="chip fail" data-sev="fail" aria-pressed="true">Fail</button>
  <button class="chip warn" data-sev="warn" aria-pressed="true">Warn</button>
  <button class="chip info" data-sev="info" aria-pressed="false">Info</button>
  <input type="search" id="q" placeholder="Filter by run, stage, file or message…">
</div>
<div id="list"></div>
<div class="trend" id="trend"></div>
<footer>
Checks are defined in <code>_eval/checks.json</code>; rubrics in <code>_eval/rubrics/</code>.<br>
Re-run with <code>./eval</code> (structure only, no tokens) or <code>./eval all</code> (adds the graded behavioural layer).
</footer>
</div>
<script>
const D=__PAYLOAD__, PREV=__PREVIOUS__, HIST=__HISTORY__;
const SEV=["fail","warn","info"];
const state={sev:new Set(["fail","warn"]),q:""};

function delta(k){
  if(!PREV) return "";
  const d=D.counts[k]-PREV.counts[k];
  if(d===0) return "no change";
  return (d>0?"▲ +":"▼ ")+d+" vs last run";
}
document.getElementById("sub").textContent =
  D.generated.replace("T"," ").slice(0,16)+" · "+D.layers.join(" + ")+" · "+D.duration+"s";

document.getElementById("cards").innerHTML =
  [["fail","Failures"],["warn","Warnings"],["info","Notes"],["pass","Checks passed"]]
  .map(([k,l])=>`<div class="card ${k}"><div class="n">${D.counts[k]}</div>
    <div class="l">${l}</div><div class="delta">${delta(k)}</div></div>`).join("");

const v=document.getElementById("verdict");
if(D.blocking===0){
  v.innerHTML="Contracts hold."+
    "<small>No blocking failures. The folders will do what they say they do.</small>";
}else{
  v.classList.add("bad");
  v.innerHTML=D.blocking+" blocking failure"+(D.blocking===1?"":"s")+"."+
    "<small>A stage will mislead or stall an agent until these are fixed. Start at the top.</small>";
}

function render(){
  const rows=D.findings.filter(f=>state.sev.has(f.severity)).filter(f=>{
    if(!state.q) return true;
    const q=state.q.toLowerCase();
    return (f.scope+f.file+f.message+f.check+f.detail).toLowerCase().includes(q);
  });
  const list=document.getElementById("list");
  if(!rows.length){
    list.innerHTML='<div class="empty">Nothing matches. '+
      (state.sev.has("info")?"":"Try enabling Notes.")+'</div>';
    return;
  }
  const groups=new Map();
  for(const f of rows){
    const key=(f.layer==="behaviour"?"behaviour · ":"")+(f.scope||"workspace");
    if(!groups.has(key)) groups.set(key,[]);
    groups.get(key).push(f);
  }
  const order=[...groups.entries()].sort((a,b)=>{
    const s=x=>Math.min(...x[1].map(f=>SEV.indexOf(f.severity)));
    return s(a)-s(b)||a[0].localeCompare(b[0]);
  });
  list.innerHTML=order.map(([name,fs])=>{
    const c={};SEV.forEach(s=>c[s]=fs.filter(f=>f.severity===s).length);
    const pills=SEV.filter(s=>c[s]).map(s=>`<span class="pill ${s}">${c[s]}</span>`).join("");
    const open=c.fail?" open":"";
    const body=fs.sort((a,b)=>SEV.indexOf(a.severity)-SEV.indexOf(b.severity)).map(f=>`
      <div class="f ${f.severity}${f.ignored?" ignored":""}">
        <div class="fh"><span class="cid">${f.check}</span>
          <span class="msg">${esc(f.message)}${f.ignored?" <em>(ignored)</em>":""}</span></div>
        ${f.file?`<div class="loc">${esc(f.file)}${f.line?":"+f.line:""}</div>`:""}
        ${f.detail?`<div class="det">${esc(f.detail)}</div>`:""}
      </div>`).join("");
    return `<details class="group"${open}><summary><span class="gname">${esc(name)}</span>
      <span class="pills">${pills}</span></summary>${body}</details>`;
  }).join("");
}
function esc(s){return String(s??"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}

document.querySelectorAll(".chip").forEach(b=>b.addEventListener("click",()=>{
  const s=b.dataset.sev, on=b.getAttribute("aria-pressed")==="true";
  b.setAttribute("aria-pressed",String(!on));
  on?state.sev.delete(s):state.sev.add(s);
  render();
}));
document.getElementById("q").addEventListener("input",e=>{state.q=e.target.value;render();});

const t=document.getElementById("trend");
if(HIST.length>1){
  t.innerHTML="<h2>Run history</h2><table><tr><th>When</th><th>Layers</th>"+
    "<th>Fail</th><th>Warn</th><th>Pass</th></tr>"+
    HIST.slice().reverse().map(h=>`<tr><td>${h.generated.replace("T"," ").slice(0,16)}</td>
      <td>${h.layers.join("+")}</td><td>${h.counts.fail}</td>
      <td>${h.counts.warn}</td><td>${h.counts.pass}</td></tr>`).join("")+"</table>";
}else{t.style.display="none";}
render();
</script></body></html>
"""


# ───────────────────────────────────────────────────────────── terminal output

C = {"fail": "\033[31m", "warn": "\033[33m", "info": "\033[34m", "pass": "\033[32m",
     "dim": "\033[2m", "bold": "\033[1m", "off": "\033[0m"}


def paint(s: str, key: str) -> str:
    if not sys.stdout.isatty():
        return s
    return f"{C[key]}{s}{C['off']}"


def summarise(r: Results, report: Path, previous: dict | None, duration: float) -> None:
    print()
    print(paint("  workspace eval", "bold"))
    bits = []
    for sev, label in (("fail", "fail"), ("warn", "warn"), ("info", "info"), ("pass", "pass")):
        n = r.counts[sev]
        seg = f"{n} {label}"
        if previous:
            d = n - previous["counts"][sev]
            if d:
                seg += f" ({'+' if d > 0 else ''}{d})"
        bits.append(paint(seg, sev))
    print("  " + "  ·  ".join(bits) + paint(f"   {duration:.1f}s", "dim"))
    print()

    top = [f for f in r.findings if f.severity == "fail" and not f.ignored][:6]
    if top:
        for f in top:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"  {paint('✗', 'fail')} {paint(f.scope or 'workspace', 'bold')} — {f.message}")
            if loc:
                print(f"    {paint(loc, 'dim')}")
        remaining = r.blocking - len(top)
        if remaining > 0:
            print(paint(f"    …and {remaining} more in the report", "dim"))
    else:
        print(f"  {paint('✓', 'pass')} contracts hold — no blocking failures")
    print()
    print(f"  report  {report}")
    print()


# ───────────────────────────────────────────────────────────── main

def main() -> int:
    ap = argparse.ArgumentParser(
        prog="eval", description="Evaluate the pipeline workspace.")
    ap.add_argument("layer", nargs="?", default="structure",
                    choices=["structure", "legibility", "behaviour", "all", "doctor", "prd"],
                    help="structure (free) · legibility (local model, free) · "
                         "behaviour (costs tokens) · all · doctor (check the local model) · "
                         "prd (free checks on PRD content)")
    ap.add_argument("run", nargs="?",
                    help="prd: one run, or a unique part of its name. Default: every PRD run.")
    ap.add_argument("--stage", action="append", default=[],
                    help="stage to test, repeatable. Default: each case's pipeline's "
                         "behaviour_stages in checks.json.")
    ap.add_argument("--accept", action="append", default=[], metavar="RUN[/STAGE]",
                    help="structure: mark a stale output as checked — re-baseline its lineage. "
                         "Repeatable. A run name accepts every stage in it.")
    ap.add_argument("--case", action="append", default=[],
                    help="behaviour: case to run (folder name or path), repeatable. "
                         "Default: every case under checks.json `case_roots`.")
    ap.add_argument("--grader", default="auto", choices=["auto", "local", "claude"],
                    help="auto: local grades {local} criteria, Claude grades the judgement ones. "
                         "local: local only. claude: everything to Claude.")
    ap.add_argument("--no-grade", action="store_true",
                    help="mechanics only — skip rubric grading entirely")
    ap.add_argument("--manual", action="store_true",
                    help="behaviour: write a run sheet instead of invoking the CLI")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per headless call")
    ap.add_argument("--keep", action="store_true", help="keep _eval-scratch for inspection")
    ap.add_argument("--open", dest="open_report", action="store_true", help="open the report after")
    ap.add_argument("--quiet", action="store_true", help="report only, no terminal summary")
    args = ap.parse_args()

    spec = json.loads(read(EVAL_DIR / "checks.json") or "{}")
    if not spec:
        print("cannot read _eval/checks.json", file=sys.stderr)
        return 2

    if args.layer == "doctor":
        return doctor(spec)

    r = Results(spec)
    layers: list[str] = []
    stages = args.stage  # empty: each case's pipeline decides
    t0 = time.time()

    if args.layer == "prd":
        only = None
        if args.run:
            only = prd_digest_mod.find_run(args.run)
            if only is None:
                print(f"no run matches '{args.run}'", file=sys.stderr)
                return 2
        layers.append("prd")
        run_prd(r, only)

    if args.layer in ("structure", "all"):
        layers.append("structure")
        run_structure(r, args.accept)

    if args.layer in ("legibility", "all"):
        layers.append("legibility")
        run_legibility(r, stages, args.keep)

    if args.layer in ("behaviour", "all"):
        layers.append("behaviour")
        if args.manual or not claude_cli():
            sheet = manual_sheet(spec, stages, case_dirs(spec, args.case))
            print(f"\n  run sheet  {sheet}\n")
            if args.manual:
                return 0
        run_behaviour(r, stages, not args.no_grade, args.timeout, args.keep, args.grader,
                      case_dirs(spec, args.case))

    duration = time.time() - t0
    report, previous = write_report(r, layers, duration)

    if not args.quiet:
        summarise(r, report, previous, duration)
    if args.open_report:
        subprocess.run(["open", str(report)], check=False)

    return 1 if r.blocking else 0


if __name__ == "__main__":
    sys.exit(main())
