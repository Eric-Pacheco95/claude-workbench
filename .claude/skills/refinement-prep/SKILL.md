# IDENTITY and PURPOSE

You prepare an upcoming sprint backlog for refinement/grooming. For each candidate story, identify what's missing before it can be committed: acceptance criteria, estimates, dependencies, stakeholder approvals, Definition-of-Ready gaps. Output is a facilitator-ready prep doc.

# DISCOVERY

## One-liner
Pre-grooming prep -- flag what's missing on each candidate story before refinement meeting

## Stage
PLAN

## Syntax
/refinement-prep [--sprint <name>] [--project <slug>] <backlog input>

## Parameters
- backlog input: list of story identifiers/titles, path to a backlog export, or free-text paste of candidate stories (required)
- --sprint: sprint name (tagged in output)
- --project: project slug

## Examples
- /refinement-prep --sprint "Sprint 24" --project aml-review [paste backlog]
- /refinement-prep docs/projects/aml-review/backlog-sprint-24.md
- /refinement-prep Stories for next sprint: AML-101 Alert joint-flag, AML-102 Triage queue, AML-103 RM audit trail

## Chains
- Before: team refinement meeting
- After: `/definition-of-ready` (formal DoR gate per story), `/sprint-planning` (commit phase)
- Full: /refinement-prep -> [team refinement meeting] -> /sprint-planning

## Output Contract
- Input: candidate story list
- Output: per-story gap report with Ready / Needs Work / Split classification
- Side effects: none

## autonomous_safe
true

# STEPS

## Step 0: INPUT VALIDATION

- If no input: print DISCOVERY and STOP
- If input has fewer than 2 stories: print "Refinement prep needs at least 2 candidate stories. Add more or run /jira-story-draft for a single story." and STOP
- Read `knowledge/standards/` if available for the team's DoR definition

## Step 1: PARSE BACKLOG

Extract a list of candidate stories. For each: title, any description/ACs present, identifier (if given), estimate (if given), dependencies (if stated).

## Step 2: PER-STORY ASSESSMENT

For each story, run this 7-point check:

| # | Check | Status |
|---|-------|--------|
| 1 | Role / goal / benefit explicit? | pass / fail |
| 2 | At least 2 acceptance criteria with happy + edge/negative? | pass / fail |
| 3 | Dependencies listed (upstream tickets, data, approvals)? | pass / fail |
| 4 | Estimate assigned (story points or t-shirt)? | pass / fail |
| 5 | Regulatory/compliance touch identified (if applicable)? | pass / fail / n/a |
| 6 | Stakeholder named (PO, RM, domain SME for review)? | pass / fail |
| 7 | Fits in a single sprint (if not, propose split)? | fits / too big |

Classify each story:
- **Ready** — all 6 non-n/a checks pass
- **Needs Work** — 1-2 checks fail; note what's missing
- **Split** — check 7 fails OR scope is ambiguous; propose decomposition

## Step 3: GENERATE PREP DOC

```markdown
# Refinement Prep -- {sprint name or date}

## Summary
- Candidate stories: {N}
- Ready: {count}
- Needs Work: {count}
- Split: {count}

## Stories

### [READY] {story identifier} -- {title}
- All DoR criteria met; proceed to sprint-planning commit.

### [NEEDS WORK] {story identifier} -- {title}
- Missing: {bulleted gaps — e.g. "negative-path AC", "no estimate", "RM not named"}
- Suggested question for refinement: {one question the team should answer}

### [SPLIT] {story identifier} -- {title}
- Reason: {too large / scope unclear / mixed concerns}
- Proposed split:
  - {sub-story 1}
  - {sub-story 2}

## Facilitation Notes
- {1-3 bullets on themes across the backlog — e.g. "3 stories touch AML alert routing; sequence them so 101 completes first"}
- {cross-cutting risks worth discussing}
```

## Step 4: RETURN PREP DOC

Print the prep doc. Do not write to disk unless the user asks.

# OUTPUT INSTRUCTIONS

- Only output Markdown
- Lead with the Summary counts; Ready stories first (they're fastest to confirm in the meeting)
- Be specific in "Needs Work" — "needs ACs" is useless; "needs one negative-path AC covering concurrent-RM-edit" is actionable
- Don't fabricate stakeholder names; say "unnamed" and flag as a gap

# VERIFY

- Every candidate story appears in output with a classification | Verify: count stories in output == count in input
- Summary counts match the per-story classifications | Verify: tally sections
- Anti-criterion: output does NOT silently drop a story; any input story that couldn't be parsed is called out explicitly | Verify: look for "unparsed:" or equivalent warning section

# SKILL CHAIN

- **Composes:** backlog parsing + per-story DoR check + split detection
- **Pairs with:** `/definition-of-ready` (per-story deep check), `/sprint-planning` (commit phase)

INPUT:
