# Run: <FEATURE NAME>

Feature PRD run. Fill this header when instantiating the run.

## Identity
- **Pipeline:** feature-prd
- **Upstream:** none
- **Feature:** <one line — what the user can do after this ships>
- **Release:** <which release this belongs to, or none>
- **Owners:** Product — <name> · Engineering — <name>

## Route
`Pipeline` names the method this run copies (`_templates/feature-prd/`). `Upstream` is a
workspace-relative path to the output this feature is a slice of — usually a release PRD run's
`04_prd/output/prd.md` — or `none`.

Read `CONTEXT.md` for the running order. Then open the stage folder you are working and read its
`CONTEXT.md`. Load `../_shared/operating-principles.md` and `../_shared/house-view.md` always; load
nothing else unless the stage contract's Inputs list names it.
