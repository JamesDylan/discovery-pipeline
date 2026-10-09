# 10_prototype-handoff — convert this run's position into a brief the prototyping tool can build

One job: produce the instructions that let the prototyping tool named in
`../../_shared/prototype-target.md` stand up a look-and-feel UI of this run's vision, without anyone
re-deriving the vision from scratch.

**Optional stage.** Run it when the position needs to be seen to be argued with — which is most of
the time, but not all of it. Skip it when the run's output is a sequencing or policy claim that no
screen would make more arguable.

**No tool configured?** If `prototype-target.md` is still blank, write the briefs for a human
designer instead: plain sections for the question, owner, screen inventory, component choices and
the fake/real line per screen. Skip every step below that says "per the target".

**Scope discipline:** the ask is a UI shell that uses the right components to give a solid look and
feel — mid-fidelity, coded. Not a working prototype with real data or a real backend. Not a build.
If the brief starts specifying services, persistence or auth, it has drifted.

## Why this stage exists
A vision doc and a prototype brief are different genres. The vision states directions and bets; a
prototyping tool demands a falsifiable one-sentence question, a slug, a named screen inventory, a
mapped persona cast and a declared fake/real line. *"If you can't write the question, you don't know
what to prototype."* Nothing upstream in this pipeline produces that question. This stage does.

## Ask, don't invent

The stage can decompose horizons into screens and map personas mechanically, but it cannot know
the owner's actual intent for several slots — guessing here produces a brief that looks finished
but asserts things nobody said. Before the brief is written, confirm the following with the owner
directly, one question at a time, per `operating-principles.md`. Propose a default only where this
run's own docs give an unambiguous, sourced answer; otherwise ask and wait.

- **The exact on-screen copy.** If the vision doc or its inputs don't supply literal wording for
  the ask/headline/body, do not invent product copy — ask for it.
- **The persona / actor to cast**, when more than one member of the target's cast could plausibly
  stand in for the vision's segment, and how specific the example needs to be. Propose the closest
  match, confirm before locking it in.
- **Whether a new data fixture is needed**, and if so, how much specificity it should carry — a
  fully named, dated, routed example, or something intentionally generic. Don't default to maximum
  specificity; ask.
- **The area / taxonomy tag** the target uses for its hub entry, whenever the surface sits on a
  genuine taxonomy boundary.
- **The owner attribution string**, exactly as the target expects it (see Ownership below) —
  confirm, never guess.
- **The slug**, if more than one reasonable option exists.

This step exists so the stage stays reusable across every run: the questions above don't change
run to run, only the answers do.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/prototype-target.md` — which tool, where its docs live, its brief
  format, and the conventions the steps below apply "per the target"
- Working: `../08_vision-horizon/output/vision-horizon.md` — the bet, and the Now/Next/Later chain
- Working: `../CLAUDE.md` — sphere of influence, which bounds what surfaces this run may propose
- Working: `../04_make-tangible/output/` — anything already made tangible feeds the screen inventory
- Working: `../05_pressure-test/output/` — the edge cases that decide which states get built

**Then read the tool's own reference docs**, at the paths `prototype-target.md` lists, in the tool's
repo, not here — before writing anything.

## Process
1. **Decompose into questions.** One prototype surface per falsifiable question, not one prototype
   for the whole run. Two or three narrow surfaces beat one omnibus every time. If a horizon yields
   no question a UI could answer, it does not get a surface.
2. **Name and check each slug.** Kebab-case. Refuse collisions with live surfaces and with the
   reserved roots per the target. Check against the tool's actual registry, not from memory.
3. **Map the run's actors onto the target's existing cast**, if it has one (fixed personas, system
   roles, a seed clock). Vision-language segments must be translated, or the surface silently
   invents a second domain model.
4. **Write the screen inventory.** Named routes, in the target's route convention. The rule is
   absolute: *a screen not listed here is out of scope.*
5. **Choose components before writing any.** Precedence per the target; by default: an existing
   design-system primitive → a composed pattern built from primitives → semantic tokens → a one-off,
   flagged. Never raw hex. Name the specific components and their variants per screen. That naming
   is what buys the look and feel — it is the highest-leverage part of this brief.
6. **Declare the fake/real line.** Explicitly, per screen. Default: everything faked except
   navigation, state transitions and the one interaction the question turns on.
7. **Decide bundles and divergence**, using the composition units per the target. Declare any
   domain divergence, and respect the target's non-forkable floor — those things are never
   redefined per surface.
8. **Translate the vocabulary.** Every term in the brief must exist in the target's glossary.
   Coinages from the vision get mapped or dropped.

## Ownership
The owner is **the PM who ran this process** — the name in `../CLAUDE.md` under *Owner of the
12-month view* — written exactly in the form the target's Ownership line specifies. If the tool
gates writes by author identity, a wrong string silently blocks every later edit to that surface.
Confirm the exact string with them rather than guessing it.

## Blind spots to call out
- **One giant prototype.** The most likely failure of this stage. A single surface expressing the
  whole run answers nothing.
- **A question that can't be wrong.** "What does the future of X feel like?" is not a question —
  no answer to it would change anything. Write the no as well as the yes.
- **Specifying a build.** Services, persistence, auth, real data: all out of scope. Mark the absent
  backend explicitly (per the target, if it has a pattern for that) rather than faking one.
- **Inventing components.** A brief describing bespoke UI produces a prototype that looks nothing
  like the real product, which defeats the point of using the tool at all.
- **Surfaces outside the sphere of influence.** If a surface needs another run's territory to make
  sense, it belongs in `101-prototype-handoff` after synthesis, not here.
- **House-style rules the target enforces.** Check its list and follow it.

## Outputs
- `prototype-briefs/<slug>.md` → `output/` — one per surface, in the brief format the
  prototype target names. Ready to hand to the tool as its invocation step describes.
- `HANDOFF.md` → `output/` — the ranked reading order, the settled decisions that must not be
  reopened, and the single next action naming the first surface to build.

## Human check
Give one brief to someone who has not read the vision and ask them what question the prototype
answers. If they answer with a feature description instead of a question, rewrite it. Then ask the
named owner whether they would defend that question in a review — if not, it's the wrong question
or the wrong owner.
