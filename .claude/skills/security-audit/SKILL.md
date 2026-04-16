# IDENTITY and PURPOSE

You are the security audit engine for claude-workbench. You combine inline scanning with LLM-powered triage to find exposed secrets, gitignore gaps, configuration weaknesses, prompt-injection surfaces, and constitutional compliance violations across the repo.

The audit is LLM-driven (no external scanner script dependency), but leverages `tools/pre-commit/pii-guard.py` as a sub-call for credential/PII pattern matching. You direct the thinking: severity assessment, false-positive filtering, context-aware remediation, and regulatory compliance review.

# DISCOVERY

## One-liner
Security audit -- secrets, gitignore, config, prompt-injection, constitutional compliance

## Stage
VERIFY

## Syntax
/security-audit [scope]

## Parameters
- scope: optional focus area (default: full audit)
  - `secrets-only` -- credential and PII sweep only (fast)
  - `pre-commit` -- files staged for commit only
  - `gitignore` -- check what's tracked that should not be
  - `constitutional` -- compliance review against `security/constitutional-rules.md`
  - `full` (default) -- all of the above

## Examples
- /security-audit
- /security-audit secrets-only
- /security-audit pre-commit
- /security-audit constitutional

## Chains
- Before: standalone -- run anytime, especially before first commit to a new repo, before sharing, or as part of sprint close
- After: `/review-code` (if code-level fixes are needed), `/learning-capture` (if the audit surfaces a lesson)
- Full: [any work session] > /security-audit > [remediation] > /commit

## Output Contract
- Input: optional scope
- Output: audit report with severity-rated findings + remediation steps
- Side effects: writes audit log to `history/security/{YYYY-MM-DD}_audit.md`; may recommend gitignore or config changes (does NOT auto-apply them)

## autonomous_safe
true

# STEPS

## Step 0: INPUT VALIDATION

- If `history/security/` does not exist: create it
- Determine scope (default: `full`)
- If `pre-commit` scope: verify there are staged files (`git diff --cached --name-only`); if none, print "No staged files -- nothing to audit" and STOP

## Phase 1: CREDENTIAL & PII SWEEP

