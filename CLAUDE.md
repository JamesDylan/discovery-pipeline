# Pipeline workspace

Umbrella workspace. Runs (`NN-<slug>/`) each follow one **pipeline** — a method kept blank in
`_templates/<pipeline>/` — and share one reference layer in `_shared/`. The product and company are
named in `_shared/product-context.md`, never here. This file is a catalog: it points at things and
holds almost nothing. It knows no pipeline's stages; each pipeline's `CONTEXT.md` declares its own.

## Route by task

| I am… | Go to |
|---|---|
| Working a run | `NN-<slug>/CONTEXT.md` — list runs with `ls -d [0-9][0-9]*-*/` |
| Choosing or comparing pipelines | `CONTEXT.md` |
| Running a pipeline's terminal folder (e.g. `99-…`) | that folder's `CONTEXT.md` |
| Starting a new run | `new <pipeline> <slug>` — see Commands below |
| Looking for rules, brief, context, decisions | `_shared/CONTEXT.md` |
| Designing or changing a pipeline | `AUTHORING.md` |
| Asked how to use the workspace, start a run, or run a stage | `README.md` |
| Facilitating a discovery programme, workshop, or solo test | `RUNBOOK.md` |
| Checking whether the folders still work after editing them | `./eval` — see `_eval/README.md` |

## Commands

Users type these at the workspace root. Treat close variants ("start a run called…", "what's
next on…") as the same command. `<run>` may be a partial name: `expense` matches
`04-expense-capture`. If it matches more than one folder, ask which.

A run's pipeline is the `Pipeline:` line in its `CLAUDE.md`. If the line is missing, it is
`discovery`. The pipeline's **running order** is the table in `_templates/<pipeline>/CONTEXT.md`:
each stage is `core`, `live` or `optional`, and any **Gates** are listed under the table. Always
read the running order from the template, not the run's copy — the template is the method.

**`new <pipeline> <slug>`** — start a run.
1. If `<pipeline>` is missing or is not a folder in `_templates/`, list the pipelines (one line
   each, from `CONTEXT.md`) and ask which.
2. Number: one more than the highest `NN` used by any top-level run, skipping numbers that a
   terminal folder uses (e.g. `99`–`101`). Pad to 2 digits. Copy `_templates/<pipeline>` to `NN-<slug>`.
3. Fill the identity block in `NN-<slug>/CLAUDE.md` with the user, one question at a time
   (per `_shared/operating-principles.md`). Don't invent answers. "Skip" leaves the placeholder.
   Ask for `Upstream:` — a path to another run's output this run builds on, or `none`. Check the
   path exists.
4. If the identity has a `Run-specific notes by stage` section, ask whether they have notes. If not,
   delete the whole section.
5. Stop. Report the folder name and say: start a new session and type `work NN-<slug>`.
   Do not start a stage in this session.

**`status [run]`** — report where things stand. Read only.
1. Run the Status command below (or its run-scoped equivalent).
2. Group runs by pipeline. Per run: steps done, steps not run, and the next step `work` would
   propose. Flag any unfilled `<…>` placeholder in the run's `CLAUDE.md`.
3. Show `optional` steps and terminal folders as "not run", never as incomplete. Don't open any
   output file.
4. Mention any `lineage.stale` warning from the last `./eval` — an output built on an input that
   has since changed.

**`work <run>`** — guided: run the next step.
1. If the run's `CLAUDE.md` still has placeholders, fill those first (as in `new`, step 3).
2. Work out the next step from the running order: the first `core` or `live` step after the
   highest-numbered step that has output. Nothing done → the first step. All `core` and `live`
   steps done → offer the `optional` ones, or stop. Before a step, honour any Gate that names it.
   If the next step is `live`, say it is a live meeting and offer to help prepare or write up the
   output instead.
3. Propose it in one line with the reason, and ask the user to confirm or name another step.
4. Run that step exactly as its `CONTEXT.md` says.
5. When the output file is written, stop. Quote the step's **Human check**, tell the user to edit
   the output if they disagree, and say: start a new session and type `work <run>` again.
   **Never run a second step in the same session.**

**`work <run>/<step>`** — manual: run one named step. Go straight to step 4 above, then step 5.
If a named input is missing, follow the run's `CONTEXT.md` rule — name the missing step, don't guess.

**`work <terminal folder>`** (e.g. `work 99-…`) — run that folder's `CONTEXT.md`. Same stop rule
as step 5.

## Before acting in any folder

Load `_shared/operating-principles.md` and `_shared/house-view.md`. Load nothing else unless the
stage contract's **Inputs** list names it by path. Do not crawl the workspace.

## Status

`ls -d [0-9]*/[0-9]*_*/output/* [0-9]*/output/* 2>/dev/null` — a file present means that step is
done. The leading `[0-9]` excludes `_templates/`, which holds the blank methods and is never "done".
The first pattern catches stages inside a run; the second catches the terminal folders. There is no
other status tracker.

## Walk test

An agent with no memory must be able to orient, act, and report status from these files alone.
If it cannot, the files are wrong — not the agent. Re-run this test after any structural change.

`./eval` automates the mechanical half of it — contracts, input paths, output filenames, drift from
the template, stale outputs. `./eval legibility` then has a local model execute a stage, which tests
whether the contract is unambiguous enough to follow; both of these are free, so run them while
editing. `./eval behaviour` runs stages against a fixture and grades what they produce, which costs
tokens and is the checkpoint rather than the loop. Details in `_eval/README.md`.

None of it replaces watching a real person work a run — no script can test that. They catch the
breakages that are silent.
