# 00_intake — gather the sources

One job: list every source this release rests on, and confirm each one can be reached. No opinions
on the problem yet.

## Inputs
- Reference (every run): `../../_shared/operating-principles.md`
- Reference (every run): `../../_shared/house-view.md`
- Reference: `../../_shared/product-context.md`
- Working: `../CLAUDE.md` — run identity, and the file its `Upstream:` line names, if any
- **Do NOT load:** any other stage folder of this run.

## Process
1. Read the `Upstream:` file, if there is one. Note which of its sections this release depends on.
2. Ask what else exists: research, analytics, tickets, prior PRDs, designs, meeting notes, named
   experts. One question at a time.
3. For each source, test access, not content. Note its date and owner.
4. Mark each gap: **blocking** (the PRD cannot be credible without it) · **degrading** · **ignore**.

## Outputs
- `sources.md` → `output/` — sources with location, date, owner and access status; gaps by severity

## Human check
Point at the one source you would trust most if two disagreed. If it is not on the list, the list is
not finished.
