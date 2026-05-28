# PRD — Do-Not-Send Pre-Retrieval Data-Classification Gate (Backlog A.1)

**Project:** do-not-send-gate
**Author:** Eric Pacheco (drafted via Claude Code, AI-assisted)
**Date:** 2026-05-27
**Status:** Draft
**Version:** 1.0
**Source:** `docs/backlog.md` → "Enterprise context layer" pack, item A.1. Gating prerequisite for the read-only Confluence/Jira/Outlook adapters (B.3–B.5).

---

## OVERVIEW

A deterministic, pure-Python checkpoint that scans content at the boundary where it would enter the Claude model context, and blocks Do-Not-Send data (SIN, PAN, credentials, JWTs, secrets) before it leaves the bank laptop. Every read-only retrieval adapter routes its output through this gate; nothing reaches the model context unscanned. This is the single control that converts "pull bank data into an LLM session" from a SOX/PCI/PIPEDA egress finding into a governed, audited operation.

## PROBLEM AND GOALS

**Problem:** The shipped BA/agile skills consume pasted text. Wiring live Confluence/Jira/Outlook (backlog B.3–B.5) means tool output flows into the model context — which is egress to an external LLM provider. On a SOX/PCI-aware bank laptop, sending a SIN, full PAN, or a system credential outbound is a reportable finding. There is currently no enforced control between a retrieval source and the context window.

**Goals:**
1. Detect Do-Not-Send patterns deterministically (no model judgment in the detection path).
2. Default-deny: a match blocks the content from reaching the model context.
3. Produce an immutable audit trail of every decision, recording the pattern *class* and disposition — never the matched value.
4. Run entirely on the locked-down laptop: Python stdlib only, zero network calls.

## NON-GOALS

