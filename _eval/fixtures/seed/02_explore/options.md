# 02_explore — options (fixture seed)

Synthetic. Four materially different bets, deliberately including one the pair would resist. No
ranking — that belongs to `03_converge`.

## Option A — Credits become company currency, not traveller property

**The bet:** ownership is the problem, so move it. At cancellation, residual value is pooled to the
company; the traveller is released from it entirely.

**How it works:** the pool is a company-level balance. Booking draws down automatically when a fare
on a held carrier is within a policy-set tolerance of the cheapest option. The traveller sees a
normal booking flow and never sees a credit.

**Assumes:** credits can be legally re-pointed between employees (load-bearing assumption 2).

**Why someone smart chooses it:** it removes the need rather than easing the task. Nobody
administers anything, and the saving lands where the budget is.

## Option B — Silent drawdown at fare-choice time

**The bet:** the decision moment is the leverage point, and the decision should never be surfaced.
The system re-ranks fares to favour carriers holding credits, within tolerance, and shows one
price: the net price.

**How it works:** no balance, no wallet, no notification. The credit is spent as a consequence of
normal booking.

**Assumes:** travellers accept a constrained itinerary when the constraint is invisible
(assumption 1). Also assumes the company accepts an opaque ranking.

**Why someone smart chooses it:** highest conversion per unit of effort, and it needs no behaviour
change from anyone.

## Option C — Make it Finance's number

**The bet:** this is not a product problem at the point of booking. It is a reporting problem.
Outstanding and expiring credit value appears on the spend report Finance already reads, with an
expiry clock.

**How it works:** no change to the booking flow at all. One new block on an existing report, plus
a threshold alert. Finance then applies pressure through policy, which is what Finance does.

**Assumes:** Finance acts when leakage becomes visible (assumption 3).

**Why someone smart chooses it:** cheapest to build, tests the business case before any flow work,
and creates the internal advocate the other options need.

## Option D — Underwrite the credits and drop the problem

**The bet:** product should not manage this at all. the company (or a partner) buys the residual value at
a discount at cancellation, the company gets cash back immediately, and the credit-spending problem
becomes someone's balance sheet.

**How it works:** commercial mechanism with a thin product surface — accept/decline at
cancellation.

**Assumes:** the discount is acceptable to companies and the book is profitable at scale.

**Why someone smart chooses it:** it converts an administration problem into a priced one and is
the only option that works on carriers that report nothing back.

## The one the pair would resist

D. It is barely a product, it carries balance-sheet risk, and it makes the team's work smaller. It
is in the set because it is the only option that ignores the visibility framing entirely, and
because it sets the price the other three options have to beat.

## What is not here

No option that helps a traveller find and manually apply a credit. That is the balance-screen
answer `01_frame` argued against, and including it would only serve to make the others look bold.
