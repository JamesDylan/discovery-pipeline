# Rubric — 02_explore

Grading `options.md`. The stage's job is to open the solution space. Judge divergence and the
absence of judgement, not polish.

Source: the stage's own Hard rule, Interrogate and Human check sections, plus claim H2 in
`RUNBOOK.md`.

> **Grader routing.** A criterion tagged `{local}` is mechanical enough for a small local model
> to judge (presence, count, structural completeness). Untagged criteria are judgement calls and
> go to the strong model. `./eval all --grader auto` splits them; `--grader local` grades only the
> tagged ones and reports the rest as ungraded rather than guessing. Move a tag if you disagree.

---

**E1 — three or more options** {local}
At least three distinct options are presented.

**E2 — materially different bets**
Apply the contract's own test: if two options would be built by the same team in the same sequence,
they are one option. Fail if any two options collapse under that test. Different UI over the same
underlying mechanism is one option.

**E3 — divergence axes actually crossed**
The set spans at least two of: remove the need vs ease the task · system-inferred vs
user-declared · progressive vs upfront · individual vs network · product vs incentive vs policy.
Name which axes are crossed. Four options all sitting on the same axis fails.

**E4 — no ranking** {local}
No option is scored, ranked, preferred or recommended. A "recommended option", a scoring table, or
language that positions one option as the obvious answer fails. Naming the option the pair would
resist is *not* ranking — it is required by the contract.

**E5 — the uncomfortable option is present and identified** {local}
There is an option that is politically, commercially or technically inconvenient, and the document
says which one and why it is uncomfortable. A set where every option is safe fails.

**E6 — the no-one-decides option**
At least one option works without any human deciding anything — the need is removed rather than
the task eased. Fail if every option requires a user or admin to act.

**E7 — each option is arguable** {local}
Every option states its underlying bet, how it works, what it assumes, and why someone smart would
choose it. An option missing its assumption or its bet fails this criterion.

**E8 — analogues mined, and from outside travel** {local}
The document draws on patterns from outside the immediate domain. If the run's `CLAUDE.md` names
analogue domains to look at, at least two are visibly used. Generic references ("like Amazon")
without a named mechanism fail.

**E9 — inherits the frame**
The options respond to the problem as `frame.md` framed it, including any framing `frame.md`
explicitly rejected. An option that re-introduces a rejected framing without arguing for it fails.
