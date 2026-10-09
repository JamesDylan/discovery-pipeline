# The map — one screen

## Pipelines

A pipeline is a repeatable process kept as a blank method in `_templates/<pipeline>/`. A run is one
copy of it, working one problem. Every run in this workspace shares `_shared/`.

| Pipeline | Takes | Produces | Terminal folders |
|---|---|---|---|
| `discovery` | A problem space | A decision-ready direction and a 12-month vision claim | `99-vision-synthesis`, `100-report`, `101-prototype-handoff` |
| `release-prd` | A release, often a discovery run's direction | The release PRD | — |
| `feature-prd` | One feature, often a slice of a release PRD | A feature PRD small enough for agentic delivery | — |

Each pipeline's `CONTEXT.md` holds its running order: which stages are `core`, `live` or
`optional`, and any gates. The `release-prd` and `feature-prd` pipelines are skeletons: the stage
shapes are set, the processes are still being written.

## Shape

```
CLAUDE.md                 L0 routing and commands — knows no pipeline's stages
CONTEXT.md                L1 this file
AUTHORING.md              the rules for designing a pipeline
_shared/                  L3 factory — rules, context, decisions. Stable across runs and pipelines.
_templates/<pipeline>/    the methods, blank. Copy one per run.
NN-<slug>/                a run: one pipeline's stages, own CLAUDE.md (identity) + CONTEXT.md
99-, 100-, 101-           terminal folders: combine or render runs of one pipeline
```

Each run is self-contained. Runs share nothing except `_shared/` — and, when a run names one, the
`Upstream:` file it builds on. Method and instance live apart: change the method in
`_templates/<pipeline>/`, never by editing a live run.

## How runs connect

A run never reaches into another run's working folders. It may name one other run's output file as
its `Upstream:`. A feature PRD names its release PRD's `prd.md`; a release PRD may name a discovery
run's `solution-scope.md`. When an upstream file changes after a run built on it, `./eval` reports
`lineage.stale`. The same check covers stages inside one run.

## Every output is an edit surface

Open the file, change it, and the next stage reads whatever you left there.
