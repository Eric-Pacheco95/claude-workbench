# PII Guard

Hard-block pre-commit scanner for claude-workbench. Blocks commits that stage content containing SIN, PAN, API keys, Slack tokens, JWTs, AWS access keys, private keys, high-entropy secrets, or recognized internal system codes.

Scans only files under `history/lessons-learned/` and `history/synthesis/` — the free-form capture surfaces. Other paths are ignored to avoid noise.

## Install

Once per clone:

```bash
git config core.hooksPath .githooks
```

Verify:

```bash
git config --get core.hooksPath   # should print: .githooks
```

## Test

Create a synthetic test file and try to commit:

```bash
echo "fake SIN 123-456-789" > history/lessons-learned/test/2026-04-16_test.md
git add history/lessons-learned/test/2026-04-16_test.md
git commit -m "test"
# should block and print the match
rm history/lessons-learned/test/2026-04-16_test.md
```

## Override (use sparingly)

Only for confirmed false positives. Every override is logged to `tools/pre-commit/.override.log` (gitignored).

```bash
GIT_PII_FORCE=1 git commit -m "..."
```

Or run the scanner directly against arbitrary files:

```bash
tools/pre-commit/pii-guard.py path/to/file.md
```

## Extending patterns

Edit `pii-guard.py` `PATTERNS` and `INTERNAL_SYSTEM_CODES` constants. Keep patterns narrow — false positives erode trust and push users toward `--force`.
