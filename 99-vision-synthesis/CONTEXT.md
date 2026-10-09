# 99-vision-synthesis — one vision, not two summaries

One job: produce a 12-month product vision that no run produced alone.

## Inputs
- Reference (every run): `../_shared/operating-principles.md`
- Reference (every run): `../_shared/house-view.md`
- Reference: `../_shared/vision-principles.md`
- Working: `../NN-<slug>/08_vision-horizon/output/vision-horizon.md` — one per completed run.
  Find them with `ls [0-9]*-*/08_vision-horizon/output/vision-horizon.md` (only discovery runs have an `08`)
- Reference: `../_shared/product-context.md` — the product, and the key partner for the readout
- Reference: `../_shared/decision-log.md`
- **Do NOT load:** the runs' intermediate stages. If the `08` outputs don't carry the argument,
  fix them there rather than reaching back through the pipeline.

## Hard rule
**Do not staple.** Domain visions side by side is not a product vision — it is the exact
"vision by aggregation" failure mode, and the team will read it as one. The synthesis must produce
something no run produced alone, or it has failed.

## Process
1. **Read the bets side by side.** Where do they agree? A shared belief reached independently is
   the strongest signal available. Where do they conflict? Resolve it — don't average it.
   What belief sits above both?
2. **Find the through-line.** Test a candidate: does it explain every run's Now/Next/Later, and
   would it have predicted them? Too general to be wrong = too weak to be useful.
3. **Sequence across runs.** One dependency map. Look for shared foundations being built twice,
   ordering conflicts where A's Next needs B's Later, and the single capability unlocking the most.
4. **Name the gaps.** Which parts of the product have no vision because no run covered them? Name them as
   the next problem spaces rather than pretending the picture is complete.
5. **The belief test.** Would an engineer on the product, after reading this, be able to say what
   it is becoming? If not, iterate. Quality of analysis is irrelevant if it doesn't change what the team
   believes — that belief is the actual deliverable.
6. **Partner readout** — only if `product-context.md` names a key partner. Different audience,
   different cut: the commercial thesis rather than the product story · what the product uniquely
   does that matters to them · **committed vs aspirational,
   labelled honestly** (aspirational framed as committed is the fastest way to lose that room) ·
   what decision or support is being asked for.

## Interrogate
- What is here because it's real, and what because it completes the story?
- Which run is carrying the vision, and do the others add anything?
- Where is this indistinguishable from a competitor's vision?

## Outputs
- `12-month-vision.md` → `output/` — through-line, sequenced horizons, capabilities, what we're
  betting against, gaps, owner per domain
- `partner-readout.md` → `output/` — optional, per step 6. A one-off for that meeting; it stays markdown
  and does **not** feed `100-report`, which renders the standing vision only.

## Human check
Say the one sentence to three people who work on the product. If you get three different readings of what
it means, it isn't finished.
