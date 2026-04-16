# Workbench Backlog

> Proposed skills, templates, and knowledge additions. Build order is suggested, not binding.

## Enterprise Gap Pack (BA/BSA/PO workflows)

### Build next

1. **`/requirements-extract`** (S) — Meeting transcript or email thread -> structured requirements doc using `templates/requirements.md`.
   - Note: auto-flag PIPEDA/OSFI relevance when content mentions data handling, client info, or compliance
   - Chains: after input capture -> `/story-split` or `/create-prd`
2. **`/story-split`** (S) — Epic or coarse story -> INVEST-compliant user stories with DoR/DoD applied from `knowledge/standards/`.
   - Note: integrate with `/acceptance-criteria` (below) for per-story ACs
   - Depends on: `knowledge/standards/` populated with INVEST + DoR + DoD references
3. **`/stakeholder-map`** (S) — On new project, auto-offer to create `context/stakeholders/{project}.md`. Already wired as a steering rule; this promotes it to a first-class skill with intake prompts and a default template.
4. **`/meeting-to-actions`** (S) — Transcript -> action items with owners + due dates via `templates/meeting-notes.md`. Appends a one-line entry to `context/sprint-log/{project}.md`.
5. **`/risk-register`** (M) — Reads project docs + ADRs -> enterprise risk register entry (likelihood x impact + mitigation). Output format: bank-standard risk register row.
6. **`/regulatory-impact`** (M) — **BLOCKED** until `knowledge/regulatory/` is populated. When unblocked: OSFI/PIPEDA/SOX update -> scoped impact analysis + NFR inserts into the affected PRD.

### Embedded (not standalone)

7. **Glossary auto-append** -- Sub-step inside `/learning-capture`: after the lesson is written, scan it for terms/acronyms/system names not in `context/glossary.md` and propose additions. No standalone `/glossary-audit` skill.

## Agile / Jira Gap Pack

### Build next (top-5 demo set)

1. **`/jira-story-draft`** (M) — Problem statement + context -> Jira-ready story (summary, description, acceptance criteria, DoR check). Uses `templates/requirements.md` as upstream if available. Highest-value BA/PO daily skill.
2. **`/acceptance-criteria`** (S) — Story -> Gherkin / Given-When-Then acceptance criteria with edge cases, error paths, non-functional NFRs. Integrates with `/jira-story-draft`.
3. **`/refinement-prep`** (S) — Upcoming sprint backlog -> stories needing refinement + what's missing (ACs, estimates, dependencies). Pre-grooming prep.
4. **`/standup-brief`** (S) — Yesterday / today / blockers formatted with work-item links and PR / ticket status. Daily ritual skill.
5. **`/retro-facilitator`** (M) — Sprint data -> retro prompts (Start/Stop/Continue, 4Ls, Mad/Sad/Glad). Pairs with `/synthesize-signals` for cross-sprint pattern detection.

### Backlog (next /extract-harness run)

6. **`/sprint-planning`** (M) — Backlog + historical velocity -> proposed sprint commitment with capacity math.
7. **`/release-notes`** (S) — Commits / tickets since last tag -> stakeholder-readable changelog.
8. **`/definition-of-ready`** (S) — Apply DoR checklist to a ticket, flag gaps, propose fixes. On-demand gate.
9. **`/incident-postmortem`** (M) — Incident -> blameless postmortem using ADR-style format (timeline, contributing factors, action items).
10. **`/ba-elicitation-prep`** (S) — Stakeholder interview prep -- role-specific question bank from `context/stakeholders/{project}.md`.
11. **`/velocity-forecast`** (S) — Historical velocity -> completion forecast with confidence band. Quarterly planning.
12. **`/epic-breakdown`** (M) — Epic -> story tree (distinct from `/story-split` which handles story -> tasks).

## Knowledge gaps (deferred — do not auto-extract)

- `knowledge/banking/` — would be useful but must be sourced from TD-approved internal material, not extracted from a personal repo
- `knowledge/standards/review-checklists.md` — code / PRD / architecture review templates; author from scratch when first needed

## Notes on sizing

- **S** -- small, < 2 hours to build (single-file SKILL.md, one template, minimal branching)
- **M** -- medium, half-day (multi-step flow, existing template integration, moderate testing)
- **L** -- large, multi-session (new template(s), cross-skill integration, validation data)
