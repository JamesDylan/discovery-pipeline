# Pipeline Workspace — How This Works

A workspace for repeatable product processes. Each process is a **pipeline**: `discovery` (a problem
space to a 12-month vision), `release-prd` and `feature-prd`. Each folder is one step of the work. Each step folder holds its own instructions (`CONTEXT.md`) and
an `output/` folder. Open the workspace in Claude, name the step, and Claude does that step only —
using only the files that step lists.

No tool to learn. No special software. Folders hold the order, files hold the state.

**Part A** gets you running in five minutes. **Part B** explains the discovery pipeline: what it is
for and why it works. `RUNBOOK.md` is the facilitator's guide for discovery. `AUTHORING.md` is the
rulebook for designing a new pipeline.

---
---

# Part A — Use it

## Quick start (5 minutes)

1. **Open the workspace root** (the folder this README is in) in Claude Code — desktop app, IDE,
   or `claude` in a terminal. Always the root, never a subfolder.
2. **Type:** `new discovery expense-capture` (or `new release-prd …`, `new feature-prd …`)
   Claude copies `_templates/discovery` to the next free number (e.g. `05-expense-capture`) and asks
   you the run's identity questions, one at a time.
3. **Start a new conversation and type:** `work expense-capture`
   Claude checks what's done, proposes the next stage, runs it, and stops at the human check.
4. Repeat step 3 — one stage per conversation. (`/clear` starts a fresh one.)

Prefer doing it by hand? Copy `_templates/<pipeline>`, rename it `NN-your-problem`, fill its
`CLAUDE.md`, then go to step 3.

> **Why the number?** The eval and the status check find runs by their number prefix. It is only an
> ID. Runs of every pipeline share one number sequence.

## Pipelines and how runs connect

| Pipeline | Use it for |
|---|---|
| `discovery` | A problem space: frame, explore, decide, prototype, and a 12-month vision |
| `release-prd` | The PRD for a key release. Short: it names its features, it does not specify them |
| `feature-prd` | One feature, specified for agentic delivery. Anyone can start one at any time |

A run can build on one other run's output: its `Upstream:` line. A feature PRD usually points at a
release PRD's `04_prd/output/prd.md`. When that file changes, `./eval` flags every feature PRD built
on the old version (`lineage.stale`). Re-run the stage, or check it and type
`./eval --accept <run>/<stage>`.

`release-prd` and `feature-prd` are skeletons: the stages and checks are set, the processes are first
drafts.

## Commands

| Type | What happens |
|---|---|
| `new <pipeline> <name>` | Creates the run folder and fills its identity with you. Stops there |
| `work <run>` | **Guided.** Proposes the next stage, runs it once you confirm, stops at the human check |
| `work <run>/<stage>` | **Manual.** Runs that one stage. Use it to skip ahead, go back, or re-run |
| `status` or `status <run>` | Lists runs by pipeline, which stages are done and what's next. Changes nothing |

`<run>` can be part of the name — `work churn` finds `04-reduce-churn`. Close wording works too
("what's next on churn?"). The exact behaviour is defined in `CLAUDE.md` → Commands.

**Two habits that matter:**

- **New conversation for each stage.** In one long chat, context from earlier
  stages leaks into later ones and Claude's questions get weaker.
- **Edit any output before the next stage.** The next stage reads whatever is in `output/`. You are
  never stuck with what Claude wrote.

## Full setup (first time in a workspace, ~1 hour)

Do this once per workspace, not once per run. It is what makes output specific instead of generic.
Skip it if another run has already done it.

**1. Shared context — `_shared/`**

| File | What to do | Time |
|---|---|---|
| `product-context.md` | Product, customers, numbers, constraints. Filled by stage `00` (below) | 15–30 min |
| `house-view.md` | Your opinion of what good looks like. Write it yourself — Claude cannot | 30 min |
| `timeline.md` | Check the dates are for the current cycle | 2 min |
| Everything else | Already written. `_shared/CONTEXT.md` says what each file is for | — |

