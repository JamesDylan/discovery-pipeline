# Rubric — 03_converge

Grading `direction.md`. The stage's job is to make the call and own the trade-off. The failure mode
is false consensus: a decision that reads as agreement because nothing was actually given up.

Source: the stage's own Human check and Blind spots sections, plus claim H3 in `RUNBOOK.md`.

> **Grader routing.** A criterion tagged `{local}` is mechanical enough for a small local model
> to judge (presence, count, structural completeness). Untagged criteria are judgement calls and
> go to the strong model. `./eval all --grader auto` splits them; `--grader local` grades only the
> tagged ones and reports the rest as ungraded rather than guessing. Move a tag if you disagree.

---

**C1 — a decision exists** {local}
One direction is chosen, unambiguously. "We will pursue A and B in parallel" with no sequence or
dependency is not a decision.

**C2 — the trade-off sentence** {local}
There is a plainly stated sentence of the form *we are choosing X, which means we accept worse Y*.
Y must be something a stakeholder would mind. If the stated cost is one nobody would defend
("we accept this takes engineering effort"), fail.

**C3 — the cost is specific and attributable** {local}
The trade-off names who bears it and roughly for how long. A trade-off with no bearer is
decoration.

**C4 — rejections are argued, not listed**
Each rejected option has a reason that engages its strongest case. "Too expensive" with no
comparison fails. Where an option was rejected on sequencing rather than merit, that distinction is
made explicitly.

**C5 — the bet is named** {local}
The document says what it is betting against — the belief that has to be wrong for this to be the
wrong call.

**C6 — reversal conditions are observable** {local}
There are conditions under which the decision would be reversed, and each is something that could
actually be observed, with a rough threshold or timeframe. "If it doesn't work, reconsider" fails.

**C7 — ties back to assumptions**
The decision engages the load-bearing assumptions from `frame.md`. If an assumption is unproven and
the chosen direction depends on it, that is stated. Silently building on an unproven assumption
fails.

**C8 — no option smuggled back in**
The chosen direction does not quietly reinstate an option the document claims to have rejected. If
a rejected option survives as a component, that is stated openly and justified.

**C9 — open questions have owners or are marked ownerless** {local}
Unresolved items are listed, and each either has an owner or is explicitly flagged as having none.
An open question floating with no ownership status fails.
