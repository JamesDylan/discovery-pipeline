# Vision Pipeline — Workspace

Umbrella workspace. Problem-space pipelines share one reference layer and converge into one
vision. This file is a catalog: it points at things and holds almost nothing.

## Route by task

| I am… | Go to |
|---|---|
| Working a specific problem space | `NN-<slug>/CONTEXT.md` |
| Combining finished runs into the vision | `99-vision-synthesis/CONTEXT.md` |
| Rendering the vision as a stakeholder asset | `100-report/CONTEXT.md` |
| Briefing a prototyping tool off the vision | `101-prototype-handoff/CONTEXT.md` |
| Rendering or briefing **one run** on its own | that run's `09_report/` or `10_prototype-handoff/` |
| Starting a new problem space | `cp -R _template NN-<slug>`, then fill its `CLAUDE.md` |
| Looking for rules, brief, context, decisions | `_shared/CONTEXT.md` |
| Orienting on the whole thing | `CONTEXT.md` |
| Running a stage, a workshop, or the solo test | `RUNBOOK.md` |
| Checking whether the folders still work after editing them | `./eval` — see `_eval/README.md` |

**`09`, `10`, `100` and `101` are optional and discrete.** Run them when something needs to travel
or be seen. Nothing downstream waits on them, and not every run needs either.

## Before acting in any folder

Load `_shared/operating-principles.md` and `_shared/house-view.md`. Load nothing else unless the
stage contract's **Inputs** list names it by path. Do not crawl the workspace.

## Status

`ls -d [0-9]*/[0-9]*_*/output/* [0-9]*/output/* 2>/dev/null` — a file present means that step is
done. The leading `[0-9]` excludes `_template/`, which is the blank method and is never "done".
The first pattern catches stages inside a run; the second catches the terminal folders (`99-`,
`100-`, `101-`). There is no other status tracker.

An empty `09`, `10`, `100` or `101` means "not run", which is a legitimate end state — do not read
it as incomplete.

## Walk test

An agent with no memory must be able to orient, act, and report status from these files alone.
If it cannot, the files are wrong — not the agent. Re-run this test after any structural change.

`./eval` automates the mechanical half of it — contracts, input paths, output filenames, drift from
`_template`. `./eval legibility` then has a local model execute a stage, which tests whether the
contract is unambiguous enough to follow; both of these are free, so run them while editing.
`./eval behaviour` runs stages against a fixture and grades what they produce, which costs tokens
and is the checkpoint rather than the loop. Details in `_eval/README.md`.

None of it replaces watching a real pair work — that is the one claim (H6 in `RUNBOOK.md`) no
script can test. They catch the breakages that are silent.
