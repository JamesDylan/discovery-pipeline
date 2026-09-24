# 09_report — render this run's position as an asset a room will believe

One job: turn `08_vision-horizon/output/vision-horizon.md` into a single self-contained HTML file
the pair can open in front of stakeholders and defend line by line.

**Optional stage.** Run it when this run's position needs to travel on its own — a stakeholder
review, a playback to a team, a pre-read. Skip it when the run is feeding straight into synthesis
and the only audience is `99`. Skipping is not failure; rendering a position nobody asked to see is.

## Why this stage exists
Stage `08` produces a correct argument in markdown. Markdown does not survive contact with a
stakeholder room — it gets pasted into a deck, loses its evidence, and becomes six bullets someone
else wrote. This stage protects the argument's structure by making the structure the artefact:
claims on the surface, evidence folded underneath, sources dated at the bottom.

This is a **rendering** stage, not a writing stage. If the argument is wrong, fix `08`. Nothing new
gets asserted here.

## Scope of the claim
This report speaks for **this run's sphere of influence only** — the boundary set in `../CLAUDE.md`.
A run-level report that quietly widens into a claim about all of the product is this stage's characteristic
failure. That wider claim is `100-report`'s job, and only after `99` has done the synthesis.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/report-design-system.md` — the visual contract. Non-negotiable.
- Reference: `../../_shared/report-content-schema.md` — the slot map and stage→block mapping
- Working: `../08_vision-horizon/output/vision-horizon.md` — **the source. `<source>` in the schema.**
- Working: `../CLAUDE.md` — sphere of influence, which bounds the claim
- Working: `../03_converge/output/direction.md` — for the trade-offs and the "where we stall" blocks
- Working: `../05_pressure-test/output/` — for the caveats section and the stats
- Working: `../../_shared/decision-log.md` — for the method note

## Process
1. **Fill the schema first, in a file.** Produce `content.yaml` before writing a line of HTML. Every
   slot filled from a named source. Slots you cannot fill from the inputs are logged, not invented.
2. **Take the empty slots to the pair.** This is the stage's one real decision point. For each gap:
   cut the claim, demote it to a caveat, or source it. Do not proceed with a slot filled by prose.
3. **Cut the sections this run doesn't earn.** The design system's eleven-section rhythm is the
   full shape, not a quota. A single-run report often has no competitive "what changed" section and
   no five-step journey. Build what the argument supports and keep the ground rhythm intact.
4. **Build the page.** Compose only from the sixteen components. Use CSS custom properties and
   classes — the source's inline-style authoring is not the contract, its values are.
5. **Add what the source lacked:** breakpoints at 1024/768, an `@media print` that force-opens every
   `<details>`, and an `?expand=1` deep link.
6. **Wire the evidence.** Every headline claim gets its `<details>`. One global expand/collapse pill
   in the header. Check it with JS disabled — native `<details>` must still open.

## Blind spots to call out
- **Decoration standing in for evidence** — the flywheel figure is beautiful and will get built
  whether or not its numbers are real. Build it last, from the numbers, or not at all.
- **New claims smuggled in at render time.** Anything in the HTML that is not in `08` is a bug.
- **Claim creep past the sphere of influence.** See above. Check the headline against `../CLAUDE.md`.
- **Dropping the caveats** because the page reads stronger without them. It reads stronger and
  lands weaker. The self-criticism is the trust move.
- **Padding to fill the shape** — five journey steps when the argument has three, four hero stats
  when two are sourced. An empty slot is a signal, not a hole to fill.
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
