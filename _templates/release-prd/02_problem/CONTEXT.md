# 02_problem — decide the problem worth solving

One job: one problem statement, with the evidence behind it and the metric it moves.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/product-context.md`
- Reference: `../../_shared/prd-principles.md`
- Working (this run): `../01_synthesis/output/synthesis.md`
- Working (this run): `../CLAUDE.md` — run identity
- **Do NOT load:** `../03_scope/` onward.

## Process
1. State the problem in one sentence: who, what fails for them, and when.
2. Show the evidence: quantitative and qualitative, each with its source. Name what is assumed.
3. Name the metric that moves, its current value, and the target.
4. Say what is **not** the problem — the nearby problem this release will not solve.

## Outputs
- `problem.md` → `output/` — problem statement, evidence, metric, what is out

## Human check
Say the metric and its current value without looking. If you cannot, the evidence is not strong
enough to write a PRD against.