`house-view.md` matters most. If it is thin, every stage runs on generic best practice. Write it the
way you would brief a new senior hire: specific, opinionated, easy to disagree with.

**2. Run identity — `<your-run>/CLAUDE.md`**

`new` fills this with you. Doing it by hand: fill the identity block (problem, sphere of influence,
pair, owner, questions in scope). Delete the `Run-specific notes by stage` section if you have
nothing for it — an empty heading misleads later stages.

**3. Stage 00 — `work <your-run>/00_setup`**

Claude walks the setup questionnaire with you, updates `_shared/product-context.md`, and lists which
assets you can and cannot open. It will stop you if you start solving the problem — that boundary
is the point. Skippable for small or solo runs.

**4. Kickoff** (discovery only) — a live meeting before `01_frame`. See `RUNBOOK.md`.

For the PRD pipelines, also fill `_shared/prd-principles.md`, `prd-template.md`,
`feature-prd-template.md` and, before any delivery handoff, `delivery-target.md`.

## Checking the folders still work (eval)

Run the eval when you **change the method** — a `CONTEXT.md` in `_templates/`, a `_shared/` file, or
the folder structure. You do not need it to run a normal stage.

| When | Run | Cost |
|---|---|---|
| After any edit to a stage or folder | `./eval` | Free, 1 second |
| After rewording a stage's instructions | `./eval legibility --stage 02_explore` | Free (local model) |
| Before handing the method to other people | `./eval behaviour` | Uses Claude tokens |

Easiest way: ask Claude to "run `./eval` and summarise the failures". `./eval --open` opens the full
report. The local model needs a one-time `./eval doctor`. Details: `_eval/README.md`.

A clean eval proves the plumbing connects. It does not prove the thinking is good — only a real
person running a stage tells you that.

## Updating the method (engine and instance)

The method is the **engine**: a public repo, released as tags (`v0.1`, …). Your workspace is an
**instance**: the engine plus your own `_shared/` content and runs. `engine.manifest` lists every
engine-owned file.

- **Get a new version:** `./pull-engine.sh v0.2`. It replaces engine files, deletes ones the engine
  dropped, and adds blank `_shared/` starter files only if you don't have them. Your content and runs
  are never touched. Review with `git status`, then commit.
- **Don't edit engine files here.** `./eval` fails (`engine.edited`) if you do, and `pull-engine.sh`
  refuses to run until you revert or pass `--force`. Fix the method upstream in the engine, tag it,
  then pull.
- **In the engine repo itself:** after changing the method, run
  `python3 _eval/manifest.py build --version=vX.Y`, commit, then tag.

## What's in the folder

```
CLAUDE.md        the map Claude reads first, and the command definitions
README.md        this file
AUTHORING.md     the rules for designing a pipeline
RUNBOOK.md       facilitator's guide for discovery: roles, each stage in detail, what goes wrong
_shared/         background every stage uses. Write once, every run improves
_templates/      the blank methods, one folder per pipeline. Copy one to start a run
NN-<run>/        one run going through its pipeline's stages
99-, 100-, 101-  discovery: combine runs into one vision; optionally render it or brief the prototyping tool
_eval/, eval     the self-check
engine.manifest, pull-engine.sh   which files are the method, and how to update them
```

Inside a run, each stage folder is `NN_name/` with a `CONTEXT.md` (inputs, process, output, human
check) and an `output/` folder. A file in `output/` means that stage is done.

---
---

# Part B — Understand the discovery pipeline

## 1. What this is

A shared workspace that takes one product problem area from "we don't really know" to two things:

1. **A product and design direction** for the next 1–3 months, ready for leadership to decide on.
2. **A 12-month view** of where that part of the product is going.

The workspace is not a place to store documents. **It is the process itself.**

## 2. Why we are doing this

The near-term product work is strong. What is missing is the 12-month picture. That gap has a real
cost: people in the team do not believe the product has a direction, and a competing internal story
can fill the space with noise that the product has no answer to.

