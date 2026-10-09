"""
Free PRD checks — the mechanical half of the Ready bar. No model. Run as `./eval prd [run]`.

Model review should spend tokens on judgement only. Everything here is a lookup: does each pointer
land, does each value come from the house list, did any template text survive. It reads the same
parser as `./digest` (`_tools/prd_digest.py`), so it finds things by heading and table column, not
by one house's template.

House vocabularies come from the ```prd-rules block in `_shared/prd-principles.md`, as
comma-separated lists (keys in VOCAB below). A key that is missing skips that check; the caller
reports it as `info`. No third-party modules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import prd_digest as pd

VOCAB = {
    "br.prefixes": "business requirement prefix",
    "priority": "priority",
    "question.class": "question class",
    "question.status": "question status",
    "screen.change": "screen change",
    "sensitivity": "sensitivity",
}

SECTIONS = {
    "out_of_scope": r"^out of scope$",
    "priorities": r"^priorities$",
}

PLACEHOLDER_ROW_RE = re.compile(r"^\(.*\)$")
UNKNOWN_RE = re.compile(r"\b(Unresolved|Conflicted)\b")
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
ANGLE_RE = re.compile(r"\\<[^>\n]*\\>|<(?!br\b|!--)[a-z][a-z /-]*>", re.I)
BRACKET_RE = re.compile(r"(?<![!\]\\])\[(?![ xX]\]|\^)([^\]\n]+)\](?![(\[:])")
ITALIC_LINE_RE = re.compile(r"^\*(?![*\s])")
ROW_ID_RE = re.compile(r"^[A-Za-z]{0,4}-?\d+(?:\.\d+)*[a-z]?$")


@dataclass
class Issue:
    check: str
    message: str
    line: int = 0      # 1-based
    detail: str = ""


# ───────────────────────────────────────────────────────────── config

def vocab(rules: dict[str, str]) -> dict[str, list[str]]:
    """The house's allowed values, by VOCAB key. Missing keys are absent, not empty."""
    return {k: [v.strip() for v in rules[k].split(",") if v.strip()]
            for k in VOCAB if rules.get(k, "").strip()}


def house(cfg: dict) -> dict[str, list[str]]:
    return vocab(pd.house_rules(pd.ROOT / cfg["rules_file"]))


# ───────────────────────────────────────────────────────────── markdown, with line numbers

def section_range(lines: list[str], pattern: str) -> tuple[int, int]:
    """[start, end) line indexes of the first matching section's body; (0, 0) if none."""
    hs = pd.headings(lines)
    rx = re.compile(pattern, re.I)
    for n, (i, level, title) in enumerate(hs):
        if rx.search(pd.clean(title)):
            end = next((j for j, lv, _ in hs[n + 1:] if lv <= level), len(lines))
            return i + 1, end
    return 0, 0


def table_rows(lines: list[str], start: int = 0, end: int | None = None):
    """(line index, header cells, raw row cells) for every data row of every pipe table."""
    end = len(lines) if end is None else end
    i = start
    while i < end:
        if lines[i].lstrip().startswith("|") and i + 1 < end \
                and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            header = [pd.clean(c) for c in pd.cells(lines[i])]
            i += 2
            while i < end and lines[i].lstrip().startswith("|"):
                yield i, header, pd.cells(lines[i])
                i += 1
            continue
        i += 1


def fenced(lines: list[str]) -> set[int]:
    out, inside = set(), False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            inside = not inside
            out.add(i)
        elif inside:
            out.add(i)
    return out


def header_status(lines: list[str], cfg: dict) -> str:
    start, end = section_range(lines, cfg["sections"]["header"])
    for _, header, row in table_rows(lines, start, end):
        for pair in (header, [pd.clean(c) for c in row]):
            if len(pair) >= 2 and re.match(r"^status$", pd.clean(pair[0]), re.I):
                return pd.clean(pair[1])
    return ""


def doc_id(lines: list[str], cfg: dict) -> str:
    start, end = section_range(lines, cfg["sections"]["header"])
    for _, header, row in table_rows(lines, start, end):
        for pair in (header, [pd.clean(c) for c in row]):
            if len(pair) >= 2 and re.search(r"\bid\b", pd.clean(pair[0]), re.I):
                return pd.clean(pair[1])
    return ""


# ───────────────────────────────────────────────────────────── the document's IDs

def qid_rx(cfg: dict) -> re.Pattern:
    """A question ID as a whole token: Q6 does not match inside Q6.1."""
    return re.compile(rf"(?<![\w.-])({cfg['id_patterns']['question']})(?!\w|\.\d)")


