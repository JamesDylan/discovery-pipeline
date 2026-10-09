# 03_review — engineering refinement

One job: a live refinement that ends with the feature PRD ready to build. This is a meeting. The
agent prepares it and writes it up; it never simulates the meeting.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Working (this run): `../02_spec/output/feature-prd.md`
- Working (this run): `../CLAUDE.md` — run identity
- **Do NOT load:** `../00_intake/`, `../04_delivery-handoff/`.

## Process
1. **Before:** list the questions engineering must answer — feasibility, dependencies, sizing risk.
2. **After:** write up decisions, changes, and open questions with an owner and a date.
3. A change to behaviour goes back into `feature-prd.md`. It does not live only here.
4. A revision edits only the section that changed. Never rewrite the whole file.

## Outputs
- `review.md` → `output/` — decisions, changes made, open questions with owners and dates

## Human check
Engineering would start building from `feature-prd.md` tomorrow without another meeting.
