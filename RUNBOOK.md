# Runbook

This is the step-by-step guide for running the process. Read `README.md` first. It explains what
this workspace is and why it exists. This file explains how to use it.

> **This is a guide, not a fixed schedule.** The steps below are in the usual order, with rough
> times. You can change the order, skip ahead, or go back. One rule is fixed: **every step saves a
> file**, so the next step has something to work from.

**How this file is organised**

- **Part 0 — Terminal basics.** Read this if you do not use the terminal often. Five minutes.
- **Part 1 — Getting started.** Do these steps in order the first time you start a new problem area.
- **Part 2 — Stage-by-stage reference.** What each stage is for, who is involved, and what goes wrong.

---

# Part 0 — Terminal basics

You need only a few terminal actions for this process. This part shows all of them.

**Tip: you can ask Claude to do the terminal work for you.** After you start Claude Code (0.3
below), you can type a request in plain English, for example: *"Copy `_template` to a new folder
called `05-expense-capture`."* Claude shows you the command and asks before it runs it. The
commands in this runbook are there if you want to run them yourself.

### 0.1 Open the terminal

1. Press **Cmd + Space** to open Spotlight.
2. Type **Terminal** and press **Enter**.

A window opens with a text prompt. You type a command, then press **Enter** to run it.

### 0.2 Go to the workspace root

The **workspace root** is the top folder of this workspace. It is the folder that contains
`README.md`, `RUNBOOK.md` and `_template`. Its name depends on where you got it — for example
`discovery-pipeline`.

1. In the terminal, type `cd` followed by **one space**. Do not press Enter yet.
2. Open Finder and find the workspace root folder.
3. Drag the folder from Finder into the terminal window. The terminal fills in the full path.
4. Press **Enter**.
5. Check you are in the right place. Type `ls` and press **Enter**. You should see `README.md`,
   `RUNBOOK.md` and `_template` in the list.

> The drag-and-drop method handles folder names that contain spaces. If you type a path by hand
> and it contains spaces, put it in quotes: `cd "Product Discovery Agentic Process"`.

### 0.3 Start Claude Code

1. Make sure you are at the workspace root (0.2).
2. Type `claude` and press **Enter**.
3. Claude Code starts inside the terminal. You now type messages to Claude, not terminal commands.

**Useful commands inside Claude Code:**

| Type this | What it does |
|---|---|
| `/clear` | Starts a fresh conversation. Use this between stages. |
| `/exit` | Closes Claude Code and returns you to the normal terminal. |

### 0.4 Run a command from this runbook

1. Copy the command from the grey box in this file.
2. Click in the terminal window and paste it with **Cmd + V**.
3. Replace any placeholder before you press **Enter** (see the next section).
4. Press **Enter**.

Run terminal commands in the **normal terminal**, not inside Claude Code. If Claude Code is open,
either type `/exit` first, or open a second terminal window with **Cmd + N** and repeat 0.2 in it.

### 0.5 How placeholders work

Text inside angle brackets is a placeholder. Replace it, **including the brackets**, with your own
value.

| The runbook says | You type (example) |
|---|---|
| `NN-<slug>` | `05-expense-capture` |
| `<run>` | `01-expense-capture` |

---

# Part 1 — Getting started

Follow these steps in order the first time you start a new problem area. They take you from "I
have a problem worth a 12-month view" to the first stage finished and checked.

## Step 1 — Pick your problem and name it

**What:** Decide the problem, and give it a short name that becomes its folder name.

**How:**

1. Write your problem as one sentence. Keep this sentence — you need it in Step 4.
2. Write a short name (a "slug") for it: two to four words, lowercase, joined with hyphens. For
   example: `expense-capture`, `reduce-churn`.
3. Check that nobody is already working on this problem. Open the workspace root in Finder and
   look at the folders that start with a number. Each one is a run.
4. If your problem overlaps an existing run, work inside that run. Do not start a new one.

## Step 2 — Check the shared context is ready (first run only)

**What:** Every run reads the same background files in `_shared/`. If they are empty, every stage
produces weak, generic output. Check them once for the whole workspace, not once per run.

**How:**

