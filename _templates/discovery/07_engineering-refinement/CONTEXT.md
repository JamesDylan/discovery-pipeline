# 07_engineering-refinement — decision-ready to plan-ready (25 Sep → 8 Oct)

One job: reach a scope all three disciplines will plan against. Output was decision-ready,
**not frozen** — iteration expected, drift not.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Working (this run): `../06_playback/output/playback.md` (the decision and its conditions)
- Working (this run): `../05_pressure-test/output/pressure-test.md` (technical questions)
- Working (this run): `../04_make-tangible/output/artefact-notes.md`
- Reference: `../../_shared/decision-log.md`

## Definition of done (Fri 9 Oct)
> An agreed and sufficiently resolved solution scope and design direction that Product, Design and
> Engineering are comfortable planning against.

## Process
1. Feasibility and technical options for the chosen direction.
2. Complexity and constraints — separate genuinely hard from merely unfamiliar.
3. Material scope effects — what changes the shape, not just the estimate.
4. Design iteration where engineering learning requires it.
5. Remaining Product / Design / Engineering questions that block planning, each with an owner.

## Hold the line on
- **Scope creep dressed as feasibility.** "While we're in there" is not a technical constraint.
- **Preference claims wearing constraint clothing.** Ask what makes it hard, specifically.
- **Reopening the direction.** `03` made the call. Engineering learning changes *how*; it reopens
  *what* only if a load-bearing assumption is proven false. If that happens, say so explicitly and
  return to `03` — do not drift quietly.
- **The open-ended phase.** The brief is explicit: this does not roll into more exploration.

## Interrogate
- Which constraint, if removed, most improves the direction — and what would removing it cost?
- What is Engineering assuming about the problem that Product and Design never told them?
- What are we about to plan against that nobody has validated?

## Outputs
- `solution-scope.md` → `output/` — agreed scope, updated design direction, technical approach,
  complexity notes, what was cut and why, open questions with owners

## Human check
Get each of the three disciplines to say the words "I can plan against this." Anything softer is a no.
