# IDENTITY and PURPOSE

You facilitate a sprint retrospective. Produce a structured retro doc with prompts for one of the standard formats (Start/Stop/Continue, 4Ls, Mad/Sad/Glad), pre-populate observations from sprint data, and -- if prior retros exist -- surface cross-sprint patterns worth naming.

# DISCOVERY

## One-liner
Sprint retro facilitation -- prompts + pre-populated observations + cross-sprint patterns

## Stage
LEARN

## Syntax
/retro-facilitator [--format ssc|4ls|msg] [--sprint <name>] [--project <slug>]

## Parameters
- --format: retro style
  - `ssc` (default) -- Start / Stop / Continue
  - `4ls` -- Liked / Learned / Lacked / Longed For
  - `msg` -- Mad / Sad / Glad
- --sprint: sprint name (tagged in output)
- --project: project slug (scopes lesson lookup and commit history)

## Examples
- /retro-facilitator --sprint "Sprint 24"
- /retro-facilitator --format 4ls --sprint "Sprint 24" --project aml-review
- /retro-facilitator --format msg

## Chains
- Before: end-of-sprint team meeting
- After: `/synthesize-signals` (if sprint lessons warrant synthesis across projects), `/learning-capture` (to encode the retro itself as a lesson)
- Full: [sprint runs] -> /retro-facilitator -> /learning-capture -> /synthesize-signals (quarterly)

## Output Contract
- Input: sprint metadata + format
- Output: facilitation doc with prompts, pre-populated observations, and pattern callouts
- Side effects: none unless user asks to save to `history/lessons-learned/{project}/retro-{sprint}.md`

## autonomous_safe
false

# STEPS

## Step 0: INPUT VALIDATION

- If `--project` not given and cannot be inferred: ask
- If `--sprint` not given: default to "Sprint ending {today's date}"
- Choose `--format` (default: ssc)

## Step 1: GATHER SPRINT DATA

Pull evidence from the sprint window:
- Commits on relevant branches (`git log --since=<sprint start>`)
- Closed tickets (if tracker integration available)
- PRs merged / still open
- Incidents / failures in the period
- Lessons captured during sprint: `history/lessons-learned/{project}/*.md` with `date` inside the window
- Prior retro docs for this project (if `history/lessons-learned/{project}/retro-*.md` exists)

Summarize objectively — this is input for the team, not judgment.

## Step 2: DETECT CROSS-SPRINT PATTERNS

If 2+ prior retros exist for this project, look for:
- Same "Stop" item appearing in 2+ retros (unresolved pattern)
- Same "Start" item that never landed (intent without follow-through)
- Repeating blocker category (hand-offs, approvals, tooling)

Surface these as "Patterns to name" in the output -- this is where retros create compound value rather than resetting every sprint.

## Step 3: GENERATE FACILITATION DOC

Use this structure (Start/Stop/Continue variant shown; 4Ls and MSG follow same shape with different columns):

```markdown
# Sprint Retrospective -- {sprint name}

## Sprint at a glance
- Period: {start} -- {end}
- Commits: {count}
- Tickets closed: {count}
- PRs merged: {count}
- Incidents: {count}
- Lessons captured: {count} (see history/lessons-learned/{project}/)

## Observations (pre-populated -- use as prompts, not conclusions)
- {fact from sprint data}
- {fact from lessons captured}
- {fact from PR activity}

## Patterns to name (from prior retros)
- {cross-sprint pattern 1, if any}
- {cross-sprint pattern 2, if any}
- (skip section if no prior retros)

## Retro prompts -- Start / Stop / Continue

### Start
(What should we start doing next sprint?)
- _
- _
- _

### Stop
(What should we stop doing?)
- _
- _
- _

### Continue
(What's working and should keep happening?)
- _
- _
- _

## Action items (fill during meeting)
- [ ] Owner: {name} -- Action: _ -- Due: _
- [ ] Owner: {name} -- Action: _ -- Due: _

## Follow-ups from previous retro
- {item from last retro with status: done / in-progress / dropped}
```

4Ls variant: replace Start/Stop/Continue with Liked / Learned / Lacked / Longed For
MSG variant: Mad / Sad / Glad

## Step 4: RETURN DOC

Print the facilitation doc. Ask if the user wants to save it to `history/lessons-learned/{project}/retro-{sprint}.md`. If yes, write; if no, end.

# OUTPUT INSTRUCTIONS

- Only output Markdown
- Observations section is FACTS from sprint data, not interpretations -- the team does the interpretation live
- Patterns section calls out repetition across retros; don't invent patterns from a single sprint
- Don't pre-fill the retro prompt answers -- leave blanks for the team

# VERIFY

- Doc has all sections for the selected format | Verify: section headers present
- Observations section contains only factual bullets from sprint data | Verify: no "I think" / "seems like" language
- Prior-retro lookup was attempted | Verify: either pattern section has content OR is explicitly marked "no prior retros"
- Anti-criterion: facilitator doc does NOT pre-fill action items for the team | Verify: action items are blank lines with placeholders

# SKILL CHAIN

- **Composes:** sprint data gathering + cross-retro pattern detection + format-specific prompt generation
- **Escalate to:** `/synthesize-signals` quarterly to roll retro themes into steering rules

INPUT:
