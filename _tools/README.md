# _tools — scripts the process runs

Stage contracts call these as steps. They are part of making the work, not checking it; checking is
`_eval/`. Each one is free and uses no model. An agent runs them when a contract says so; a person
never has to.

## `./digest` — release PRD digest

A feature run needs its release PRD's IDs and the one-line meaning of each, not the whole document.
`./digest <release-run>` reads `04_prd/output/prd.md` and writes `prd-digest.md` beside it: header,
terms, which source wins, business rules, access, business requirements (no acceptance criteria),
open questions (closed ones as IDs only), screens, features and metrics.

**Who runs it, and when.** The agent, as a step in these stage contracts:

| Stage | When |
|---|---|
| `release-prd/04_prd` | Last step, after writing or revising `prd.md` |
| `release-prd/05_review` | After a review change is written back into `prd.md` |
| `feature-prd/00_intake`, `01_behaviour`, `02_spec` | Before reading the digest, with the `Upstream:` path. Covers a hand edit to `prd.md` |

Running it when the digest is current changes nothing, so a stage can always run it.

**How it finds things.** By heading and table column, so it is not tied to one template. Generic
defaults live in `prd_digest.py`. A house overrides them in a ` ```prd-rules ` block in
`_shared/prd-principles.md`, as lines of `id.<kind>: regex` (kinds: `requirement`, `question`,
`metric`, `feature`) or `section.<name>: regex`.

**How the eval checks it.** The digest's first line holds a hash of the PRD it was built from.
`./eval` reports `prd.digest-missing` and `prd.digest-stale` when the digest does not match, and
`prd.digest-fixture` when the parser no longer produces `_eval/fixtures/prd-digest/expected-digest.md`.

`./digest --file <prd> [--out <file>]` digests any PRD, for trying it on a real one.
