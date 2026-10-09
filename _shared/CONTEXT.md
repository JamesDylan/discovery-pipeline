# _shared — the factory layer (L3)

Stable across every run and every pipeline. These are **constraints to internalise**, not working artifacts to process.

Stage names below are per pipeline: `discovery/03_converge` means stage `03_converge` of a
discovery run.

| File | What it is | Load when |
|---|---|---|
| `operating-principles.md` | How Claude behaves in every stage | Always |
| `house-view.md` | Your theory of best for this product's work | Always |
| `vision-principles.md` | Tests a 12-month vision must pass, and failure modes | `discovery/03_converge`, `discovery/08_vision-horizon`, `99-` |
| `product-context.md` | Product, customer, commercial and constraint context | `discovery/00_setup` fills it; most pipelines read it |
| `setup-questionnaire.md` | The questions that fill `product-context.md` fast | `discovery/00_setup` only |
| `decision-log.md` | Append-only record of calls made and why | Written by decision stages in any pipeline |
| `accelerator-brief.md` | The source brief — method, dates, roles, problem spaces, playback questions | `discovery/00_setup`, `discovery/06_playback` |
| `timeline.md` | Hard dates for this cycle | As needed |
| `report-design-system.md` | The visual contract for every report this workspace renders | `09_report`, `100-report` |
| `report-content-schema.md` | The report's slot map and stage→block mapping | `09_report`, `100-report` |
| `prototype-target.md` | Which prototyping tool the handoffs brief, and its conventions. Blank = brief a human designer | `discovery/10_prototype-handoff`, `101-prototype-handoff` |
| `prd-principles.md` | Tests a PRD must pass, and failure modes | `release-prd/02_problem`, `release-prd/03_scope`, `feature-prd/01_behaviour` |
| `prd-template.md` | The release PRD's section shape | `release-prd/04_prd` |
| `feature-prd-template.md` | The feature PRD's section shape | `feature-prd/02_spec` |
| `delivery-target.md` | Which delivery tool feature PRDs convert for, and its conventions. Blank = the handoff stops | `feature-prd/04_delivery-handoff` |

`accelerator-brief.md`, `timeline.md`, `product-context.md`, `house-view.md`, `prototype-target.md` and
`delivery-target.md` ship blank: fill them for your organisation. `prd-principles.md`, `prd-template.md`
and `feature-prd-template.md` ship as generic starters: replace them with your own. The two `report-*` files are part of the method and
work as shipped — change them only if you want a different report look.

## Rules

- **One home per fact.** If something here is true, do not restate it in a stage contract — point at it.
- If a stage is about to proceed on an assumption that belongs in `product-context.md` and isn't
  there, stop and flag the gap rather than inventing it.
- `decision-log.md` is append-only. Never rewrite an entry.
