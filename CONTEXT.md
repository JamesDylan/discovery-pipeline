# The map — one screen

## What is being built

Two things, deliberately separate:

| | Accelerator output | Vision output |
|---|---|---|
| Horizon | Next 1–3 months | 12 months |
| Artefact | Prototype + rationale | Narrative arc + capability sequence |
| Decision | "Do we build this?" | "Where is this part of the product going?" |

The source brief produces only the left column. Stage `08_vision-horizon` produces the right one.
Skip it and this project fails at its actual purpose — the team believing there is a vision.

## Shape

```
CLAUDE.md                 L0 routing
CONTEXT.md                L1 this file
_shared/                  L3 factory — rules, context, the brief. Stable across runs.
_template/                the method, blank. Copy per problem space.
NN-<slug>/                instance (a run): a full pipeline, own CLAUDE.md + CONTEXT.md
99-vision-synthesis/      terminal: combines runs into one vision
100-report/               terminal, optional: renders the vision as a stakeholder asset
101-prototype-handoff/    terminal, optional: briefs the prototyping tool off the vision
```

Each run is self-contained. Runs share nothing except `_shared/`. Method and instance live apart —
change the method in `_template/`, never by editing a live run.

## The nine stages

`00_setup` · `01_frame` · `02_explore` · `03_converge` · `04_make-tangible` ·
`05_pressure-test` · `06_playback` · `07_engineering-refinement` · `08_vision-horizon`

Each has one job, one `output/` folder, and exactly one human check. One stage's `output/` is the
next stage's input. **Every output is an edit surface** — open the file, change it, and the next
stage reads whatever you left there.

## The two optional steps

`09_report` · `10_prototype-handoff`

These sit after `08` in every run, and again as `100-report` and `101-prototype-handoff` at the top
level running off `99`. Both are **optional and discrete** — run either, both, or neither, at run
level or vision level. Nothing downstream waits on them.

They exist because `08` and `99` produce arguments in markdown, and markdown does neither of the
two things a position needs to survive: it doesn't hold its structure in a stakeholder room, and it
can't be looked at. `09`/`100` renders the argument as a self-contained HTML asset with its
evidence folded underneath. `10`/`101` converts it into briefs the prototyping tool named in
`_shared/prototype-target.md` can build a look-and-feel UI from.

**Neither asserts anything new.** If a report or a brief is wrong, the stage that produced the
argument is wrong. Fix it there.

| | Run level | Vision level |
|---|---|---|
| Render | `NN-<run>/09_report/` | `100-report/` |
| Prototype brief | `NN-<run>/10_prototype-handoff/` | `101-prototype-handoff/` |
| Scope of claim | that run's sphere of influence | the whole product |
| Source | `08_vision-horizon/output/` | `99-vision-synthesis/output/` |

## Where your attention goes

Expect a U-curve. Heavy at `01_frame` (setting direction), light through the middle (the work is
constrained by both anchors), heavy again at `08_vision-horizon` (deciding if this is your version
of right). Correction is cheapest at the earliest gate — an hour spent in `01_frame` is worth a day
spent in `05_pressure-test`.

## Timeline

See `_shared/timeline.md`.
