# _eval — does this workspace still do what it says?

The workspace has one load-bearing claim, stated in the root `CLAUDE.md`:

> An agent with no memory must be able to orient, act, and report status from these files alone.

That claim is cheap to break and expensive to notice. You edit a stage contract, rename an output,
sharpen a process step — and three stages downstream an agent quietly works from the wrong file or
stalls. This folder turns the walk test into something you can run.

## Run it

From the workspace root:

```
./eval                  # structure only — no tokens, ~1 second
./eval --open           # …and open the report
./eval doctor           # check the local Ollama model, once
./eval legibility       # local model runs the stages — free, repeatable
./eval all              # everything, including the graded behavioural layer
```

Terminal gives you a verdict and the top failures. The full detail is the HTML report at
`_eval/report/index.html` — grouped, filterable, with the file and line for every finding.

Exit code is `1` if anything blocking failed, `0` otherwise. Safe to put in a pre-commit hook.

## Three tiers, and what each one actually tells you

| Tier | Cost | Answers |
|---|---|---|
| `structure` | free, 0.1s | Do the contracts refer to things that exist, and agree with each other? |
| `legibility` | free (local model) | Is each contract unambiguous enough to *execute*? |
| `behaviour` | tokens | Does the stage produce work worth having? |

They are not substitutes. Structure can't tell you a contract is confusing. Legibility can't tell
you the thinking is any good. Only the last one answers the question the workspace exists to
answer, and it is the only one that costs anything — because **the agent is the thing under test**.
Validating contracts against a small local model and then running the programme on Claude would be
evaluating the wrong system.

---

## The layers, deliberately separate

### `structure` — free, fast, run it constantly

Pure filesystem and markdown analysis. No model calls. This is the layer you run every time you
touch a contract.

| Check | What breaks if you don't catch it |
|---|---|
| `walk.entrypoint-missing` | An agent lands in the workspace with nothing to orient on |
| `walk.route-target-missing` | The root route table sends you somewhere that isn't there |
| `contract.missing-section` | A stage with no Outputs section leaves nothing behind; with no Human check, nobody stops it |
| `contract.input-unresolved` | A contract names a reference file that doesn't exist — the stage runs on less than it claims |
| `contract.input-stage-missing` | A contract names a stage this run doesn't have |
| `contract.downstream-disagree` | **The silent killer.** Stage 02 writes `options.md`, stage 03 asks for `ideas.md`. Nothing errors; the pipeline just stalls or invents |
| `contract.output-mismatch` | A stage's Outputs section and the canonical map disagree on what it produces |
| `contract.table-mismatch` | The pipeline table in `CONTEXT.md` promises a different filename than the contract delivers |
| `contract.do-not-load-conflict` | A path sits in both Inputs and "Do NOT load" — the contract contradicts itself |
| `contract.always-loaded-missing` | A stage forgets to name `operating-principles.md` or `house-view.md` |
| `identity.placeholder` | A run's `CLAUDE.md` still has `<fill>` in it, so every stage runs on a blank identity |
| `identity.empty-promise` | `Run-specific notes by stage` exists but is empty, and four contracts point at it |
| `shared.dangling-reference` | Something points at a `_shared/` file that isn't there |
| `run.stage-missing` / `run.extra-stage` | Method and instance have drifted apart |
| `drift.template` | A live run's contract was edited instead of its template — the fix dies with the run |
| `pipeline.unregistered` | A folder in `_templates/` has no entry under `pipelines` in `checks.json`, or the reverse |
| `pipeline.running-order` | A template stage has no row with a type (`core`/`live`/`optional`) in its `CONTEXT.md` table, or the optional rows disagree with `checks.json`. `work` reads that table, so a missing row is a stage nobody is offered |
| `identity.pipeline-unknown` | A run's `Pipeline:` line names a pipeline that does not exist |
| `identity.upstream-missing` | A run's `Upstream:` path does not resolve. (`identity.upstream-not-run` is the info version: the run exists, its stage has not run yet) |
| `lineage.stale` | A stage output was built on an input that has since changed — a frame edited after options were written, or a release PRD revised after a feature PRD used it. See below |
| `engine.edited` | An engine-owned file (per `engine.manifest`) was changed in an instance — the fix never reaches anyone else, and the next pull would overwrite it. Only runs if `engine.manifest` exists |
| `order.out-of-sequence` | A stage produced output without its declared inputs existing. Legal if deliberate, suspicious otherwise |
| `contract.upstream-not-run` | Informational: an input isn't there yet because its stage hasn't run |

