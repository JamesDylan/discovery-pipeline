#!/usr/bin/env python3
"""
PRD digest — a short index of a release PRD, for the feature runs that build on it. No model.
Part of the process, not the eval: agents run it as a stage step. See `_tools/README.md`.

  ./digest <release-run>               write <run>/04_prd/output/prd-digest.md from prd.md
  ./digest <path/to/prd.md>            the same, given the path a feature run's Upstream: line names.
                                       Exit 3, "no release PRD there", if the path is anything else
  ./digest --file PRD [--out OUT]      digest any PRD file; prints to stdout without --out

A feature run needs the parent's IDs and the one-line meaning of each, not the whole document. The
digest keeps one line per item: header, terms, which source wins, business rules, access, business
requirements (no acceptance criteria), open questions, screens, features and metrics. It finds them
by heading and by table columns, so it is not tied to one house's template.

Section headings and ID patterns have generic defaults below. A house overrides them in a
```prd-rules block in `_shared/prd-principles.md`, as lines of `id.<kind>: regex` or
`section.<name>: regex`.

The first line records a hash of the PRD it was built from; `./eval` checks it still matches.
Running it when the digest is current changes nothing. No third-party modules.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STAMP_RE = re.compile(r"<!-- prd-digest of (\S+) sha:([0-9a-f]+)")
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
SENTENCE_RE = re.compile(r"(.+?[.?!])(?:\s|$)")

DEFAULTS = {
    "source": "prd.md",
    "output": "prd-digest.md",
    "stage": "04_prd",
    "rules_file": "_shared/prd-principles.md",
    "sections": {
        "header": r"^(document )?header$",
        "terms": r"\bterms\b",
        "source_wins": r"source wins",
        "business_rules": r"^business rules$",
        "access": r"access summary",
        "requirements": r"^business requirements$",
        "questions": r"^open questions$",
        "screens": r"screen inventory",
        "features": r"^feature (prds|index)$",
        "metrics": r"^goals",
    },
    "header_fields": r"\b(id|version|status|date)\b",
    "closed_statuses": r"^(closed|answered|resolved|n/?a)$",
    "id_patterns": {
        "requirement": r"[A-Z]+(?:-[A-Z0-9]+)*-\d+",
        "question": r"Q\d+(?:\.\d+)*",
        "metric": r"[A-Z]+\d+",
        "feature": r"F\d+",
    },
}


# ───────────────────────────────────────────────────────────── config

def load_config(house: bool = True) -> dict:
    """
    The defaults, with the house's ```prd-rules overrides on top.
    house=False skips the house block: the engine fixture is checked against generic patterns.
    """
    cfg = {**DEFAULTS, "sections": dict(DEFAULTS["sections"]),
           "id_patterns": dict(DEFAULTS["id_patterns"])}
    if house:
        for key, value in house_rules(ROOT / cfg["rules_file"]).items():
            if key.startswith("id."):
                cfg["id_patterns"][key[3:]] = value
            elif key.startswith("section."):
                cfg["sections"][key[8:]] = value
    return cfg


@functools.lru_cache(maxsize=1)
def config() -> dict:
    """The workspace's config, read once."""
    return load_config()


