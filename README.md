# Vision Pipeline — How This Works

Read this before you open any folder. It takes about ten minutes.

**Ready to start? Use `RUNBOOK.md`.** It gives the step-by-step instructions, from "I have a
problem and nothing else" to the first stage finished. If you do not use the terminal often, start
with its Part 0.

---

## 1. What this is

A shared workspace that takes one problem area of your product from "we don't really know" to two things:

1. **A product and design direction** for the next 1–3 months, ready for leadership to decide on.
2. **A 12-month view** of where that part of the product is going.

The workspace is not a place to store documents. **It is the process itself.** Each folder is one
step of the work, and holds the instructions for that step. When you work in a folder with Claude,
Claude knows only what that step needs — nothing else.

Every problem area (called a **run**) is a copy of the same blank method in `_template`. Each run is
a numbered folder at the top of the workspace, for example `01-<run-slug>`.

---

## 2. Why we are doing this

Near-term product work can be strong while the 12-month picture is missing. That gap has a real
cost: people in the team stop believing there is a direction.

So the goal is not a document. **The goal is that people believe there is a direction.** A vision
that is well argued but changes nobody's mind has failed.

The second goal is about who sets the vision. Here, senior people set it for the area they know
best — it is not handed down. This workspace lets a Product and Design pair form a point of view
and defend it without waiting for permission.

---

## 3. The two outputs — keep them separate

|                   | Near-term output (the "accelerator") | Vision output                          |
| ----------------- | ------------------------------------ | --------------------------------------- |
| **Time horizon**  | Next 1–3 months                      | 12 months                               |
| **What you make** | A prototype and the reasoning behind it | A story of where it goes, and the order capabilities arrive in |
| **Question**      | "Do we build this?"                  | "Where is this part of the product going?"      |

A perfect three-day sprint on one feature gives you the left column only — and the team still says
there is no vision. Stage `08_vision-horizon` produces the right column. It is not optional, and it
is not a nice extra at the end. **If time runs short, cut prototype polish in stage `04`. Never
cut stage `08`.**

---

## 4. The steps

Each step has one job, one output file, and one human check. You can run them out of order, skip
ahead, or go back. The fixed rule is that every step saves a file, so the next step has something
to work from. `RUNBOOK.md` Part 2 has the full detail on each step, including common problems.

### The nine main steps

| Step                        | Its one job                                       | Output file            |
| --------------------------- | ------------------------------------------------- | ---------------------- |
| `00_setup`                  | Remove setup problems. Nothing else.              | `inventory.md`         |
| `01_frame`                  | Work out what problem is really being solved      | `frame.md`             |
| `02_explore`                | Find really different solutions. No judging yet.  | `options.md`           |
| `03_converge`               | Choose one, and own what you give up              | `direction.md`         |
| `04_make-tangible`          | Build something people can react to               | `artefact-notes.md`    |
| `05_pressure-test`          | Try to break it before leadership does            | `pressure-test.md`     |
| `06_playback`               | Get a real decision from leadership, live         | `playback.md`          |
| `07_engineering-refinement` | Turn the decision into something teams can plan against | `solution-scope.md` |
| `08_vision-horizon`         | Turn the solution into a 12-month story           | `vision-horizon.md`    |

Stages `06` and `07` are live meetings with people. Claude helps you prepare and write them up, but
the decisions happen in the room.

### Two optional steps

| Step | Its one job | Output file |
| --- | --- | --- |
| `09_report` | Turn the position into a page people will believe | `vision-report.html` |
| `10_prototype-handoff` | Turn the position into briefs a prototyping tool can build from | `prototype-briefs/*.md` |

Run either, both, or neither. They exist because a markdown file has two weaknesses: it loses its
structure when someone pastes it into a deck, and it cannot be seen as a product.

- `09` turns the argument into an HTML page, with the evidence one click under every claim.
- `10` turns it into a UI brief that the your prototyping tool can use to build a look-and-feel
  prototype — a shell that uses the right components, not a working product.

**Neither step adds anything new.** If the report or the brief is wrong, `08` is wrong.

