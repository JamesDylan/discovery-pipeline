# Authoring a pipeline

How to turn a repeatable process into a pipeline in this workspace. The rules come from what made
the `discovery` pipeline work, and from the method it follows: Interpretable Context Methodology
(Van Clief & McDermott, arXiv:2603.16021).

A pipeline is a folder of numbered stages. Each stage is a contract: what to read, what to do, what
to write, and how a person checks it. One agent reads the right files at the right moment. The
folders do the work a framework would do in code.

---

## A. Does this process need a pipeline?

**1. Build one only for sequential, human-reviewed work that repeats.** The process runs at least 3
times, each step is checked by a person, and the result is a document someone acts on. If it runs
once, use a prompt. If it needs no review between steps, use a skill or a script. If many people
must work on one run at the same time, this method does not fit.

**2. Name where the job breaks before you name any stage.** Write down the point where this work
usually goes wrong — the wrong problem, an unstated edge case, an owner nobody named. Put a stage
and a human check at that point. A pipeline with no named break point is ceremony.

## B. Stages

**3. One stage, one job.** Gathering, reconciling, deciding, making, testing and rendering never
share a stage. A stage that gathers does not also filter. A stage that filters does not also decide.

**4. Every contract has the same four sections.** `## Inputs`, `## Process`, `## Outputs`,
`## Human check`. Inputs ends with a **Do NOT load** line naming the stages this one must not see —
usually everything downstream.

**5. One fixed output file per stage, in `output/`.** A file present means the stage is done. There
is no other status tracker. Several files are allowed only when one stage writes one file per item
(`<slug>.md`).

**6. Exactly one human check, written as a test a person can fail.** "Review the output" is not a
check. "Read the trade-off sentence to someone who was not in the room — if they do not wince, it is
not a trade-off" is.

**7. A decision stage ends with a trade-off and a log entry.** It completes "We are choosing X, which
means we accept worse ___" and "We reverse this if ___", and appends the call to
`_shared/decision-log.md`.

**8. A meeting is a `live` stage.** Its output is the write-up. The agent helps prepare and writes it
up; it never simulates the meeting.

**9. Render and handoff stages assert nothing new.** A report, a prototype brief or a delivery
handoff converts an argument made upstream. If it is wrong, fix the stage that made the argument.

**10. Aim for 5–9 stages.** If two stages always run back-to-back with no human edit between them,
merge them. If a stage has two human checks, split it.

**11. Put attention at the ends.** Pull hard for human input at the first decision and at the last.
Stay quiet in the middle of a stage. Say in the pipeline's `CONTEXT.md` where attention goes.

## C. Context

**12. Keep the five layers apart.**

| Layer | File | Answers |
|---|---|---|
| 0 | `CLAUDE.md` (workspace) | Where am I? What can I type? |
| 1 | `CONTEXT.md` (workspace, then pipeline) | Which pipeline, which stage? |
| 2 | stage `CONTEXT.md` | What do I do? |
| 3 | `_shared/` | What rules apply? Stable across runs. |
| 4 | `output/`, the run's `CLAUDE.md` | What am I working with? Changes every run. |

Never mix layer 3 and layer 4 in one file. Rules are absorbed as constraints; working files are
processed as input.

**13. Name every input by exact relative path, and label it.** `Reference:` for layer 3, `Working:`
for layer 4. Nothing loads unless it is named. No more than 2 files are loaded by every stage.

**14. One home per fact.** If it is true in `_shared/`, the contract points at it. It never restates
it.

**15. Contracts never name the company or product.** Organisation-specific facts live in `_shared/`
files that contracts read as inputs. That keeps the method portable.

**16. Stay inside a budget.** The workspace map plus one stage contract stays under about 1,500
words. A full stage load stays under about 8,000 tokens. If a reference file is long, name the
section the stage needs.

## D. Method, runs and connections

**17. Change the template, never a live run.** The method is `_templates/<pipeline>/`. A fix made in
a run dies with the run. `./eval` reports `drift.template` when a run's contract differs.

**18. A run's identity is filled, not assumed.** The run's `CLAUDE.md` has a `Pipeline:` line, an
`Upstream:` line and placeholders in `<angle brackets>` that `./eval` detects. Never leave a heading
empty: an empty promise is worse than none.

**19. Fork, don't branch.** If a process needs a different stage, write a new pipeline. Never add
"if this is a feature PRD, then…" to a contract.

**20. Runs connect only through output files.** A run may name one other run's output as its
`Upstream:` (workspace-relative). It never reads another run's working folders. A stage reads the
upstream file only if its Inputs say so. When the upstream file changes, `./eval` reports
`lineage.stale` on every output built on the old version.

**21. External tools are targets, named in `_shared/`.** A prototyping tool, a delivery tool or a
ticket system is described in one `_shared/<thing>-target.md` file: name, location, format,
validation. The handoff stage reads it. When the target is blank, the stage stops and says so.

## E. Running and proving it

**22. One stage per session.** A session runs one stage, writes its output, quotes the human check,
and stops. The person edits the output before the next session.

**23. The operating principles apply in every stage.** One question at a time. Plain English. Push
for a call; "it depends" is a failure. See `_shared/operating-principles.md`.

**24. Register it and pass `./eval` before anyone uses it.** See the checklist below.

**25. Grade the decision stages.** Write a rubric for each stage that makes a call, in
`_eval/rubrics/<pipeline>/<stage>.md`. Every criterion is individually falsifiable. Add at least one
synthetic fixture case whose problem is unlike your own domain.

**26. Pilot on 2–3 real runs before you call it done.** Then run the walk test: an agent with no
memory can orient, act and report status from the files alone. If it cannot, the files are wrong.

---

## Checklist: adding a pipeline

1. Write the break point (rule 2) and the stage list as a table: stage, type, one job, output file.
2. Create `_templates/<pipeline>/`:
   - `CLAUDE.md` — run identity with `- **Pipeline:** <pipeline>` and `- **Upstream:** none`, a
     title placeholder, and a Route section.
   - `CONTEXT.md` — the **Running order** table with a `Type` column (`core`, `live` or
     `optional`), a **Gates** line, Status, the missing-input rule, and where attention goes.
   - One `NN_<name>/CONTEXT.md` per stage, with the four sections.
3. Add any reference files to `_shared/` and list them in `_shared/CONTEXT.md`. In the engine, add
   blank or starter versions to `SEED` in `_eval/manifest.py`.
4. Register it under `pipelines` in `_eval/checks.json`: `canonical_outputs`, `optional_stages`
   (must match the table), `terminal_folders`, `behaviour_stages`.
5. Add the pipeline to the table in the workspace `CONTEXT.md`.
6. Run `./eval`. Fix every failure.
7. Add rubrics and a fixture case (`_eval/fixtures/<pipeline>/run/CLAUDE.md` plus `seed/`), then
   run `./eval legibility` and `./eval behaviour --stage <stage>`.
8. Pilot it: `new <pipeline> <slug>`, then `work` one stage per session.

## What this method does not do

It does not run stages in parallel, retry failed stages, or branch on an agent's output. A person
decides between stages. That is the trade: less automation, in return for every step being a file
anyone can read, edit and check.
