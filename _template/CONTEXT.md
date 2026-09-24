# Pipeline — one screen

Nine stages. Each has one job, one `output/` folder, one human check.
One stage's `output/` is the next stage's input. Edit any output before running the next stage —
the next stage reads whatever you left there.

| Stage | One job | Output file |
|---|---|---|
| `00_setup` | Remove setup friction. Nothing else. | `inventory.md` |
| `01_frame` | Establish what problem is really being solved | `frame.md` |
| `02_explore` | Open the solution space | `options.md` |
| `03_converge` | Make the call, own the trade-off | `direction.md` |
| `04_make-tangible` | Build the artefact people react to | `artefact-notes.md` |
| `05_pressure-test` | Attack it before leadership does | `pressure-test.md` |
| `06_playback` | Get a real decision (Fri 25 Sep) | `playback.md` |
| `07_engineering-refinement` | Decision-ready → plan-ready (by 9 Oct) | `solution-scope.md` |
| `08_vision-horizon` | Lift the solution into a 12-month arc | `vision-horizon.md` |

## Status
`ls [0-9]*_*/output/` — file present means done.

## When a named input does not exist
The stage that produces it has not run. Do not invent the file and do not proceed on a guess.
Say which stage is missing and offer to run it. The only exception is `08_vision-horizon`, which
may run on `03_converge`'s output alone if `07` is still in flight.

## Sequence is not a cage
The brief is explicit: there is no required daily process. Stages `01`–`05` are thinking moves, not
gates. Prototype while still exploring; revisit the frame when something changes your thinking.
What is fixed is that each move leaves a file behind, so the next one has something to stand on.

## The one rule about 08
`08_vision-horizon` is not optional and is not a nice-to-have at the end. It is the reason this
workspace exists. If time runs short, cut fidelity in `04`, not `08`.
