#!/usr/bin/env python3
"""
Local-model support for the workspace eval, via Ollama.

Three jobs:
  probe()        — what's installed, and can it do tools and JSON? Powers `./eval doctor`.
  grade_local()  — rubric criteria tagged {local} in the markdown.
  run_stage()    — a deliberately small agent loop, for the `legibility` tier.

Stdlib only. Ollama is reached over plain HTTP, so nothing needs installing beyond Ollama itself.

On the legibility tier: this is NOT a cheap substitute for the behavioural layer. A small local
model running a stage tests whether the contract is mechanically unambiguous — can it find its
inputs, respect its "do NOT load" list, and write the declared output where it promised. It says
nothing about the quality of the thinking. Findings here are warnings, never failures, because a
local model falling over is ambiguous evidence: it may be the contract, or it may be the model.
The transcript is kept so you can tell which.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

DEFAULTS = {
    "base_url": "http://localhost:11434",
    "model": "",
    "grader_model": "",
    "num_ctx": 16384,
    "temperature": 0,
    "max_turns": 24,
    "timeout": 300,
    "prefer": ["qwen2.5:32b", "qwen2.5:14b", "qwen2.5:7b", "qwen2.5", "qwen3", "llama3.1"],
}


class LocalError(RuntimeError):
    pass


# ───────────────────────────────────────────────────────────── transport

def _post(cfg: dict, path: str, body: dict, timeout: int | None = None) -> dict:
    url = cfg["base_url"].rstrip("/") + path
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout or cfg["timeout"]) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise LocalError(f"{path} → HTTP {e.code}: {e.read().decode()[:300]}") from e
    except urllib.error.URLError as e:
        raise LocalError(
            f"cannot reach Ollama at {cfg['base_url']} ({e.reason}). Is `ollama serve` running?"
        ) from e
    except TimeoutError as e:
        raise LocalError(f"{path} timed out after {timeout or cfg['timeout']}s") from e


def _get(cfg: dict, path: str, timeout: int = 15) -> dict:
    url = cfg["base_url"].rstrip("/") + path
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.URLError as e:
        raise LocalError(
            f"cannot reach Ollama at {cfg['base_url']} ({e.reason}). Is `ollama serve` running?"
        ) from e


def chat(cfg: dict, model: str, messages: list[dict], *, tools: list | None = None,
         as_json: bool = False, timeout: int | None = None) -> dict:
    body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": cfg["temperature"], "num_ctx": cfg["num_ctx"]},
    }
    if tools:
        body["tools"] = tools
    if as_json:
        body["format"] = "json"
    return _post(cfg, "/api/chat", body, timeout)


# ───────────────────────────────────────────────────────────── doctor

def probe(cfg: dict) -> dict:
    """Inspect the local Ollama. Never raises: returns a findings dict."""
    out: dict = {"base_url": cfg["base_url"], "reachable": False, "models": [],
                 "chosen": "", "tools": None, "json": None, "notes": []}
    try:
        tags = _get(cfg, "/api/tags")
    except LocalError as e:
        out["notes"].append(str(e))
        return out

    out["reachable"] = True
    out["models"] = sorted(m.get("name", "") for m in tags.get("models", []))
    if not out["models"]:
        out["notes"].append("Ollama is running but has no models pulled.")
        return out

    chosen = cfg.get("model") or ""
    if chosen and chosen not in out["models"]:
        out["notes"].append(f"configured model {chosen!r} is not installed — picking another")
        chosen = ""
    if not chosen:
        for want in cfg["prefer"]:
            match = [m for m in out["models"] if m == want or m.startswith(want + ":")
                     or m.split(":")[0] == want]
            if match:
                chosen = sorted(match)[0]
                break
    if not chosen:
        chosen = out["models"][0]
        out["notes"].append(f"no preferred model found — falling back to {chosen}")
    out["chosen"] = chosen

    try:
        info = _post(cfg, "/api/show", {"model": chosen}, timeout=20)
        caps = info.get("capabilities")
        if isinstance(caps, list):
            out["declared_capabilities"] = caps
    except LocalError as e:
        out["notes"].append(f"/api/show unavailable: {e}")

    # live JSON-mode probe
    try:
        r = chat(cfg, chosen,
                 [{"role": "user", "content":
                   'Reply with this exact JSON and nothing else: {"ok": true}'}],
                 as_json=True, timeout=90)
        text = (r.get("message") or {}).get("content", "")
        out["json"] = bool(re.search(r'"ok"\s*:\s*true', text))
        if not out["json"]:
            out["notes"].append(f"JSON mode returned something unexpected: {text[:120]!r}")
    except LocalError as e:
        out["json"] = False
        out["notes"].append(f"JSON probe failed: {e}")

    # live tool-calling probe
    tool = [{"type": "function", "function": {
        "name": "read_file",
        "description": "Read a file from disk.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "path to read"}},
            "required": ["path"]}}}]
    try:
        r = chat(cfg, chosen,
                 [{"role": "user", "content":
                   "Read the file CONTEXT.md. Use the read_file tool. Do not answer in prose."}],
                 tools=tool, timeout=120)
        calls = (r.get("message") or {}).get("tool_calls") or []
        out["tools"] = bool(calls)
        if not out["tools"]:
            out["notes"].append(
                "model did not emit a tool call. Grading will work; the legibility tier will not.")
    except LocalError as e:
        out["tools"] = False
        out["notes"].append(f"tool probe failed: {e}")

    return out


# ───────────────────────────────────────────────────────────── rubric routing

CRITERION_RE = re.compile(r"^\*\*([A-Za-z]+\d+)\s*—\s*(.+?)\*\*(.*)$")


def split_rubric(text: str) -> tuple[list[str], list[str], str, str]:
    """
    Criteria are '**ID — title**' lines. A trailing '{local}' marks one as safe for a small
    local model to grade. Returns (local_ids, strong_ids, local_rubric, strong_rubric).
    """
    preamble, blocks, current = [], [], None
    for line in text.splitlines():
        m = CRITERION_RE.match(line.strip())
        if m:
            if current:
                blocks.append(current)
            current = {"id": m.group(1), "local": "{local}" in m.group(3), "lines": [line]}
        elif current:
            current["lines"].append(line)
        else:
            preamble.append(line)
    if current:
        blocks.append(current)

    head = "\n".join(preamble).strip()
    local = [b for b in blocks if b["local"]]
    strong = [b for b in blocks if not b["local"]]

    def render(bs: list[dict]) -> str:
        if not bs:
            return ""
        body = "\n".join("\n".join(b["lines"]).rstrip() for b in bs)
        return f"{head}\n\n---\n\n{body}\n"

    return ([b["id"] for b in local], [b["id"] for b in strong],
            render(local), render(strong))


GRADER_SYSTEM = (
    "You grade a document against a rubric. Be strict and literal. A document that sounds "
    "plausible but does not satisfy a criterion fails it. Judge only what is written, never what "
    "the author probably meant. Reply with JSON only."
)


def grade_local(cfg: dict, rubric_md: str, produced: str, ids: list[str]) -> tuple[list[dict], str]:
    """Grade the {local} criteria. Returns (checks, error)."""
    model = cfg.get("grader_model") or cfg.get("model")
    if not model:
        return [], "no local model configured — run `./eval doctor`"

    budget = max(4000, cfg["num_ctx"] * 3 - len(rubric_md) - 1200)
    prompt = (
        "=== RUBRIC ===\n" + rubric_md +
        "\n\n=== DOCUMENT UNDER TEST ===\n" + produced[:budget] +
        "\n\n=== TASK ===\n"
        f"Grade exactly these criteria, one entry each, in this order: {', '.join(ids)}.\n"
        'Return only: {"checks":[{"id":"<id>","verdict":"pass" or "fail",'
        '"evidence":"<one sentence quoting the document>"}]}'
    )
    try:
        r = chat(cfg, model,
                 [{"role": "system", "content": GRADER_SYSTEM},
                  {"role": "user", "content": prompt}],
                 as_json=True)
    except LocalError as e:
        return [], str(e)

    text = (r.get("message") or {}).get("content", "")
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return [], f"local grader returned no JSON: {text[:200]!r}"
    try:
        checks = json.loads(m.group(0)).get("checks", [])
    except json.JSONDecodeError as e:
        return [], f"unparseable local grader JSON: {e}"

    wanted = set(ids)
    keep = [c for c in checks if c.get("id") in wanted]
    for missing in wanted - {c.get("id") for c in keep}:
        keep.append({"id": missing, "verdict": "unknown",
                     "evidence": "local grader did not return a verdict for this criterion"})
    return keep, ""


# ───────────────────────────────────────────────────────────── legibility agent loop

TOOLS = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read a UTF-8 text file. Paths are relative to the workspace root.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "list_dir",
        "description": "List the entries of a directory, relative to the workspace root.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write a UTF-8 text file, creating parent folders. Overwrites.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"}}, "required": ["path", "content"]}}},
]

AGENT_SYSTEM = """You are executing one stage of a product-discovery pipeline.

