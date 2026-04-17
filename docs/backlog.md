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

### Completed -- Phase 3 (2026-04-16, placeholder v1 -- refine after field use)

All 10 skills shipped as working placeholders. They follow the workbench SKILL.md structure and are demo-ready; refine per real usage.

1. **`/jira-story-draft`** -- Problem statement + context -> INVEST story (summary, description, AC stub, NFRs, DoR checklist, metadata)
2. **`/acceptance-criteria`** -- Story -> Gherkin (happy + edge + negative + NFR), or checklist format via `--format`
3. **`/refinement-prep`** -- Batch backlog -> 7-point gap report per story, classified Ready / Needs Work / Split
4. **`/standup-brief`** -- Yesterday / Today / Blockers from git log + tickets + user notes
5. **`/retro-facilitator`** -- Sprint retro facilitation doc (ssc / 4ls / msg) with cross-sprint pattern detection
6. **`/sprint-planning`** -- Backlog + velocity + capacity -> committed + stretch sets with risk register
7. **`/release-notes`** -- Release window -> internal changelog + stakeholder summary; audit notes for regulated changes
8. **`/definition-of-ready`** -- Single-story DoR gate with pass/fail verdict and specific gap list
9. **`/incident-postmortem`** -- Blameless postmortem: timeline, 5-whys, contributing factors, action items
10. **`/ba-elicitation-prep`** -- Elicitation prep: session goal + 8-15 open questions + anticipated friction

### Backlog (next /extract-harness run)

11. **`/velocity-forecast`** (S) -- Historical velocity -> completion forecast with confidence band. Quarterly planning.
12. **`/epic-breakdown`** (M) -- Epic -> story tree (distinct from `/story-split` which handles story -> tasks).

## Knowledge gaps (deferred — do not auto-extract)

- `knowledge/banking/` — would be useful but must be sourced from TD-approved internal material, not extracted from a personal repo
- `knowledge/standards/review-checklists.md` — code / PRD / architecture review templates; author from scratch when first needed

## Notes on sizing

- **S** -- small, < 2 hours to build (single-file SKILL.md, one template, minimal branching)
- **M** -- medium, half-day (multi-step flow, existing template integration, moderate testing)
- **L** -- large, multi-session (new template(s), cross-skill integration, validation data)