1. Open `_shared/product-context.md`. This holds facts about the product, customers and constraints.
   - If it is mostly placeholder text, answer the questions in `_shared/setup-questionnaire.md`
     and write the answers into `product-context.md`.
   - A rough, fast version is fine. It only needs to be good enough that `01_frame` does not stall.
2. Open `_shared/house-view.md`. This holds the team's opinion of what good looks like in the product.
   - If it is thin or generic, fill it in. Write it the way you would explain it to a new senior
     hire over coffee: specific and opinionated, not balanced.

**Skip this step** if another run has already filled these files in.

## Step 3 — Copy the blank method into a new run folder

**What:** Every run is a copy of `_template`. You make a new copy with the next free number and your
slug.

**How:**

1. Find the next free number. Look at the numbered folders in the workspace root. Pick the next
   number that is not taken. For example, if `01`, `02`, `03` and `04` exist, use `05`.
2. Open the terminal at the workspace root (Part 0.2).
3. Run this command, with your number and slug:

   ```
   cp -R _template NN-<slug>
   ```

   Example: `cp -R _template 05-expense-capture`

4. Check it worked:

   ```
   ls NN-<slug>
   ```

   You should see 11 stage folders (`00_setup` to `10_prototype-handoff`), plus `CLAUDE.md` and
   `CONTEXT.md`.

**Or ask Claude:** *"Copy `_template` to a new run folder called `05-expense-capture`."*

## Step 4 — Fill in the run's identity

**What:** Tell the run what it is about and who owns it.

**How:**

1. Open `NN-<slug>/CLAUDE.md` in any text editor (for example VS Code, or TextEdit).
2. Under **Identity**, replace each placeholder:
   - **Problem space** — your one sentence from Step 1.
   - **Sphere of influence** — which part of the product this run has a point of view on. Be specific
     enough that someone could tell whether a given feature is inside it or outside it. Stage `08`
     makes its 12-month claim inside this boundary.
   - **Pair** — the Product person and the Design person, by name. If you are working alone, write
     that clearly. Do not leave a placeholder.
   - **Owner of the 12-month view** — one named person. It should not automatically be the person
     running the process.
3. Under **Questions in scope**, write two or three questions this run must answer.
4. Look at **Run-specific notes by stage**. Choose one:
   - **Fill it in:** write guidance under each sub-heading (where to look for ideas in
     `02_explore`, and the edge cases that matter in `05_pressure-test`).
   - **Delete it:** remove the whole section, including the heading and the quoted note.

   Do not leave the heading with nothing under it. A later stage will look there for guidance and
   find nothing.
5. Save the file.

## Step 5 — Start Claude Code at the workspace root

**What:** Open Claude Code in the right folder.

**How:** Follow Part 0.2, then Part 0.3.

> **Always start Claude Code at the workspace root.** Do not `cd` into the run folder or a stage
> folder first. There are two reasons:
>
> - The root `CLAUDE.md` only loads automatically when you start at the root.
> - The stage files use relative paths (like `../../_shared/...`). These only work when Claude
>   reads them from their place in the folder tree.
>
> Stay at the root and tell Claude which folder to work in.

## Step 6 — Run stage 00 (setup)

**What:** List what already exists for this problem (research, analytics, designs, experts) and
check you can actually open each item.

**How:**

1. In Claude Code, type:

   ```
   work NN-<slug>/00_setup
   ```

   This is a plain message, not a special command. Claude reads the root map, then the stage's
   `CONTEXT.md`, and follows the instructions in it.
2. Answer Claude's questions.
3. Claude saves the result to `NN-<slug>/00_setup/output/inventory.md`.

**Can you skip `00_setup`?** Yes, if you have already checked you can open everything this run
needs, or if this is a small or solo run. In that case, go to Step 7.

## Step 7 — Hold the Kickoff (a live meeting, not a Claude session)

**What:** Leadership and the pair meet before framing starts. Do not skip this before `01_frame`.

**How:** Book a meeting with leadership and the pair. Cover the agenda in Part 2, "Kickoff". The
most important item: **name the owner of the 12-month view, out loud, in the room.** Then update
the run's `CLAUDE.md` if anything changed.

## Step 8 — Check the output, then stop

**What:** Every stage ends with one file in its `output/` folder. A person must check it before
moving on.

**How:**

1. Open the output file and read it carefully.
2. Do the check in the **Human check** section of that stage's `CONTEXT.md`. For example, in `01_frame`:
   read the problem statement aloud — if it could not be wrong, it says nothing.
