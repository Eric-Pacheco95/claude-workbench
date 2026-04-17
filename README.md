# Claude Workbench

A structured AI workflow harness for building repeatable, auditable processes with [Claude Code](https://claude.ai/code).

## What Is This?

Claude Workbench gives you a disciplined framework for using Claude Code to create and execute workflows. It provides:

- **The Algorithm**: A 7-phase execution loop (OBSERVE -> THINK -> PLAN -> BUILD -> EXECUTE -> VERIFY -> LEARN) that ensures you think before you build
- **Ideal State Criteria (ISC)**: Binary-testable acceptance criteria with a 6-check quality gate
- **41 Skills**: Reusable workflow patterns that chain together into pipelines
- **Security Rules**: Constitutional rules that prevent secrets exposure, prompt injection, and destructive operations
- **PII Pre-Commit Guard**: Hard-block scanner that prevents SIN, PAN, API keys, JWTs, and other credential patterns from being committed (enable with `git config core.hooksPath .githooks`)

## Quick Start

1. Clone this repo
2. Open it in Claude Code: `cd claude-workbench && claude`
3. Try a skill: `/delegation I want to build a compliance report generator`

## Skills

| Skill | Stage | What It Does |
|-------|-------|-------------|
| `/research` | OBSERVE | Research any topic (market, technical, live) |
| `/absorb` | OBSERVE | Absorb a URL -- dual-lens wisdom + fallacy analysis |
| `/deep-audit` | OBSERVE | Multi-axis codebase audit (architecture, security, errors, domain, testing) |
| `/extract-alpha` | OBSERVE | Extract the highest-signal, most novel ideas from any content |
| `/first-principles` | THINK | Break a problem down to bedrock assumptions |
| `/red-team` | THINK | Stress-test a plan for weaknesses and failure modes |
| `/architecture-review` | THINK | Parallel multi-angle analysis (first-principles + fallacies + red-team) |
| `/find-logical-fallacies` | THINK | Identify reasoning flaws, hidden assumptions, false analogies |
| `/analyze-claims` | THINK | Audit claims, map evidence, rate argument support |
| `/make-prediction` | THINK | Structured multi-outcome predictions with committed probabilities |
| `/create-prd` | PLAN | Generate a PRD with ISC criteria |
| `/project-init` | PLAN | Full ISC project pipeline -- research, stress-test, PRD |
| `/implement-prd` | BUILD | Execute a PRD end-to-end with verify loops |
| `/create-pattern` | BUILD | Create new reusable skills |
| `/create-keynote` | BUILD | Build narrative-driven slide decks with speaker notes |
| `/visualize` | BUILD | Generate Mermaid diagrams from projects, workflows, systems |
| `/write-essay` | BUILD | Write a clear, direct, publish-ready essay |
| `/review-code` | VERIFY | Security-focused code review |
| `/quality-gate` | VERIFY | Audit completed work for compliance |
| `/validation` | VERIFY | Run ISC format gate and verify all criteria |
| `/security-audit` | VERIFY | Secrets, gitignore, config, constitutional compliance scan |
| `/learning-capture` | LEARN | End-of-task lesson capture -- structured, multi-user, PII-safe |
| `/synthesize-signals` | LEARN | Distill accumulated lessons into proposed steering rules |
| `/extract-wisdom` | LEARN | Extract ideas, insights, quotes, habits from any content |
| `/teach` | LEARN | Deep-dive lesson on any topic with worked examples |
| `/update-steering-rules` | LEARN | Propose new or updated CLAUDE.md steering rules |
| `/retro-facilitator` | LEARN | Sprint retro facilitation doc (ssc / 4ls / msg) with cross-sprint patterns |
| `/incident-postmortem` | LEARN | Blameless postmortem -- timeline, 5-whys, action items |
| `/ba-elicitation-prep` | OBSERVE | BA stakeholder elicitation prep -- goal + open questions + friction |
| `/jira-story-draft` | PLAN | Problem statement -> INVEST user story with ACs stub + DoR |
| `/acceptance-criteria` | PLAN | Story -> Gherkin ACs (happy + edge + negative + NFR) |
| `/refinement-prep` | PLAN | Batch backlog -> per-story gap report (Ready/Needs Work/Split) |
| `/sprint-planning` | PLAN | Backlog + velocity + capacity -> committed sprint plan |
| `/definition-of-ready` | VERIFY | Single-story DoR gate -- pass/fail with gap list |
| `/commit` | ORCHESTRATE | Clean conventional commits with emoji |
| `/delegation` | ORCHESTRATE | Route any task to the right skill |
| `/workflow-engine` | ORCHESTRATE | Chain skills into automated pipelines |
| `/backlog` | ORCHESTRATE | Capture task ideas from chat into the project backlog |
| `/standup-brief` | ORCHESTRATE | Daily standup brief -- Yesterday / Today / Blockers |
| `/release-notes` | ORCHESTRATE | Release window -> internal changelog + stakeholder summary |
| `/improve-prompt` | UTILITY | Rewrite prompts for clarity and reliability |

## Built-in Pipelines

```
Full build:         /research -> /create-prd -> /implement-prd -> /quality-gate -> /learning-capture
Deep analysis:      /first-principles -> /find-logical-fallacies -> /red-team -> /create-prd
Security review:    /red-team --stride -> /review-code -> /security-audit
New project:        /project-init -> /implement-prd -> /quality-gate -> /learning-capture
Learning loop:      /learning-capture (per task) -> /synthesize-signals (sprint/quarter) -> /update-steering-rules --audit
Content analysis:   /absorb <url> --deep -> /extract-alpha -> /analyze-claims
Prediction:         /research -> /make-prediction --deep -> /red-team
Presentation:       /research -> /create-keynote --pptx
Story -> sprint:    /jira-story-draft -> /acceptance-criteria -> /definition-of-ready -> /refinement-prep -> /sprint-planning
Sprint operations:  /sprint-planning -> /standup-brief (daily) -> /retro-facilitator -> /release-notes
Incident response:  /incident-postmortem -> /learning-capture -> /synthesize-signals
```

## Directory Structure

```
claude-workbench/
+-- CLAUDE.md                  # Root context and steering rules
+-- .claude/
|   +-- settings.json          # Claude Code permissions
|   +-- skills/                # 41 skill definitions
+-- .githooks/
|   +-- pre-commit             # PII guard hook (install via git config core.hooksPath .githooks)
+-- security/
|   +-- constitutional-rules.md
+-- templates/                 # Artifact templates (requirements, ADR, meeting-notes, status-update)
+-- context/
|   +-- glossary.md            # Terms, acronyms, system names (auto-populated)
|   +-- stakeholders/          # Per-project stakeholder maps
|   +-- sprint-log/            # Lightweight delivery history per project
|   +-- teach/                 # Saved lessons from /teach
+-- knowledge/                 # Domain knowledge by topic
+-- docs/                      # PRDs, specs, research briefs
|   +-- projects/              # Per-project directories
|   +-- absorbed/              # Absorbed URL analyses
|   +-- predictions/           # Prediction records
|   +-- backlog.md             # Task backlog + proposed skills
+-- history/
|   +-- decisions/             # Decision log with rationale (ADR format)
|   +-- lessons-learned/       # Per-task lessons from /learning-capture
|   +-- synthesis/             # Sprint/quarter themes from /synthesize-signals
|   +-- security/              # Audit logs from /security-audit
|   +-- validations/           # ISC validation reports
+-- tools/
|   +-- pre-commit/            # PII guard scanner (pii-guard.py)
```

## Stateless by Design

This harness is intentionally stateless at the infrastructure level. It does not:
- Run autonomous background agents
- Maintain cross-session memory automatically
- Connect to external services by default

It **does**:
- Follow a disciplined workflow algorithm
- Enforce security rules on every action
- Log decisions for audit trails
- Create reusable skill patterns
- Track predictions for future resolution
- Absorb and analyze external content

## Creating New Skills

```
/create-pattern a skill that generates compliance checklists from policy documents
```

This creates a new SKILL.md in `.claude/skills/` that you can invoke by name in future sessions.

## License

Private use.