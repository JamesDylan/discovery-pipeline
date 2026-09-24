# _shared — the factory layer (L3)

Stable across every run. These are **constraints to internalise**, not working artifacts to process.

| File | What it is | Load when |
|---|---|---|
| `operating-principles.md` | How Claude behaves in every stage | Always |
| `house-view.md` | Your theory of best for this product's work | Always |
| `vision-principles.md` | Tests a 12-month vision must pass, and failure modes | `03_converge`, `08_vision-horizon`, `99-` |
| `product-context.md` | Product, customer, commercial and constraint context | `00_setup` fills it; `01_frame`, `05_pressure-test` and `08_vision-horizon` read it |
| `setup-questionnaire.md` | The questions that fill `product-context.md` fast | `00_setup` only |
| `decision-log.md` | Append-only record of calls made and why | Written by `03`, `06`, `07` |

Not shipped here, but referenced by `RUNBOOK.md` if you want them: a source brief for your own
accelerator/programme, a hard-dates `timeline.md`, and a report design system / prototype-handoff
contract if you build (or already have) a rendering or prototyping tool downstream. Those are
specific to your organisation's tooling — add them here once you have them, following the shape of
the files already in this folder.

## Rules

- **One home per fact.** If something here is true, do not restate it in a stage contract — point at it.
- If a stage is about to proceed on an assumption that belongs in `product-context.md` and isn't
  there, stop and flag the gap rather than inventing it.
- `decision-log.md` is append-only. Never rewrite an entry.
