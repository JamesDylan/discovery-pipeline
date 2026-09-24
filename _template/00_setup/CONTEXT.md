# 00_setup — remove setup friction

One job: make sure everything needed is reachable before Day 1. Nothing else.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/accelerator-brief.md`
- Reference: `../../_shared/setup-questionnaire.md`
- Working: `../CLAUDE.md` (the run's identity)
- **Do NOT load:** any other stage folder. No framing, no options, no opinions on the problem.

## Explicit non-goal
This is not an unofficial extra Accelerator day. If the user starts framing the problem, generating
ideas, or forming a point of view — stop them and say so. That boundary is this stage's entire value.

## Process
1. Walk `../../_shared/setup-questionnaire.md` with the user and write answers into
   `../../_shared/product-context.md`.
2. Inventory what exists: research (note anything >12 months old), Productboard, analytics,
   prior designs, design-system assets, named SMEs, customer-facing colleagues.
3. For each item, test *access*, not content. An unreachable asset on Day 1 is the failure mode.
4. Classify gaps: **blocking** (run cannot proceed credibly) · **degrading** (weaker evidence base)
   · **ignore**.
5. Ask the three questions that most often save a day:
   - What do you already know that lets you skip a research step entirely?
   - What are you assuming that was last checked over a year ago?
   - Whose 20 minutes would save you a day?

## Outputs
- `inventory.md` → `output/` — assets, access status, gaps by severity, SMEs to book
- `../../_shared/product-context.md` populated

## Human check
Open `product-context.md` and read it end to end. If you learn nothing from your own file, it isn't
filled yet.
