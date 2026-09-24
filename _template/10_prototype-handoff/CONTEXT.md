# 10_prototype-handoff — convert this run's position into a brief a prototyping tool can build

One job: produce the instructions that let a prototyping tool stand up a look-and-feel UI of
this run's vision, without anyone re-deriving the vision from scratch.

**Optional stage.** Run it when the position needs to be seen to be argued with — which is most of
the time, but not all of it. Skip it when the run's output is a sequencing or policy claim that no
screen would make more arguable.

**This stage's contract assumes you have a prototyping tool of your own** — an internal app, a
design-system-aware scaffold, or a shared Claude Code skill that turns a brief into a working UI
shell. If you don't have one yet, treat everything below as a design brief for a human designer
instead of a machine-consumable contract, and skip the tool-specific sections.

**Scope discipline:** the ask is a UI shell that uses the right components to give a solid look and
feel — mid-fidelity, coded, not pixel-perfect. Not a working prototype with real data or a real
backend. Not a build. If the brief starts specifying services, persistence or auth, it has drifted.

## Why this stage exists
A vision doc and a prototype brief are different genres. The vision states directions and bets; a
prototyping tool demands a falsifiable one-sentence question, a slug, a named screen inventory, a
mapped persona cast and a declared fake/real line. If your tool has a playbook, it probably says
something like: *"If you can't write the question, you don't know what to prototype."* Nothing
upstream in this pipeline produces that question. This stage does.

## Ask, don't invent

The stage can decompose horizons into screens and map personas mechanically, but it cannot know
the owner's actual intent for several slots — guessing here produces a brief that looks finished
but asserts things nobody said. Before the brief is written, confirm the following with the owner
directly, one question at a time, per `operating-principles.md`. Propose a default only where this
run's own docs give an unambiguous, sourced answer; otherwise ask and wait.

- **The exact on-screen copy.** If the vision doc or its inputs don't supply literal wording for
  the ask/headline/body, do not invent product copy — ask for it.
- **The persona / actor to cast**, when more than one plausible persona could stand in for the
  vision's segment, and how specific the example needs to be. Propose the closest match, confirm
  before locking it in.
- **Whether a new data fixture is needed**, and if so, how much specificity it should carry — a
  fully named, dated, routed example, or something intentionally generic. Don't default to maximum
  specificity; ask.
- **The area/taxonomy tag for the hub entry**, whenever the surface sits on a genuine boundary in
  your own product's information architecture.
- **The owner attribution string**, exactly as your prototyping tool expects it (e.g. a
  `git config user.name`, if that's how your tool's write-guard identifies authors) — confirm,
  never guess.
- **The slug**, if more than one reasonable option exists.

This step exists so the stage stays reusable across every run: the questions above don't change
run to run, only the answers do.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Working: `../08_vision-horizon/output/vision-horizon.md` — the bet, and the Now/Next/Later chain
- Working: `../CLAUDE.md` — sphere of influence, which bounds what surfaces this run may propose
- Working: `../04_make-tangible/output/` — anything already made tangible feeds the screen inventory
- Working: `../05_pressure-test/output/` — the edge cases that decide which states get built

**Your prototyping tool's own reference docs — read before writing, in that tool's own repo, not
here.** Name the actual paths in this run's `CLAUDE.md` once you have a tool, the same way
`_shared/CONTEXT.md` names `_shared/` files. Typically you'll want:
- the tool's invocation contract (how it turns a brief into a prototype)
- its component/design-system foundations doc, read before proposing any UI
- its own glossary — vocabulary the brief must match, not invent
- a worked example brief from a prior run, if one exists, as the model to copy

## Process
1. **Decompose into questions.** One prototype surface per falsifiable question, not one prototype
   for the whole run. Two or three narrow surfaces beat one omnibus every time. If a horizon yields
   no question a UI could answer, it does not get a surface.
2. **Name and check each slug.** Kebab-case. Refuse collisions with live surfaces and with any
   reserved roots your tool uses (e.g. `login`, `api`, `_shared`, a hub route). Check against your
   tool's actual registry, not from memory.
3. **Map the run's actors onto your tool's existing cast**, if it has one. Many prototyping tools
   ship a fixed persona set, fixed system roles and a fixed clock for demo data. Vision-language
   segments must be translated onto that cast, or the surface silently invents a second domain
   model.
4. **Write the screen inventory.** Named routes. Whatever your tool's convention is, the rule is
   absolute either way: *a screen not listed here is out of scope.*
5. **Choose components before writing any.** Precedence: an existing design-system primitive → a
   composed pattern built from primitives → semantic design tokens → a one-off, flagged. Never raw
   hex values. Name the specific components and their variants per screen. That naming is what buys
   the look and feel — it is the highest-leverage part of this brief.
6. **Declare the fake/real line.** Explicitly, per screen. Default: everything faked except
   navigation, state transitions and the one interaction the question turns on.
7. **Decide bundles and divergence**, matching whatever composition units your tool supports (a
   shell, a demo switcher, named flow slices, or the full set). Declare any domain divergence, and
   respect whatever non-forkable floor your tool defines (shared entity ids, a shared cast, a shared
   seed clock, or similar) — those are never redefined per-surface.
8. **Translate the vocabulary.** Every term in the brief must exist in your tool's own glossary, if
   it has one. Coinages from the vision get mapped or dropped.

## Ownership
If your prototyping tool gates writes by author identity, put that exact string here — the name in
`../CLAUDE.md` under *Owner of the 12-month view*, written exactly as your tool expects it (e.g. a
human name matching `git config user.name`, never a handle or an email). Get it wrong and a
write-guard hook can silently deny every subsequent edit to that surface. Confirm the exact string
with the owner rather than guessing it.

## Blind spots to call out
- **One giant prototype.** The most likely failure of this stage. A single surface expressing the
  whole run answers nothing.
- **A question that can't be wrong.** "What does the future of X feel like?" is not a question — no
  answer to it would change anything. Write the no as well as the yes.
- **Specifying a build.** Services, persistence, auth, real data: all out of scope. Prefer a
  pattern that marks the absence of a real backend explicitly rather than faking one convincingly.
- **Inventing components.** A brief describing bespoke UI produces a prototype that looks nothing
  like your actual product, which defeats the point of using a shared prototyping tool at all.
- **Surfaces outside the sphere of influence.** If a surface needs another run's territory to make
  sense, it belongs in `101-prototype-handoff` after synthesis, not here.
- **House-style rules your tool enforces** (e.g. no em dashes in rendered copy) — check for them
  and follow them; they're usually there for a reason specific to that tool's rendering.

## Outputs
- `prototype-briefs/<slug>.md` → `output/` — one per surface. Match whatever frontmatter/spec
  format your prototyping tool actually consumes; if you don't have one yet, use plain sections for
  title, owner, date, the one falsifiable question, screen inventory, component choices, and the
  fake/real line per screen.
- `HANDOFF.md` → `output/` — the ranked reading order, the settled decisions that must not be
  reopened, and the single next action naming the first surface to build.

## Human check
Give one brief to someone who has not read the vision and ask them what question the prototype
answers. If they answer with a feature description instead of a question, rewrite it. Then ask the
named owner whether they would defend that question in a review — if not, it's the wrong question
or the wrong owner.
