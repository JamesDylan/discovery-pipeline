# 02_explore — open the solution space

One job: generate materially different approaches. No evaluation.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Working (this run): `../CLAUDE.md` — run identity **and any run-specific note on this stage**
- Working (this run): `../01_frame/output/frame.md`
- Working (this run): `../00_setup/output/inventory.md` (reusable patterns and assets only)
- **Do NOT load:** `../03_converge/` onward. Ranking happens in the next stage, not this one.

## Hard rule
No option is judged here. If the user starts ranking, stop them.

## Process
1. **Generate three or more materially different approaches.** "Materially different" means a
   different underlying bet, not different UI. Test: if two options would be built by the same
   team in the same sequence, they are one option.
   Axes that force real divergence:
   - Remove the need *vs* make the task easier
   - System-inferred *vs* user-declared
   - Progressive (earn it over time) *vs* upfront
   - Individual *vs* network (use the org graph)
   - Product *vs* incentive *vs* policy
2. **Mine what exists.** Existing product patterns worth extending, and analogous experiences outside travel.
   The run's `CLAUDE.md` names where to look for this problem space specifically.
3. **Use AI to broaden, not polish.** Argue for the option the pair likes least. Ask what a
   competitor with no legacy would do. Ask what is obvious in hindsight.
4. **Make each option arguable.** One paragraph plus the key moment sketched. Not designs.

## Interrogate
- Which option came first, and what does its existence stop you seeing?
- What does this look like if the user has to do nothing at all?
- Which option are you avoiding because it's politically or technically inconvenient? Add it.

## Outputs
- `options.md` → `output/` — each option with: the underlying bet, how it works, what it assumes,
  why someone smart would choose it

## Human check
Point at the option that makes you uncomfortable. If there isn't one, the set is too narrow — go again.
