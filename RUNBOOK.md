# Runbook

How to actually run this. Two parts:

- **Part 0** — the solo test run. Do this first, before anyone else touches the process.
- **Part 1** — the full workshop process, start to finish.

Read `README.md` first if you haven't. This document assumes you know what the workspace is for.

> **This is a runbook, not a schedule.** There is no required daily process baked into the method
> itself. What follows is the order these moves usually happen in and roughly how long they take.
> Deviate freely. The only fixed rule is that each move leaves a file behind, so the next one has
> something to stand on.

---
---

# PART 0 — The solo test run

**Time:** ~2.5 hours, best split across two sittings.
**Who:** you, alone.
**Purpose:** find out whether the process does real work, before you ask a senior pair to spend
protected days inside it.

## 0.1 What you are trying to prove

Six claims. Five you can test alone. One you cannot — and it is the most important.

| # | Claim | How you'll know | Testable solo? |
|---|---|---|---|
| **H1** | The stages do work, not just organise it | `01_frame` **changes your mind** about the problem, rather than tidying what you already thought | Yes |
| **H2** | Divergence is forced, not politely requested | `02_explore` gives three different **bets**, not three UIs for one bet | Yes |
| **H3** | The process extracts trade-offs | `03_converge` makes you say something out loud you'd rather have left vague | Yes |
| **H4** | Stage 08 produces a position, not a roadmap | A colleague could **disagree** with the one-sentence vision | Yes |
| **H5** | The house view is load-bearing | Pass 2 of `01_frame` (house view filled) is visibly sharper than pass 1 | Yes |
| **H6** | **It runs without you in the room** | A pair reaches a defensible position with no input from you | **No** |

**On H6.** This is the claim the whole programme rests on — your goal is that senior people drive
vision in their own area, not that you steer the ship. Your solo test cannot check it. By
definition, you are in the room. The only real test is watching a pair run `01_frame` while you
stay out. Plan for that now; don't let a clean solo run convince you H6 is proven.

## 0.2 Two mechanics to get right before you start

**Always work from the workspace root**, not from inside a stage folder. Two reasons: the root
`CLAUDE.md` only loads automatically when the root is your working directory, and the stage
contracts use paths like `../../_shared/...` written to resolve from the stage folder's position in
the tree, not from wherever you happen to have opened a terminal.

**Use a fresh session for each stage.** One long conversation across all four stages defeats the
design — context bleeds between stages and you end up testing a long chat rather than the pipeline.
A new session per stage is how the pairs will work, so it's what you should test.

---

## 0.3 Phase A — Choose the problem (10 min)

**Step 1.** Write your candidate test problem in one sentence, somewhere scratch.

**Step 2.** Check it against three rules. If it fails any, pick again.

| Rule                                                    | Why                                                                                                           |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Not** one of the real problem spaces you're about to run for real | If you frame that first, the pair inherits your framing — and you've undercut the thing you said you wanted |
| **Not** something you've already solved in your head    | If you know the answer, H1 is untestable. Nothing can change your mind.                                       |
| Real enough that you'd recognise a bad answer            | A toy problem tests nothing                                                                                   |

**Step 3.** Write a two-to-four word slug for it, lowercase, hyphenated — e.g. `expense-capture`.
You'll use it in the folder name.

---

## 0.4 Phase B — Fill the facts, withhold the opinion (15 min)

**Step 4.** Open two files side by side:

- `_shared/product-context.md` — the one you're filling
- `_shared/setup-questionnaire.md` — the prompts that fill it

**Step 5.** Fill **only** the sections your test problem actually touches. For most problems that's
four of the seven:

| Section | Fill? |
|---|---|
| `## Product` | Yes — always |
| `## Customers & segments` | Yes — always |
| `## Current state numbers` | Yes — whatever numbers bear on your problem |
| `## Constraints` | Yes — the real ones, not the assumed ones |
| `## Commercial` | Only if your problem has a revenue angle |
| `## Existing assets` | Skip for the test |
| `## Competitive / positioning context` | Skip unless your problem touches it |

