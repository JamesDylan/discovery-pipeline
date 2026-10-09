# 04_delivery-handoff — convert for the delivery tool

One job: convert the feature PRD into the format the delivery tool needs. Assert nothing new. If the
handoff is wrong, the feature PRD is wrong — fix it there.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/delivery-target.md` — which delivery tool, where its files go, its conventions
- Working (this run): `../02_spec/output/feature-prd.md`
- Working (this run): `../03_review/output/review.md`
- Working (this run): `../CLAUDE.md` — run identity
- **Do NOT load:** `../00_intake/`, `../01_behaviour/`.

## Process
1. If `delivery-target.md` is blank, stop and say so. Do not guess a format.
2. Write the delivery artefacts where `delivery-target.md` says, in its format.
3. Record what was written and where.

## Outputs
- `handoff.md` → `output/` — what was written, where, and how to validate it

## Human check
The delivery tool accepts the artefacts without hand edits. If it needs edits, fix the feature PRD
or `delivery-target.md`, then re-run this stage.
