# history/

Immutable audit trail -- every significant decision, change, and verification is logged here.

## Structure

```
history/
+-- decisions/        # Decision logs with rationale
+-- validations/      # Validation reports from /validation
```

## Decisions

Every significant architectural or workflow decision gets a log entry. Format:

```markdown
# Decision: {title}

- Date: YYYY-MM-DD
- Skill: {skill that triggered this decision, or "manual"}
- Context: {why this decision was needed}

## Options Considered
1. Option A -- pros/cons
2. Option B -- pros/cons

## Decision
{What was decided and why}

## Outcome
{Fill in after the fact: did this work?}
```

## Validations

ISC validation reports from `/validation` are written here automatically as `{YYYY-MM-DD}-{slug}.md`.

## Rules

- Never delete entries -- history is append-only
- Never edit past entries to change outcomes -- add a correction entry instead
- Log all significant decisions, not just code changes