The same two steps also exist at the top level, as `100-report/` and `101-prototype-handoff/`. They
work from the combined vision (stage `99`) instead of one run.

### Where your effort goes

Expect a U-shape. Heavy at the start, when you set the direction. Light in the middle, while the
work gets done. Heavy again at the end, when you decide if it is really right. A little judgement
at each end saves a lot of rework in the middle.

**Fixing things early is cheap.** One hour in `01_frame` is worth a day in `05_pressure-test`.
Each step ends where a person would naturally stop and check.

---

## 5. Who is involved

| Who | What they do |
| --- | --- |
| **The Product + Design pair** | Own the work together — not Product writing a spec and handing it to Design. Senior enough to make trade-offs and to be wrong. |
| **Cross-functional leadership** | Set the challenge, protect the time, remove blockers, act as experts, and make the decision at the playback. |
| **Senior Engineering partners** | Join *after* the playback decision, for stage `07`. They cover feasibility, complexity, and anything that changes the shape of the solution. |
| **Domain experts and customer-facing colleagues** | Brought in briefly when an assumption could change the direction. Twenty minutes, not a workshop. |
| **The named owner of the 12-month view** | One person per run. Their name goes in the run's `CLAUDE.md`. |
| **Commercial partner** | Sees a separate version of the output. Different audience, different angle — a commercial argument, not a product story. |

---

## 6. How to start

**Follow `RUNBOOK.md` Part 1, in order, the first time.** In short, you will:

1. Pick your problem and give it a short name.
2. Copy `_template` into a new numbered folder.
3. Fill in who owns the run and what it covers.
4. Start Claude Code at the workspace root and tell it which stage to work on.

**The rhythm once a run exists:** start a fresh Claude conversation, tell Claude which stage to
work on, answer its questions, check the output file, then start a fresh conversation for the next
stage.

**How to see where things are.** Look in each stage's `output/` folder. A file there means that
stage is done. There is no separate tracker — the files *are* the status. (`RUNBOOK.md` shows how
to check this in Finder, in the terminal, or by asking Claude.)

**How one step hands over to the next.** One step's `output/` file is the next step's input. Open
the file, change anything you disagree with, and save it. The next step reads what you left there.
**You can always edit an output.** You are never stuck with what Claude wrote.

**Changing the method.** To change how a step works, edit it in `_template`. Never edit a live run
to change the method.

---

## 7. Why this works

**One job per folder.** A step that gathers does not also filter. A step that filters does not
also decide. Mixing jobs is how you end up with vague output.

**Claude sees only what the step needs.** Each step lists its input files by exact path, and says
what *not* to load. This matters more than it sounds. Claude works worse when given everything than
when given the right thing. And you cannot check a decision if you do not know what informed it.

**The order of the work is the order of the folders.** No special software, no framework, no tool
to learn. Numbered folders hold the order. Plain text files hold the state.

**Everything is readable and editable.** Plain markdown files. No database, no export, no special
format. Anyone can open any file, see where things are, and change it.

**Set it up once, run it many times.** Product context, house view and principles live in `_shared`
and are written once. Every run uses the same setup. Improve something there, and every run
improves.

**It does not depend on the person who built it.** The judgement is in the files, not in someone's
head. A pair can run a step without waiting for anyone, and the method outlives this run.

**The method is published.** It is not a local invention. It follows ICM (Interpretable Context
Methodology) — Van Clief & McDermott, arXiv:2603.16021, `github.com/RinDig/icm-architect`. The same
pattern — plain folders and files as the way to hand judgement to an AI — appears independently in
most serious agent workflows.

---

## 8. Strengths

- **Quick to learn.** No tool to learn. If you can read a folder, you can use it.
- **Transparent.** You can always see what Claude was told, and why it said what it said.
- **Cheap to change.** Disagree with a step? Rewrite its `CONTEXT.md`. That is the whole change.
- **Hard to lose work.** Everything is a file. Nothing lives only in a chat history.
- **Forces clear trade-offs.** Several steps do not accept "both are valid" as an answer.
- **Portable.** Works with any AI assistant. Nothing here is tied to one product.
- **Checks itself.** The "walk test" asks: can a fresh assistant with no memory find its way, do
  the work and report status from the files alone? Running `./eval` checks this automatically and
  catches problems before they spread. See `_eval/README.md`.

