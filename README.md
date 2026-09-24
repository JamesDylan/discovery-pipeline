# Vision Pipeline — How This Works

Read this before you open any folder. It takes about ten minutes.

**To actually run it, use `RUNBOOK.md`** — step-by-step for the solo test run and the full workshop process.

---

## 1. What this is

A shared working folder for taking one problem area of your product from "we don't really know" to
two things:

1. **A decision-ready product and design direction** for the next 1–3 months.
2. **A 12-month view** of where that part of the product is going.

The folder is not a document store. It is the process itself. Each folder is one step of the work
and holds the instructions for that step. When you open a folder and work in it with Claude, you
get an assistant that knows only what that step needs — nothing else.

You can run several problem areas through it side by side, each in its own numbered folder, e.g.:

- `01-<slug>` — a customer-facing capability gap
- `02-<slug>` — a trust or guardrails gap

Each is a copy of the same blank method, which lives in `_template`. There's no fixed number of
runs — start with one.

---

## 2. Why we are doing this

Near-term product work can be strong while the 12-month picture is missing. That gap has a real
cost: people inside the team stop believing there is a direction.

So the goal is not a document. **The goal is that people believe there is a direction.** A vision
that is well argued and changes nobody's mind has failed.

The second goal is about who does it. Vision here is set by senior people in the area they know
best — not handed down. This folder exists so that a Product and Design pair can form a point of
view and defend it without waiting for permission.

---

## 3. The two outputs — do not mix them up

|                   | Accelerator output                | Vision output                          |
| ----------------- | ---------------------------------- | -------------------------------------- |
| **Time horizon**  | Next 1–3 months                    | 12 months                              |
| **What you make** | A prototype and the reasoning      | A narrative arc and capability sequence |
| **Question**      | "Do we build this?"                | "Where is this part of the product going?" |

A short, well-run sprint on one feature gives you a feature, and the team still says there is no
vision if that's all that happens.

Stage `08_vision-horizon` is the step that produces the vision column. It is not optional and it is
not a nice-to-have at the end. **If time runs short, cut prototype polish in stage 04, not stage 08.**

---

## 4. The nine steps, plus two optional ones

Each step has one job, one output file, and one human check. You can run them out of order, skip
ahead, or loop back. What is fixed is that each step leaves a file behind, so the next one has
something to stand on.

| Step                        | One job                                          | Produces              |
| --------------------------- | ------------------------------------------------ | --------------------- |
| `00_setup`                  | Remove setup friction. Nothing else.             | `inventory.md`        |
| `01_frame`                  | Work out what problem is really being solved     | `frame.md`            |
| `02_explore`                | Open up the solution space. No judging.          | `options.md`          |
| `03_converge`               | Make the call and own the trade-off              | `direction.md`        |
| `04_make-tangible`          | Build something people can react to              | `artefact-notes.md`   |
| `05_pressure-test`          | Attack it before leadership does                 | `pressure-test.md`    |
| `06_playback`               | Get a real decision                              | `playback.md`         |
| `07_engineering-refinement` | Go from decision-ready to plan-ready             | `solution-scope.md`   |
| `08_vision-horizon`         | Turn the solution into a 12-month arc            | `vision-horizon.md`   |

### Two optional steps after that

| Step | One job | Produces |
| --- | --- | --- |
| `09_report` | Render the position as an asset a room will believe | `vision-report.html` |
| `10_prototype-handoff` | Turn the position into briefs a prototyping tool can build | `prototype-briefs/*.md` |

Run either, both, or neither. They exist because markdown does neither of the two things a position
needs to survive: it doesn't hold its structure once someone pastes it into a deck, and it can't be
looked at. `09` folds the argument into an HTML asset with its evidence one click under every
claim. `10` converts it into a UI brief a prototyping tool can build a look-and-feel prototype
from — a shell that uses the right components, not a working product.

**Neither step asserts anything new.** If the report or the brief is wrong, `08` is wrong.

The same two steps exist at the top level as `100-report/` and `101-prototype-handoff/`, running
off the synthesised vision instead of one run's. Same method, wider claim.

**Where your attention goes.** Expect a U-shape. Heavy at the start, when you are setting
direction. Light through the middle, while the work grinds. Heavy again at the end, when you decide
whether this is actually right. A small amount of judgement at the two ends saves a large amount of
churn in between.

