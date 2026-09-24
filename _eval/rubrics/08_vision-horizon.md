# Rubric — 08_vision-horizon

Grading `vision-horizon.md`. This is the stage the programme is named after, so grade it hardest.
The deliverable is a *position*, not a plan. The two named failure modes are "roadmap in a
trenchcoat" and "aspiration with no mechanism".

Source: the stage's own Human check and Blind spots sections, `_shared/vision-principles.md`, and
claim H4 in `RUNBOOK.md`.

> **Grader routing.** A criterion tagged `{local}` is mechanical enough for a small local model
> to judge (presence, count, structural completeness). Untagged criteria are judgement calls and
> go to the strong model. `./eval all --grader auto` splits them; `--grader local` grades only the
> tagged ones and reports the rest as ungraded rather than guessing. Move a tag if you disagree.

---

**V1 — one sentence, and it is a bet**
There is a single-sentence version of the vision. It asserts something about where this part of the
product is going that a reasonable colleague could disagree with. A sentence that only a contrarian
could dispute passes; a sentence nobody could dispute fails.

**V2 — disagreeable, not merely ambitious**
Apply the Human check directly: could someone who works on the product but not on this run find something
to disagree with? If the sentence is a statement of aspiration ("company management becomes
seamless and intelligent"), fail — that is the aspiration failure mode.

**V3 — mechanism is present**
For the central claim, the document says *how it becomes true* — what the system does, what it
knows, and where that knowledge comes from. A claim that a capability will exist, with no account
of the mechanism, fails.

**V4 — Now / Next / Later with real dependency**
The three horizons are present, and Next depends on something Now produces, and Later on Next.
State the dependency you found. If the three horizons are three independent workstreams that could
be reordered freely, that is the roadmap-in-a-trenchcoat failure — fail.

**V5 — capabilities, not features**
Each horizon names a capability gained (something the system can now do, or something it now
knows), not a list of things to build. A horizon expressed purely as deliverables fails.

**V6 — what it is betting against** {local}
The document states the alternative future it is rejecting, or the belief that must be wrong. An
absent counter-position fails.

**V7 — bounded by the sphere of influence**
The claim stays inside the sphere of influence declared in the run's `CLAUDE.md`. A vision that
quietly claims territory belonging to another run or to all of the product fails.

**V8 — honest about AI**
If AI is central to the bet, the mechanism is specified (what it infers, from what data, and what
happens when it is wrong). If AI is incidental, the document says so plainly. A decorative AI
framing fails; an honest absence passes.

**V9 — named owner** {local}
A specific named owner is stated for the 12-month view.

**V10 — open questions that would change the view**
There are open questions, and at least one of them, resolved a particular way, would genuinely
change the position — not merely its implementation detail.

**V11 — survives an upstream gap honestly** {local}
If `07_engineering-refinement` has not run, the document proceeds on `03_converge`'s output and
says so, rather than either stalling or silently inventing engineering scope. Inventing feasibility
detail that no engineer supplied fails.
