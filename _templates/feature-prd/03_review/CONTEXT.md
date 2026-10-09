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
1. **Mechanical checks first.** From the workspace root, run `./eval prd <run>`. It checks
   pointers, IDs, house values and leftover template text for free. Put its findings on the
   review list as they are. Do not spend review time re-checking what it checks.
2. **Before:** list the questions engineering must answer — feasibility, dependencies, sizing risk.
3. **After:** write up decisions, changes, and open questions with an owner and a date.
4. A change to behaviour goes back into `feature-prd.md`. It does not live only here.
5. A revision edits only the section that changed. Never rewrite the whole file.
6. After changing the PRD, run `./eval prd <run>` again. The review is done when it shows
   no finding the review did not accept on purpose.

## Outputs
- `review.md` → `output/` — decisions, changes made, open questions with owners and dates

## Human check
Engineering would start building from `feature-prd.md` tomorrow without another meeting.
