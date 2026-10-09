# 03_scope — decide the release slice

One job: what this release includes and excludes, with the trade-off owned.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/prd-principles.md`
- Working (this run): `../02_problem/output/problem.md`
- Working (this run): `../01_synthesis/output/synthesis.md`
- Working (this run): `../CLAUDE.md` — run identity
- **Do NOT load:** `../04_prd/` onward.

## Process
1. Propose the smallest slice that moves the metric in `problem.md`.
2. List what is out, and why each item is out.
3. Complete: "We are choosing X, which means we accept worse ______." · "We reverse this if ______."
4. List candidate feature PRDs: one line and one slug each. Do not specify them here.

## Outputs
- `scope.md` → `output/` — the slice, what is out, the trade-off, candidate features with slugs
- Append the call to `../../_shared/decision-log.md`

## Human check
Read the trade-off sentence to someone who was not in the room. If they do not wince slightly, it is
not a real trade-off.