def brid_rx(cfg: dict) -> re.Pattern:
    return re.compile(rf"(?<![\w-])({cfg['id_patterns']['requirement']})(?![\w-])")


def questions(lines: list[str], cfg: dict) -> dict[str, tuple[int, dict[str, str]]]:
    """Open Questions rows: id -> (line index, {column name: cell})."""
    rx = re.compile(rf"^{cfg['id_patterns']['question']}$")
    start, end = section_range(lines, cfg["sections"]["questions"])
    out = {}
    for i, header, row in table_rows(lines, start, end):
        qid = pd.cell_at(row, 0)
        if rx.match(qid):
            out[qid] = (i, {h.lower(): pd.cell_at(row, n) for n, h in enumerate(header)})
    return out


def requirements(lines: list[str], cfg: dict) -> list[tuple[int, str, str, dict[str, str]]]:
    """Business requirement rows that carry an ID: (line index, id cell, bare id, cells by column)."""
    rx = re.compile(rf"^({cfg['id_patterns']['requirement']})")
    start, end = section_range(lines, cfg["sections"]["requirements"])
    out = []
    for i, header, row in table_rows(lines, start, end):
        if pd.column(header, r"requirement") < 0:
            continue
        cell = pd.cell_at(row, 0)
        m = rx.match(cell)
        if m:
            out.append((i, cell, m.group(1), {h.lower(): pd.cell_at(row, n)
                                               for n, h in enumerate(header)}))
    return out


def is_placeholder(text: str) -> bool:
    return bool(PLACEHOLDER_ROW_RE.match(text.strip()))


def ids_in(text: str, cfg: dict) -> set[str]:
    return set(brid_rx(cfg).findall(text)) | set(qid_rx(cfg).findall(text))


# ───────────────────────────────────────────────────────────── checks

def check_questions(lines: list[str], cfg: dict, own_id: str, parent_ids: set[str] | None,
                    children: list[str]) -> list[Issue]:
    out = []
    qs = questions(lines, cfg)
    q_rx = qid_rx(cfg)
    see_rx = re.compile(rf"\bsee\s+(?:([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+),?\s+)?"
                        rf"({cfg['id_patterns']['question']})(?!\w|\.\d)")
    skip = fenced(lines)
    for i, line in enumerate(lines):
        if i in skip:
            continue
        for m in see_rx.finditer(line):
            doc, qid = m.group(1), m.group(2)
            if doc and doc != own_id:
                if parent_ids is not None and qid not in parent_ids:
                    out.append(Issue("prd.question-pointer",
                                     f"`{m.group(0)}`: {doc} has no {qid} in its digest", i + 1))
            elif qid not in qs and (parent_ids is None or qid not in parent_ids):
                out.append(Issue("prd.question-pointer",
                                 f"`{m.group(0)}`: there is no {qid} in Open Questions", i + 1))

    # orphans: a question nothing outside its own row mentions. A sub-item's mention counts for
    # its parent question (Q6.4 points at Q6). Child feature PRDs count for a release PRD.
    mentioned: set[str] = set()
    rows = {i for i, _ in qs.values()}
    texts = ["\n".join(l for n, l in enumerate(lines) if n not in rows)] + children
    for text in texts:
        for qid in q_rx.findall(text):
            parts = qid.split(".")
            mentioned |= {".".join(parts[:n]) for n in range(1, len(parts) + 1)}
    for row_qid, (i, row) in qs.items():
        for other, (_, cells) in qs.items():
            if other != row_qid and row_qid in q_rx.findall(" ".join(cells.values())):
                mentioned.add(row_qid)
    for qid, (i, _) in qs.items():
        if qid not in mentioned:
            out.append(Issue("prd.question-orphan",
                             f"{qid} is not pointed to from anywhere in the PRD", i + 1,
                             "Every question is pointed to from the item it blocks. Point to it, "
                             "or close it."))
    return out


def check_unknowns(lines: list[str], cfg: dict) -> list[Issue]:
    """Every `Unresolved` or `Conflicted` outside Open Questions carries a question pointer."""
    out = []
    q_rx = qid_rx(cfg)
    q_start, q_end = section_range(lines, cfg["sections"]["questions"])
    skip = fenced(lines)
    for i, line in enumerate(lines):
        if i in skip or q_start <= i < q_end or line.lstrip().startswith("#"):
            continue
        text = CODE_SPAN_RE.sub("", line)
        if line.lstrip().startswith("|"):
            pieces = pd.cells(text)
        else:
            pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z*(])", text)
        for piece in pieces:
            m = UNKNOWN_RE.search(piece)
            if m and not q_rx.search(piece):
                out.append(Issue("prd.unresolved-pointer",
                                 f"`{m.group(1)}` with no question pointer: "
                                 f"{pd.clean(piece)[:90]}", i + 1,
                                 "Write it as `(Unresolved, see Qn)`."))
    return out


