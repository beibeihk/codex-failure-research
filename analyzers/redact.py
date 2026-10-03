"""Defense in depth: allowlist collection first, redaction second, review third."""
import os
import re

PATTERNS = [
    (re.compile(r"\b(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})"), "<secret>"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{16,}"), "Bearer <secret>"),
    (re.compile(r"(?i)(\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|client[_-]?secret|cookie)\b\s*[=:]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s,;}<>]+)"), r"\1<secret>"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "<email>"),
    (re.compile(r"(?i)[A-Z]:[\\/]Users[\\/][^\s\"'<>]+"), "<personal-path>"),
    (re.compile(r"(?i)/(?:home|Users)/[^\s\"'<>]+"), "<personal-path>"),
    (re.compile(r"(?i)\b(?:chatgptAccountId|account_id|accountId|user_id)\b\s*[=:]\s*[\"']?[^\s,;}\"']+"), "<account-id>"),
]


def redact(text, personal_literals=()):
    literals = list(personal_literals)
    for name, value in os.environ.items():
        if re.search(r"(?i)(key|token|secret|password|cookie)", name) and len(value) >= 8:
            literals.append(value)
    for literal in sorted(set(literals), key=len, reverse=True):
        if literal:
            text = text.replace(literal, "<redacted>")
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def sensitive_findings(text):
    # Return categories only; never echo a detected credential.
    return [str(index) for index, (pattern, _) in enumerate(PATTERNS) if pattern.search(text)]

