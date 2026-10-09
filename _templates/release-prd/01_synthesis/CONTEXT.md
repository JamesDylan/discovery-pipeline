# 01_synthesis — reconcile the sources

One job: say what the sources agree on, where they conflict, and what none of them answers. Do not
decide anything yet.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Working (this run): `../00_intake/output/sources.md` — and the sources it lists
- Working (this run): `../CLAUDE.md` — run identity, and the `Upstream:` file, if any
- **Do NOT load:** `../02_problem/` onward.

## Process
1. **What we know** — facts at least 2 sources agree on, and decisions already made, with source.
2. **Conflicts** — one line each: "Source A says X. Source B says Y."
3. **Gaps** — questions no source answers.
4. **Proposed assumptions** — where sources are silent, the assumption you would carry forward.
   Ask the user to confirm, correct or reject each one, one at a time.

## Outputs
- `synthesis.md` → `output/` — what we know, conflicts, gaps, assumptions with their status

## Human check
Every conflict has a resolution or a named person who will resolve it. An unowned conflict will
come back as a defect.