---

## 9. Limitations — read this section carefully

**Limits of the method itself**

- It suits step-by-step work with a person checking each stage. It does not suit real-time work,
  many people using the same run at once, or a system that needs to change course on its own.
- It does not make anyone smarter. It organises thinking. It does not supply it.

**Problems to watch for in this workspace**

These are risks, not facts about the current state. Check `_shared/house-view.md` and
`_shared/product-context.md` yourself — both should improve over time.

- **If `_shared/house-view.md` becomes thin or generic,** every step runs on generic best
  practice, and generic input gives generic output. A process with no opinion cannot produce a
  point of view. This is the most important file in the workspace to keep sharp.
- **If `_shared/product-context.md` is out of date or thin,** every later step is weaker.
- **If a run's "owner of the 12-month view" is still a placeholder,** the run becomes a tidier
  version of one person steering alone. Check that someone was named, out loud, at the Kickoff
  (`RUNBOOK.md` Part 2).
- **A short working window limits pressure-testing.** `05_pressure-test` will mostly use existing
  evidence and expert judgement, not new user research. Say this honestly at the playback.
- **A few runs are a thin base for a whole-product vision.** Stage `99` must find a through-line
  that no single run found on its own. If it just joins summaries together, the team will
  correctly see it as "no vision, just workstreams."

**The biggest risk**

Structure can become theatre. Neatly filled folders can look like progress while the thinking stays
shallow. The files are there to hold judgement, not to replace it. If a step is not helping, say so
and merge it into another. The limit is time, not process.

---

## 10. How we will know it worked

Not by how good the documents are. By this test:

> **Can a Product and Design pair run a step and reach a position they can defend, without the
> person who set this up in the room?**

That is the real measure. If the answer is no, the process has only created a bottleneck with
better filing.

A second test, for the vision itself: say the one-sentence version to someone who works on the product but
not on this run, and ask them to disagree with it. If they cannot find anything to disagree with,
it is not a position yet.

---

## 11. Rules that do not change

1. **Load only what the step names.** Do not point Claude at the whole workspace.
2. **One home for each fact.** If something is in `_shared`, do not repeat it elsewhere. Point to it.
3. **Keep the method and live work separate.** Change `_template`, never a live run.
4. **Every working session ends with a saved file.** A session that produces only slides or a good
   feeling has failed. Write the decision down before you leave the room.
5. **No polished slide deck at the playback.** Use the real work. A deck suggests the work cannot
   speak for itself.
6. **Stage `08` is not optional.** It is the reason this workspace exists.

---

## 12. Glossary

| Term | Meaning |
| --- | --- |
| **Run** | One problem area going through the steps, in its own numbered folder (e.g. `01-<run-slug>`) |
| **Stage / step** | One numbered folder inside a run, with one job |
| **Workspace root** | The top folder of this workspace — the one that contains `README.md`, `RUNBOOK.md` and `_template` |
| **`output/` folder** | Where each stage saves its file. A file here means the stage is done. |
| **`CLAUDE.md`** | The map for a folder. It points to things and holds almost nothing itself. |
| **`CONTEXT.md`** | The instructions for a stage: inputs, what to do, what to produce, and the human check |
| **`_shared`** | Background files every stage uses. Stable. Written once. |
| **`_template`** | The blank method. Copy it to start a new run. |
| **Decision-ready** | Good enough for leadership to make a real decision and hand over to Engineering |
| **Plan-ready** | Product, Design and Engineering can all say "I can plan against this" |
| **House view** | The team's specific opinion of what good looks like in your product. Kept in `_shared/house-view.md`. |
| **Walk test** | Can a fresh assistant find its way, do the work and report status from the files alone? |
| **Slug** | A short, lowercase, hyphenated name for a run, e.g. `expense-capture` |

---

*Method reference: Van Clief & McDermott, "Interpretable Context Methodology: Folder Structure as
Agent Architecture", arXiv:2603.16021 · `github.com/RinDig/icm-architect`*
