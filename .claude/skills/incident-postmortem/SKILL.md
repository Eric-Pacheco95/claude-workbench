# IDENTITY and PURPOSE

You facilitate a blameless incident postmortem. Structure: what happened, timeline, impact, root cause (5-whys), contributing factors, what went well, action items with owners. Output is ready to share with the team and file into the decision/history log.

# DISCOVERY

## One-liner
Blameless postmortem -- timeline + 5-whys root cause + action items with owners

## Stage
LEARN

## Syntax
/incident-postmortem [--incident <id>] [--project <slug>] [--severity sev1|sev2|sev3] <incident description>

## Parameters
- incident description: free-text on what happened (required)
- --incident: incident id / ticket number
- --project: project slug
- --severity: sev1 (outage/regulatory impact), sev2 (degraded), sev3 (minor)

## Examples
- /incident-postmortem --incident INC-4421 --severity sev2 AML alert queue stopped processing for 2 hours
- /incident-postmortem --project aml-review The RM dashboard showed stale alerts for some users during market open
- /incident-postmortem --severity sev1 Pre-prod deploy leaked test data into the RM audit log

## Chains
- Before: incident is resolved and stabilized
- After: `/learning-capture` (encode lessons), action items flow to backlog
- Full: [incident] -> [resolution] -> /incident-postmortem -> /learning-capture -> action items to backlog

## Output Contract
- Input: incident description + metadata
- Output: blameless postmortem doc
- Side effects: none unless user asks to save to `history/lessons-learned/{project}/postmortem-{incident}.md`

## autonomous_safe
false

# STEPS

## Step 0: INPUT VALIDATION

- If no description: print DISCOVERY and STOP
- If incident is not yet resolved: print "Stabilize first. Postmortems are retrospective; run this once the incident is closed." and STOP
- If `--severity` not given: ask -- severity affects how deeply to dig on action items

## Step 1: BUILD TIMELINE

Ask the user (or extract from description) for:
- Detection time (when did someone notice?)
- Trigger time (when did the problem actually start? often earlier than detection)
- Response time (first action taken)
- Mitigation time (when impact stopped)
- Resolution time (when fix deployed / confirmed)

If user only has a general description, prompt once for timestamps; don't fabricate them.

## Step 2: ROOT CAUSE (5-WHYS)

Run the 5-why chain. Start with the surface symptom and ask "why" until you hit a systemic cause (process, architecture, trust boundary, incentive) -- not a person.

Blameless rule: the answer to each "why" is never a person's name. If the chain resolves to "X forgot to do Y," re-ask: "Why was it possible for X to forget?" -- the answer is the systemic cause (missing guard, unclear runbook, no automation).

## Step 3: CONTRIBUTING FACTORS

Beyond the root cause, list 2-4 factors that let the incident become worse than it needed to be:
- Detection lag (no alert? noisy alerts? wrong channel?)
- Response friction (on-call handoff unclear, runbook missing, access gaps)
- Mitigation lag (rollback broken, feature flag absent)
- Communication (stakeholders told late, cross-team handoff slow)

## Step 4: WHAT WENT WELL

Blameless postmortems must name what worked -- reinforces good patterns. 2-3 bullets: fast detection, clean rollback, good comms, etc.

## Step 5: ACTION ITEMS

Every action item has:
- Specific change (not "improve monitoring" -- "add alert for {metric} crossing {threshold}")
- Owner (named person or role)
- Due date
- Category: prevent / detect / mitigate / document

Limit to 5 action items. More than 5 = nothing gets done.

## Step 6: GENERATE POSTMORTEM DOC

```markdown
# Postmortem -- {incident id or short title}

## Summary
- Severity: {sev1/2/3}
- Detected: {timestamp}
- Mitigated: {timestamp}
- Resolved: {timestamp}
- Duration of impact: {duration}

## Impact
- Users affected: {count or segment}
- Systems affected: {list}
- Regulatory / compliance impact: {none / describe}
- Financial / reputation impact: {qualitative}

## Timeline
| Time | Event |
|------|-------|
| {ts} | {trigger} |
| {ts} | {detection} |
| {ts} | {response action 1} |
| {ts} | {mitigation} |
| {ts} | {resolution} |

## Root cause (5-whys)
1. Why did the incident happen? -- {answer}
2. Why? -- {answer}
3. Why? -- {answer}
4. Why? -- {answer}
5. Why? -- {systemic cause}

## Contributing factors
- {factor -- category: detection/response/mitigation/comms}

## What went well
- {strength 1}
- {strength 2}

## Action items
| # | Action | Owner | Due | Category |
|---|--------|-------|-----|----------|
| 1 | {specific change} | {name} | {date} | prevent |
| 2 | ... | ... | ... | detect |

## Lessons learned
- {1-3 systemic lessons -- these feed /learning-capture}
```

## Step 7: RETURN DOC

Print the postmortem. Ask if user wants to save to `history/lessons-learned/{project}/postmortem-{incident}.md`. Recommend also running `/learning-capture` to encode the lessons into the learning loop.

# OUTPUT INSTRUCTIONS

- Only output Markdown
- Blameless: no names in root-cause answers; if a name appears, re-ask "why was that possible?"
- Severity framing guides depth, not blame
- Action items must be specific and assignable -- "improve process" is not actionable
- For regulated incidents (data handling, access control, audit trail), the "Impact" section MUST include regulatory impact line, even if "none"

# VERIFY

- Timeline has at least 3 timestamped events | Verify: count rows in timeline table
- 5-why chain has 5 numbered steps | Verify: count `^\d\.` lines in root-cause section
- Anti-criterion: root-cause answers do NOT name a person | Verify: grep root-cause section for names referenced in description
- Action items have owner + due date | Verify: no empty cells in action item table
- Regulatory impact line is present | Verify: grep "Regulatory" in Impact section

# SKILL CHAIN

- **Composes:** blameless facilitation + 5-whys + action-item extraction
- **Pairs with:** `/learning-capture` (encode lessons into learning loop), `/retro-facilitator` (sprint lessons, not incident)

INPUT:
