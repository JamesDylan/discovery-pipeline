# 00_intake — state the feature and its upstream

One job: one statement of the feature, and a list of what its upstream already decided. No design
yet.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/product-context.md`
- Working: `../CLAUDE.md` — run identity
- Working (upstream): the `prd-digest.md` beside the file the `Upstream:` line names, not that file
  itself. First run `./digest <Upstream path>` from the workspace root; it is free and refreshes the
  digest if the PRD changed. If it says there is no release PRD there, load the upstream file
  instead. Open a full upstream section only when the digest line is not enough, and name the
  section you opened.
- **Do NOT load:** any other stage folder of this run.

## Process
0. If `output/intake.md` already exists, it was pre-filled from the release run's
   `feature-intakes/`. Do not redo steps 1–3. Run only the Human check, and edit the intake if it
   fails.
1. State the feature in one sentence: who can do what, that they cannot do today.
2. From the upstream digest, list the decisions that bind this feature, by ID (rule, requirement,
   question) or section. Do not copy them.
3. List any other sources and constraints. Ask; do not assume. One question at a time.

## Outputs
- `intake.md` → `output/` — a title of the feature's ID in the upstream digest (if it has one) and
  its name, then headings: Feature, Release, Binding upstream decisions (by reference),
  Screens it owns, Open questions, Sources and constraints. The release run's `04_prd` writes the
  same shape

## Human check
Read the feature sentence to the release owner. If they describe a different feature, stop here.