**Fixing things early is cheap.** An hour spent in `01_frame` is worth a day spent in
`05_pressure-test`. The step boundaries sit where a person would naturally stop and check.

---

## 5. Who is involved

| Who                                                                                 | What they do                                                                                                      |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **The Product + Design pair**                                                        | Own the work jointly. Not Product specifying and handing to Design. Senior enough to make trade-offs and be wrong. |
| **Cross-functional leadership**                                                      | Frame the challenge, protect the time, remove blockers, act as SMEs, make the decision at playback.                |
| **Senior Engineering partners**                                                      | Join *after* the decision, for stage `07`. Feasibility, complexity, what changes the shape of the thing.           |
| **Domain SMEs and customer-facing colleagues**                                       | Pulled in briefly where an assumption could change the direction. Twenty minutes, not a workshop.                   |
| **The named owner of the 12-month view**                                             | One person per problem area. Their name goes in the run's `CLAUDE.md`.                                             |
| **Commercial or partner stakeholders**                                               | See the output later. Different audience, different cut — commercial thesis, not product story.                    |

---

## 6. How to actually use it

**Your first ten minutes**

1. Open the workspace. Read `CLAUDE.md` — it is a one-page map, nothing more.
2. Read `CONTEXT.md` for the shape of the whole thing.
3. Open your problem area folder. Read its `CLAUDE.md` (what this run is) and `CONTEXT.md` (the
   step table).
4. Open the step folder you are on. Read its `CONTEXT.md`. That is your brief.
5. Work. Save your output into that step's `output/` folder.

**How to know where things stand**

Run the status command in `CLAUDE.md`. A file in an `output/` folder means that step is done.
There is no separate tracker to keep updated — the files *are* the status.

**How handover works**

One step's `output/` folder is the next step's input. Open the file, change anything you disagree
with, and the next step reads whatever you left there. **Every output is something you can edit.**
You are never stuck with what the assistant produced.

**Starting a new problem area**

Copy `_template` to a new numbered folder and fill in its `CLAUDE.md`. Never edit a live run to
change the method — change `_template`.

---

## 7. Why this works

Six reasons, in plain terms.

**One job per folder.** A step that gathers does not also filter. A step that filters does not also
decide. This is the oldest rule in software design and it applies just as well to thinking work —
mixing jobs is how you end up with vague output.

**The assistant only sees what the step needs.** Each step lists its inputs by exact file path, and
says what *not* to load. This matters more than it sounds. An assistant given everything performs
worse than one given the right thing, and you cannot audit a decision when you don't know what
informed it.

**The order of the work is the order of the folders.** No orchestration software, no framework, no
tool to learn. Numbered folders carry the sequence. Plain text carries the state.

**Everything is readable and editable by a person.** Plain markdown files. No database, no export,
no proprietary format. Anyone can open any file, see exactly where things stand, and change it.

**Set up the factory once, run it many times.** Product context, house view and principles live in
`_shared` and are written once. Every problem area draws on the same setup. Fix something there and
every run improves at the same time.

**It survives the person who built it.** The judgement is in the files, not in someone's head.
That is the entire point — a pair can run a step without waiting on anyone, and the method outlives
this particular sprint.

**The method is published.** This is not a local invention. It follows ICM (Interpretable Context
Methodology) — Van Clief & McDermott, arXiv:2603.16021, `github.com/RinDig/icm-architect`. Every
major AI lab has landed on the same pattern: plain folders and files as the way judgement gets
handed to a machine.

---

## 8. Strengths

- **Fast to pick up.** No tool to learn. If you can read a folder, you can use it.
- **Transparent.** You can always see what the assistant was told and why it said what it said.
- **Cheap to change.** Disagree with a step? Rewrite its `CONTEXT.md`. That is the whole change.
- **Hard to lose work.** Everything is a file. Nothing lives in a chat history.
- **Forces explicit trade-offs.** Several steps refuse to let "both are valid" stand as an answer.
- **Portable.** Works with any assistant. Nothing here is tied to one product.
- **Self-checking.** The "walk test" — can a fresh assistant with no memory orient, act and report
  status from the files alone? — catches decay before it spreads.

