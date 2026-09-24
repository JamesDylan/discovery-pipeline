# Rubric — 01_frame

Grading `frame.md`. The stage's job is to establish what problem is really being solved. The test
is not whether the document is well written; it is whether the framing does work the pair had not
already done.

Source of these criteria: the stage's own Human check, plus claims H1 and H5 in `RUNBOOK.md`.

> **Grader routing.** A criterion tagged `{local}` is mechanical enough for a small local model
> to judge (presence, count, structural completeness). Untagged criteria are judgement calls and
> go to the strong model. `./eval all --grader auto` splits them; `--grader local` grades only the
> tagged ones and reports the rest as ungraded rather than guessing. Move a tag if you disagree.

---

**F1 — falsifiable problem statement**
There is a single-sentence problem statement, and it could be wrong. A statement that could not
possibly be wrong ("travellers need better visibility of credits") fails. Ask: what would have to
be observed for this sentence to be false?

**F2 — reframes rather than restates**
The document names a problem that the run's `CLAUDE.md` questions did not already name, or
explicitly rejects a framing implied by those questions and says why. Restating the questions in
fuller prose fails, however competent the prose.

**F3 — symptom handled as symptom**
Where the run's identity flags a metric or a stated symptom, the frame establishes what *kind* of
problem it is (flow, motivation, trust, incentive, timing) before anything is designed against it.
Accepting the symptom as the problem fails.

**F4 — evidence cuts both ways** {local}
Evidence against the framing is present, specific, and consequential — not a token caveat.
Staleness, derivation and measurement gaps in the inputs are carried forward rather than dropped.

**F5 — load-bearing assumptions are load-bearing** {local}
Assumptions are listed *with what breaks if each is false*. A list of assumptions with no stated
consequence fails.

**F6 — an explicit cut** {local}
The document says what it is not solving, and at least one item is something a reasonable person
would have expected to be in scope. "Out of scope: everything unrelated" fails.

**F7 — ownership is located** {local}
It says whose problem this is, and where the felt-pain sits versus where the cost sits. If those
differ, the asymmetry is named.

**F8 — house view is visible**
If `_shared/house-view.md` contains a filled house view, the frame applies at least one standard or
kill-criterion from it that a competent outsider would not have known. If the house view is empty
(`STATUS: EMPTY`), mark this **pass** and note that it was untestable — this criterion is the H5
experiment, and an empty house view means the experiment was not run, not that the stage failed.
