# Pipeline: discovery — one screen

Takes one problem space from setup to a 12-month vision claim. Nine core stages. Each has one job,
one `output/` folder, one human check. One stage's `output/` is the next stage's input. Edit any
output before running the next stage — the next stage reads whatever you left there.

## Running order

| Stage | Type | One job | Output file |
|---|---|---|---|
| `00_setup` | core | Remove setup friction. Nothing else. | `inventory.md` |
| `01_frame` | core | Establish what problem is really being solved | `frame.md` |
| `02_explore` | core | Open the solution space | `options.md` |
| `03_converge` | core | Make the call, own the trade-off | `direction.md` |
| `04_make-tangible` | core | Build the artefact people react to | `artefact-notes.md` |
| `05_pressure-test` | core | Attack it before leadership does | `pressure-test.md` |
| `06_playback` | live | Get a real decision | `playback.md` |
| `07_engineering-refinement` | live | Decision-ready → plan-ready | `solution-scope.md` |
| `08_vision-horizon` | core | Lift the solution into a 12-month arc | `vision-horizon.md` |
| `09_report` | optional | Render the argument as a stakeholder asset | `vision-report.html` |
| `10_prototype-handoff` | optional | Brief the prototyping tool | `HANDOFF.md` |

**Types.** `core` — runs in order. `live` — a meeting; the agent helps prepare and writes up the
output, it never simulates the meeting. `optional` — run when something needs to travel or be seen;
"not run" is a legitimate end state.

**Gates.** Before the first `01_frame`, ask whether Kickoff has happened.

**Terminal folders.** `99-vision-synthesis` combines every discovery run's `08` into one vision.
`100-report` and `101-prototype-handoff` are the vision-level versions of `09` and `10`.

## What is being built

Two things, deliberately separate. `00`–`07` produce the near-term output: a prototype and
rationale that answer "do we build this?". `08` produces the 12-month view: "where is this part of
the product going?". Skip `08` and the run fails at its actual purpose.

## Status
`ls [0-9]*_*/output/` — file present means done.

## When a named input does not exist
The stage that produces it has not run. Do not invent the file and do not proceed on a guess.
Say which stage is missing and offer to run it. The only exception is `08_vision-horizon`, which
may run on `03_converge`'s output alone if `07` is still in flight.

## Sequence is not a cage
Stages `01`–`05` are thinking moves, not gates. Prototype while still exploring; revisit the frame
when something changes your thinking. What is fixed is that each move leaves a file behind, so the
next one has something to stand on.

## Where attention goes
Expect a U-curve: heavy at `01_frame`, light through the middle, heavy again at `08`. An hour spent
in `01_frame` is worth a day spent in `05_pressure-test`. If time runs short, cut fidelity in `04`,
not `08`.
