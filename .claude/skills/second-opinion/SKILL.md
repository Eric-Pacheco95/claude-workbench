# IDENTITY and PURPOSE

You generate a self-contained review prompt that an EXTERNAL agent (Codex, GPT, Gemini, another Claude session, a human reviewer) can paste into its session to perform an independent audit of a target repo. This skill does not perform the audit — it produces the brief. The output is a single markdown file ready to hand off.

The prompt is harness-first: every potential wall (missing secrets, external APIs, Windows-only code, MCP servers, the `claude` CLI itself) becomes an instruction to BUILD a stub/mock/fake rather than skip. "Could not verify" is not an acceptable outcome.

# DISCOVERY

## One-liner
Generate a self-contained external-reviewer prompt for independent repo audit

## Stage
PLAN

## Syntax
/second-opinion [--static | --dynamic] [--target <path-or-url>] [--out <path>] [--reviewer <name>]

## Parameters
- `--static` — read-only variant (no execution, no harnesses, ~1 hour budget)
- `--dynamic` — full harness + runtime checks variant (default, 4+ hour budget)
- `--target <path-or-url>` — repo to review (default: current working repo)
- `--out <path>` — output prompt file (default: `./REVIEW_PROMPT.md`)
- `--reviewer <name>` — reviewer identifier woven into intro (default: `Codex`)

## Examples
- `/second-opinion` — full dynamic Codex prompt for current repo at ./REVIEW_PROMPT.md
- `/second-opinion --static` — read-only static-scan variant
- `/second-opinion --reviewer "GPT-5" --out docs/review-prompts/gpt5_review.md`
- `/second-opinion --target https://github.com/org/repo --dynamic`
- `/second-opinion --static --target https://github.com/org/aml-api` — static review of an AML service

## Chains
- Before: team wants an independent perspective on a codebase before a major release or regulatory review
- After: paste the file into the external agent; on return, optionally `/learning-capture` the findings
- Composes: pairs with `/deep-audit` (internal audit) as the external counterpart

## Output Contract
- Input: flags + target
- Output: single markdown file at `--out` path, self-contained, ready to paste
- Side effects: one file written; no code changes

## autonomous_safe
true

# STEPS