### `legibility` — free, local model, run it after editing any contract

A small local model (Ollama) is pointed at one stage and asked to execute it. We check only the
mechanics:

| Check | What a failure means |
|---|---|
| `legibility.output-missing` | It never wrote the declared file. Read the attached transcript: if it was hunting for inputs, the Inputs paths are unclear |
| `legibility.wrong-path` | It wrote the right filename in the wrong folder — the output path in the contract is ambiguous |
| `legibility.forbidden-read` | It read a stage the contract excludes. The "Do NOT load" line is not landing |
| `legibility.input-not-read` | It couldn't find a named input. Check that relative path resolves from the stage folder as written |
| `legibility.stalled` | Hit the turn cap without finishing |
| `legibility.ok` | Executed cleanly. **Not a quality signal** |

**Every legibility finding is a warning, never a failure.** A small model falling over is ambiguous
evidence — it may be your contract, or it may just be the model. The transcript is attached to each
finding so you can tell which. Treat this tier as a clarity smoke test: *a contract that confuses
Qwen is probably underspecified.*

It does **not** grade the output. The local model is not asked to mark work it just wrote —
self-marking isn't evidence. Grading belongs to the behavioural layer, where a different model ran
the stage.

First run needs one setup step:

```
./eval doctor
```

That probes your Ollama, lists installed models, picks the best available (preferring larger
Qwen2.5 tags), live-tests JSON mode and tool calling, and writes the choice into `checks.json`.
Tool calling is the thing to watch: without it the legibility tier can't work, and smaller tags are
where it tends to break. If the doctor reports no tool call, `ollama pull qwen2.5:14b`.

### `behaviour` — costs tokens, run it when you've changed a contract's substance

Structure tells you the plumbing connects. It cannot tell you whether a contract still makes an
agent *do the work*. This layer runs a stage for real and grades the result.

For each stage under test it builds a throwaway run at `_eval-scratch/` — a fresh copy of
the case's pipeline template with the fixture identity from `fixtures/<pipeline>/run/CLAUDE.md` and
upstream outputs seeded from `fixtures/<pipeline>/seed/`. The stage under test starts with an empty `output/`. Then:

**Mechanics** — scripted, objective, no grader:

- `behaviour.output-missing` — did it write the file its contract promised?
- `behaviour.output-empty` — is that file actually substantive?
- `behaviour.forbidden-read` — did it touch a stage its contract says not to load? The fixture
  deliberately seeds downstream outputs so there is something to illegally peek at.
- `behaviour.input-not-read` — did it read every input it claims to need?

**Judgement** — graded against `rubrics/<pipeline>/<stage>.md`:

- `behaviour.rubric` — one finding per failed criterion, with the grader's evidence quoted and the
  model that judged it named in the detail.
- `behaviour.rubric-ungraded` — a criterion nobody judged, so you know the coverage gap exists
  rather than reading silence as a pass.

Run mechanics alone with `--no-grade`, which is much cheaper and still catches the
contract-compliance failures.

```
./eval behaviour --stage 02_explore --keep      # one stage, leave _eval-scratch to inspect
./eval behaviour --no-grade                     # mechanics only
./eval all --open
```

#### Splitting the grading between models

Rubric criteria are not equally hard to judge. "Is there a named owner?" is a lookup. "Are these
*materially different* bets?" is the whole skill. So each criterion is tagged in the rubric:

```markdown
**V9 — named owner** {local}
**V4 — Now / Next / Later with real dependency**
```

`{local}` means mechanical enough for a small local model — presence, counting, structural
completeness. Untagged means judgement, and goes to the strong model.

| Flag | Behaviour |
|---|---|
| `--grader auto` (default) | Local grades the `{local}` criteria, Claude grades the rest. Cheapest honest option |
| `--grader local` | Local only. Judgement criteria are reported as **ungraded**, not guessed at |
| `--grader claude` | Everything to Claude |

Current split: local takes 18 of the 37 criteria across the four rubrics. Note the shape — local
takes 6 of 9 in `03_converge` (much of it is structural presence) but only 3 of 11 in
`08_vision-horizon`, where nearly every criterion is a judgement about whether something is a
position or a roadmap in a trenchcoat. Move a tag if you disagree with where a criterion sits —
it's just markdown.

Under `--grader auto`, if Ollama is unreachable the local criteria are handed to Claude rather than
dropped, and you get a warning saying so. Nothing goes silently ungraded.

