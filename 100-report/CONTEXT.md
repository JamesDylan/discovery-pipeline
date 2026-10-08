# 100-report — render the vision as an asset a room will believe

One job: turn `12-month-vision.md` into a single self-contained HTML file the team can open in
front of stakeholders and defend line by line.

**Optional and discrete.** Run it when the vision needs to travel. Skip it when the synthesis is
feeding a decision that happens in the room it was written for.

## Why this stage exists
The synthesis produces a correct argument in markdown. Markdown does not survive contact with a
stakeholder room — it gets pasted into a deck, loses its evidence, and becomes six bullets someone
else wrote. This stage protects the argument's structure by making the structure the artefact:
claims on the surface, evidence folded underneath, sources dated at the bottom.

This is a **rendering** stage, not a writing stage. If the argument is wrong, fix `99`. Nothing new
gets asserted here.

## Inputs
- Reference (every run): `../_shared/operating-principles.md`
- Reference (every run): `../_shared/house-view.md`
- Reference: `../_shared/report-design-system.md` — the visual contract. Non-negotiable.
- Reference: `../_shared/report-content-schema.md` — the slot map and stage→block mapping
- Working: `../99-vision-synthesis/output/12-month-vision.md` — **the source.**
- Working: `../_shared/product-context.md` — for the "what changed" section and the hero stats
- Working: `../_shared/decision-log.md` — for the caveats section and the method note
- **Do NOT load:** the runs' intermediate stages. Reach back and this becomes a rewrite. If the
  synthesis output doesn't carry the argument, fix it in `99`.

## Process
1. **Fill the schema first, in a file.** Produce `content.yaml` before writing a line of HTML. Every
   slot filled from a named source. Slots you cannot fill from the inputs are logged, not invented.
2. **Take the empty slots to a human.** This is the stage's one real decision point. For each gap:
   cut the claim, demote it to a caveat, or source it. Do not proceed with a slot filled by prose.
3. **Build the page.** Compose only from the sixteen components. Use CSS custom properties and
   classes — the source's inline-style authoring is not the contract, its values are.
4. **Add what the source lacked:** breakpoints at 1024/768, an `@media print` that force-opens every
   `<details>`, and an `?expand=1` deep link.
5. **Wire the evidence.** Every headline claim gets its `<details>`. One global expand/collapse pill
   in the header. Check it with JS disabled — native `<details>` must still open.

## Blind spots to call out
- **Decoration standing in for evidence** — the flywheel figure is beautiful and will get built
  whether or not its four leak numbers are real. Build it last, from the numbers.
- **New claims smuggled in at render time.** Anything in the HTML that is not in `99` is a bug.
- **Stapling, visually.** If the page reads as two runs' sections bolted together, the synthesis
  failed and the render is exposing it. Send it back to `99` rather than styling over the seam.
- **Dropping the caveats** because the page reads stronger without them. It reads stronger and
  lands weaker. The self-criticism is the trust move.
- **Two keystones.** The flywheel takes exactly one. Two means the converge stage didn't decide.
- **Deck-shaped thinking** — if the output is a sequence of slides in HTML clothing, the structure
  has already failed.

## Outputs
- `content.yaml` → `output/` — the filled schema, each slot attributed to its source
- `gaps.md` → `output/` — slots that could not be sourced, and what was decided about each
- `vision-report.html` → `output/` — one self-contained file, no build step, no external assets

## Human check
Open it on a laptop, hand it to someone in the room, and have them find the evidence for the single
number they trust least. If they can't get from the claim to its working in one click, the folding
is wrong. Then print it — if the evidence is missing on paper, the print styles are wrong.
