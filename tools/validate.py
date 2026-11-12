"""Repository checks. Standard library only. Run: python3 -I tools/validate.py

- Every skills/<dir>/SKILL.md has frontmatter with a valid `name` (matching <dir>) and `description`.
- Every skill-relative path mentioned in backticks inside a skill exists.
- No tracked text file contains something that looks like a secret.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PATH_RE = re.compile(r"`((?:references|templates|scripts|examples)/[A-Za-z0-9._/-]+)`")
SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("ElevenLabs-style key", re.compile(r"\bsk_[a-f0-9]{40,}\b")),
    ("assigned API key", re.compile(r"(?i)\b[A-Z0-9_]*API_KEY\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}")),
    ("bearer token", re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{24,}")),
]
TEXT_SUFFIXES = {".md", ".py", ".mjs", ".js", ".json", ".yml", ".yaml", ".txt", ".toml", ".example", ""}
SKIP_DIRS = {".git", ".tools", "node_modules", "__pycache__"}


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fields


def check_skill(skill_dir, errors):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
        return
    fm = frontmatter(skill_md.read_text(encoding="utf-8"))
    rel = skill_md.relative_to(ROOT)
    if fm is None:
        errors.append(f"{rel}: missing YAML frontmatter")
        return
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{rel}: name {name!r} must be lowercase letters/digits/hyphens, max 64 chars")
    if name != skill_dir.name:
        errors.append(f"{rel}: name {name!r} must match folder {skill_dir.name!r}")
    if not desc or len(desc) > 1024:
        errors.append(f"{rel}: description must be 1-1024 chars (got {len(desc)})")
    for md in skill_dir.rglob("*.md"):
        for ref in PATH_RE.findall(md.read_text(encoding="utf-8")):
            if not (skill_dir / ref).exists():
                errors.append(f"{md.relative_to(ROOT)}: referenced path `{ref}` does not exist")


def scan_secrets(errors):
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in TEXT_SUFFIXES or path.name == ".env":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS:
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{path.relative_to(ROOT)}:{line}: possible {label}")
    if (ROOT / ".env").exists():
        print("note: a local .env exists; make sure it stays untracked (it is git-ignored).")


def main():
    errors = []
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if not skills:
        errors.append("no skills found under skills/")
    for skill_dir in skills:
        check_skill(skill_dir, errors)
    scan_secrets(errors)
    for e in errors:
        print("error:", e)
    print(f"checked {len(skills)} skill(s): {'FAILED' if errors else 'ok'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
