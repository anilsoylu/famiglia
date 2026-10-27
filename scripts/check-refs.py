#!/usr/bin/env python3
"""Lint the skills in skills/: frontmatter is valid, and every file a skill's markdown points to exists.

A reference is any `backticked` token ending in .md, .py, .sh, .json or a trailing / . It resolves against the skill dir,
then the skill's references/ dir, then the file's own dir. Vendored skills (vendor.json) only get the frontmatter check.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = re.compile(r"`([\w./-]+\.(?:md|py|sh|json|mjs|cjs)|[\w./-]+/)`")
IGNORE = {"AGENCY.md", "CLIENT.md", "HANDOFF.md", "LEDGER.md", "LINKS.md", "TECH.md", "REPORT.md", "STRATEGY.md",
          "SITE.md", "RULES.md", "CLAUDE.md", "geo.md", "keywords.md", "agency/", "briefs/", "pages/", "data/", "scratch/",
          "artifacts/", "README.md", "SKILL.md", "CONTRIBUTING.md", "AGENTS.md", "CODING_STANDARDS.md", "package.json", "app.json"}


def frontmatter(p: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", p.read_text(), re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\w[\w-]*:", line):
            key, _, val = line.partition(":")
            out[key] = val.strip()
        elif key:
            out[key] += " " + line.strip()
    return out


def main() -> int:
    vendored = {n for s in json.loads((ROOT / "vendor.json").read_text())["sources"] for n in s["skills"]}
    errors = []
    for skill in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        sk = skill / "SKILL.md"
        if not sk.exists():
            errors.append(f"{skill.name}: no SKILL.md"); continue
        fm = frontmatter(sk)
        if fm.get("name") != skill.name:
            errors.append(f"{skill.name}: frontmatter name is {fm.get('name')!r}")
        if len(fm.get("description", "")) < 40:
            errors.append(f"{skill.name}: description missing or too short")
        if skill.name in vendored:
            continue
        for md in skill.rglob("*.md"):
            if "evals" in md.parts:
                continue
            for ref in set(REF.findall(md.read_text())):
                if ref in IGNORE or "<" in ref or ref.startswith(("http", "~", "/", "sources/seo-prompt/", "sources/code-prompt/")) or "YYYY" in ref:
                    continue
                if not any((base / ref).exists() for base in (skill, skill / "references", md.parent)):
                    errors.append(f"{md.relative_to(ROOT)}: missing `{ref}`")
    for e in errors:
        print("FAIL", e)
    print("ok" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