def house_rules(path: Path) -> dict[str, str]:
    """`key: value` lines from the first ```prd-rules fenced block. {} if there is none."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    m = re.search(r"^```prd-rules[ \t]*\n(.*?)^```", text, re.M | re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if line and not line.startswith("#") and ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


# ───────────────────────────────────────────────────────────── markdown

def source_hash(text: str) -> str:
    normed = "\n".join(l.rstrip() for l in text.strip().splitlines())
    return hashlib.sha256(normed.encode()).hexdigest()[:12]


def clean(cell: str) -> str:
    """Plain text: links to their label, emphasis and line breaks dropped, spaces collapsed."""
    cell = LINK_RE.sub(r"\1", cell)
    cell = re.sub(r"<br\s*/?>", " ", cell, flags=re.I)
    cell = cell.replace("**", "").replace("\\<", "<").replace("\\>", ">")
    cell = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", cell)
    return re.sub(r"\s+", " ", cell).strip()


def first_sentence(text: str) -> str:
    m = SENTENCE_RE.match(text)
    return m.group(1) if m else text


def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """(line index, level, title) for every ATX heading outside code fences."""
    out, fenced = [], False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced:
            m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if m:
                out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def section(lines: list[str], pattern: str) -> list[str]:
    """Body of the first heading whose title matches, up to the next heading at its level or above."""
    hs = headings(lines)
    rx = re.compile(pattern, re.I)
    for n, (i, level, title) in enumerate(hs):
        if rx.search(clean(title)):
            end = next((j for j, lv, _ in hs[n + 1:] if lv <= level), len(lines))
            return lines[i + 1:end]
    return []


def cells(row: str) -> list[str]:
    parts = re.split(r"(?<!\\)\|", row.strip())
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def tables(lines: list[str]) -> list[tuple[str, list[str], list[list[str]]]]:
    """(nearest heading above, header cells, data rows) for each pipe table in `lines`."""
    out, i, heading = [], 0, ""
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^#{1,6}\s+(.+)", line)
        if m:
            heading = clean(m.group(1))
        if line.lstrip().startswith("|") and i + 1 < len(lines) \
                and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            header = [clean(c) for c in cells(line)]
            rows, i = [], i + 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            out.append((heading, header, rows))
            continue
        i += 1
    return out


def column(header: list[str], pattern: str) -> int:
    rx = re.compile(pattern, re.I)
    return next((n for n, h in enumerate(header) if rx.search(h)), -1)


def cell_at(row: list[str], n: int) -> str:
    return clean(row[n]) if 0 <= n < len(row) else ""


def bullets(lines: list[str]) -> list[str]:
    """Top-level list items, continuation lines joined."""
    items: list[str] = []
    for line in lines:
        m = re.match(r"^(?:[-*]|\d+\.)\s+(.*)", line)
        if m:
            items.append(m.group(1))
        elif items and line.startswith((" ", "\t")) and line.strip():
            items[-1] += " " + line.strip()
        elif not line.strip() or line.startswith(("|", "#")):
            if items and items[-1] != "":
                items.append("")  # a blank line ends a list item
    return [i for i in items if i]


# ───────────────────────────────────────────────────────────── digest parts

def part_header(lines: list[str], cfg: dict) -> list[str]:
    title = next((t for _, lv, t in headings(lines) if lv == 1), "")
    fields = []
    for _, header, rows in tables(section(lines, cfg["sections"]["header"])):
        for row in [header] + rows:
            if len(row) >= 2 and re.search(cfg["header_fields"], clean(row[0]), re.I):
                fields.append(f"{clean(row[0])}: {clean(row[1])}")
    out = [f"# {clean(title)}"] if title else []
    if fields:
        out.append(". ".join(fields) + ".")
    return out


def part_bullets(lines: list[str], pattern: str, title: str) -> list[str]:
    items = bullets(section(lines, pattern))
    return [f"## {title}"] + [f"- {first_sentence(clean(b))}" for b in items] if items else []


def part_rules(lines: list[str], cfg: dict) -> list[str]:
    body = section(lines, cfg["sections"]["business_rules"])
    out = []
    for line in body:
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            bold = BOLD_RE.search(m.group(2))
            text = clean(bold.group(1)) if bold else first_sentence(clean(m.group(2)))
            out.append(f"{m.group(1)}. {text}")
    for _, header, rows in tables(body):
        r, s = column(header, r"^rule"), column(header, r"status")
        if r < 0 or s < 0:
            continue
        for row in rows:
            rule = cell_at(row, r)
            out.append(f"- Not set: {rule}{'' if rule.endswith(('.', '?')) else '.'} {cell_at(row, s)}")
    return ["## Business rules"] + out if out else []


def part_access(lines: list[str], cfg: dict) -> list[str]:
    out = []
    for _, header, rows in tables(section(lines, cfg["sections"]["access"])):
        a, ok, no = column(header, r"actor|role"), column(header, r"^allowed"), column(header, r"not allowed")
        if a < 0 or ok < 0:
            continue
        for row in rows:
            line = f"- {cell_at(row, a)}. Allowed: {cell_at(row, ok)}"
            if no >= 0:
                line += f" Not allowed: {cell_at(row, no)}"
            out.append(line)
    return ["## Access"] + out if out else []


def part_requirements(lines: list[str], cfg: dict) -> list[str]:
    id_rx = re.compile(rf"^{cfg['id_patterns']['requirement']}$")
    out, last_group = [], None
    for heading, header, rows in tables(section(lines, cfg["sections"]["requirements"])):
        req, pri = column(header, r"requirement"), column(header, r"priority")
        if req < 0:
            continue
        group = re.sub(r"^group:\s*", "", heading, flags=re.I)
        for row in rows:
            rid = cell_at(row, 0)
            if not id_rx.match(rid) or cell_at(row, req).startswith("<"):
                continue  # malformed row, or a template example left in
            if group != last_group:
                out.append(f"### {group}")
                last_group = group
            text = cell_at(row, req)
            if text.startswith("(") and text.endswith(")"):
                # a placeholder row: the requirement lives elsewhere, e.g. "(carried to F2 — why)"
                out.append(f"- {rid} → {text[1:-1].split(' — ')[0]}")
            else:
                priority = cell_at(row, pri)
                out.append(f"- {rid}{' ' + priority if priority else ''}: {text}")
    return ["## Business requirements"] + out if out else []


def part_questions(lines: list[str], cfg: dict) -> list[str]:
    id_rx = re.compile(rf"^{cfg['id_patterns']['question']}$")
    closed_rx = re.compile(cfg["closed_statuses"], re.I)
    out, closed = [], []
    for _, header, rows in tables(section(lines, cfg["sections"]["questions"])):
        q, st, ow = column(header, r"question"), column(header, r"status"), column(header, r"owner")
        if q < 0:
            continue
        for row in rows:
            qid = cell_at(row, 0)
            if not id_rx.match(qid):
                continue
            status = cell_at(row, st)
            if closed_rx.match(status):
                closed.append(f"{qid} ({status})")
                continue
            meta = ", ".join(x for x in (status, cell_at(row, ow)) if x)
            out.append(f"- {qid}{' ' + meta if meta else ''}: {cell_at(row, q)}")
    if closed:
        out.append(f"- Closed, question text omitted: {', '.join(closed)}")
    return ["## Open questions"] + out if out else []


def part_screens(lines: list[str], cfg: dict) -> list[str]:
    out = []
    for _, header, rows in tables(section(lines, cfg["sections"]["screens"])):
        s, pri, feat = column(header, r"screen"), column(header, r"priority"), column(header, r"feature")
        if s < 0:
            continue
        for row in rows:
            name = cell_at(row, s)
            if not name or name.startswith("<"):
                continue
            extra = ", ".join(x for x in (cell_at(row, feat), cell_at(row, pri)) if x)
            out.append(f"- {name}{': ' + extra if extra else ''}")
    return ["## Screens"] + out if out else []


def part_features(lines: list[str], cfg: dict) -> list[str]:
    id_rx = re.compile(rf"^{cfg['id_patterns']['feature']}$")
    out = []
    for _, header, rows in tables(section(lines, cfg["sections"]["features"])):
        name, own = column(header, r"feature"), column(header, r"question")
        if name < 0:
            continue
        for row in rows:
            fid = cell_at(row, 0)
            if not id_rx.match(fid):
                continue
            questions = cell_at(row, own)
            out.append(f"- {fid} {cell_at(row, name)}"
                       + (f". Own questions: {questions}" if questions else ""))
    return ["## Features"] + out if out else []


def part_metrics(lines: list[str], cfg: dict) -> list[str]:
    id_rx = re.compile(rf"^({cfg['id_patterns']['metric']}):\s*(.*)")
    out = []
    for _, header, rows in tables(section(lines, cfg["sections"]["metrics"])):
        if column(header, r"^metric") != 0:
            continue
        for row in rows:
            first = cell_at(row, 0)
            if not first or first.startswith("<"):
                continue
            m = id_rx.match(first)
            out.append(f"- {m.group(1)}: {m.group(2)}" if m else f"- {first}")
    return ["## Metrics"] + out if out else []


def build(text: str, cfg: dict, source_name: str = "prd.md") -> str:
    lines = text.splitlines()
    s = cfg["sections"]
    parts = [
        part_header(lines, cfg),
        part_bullets(lines, s["terms"], "Terms"),
        part_bullets(lines, s["source_wins"], "Which source wins"),
        part_rules(lines, cfg),
        part_access(lines, cfg),
        part_requirements(lines, cfg),
        part_questions(lines, cfg),
        part_screens(lines, cfg),
        part_features(lines, cfg),
        part_metrics(lines, cfg),
    ]
    head = [
        f"<!-- prd-digest of {source_name} sha:{source_hash(text)} — written by ./digest. "
        "Do not edit; edit the PRD and run it again. -->",
        "",
        f"> Digest of `{source_name}`: one line per item. Open a full section of the PRD only when a "
        "line here is not enough, and name the section you opened.",
        "",
        "",
    ]
    body = "\n\n".join("\n".join(p) for p in parts if p)
    return "\n".join(head) + body + "\n"


# ───────────────────────────────────────────────────────────── staleness

def stamp_of(digest_text: str) -> str:
    m = STAMP_RE.search(digest_text[:400])
    return m.group(2) if m else ""


def is_stale(prd: Path, digest_file: Path) -> bool:
    try:
        return stamp_of(digest_file.read_text(encoding="utf-8")) != \
            source_hash(prd.read_text(encoding="utf-8"))
    except OSError:
        return True


# ───────────────────────────────────────────────────────────── cli

def find_run(name: str) -> Path | None:
    """
    A run folder by exact name, by unique partial name ("expense" → "04-expense-capture"), or by a
    workspace-relative path inside it, such as a feature run's `Upstream:` value.
    """
    name = name.removeprefix("./").strip("/")
    if "/" in name:
        name = name.split("/", 1)[0]
    if not name or name.startswith("."):
        return None  # a run is a top-level folder; nothing outside the workspace
    runs = [p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^\d+-", p.name)]
    exact = [p for p in runs if p.name == name]
    if exact:
        return exact[0]
    hits = [p for p in runs if name in p.name]
    if len(hits) == 1:
        return hits[0]
    if hits:
        print(f"'{name}' matches more than one run: {', '.join(sorted(h.name for h in hits))}",
              file=sys.stderr)
    return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="digest",
                                 description="Write a release PRD's digest for its feature runs. No model.")
    ap.add_argument("run", nargs="?",
                    help="release run folder, a unique part of its name, or a path inside it")
    ap.add_argument("--file", help="digest this PRD file instead of a run's")
    ap.add_argument("--out", help="with --file: write here instead of stdout")
    ap.add_argument("--generic", action="store_true",
                    help="ignore the house ```prd-rules block (how the engine fixture is built)")
    args = ap.parse_args(argv)
    cfg = load_config(house=not args.generic)

    if args.file:
        src = Path(args.file)
        text = src.read_text(encoding="utf-8")
        result = build(text, cfg, src.name)
        if args.out:
            Path(args.out).write_text(result, encoding="utf-8")
            print(f"  wrote {args.out}  ({len(result.split())} words from {len(text.split())})")
        else:
            sys.stdout.write(result)
        return 0

    if not args.run:
        ap.print_usage(sys.stderr)
        return 2
    run = find_run(args.run)
    if run is None:
        print(f"no run matches '{args.run}'", file=sys.stderr)
        return 2
    src = run / cfg["stage"] / "output" / cfg["source"]
    if "/" in args.run.strip("/") and (ROOT / args.run.removeprefix("./")).resolve() != src.resolve():
        print(f"no release PRD there: {args.run} is not {src.relative_to(ROOT)}. "
              "No digest; read that file directly.", file=sys.stderr)
        return 3
    if not src.is_file():
        print(f"{src.relative_to(ROOT)} does not exist — run {cfg['stage']} first", file=sys.stderr)
        return 2
    text = src.read_text(encoding="utf-8")
    out = src.with_name(cfg["output"])
    result = build(text, cfg, cfg["source"])
    if out.is_file() and out.read_text(encoding="utf-8") == result:
        print(f"  {out.relative_to(ROOT)} is up to date")
        return 0
    out.write_text(result, encoding="utf-8")
    words, total = len(result.split()), len(text.split())
    print(f"  wrote {out.relative_to(ROOT)}  ({words} words, {100 * words // max(total, 1)}% of "
          f"{cfg['source']})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
