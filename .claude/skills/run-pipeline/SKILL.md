---
name: run-pipeline
description: Orchestrate a product-discovery run (01-<run-slug>, 02-<run-slug>, a 03-test-* solo run, etc.) stage by stage — 00_setup through 10_prototype-handoff — automating the choreography of moving between stage folders while keeping every human interrogation and human-check gate the RUNBOOK requires. Use when the user wants to "run the pipeline", "orchestrate a run", "kick off the next stage automatically", or move a run forward without manually starting a new session per folder.
allowed-tools: Read, Bash, Agent, AskUserQuestion, Edit
---

# run-pipeline

**Usage:** `/run-pipeline <run-folder>` — e.g. `/run-pipeline 01-<run-slug>`. If no
folder is given, ask which run (list root-level folders that contain a `01_frame` subfolder — that
excludes `_template`, `99-vision-synthesis`, `100-report`, `101-prototype-handoff`, which aren't
per-run pipelines).

You are the orchestrator, not the worker. You never do a stage's actual thinking yourself and you
never invent answers on a pair's behalf. Your job is only: move between folders, launch a fresh
agent to do each stage's real work, surface its output, and run the human-check gate — exactly
what a person would otherwise do by hand, one new session at a time.

## Why fresh agents, not you doing it inline

`RUNBOOK.md` §0.2 is explicit: **"Use a fresh session for each stage... context bleeds between
stages and you end up testing a long chat rather than the pipeline."** So every stage's work is
delegated to a brand-new subagent with zero prior context — never a `fork` (a fork inherits this
conversation's context, which is exactly the bleed the design forbids). You (the orchestrator) are
allowed to accumulate context across stages — you're not the one doing the thinking, just the
choreography — but the worker agent for each stage must start clean every time.

## `AskUserQuestion` is not available to worker agents — hand back, don't work around it

Confirmed by direct test (two `ToolSearch` attempts inside a live worker, both empty): a subagent
launched via `Agent` cannot call `AskUserQuestion`, no matter what tools its type nominally grants.
Only you, the orchestrator, have a live channel to the human. Do not have the worker attempt the
call, and do not have it invent answers to route around the gap — both break the one rule that
matters more than anything else in this skill (never fabricate on the pair's behalf).

Instead, every stage whose contract requires a live answer runs in **two turns of the same worker
agent**, not one:

1. **Launch** the worker as normal. Its job this turn is to load context and prepare the
   interrogation — not to answer it. It ends its turn by handing back the full list of questions
   it needs the human to answer (sharpened per the stage's `## Process` and any blind-spots list),
   and it does **not** write the stage's output file yet.
2. **You ask** those questions to the human yourself, with `AskUserQuestion`, in this conversation
   — free text via "Other" where it isn't a clean choice — using the worker's exact question list
   as written (you're relaying, not re-deriving; if you'd sharpen a question further, that's a sign
   the worker's list was thin, not an invitation to improvise one).
3. **You resume the same worker** (`SendMessage` to its agent id — never a fresh `Agent` call,
   which would lose the context it built loading this stage's inputs) with the human's answers
   verbatim, and tell it to now write the stage's output file from those answers, per its own
   `## Outputs` section.

A stage with no live-answer requirement (pure templating, e.g. rendering an already-settled
position) can just write its output in one turn — don't force the two-turn pattern where nothing
needs asking.

## Stage order and what's automatable

Fixed order, but only act on stage folders that actually exist under the run:

| Stage | Automatable? | Model | Why |
|---|---|---|---|
| `00_setup` | Yes | sonnet | Inventory + access check — mechanical, no judgment call worth paying for |
| **Kickoff** | No — pause | — | Not a folder. Needs leadership + both pairs live. Just confirm it happened before `01`. |
| `01_frame` | Yes | opus | `RUNBOOK.md`'s attention shape is heavy here — cheapest gate to get right, adversarial interrogation |
| `02_explore` | Yes | sonnet | Attention shape is light here — still needs real divergence, not the hardest judgment call |
| `03_converge` | Yes | sonnet | Attention shape is light here — but see the override note below |
| `04_make-tangible` | Yes | sonnet | Attention shape is light here — executional, not the bet itself |
| `05_pressure-test` | Yes | opus | Attention shape is heavy again — adversarial, must actually find the break, not perform one |
| `06_playback` | No — pause | — | Live decision session with leadership. Cannot be run by an agent. |
| `07_engineering-refinement` | No — pause | — | Needs senior Engineering partners in the room. |
| `08_vision-horizon` | Yes | opus | "It is the deliverable" — must not be generic, must not slip |
| `09_report` | Yes, optional | sonnet | Rendering an already-settled position into HTML — templating, not new judgment |
| `10_prototype-handoff` | Yes, optional | sonnet | Drafting from existing docs; the ask-don't-invent checklist does the real safety work |

**Model is a default, not a rule.** Pass it via the `Agent` tool's `model` parameter when launching
each stage's worker. If the human asks for a different split (e.g. opus everywhere for a run that's
actually heading to a real customer-facing release, or cheaper/faster throughout for a scratch test), honor that
instead — say so back to them once, don't re-ask per stage. `03_converge`'s default is sonnet
because the RUNBOOK calls that span of the pipeline light-attention, but its own gotcha is false
consensus dressed as agreement — if a `03` run comes back thin or conflict-free on a real (non-test)
run, that's a signal to regenerate it at opus rather than accept it.

## Step 0 — Resolve the run and where it's up to

1. Confirm the run folder (ask if not given, per Usage above).
2. Run the status check from the root `CLAUDE.md`, scoped to this run:
   `ls -d <run>/*/output/* <run>/*_*/output/* 2>/dev/null`
   A file present means that stage is done. This tells you where to resume — never re-run a done
   stage without asking first (see Step 2).
3. Read `<run>/CLAUDE.md` and `<run>/CONTEXT.md` yourself, once, so you know the identity block and
   which stages this run's contracts customize. This is orchestration-level context, not a
   substitute for the worker agent reading it fresh.

## Step 1 — Handle Kickoff and the two human-only stages as pause points

- Before launching `01_frame` for the first time on this run: ask the human whether Kickoff
  happened (owner named out loud, boundaries stated). If not, stop here — don't run `01` on an
  un-kicked-off run.
- When you reach `06_playback` in sequence: **stop.** Tell the human this stage is a live decision
  session with leadership and cannot run as an agent. Point them at the stage's own `CONTEXT.md`
  for the running order, and remind them the decision must be appended to
  `_shared/decision-log.md` before it's real. Wait for them to say it's done, then continue.
- When you reach `07_engineering-refinement`: same pattern — stop, name why, wait.
- If the human says `07` isn't happening (small run, no engineering partners yet — as in the solo
  test), proceed straight to `08` and tell the worker agent to use `08`'s carve-out to run on `03`
  alone. Don't treat a missing `07` as blocking `08`; `08` must not slip.

## Step 2 — The per-stage loop (00–05, 08, 09, 10)

For each automatable stage folder, in order:

1. **Check for existing output** (from Step 0's status scan). If output already exists:
   ask the human — *keep it and move on* / *review it now* / *regenerate this stage* — before
   doing anything else. Never silently overwrite a human's prior edits.
2. **If running or regenerating**, read that stage's `<run>/<stage>/CONTEXT.md` yourself just far
   enough to know its `## Outputs` filename and `## Human check` text — you'll need both after the
   agent returns. Then launch a fresh `Agent` (no `fork` — this must be a clean-context worker),
   passing `model:` from the **Stage order** table above (or the human's override, if they gave
   one) so heavier stages actually get more capable reasoning instead of defaulting silently. Build
   the prompt from this template, filling in the real absolute paths and this stage's actual
   Inputs/Process/Outputs text copied out of its `CONTEXT.md` — the worker agent has never seen
   this conversation and must not need to guess anything:

   > You are starting a brand-new session in the workspace root
   > `(your current directory — never hardcode an absolute path)`, exactly as if a human had just
   > typed `work <run>/<stage>`. Load, in order: `_shared/operating-principles.md`,
   > `_shared/house-view.md`, `<run>/CLAUDE.md`, then `<run>/<stage>/CONTEXT.md`. Load only the
   > additional files that stage's `## Inputs` list names — nothing else. Do not read other stages'
   > outputs beyond what's named, and do not crawl the rest of the workspace.
   >
   > This stage's contract is an interrogation of a real human pair, not a form for you to fill in
   > from judgment. **You do not have `AskUserQuestion` or any other way to reach the human
   > directly — do not attempt to call it.** Wherever the `## Process` section poses a question
   > that needs the human's real answer, do not answer it yourself and do not invent a
   > plausible-sounding answer on the pair's behalf — a fabricated persona, number, or trade-off
   > sentence is worse than an honest gap. Instead, end this turn by handing back the complete,
   > sharpened list of questions you need the human to answer (informed by this stage's Process
   > section and any blind-spots list), and do not write the output file yet. The orchestrator will
   > ask the human directly and send you their answers in a follow-up message — at that point,
   > write the output to `<run>/<stage>/output/<filename from Outputs section>` from those answers
   > verbatim, using the human's actual words, not your own paraphrase of them.
   >
   > If this stage's contract requires no live human answer (pure templating from already-settled
   > inputs), skip the above and just write the output now. When done — whether that's this turn's
   > question list or the finished file — report back plainly which one it is.

   When the worker hands back a question list instead of a finished file: ask that exact list to
   the human via `AskUserQuestion` (free text via "Other" for anything that isn't a clean choice —
   you're relaying the worker's questions, not re-deriving your own), then resume **the same
   worker** via `SendMessage` to its agent id (never a fresh `Agent` call — that would discard the
   context it built loading this stage's inputs) with the human's answers verbatim, and tell it to
   write the output file now.

3. **When the agent returns with a finished output file**, read the output file yourself and show
   its substance to the human directly in this conversation — this *is* the stage's own human-check
   gate, so frame it with that stage's actual check text (e.g. for `01_frame`: "Read the problem
   statement aloud — if it could not be wrong, it says nothing"). Then ask: **accept and continue**
   / **edit it yourself, then continue** / **regenerate this stage** / **stop here**.
   - *Edit*: take their changes directly via `Edit` on the output file — don't spin up another
     agent for a human's own wording change.
   - *Regenerate*: go back to step 2 for the same stage.
   - *Stop*: end the run cleanly. Tell them `/run-pipeline <run-folder>` again later will pick up
     from here — Step 0's status scan is what makes that safe.
4. Move to the next stage folder.

## Step 3 — 09 and 10 are optional

After `08_vision-horizon` is accepted, ask once whether to run `09_report`, `10_prototype-handoff`,
both, or neither now. "Not run" is a legitimate end state — don't push. If the run predates these
two stages (no folders present), first run the mechanical copy from `RUNBOOK.md` §"Stages 09 and
10" before treating them as available:

```
cp _template/09_report/CONTEXT.md <run>/09_report/CONTEXT.md
cp _template/10_prototype-handoff/CONTEXT.md <run>/10_prototype-handoff/CONTEXT.md
mkdir -p <run>/09_report/output <run>/10_prototype-handoff/output/prototype-briefs
```

For `10_prototype-handoff` specifically, its `CONTEXT.md` requires an "ask, don't invent"
checklist (exact on-screen copy, persona, data fixture, `productArea`, `owner`, slug) — make sure
that instruction survives into the worker-agent prompt verbatim; a prior run that skipped it
produced an invented persona and invented ad copy.

## Rules that don't bend (from `RUNBOOK.md`, apply to you too)

1. Load only what the stage names. Don't point any agent at the whole folder.
2. One home per fact — don't restate `_shared/` content, point at it.
3. If a stage contract seems wrong, that's a finding for the human to fix in `_template` later —
   don't patch around it yourself mid-run.
4. Every stage ends in a file. If a worker agent returns without writing its output file, that's a
   failure to surface, not something to paper over.
5. Stage `08` is not optional — don't let a long pause at `06`/`07` turn into skipping it.
