# Pipeline: feature-prd — one screen

Takes one feature to a PRD small enough to hand to an agentic delivery process. Anyone can start one
at any time; it does not need its release PRD to be finished. **Skeleton:** stage shapes, outputs
and human checks are set; the processes are first drafts.

## Running order

| Stage | Type | One job | Output file |
|---|---|---|---|
| `00_intake` | core | State the feature and what its upstream already decided | `intake.md` |
| `01_behaviour` | core | Decide what the user sees, in every state | `behaviour.md` |
| `02_spec` | core | Write the feature PRD with testable acceptance criteria | `feature-prd.md` |
| `03_review` | live | Engineering refinement | `review.md` |
| `04_delivery-handoff` | optional | Convert to the delivery tool's format | `handoff.md` |

**Types.** `core` — runs in order. `live` — a meeting; the agent helps prepare and writes up the
output, it never simulates the meeting. `optional` — run when the feature goes to delivery.

**Gates.** None.

## Small on purpose

One feature PRD per run. It references its upstream by section; it never copies it. If a feature PRD
grows past what one engineer can hold in their head, it is two features: start a second run.

## Status
`ls [0-9]*_*/output/` — file present means done.

## When a named input does not exist
The stage that produces it has not run. Do not invent the file and do not proceed on a guess.
Say which stage is missing and offer to run it.

## Where attention goes
Heaviest at `01_behaviour`. Delivery agents build what is written; an unstated state gets invented.
