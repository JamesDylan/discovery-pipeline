# Pipeline: release-prd — one screen

Takes one release from scattered sources to a PRD the team can build against. **Skeleton:** stage
shapes, outputs and human checks are set; the processes are first drafts.

## Running order

| Stage | Type | One job | Output file |
|---|---|---|---|
| `00_intake` | core | Gather sources and test access. Nothing else. | `sources.md` |
| `01_synthesis` | core | Reconcile sources: what is known, what conflicts, what is missing | `synthesis.md` |
| `02_problem` | core | Decide the problem worth solving and the metric that moves | `problem.md` |
| `03_scope` | core | Decide the release slice and own the trade-off | `scope.md` |
| `04_prd` | core | Write the release PRD | `prd.md` |
| `05_review` | live | Engineering and design review | `review.md` |

**Types.** `core` — runs in order. `live` — a meeting; the agent helps prepare and writes up the
output, it never simulates the meeting.

**Gates.** None.

## Feature PRDs are separate runs

The release PRD stays short by pointing at features, not specifying them. `03_scope` lists the
candidate features, one line and one slug each. Anyone can then start `new feature-prd <slug>` at any
time, with `Upstream:` set to this run's `04_prd/output/prd.md`. Nothing in this run waits for them.
If `prd.md` changes later, `./eval` flags every feature PRD built on the old version.

## Status
`ls [0-9]*_*/output/` — file present means done.

## When a named input does not exist
The stage that produces it has not run. Do not invent the file and do not proceed on a guess.
Say which stage is missing and offer to run it.

## Where attention goes
Heaviest at `02_problem`. A wrong problem costs every later stage and every feature PRD.
