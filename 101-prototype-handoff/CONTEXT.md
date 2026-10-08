# 101-prototype-handoff — convert the vision into briefs the prototyping tool can build

One job: produce the instructions that let the prototyping tool named in
`../_shared/prototype-target.md` stand up a look-and-feel UI of the synthesised vision, without
anyone re-deriving the vision from scratch.

**Optional and discrete.** Run it for the surfaces that need more than one run's territory. Single-
run surfaces belong in that run's `10_prototype-handoff` — same method, narrower claim, and the
owner is the pair rather than whoever owns the synthesis.

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

## Inputs
- Reference (every run): `../_shared/operating-principles.md`
- Reference (every run): `../_shared/house-view.md`
- Reference: `../_shared/prototype-target.md` — which tool, where its docs live, its brief format,
  and the conventions the steps below apply "per the target"
- Working: `../99-vision-synthesis/output/12-month-vision.md` — the through-line and sequencing
- Working: each run's `CLAUDE.md` — sphere of influence, which decides who owns each surface
- Working: each run's `10_prototype-handoff/output/` if it ran — **read it before proposing
  anything.** A surface already briefed at run level is not re-briefed here.

**Then read the tool's own reference docs**, at the paths `prototype-target.md` lists, in the tool's
repo, not here — before writing anything.

## Process
1. **Decompose into questions.** One prototype surface per falsifiable question, not one prototype
   for the whole vision. Three narrow surfaces beat one omnibus every time. If a horizon yields no
   question a UI could answer, it does not get a surface.
2. **Justify why each surface is here and not in a run.** The test: does the question need two
   runs' territory to be askable? If not, it belongs to a run. Pushing run-level work up to this
   stage concentrates ownership in one person, which is the opposite of what the programme is for.
3. **Name and check each slug.** Kebab-case. Refuse collisions with live surfaces and with the
   reserved roots per the target. Check against the tool's actual registry, not from memory.
4. **Map the vision's actors onto the target's existing cast**, if it has one (fixed personas,
   system roles, a seed clock). Vision-language segments must be translated, or the surface
   silently invents a second domain model.
5. **Write the screen inventory.** Named routes, in the target's route convention. The rule is
   absolute: *a screen not listed here is out of scope.*
6. **Choose components before writing any.** Precedence per the target; by default: an existing
   design-system primitive → a composed pattern built from primitives → semantic tokens → a one-off,
   flagged. Never raw hex. Name the specific components and their variants per screen. That naming
   is what buys the look and feel — it is the highest-leverage part of this brief.
7. **Declare the fake/real line.** Explicitly, per screen. Default: everything faked except
   navigation, state transitions and the one interaction the question turns on.
8. **Decide bundles and divergence**, using the composition units per the target. Declare any
   domain divergence, and respect the target's non-forkable floor. A cross-run surface is the most
   likely place to need a real divergence — declare it rather than letting it happen.
9. **Translate the vocabulary.** Every term in the brief must exist in the target's glossary.
   Coinages from the vision get mapped or dropped.

## Ownership
The owner is **the PM who ran this process** for the run the surface sits closest to, written
exactly in the form the target's Ownership line specifies. If the tool gates writes by author
identity, a wrong string silently blocks every later edit to that surface. Confirm the exact string
with them rather than guessing it. A cross-run surface still gets **one** owner; other names go
wherever the target puts collaborators.

## Blind spots to call out
- **One giant prototype.** The most likely failure of this stage. A single surface expressing the
  whole vision answers nothing.
- **A question that can't be wrong.** "What does the future of X feel like?" is not a question —
  no answer to it would change anything. Write the no as well as the yes.
- **Hoarding surfaces here** that belong to a run. See step 2.
- **Specifying a build.** Services, persistence, auth, real data: all out of scope. Mark the absent
  backend explicitly (per the target, if it has a pattern for that) rather than faking one.
- **Inventing components.** A brief describing bespoke UI produces a prototype that looks nothing
  like the real product, which defeats the point of using the tool at all.
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
