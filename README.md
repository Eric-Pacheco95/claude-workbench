# Claude Workbench

A structured AI workflow harness for building repeatable, auditable processes with [Claude Code](https://claude.ai/code).

## What Is This?

Claude Workbench gives you a disciplined framework for using Claude Code to create and execute workflows. It provides:

- **The Algorithm**: A 7-phase execution loop (OBSERVE -> THINK -> PLAN -> BUILD -> EXECUTE -> VERIFY -> LEARN) that ensures you think before you build
- **Ideal State Criteria (ISC)**: Binary-testable acceptance criteria with a 6-check quality gate
- **13 Skills**: Reusable workflow patterns that chain together into pipelines
- **Security Rules**: Constitutional rules that prevent secrets exposure, prompt injection, and destructive operations

## Quick Start

1. Clone this repo
2. Open it in Claude Code: `cd claude-workbench && claude`
3. Try a skill: `/delegation I want to build a compliance report generator`

## Skills

| Skill | Stage | What It Does |
|-------|-------|-------------|
| `/research` | OBSERVE | Research any topic (market, technical, live) |
| `/first-principles` | THINK | Break a problem down to bedrock assumptions |
| `/red-team` | THINK | Stress-test a plan for weaknesses and failure modes |
| `/architecture-review` | THINK | Parallel multi-angle analysis (first-principles + fallacies + red-team) |
| `/create-prd` | PLAN | Generate a PRD with ISC criteria |
| `/implement-prd` | BUILD | Execute a PRD end-to-end with verify loops |
| `/review-code` | VERIFY | Security-focused code review |
| `/quality-gate` | VERIFY | Audit completed work for compliance |
| `/commit` | ORCHESTRATE | Clean conventional commits with emoji |
| `/delegation` | ORCHESTRATE | Route any task to the right skill |
| `/workflow-engine` | ORCHESTRATE | Chain skills into automated pipelines |
| `/create-pattern` | BUILD | Create new reusable skills |
| `/improve-prompt` | UTILITY | Rewrite prompts for clarity and reliability |

## Built-in Pipelines

```
Full build:      /research -> /create-prd -> /implement-prd -> /quality-gate
Deep analysis:   /first-principles -> /red-team -> /create-prd
Security review: /red-team --stride -> /review-code
New project:     /research -> /first-principles -> /create-prd -> /implement-prd
```

## Directory Structure

```
claude-workbench/
+-- CLAUDE.md                  # Root context and steering rules
+-- .claude/
|   +-- settings.json          # Claude Code permissions
|   +-- skills/                # 13 skill definitions
+-- security/
|   +-- constitutional-rules.md
+-- docs/                      # PRDs, specs, research briefs
+-- history/
    +-- decisions/             # Decision log with rationale
```

## No Learning, No Autonomous Systems

This harness is intentionally stateless. It does not:
- Store learning signals or synthesis
- Run autonomous background agents
- Maintain persistent memory across sessions
- Track personal identity or goals

It **does**:
- Follow a disciplined workflow algorithm
- Enforce security rules
- Log decisions for audit trails
- Create reusable skill patterns

## Creating New Skills

```
/create-pattern a skill that generates compliance checklists from policy documents
```

This creates a new SKILL.md in `.claude/skills/` that you can invoke by name in future sessions.

## License

Private use.