Your working directory is the workspace root. All paths you pass to tools are relative to it.

Procedure, in order:
1. read_file the stage's CONTEXT.md. It is the contract. Follow it exactly.
2. Read every file its "Inputs" section names. Resolve the relative paths in that list against the
   stage folder, not against the root. Never read anything its "Do NOT load" line excludes.
3. Do the work the "Process" section describes.
4. write_file the file its "Outputs" section names, into that stage's output/ folder.

Rules: the output file is the whole point — never finish without writing it. Use tools rather than
describing what you would do. Do not ask questions; there is nobody to answer them. Keep going
until the output file is written, then stop and say DONE."""


def _safe(root: Path, raw: str) -> Path:
    p = (root / str(raw).strip().lstrip("/")).resolve()
    if not str(p).startswith(str(root.resolve())):
        raise LocalError(f"path escapes the workspace: {raw}")
    return p


def _args(call: dict) -> dict:
    a = (call.get("function") or {}).get("arguments", {})
    if isinstance(a, str):
        try:
            a = json.loads(a)
        except json.JSONDecodeError:
            return {}
    return a if isinstance(a, dict) else {}


def run_stage(cfg: dict, root: Path, stage_rel: str) -> dict:
    """
    Drive a local model through one stage. Returns
    {reads, writes, turns, transcript, error, stalled}.
    """
    model = cfg.get("model")
    out = {"reads": [], "writes": [], "turns": 0, "transcript": [], "error": "", "stalled": False}
    if not model:
        out["error"] = "no local model configured — run `./eval doctor`"
        return out

    messages = [
        {"role": "system", "content": AGENT_SYSTEM},
        {"role": "user", "content":
         f"Work the stage at {stage_rel}. Start by reading {stage_rel}/CONTEXT.md."},
    ]

    for turn in range(1, cfg["max_turns"] + 1):
        out["turns"] = turn
        try:
            r = chat(cfg, model, messages, tools=TOOLS)
        except LocalError as e:
            out["error"] = str(e)
            return out

        msg = r.get("message") or {}
        calls = msg.get("tool_calls") or []
        text = (msg.get("content") or "").strip()
        messages.append({"role": "assistant", "content": msg.get("content") or "",
                         **({"tool_calls": calls} if calls else {})})

        if not calls:
            out["transcript"].append(f"[{turn}] said: {text[:300]}")
            if "DONE" in text.upper() or turn >= 3:
                return out
            messages.append({"role": "user", "content":
                             "Use a tool. Read the stage CONTEXT.md, then write the output file "
                             "it names."})
            continue

        for call in calls:
            name = (call.get("function") or {}).get("name", "")
            a = _args(call)
            try:
                if name == "read_file":
                    p = _safe(root, a.get("path", ""))
                    out["reads"].append(str(p))
                    body = p.read_text(encoding="utf-8")
                    result = body[:20000]
                    out["transcript"].append(f"[{turn}] read {p.name} ({len(body)} chars)")
                elif name == "list_dir":
                    p = _safe(root, a.get("path", ""))
                    result = "\n".join(sorted(x.name + ("/" if x.is_dir() else "")
                                              for x in p.iterdir()))
                    out["transcript"].append(f"[{turn}] list {a.get('path')}")
                elif name == "write_file":
                    p = _safe(root, a.get("path", ""))
                    p.parent.mkdir(parents=True, exist_ok=True)
                    content = a.get("content", "") or ""
                    p.write_text(content, encoding="utf-8")
                    out["writes"].append(str(p))
                    result = f"wrote {len(content)} chars"
                    out["transcript"].append(f"[{turn}] WROTE {p.name} ({len(content)} chars)")
                else:
                    result = f"no such tool: {name}"
                    out["transcript"].append(f"[{turn}] bad tool {name!r}")
            except FileNotFoundError:
                result = f"no such file: {a.get('path')}"
                out["transcript"].append(f"[{turn}] miss {a.get('path')}")
            except LocalError as e:
                result = str(e)
                out["transcript"].append(f"[{turn}] blocked {e}")
            except Exception as e:  # noqa: BLE001 - a tool error must not kill the run
                result = f"error: {e}"
                out["transcript"].append(f"[{turn}] error {e}")

            messages.append({"role": "tool", "tool_name": name, "content": str(result)})

    out["stalled"] = True
    return out