**Step 6.** Mark anything you're unsure of with `[assumption]`. Save.

> **Gotcha — the big one.** Fifteen minutes, not an hour. Perfectionism here eats the test. A rough
> answer in the file beats a perfect one in your head. You're filling this so `01_frame` doesn't
> stall, not so it's complete.

**Step 7.** Open `_shared/house-view.md` and confirm it still says `STATUS: EMPTY`. Do not fill it.
That's your test variable for H5. Close it.

---

## 0.5 Phase C — Create the test run (5 min)

**Step 8.** From the workspace root, copy the blank method:

```
cp -R _template 03-test-<slug>
```

Use your slug from Step 3. No date needed — this folder is temporary.

**Step 9.** Open `03-test-<slug>/CLAUDE.md` and fill the identity block:

- **Problem space** — your one sentence from Step 1
- **Questions in scope** — two or three
- **Sphere of influence** — which part of the product this run would own a view over
- **Pair** — write `<your name> (solo test)`
- **Owner of the 12-month view** — write `<your name> (solo test)`

**Step 10.** Delete the whole `## Run-specific notes by stage` section, including the blockquote.
You have nothing to put there, and four stage contracts point at it — an empty promise is worse than none.

**Step 11.** Save, then verify the copy worked:

```
ls 03-test-<slug>/
```

You should see eleven numbered stage folders — the nine core stages plus the optional `09_report`
and `10_prototype-handoff` — a `CLAUDE.md` and a `CONTEXT.md`.

---

## 0.6 Phase D — Run four stages (~90 min)

Four stages, eight steps. Each stage is: run it, then do the human check.

You're skipping `00` and `04`–`07`. That's legal, not a workaround — `08` has an explicit carve-out
to run on `03`'s output alone. Those stages need real artefacts and other people; simulating them
teaches you nothing.

---

### Step 12 — Run `01_frame` (30 min)

Start a **new session** from the workspace root. Say:

> `work 03-test-<slug>/01_frame`

What should happen: the stage contract is read, `operating-principles.md` and `house-view.md` load,
and you get interrogated — not asked what you'd like written.

Expect roughly: the problem behind the problem · whose problem it is · customer vs business outcome · evidence both ways · which assumptions are load-bearing · what you're choosing *not* to solve.

**Output:** `03-test-<slug>/01_frame/output/frame.md`

### Step 13 — Human check on `01_frame`

Open `frame.md`. Read the problem statement **out loud**.

- If it could not possibly be wrong, it says nothing. Rewrite it.
- Edit anything you disagree with, directly in the file. The next stage reads whatever you leave.

**Record for H1:** did this change your mind, or just tidy what you already thought?

---

### Step 14 — Run `02_explore` (25 min)

**New session**, from the workspace root:

> `work 03-test-<slug>/02_explore`

It should read `frame.md` as input and refuse to rank anything.

**Output:** `03-test-<slug>/02_explore/output/options.md`

### Step 15 — Human check on `02_explore`

Open `options.md`. Point at the option that makes you uncomfortable.

- If there isn't one, the set is too narrow. Go again.
- Apply the test: if two options would be built by the same team in the same sequence, they are one option.

**Record for H2:** three different bets, or three UIs for one bet?

---

### Step 16 — Run `03_converge` (20 min)

**New session**, from the workspace root:

> `work 03-test-<slug>/03_converge`

**Output:** `03-test-<slug>/03_converge/output/direction.md`

### Step 17 — Human check on `03_converge`

Find the trade-off sentence — the "we are choosing X, which means we accept worse ______" line.
Read it to someone who wasn't involved.

- If they don't wince slightly, it isn't a real trade-off.

**Record for H3:** did it make you say something you'd rather have left vague?

> **Break here.** The attention curve is heavy–light–heavy. Come back for stage 08 fresh.

---

### Step 18 — Run `08_vision-horizon` (25 min)

**New session**, from the workspace root:

> `work 03-test-<slug>/08_vision-horizon`

