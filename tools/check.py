"""Read-only structure/link checks and limited exposure signals. Not a security audit."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md",
    "templates/AGENTS.md", "templates/RULE_VERSION.md", "templates/profile.md",
    "templates/projects/index.md", "templates/projects/example.md",
    "templates/handoff-template.md", "templates/code-map-template.md",
    "templates/decision-template.md", "docs/agent-setup.md",
    "docs/handoff-walkthrough.md", "docs/limitations.md",
)
SIGNALS = (
    ("private home path", re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")),
    ("Windows home path", re.compile(r"[A-Za-z]:[\\/]Users[\\/][^\s\\/]+", re.I)),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("access credential", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
)


def signals(text):
    return [name for name, pattern in SIGNALS if pattern.search(text)]


def check(root=ROOT):
    errors = []
    for relative in REQUIRED:
        path = root / relative
        if path.is_symlink() or not path.is_file():
            errors.append(f"missing or symlink: {relative}")
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(p in {".git", "__pycache__", "local", "my-agent-home"} for p in relative.parts):
            continue
        if path.is_symlink():
            errors.append(f"symlink: {relative}")
            continue
        if not path.is_file() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(f"{relative}: {name}" for name in signals(text))
        # These maintained documents use simple Markdown links, no embedded HTML.
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if re.match(r"^[a-z]+:", target, re.I) or target.startswith("#"):
                continue
            linked = (path.parent / target.split("#", 1)[0]).resolve()
            if not linked.is_relative_to(root.resolve()) or not linked.exists():
                errors.append(f"{relative}: broken/outside link: {target}")
    return errors


if __name__ == "__main__":
    findings = check()
    for finding in findings:
        print(finding)
    print(f"Template checks: {'FAIL' if findings else 'PASS'} ({len(findings)} findings)")
    sys.exit(bool(findings))
