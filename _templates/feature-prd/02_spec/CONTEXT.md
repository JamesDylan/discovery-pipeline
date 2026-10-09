# 02_spec — write the feature PRD

One job: write the feature PRD from the decided behaviour. Assert nothing `01_behaviour` did not
decide.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/prd-principles.md`
- Reference: `../../_shared/feature-prd-template.md`
- Working (this run): `../00_intake/output/intake.md`
- Working (this run): `../01_behaviour/output/behaviour.md`
- Working (this run): `../CLAUDE.md` — run identity
- Working (upstream): the `prd-digest.md` beside the file the `Upstream:` line names, not that file
  itself. First run `./digest <Upstream path>` from the workspace root; it is free and refreshes the
  digest if the PRD changed. If it says there is no release PRD there, load the upstream file
  instead. Open a full upstream section only when the digest line is not enough, and name the
  section you opened.
- **Do NOT load:** `../03_review/` onward.

## Process
1. Write in the shape `feature-prd-template.md` sets.
2. Write each acceptance criterion as a test, in the format `prd-principles.md` sets. One behaviour per criterion.
3. Reference the upstream by ID or section. Do not restate it.
4. A revision edits only the section that changed. Never rewrite the whole file.

## Outputs
- `feature-prd.md` → `output/` — the feature PRD

## Human check
Give one acceptance criterion to an engineer who has not seen the feature. If they cannot say how
they would test it, rewrite it.