It will note that `07` hasn't run and proceed on `03`'s output — that's the designed carve-out, not
an error.

**Output:** `03-test-<slug>/08_vision-horizon/output/vision-horizon.md`

### Step 19 — Human check on `08_vision-horizon`

Take the one-sentence version to someone who works on the product but not on this problem. Ask them
to disagree with it.

- If they can't find anything to disagree with, it isn't a position yet.

**Record for H4:** a position, or a roadmap in a trenchcoat?

---

## 0.7 Phase E — The house-view A/B (40 min)

This is the actual experiment. Everything before it was setup.

**Step 20.** Open `_shared/house-view.md`. Fill all six sections:

`What good looks like` · `What you kill on sight` · `Your standing trade-offs` ·
`What outsiders get wrong` · `Evidence` · `Where the job breaks`

Answer the way you'd explain it to a new senior hire over coffee. Specific and opinionated, not
balanced. A house view nobody could disagree with will do nothing.

**Step 21.** Start a **new session**. Run `01_frame` again on the **same problem**:

> `work 03-test-<slug>/01_frame` — save the output as `frame-pass2.md`, keep `frame.md` intact

**Step 22.** Open `frame.md` and `frame-pass2.md` side by side.

| | |
|---|---|
| **Pass** | Pass 2 names a problem pass 1 missed, kills an option pass 1 entertained, or applies a standard pass 1 didn't have. It reads like a colleague who knows the business, not a competent consultant. |
| **Fail** | Same analysis, different adjectives. |

**Step 23.** If it failed: the house view file is wrong — too abstract, too balanced, or restating
generic good practice. Rewrite it sharper and repeat Steps 21–22. **Do not conclude the folders are
broken.** That's H5 doing its job.

---

## 0.8 Phase F — Close out (20 min)

**Step 24.** Port every fix you found into `_template/`. Not into your test copy — fixes made there
die when you delete it.

**Step 25.** If you changed any structure, re-run the walk test (command and criteria in `CLAUDE.md`).

**Step 26.** Either delete `03-test-<slug>`, or rename it `_archive-test-<slug>` and keep it. A real
filled-in example is worth more to the pairs than instructions are.

**Step 27.** Write anything you learned about *how product work should go here* into
`_shared/house-view.md`. After this test, that file is the most valuable thing in the workspace.

**Step 28.** Decide: ready for the pairs on kickoff day, or does a stage contract need rewriting first?

---

## 0.9 Gotchas

| Don't | Why it matters |
|---|---|
| Answer the interrogation in your head | If it isn't in the file, the next stage can't use it — and you haven't tested the handoff |
| Run all four stages in one session | Context bleeds. You'd be testing a long chat, not the pipeline. |
| `cd` into the stage folder | The root map won't load and relative paths resolve wrong |
| Rank options during `02_explore` | Everyone does this. The contract should stop you — if it doesn't, that's a finding. |
| Judge output quality instead of stage function | Good output from a stage that didn't do its job means *you* did the work and the process took the credit |
| Fix your test copy | Every fix belongs in `_template` |
| Spend an hour on `product-context.md` | Fifteen minutes. Perfectionism here eats the test. |
| Pick a problem that makes the process look good | You're testing it, not showcasing it |

---
---

# PART 1 — The full process

**Total span:** roughly two to three weeks from kickoff to a plan-ready scope, plus a later
partner/commercial readout if you have one. Set real dates before you start — see the shape below.

## Roles at a glance

| Who | Where they appear |
|---|---|
| Product + Design pair | Owns `00`–`06` and `08` jointly. Not Product specifying and handing over. |
| Cross-functional leadership | Kickoff framing, SME on call, the decision at playback |
| Senior Engineering partners | Join **after** the decision, for `07` |
| Domain SMEs / customer-facing colleagues | Twenty-minute pulls during `01` and `05` |
| Named owner of the 12-month view | One per problem area. Owns `08`. Should not default to whoever runs the programme. |
| You (the programme owner) | Frame it, protect the time, remove blockers, then **get out of the room** |