---

## 9. Limitations — read this part properly

**Honest limits of the method itself**

- It suits sequential work with a human checking at each stage. It is a poor fit for real-time
  work, many people hitting the same pipeline at once, or a system that needs to branch on its own.
- It does not make anyone smarter. It organises thinking; it does not supply it.

**Before you run this for real, fill these in**

- **`_shared/house-view.md` starts empty.** This is the file that holds your specific view of what
  good looks like in your product. Until it is filled, every step runs on generic best practice —
  and generic input produces generic output. A process with no opinion cannot produce a point of
  view.
- **`_shared/product-context.md` starts empty.** Every step downstream is weaker without it.
- **Someone has to own the 12-month view.** If that stays blank, this becomes a better-organised
  version of one person steering the ship.
- **A short accelerator is short for real pressure-testing.** Stage `05` will mostly rely on
  existing evidence and expert judgement, not new user research over a few days. Be honest about
  that at playback.
- **One or two problem areas is a thin base for a whole-product vision.** Stage `99` must produce a
  through-line that neither run produced alone. If it just staples two summaries together, the team
  will correctly read it as "no vision, just workstreams."

**The risk to watch for**

Structure can become theatre. Neatly filled folders can look like progress while the thinking stays
shallow. The files are there to hold judgement, not to replace it. If a step is not helping, say so
and collapse it. The constraint is time, not process.

---

## 10. How you will know it worked

Not by the quality of the documents. By this test:

> **Can a Product and Design pair run a step and reach a defensible position without you in the room?**

That is the real measure, and it is checkable early. If the answer is no, the process has produced
a bottleneck with better filing.

A second test, for the vision itself: say the one-sentence version to someone who works on the
product but not on this run, and ask them to disagree with it. If they cannot find anything to
disagree with, it is not a position yet.

---

## 11. Rules that are not negotiable

1. **Load only what the step names.** Do not point the assistant at the whole folder.
2. **One home per fact.** If something is true in `_shared`, do not restate it elsewhere. Point at it.
3. **Method and live work stay separate.** Change `_template`, never a running copy.
4. **Every working session ends in a file.** A session that produces only slides or a good feeling
   has failed. Write the decision down before leaving the room.
5. **No polished deck at playback.** Use the actual work. A deck signals the artefact cannot carry itself.
6. **Stage `08` is not optional.** It is the reason this workspace exists.

---

## 12. Quick glossary

| Term                | Means                                                                              |
| ------------------- | ------------------------------------------------------------------------------------ |
| **Run**             | One problem area going through the nine steps (e.g. `01-<slug>`)                    |
| **Stage / step**    | One numbered folder, one job                                                        |
| **`CLAUDE.md`**     | The map for a folder. Points at things, holds almost nothing.                       |
| **`CONTEXT.md`**    | The brief for a step. Inputs, what to do, what to produce, the human check.         |
| **`_shared`**       | Context every step uses. Stable. Written once.                                      |
| **`_template`**     | The blank method. Copy it to start a new problem area.                              |
| **Decision-ready**  | Good enough for leadership to make a real call and move to engineering              |
| **Plan-ready**      | Product, Design and Engineering can all say "I can plan against this"               |
| **House view**      | Your specific view of what good looks like in your product. Starts unwritten.       |
| **Walk test**       | Can a fresh assistant orient, act and report status from the files alone?           |

---

## 13. A typical cycle, in relative time

There's no fixed calendar shipped here — set your own dates. As a shape to start from:

| Day | What |
| ----- | ----------------------------------------------------------------------- |
| Day 0        | Setup only                                                        |
| Day 1        | Kickoff                                                           |
| Days 1–3     | Protected working days (stages `01`–`05`)                        |
| Decision day | Playback and decision — a decision point, not a showcase          |
| Following weeks | Engineering exploration and refinement (`07`), `08` alongside it |
| Definition-of-done day | Agreed scope and design direction                       |
| Later        | Partner / commercial readout, if you have one                    |

---

*Method reference: Van Clief & McDermott, "Interpretable Context Methodology: Folder Structure as
Agent Architecture", arXiv:2603.16021 · `github.com/RinDig/icm-architect`*