3. If you disagree with anything, **edit the file directly** and save it. The next stage reads
   whatever you leave in the file.
4. Move on only when you are happy with it.

## Step 9 — Start a fresh conversation for the next stage

**What:** Use a new, empty conversation for every stage.

**How:**

1. In Claude Code, type `/clear` and press **Enter**. (Or type `/exit`, then `claude` again.)
2. Type the next stage, for example:

   ```
   work NN-<slug>/01_frame
   ```

**Why a fresh conversation every time:** in one long conversation, context from earlier stages
leaks into later ones, and Claude's questions get weaker each time. A fresh start per stage is a
little more effort, and that effort is worth it.

## Step 10 — Repeat through the stages

Repeat Steps 8 and 9 for each stage in this table. Part 2 has the detail for each one.

| # | Stage | What you do | Output file |
|---|---|---|---|
| 00 | Setup | Type `work NN-<slug>/00_setup` | `inventory.md` |
| — | Kickoff | **Live meeting** — see Part 2 | — |
| 01 | Frame | Type `work NN-<slug>/01_frame` | `frame.md` |
| 02 | Explore | Type `work NN-<slug>/02_explore` | `options.md` |
| 03 | Converge | Type `work NN-<slug>/03_converge` | `direction.md` |
| 04 | Make tangible | Type `work NN-<slug>/04_make-tangible` | `artefact-notes.md` + prototype |
| 05 | Pressure-test | Type `work NN-<slug>/05_pressure-test` | `pressure-test.md` |
| 06 | Playback | **Live meeting with leadership** — see Part 2 | `playback.md` |
| 07 | Engineering refinement | **Live meetings with Engineering** — see Part 2 | `solution-scope.md` |
| 08 | Vision horizon | Type `work NN-<slug>/08_vision-horizon` | `vision-horizon.md` |
| 09 | Report *(optional)* | Type `work NN-<slug>/09_report` | `vision-report.html` |
| 10 | Prototype handoff *(optional)* | Type `work NN-<slug>/10_prototype-handoff` | `prototype-briefs/*.md` |

For `06` and `07`, the decisions happen in meetings with people, not in Claude. You can still use
Claude around the meeting: type `work NN-<slug>/06_playback` (or `07_engineering-refinement`) to
prepare beforehand, and again afterwards to write your notes into the output file.

## Check where a run is up to

**What:** See which stages are finished. A file in a stage's `output/` folder means that stage is
done. There is no other tracker.

**How (Finder):** open the run folder, then open each stage's `output/` folder. Empty means not done.

**How (terminal):** from the workspace root, run:

```
ls NN-<slug>/*/output/
```

The terminal lists each stage's `output/` folder and the files in it.

**How (Claude):** ask *"What is the status of `NN-<slug>`?"*

## Optional: let Claude move between stages for you

The `/run-pipeline` skill automates Steps 8–10. It starts a fresh helper agent for each stage,
shows you the output, and asks you to do the human check. It stops at `06` and `07`, because those
need live meetings.

**How:** in Claude Code, type `/run-pipeline NN-<slug>`.

**Before you use it:** it usually costs more and uses more context than running the stages by
hand, because it starts a full new agent for each stage on top of your own session. Running each
stage by hand (Steps 8–10) is more predictable and usually cheaper. Use `/run-pipeline` only if you
want the automation and accept that cost.

---
---

# Part 2 — Stage-by-stage reference

Detail on every stage: who is involved, what it is really for, and what usually goes wrong.
Part 1 tells you what to do. This part tells you what to watch for while you do it.

## Roles at a glance

| Who | Where they appear |
|---|---|
| Product + Design pair | Own `00`–`06` and `08` together. Not Product writing a spec and handing it to Design. |
| Cross-functional leadership | Kickoff, experts on call, and the decision at the playback |
| Senior Engineering partners | Join **after** the playback decision, for `07` |
| Domain experts / customer-facing colleagues | Short, 20-minute conversations during `01` and `05` |
| Named owner of the 12-month view | One per problem area. Owns `08`. Should not automatically be the person running the process. |
| Orchestrator (often you) | Sets up the challenge, protects the time, removes blockers, then **leaves the room** |