---

## Stage 00 — Setup (Day 0)

**Who:** each pair, separately. Time: 1–2 hours. **Not a fourth working day.**

**Do:**

1. Walk `_shared/setup-questionnaire.md`, write answers into `_shared/product-context.md`.
2. Inventory what exists — research (flag anything over a year old), roadmap tool entries,
   analytics, prior designs, design-system assets, SMEs.
3. Test **access**, not content. An asset you can't open on day one is the failure mode.
4. Classify gaps: blocking / degrading / ignore.
5. Book the SME time you'll need in `01` and `05`.

**Output:** `00_setup/output/inventory.md`, and `_shared/product-context.md` populated.

**Done when:** you can open everything on the list, and reading your own context file teaches you
something.

> **Gotcha.** This stage attracts real work like a magnet. If a pair starts framing the problem on
> day 0, stop them. The boundary is the whole value of the stage — and they'll burn the energy
> they need on day one.

---

## Kickoff (Day 1, morning)

**Who:** leadership + both pairs. Time: 60–90 min.

**Cover:**

1. Why we're doing this — the vision gap, plainly stated.
2. Unpack each problem space.
3. What "decision-ready" means here.
4. Which boundaries are deliberately removed — role boundaries, process, permission to challenge.
5. **Name the owner of each 12-month view.** Out loud, in the room.

**Then leave.** The pair takes over. Your remaining job is blockers and SME access.

> **Gotcha.** The temptation is to spec the problem while framing it. Don't. Frame the *challenge*
> and the *outcome*; the pair defines the problem in `01_frame`. If you hand them a problem
> statement, you've made them executors and you'll get execution back.

---

## Stages 01–05 — The protected days

These are **thinking moves, not daily gates**. Run them in whatever order gets to the strongest
outcome. Prototype while still exploring. Go back and reframe when something changes your thinking.

| Stage | Move | Output | Typical |
|---|---|---|---|
| `01_frame` | What are we really solving? | `frame.md` | Half a day |
| `02_explore` | Materially different approaches | `options.md` | Half a day |
| `03_converge` | Make the call, own the trade-off | `direction.md` | 2 hours |
| `04_make-tangible` | Something people can react to | `artefact-notes.md` + prototype | A day |
| `05_pressure-test` | Attack it before leadership does | `pressure-test.md` | Half a day |

**Attention shape:** heavy in `01`, light through `02`–`04`, heavy again in `05`. Correction is
cheapest at the earliest gate — an hour in `01_frame` is worth a day in `05`.

**Per-stage gotchas:**

- **`01`** — Framing too broad to resolve in a few days, or so narrow it yields a feature. Also:
  treating a low number as a UX problem when it's motivation, trust, or timing.
- **`02`** — The pair converges early because divergence feels wasteful under time pressure. It
  isn't. Three options that differ only in UI is one option.
- **`03`** — False consensus. Agreement reached because nobody wanted to spend the time disagreeing.
  Make them write the trade-off sentence down.
- **`04`** — Fidelity creep. A beautiful screen that never says how the system *knows* something.
  Resolve the moments that carry the bet; leave the rest grey and say so.
- **`05`** — Validation-seeking instead of attacking. If nothing changed, be suspicious. Also: pull
  an engineer in **now** for any technical assumption that could change the direction. Don't carry
  it into the decision.

**Pair health check.** If Product did `01`–`03` and Design did `04`, the pairing failed and the
output will show it. Both names on every file.

---

## Stage 06 — Playback and decision

**Who:** pair + leadership group. **A decision point, not a showcase.**

**Running order:**

1. Recommendation first, not the journey.
2. The trade-off, early — it invites the real conversation.
3. The three frames that carry the argument.
4. Remaining risks, classified.
5. What's needed from Engineering.
6. The 12-month view — draft. Leadership will ask; a direction with no horizon reinforces the exact
   problem this programme exists to fix.
7. State the decision being asked for, and what happens if it isn't made.

**Output:** `06_playback/output/playback.md`, plus the decision and its conditions appended to
`_shared/decision-log.md`.

