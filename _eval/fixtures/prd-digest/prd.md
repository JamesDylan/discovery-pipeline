# Release 2 — Shared Reading Lists

## Document Header

| Field | Value |
| :---- | :---- |
| **PRD Id** | PRD-LIB-002 |
| **Version** | 0.3 |
| **Status** | Draft |
| **Date** | 2026-01-15 |
| **Product Manager** | A. Example |

## Sources

| Versioned Documents | Reference |
| :---- | :---- |
| Design | [Lists design file](https://example.com/design) |
| Platform contract | Unresolved (see Q1) |

### Which source wins

- **User experience:** the design file is the source of truth for screens and copy. Where an older note disagrees, the design wins.
- **Platform behaviour:** the catalogue API contract is the source of truth for what the platform does.

### Terms used in this PRD

- **List** (UI) = **Collection** (domain). Screens say "List". Rules say "Collection".
- **Owner:** the member who created a List. There is exactly one.

## Executive Summary

Members can keep reading lists today, but only for themselves. This release lets a member share a
list with other members of the same branch.

## Goals & Objectives

### Primary Metrics

| Metric | Measurement | Target | Release |
| :---- | :---- | :---- | :---- |
| KR1: % of active members who share at least one List | Share events per member over 30 days. | **8%** | Release 2 |

### Measure-only (no target)

| Metric | Measurement | Why it is tracked | Release |
| :---- | :---- | :---- | :---- |
| Lists page visits | Page-view analytics. | Splits KR1 into found and used. | Release 2 |

### Counter Metrics — must not get worse

| Metric | Measurement | Constraint | Release |
| :---- | :---- | :---- | :---- |
| CM1: Support contacts about Lists | Tagged contacts per week. | No more than 10% relative increase. | Release 2 |

## Experience Scope

### Access Summary

| Actor | Allowed | Not allowed | Notes |
| :---- | :---- | :---- | :---- |
| Member | Create, rename and delete their own Lists. Share a List with a member of the same branch. | Edit a List someone else owns. | |
| Librarian | Same as Member. Hide a shared List that breaks the rules. | Delete a member's List. | Moderation only. |

## User Journeys

### Feature PRDs

| Id | Feature PRD | Journeys | Screens | Own Open Questions |
| :---- | :---- | :---- | :---- | :---- |
| F1 | [My Lists](features/F1.md) | Create and open a List | Lists page | Q3 |
| F2 | [Share a List](features/F2.md) | Share a List with a member | Share dialog | None |

### Screen inventory

| Screen name | Purpose | Change in this phase | Primary actor(s) | Figma frame | Priority | Feature |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Lists page | Shows the member's Lists and the Lists shared with them | New | Member | [Lists](https://example.com/design#lists) | P0 | F1 |
| Share dialog | Picks members to share a List with | New | Member | [Share](https://example.com/design#share) | P0. Mobile P1. | F2 |

## The Business View

### Business rules

These must always be true.

1. **A Collection has exactly one Owner.** Ownership never moves in this release.
2. **A Collection is shared only within one branch.** A member of another branch never sees it,
   even through a direct link.
3. **Sharing gives read access only**, never edit.

**Rules not yet set.**

| Rule | Status |
| :---- | :---- |
| What a member sees when the Owner deletes a shared List | Withheld. Unresolved (see Q2). |

## Out of scope

- Sharing across branches.

## Open Questions

| # | Question | Class | Owner | Raised on | Needed by | Status | Notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Q1 | Where is the catalogue API contract published? | Absent | B. Example | 2026-01-10 | Before Ready | open | |
| Q2 | What does a member see when the Owner deletes a List shared with them? | Absent | C. Example | 2026-01-10 | F2 build start | pending review | |
| Q3 | Is the Lists page sorted by name or by last change? | Deferred | A. Example | 2026-01-10 | F1 build start | open | |
| Q4 | Can a Librarian share a List on a member's behalf? | Absent | A. Example | 2026-01-10 | Before Ready | closed | No. |

## Business Requirements

### Group: Access & Authorisation

| BR | Requirement | Priority | Acceptance Criteria | Ref |
| :---- | :---- | :---- | :---- | :---- |
| BR-ACC-01 | Only the Owner can rename or delete a List. The server enforces this. | P0 | API test with a non-owner: every rename and delete returns 403. | Business rules / 1 |
| BR-ACC-02 | A member of another branch cannot open a shared List, even by direct link. | P0 | UI test with a member of another branch: the link shows "not found". | Business rules / 2 |
| BR-ACC-03 | \<requirement\> | P0 | \<instrument\> | Access Summary |

### Group: User Journey & Screens

| BR | Requirement | Priority | Acceptance Criteria | Ref |
| :---- | :---- | :---- | :---- | :---- |
| BR-JRN-01 | *(carried to F1 — release split)* | | | |
| BR-JRN-02 | *(split and carried to F1 and F2 — release split)* | | | |
| BR-JRN-03 | *(new in F2 — release split)* | | | |

## Risks and Concerns

| # | Risk | Mitigation |
| :---- | :---- | :---- |
| R-01 | The catalogue API slips. | Escalate at the weekly review. |
