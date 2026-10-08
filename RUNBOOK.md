# Runbook

The facilitator's guide. `README.md` covers how to open the workspace and type commands. This file
covers how to run the process with people: the order, who is involved, and what goes wrong.

> **This is a guide, not a fixed schedule.** You can change the order, skip ahead, or go back. One
> rule is fixed: **every stage saves a file**, so the next stage has something to work from.

- **Part 1 — The path through a run.** The usual order, start to finish.
- **Part 2 — Stage-by-stage reference.** What each stage is for, who is involved, what goes wrong.

---

# Part 1 — The path through a run

| # | What | How | Output |
|---|---|---|---|
| 1 | Pick the problem | One sentence, plus a short slug (`expense-capture`). Check no existing run already covers it — if one does, work in that run | — |
| 2 | Shared context *(first run only)* | Check `_shared/product-context.md`, `house-view.md` and `timeline.md` are filled and current. See README → Full setup | — |
| 3 | Create the run | `new <slug>` | `NN-<slug>/CLAUDE.md` filled |
| 4 | Setup | `work <run>/00_setup` — skippable for small or solo runs | `inventory.md` |
| 5 | **Kickoff** | **Live meeting.** Name the owner of the 12-month view out loud | — |
| 6 | Frame → Pressure-test | `work <run>` for each of `01`–`05`, one conversation per stage | `frame.md` … `pressure-test.md` |
| 7 | **Playback** | **Live meeting with leadership.** Use `work <run>/06_playback` to prepare and to write up | `playback.md` |
| 8 | **Engineering refinement** | **Live meetings with Engineering.** Same: Claude preps and writes up | `solution-scope.md` |
| 9 | Vision horizon | `work <run>/08_vision-horizon` — can run alongside `07` | `vision-horizon.md` |
| 10 | Report / handoff *(optional)* | `work <run>/09_report`, `work <run>/10_prototype-handoff` | `vision-report.html`, `prototype-briefs/*.md` |

**After every stage:** open the output file, do the **Human check** from that stage's `CONTEXT.md`,
and edit the file if you disagree. The next stage reads whatever you leave. Then start a fresh
conversation (`/clear`) before the next stage.

**Where is a run up to?** Type `status <run>`, or look in each stage's `output/` folder in Finder.
A file there means done.

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

1. **Start Claude Code at the workspace root**, never inside a run or stage folder. The root
   `CLAUDE.md` only loads from there, and the stage files' relative paths only resolve from there.
2. **Use a fresh conversation for each stage.** Type `/clear` between stages. In one long chat,
   earlier stages leak into later ones and Claude's questions get weaker.

## Day 0 — Setup (stage 00)

**Who:** each pair, on their own. **A few hours at most** — not a fourth working day.

**Do:**

1. If not done yet for this workspace: answer `_shared/setup-questionnaire.md` and write the answers
   into `_shared/product-context.md`.
2. List what exists: research (mark anything older than one year), Productboard, analytics, earlier
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

**If your run folder does not have `09_report` or `10_prototype-handoff`** (it was created before
these stages existed), ask Claude: *"Add the `09_report` and `10_prototype-handoff` stages from
`_template` to `<run>`."*

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

**What it does:** turns the position into a brief that the prototyping tool named in
`_shared/prototype-target.md` can build from. It
writes the instructions, not the prototype. The target is a mid-fidelity UI shell that uses the
right components, so it looks and feels right. **It is not a working prototype.** Each screen
answers one question that could be proven wrong. If a horizon has no sourced moment that can be
shown on screen, it gets no screen.

**How it works:** before it writes anything, the stage runs an **"ask, don't invent" checklist**.
It asks you one question at a time about anything it cannot find clearly in this run's files:

- the exact on-screen text, if the vision file does not give the wording
- which of the tool's personas to use
- whether a new data fixture is needed
- the area / taxonomy tag for the hub entry
- the owner value (see below — this must be exact)
- the slug, if there is more than one sensible option

Do not let Claude guess these and present them as decided. An early run that skipped this checklist
produced a brief with a made-up persona, a made-up booking and made-up ad text. It all looked
believable, and none of it came from the owner.

**Before you run it — check the owner's exact name, in the form the tool expects.**
`_shared/prototype-target.md` says what that is (for example, `git config user.name` run inside the
tool's repo — not this workspace, not your global settings; they can differ). Some tools only allow
later edits to a screen when this name matches exactly, and fail without a clear error if it
doesn't. If `prototype-target.md` is blank, the stage writes plain design briefs instead.

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

**The real test:** after reading it, could an engineer on the product say what it is becoming? The quality of
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
| A stage answers its own questions | Claude is guessing instead of asking | Say "ask me, one question at a time". If it repeats, tighten that stage's `CONTEXT.md` in `_template` |

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
