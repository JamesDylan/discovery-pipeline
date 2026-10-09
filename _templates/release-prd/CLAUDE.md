# Run: <RELEASE NAME>

Release PRD run. Fill this header when instantiating the run.

## Identity
- **Pipeline:** release-prd
- **Upstream:** none
- **Release:** <one line — what ships, for whom>
- **Outcome this release must move:** <fill — one metric, current value, target>
- **Owners:** Product — <name> · Design — <name> · Engineering — <name>
- **Sign-off:** <name — who accepts the PRD>

## Route
`Pipeline` names the method this run copies (`_templates/release-prd/`). `Upstream` is a
workspace-relative path to another run's output this run builds on — often a discovery run's
`07_engineering-refinement/output/solution-scope.md` — or `none`.

Read `CONTEXT.md` for the running order. Then open the stage folder you are working and read its
`CONTEXT.md`. Load `../_shared/operating-principles.md` and `../_shared/house-view.md` always; load
nothing else unless the stage contract's Inputs list names it.
