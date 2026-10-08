# Run: Unused Ticket Credits

Eval fixture. Not a real run. `_eval/evaluate.py` copies this over a fresh `_template` copy to make
a throwaway run, then tests one stage against it.

Deliberately not any live run's problem space: if the fixture shared a problem space with a live
run, the eval would start grading the live run's thinking instead of the method.

## Identity
- **Problem space:** Corporate travellers cancel flights and generate airline credits that expire unused, and neither the traveller nor the travel manager can reliably see, value or spend them.
- **Sphere of influence:** Post-booking value recovery in the booking product — what happens to money already spent once a trip changes.
- **Pair:** Product — Fixture Product · Design — Fixture Design
- **Owner of the 12-month view:** Fixture Owner

## Questions in scope
1. Who is accountable for a credit once a trip is cancelled, and does anyone experience that as their job?
2. What would have to be true for a credit to be spent by default rather than chased?
3. How much of this is a visibility problem versus an incentive problem?

## Note on Q3
Do not assume visibility. A traveller who can see a credit still has no reason to prefer the
airline that holds it. `01_frame` must establish which of the two is load-bearing before anything
is designed against it.

## Run-specific notes by stage

**`02_explore` — where to look for analogues.** Not a travel problem first. Look at gift-card and
store-credit balances, airline miles expiry mechanics, Xero credit notes against invoices, unspent
FSA/HSA balances in US healthcare, prepaid mobile top-up expiry, and cloud committed-spend
drawdown. Force at least one option where no human ever looks at a credit balance, and one where
the credit is pooled at company level rather than held by the traveller.

**`05_pressure-test` — the mess that matters here.** Credits held in the traveller's name but paid
for by the company, name-change fees that exceed the credit's value, credits on airlines the
company has no route need for, employees who leave before spending one, multi-currency and
fare-difference rules, partial-value credits, airline-specific expiry clocks, and what happens
when a company changes TMC mid-cycle.

## Route
Read `CONTEXT.md` for the pipeline and the stage table. Then open the stage folder you are working
and read its `CONTEXT.md`. Load `../_shared/operating-principles.md` and `../_shared/house-view.md`
always; load nothing else unless the stage contract's Inputs list names it.
