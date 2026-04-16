#!/usr/bin/env python3
"""PII pre-commit guard for claude-workbench.

Hard-blocks commits containing staged content that matches sensitive patterns.
Scans only files under history/lessons-learned/ and history/synthesis/ — the
directories where free-form capture content lives. Other paths are ignored
to avoid false positives in generated docs, tests, etc.

Exit codes:
    0 - clean, commit allowed
    1 - match found, commit blocked
    2 - invocation error (bad args, git not available)

Override:
    Run with --force to skip scanning (use only for confirmed false positives,
    or prepend `GIT_PII_FORCE=1` to the commit command). The override is logged
    to tools/pre-commit/.override.log for audit.

Usage:
    tools/pre-commit/pii-guard.py               # scans git-staged files
    tools/pre-commit/pii-guard.py <file> ...    # scans explicit files
    tools/pre-commit/pii-guard.py --force       # bypass, logged to .override.log
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OVERRIDE_LOG = Path(__file__).resolve().parent / ".override.log"

SCANNED_PREFIXES = (
    "history/lessons-learned/",
    "history/synthesis/",
)

PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "Canadian SIN (9-digit)",
        re.compile(r"\b\d{3}[- ]?\d{3}[- ]?\d{3}\b"),
        "Looks like a Canadian SIN. Replace with a synthetic placeholder.",
    ),
    (
        "Credit card PAN (13-19 digit)",
        re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        "Looks like a credit card PAN. Remove or replace with a placeholder.",
    ),
    (
        "OpenAI-style API key (sk-...)",
        re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
        "Looks like an API key. Rotate the real key immediately and remove from the commit.",
    ),
    (
        "Slack token (xox[baprs]-)",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}\b"),
        "Looks like a Slack token. Rotate and remove from the commit.",
    ),
    (
        "JWT",
        re.compile(r"\beyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b"),
        "Looks like a JWT. If real, revoke; remove from the commit.",
    ),
    (
        "AWS access key (AKIA.../ASIA...)",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
        "Looks like an AWS access key. Rotate immediately and remove.",
    ),
    (
        "Generic high-entropy secret",
        re.compile(r"\b[A-Za-z0-9+/=_\-]{40,}\b"),
        "High-entropy string detected. If this is a secret, remove and rotate; if it's a hash/id, consider shortening or placeholder.",
    ),
    (
        "Private key material",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
        "Private key detected. Remove and rotate the key.",
    ),
]

# Known TD-internal system codes — extend per team convention.
# Matching these doesn't prove sensitivity but warrants author review.
INTERNAL_SYSTEM_CODES = re.compile(
    r"\b(?:KRONOS|MUREX|CALYPSO|QUANTUM|RECON|CTAS|PEGA|NICE|OFSAA)\b",
    re.IGNORECASE,
)


def git_staged_files() -> list[Path]:
    """Return list of staged files in the relevant prefixes."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=REPO_ROOT,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"pii-guard: git unavailable ({e})", file=sys.stderr)
        sys.exit(2)
    files: list[Path] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if any(line.startswith(p) for p in SCANNED_PREFIXES):
            files.append(REPO_ROOT / line)
    return files


def scan_file(path: Path) -> list[tuple[int, str, str, str]]:
    """Return list of (line_no, pattern_name, snippet, advice) for matches."""
    hits: list[tuple[int, str, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:
        print(f"pii-guard: cannot read {path}: {e}", file=sys.stderr)
        return []
    for i, line in enumerate(lines, start=1):
        for name, rx, advice in PATTERNS:
            m = rx.search(line)
            if m:
                # Luhn-style sanity filter for PAN to reduce false positives
                if name.startswith("Credit card") and not _luhn_digits(m.group(0)):
                    continue
                snippet = line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:157] + "..."
                hits.append((i, name, snippet, advice))
        if INTERNAL_SYSTEM_CODES.search(line):
            hits.append(
                (
                    i,
                    "Internal system code",
                    line.strip()[:160],
                    "Internal system name detected. Confirm no confidential context and consider abstracting before commit.",
                )
            )
    return hits


def _luhn_digits(s: str) -> bool:
    digits = [int(c) for c in re.sub(r"\D", "", s)]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def log_override(reason: str) -> None:
    OVERRIDE_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    user = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
    OVERRIDE_LOG.open("a", encoding="utf-8").write(f"{ts}\t{user}\t{reason}\n")


def main(argv: list[str]) -> int:
    if os.environ.get("GIT_PII_FORCE") == "1" or "--force" in argv:
        log_override(reason=" ".join(argv) or "env:GIT_PII_FORCE")
        print("pii-guard: OVERRIDE in effect -- scan skipped (logged)", file=sys.stderr)
        return 0

    explicit = [Path(a) for a in argv[1:] if not a.startswith("--")]
    files = explicit if explicit else git_staged_files()

    if not files:
        return 0

    total_hits = 0
    for f in files:
        if not f.exists():
            continue
        hits = scan_file(f)
        if hits:
            total_hits += len(hits)
            rel = f.relative_to(REPO_ROOT) if f.is_absolute() else f
            for line_no, name, snippet, advice in hits:
                print(f"[BLOCKED] {rel}:{line_no}  {name}", file=sys.stderr)
                print(f"           {snippet}", file=sys.stderr)
                print(f"           -> {advice}", file=sys.stderr)

    if total_hits:
        print(
            f"\npii-guard: {total_hits} match(es) found -- commit blocked.\n"
            "Revise the content or run with --force (logged to .override.log) if this is a confirmed false positive.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