def check_requirements(lines: list[str], cfg: dict, allowed: dict[str, list[str]]) -> list[Issue]:
    out = []
    titles = {pd.clean(t).lower() for _, _, t in pd.headings(lines)}
    seen: dict[str, int] = {}
    for i, cell, rid, row in requirements(lines, cfg):
        if cell in seen:
            out.append(Issue("prd.br-duplicate",
                             f"{cell} is used twice (first on line {seen[cell] + 1})", i + 1))
        else:
            seen[cell] = i
        if "br.prefixes" in allowed:
            parts = rid.split("-")
            prefix = parts[-2] if len(parts) >= 2 else ""
            if prefix not in allowed["br.prefixes"]:
                out.append(Issue("prd.vocab", f"{rid}: prefix `{prefix}` is not a house "
                                 f"{VOCAB['br.prefixes']}", i + 1,
                                 "Allowed: " + ", ".join(allowed["br.prefixes"])))
        text = row.get("requirement", "")
        if is_placeholder(text):
            continue  # carried, withheld or deferred: no priority or Ref of its own
        priority = next((v for k, v in row.items() if "priority" in k), "")
        if "priority" in allowed and not UNKNOWN_RE.match(priority) \
                and priority not in allowed["priority"]:
            out.append(Issue("prd.vocab", f"{rid}: priority `{priority or '(empty)'}` is not a "
                             "house priority", i + 1, "Allowed: " + ", ".join(allowed["priority"])))
        ref = row.get("ref", "")
        for issue in ref_problems(ref, titles):
            out.append(Issue("prd.br-ref", f"{rid}: {issue}", i + 1,
                             "Ref cites a heading in this PRD, verbatim; a table row adds "
                             "` / <row id>`."))
    return out


def ref_problems(ref: str, titles: set[str]) -> list[str]:
    if not ref:
        return ["no Ref"]
    out = []
    for one in (r.strip() for r in ref.split(";") if r.strip()):
        segments = [s.strip() for s in one.split(" / ")]
        if len(segments) > 1 and ROW_ID_RE.match(segments[-1]):
            segments = segments[:-1]
        missing = [s for s in segments if s.lower() not in titles]
        if missing:
            out.append(f"Ref `{one}` names no heading in this PRD ({', '.join(missing)})")
    return out


def check_vocab_tables(lines: list[str], cfg: dict, allowed: dict[str, list[str]]) -> list[Issue]:
    """Question class and status, screen change, sensitivity: wherever their column appears."""
    out = []
    columns = [
        ("question.class", r"^class$", cfg["sections"]["questions"]),
        ("question.status", r"^status$", cfg["sections"]["questions"]),
        ("screen.change", r"^change$", cfg["sections"]["screens"]),
        ("sensitivity", r"^sensitivity$", None),
    ]
    for key, col_rx, sect in columns:
        if key not in allowed:
            continue
        start, end = section_range(lines, sect) if sect else (0, len(lines))
        for i, header, row in table_rows(lines, start, end):
            n = pd.column(header, col_rx)
            if n < 0 or (key.startswith("question.") and not re.match(
                    rf"^{cfg['id_patterns']['question']}$", pd.cell_at(row, 0))):
                continue
            value = pd.cell_at(row, n)
            if value.startswith("<") or UNKNOWN_RE.match(value) and key != "question.class":
                continue
            if value not in allowed[key]:
                label = pd.cell_at(row, 0)
                out.append(Issue("prd.vocab", f"{label}: {VOCAB[key]} `{value or '(empty)'}` is "
                                 "not a house value", i + 1,
                                 "Allowed: " + ", ".join(allowed[key])))
    return out


