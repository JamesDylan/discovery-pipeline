# 04_prd — write the release PRD

One job: turn the problem and the scope into the release PRD. Assert nothing that `02` and `03` did
not decide.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/prd-principles.md`
- Reference: `../../_shared/prd-template.md`
- Working (this run): `../01_synthesis/output/synthesis.md`
- Working (this run): `../02_problem/output/problem.md`
- Working (this run): `../03_scope/output/scope.md`
- Working (this run): `../CLAUDE.md` — run identity
- **Do NOT load:** `../00_intake/`, `../05_review/`.

## Process
1. Write the PRD in the shape `prd-template.md` sets.
2. Point at each candidate feature by slug. Do not specify features here; that is each feature PRD's job.
3. If writing exposes a gap in the problem or the scope, stop and say which stage to revisit.
4. A revision edits only the section that changed. Never rewrite the whole file.
5. Run `./eval digest <run>` from the workspace root. Run it again after every revision.

## Outputs
- `prd.md` → `output/` — the release PRD
- `prd-digest.md` → `output/` — written by `./eval digest`, never by hand. One line per ID; feature
  runs read it instead of `prd.md`

## Human check
An engineer reads only `prd.md` and can say what ships in this release and what does not.