1. Parse flags. Resolve `--target` (default: current repo name from `git rev-parse --show-toplevel`). Resolve `--out` (default: `./REVIEW_PROMPT.md`). Resolve `--reviewer` (default: `Codex`).
2. Confirm mode: `--dynamic` unless `--static` specified.
3. Read the embedded TEMPLATE block below matching the mode.
4. Substitute placeholders: `{REVIEWER}`, `{TARGET}`, `{DATE}` (today's date YYYY-MM-DD), `{REPO_HINT}` (target repo name for the header).
5. Write the substituted template to `--out`. Create parent dirs if needed.
6. Print to chat: output path + a 3-line summary of what was generated (mode, reviewer, target) + the one-line invocation to paste ("Paste the contents of <path> into your <reviewer> session").
7. Note the blind spots the external reviewer will have (Windows-only paths, real MCP servers, real API behavior, gitignored dirs) so expectations are set correctly.

# OUTPUT FORMAT

Chat response after writing the file:

```
Wrote: <out_path>
Mode: <static|dynamic> | Reviewer: <name> | Target: <repo>

Paste the contents of <out_path> into your <reviewer> session and run it.

Blind spots the reviewer will have (set expectations):
- Windows-specific code paths (only statically verifiable / simulated)
- Real MCP servers and external integrations
- Real API behavior for any third-party services
- Anything in gitignored dirs (memory/, history/, data/, secrets/)
```

# INPUT

INPUT:

# VERIFY

- Output file exists at `--out` path and is non-empty | Verify: `ls --out` exits 0 and file size > 0
- All template placeholders ({REVIEWER}, {TARGET}, {DATE}, {REPO_HINT}) are substituted | Verify: `grep '{' <output-file>` returns zero hits inside the prompt body
- Output file is NOT written inside a gitignored path (unless explicitly requested) | Verify: `git check-ignore <--out path>` returns no match
- Mode section matches flag: dynamic → contains 'Phase 3 — Dynamic' and H1-H8 playbook; static → does NOT contain those strings | Verify: `grep 'Phase 3' <output>` for dynamic; absence for static

# LEARN

- Do not auto-write a signal for this skill — it is a prompt-generation utility, not an audit itself
- If the external reviewer's findings are returned, route to `/learning-capture` with rating based on finding severity

---

# TEMPLATE: DYNAMIC

```markdown
You are doing an independent deep audit of "{REPO_HINT}" (target: `{TARGET}`). I want a harsh second opinion with runtime evidence, not static skimming. You have a 4+ hour budget and sufficient cloud compute. Depth over speed.

## Prime directive

**There are no walls. Every blocker becomes a harness task.** If a script needs a secret, stub it. If it needs a CLI tool, write a fake shim on PATH that returns fixtures. If it needs an MCP server, spawn a stdio mock. If it needs Windows, monkey-patch the stdlib. If it needs a directory that isn't in the repo, fabricate it from schema inferred by reading the writer. If a dep is missing from `requirements.txt`, install it from the import statements. If something can't be executed directly, simulate it. "Could not verify" is not an acceptable outcome — every finding must have runtime evidence or a documented reason the harness itself is the problem.

Budget up to 45 minutes per blocker on harness construction before downgrading a check to static-only. Log every harness built in the final report so it can be reused.

## Execution authorization

ALLOWED:
- Clone, checkout scratch branches (no push)
- Create and activate a venv; install any Python package needed
- Install system packages via apt if available
- Build fake CLIs, fake MCP servers, fake API endpoints (localhost HTTP, stdio fake, file-based fixtures)
- Monkey-patch stdlib (`time.time`, `os.name`, `sys.platform`, `pathlib`, `subprocess`) to simulate Windows, slow clocks, failure modes
- Write freely inside `_review_scratch/` (create it, gitignore it, never commit it)
- Fabricate synthetic data trees — infer schema from writer code, populate with realistic dummy data
- Create a synthetic `.env` with fake values for every variable referenced in code
- Run any script under `tools/`, `tests/`, `security/`
- Run every test suite you find
- Use `vulture`, `ruff`, `pyflakes`, `mypy`, `bandit`, `pip-audit`, `semgrep` — install whichever help

FORBIDDEN:
- Modify any tracked file in the working tree (scratch dir is fine)
- `git push`, `git commit`, touching any remote
- Calls to real external services with real credentials. Use fakes.
- Writing to real data dirs — redirect via env vars or monkey-patching

## Harness construction playbook (build BEFORE dynamic checks)

**H1 — Fake CLI shims.** For any CLI tool the repo invokes (identified by grepping subprocess calls), create `_review_scratch/bin/<tool>` (chmod +x), prepend to PATH. Accept relevant flags, return fixture responses. Log every call to `_review_scratch/cli_calls.jsonl`.

**H2 — Synthetic `.env`.** Grep every `os.environ`/`os.getenv`/`dotenv` lookup. Build `_review_scratch/.env` with obviously-fake values (`sk-FAKE-...`, `xoxb-FAKE-...`) for each.

**H3 — Fake MCP servers.** For each MCP server in `.claude/settings.json` / `.mcp.json`: write a minimal stdio fake that speaks MCP JSON-RPC, lists advertised tools, returns canned responses.

**H4 — Fake HTTP sinks.** Stand up local FastAPI / `http.server` on `127.0.0.1:<port>` matching external API endpoints. Redirect via env base URLs. Log to `_review_scratch/http_calls.jsonl`.

**H5 — Synthetic data trees.** For every path under `memory/`/`history/`/`data/`/`docs/`: infer schema, create at `_review_scratch/fake_<name>/`, populate with 10-50 realistic synthetic records. Redirect reads via monkey-patch or env.

**H6 — Windows simulator.** `_review_scratch/windows_shim.py` that monkey-patches: `time.time` to 15ms granularity; `sys.platform='win32'`; `os.name='nt'`; `sys.stdout.encoding='cp1252'`. Run target scripts via this shim.

**H7 — Hook invoker.** `_review_scratch/invoke_hook.py` — takes hook name + synthetic tool_use payload, looks up matcher in `settings.json`, runs the hook with correct env/stdin, reports exit + stdout + side effects.

**H8 — Dependency resolver.** AST-scan all `.py` imports, diff against `requirements*.txt` + stdlib, pip-install the gap until clean.

## Phase 1 — Orientation (~20 min)

1. `CLAUDE.md` at repo root — identity, workflow rules, quality gates, steering rules. Every rule reflects a team decision or past incident; treat as invariants the codebase SHOULD uphold.
2. `README.md` — understand project goals, scope, and team context.
3. `docs/projects/` — scan for active project context.
4. `ls .claude/skills/` — verify any skill count claimed in CLAUDE.md.
5. `.claude/settings.json`, `.mcp.json` if present.
6. `security/constitutional-rules.md`, `ls security/validators/` if present.
7. `git log --oneline -100`, `git shortlog -sn`, `git log --stat -30`.
8. Map entry points: main application, background jobs, API handlers, scheduled tasks.

## Phase 2 — Harness build (~30-45 min)

Execute H1-H8. End state: `_review_scratch/` can run any script without hitting a real external service.

## Phase 3 — Static scan (~45 min)

Draft findings in these buckets. Phase 4 will confirm with runtime evidence.

**A. Doc/reality drift** — claimed skills/paths/tasks that don't match reality; stale counts/dates; claimed "complete" work not actually wired.

**B. Steering rule violations** (highest signal — paid-for lessons):
- Anti-criterion no-ops (grep -v / awk filter-and-print verifiers that exit 0 on violation)
- `time.time()` uniqueness assumptions (Windows 15ms tick)
- Orphaned file copies after relocation
- CLI consumers not checking for rate-limit / error strings on exit 0
- MCP wildcard allow-lists on servers with mutation tools
- Hook matchers not covering their validators
- Non-ASCII in Python print paths (cp1252 hazard)
- Parallel test suites duplicating instead of extending
- `git add -f`, `--no-verify`, bypassed gitignore
- `subprocess(..., shell=True)` with interpolation
- Naive `datetime.now()` for durable timestamps

**C. Security** — `git ls-files memory/ history/` (should be empty); secret grep; validator TOCTOU/traversal/injection; path guards that can be bypassed.

**D. Dead code** — scripts/skills with zero inbound references, targets that don't exist, old TODOs.

**E. Architectural smells** — skill/module cycles, god-files >800 lines, duplicated logic, unlocked read-modify-write on shared files.

**F. Correctness** — bare excepts, swallowed exceptions, schema drift writer/reader pairs, off-by-ones, unchecked None.

## Phase 4 — Dynamic checks (~2.5+ hours, the core)

**4.1 Run every test suite.** `pytest -xvs tests/` + each script's `__main__` self-test. Record pass/fail/error/flaky. Root-cause every failure in 1-2 sentences.

**4.2 Validator fuzzing.** Every script in `security/validators/` (if present): 30+ adversarial inputs (path traversal, shell metachars, null bytes, unicode homoglyphs, JSON bombs, symlinks, oversized, empty, malformed). Use H7 to verify hook matchers actually route each validator.

**4.3 Anti-criterion verifier audit.** Every verifier script and every `Verify:` command in PRDs/CLAUDE.md/skills: construct synthetic forbidden-state input, run verifier, **assert exit != 0**. Exit 0 on forbidden state = CRITICAL.

**4.4 Windows-clock simulation.** Using H6: run any id-generator 2000× rapid succession. Count collisions. Repeat with two parallel processes.

**4.5 Concurrent-write stress.** Every shared JSON/JSONL with >1 writer: 4 writers × 500 iterations parallel. Assert no corruption / lost updates / interleaved records.

**4.6 Hook simulation.** Every hook in `settings.json`: synthetic matching tool call via H7, verify exit + stdout + side effects.

**4.7 Import graph + dead code.** Full graph across `tools/`, `.claude/skills/`. Run `vulture`. Report unreachable modules/functions and cycles.

**4.8 Schema drift.** Every JSON/JSONL with writer A + reader B: diff A's write keys vs B's expected keys. Report mismatches.

**4.9 Static analyzers.** `ruff`, `pyflakes`, `mypy --ignore-missing-imports`, `bandit -r .`, `semgrep --config=auto .`. Top 20 by severity from each.

**4.10 Git hygiene.** `git fsck`, blobs >1MB in history, merged-undeleted branches, stale worktrees, `git ls-files` sanity on sensitive dirs.

**4.11 Rate-limit / error handling.** H1 in error-response mode. Every CLI consumer: verify it detects + handles failures. Treating error as success = HIGH finding.

## Phase 5 — Report (~30 min)

Write to `_review_scratch/REVIEW.md`:

```
# {REVIEWER} Deep Audit — {REPO_HINT}
Date: {DATE} | HEAD: <sha> | Wall time: <hh:mm>
Tests ran/passed/failed/errored: <counts>
Harnesses built: <count>

## TL;DR
<5 bullets, severity-ranked>

## Findings

### CRITICAL
- **<title>** — `path:line`
  Static: <snippet>
  Dynamic evidence: <command + output>
  Impact: <1-2 sentences>
  Fix: <concrete>

### HIGH / MEDIUM / LOW
...

## Dynamic check results
<table per 4.1-4.11>

## What's GOOD
<3-5 bullets — prevents over-refactor>

## Meta-observations
<recurring bug classes, architectural patterns causing pain>

## Harnesses built (reusable)
<list each: path + invocation>

## Command log
<full reproducible log>

## STATIC-ONLY findings
<with reason the harness itself failed — should be near-empty>
```

## Ground rules

- **Harnesses, not excuses.** Walls are tasks.
- **Every finding needs file:line + runtime evidence** except rare STATIC-ONLY (with justification).
- **Harsh, no sycophancy.** Call out over-abstraction, speculative helpers, defensive validation on internal boundaries, narrating comments. If something should be deleted, say delete.
- **CLAUDE.md steering rules and Core Principles violations are the top-signal finding class.** Surface loudly.
- **Concrete fixes only.** "Replace X on line 47 with Y because Z" — never "refactor this".
- **4+ hours is expected.** If finishing early, go deeper on 4.2, 4.5, 4.11.

Begin Phase 1 now. Work continuously through Phase 5. One report at the end.
```

---

# TEMPLATE: STATIC

```markdown
You are doing an independent second-opinion review of "{REPO_HINT}" (target: `{TARGET}`). I want fresh eyes — no prior context. Read-only static analysis, ~1 hour budget.

## Orientation (first, in order)

1. `CLAUDE.md` at the repo root — identity, workflow rules, quality gates, steering rules. Every rule was added after a real incident; treat as invariants.
2. `README.md` — project goals and team context.
3. `docs/projects/` — scan for active project context.
4. `ls .claude/skills/` — verify any count claimed in CLAUDE.md.
5. `.claude/settings.json` — hooks, permissions, MCP, validators.
6. `security/constitutional-rules.md`, `ls security/validators/` if present.
7. `git log --oneline -50` and `git log --stat -20`.

Timebox orientation to ~15 min. Sample, don't exhaustively read.

## Scan buckets

Organize findings below. For each, cite `file:line` and quote the snippet.

### A. Doc/reality drift
- Skills claimed that don't exist; paths referenced in rules that don't exist; `[x]` tasks with no artifact; stale counts/dates.

### B. Steering rule violations (highest signal)
- Anti-criterion no-ops (`grep -v`/`awk` verifiers exiting 0 on violation)
- `time.time()` uniqueness without ns + counter (Windows hazard)
- Orphaned file copies after relocation
- CLI exit-0 consumers not checking error strings
- MCP wildcard allow-lists on mutation servers
- Hook matchers not covering their validators
- Non-ASCII in Python print paths (cp1252 hazard)
- Parallel test suites instead of extending

### C. Security
- `git ls-files memory/ history/` (should be empty)
- Secret grep in `.py`/`.json`/`.md`/`.env*`
- Validator TOCTOU, path traversal, shell injection, bypasses
- `subprocess(..., shell=True)` with interpolation
- `git add -f`, `--no-verify`

### D. Dead code
- Scripts with no inbound references; skills not referenced anywhere; old TODOs (date via blame).

### E. Architectural smells
- Circular deps, god-files >800 lines, duplicated logic, unlocked read-modify-write.

### F. Correctness
- Bare excepts, naive `datetime.now()`, schema drift, off-by-ones, unchecked None.

## Output format

Single markdown report:

```
# {REVIEWER} Independent Review — {REPO_HINT}
Date: {DATE}
Scope: <sha of HEAD>

## TL;DR
<5 bullets, severity-ranked>

## Findings

### CRITICAL
- **<title>** — `path:line`
  Evidence: `<snippet>`
  Why it matters: <1-2 sentences>
  Fix: <concrete, not hand-wavy>

### HIGH / MEDIUM / LOW
...

## What's GOOD
<3-5 bullets — prevents over-refactor>

## Meta-observations
<patterns across findings>

## Could not verify
<anything that would need execution — list here for a dynamic follow-up pass>
```

## Ground rules

- **Read-only.** Do not modify any file.
- **Cite evidence.** Every finding needs `file:line` + quoted snippet. Uncited claims ignored.
- **Concrete fixes.** "Refactor this" = useless.
- **Depth > breadth.** 10 real bugs > 50 nits.
- **Harsh, no sycophancy.** Call out over-abstraction, speculative helpers, narrating comments. If something should be deleted, say delete.
- **Steering rule + Core Principle violations are highest-signal.** Surface loudly.

Begin with orientation, then scan, then report.
```