Default stages come from each pipeline's `behaviour_stages` in `checks.json`. For discovery they are
the four from the solo test in `RUNBOOK.md`: `01_frame`, `02_explore`, `03_converge`,
`08_vision-horizon`. The PRD pipelines have none yet: they need a fixture and rubrics first.
`--stage` filters; a case only runs the stages its own pipeline has.

Requires the `claude` CLI on your PATH. Without it you get `report/manual-run-sheet.md` — the same
tests, laid out to work through by hand.

> **The behavioural layer reads the live `_shared/`, not a fixture copy.** That is deliberate: a
> thin `house-view.md` is the most common cause of generic output, and the eval should feel that.
> If your output quality drops, suspect `_shared/house-view.md` before you suspect the folders —
> that is exactly what `RUNBOOK.md` claim H5 predicts.

---

## Lineage — stale outputs

Every output is an edit surface, so inputs change after outputs are written. `./eval` keeps a
ledger (`_eval/lineage.json`) of the hash of each stage output and of every input it was built from:
the same-run upstream outputs its contract names, plus the run's `Upstream:` file when the
contract's Inputs mention it. While an output is unchanged, any input whose hash moves makes it
`lineage.stale`.

- **Clear it** by re-running the stage, editing its output, or — once you have checked it still
  holds — `./eval --accept <run>/<stage>` (or `--accept <run>` for every stage in it).
- **Hashes, not timestamps,** because a git checkout resets timestamps. The one exception is the
  first time `./eval` sees an output: with no history, an input newer than the output is recorded
  as unknown and stays stale until the output changes or is accepted.
- **Commit the ledger** in an instance, so the whole team shares one history. The engine never
  ships one.
- It cannot see changes made before the first `./eval` after a stage ran, beyond that timestamp
  check. Run `./eval` after each stage to keep the history tight.

## PRD digest — is it current?

Making the digest is part of the process (`./digest`, see `_tools/README.md`). The eval only checks
that it matches:

- `prd.digest-missing` — a release run has `prd.md` and no `prd-digest.md`.
- `prd.digest-stale` — `prd.md` changed after the digest was written. The digest's first line holds
  a hash of the PRD it was built from; the check compares hashes, not timestamps.
- `prd.digest-fixture` — `./digest` no longer turns `fixtures/prd-digest/prd.md` into
  `expected-digest.md`. If you changed the parser on purpose, regenerate it with the command the
  finding prints.

Feature stages read the digest beside their `Upstream:` file, so lineage hashes the digest, not the
PRD.

## PRD checks — `./eval prd [run]`

The mechanical half of the Ready bar, checked for free, so a model review spends tokens only on
judgement. It reads each release PRD (`04_prd/output/prd.md`) and feature PRD
(`02_spec/output/feature-prd.md`), or one run's, with the same parser as `./digest`.

| Check | What it catches |
|---|---|
| `prd.question-pointer` | `see Qn` names a question that does not exist (here, or in the parent for a feature PRD) |
| `prd.question-orphan` | A question nothing points to. A sub-item's pointer counts for its parent; feature PRDs count for their release |
| `prd.unresolved-pointer` | `Unresolved` or `Conflicted` with no question ID in the same cell or sentence |
| `prd.br-ref` | A requirement's Ref is empty or names no heading in the same PRD. A trailing row id (`/ 9`) is allowed |
| `prd.br-duplicate` | The same requirement ID twice |
| `prd.vocab` | A requirement prefix or priority, question class or status, screen change or sensitivity outside the house list |
| `prd.authoring-left` | `AUTHORING RULES`, italic instruction lines, `[placeholder]` brackets, `<…>` template example rows |
| `prd.scope-overlap` | An item in both Out of scope and Priorities. Exact match only, so it stays `warn` |
| `prd.inherited-id` | Feature PRD: a requirement ID it names but does not define, missing from the parent's digest |
| `prd.carried-unmatched` | Release PRD: a row carried to a feature that no feature PRD defines (only once feature runs exist) |

**Severity follows the PRD.** Findings are `warn` while the header Status is Draft and `fail` once
it says Ready (`prd_checks.ready_status` in `checks.json`), except `ready_exempt`.

