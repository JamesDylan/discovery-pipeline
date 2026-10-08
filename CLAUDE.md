# 12-Month Vision — Workspace

Umbrella workspace. Problem-space pipelines (runs, `NN-<slug>/`) share one reference layer and
converge into one vision. The product and company are named in `_shared/product-context.md`, never
here. This file is a catalog: it points at things and holds almost nothing.

## Route by task

| I am… | Go to |
|---|---|
| Working a run | `NN-<slug>/CONTEXT.md` — list runs with `ls -d [0-9][0-9]-*/` |
| Combining finished runs into the vision | `99-vision-synthesis/CONTEXT.md` |
| Rendering the vision as a stakeholder asset | `100-report/CONTEXT.md` |
| Briefing the prototyping tool off the vision | `101-prototype-handoff/CONTEXT.md` |
| Rendering or briefing **one run** on its own | that run's `09_report/` or `10_prototype-handoff/` |
| Starting a new problem space | `new <slug>` — see Commands below |
| Looking for rules, brief, context, decisions | `_shared/CONTEXT.md` |
| Orienting on the whole thing | `CONTEXT.md` |
| Asked how to use the workspace, start a run, or run a stage | `README.md` |
| Facilitating the programme, a workshop, or the solo test | `RUNBOOK.md` |
| Checking whether the folders still work after editing them | `./eval` — see `_eval/README.md` |

**`09`, `10`, `100` and `101` are optional and discrete.** Run them when something needs to travel
or be seen. Nothing downstream waits on them, and not every run needs either.

## Commands

Users type these at the workspace root. Treat close variants ("start a run called…", "what's
next on…") as the same command. `<run>` may be a partial name: `expense` matches
`04-expense-capture`. If it matches more than one folder, ask which.

**`new <slug>`** — start a run.
1. Find the next free number across top-level `NN-` folders below `99`. Copy `_template` to `NN-<slug>`.
2. Fill the identity block in `NN-<slug>/CLAUDE.md` with the user, one question at a time
   (per `_shared/operating-principles.md`). Don't invent answers. "Skip" leaves the placeholder.
3. Ask whether they have run-specific notes. If not, delete the whole `Run-specific notes by stage`
   section.
4. Stop. Report the folder name and say: start a new session and type `work NN-<slug>`.
   Do not start a stage in this session.

**`status [run]`** — report where things stand. Read only.
1. Run the Status command below (or its run-scoped equivalent).
2. Per run: steps done, steps not run, and the next step `work` would propose. Flag any unfilled
   `<…>` placeholder in the run's `CLAUDE.md`.
3. Show `09`/`10`/`100`/`101` as "not run", never as incomplete. Don't open any output file.

**`work <run>`** — guided: run the next step.
1. If the run's `CLAUDE.md` still has placeholders, fill those first (as in `new`, step 2).
2. Work out the next step: the first core step (`00`–`08`) after the highest-numbered step that has
   output. Nothing done → `00_setup`. All of `00`–`08` done → offer `09`, `10`, or stop.
   Before the first `01_frame`, ask whether Kickoff has happened. If the next step is `06` or `07`,
   say it is a live meeting and offer to help prepare or write up the output instead.
3. Propose it in one line with the reason, and ask the user to confirm or name another step.
4. Run that step exactly as its `CONTEXT.md` says.
5. When the output file is written, stop. Quote the step's **Human check**, tell the user to edit
   the output if they disagree, and say: start a new session and type `work <run>` again.
   **Never run a second step in the same session.**

**`work <run>/<step>`** — manual: run one named step. Go straight to step 4 above, then step 5.
If a named input is missing, follow the run's `CONTEXT.md` rule — name the missing step, don't guess.

**`work 99-…` / `work 100-…` / `work 101-…`** — run that terminal folder's `CONTEXT.md`. Same
stop rule as step 5.

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