- Not a network DLP appliance; scope is the Claude Code session boundary only.
- Does not classify business sensitivity tiers (public/internal/confidential) — only hard Do-Not-Send patterns in v1.
- Does not build the adapters themselves (B.3–B.5) — it is their prerequisite.
- Does not govern write-back to Jira/Confluence/Outlook (separate SOX change-control item, deferred gap #15).
- User-pasted input is out of scope; it remains the behavioral rule in Compliance Pack #1 (`CLAUDE.md`). This gate covers the retrieval-adapter path only.
- Tamper-resistant / cryptographic audit storage is a v2 concern; v1 writes a plain append-mode log.

## USERS AND PERSONAS

- **Primary — the bank-laptop operator (Eric / BA-PO):** runs Claude Code interactively; needs retrieval to "just work" while staying inside compliance.
- **Secondary — Risk/Compliance reviewer:** consumes the audit trail to attest no Do-Not-Send data left the endpoint.

## USER JOURNEYS OR SCENARIOS

1. **Clean pull:** Operator pulls a Jira ticket with no sensitive data → gate passes it unchanged → content enters context → audit log records `PASS`.
2. **Blocked pull:** Operator pulls a Confluence page containing a client SIN → gate blocks it → operator sees a redaction/refusal notice, not the SIN → audit log records `BLOCK class=SIN` with no raw value.
3. **Backstop:** A future adapter forgets to call the scrubber library → the session hook still scans its output → unscanned content cannot reach context.
4. **Fault:** The gate raises an exception mid-scan → it fails closed (blocks) → audit log records `BLOCK class=GATE_ERROR`.

## FUNCTIONAL REQUIREMENTS

### FR-01: Deterministic classifier — Must
**As a** compliance-bound operator **I want** Do-Not-Send patterns detected by deterministic rules **so that** detection never depends on model judgment.
- Detects: Canadian SIN (with check-digit validation), PAN / credit-card numbers (Luhn-valid), API-key/token shapes, JWTs, and secret/credential assignments (`password=`, `api_key=`, etc.).
- Client-identifier patterns are configurable via a local rules file.

### FR-02: Enforcement at the retrieval boundary — Must
**As an** operator **I want** every retrieval adapter's output to pass through the gate before it enters context **so that** raw sensitive data is never sent to the LLM.
- On match, the default disposition is **block**; redaction is an opt-in policy mode, not the default.
- Architectural constraint: no retrieval-adapter output reaches model context without first passing the gate (enforced by the library contract plus the FR-04 backstop hook).

### FR-03: Audit trail — Must
**As a** Risk reviewer **I want** an append-only log of every gate decision **so that** I can attest to outbound-data controls.
- Each entry: timestamp, source tool/adapter, matched pattern *class*, disposition. Never the matched value.

### FR-04: Backstop session hook — Should
**As an** operator **I want** a Claude Code hook that scans retrieval-adapter output independently of the library **so that** an adapter that forgets to call the scrubber still cannot leak.

### FR-05: Offline, stdlib-only — Must
**As a** locked-down-laptop user **I want** the gate to run on Python stdlib with no network **so that** it installs and runs under bank endpoint restrictions.

## NON-FUNCTIONAL REQUIREMENTS

| Category | Requirement | Metric |
|----------|-------------|--------|
| Security | Default-deny on match; fail-closed on error | No raw match value ever passed downstream |
| Compliance | Aligns to PIPEDA / OSFI B-13 / SOX outbound-data control | Audit trail demonstrates control |
| Performance | Scan adds negligible latency to a retrieval call | < 200 ms for a 50 KB document |
| Auditability | Append-only log, retained | Retention period — see OQ-2 |
| Portability | Python stdlib only, zero network | No third-party import, no socket open |

## ACCEPTANCE CRITERIA

> ISC format: `- [ ] criterion | Verify: method`. Tags: [E]xplicit / [I]nferred / [R]everse-engineered · [M]easurable / [A]rchitectural.

- [ ] SIN, Luhn-valid PAN, API-key, JWT, and secret-assignment patterns are detected in arbitrary input text [E][M] | Verify: Test (positive-fixture corpus, 100% caught)
- [ ] A document containing no Do-Not-Send patterns passes through byte-for-byte unchanged [E][M] | Verify: Test (negative fixtures)
- [ ] On any pattern match the default disposition blocks the content from reaching model context [E][A] | Verify: Test
- [ ] The audit log records the pattern class and disposition but never the matched secret value [E][M] | Verify: Grep (audit fixtures contain class names and zero raw secrets)
- [ ] The gate imports only the Python standard library [E][A] | Verify: Review (import statements)
- [ ] The gate opens no network socket during a scan [E][A] | Verify: Test (no-socket assertion)
- [ ] When the gate raises an exception it fails closed and blocks rather than passing content [E][M] | Verify: Test (injected fault)
- [ ] The gate never transmits scanned content to any external service [E][A] | Verify: Review

**ISC Quality Gate: PASS (6/6)** — Count 8 (≤8) · Conciseness one sentence each, no compound criteria · State-not-action · Binary-testable · Anti-criteria present (rows 4, 7, 8; row 6 no-socket is a safety bound) · Verify method on every row. The retrieval-boundary enforcement criterion folded into FR-02 as an architectural constraint.

## SUCCESS METRICS

- 100% of seeded Do-Not-Send fixtures blocked; 0 false-negatives in the test corpus.
- 0 raw sensitive values present in the audit log across the fixture run.
- Adapters B.3–B.5 are unblocked to build against a passing gate.

## OUT OF SCOPE

- Business-sensitivity tiering, network DLP, write-back governance, and any adapter implementation.

## DEPENDENCIES AND INTEGRATIONS

- **Blocks:** backlog B.3 (Confluence), B.4 (Jira), B.5 (Outlook) adapters.
- **Relates to:** Compliance Pack #1 (PII Do-Not-Send rule — this PRD operationalizes it as enforced code), #5 `pipeda-basics.md` (knowledge dependency for client-identifier rules), `knowledge/regulatory/OSFI-E23-summary.md`.
- **Gate before BUILD:** run `/architecture-review` before the first code-emitting step — this control sits on a trust boundary on a regulated machine.

## RISKS AND ASSUMPTIONS

**Risks:**
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Regex false-negative leaks a novel PII shape | Med | High | Default-deny + backstop hook + extensible rules file; treat misses as P1 |
| Operator disables the gate to reduce friction | Low | High | Fail-closed default; audit log shows gaps; no documented bypass flag |
| Over-blocking creates workflow friction | Med | Med | Redaction policy mode + tunable client-identifier rules |

**Assumptions:**
- Claude Code on the TD laptop supports PostToolUse-style hooks for the backstop (FR-04). If not, FR-04 degrades to a library-only contract — flag at architecture-review.
- Retrieval adapters are the only sanctioned path for external content into context.

## OPEN QUESTIONS

| # | Question | Owner | Due | Status |
|---|----------|-------|-----|--------|
| 1 | Block-only vs block-with-redaction as the shipped default? | Eric / Compliance | Before BUILD | Open (default: block-only) |
| 2 | Audit-log retention period and storage location on the endpoint? | Eric / Risk | Before BUILD | Open |
| 3 | Does the TD-laptop Claude Code build support output-scanning hooks (FR-04)? | Eric | At architecture-review | Open |
| 4 | Which client-identifier patterns are in scope for v1 (account #, member ID)? | Eric / SME | Before BUILD | Open |

---

*Status is Draft. Do not mark Approved without explicit owner confirmation. Next: `/architecture-review` → resolve OQs → `/implement-prd`. AI-assisted, human-reviewed.*