## Two rules to follow every time

1. **Start Claude Code at the workspace root**, never inside a run or stage folder. (See Part 1,
   Step 5, for why.)
2. **Use a fresh conversation for each stage.** Type `/clear` between stages. (See Part 1, Step 9,
   for why.)

## Day 0 — Setup (stage 00)

**Who:** each pair, on their own. **A few hours at most** — not a fourth working day.

**Do:**

1. If not done yet for this workspace: answer `_shared/setup-questionnaire.md` and write the answers
   into `_shared/product-context.md`.
2. List what exists: research (mark anything older than one year), product feedback tools, analytics, earlier
   designs, design-system assets, and experts.
3. Check you can **open** each item. You are testing access, not reading the content. The common
   failure is finding on day one that you cannot open something you need.
4. Sort the gaps into three groups: **blocking**, **degrading** (makes the work worse), or **ignore**.
5. Book time with the experts you will need in `01` and `05`.

**Output:** `00_setup/output/inventory.md`

**Done when:** you can open everything on the list, and reading your own context file teaches you
something new.

> **Watch out.** People start doing the real work during setup. If a pair starts framing the problem
> on day 0, stop them. Keeping setup separate is the whole value of this stage.

## Kickoff — a live meeting, not a folder

**Who:** leadership and the pair. This cannot be done by Claude, and it must happen before
`01_frame` starts.

**Agenda:**

1. Why this run exists — the gap it closes, said plainly.
2. The problem area, explained.
3. What "decision-ready" means for this run.
4. Which normal limits are removed on purpose — for example role boundaries, process, and
   permission to challenge.
5. **Name the owner of the 12-month view.** Out loud, in the room.

**Then leave.** The pair takes over. The orchestrator's only remaining jobs are removing blockers
and getting access to experts.

> **Watch out.** It is tempting to define the problem for the pair during kickoff. Don't. Describe
> the *challenge* and the *outcome* you want. The pair defines the problem in `01_frame`. If you
> hand them a problem statement, you turn them into people who just execute — and you get only
> execution back.

## Days 1–3 — The protected working days (stages 01–05)

These stages are **ways of thinking, not daily checkpoints**. Run them in whatever order gives the
strongest result. You can build a prototype while you are still exploring. You can go back and
reframe when you learn something new.

| Stage | Question | Output | Typical time |
|---|---|---|---|
| `01_frame` | What are we really solving? | `frame.md` | Half a day |
| `02_explore` | What are the really different ways to solve it? | `options.md` | Half a day |
| `03_converge` | Which one do we choose, and what do we give up? | `direction.md` | 2 hours |
| `04_make-tangible` | What can people see and react to? | `artefact-notes.md` + prototype | A day |
| `05_pressure-test` | How does it break, before leadership finds out? | `pressure-test.md` | Half a day |

**Where your effort goes:** heavy in `01`, light in `02`–`04`, heavy again in `05`. Fixing a
mistake early is cheapest — one hour in `01_frame` saves a day in `05`.

**What goes wrong in each stage:**

- **`01`** — The problem is too broad to solve in three days, or so narrow it becomes one feature.
  Also: treating a low number as a UX problem when the real cause is motivation, trust or timing.
- **`02`** — The pair picks an answer too early, because exploring feels like wasted time. It is
  not wasted. Three options that differ only in their UI are really one option.
- **`03`** — False agreement: everyone agrees because nobody wants to spend time disagreeing. Make
  the pair write down the trade-off in one sentence.
- **`04`** — Too much polish. A beautiful screen that never explains how the system *knows*
  something. Build the moments that carry the bet properly. Leave the rest rough, and say so.
- **`05`** — Looking for proof it works, instead of trying to break it. If nothing changed after
  this stage, be suspicious. Also: if a technical assumption could change the direction, bring in
  an engineer **now**. Do not carry that risk into the playback.

**Pair health check:** if Product did `01`–`03` alone and Design did `04` alone, the pairing
failed, and the output will show it. Both names go on every file.

## Stage 06 — Playback and decision

**Who:** the pair and the leadership group. **This is a decision meeting, not a showcase.** It is
a live meeting, not a Claude session.

**Running order:**