**Done when:** a clear decision exists. Not "good work, let's discuss next week."

> **Gotchas.** No deck — a deck signals the artefact can't carry itself.
> Write the decision down *before leaving the room*; a decision not written down did not happen.
> And if the session ends with only slides or a good feeling, it failed.

---

## Stage 07 — Engineering refinement

**Who:** pair + senior Engineering partners.

**Target:** an agreed, sufficiently resolved scope and design direction that Product, Design and
Engineering are all comfortable planning against.

**Hold the line on:**

- **Scope creep dressed as feasibility.** "While we're in there" is not a technical constraint.
- **Preference claims wearing constraint clothing.** Ask what makes it hard, specifically.
- **Reopening the direction.** Engineering learning changes *how*. It reopens *what* only if a
  load-bearing assumption is proven false — and then you go back to `03_converge` explicitly, not
  by drifting.
- **The open-ended phase.** This does not roll into more exploration.

**Done when:** all three disciplines say the words *"I can plan against this."* Anything softer is a no.

---

## Stage 08 — Vision horizon

**Who:** the named owner, with the pair. Can run alongside `07`. **Must not slip past your
definition-of-done date.**

This is the deliverable the programme is named after. If time runs short, cut fidelity in `04`,
never this.

**Produces:** the bet in one sentence · Now / Next / Later with stated dependency between them ·
capabilities gained · what you're betting against · the owner's name.

> **Gotchas.** Roadmap in a trenchcoat — three horizons that are just three release trains. And
> aspiration with no mechanism: "seamless, intelligent X" with no account of how it becomes true.
> If AI is incidental to the bet, say so plainly; a forced AI framing is worse than an honest
> absence.

**Done when:** someone who works on the product but not on this run can hear the one sentence and
disagree with it.

---

## Stages 09 and 10 — Report and prototype handoff (optional)

**Who:** the pair, with the named owner. Any time after `08`. Nothing waits on these.

Run them when the position needs to leave the room it was written in. Skip them when the run is
feeding straight into `99` and the only reader is the synthesis. Skipping is a legitimate end
state, not an incomplete run.

**If the run was created before these stages existed**, `09_report/` and `10_prototype-handoff/`
won't be in it. Copy them in before running — mechanical, not a judgment call:

```
cp _template/09_report/CONTEXT.md <run>/09_report/CONTEXT.md
cp _template/10_prototype-handoff/CONTEXT.md <run>/10_prototype-handoff/CONTEXT.md
mkdir -p <run>/09_report/output <run>/10_prototype-handoff/output/prototype-briefs
```

### `09_report`

Renders `vision-horizon.md` as one self-contained HTML file: claims on the surface, evidence folded
into `<details>` under each one, sources dated at the bottom. It exists because markdown doesn't
survive a stakeholder room — it gets pasted into a deck and becomes six bullets someone else wrote.

**What actually happens when you run it:** the stage fills a schema (`content.yaml`) from named
upstream inputs first, before writing any HTML. Where an input is missing or empty — `03_converge`
skipped, `05_pressure-test` never run, `house-view.md` still blank — it logs the gap in `gaps.md`
instead of inventing content, then brings the list to you as one decision block: cut the claim,
demote it to a caveat, or source it yourself. Expect this on any run that skipped stages, which
includes every solo test.

**Output:** `content.yaml`, `gaps.md`, `vision-report.html` → `09_report/output/`.

> **Gotcha.** The stage asserts nothing new — if the report reads wrong, `08` is wrong; fix it
> there, don't patch the render. Don't pad the page to fill the design system's full rhythm on a
> thin run. Don't drop the caveats because the page reads stronger without them — it reads stronger
> and lands weaker.

**Done when:** a reader can get from the number they trust least to its working in one click, on
screen and on paper.

### `10_prototype-handoff`

Converts the position into a brief a prototyping tool can build from — not the prototype itself,
the instructions for it. Target: a mid-fi UI shell using the right components for a solid look and
feel. **Not a working prototype.** One surface per falsifiable question; a horizon with no sourced,
screen-able moment gets no surface at all — infrastructure-shaped horizons usually don't.

