# 05_review — engineering and design review

One job: a live review of the PRD that ends in decisions, not comments. This is a meeting. The agent
prepares it and writes it up; it never simulates the meeting.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Working (this run): `../04_prd/output/prd.md`
- Working (this run): `../03_scope/output/scope.md`
- Working (this run): `../CLAUDE.md` — run identity
- **Do NOT load:** `../00_intake/`, `../01_synthesis/`.

## Process
1. **Mechanical checks first.** From the workspace root, run `./eval prd <run>`. It checks
   pointers, IDs, house values and leftover template text for free. Put its findings on the
   review list as they are. Do not spend review time re-checking what it checks.
2. **Before:** list the 3–5 questions the review must answer — risks, feasibility, open decisions.
3. **After:** write up each decision, each change, and each open question with an owner and a date.
4. A change to the slice goes back into `scope.md` or `prd.md`. It does not live only here.
5. A revision edits only the section that changed. Never rewrite the whole file.
6. If you changed `prd.md`, run `./digest <run>` from the workspace root.
7. After changing the PRD, run `./eval prd <run>` again. The review is done when it shows
   no finding the review did not accept on purpose.

## Outputs
- `review.md` → `output/` — decisions, changes made, open questions with owners and dates

## Human check
Every open question has an owner and a date. An open question without an owner is a decision nobody
is making.
