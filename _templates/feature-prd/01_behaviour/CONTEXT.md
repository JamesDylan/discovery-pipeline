# 01_behaviour — decide what the user sees

One job: the behaviour of the feature in every state, including the unhappy ones. Decide it; do not
write the PRD yet.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/prd-principles.md`
- Working (this run): `../00_intake/output/intake.md`
- Working (this run): `../CLAUDE.md` — run identity
- Working (upstream): the `prd-digest.md` beside the file the `Upstream:` line names, not that file
  itself. First run `./digest <Upstream path>` from the workspace root; it is free and refreshes the
  digest if the PRD changed. If it says there is no release PRD there, load the upstream file
  instead. Open a full upstream section only when the digest line is not enough, and name the
  section you opened.
- **Do NOT load:** `../02_spec/` onward.

## Process
1. Name the users and the job each one is doing.
2. Walk the main path, step by step.
3. List every state: empty, loading, error, no permission, partial data, and any the domain adds.
   Give each one an outcome.
4. List non-goals and the decisions still open, each with an owner.

## Outputs
- `behaviour.md` → `output/` — users and jobs, main path, states with outcomes, non-goals, open decisions

## Human check
Walk the unhappy path aloud. Every state you reach has a defined outcome. Any state without one will
be invented by whoever builds it.
