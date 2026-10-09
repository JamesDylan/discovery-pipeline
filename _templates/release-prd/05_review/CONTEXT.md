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
1. **Before:** list the 3–5 questions the review must answer — risks, feasibility, open decisions.
2. **After:** write up each decision, each change, and each open question with an owner and a date.
3. A change to the slice goes back into `scope.md` or `prd.md`. It does not live only here.
4. A revision edits only the section that changed. Never rewrite the whole file.
5. If you changed `prd.md`, run `./digest <run>` from the workspace root.

## Outputs
- `review.md` → `output/` — decisions, changes made, open questions with owners and dates

## Human check
Every open question has an owner and a date. An open question without an owner is a decision nobody
is making.