def check_authoring(lines: list[str]) -> list[Issue]:
    """Template text that should have been deleted before the PRD was called Ready."""
    out = []
    skip = fenced(lines)
    for i, line in enumerate(lines):
        if i in skip:
            continue
        text = CODE_SPAN_RE.sub("", line)
        if re.search(r"authoring rules?", text, re.I) and text.strip().upper() == text.strip():
            out.append(Issue("prd.authoring-left", "an AUTHORING RULES block survives", i + 1))
        elif ITALIC_LINE_RE.match(line) and not line.lstrip().startswith("|"):
            out.append(Issue("prd.authoring-left",
                             f"italic instruction line: {pd.clean(line)[:80]}", i + 1))
        elif ANGLE_RE.search(text):
            kind = "template example row" if line.lstrip().startswith("|") else "template placeholder"
            out.append(Issue("prd.authoring-left",
                             f"{kind}: {ANGLE_RE.search(text).group(0)}", i + 1))
        else:
            m = BRACKET_RE.search(text)
            if m:
                out.append(Issue("prd.authoring-left", f"[placeholder] bracket: {m.group(0)}", i + 1))
    return out


def check_scope_overlap(lines: list[str]) -> list[Issue]:
    """Exact matches only: an item listed both in Out of scope and in Priorities."""
    def key(s: str) -> str:
        return re.sub(r"[.\s]+$", "", pd.clean(s)).lower()

    start, end = section_range(lines, SECTIONS["out_of_scope"])
    out_items = {key(b) for b in pd.bullets(lines[start:end])}
    out_items |= {key(pd.cell_at(row, 0)) for _, _, row in table_rows(lines, start, end)}
    out = []
    start, end = section_range(lines, SECTIONS["priorities"])
    for i, header, row in table_rows(lines, start, end):
        item = pd.cell_at(row, max(pd.column(header, r"^item"), 0))
        if item and key(item) in out_items:
            out.append(Issue("prd.scope-overlap",
                             f"`{item[:80]}` is in both Out of scope and Priorities", i + 1,
                             "Out of scope means out of this experience, not out of this release."))
    return out


def check_inherited(lines: list[str], cfg: dict, parent_ids: set[str], parent: str) -> list[Issue]:
    """Feature PRD: every requirement ID it names but does not define exists in the parent."""
    own = {rid for _, _, rid, _ in requirements(lines, cfg)}
    rx = brid_rx(cfg)
    # only IDs of a family the PRDs use for requirements (BR-ACC-…), not risk or document IDs
    families = {rid.rsplit("-", 1)[0] for rid in own | {i for i in parent_ids if rx.fullmatch(i)}
                if "-" in rid}
    skip = fenced(lines)
    seen, out = set(), []
    for i, line in enumerate(lines):
        if i in skip:
            continue
        for rid in rx.findall(line):
            if rid in own or rid in parent_ids or rid in seen \
                    or rid.rsplit("-", 1)[0] not in families:
                continue
            seen.add(rid)
            out.append(Issue("prd.inherited-id", f"{rid} is not defined here and is not in "
                             f"the parent digest ({parent})", i + 1))
    return out


def check_carried(lines: list[str], cfg: dict, children: list[str]) -> list[Issue]:
    """Release PRD: every row carried to a feature has a matching ID in some feature PRD."""
    child_ids: set[str] = set()
    for text in children:
        child_ids |= {rid for _, _, rid, _ in requirements(text.splitlines(), cfg)}
    out = []
    for i, cell, rid, row in requirements(lines, cfg):
        text = row.get("requirement", "")
        if is_placeholder(text) and re.search(r"\bcarried\b", text, re.I) and rid not in child_ids:
            out.append(Issue("prd.carried-unmatched",
                             f"{rid} is carried to a feature, and no feature PRD defines it", i + 1,
                             f"Carried: {text}"))
    return out


# ───────────────────────────────────────────────────────────── entry point

def check(text: str, cfg: dict, allowed: dict[str, list[str]], *, parent_digest: str | None = None,
          parent_name: str = "", children: list[str] | None = None) -> tuple[str, list[Issue]]:
    """
    (header Status, issues) for one PRD. parent_digest: a feature PRD's parent digest text, when
    there is one. children: the text of feature PRDs built on this release PRD.
    """
    lines = text.splitlines()
    own_id = doc_id(lines, cfg)
    parent_ids = ids_in(parent_digest, cfg) if parent_digest is not None else None
    children = children or []
    issues = (
        check_questions(lines, cfg, own_id, parent_ids, children)
        + check_unknowns(lines, cfg)
        + check_requirements(lines, cfg, allowed)
        + check_vocab_tables(lines, cfg, allowed)
        + check_authoring(lines)
        + check_scope_overlap(lines)
    )
    if parent_ids is not None:
        issues += check_inherited(lines, cfg, parent_ids, parent_name)
    if children:
        issues += check_carried(lines, cfg, children)
    return header_status(lines, cfg), sorted(issues, key=lambda x: x.line)