So the goal is not a document. **The goal is that people believe there is a direction.** A vision
that is well argued but changes nobody's mind has failed.

The second goal is about who sets the vision. Here, senior people set it for the area they know
best — it is not handed down. This workspace lets a Product and Design pair form a point of view
and defend it without waiting for permission.

## 3. The two outputs — keep them separate

|                   | Near-term output (the "accelerator") | Vision output                          |
| ----------------- | ------------------------------------ | --------------------------------------- |
| **Time horizon**  | Next 1–3 months                      | 12 months                               |
| **What you make** | A prototype and the reasoning behind it | A story of where it goes, and the order capabilities arrive in |
| **Question**      | "Do we build this?"                  | "Where is this part of the product going?" |

A perfect three-day sprint on one feature gives you the left column only — and the team still says
there is no vision. Stage `08_vision-horizon` produces the right column. It is not optional for
long-term roadmap and direction setting, but not needed if the long-term vision is already clear.
**If time runs short, cut prototype polish in stage `04`. Never cut stage `08`.**

## 4. The stages

Each stage has one job, one output file, and one human check. You can run them out of order, skip
ahead, or go back. The fixed rule is that every stage saves a file, so the next stage has something
to work from. `RUNBOOK.md` has the full detail on each one.

| Stage                       | Its one job                                                               | Output file         |
| --------------------------- | ------------------------------------------------------------------------- | ------------------- |
| `00_setup`                  | Checks you have the right files and setup to run this flow. Nothing else. | `inventory.md`      |
| `01_frame`                  | Work out what problem is really being solved                              | `frame.md`          |
| `02_explore`                | Find really different solutions. No judging yet.                          | `options.md`        |
| `03_converge`               | Choose one, and own what you give up                                      | `direction.md`      |
| `04_make-tangible`          | Build something people can react to                                       | `artefact-notes.md` |
| `05_pressure-test`          | Try to break it before leadership does                                    | `pressure-test.md`  |
| `06_playback`               | Get a real decision from leadership, live                                 | `playback.md`       |
| `07_engineering-refinement` | Turn the decision into something teams can plan against                   | `solution-scope.md` |
| `08_vision-horizon`         | Turn the solution into a 12-month story                                   | `vision-horizon.md` |
| `09_report` *(optional)*    | Turn the position into a page people will believe                         | `vision-report.html` |
| `10_prototype-handoff` *(optional)* | Turn the position into briefs the prototyping tool can build from | `prototype-briefs/*.md` |

Stages `06` and `07` are live meetings with people. Claude helps you prepare and write them up, but
the decisions happen in the room.

`09` and `10` add nothing new — if the report or brief is wrong, `08` is wrong. The same two steps
exist at the top level (`100-report/`, `101-prototype-handoff/`), working from the combined vision
in `99` instead of one run.

**Expected token cost:**

- Large project (multi-screen, multi-user, multiple releases): ~$15
- Small project (one screen or modal): ~$2

**Where your effort goes.** Expect a U-shape. Heavy at the start, when you set the direction. Light
in the middle. Heavy again at the end, when you decide if it is really right. One hour in
`01_frame` is worth a day in `05_pressure-test`.

## 5. Who is involved

| Who | What they do |
| --- | --- |
| **The Product + Design pair** | Own the work together — not Product writing a spec and handing it to Design. Senior enough to make trade-offs and to be wrong. |
| **Cross-functional leadership** | Set the challenge, protect the time, remove blockers, act as experts, and make the decision at the playback. |
| **Senior Engineering partners** | Join *after* the playback decision, for stage `07`. |
| **Domain experts and customer-facing colleagues** | Brought in briefly when an assumption could change the direction. Twenty minutes, not a workshop. |
| **The named owner of the 12-month view** | One person per run. Their name goes in the run's `CLAUDE.md`. |
| **Commercial partner** | Sees a separate version of the output — a commercial argument, not a product story. |

