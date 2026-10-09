# 00_setup — inventory (fixture seed)

Synthetic. Plausible shape, invented numbers. Exists so a downstream stage has a real input to
stand on rather than stalling.

## Assets, with access tested

| Asset | What it is | Access | Age |
|---|---|---|---|
| Cancellation events extract | 18 months of cancelled-segment records with residual value flags | Opened | Current |
| Airline credit rules matrix | Per-carrier expiry, name-change and fare-difference rules, 14 carriers | Opened | 7 months — partial |
| Travel manager interviews (n=9) | Transcripts, 2024 study on post-booking admin load | Opened | 14 months — **flag as stale** |
| Support ticket taxonomy | Tickets tagged `credit`, `residual`, `unused-ticket` | Opened | Current |
| Design system | Existing product components, including balance and wallet patterns | Opened | Current |
| Finance reconciliation spec | How credits currently appear (or don't) in company reporting | **Cannot open** — owner on leave | Unknown |

## Current-state numbers

- ~4.1% of booked segments are cancelled with residual value. `[assumption]` — derived, not measured
- Median residual value per credit: ~$310
- Estimated share expiring unused: 55–70%. Wide because two carriers report nothing back
- Support tickets mentioning a credit: ~1.8% of all tickets, but 3rd-highest handling time
- Travel managers who could name their company's outstanding credit balance when asked: 1 of 9

## Gaps, classified

- **Blocking:** finance reconciliation spec is unreadable. Any option that puts credits into
  company-level reporting cannot be scoped without it.
- **Degrading:** traveller-side interviews are 14 months old and pre-date the current booking flow.
  Usable for motivation, not for flow.
- **Ignore:** per-carrier rules are incomplete for 3 small carriers. Long tail, not load-bearing.

## Reusable patterns

- Wallet / balance component exists in the design system and is already used for expense floats.
- The booking flow already surfaces a "you have previously flown this route" nudge — a proven
  injection point with measured engagement.

## SMEs booked

- Airline contracts lead — 20 min, for `01_frame`
- Two travel managers — 20 min each, for `05_pressure-test`
- Finance systems analyst — pending, blocked on the same absent owner
