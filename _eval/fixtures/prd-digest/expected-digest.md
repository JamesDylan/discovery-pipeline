<!-- prd-digest of prd.md sha:fc4a1e47419d — written by ./eval digest. Do not edit; edit the PRD and run it again. -->

> Digest of `prd.md`: one line per item. Open a full section of the PRD only when a line here is not enough, and name the section you opened.

# Release 2 — Shared Reading Lists
PRD Id: PRD-LIB-002. Version: 0.3. Status: Draft. Date: 2026-01-15.

## Terms
- List (UI) = Collection (domain).
- Owner: the member who created a List.

## Which source wins
- User experience: the design file is the source of truth for screens and copy.
- Platform behaviour: the catalogue API contract is the source of truth for what the platform does.

## Business rules
1. A Collection has exactly one Owner.
2. A Collection is shared only within one branch.
3. Sharing gives read access only
- Not set: What a member sees when the Owner deletes a shared List. Withheld. Unresolved (see Q2).

## Access
- Member. Allowed: Create, rename and delete their own Lists. Share a List with a member of the same branch. Not allowed: Edit a List someone else owns.
- Librarian. Allowed: Same as Member. Hide a shared List that breaks the rules. Not allowed: Delete a member's List.

## Business requirements
### Access & Authorisation
- BR-ACC-01 P0: Only the Owner can rename or delete a List. The server enforces this.
- BR-ACC-02 P0: A member of another branch cannot open a shared List, even by direct link.
### User Journey & Screens
- BR-JRN-01 → carried to F1
- BR-JRN-02 → split and carried to F1 and F2
- BR-JRN-03 → new in F2

## Open questions
- Q1 open, B. Example: Where is the catalogue API contract published?
- Q2 pending review, C. Example: What does a member see when the Owner deletes a List shared with them?
- Q3 open, A. Example: Is the Lists page sorted by name or by last change?
- Closed, question text omitted: Q4 (closed)

## Screens
- Lists page: F1, P0
- Share dialog: F2, P0. Mobile P1.

## Features
- F1 My Lists. Own questions: Q3
- F2 Share a List. Own questions: None

## Metrics
- KR1: % of active members who share at least one List
- Lists page visits
- CM1: Support contacts about Lists