**House values** come from the ` ```prd-rules ` block in `_shared/prd-principles.md` — the block
`./digest` reads — as comma-separated lists: `br.prefixes`, `priority`, `question.class`,
`question.status`, `screen.change`, `sensitivity`. Values match exactly, case included. A missing
key skips that check and is reported once as `prd.vocab-missing` (`info`).

`./eval prd` writes the same report as the other layers. It is not part of plain `./eval`. The
review stages (`release-prd/05_review`, `feature-prd/03_review`) run it first and again after each
change, so the review meeting spends its time on judgement.

---

## Changing what it enforces

Almost everything lives in **`checks.json`**, not in code:

- `pipelines.<name>` — one entry per folder in `_templates/`:
  - `canonical_outputs` — the one true map of stage → output filename. Rename an output here and
    the eval will tell you every contract and table that still uses the old name.
  - `optional_stages` — must match the `optional` rows of the template's running-order table.
  - `terminal_folders`, `behaviour_stages`.
- `default_pipeline` — the pipeline of a run whose `CLAUDE.md` has no `Pipeline:` line.
- `lineage_file` — where the lineage ledger lives (see below).
- `required_sections` — the sections every stage contract must have.
- `placeholder_tokens` — the strings that mean "not filled in yet".
- `severities` — promote or demote any check to `fail` / `warn` / `info`.
- `ignore.check_ids` / `ignore.paths` — record a known, accepted deviation. It still shows in the
  report, greyed out, but stops failing the exit code.
- `local` — Ollama settings: `base_url`, `model`, `grader_model`, `num_ctx`, `max_turns`,
  `timeout`, and the `prefer` list the doctor picks from. `./eval doctor` writes `model` for you.

**Rubrics** are plain markdown in `rubrics/<pipeline>/`. Drop in `rubrics/discovery/05_pressure-test.md` and that stage
becomes gradeable; no code change. Write criteria as numbered, individually falsifiable items with
an explicit fail condition — the grader is told to be strict, and vague criteria produce vague
verdicts.

## Workflow for improving the folders over time

1. `./eval` — know you're starting from green (or from a known set of accepted findings).
2. Change a contract in `_templates/<pipeline>/`.
3. `./eval` — catches anything you broke mechanically. Seconds, free.
4. `./eval legibility --stage <the one you changed>` — did you make it *less executable*? Free, so
   run it as often as you like. This is the loop for iterating on wording.
5. `./eval behaviour --stage <the one you changed>` — did the change do what you intended to the
   thinking? Costs tokens, so run it when you believe you're done, not while you're still editing.
6. Compare against last time. `report/index.html` shows the delta against the previous run and a
   history table; `report/history.jsonl` is the raw series.

Steps 3 and 4 are the fast loop and cost nothing — that's where the iteration happens. Step 5 is
the checkpoint.

Every run appends to `report/history.jsonl`, so the trend survives even though `results.json` and
`index.html` are overwritten. Delete `report/` any time — it regenerates.

## Files

```
_eval/
  README.md          this
  evaluate.py        the engine. Stdlib only, no dependencies
  prd_checks.py      ./eval prd: free checks on PRD content
  local.py           Ollama client, rubric routing, the legibility agent loop
  checks.json        what is enforced. Edit this, not the code
  rubrics/<pipeline>/          one markdown rubric per gradeable stage, criteria tagged {local} or not
  fixtures/<pipeline>/
    run/CLAUDE.md              the fixture run identity — a problem space no live run uses
    seed/<stage>/              pre-made upstream outputs so any stage can be tested in isolation
  fixtures/prd-digest/         a synthetic release PRD and the digest ./digest must make of it
  lineage.json                 instance only: which input versions each output was built from. Commit it
  report/                      generated: index.html, results.json, history.jsonl
```

## Known limits

- Only discovery has a fixture, and it is one problem space. A contract that works for unused ticket credits and fails for
  something structurally different will pass here. Add a second fixture if that starts to bite.
- Rubric grading is a model judgement and will vary run to run. Treat a single rubric failure as a
  prompt to read the output yourself, not as a verdict.
- `drift.template` is a plain line-count diff, not semantic. It tells you a live run was edited; it
  does not tell you whether the edit was good.
- The behavioural layer cannot test claim H6 from `RUNBOOK.md` — whether a *pair* reaches a
  defensible position without you in the room. Nothing scriptable can. Watch a real pair instead.
- The legibility tier confounds two causes. A contract that a local model can't execute may be
  underspecified, or the model may simply be too small. The transcript is there so you can judge;
  don't act on the verdict alone.
- Local rubric verdicts are weaker than they look. A small model grading "is there a named owner?"
  is reliable; the same model on anything requiring taste is not, which is why those criteria are
  untagged. Resist the temptation to tag more of them to save tokens — you'd be buying a cheaper
  number, not a better one.