## 6. Why this works

- **One job per folder.** A stage that gathers does not also filter. A stage that filters does not
  also decide. Mixing jobs is how you get vague output.
- **Claude sees only what the stage needs.** Each stage lists its inputs by exact path. Claude works
  worse when given everything — and you cannot check a decision if you do not know what informed it.
- **Everything is readable and editable.** Plain markdown. Anyone can open any file and change it.
- **Set it up once, run it many times.** Improve `_shared` and every run improves.
- **It does not depend on the person who built it.** The judgement is in the files, not in
  someone's head.
- **The method is published.** It follows ICM (Interpretable Context Methodology) — Van Clief &
  McDermott, arXiv:2603.16021, `github.com/RinDig/icm-architect`.

## 7. Limitations

**Of the method:** it suits step-by-step work with a person checking each stage. It does not suit
real-time work or many people in one run at once. It organises thinking; it does not supply it.

**To watch for in this workspace:**

- **A thin `house-view.md`** means generic output. This is the most important file to keep sharp.
- **An out-of-date `product-context.md`** weakens every later stage.
- **A placeholder owner** turns the run into one person steering alone. Name someone at Kickoff.
- **A short window limits pressure-testing.** `05` will lean on existing evidence. Say so at the
  playback.
- **A few runs are a thin base for a whole-product vision.** Stage `99` must find a through-line
  no single run found. Joined summaries read as "no vision, just workstreams."
- **Dates change each cycle.** They live in `_shared/timeline.md`.

**The biggest risk:** structure becomes theatre. Neat folders can look like progress while the
thinking stays shallow. If a stage is not helping, say so and merge it into another.

## 8. How we will know it worked

> **Can a Product and Design pair run a stage and reach a position they can defend, without the
> person who set this up in the room?**

If not, the process has only created a bottleneck with better filing.

For the vision itself: say the one-sentence version to someone on the product but not on this run, and ask
them to disagree. If they cannot, it is not a position yet.

## 9. Rules that do not change

1. **Load only what the stage names.** Do not point Claude at the whole workspace.
2. **One home for each fact.** If it is in `_shared`, point to it. Do not copy it.
3. **Keep the method and live work separate.** Change `_templates/<pipeline>`, never a live run.
4. **Every session ends with a saved file.** Write the decision down before you leave the room.
5. **No polished slide deck at the playback.** Use the real work.
6. **Stage `08` is not optional.** It is the reason this workspace exists.

## 10. Glossary

| Term | Meaning |
| --- | --- |
| **Run** | One piece of work going through one pipeline's stages, in its own numbered folder (e.g. `01-<slug>`) |
| **Stage** | One numbered folder inside a run, with one job |
| **Workspace root** | The top folder — the one that contains `README.md`, `RUNBOOK.md` and `_templates` |
| **`output/` folder** | Where each stage saves its file. A file here means the stage is done |
| **`CLAUDE.md`** | The map for a folder. Points to things, holds almost nothing itself |
| **`CONTEXT.md`** | The instructions for a stage: inputs, process, output, human check |
| **`_shared`** | Background files every stage uses. Written once |
| **Pipeline** | A repeatable process, kept blank in `_templates/<pipeline>/` |
| **`_templates`** | The blank methods. Copy one to start a new run |
| **Upstream** | The one output file from another run that a run builds on |
| **Decision-ready** | Good enough for leadership to make a real decision |
| **Plan-ready** | Product, Design and Engineering can all say "I can plan against this" |
| **House view** | The team's opinion of what good looks like for the product. `_shared/house-view.md` |
| **Walk test** | Can a fresh assistant find its way, do the work and report status from the files alone? |
| **Slug** | A short, lowercase, hyphenated name for a run, e.g. `expense-capture` |

---

*Method reference: Van Clief & McDermott, "Interpretable Context Methodology: Folder Structure as
Agent Architecture", arXiv:2603.16021 · `github.com/RinDig/icm-architect`*