**What actually happens when you run it:** before drafting anything, the stage runs an **"ask,
don't invent" checklist** — one question at a time, per `operating-principles.md` — for every slot
it can't source unambiguously from this run's own docs:

- the exact on-screen copy, if the vision doc doesn't supply literal wording
- which persona to cast, and whether the example should be specific or generic
- whether a new data fixture is needed, and how specific it should be
- the taxonomy area for the hub entry, when the surface sits on a genuine boundary
- who owns the write — see the gotcha below, non-negotiable
- the slug, if more than one reasonable option exists

Don't let an agent guess these and present them as settled. A first pass that skipped this step
produced a brief with an invented persona, an invented booking and invented ad copy — all
plausible-looking, none of it something the owner actually said.

**Output:** `prototype-briefs/<slug>.md`, `HANDOFF.md` → `10_prototype-handoff/output/`.

> **Before running it**, this stage's contract in `_template/10_prototype-handoff/CONTEXT.md`
> assumes you have your own prototyping tool with its own brief-consumption contract (an equivalent
> of "here's the exact `owner:` string it gates writes on, here's the file it reads"). Point the
> stage at your tool's own docs the same way `_shared/CONTEXT.md` points stages at `_shared/` — by
> exact path, named in that run's `CLAUDE.md`. If you don't have such a tool yet, treat this stage's
> output as a design brief for a human, not a machine-consumable contract.

**Done when:** someone who hasn't read the vision can say what question the prototype answers — as
a question, not a feature description.

The same two steps exist at the top level as `100-report/` and `101-prototype-handoff/`, running
off the synthesised vision rather than one run's. Same method, wider claim. Use the run-level pair
when a surface sits inside one sphere of influence; use the top-level pair when it needs two.

---

## Stage 99 — Synthesis

**Who:** the programme owner, plus both owners. After both runs finish `08`.

**The rule:** do not staple. Two domain visions side by side is not a product vision — it's the
"vision by aggregation" failure, and the team will read it as one. The synthesis must produce a
through-line neither run produced alone.

**Then the partner cut, if you have one:** commercial thesis rather than product story, and
**committed vs aspirational labelled honestly.** Aspirational framed as committed is the fastest
way to lose that room.

**The real test:** would an engineer on the product, having read it, be able to say what the
product is becoming? Quality of analysis is irrelevant if it doesn't change what the team
believes. That belief is the deliverable.

---

## When things go wrong

| Symptom | Likely cause | Move |
|---|---|---|
| Pair is stuck in `01` on day two | Framing too broad | Force the cut: what one thing makes the rest easier or irrelevant? |
| Options all look the same | Converged early under time pressure | Make them generate one option they'd hate to build |
| Nothing broke in `05` | Validation-seeking, not attacking | Run the pre-mortem properly, or bring in the known sceptic |
| Playback ends without a decision | Recommendation led with journey, not answer | Reconvene within 48h with the ask stated first |
| Engineering wants to reopen the direction | A load-bearing assumption may be false | Check which one. If genuinely false, return to `03`. If not, hold. |
| `08` keeps slipping | It's being treated as a write-up, not the deliverable | It is the deliverable. Cut `04` polish instead. |
| Output feels generic | `_shared/house-view.md` is thin | Fix the file, not the folders |
| A stage contract feels wrong | It probably is | Rewrite it in `_template`, re-run the walk test |

---

## Rules that don't bend

1. Load only what the stage names. Don't point the assistant at the whole folder.
2. One home per fact. If it's in `_shared`, point at it — don't restate it.
3. Change `_template`, never a live run.
4. Every session ends in a file.
5. No polished deck at playback.
6. Stage `08` is not optional.

---

*Companion documents: `README.md` (what this is and why) · `CLAUDE.md` (the map) ·
`CONTEXT.md` (the shape) · `_shared/CONTEXT.md` (the reference layer)*
