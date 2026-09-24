# 03_converge — direction (fixture seed)

Synthetic. Exists so `08_vision-horizon` can be tested in isolation via the documented carve-out
(`08` may run on `03`'s output alone when `07` is still in flight).

## The call

Option C first (make it Finance's number), then Option A (credits become company currency). B is
folded into A as its booking mechanic. D is priced and parked.

## Why

Two of three load-bearing assumptions from `01_frame` are unproven, and A is expensive against
both. C costs least, tests assumption 3 directly, and produces the internal advocate A will need
to clear a legal and tax question. Sequencing C before A is not caution — C is the cheapest
available experiment on the assumption that carries the most weight.

## What was rejected, and why

- **B alone** — an opaque re-ranking with no company-level owner is a trust liability. Someone
  eventually asks why the more expensive flight was recommended, and "we spent your credit" is a
  bad answer arriving late. B survives only inside A, where the pool makes it legible.
- **D** — not rejected on merit. It is the only option that works on non-reporting carriers, and it
  sets the price A must beat. Parked, with the discount rate written down so the comparison can be
  made honestly later.
- **The balance screen** — never entered the set. `01_frame` established this is not a visibility
  problem.

## The trade-off, stated plainly

We are choosing to make this Finance's problem before we make it the product's problem, which
means we accept that no traveller's experience improves for at least two quarters, and that the
first thing we ship is a report block rather than a capability. We are betting that an internal
advocate is worth more than an early traveller-facing win.

## What we are betting against

That anyone will experience unused credits as their own problem without a number on a report they
already read.

## Reversal conditions

- If Finance sees the number and does not change policy within one quarter, assumption 3 is false.
  Stop; the business case is smaller than claimed and A is not fundable.
- If the legal question on re-pointing credits resolves negatively for major carriers, A is dead
  and D becomes the only path past traveller-level options.
- If a carrier changes reporting such that residual value becomes measurable, the expiry estimate
  should be re-derived before A is scoped — the 55–70% range may be doing more work than it can
  bear.

## Open, owned

- Legal position on re-pointing credits between employees — no owner yet. **This blocks A.**
- Finance reconciliation spec still unreadable. Blocks C's scoping, not its decision.