1. Start with the recommendation, not the story of how you got there.
2. State the trade-off early. It starts the real conversation.
3. Show the three screens or frames that carry the argument.
4. List the remaining risks, grouped by type.
5. Say what you need from Engineering.
6. Show a draft of the 12-month view. Leadership will ask for it. A direction without a horizon
   repeats the exact problem this process exists to fix.
7. State the decision you are asking for, and what happens if it is not made.

**Output:** `06_playback/output/playback.md`. Also add the decision and its conditions to
`_shared/decision-log.md`.

**Done when:** there is a clear decision. "Good work, let's discuss next week" is not a decision.

> **Watch out.** Do not bring a polished slide deck — it suggests the work cannot speak for itself.
> Write the decision down **before anyone leaves the room**. A decision that is not written down
> did not happen.

## Stage 07 — Engineering refinement

**Who:** the pair and senior Engineering partners, in live meetings (not a Claude session). Runs
from the playback decision until an agreed end date. Pick a real date and keep to it.

**Goal:** a scope and design direction that is clear enough for Product, Design and Engineering to
plan against.

**Push back on:**

- **Extra scope presented as a technical need.** "While we're in there…" is not a technical
  constraint.
- **Preferences presented as constraints.** Ask exactly what makes it hard.
- **Reopening the direction.** What Engineering learns can change *how* you build it. It can only
  change *what* you build if a key assumption turns out to be false. If that happens, go back to
  `03_converge` on purpose — do not drift there.
- **Endless exploring.** This stage does not turn into more exploration.

**Done when:** all three disciplines say the words *"I can plan against this."* Anything weaker
means no.

## Stage 08 — Vision horizon

**Who:** the named owner, with the pair. It can run at the same time as `07`. **Do not let it
slip.** This is the main deliverable of the whole process. If time runs short, cut polish in
`04` — never cut `08`.

**It produces:**

- the bet, in one sentence
- Now / Next / Later, with how each depends on the one before
- the capabilities gained
- what you are betting against
- the owner's name

> **Watch out.**
> - **A roadmap in disguise:** three horizons that are really just three release dates.
> - **Ambition with no mechanism:** "seamless, intelligent company management" with no
>   explanation of how it becomes true.
> - **Forced AI:** if AI is not central to the bet, say so plainly. A forced AI story is worse than
>   no AI story.

**Done when:** someone who works on the product, but not on this run, can hear the one sentence and
disagree with it.

## Stages 09 and 10 — Report and prototype handoff (optional)

**Who:** the pair, with the named owner. Any time after `08`. Nothing waits on these stages.

Run them when the position needs to reach people outside the team. Skip them when the run only
feeds into stage `99`. Skipping them is a normal end state, not an unfinished run.

**If your run folder does not have `09_report` or `10_prototype-handoff`** (because it was created
before these stages existed), copy them in first. From the workspace root, run these three
commands, replacing `<run>` with your run folder name:

```
cp _template/09_report/CONTEXT.md <run>/09_report/CONTEXT.md
cp _template/10_prototype-handoff/CONTEXT.md <run>/10_prototype-handoff/CONTEXT.md
mkdir -p <run>/09_report/output <run>/10_prototype-handoff/output/prototype-briefs
```

Or ask Claude: *"Add the `09_report` and `10_prototype-handoff` stages from `_template` to `<run>`."*

### `09_report`

**What it does:** turns `vision-horizon.md` into one self-contained HTML page. Claims are on the
surface. The evidence for each claim is one click below it. Sources are listed and dated at the
bottom. It exists because a markdown file does not survive a stakeholder meeting — someone pastes
it into a deck and it becomes six bullet points written by someone else.

**How it works:**

1. The stage first fills in a structured file (`content.yaml`) from the earlier stages' outputs.
   It does this before writing any HTML.
2. When an input is missing or empty (for example `03_converge` was skipped, or `house-view.md` is
   blank), it does **not** invent content. It records the gap in `gaps.md`.
3. It then shows you all the gaps together. For each one, you choose: cut the claim, turn it into
   a caveat, or give the source yourself.

**Output:** `content.yaml`, `gaps.md` and `vision-report.html`, in `09_report/output/`.

> **Watch out.**
> - The report adds nothing new. If the report is wrong, `08` is wrong. Fix `08`, not the report.
> - On a thin run, do not add filler to make the page look complete.
> - Do not remove the caveats to make the page sound stronger. It sounds stronger and convinces
>   fewer people.