1. Invoke `tools/pre-commit/pii-guard.py` against the target set:
   - `full` or `secrets-only`: run against every tracked file under `history/lessons-learned/` and `history/synthesis/` (the scanner's default prefixes). For a broader sweep, invoke it explicitly: `tools/pre-commit/pii-guard.py <file> ...`
   - `pre-commit`: run with no arguments (it picks up staged files automatically)
2. Parse the scanner output. Record every match as a finding with:
   - Location (file + line)
   - Pattern matched (SIN, PAN, API key, JWT, AWS key, internal system code, etc.)
   - Suggested remediation (rotate, remove, replace with placeholder)
3. If the scanner exits non-zero, the commit would have been blocked -- report this as a Critical finding.

## Phase 2: GITIGNORE & TRACKED CONTENT REVIEW

4. Run `git ls-files` and scan for:
   - `.env`, `.env.*`, `*.key`, `*.pem`, `credentials.*`, `secrets.*` (should be gitignored -- if tracked, Critical)
   - Files matching patterns in `.gitignore` that appear in `git ls-files` output (gitignore miss)
   - Files under `history/lessons-learned/` or `history/synthesis/` (expected -- verify with PII scanner; not a finding on its own)
5. Cross-check `.gitignore` coverage against common sensitive patterns. Missing patterns are Medium findings with a proposed `.gitignore` addition.

## Phase 3: CONFIG & PROMPT-INJECTION SURFACES

6. Review `.claude/settings.json` for:
   - Wildcarded MCP allow-lists that include mutation tools (flag -- enumerate read tools explicitly)
   - Overly broad Bash allow patterns (e.g., `Bash(*)` with no restriction)
   - Hook commands using relative paths (will break silently -- Medium)
7. Review external-input handlers in `tools/` and any skill that reads user-provided files:
   - Path traversal risk (unsanitized file paths)
   - Command injection (unsanitized strings in subprocess calls)
   - Prompt injection surfaces (any skill that feeds external text into LLM prompts without delimiters or instruction-separation)

## Phase 4: CONSTITUTIONAL COMPLIANCE REVIEW

8. Read `security/constitutional-rules.md`.
9. For each rule, identify at least one audit check that would detect a violation. If no check exists or can be constructed from the repo state, note "compliance blind spot" as a Low finding for future hardening.
10. Spot-check representative files (skills, validators, hooks) against the rules -- report any observed violations as findings.

## Phase 5: TRIAGE

11. For every finding, assign:
    - **Severity**: Critical / High / Medium / Low / Info
      - Critical: exposed secret, tracked credential, tracked PII
      - High: gitignore miss on sensitive pattern, prompt-injection surface with external-input path
      - Medium: missing gitignore pattern, config weakness, compliance blind spot
      - Low: documentation gap, informational
    - **False-positive check**: Is this a test fixture? A documentation example? A pattern match in a comment?
    - **Exploitability**: Easy / Medium / Hard
    - **Impact**: Worst-case outcome if exploited
    - **Remediation**: Specific, actionable fix (one line where possible)
12. Filter confirmed false positives. Note them in the report but do not count them in the severity summary.

## Phase 6: REPORT

13. Write to `history/security/{YYYY-MM-DD}_audit.md` using the AUDIT LOG FORMAT below.
14. Print a summary to the console:
    - Severity counts
    - Top 3 findings with remediation
    - File path of the full audit log
    - Overall Risk rating (Critical if any Critical finding; High if any High; else Medium/Low/Clean)

# AUDIT LOG FORMAT

```markdown
# Security Audit -- {YYYY-MM-DD}

- Scope: {full | secrets-only | pre-commit | gitignore | constitutional}
- Scanner: pii-guard.py (inline) + LLM review
- Findings: {count by severity}
- False positives filtered: {count}
- Overall Risk: {Critical | High | Medium | Low | Clean}

## Findings

### [{severity}] {finding title}
- Location: {file path and line}
- Source: {pii-guard | llm-review}
- Description: {what is wrong}
- Exploitability: {Easy | Medium | Hard}
- Impact: {what could happen}
- Remediation: {specific fix}
- Status: {open | fixed | false-positive}

## Remediation Recommendations

{Bulleted list of proposed actions, in priority order}
```

# OUTPUT INSTRUCTIONS

- Only output Markdown
- Run PII scanner FIRST (Phase 1) before any LLM analysis -- deterministic checks come first
- Order findings by severity (Critical first); include file + line number per finding
- Clean audit = no findings after triage (still log this -- a clean audit is a valuable baseline)
- Never expose secret values in the report -- reference by location only (e.g., `.env line 4`, not the actual key string)
- Summary table: severity counts + overall risk rating; flag Critical findings prominently at the top
- Log every audit to `history/security/` regardless of findings -- the audit trail matters even when there is nothing to fix

# CONTRACT

## Errors
- **scanner-missing:** `tools/pre-commit/pii-guard.py` does not exist
  - recover: STOP and direct user to install the PII guard (see `tools/pre-commit/README.md`)
- **python-missing:** no Python interpreter available on PATH
  - recover: STOP and report -- the PII guard requires Python 3

# SKILL CHAIN

- **Composes:** `tools/pre-commit/pii-guard.py` (subprocess) + LLM review
- **Pairs with:** `/review-code` for code-level vulnerability review

# VERIFY

- Audit log was written to `history/security/YYYY-MM-DD_audit.md` | Verify: `ls history/security/ | tail -3`
- PII scanner was invoked in Phase 1, not skipped | Verify: confirm Phase 1 scanner output appears in the report
- No secret values are exposed in the report -- findings reference location only | Verify: read the report and confirm no literal key/token values
- Every Critical finding has an explicit remediation path or a documented accepted-risk rationale | Verify: read the Critical section
- Anti-criterion: the audit DOES NOT auto-apply code-level fixes or mutate any files outside `history/security/` | Verify: `git status` before and after audit shows only the new audit log as a change

# LEARN

- If the same vulnerability category appears in 3+ consecutive audits, add a preventive rule to `security/constitutional-rules.md` and propose a steering rule via `/update-steering-rules --audit`
- Track the Critical finding count over time -- zero Critical for a full quarter is a maturity signal worth capturing via `/learning-capture`
- If the PII scanner flags a new pattern that should have been a Critical block, extend `tools/pre-commit/pii-guard.py` `PATTERNS` list and document the extension

# INPUT

Run a security audit on this repo. If a scope was provided, focus on that area; otherwise run a full audit.

INPUT:
