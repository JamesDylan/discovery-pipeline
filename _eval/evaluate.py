#!/usr/bin/env python3
"""
12-month vision workspace — eval.

Two layers:
  structure  — pure filesystem/markdown analysis. Zero tokens. Fast.
  behaviour  — runs stages headless against each case (synthetic fixtures + frozen real runs)
               and grades the output. Costs tokens. Case dirs: `case_roots` in checks.json.

What it enforces lives in checks.json, not here. Rubrics live in rubrics/.
Run it with ../eval from the workspace root.
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
import local as local_mod  # noqa: E402
import manifest as manifest_mod  # noqa: E402

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

def template_stages() -> list[str]:
    return sorted(p.name for p in (ROOT / "_template").iterdir()
                  if p.is_dir() and STAGE_RE.match(p.name))


def runs() -> list[Path]:
    return sorted(p for p in ROOT.iterdir()
                  if p.is_dir() and RUN_RE.match(p.name)
                  and any(c.is_dir() and STAGE_RE.match(c.name) for c in p.iterdir()))


def stages_of(run: Path) -> list[str]:
    return sorted(p.name for p in run.iterdir() if p.is_dir() and STAGE_RE.match(p.name))


# ───────────────────────────────────────────────────────────── structural checks

def check_walk(r: Results) -> None:
    """Entry points exist, and the root route table points at real files."""
    for ep in r.spec["entrypoints"]:
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


def check_run_shape(r: Results, run: Path, tmpl_stages: list[str]) -> None:
    present = stages_of(run)
    optional = set(r.spec["optional_stages"])
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
                  f"stage {stage} exists in this run but not in _template — method and instance have diverged",
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
                         tmpl_stages: list[str]) -> None:
    scope = f"{run.name} / {stage}"
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
        target = (run / stage / token).resolve()
        if target.exists():
            r.ok("contract.input-unresolved")
            continue
        # a missing output file is normal; a missing stage folder is not
        m = re.match(r"\.\./(\d{2}_[a-z0-9-]+)/", token)
        if m:
            if m.group(1) not in tmpl_stages:
                r.add("contract.input-stage-missing",
                      f"input names stage {m.group(1)}, which is not a stage in _template",
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


def check_drift(r: Results, run: Path, stage: str) -> None:
    live = run / stage / "CONTEXT.md"
    tmpl = ROOT / "_template" / stage / "CONTEXT.md"
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
          f"stage contract differs from _template (+{added} / -{removed} lines)",
          scope=f"{run.name} / {stage}", file=rel(live),
          detail="The workspace rule is: change the method in _template, never in a live run. "
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
    for name in r.spec["terminal_folders"]:
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


def run_structure(r: Results) -> None:
    canonical = r.spec["canonical_outputs"]
    tmpl_stages = template_stages()
    check_engine_manifest(r)
    check_walk(r)
    check_shared_references(r)
    check_terminals(r)

    # the template itself is a run for contract purposes
    targets = [ROOT / "_template"] + runs()
    for run in targets:
        is_template = run.name == "_template"
        if not is_template:
            check_run_shape(r, run, tmpl_stages)
            check_identity(r, run)
        check_pipeline_table(r, run, canonical)
        for stage in stages_of(run):
            check_stage_contract(r, run, stage, canonical, tmpl_stages)
            if not is_template:
                check_drift(r, run, stage)
                check_order(r, run, stage, canonical)


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


def build_scratch(stage: str, spec: dict, case: Path) -> Path:
    """Materialise a throwaway run containing the case identity and seeded upstream outputs."""
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    shutil.copytree(ROOT / "_template", SCRATCH)
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


def grade_stage(r: Results, stage: str, produced: str, scope: str, cli: str | None,
                grader: str, timeout: int, layer: str = "behaviour") -> None:
    """
    Route each rubric criterion to a grader.

    Criteria tagged '{local}' in the rubric are mechanical enough for a small local model.
    The rest are judgement calls and go to the strong model. `grader` picks the policy:
      auto   — local does its share, the strong model does the rest (default)
      local  — local only; judgement criteria are reported ungraded rather than guessed at
      claude — everything to the strong model
    """
    rubric = EVAL_DIR / "rubrics" / f"{stage}.md"
    if not rubric.exists():
        r.add("behaviour.error", f"no rubric at rubrics/{stage}.md — output quality not graded",
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
                  layer=layer, scope=scope, file=f"rubrics/{stage}.md",
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
                  layer=layer, scope=scope, file=f"rubrics/{stage}.md")
        else:
            r.add("behaviour.rubric", f"{c.get('id', '?')} — {c.get('evidence', '')}",
                  layer=layer, scope=scope, file=f"rubrics/{stage}.md",
                  detail=f"graded by: {who}")


def run_behaviour(r: Results, stages: list[str], do_grade: bool, timeout: int,
                  keep: bool, grader: str = "auto", cases: list[Path] | None = None) -> None:
    cli = claude_cli()
    if not cli:
        r.add("behaviour.error",
              "the `claude` CLI is not on PATH, so no stage could be run headless",
              layer="behaviour", scope="workspace",
              detail="Install it (npm i -g @anthropic-ai/claude-code) and re-run, or use "
                     "`./eval behaviour --manual` to print a run sheet you can work through by hand.")
        return

    canonical = r.spec["canonical_outputs"]
    cases = cases if cases is not None else case_dirs(r.spec)
    if not cases:
        r.add("behaviour.error", "no eval cases found — check `case_roots` in _eval/checks.json",
              layer="behaviour", scope="workspace")
        return
    for case, stage in ((c, s) for c in cases for s in stages):
        scope = f"{rel(case)} / {stage}"
        if not (ROOT / "_template" / stage).is_dir():
            r.add("behaviour.error", f"{stage} is not a stage in _template",
                  layer="behaviour", scope=scope)
            continue
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
            grade_stage(r, stage, produced_text, scope, cli, grader, timeout)

    if SCRATCH.exists() and not keep:
        shutil.rmtree(SCRATCH)


def run_legibility(r: Results, stages: list[str], keep: bool) -> None:
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

    canonical = r.spec["canonical_outputs"]
    cases = case_dirs(r.spec)
    if not cases:
        r.add("legibility.error", "no eval cases found — check `case_roots` in _eval/checks.json",
              layer="legibility", scope="workspace", severity="fail")
        return
    case = cases[0]  # legibility tests the contract, not the thinking — one case is enough
    for stage in stages:
        scope = f"legibility / {stage}"
        if not (ROOT / "_template" / stage).is_dir():
            r.add("legibility.error", f"{stage} is not a stage in _template",
                  layer="legibility", scope=scope, severity="fail")
            continue

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


def manual_sheet(spec: dict, stages: list[str], cases: list[Path] | None = None) -> Path:
    cases = cases if cases is not None else case_dirs(spec)
    case = rel(cases[0]) if cases else "_eval/fixtures"
    lines = ["# Behavioural eval — manual run sheet", "",
             "The `claude` CLI was not available, so run these by hand.",
             "Fresh session per stage, always from the workspace root.", ""]
    for stage in stages:
        rubric = EVAL_DIR / "rubrics" / f"{stage}.md"
        lines += [f"## {stage}", "",
                  f"1. `cp -R _template _eval-scratch` then copy `{case}/run/CLAUDE.md` over it,",
                  f"   and seed upstream outputs from `{case}/seed/`.",
                  f"2. New session, from the root: `work _eval-scratch/{stage}`",
                  f"3. Expect `_eval-scratch/{stage}/output/"
                  f"{', '.join(spec['canonical_outputs'].get(stage, []))}`", ""]
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
    previous = history[-1] if history else None

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

DEFAULT_BEHAVIOUR_STAGES = ["01_frame", "02_explore", "03_converge", "08_vision-horizon"]


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="eval", description="Evaluate the 12-month vision workspace.")
    ap.add_argument("layer", nargs="?", default="structure",
                    choices=["structure", "legibility", "behaviour", "all", "doctor"],
                    help="structure (free) · legibility (local model, free) · "
                         "behaviour (costs tokens) · all · doctor (check the local model)")
    ap.add_argument("--stage", action="append", default=[],
                    help="stage to test, repeatable. Default: the four solo-test stages.")
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
    stages = args.stage or DEFAULT_BEHAVIOUR_STAGES
    t0 = time.time()

    if args.layer in ("structure", "all"):
        layers.append("structure")
        run_structure(r)

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
