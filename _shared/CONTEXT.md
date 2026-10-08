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
| `accelerator-brief.md` | The source brief — method, dates, roles, problem spaces, playback questions | `00_setup`, `06_playback` |
| `timeline.md` | Hard dates for this cycle | As needed |
| `report-design-system.md` | The visual contract for every report this workspace renders | `09_report`, `100-report` |
| `report-content-schema.md` | The report's slot map and stage→block mapping | `09_report`, `100-report` |
| `prototype-target.md` | Which prototyping tool the handoffs brief, and its conventions. Blank = brief a human designer | `10_prototype-handoff`, `101-prototype-handoff` |

`accelerator-brief.md`, `timeline.md`, `product-context.md`, `house-view.md` and `prototype-target.md`
ship blank: fill them for your organisation. The two `report-*` files are part of the method and
work as shipped — change them only if you want a different report look.

## Rules

- **One home per fact.** If something here is true, do not restate it in a stage contract — point at it.
- If a stage is about to proceed on an assumption that belongs in `product-context.md` and isn't
  there, stop and flag the gap rather than inventing it.
- `decision-log.md` is append-only. Never rewrite an entry.
