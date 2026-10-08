# Report content schema — the shape of the input

What the report builder needs handed to it. Every slot maps to a component in
`report-design-system.md`. **A slot with no evidence behind it is cut, not filled with prose.**

The pipeline already produces most of this. The right-hand column names where it comes from —
where it says *derive*, that is a real gap the report stage has to close by asking.

## Two sources, one schema

The report stage runs in two places, against two different argument documents:

| Stage | Source document | Scope of the claim |
|---|---|---|
| `NN-<run>/09_report` | `../08_vision-horizon/output/vision-horizon.md` | one problem space |
| `100-report` | `../99-vision-synthesis/output/12-month-vision.md` | the whole product |

Below, **`<source>`** means whichever of those two the stage was pointed at. The schema and the
design system are identical either way — a single-run report is not a lesser artefact, it is a
narrower claim. A run-level report that quietly widens its claim past the run's sphere of influence
is the failure mode to watch for.

---

## Document

```yaml
document:
  title:        string          # "The Company Layer" — a noun phrase, not a sentence
  meta_line:    string          # "Product position & plan · internal · rev. 25 Aug 2026"
  nav:          [{ label, anchor }]          # 6 max. Not every section is in the nav.
```
| Slot | Source |
|---|---|
| `title` | *derive* — the through-line compressed to a noun phrase |
| `meta_line` | run metadata + date |
| `nav` | the sections you actually build |

## Hero — C3 + C4

```yaml
hero:
  eyebrow:          string                    # uppercase kicker
  headline_line1:   string                    # the rejection: "We are not X"
  headline_line2:   string                    # the assertion, rendered <em> in forest
  deck:             prose                     # ≤ 3 sentences, one of which says where evidence lives
  stats: [{ value, qualifier?, caption }]     # EXACTLY 4
```
`headline` is the reframe move — reject the obvious identity, assert a better one. The four stats
must be independently sourced, and each must appear again later with its working shown. No need to link to the working here. Four stats you cannot source is the signal to cut the strip, not to soften the numbers.

**Source:** `<source>` (the through-line, or the run's bet) · *derive* the stats from
`05_pressure-test` and `_shared/product-context.md`.

## Verdict — C5

```yaml
verdict:
  eyebrow:          string
  prose:            string     # 3 sentences. The whole argument, before any argument.
  emphasis_clause:  string     # rendered gold <strong> inside prose
```
The skim-stop. If a reader stops here they must still have the position.
**Source:** the one sentence from `<source>`.

## Journey — C6 + C7

```yaml
journey:
  title: string
  deck:  prose
  steps: [{ number, title, one_line }]        # EXACTLY 5
```
Each step answers one question and sets up the next. Five steps that could be reordered are a
contents page, not a journey — that is the failure mode.
**Source:** the sequenced horizons in `<source>`. At run level this is usually the Now/Next/Later
chain expanded; if it only yields three steps, build three cells rather than padding to five.

## Stages

```yaml
stages: [
  id:           string                        # anchor
  badge:        string                        # "01".."05" | "AI" | "†" | "§" | "▪"
  title:        string
  deck:         prose
  ground:       enum[paper, surface, ink, sage, sand]
  blocks:       [ <block> ]
]
```
Ground assignment is fixed by the rhythm in the design system, not chosen per report.

### Blocks

```yaml
comparison_cards:        # C8 — external threat, three rivals
  items: [{ kicker, title, body, callout_label, callout_body, accent }]   # 3
  # callout_label is "The catch:" or "Watch:" — every positive card carries a counterweight

asset_grid:              # C9 — what we own. Renders on ink.
  items: [{ index, title, body, proof_point }]      # 5
  one_liner: { kicker, statement, emphasis, footnote }   # the 6th cell, forest ground

flywheel:                # C10 — the loop and where it leaks
  aria_label: string
  gears: [{ index, name, volume_value, volume_label, leak_text, accent, keystone: bool }]  # 4
  connectors: [{ label, glyph }]                    # 4
  centre: { headline, body, emphasis, alarm_line }  # the keystone callout
  caption: string
  # EXACTLY ONE gear carries keystone:true. Two keystones means you haven't decided.

numbered_articles:       # C11 — ranked leaks, or the things we build
  rule: enum[ink-2px, forest-2px]
  ordinal_style: enum[ordinal_words, two_digit]     # "1st" vs "01"
  items: [{ ordinal, title, body, tagline? }]       # 3
  # tagline binds each item to a mechanism, a rival and a target:
  # "Turns gear 03 · answers a rival's Aug release · target: 20% → 35%"

accent_band:             # C12 — a decision or a trade, stated once
  tone: enum[coral, forest]
  kicker, headline, body, emphasis?

data_table:              # C14 — the metrics table, the release log
  columns: [string]
  rows: [[ { text, tone: enum[default, muted, alarm, numeric, key] } ]]
  # key=first col bold nowrap · numeric=Georgia · alarm=coral bold (e.g. "None")

caution_list:            # C15 — Read with care
  items: [{ title, body }]                          # 5

footnote_cards:          # small C8 variant
  items: [{ title, body }]                          # 3

evidence:                # C13 — attaches to ANY stage
  summary_label: string                             # prefixed "▸ "
  layout: enum[table, two_column_prose, single_prose, stacked_prose]
  body: prose | prose[] | data_table
```

## Sources & footer — C16

```yaml
sources:
  items: [{ index, label, url }]     # 12 in the source. Public sources dated; internal named.
  method_note: prose                 # what changed between drafts, and what the method was
footer:
  left:  string                      # document identity
  right: string                      # revision + provenance
```

---

## Stage → block mapping

The pipeline's stages do not map one-to-one onto the report's sections. This is the mapping the
report builder applies. Run-level paths are relative to the run root; `100-report` substitutes the
synthesis output wherever a run stage is named.

| Report section | Block | Fed by |
|---|---|---|
| Hero, Verdict | C3, C4, C5 | `<source>` — through-line / the bet + the one sentence |
| The journey | C7 | `<source>` — sequenced horizons |
| What changed | C8 + evidence table | `_shared/product-context.md` · `02_explore` competitive scan |
| What we own | C9 | `<source>` — capabilities gained |
| Where we stall | C10 + C11 | `03_converge/output/direction.md` · `05_pressure-test` |
| What we build | C11 + C12 | `<source>` — Now/Next/Later with stated dependency |
| Where this lands | C14 + C12 | `07_engineering-refinement/output/solution-scope.md` · owners |
| Read with care | C15 + evidence | `05_pressure-test` · `<source>` gaps · `_shared/decision-log.md` |
| Sources | C16 | every stage's citations, plus the method note |

---

## The evidence rule

Every headline claim in the report must have a `<details>` under it carrying the working. The
report is not allowed to assert anything the pipeline did not evidence.

Three outcomes when a claim has no evidence, in order of preference:
1. **Cut the claim.** Usually correct.
2. **Demote it** into the caveats section as a stated assumption.
3. **Label it aspirational**, explicitly, in the body text — never in a headline or a stat.

Writing prose to fill an empty slot is the fourth option and it is not available.

> **One-off audience cuts** — a readout for a specific meeting, where committed-vs-aspirational
> needs to be an explicit column — are not part of this stage. Render the standing report, then
> cut for the room by hand.