**Done when:** a reader can go from the number they trust least to where it came from, in one
click, on screen and on paper.

### `10_prototype-handoff`

**What it does:** turns the position into a brief that the your prototyping tool can build from. It
writes the instructions, not the prototype. The target is a mid-fidelity UI shell that uses the
right components, so it looks and feels right. **It is not a working prototype.** Each screen
answers one question that could be proven wrong. If a horizon has no sourced moment that can be
shown on screen, it gets no screen.

**How it works:** before it writes anything, the stage runs an **"ask, don't invent" checklist**.
It asks you one question at a time about anything it cannot find clearly in this run's files:

- the exact on-screen text, if the vision file does not give the wording
- which persona to use
- whether a new data fixture is needed
- the `productArea` for the hub entry
- the `owner:` value (see below — this must be exact)
- the slug, if there is more than one sensible option

Do not let Claude guess these and present them as decided. An early run that skipped this checklist
produced a brief with a made-up persona, a made-up booking and made-up ad text. It all looked
believable, and none of it came from the owner.

**Before you run it — check the owner's exact name.** If your prototyping tool gates edits on the
author's name (for example `git config user.name` in the tool's own repo), check the exact value
**in that repo** and use it as the `owner:` value. It can differ from your global settings. If it
is wrong, later edits may be blocked without a clear error, long after this step.

**Output:** `prototype-briefs/<slug>.md` and `HANDOFF.md`, in `10_prototype-handoff/output/`.

**Done when:** someone who has not read the vision can say what question the prototype answers —
as a question, not as a feature description.

### Top-level versions: `100-report` and `101-prototype-handoff`

The same two steps also exist at the workspace root, as `100-report/` and `101-prototype-handoff/`.
They work from the combined vision (stage `99`) instead of one run. Use the run-level versions
when a screen belongs to one run's sphere of influence. Use the top-level versions when it spans
two or more.

## Stage 99 — Synthesis

**Who:** the orchestrator, plus the owners of each run. After every run in scope has finished `08`.

**The rule: do not just join the runs together.** Two area visions side by side are not a product
vision. The team will see that as "no vision, just workstreams." The synthesis must find a
through-line that no single run found on its own.

**Then make the partner version:** a commercial argument rather than a product story. **Label what
is committed and what is aspirational, honestly.** Presenting an aspiration as a commitment is the
fastest way to lose that audience.

**The real test:** after reading it, could an engineer on the product say what the product is becoming? The quality of
the analysis does not matter if it does not change what the team believes. That belief is the
deliverable.

## When things go wrong

| What you see | Likely cause | What to do |
|---|---|---|
| Still stuck in `01` on day two | The problem is too broad | Force a cut: which one thing makes the rest easier, or not needed? |
| All the options look the same | The pair chose too early, under time pressure | Ask them for one option they would hate to build |
| Nothing broke in `05` | Looking for proof, not trying to break it | Run the pre-mortem properly, or bring in the known sceptic |
| Playback ends with no decision | The pitch started with the story, not the answer | Meet again within 48 hours, and state the ask first |
| Engineering wants to reopen the direction | A key assumption may be false | Find out which one. If it really is false, go back to `03`. If not, hold the line. |
| `08` keeps slipping | It is treated as a write-up, not the deliverable | It is the deliverable. Cut polish in `04` instead. |
| The output feels generic | `_shared/house-view.md` is thin | Fix that file, not the stage folders |
| A stage's instructions feel wrong | They probably are | Rewrite them in `_template`, then run `./eval` to check nothing broke |
| A stage keeps answering questions you should answer | `/run-pipeline` is guessing instead of asking | Run that stage by hand instead, or answer its list of questions directly |

## Rules that do not change

1. Load only what the stage names. Do not point Claude at the whole workspace.
2. One home for each fact. If it is in `_shared`, point to it — do not copy it.
3. Change `_template`, never a live run.
4. Every session ends with a saved file.
5. No polished slide deck at the playback.
6. Stage `08` is not optional.

---

*Related files: `README.md` (what this is and why) · `CLAUDE.md` (the map) ·
`CONTEXT.md` (the structure) · `_shared/CONTEXT.md` (the shared reference files)*
