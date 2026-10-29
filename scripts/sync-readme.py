#!/usr/bin/env python3
"""Regenerate the skill and credits tables in README.md from each SKILL.md and vendor.json.

  scripts/sync-readme.py          rewrite the blocks between <!-- SKILLS:START/END --> and <!-- CREDITS:START/END -->
  scripts/sync-readme.py --check  exit 1 if README.md is stale or a skill has no group below

A new skill must be added to GROUPS, so the README never lists it under the wrong heading.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUPS = {
    "Code: plan to production": ["dev-flow", "review", "commit-gate", "perf", "optimize", "security-audit", "clean",
                                 "cpr", "pr-update", "pr-ready", "pr-triage", "stacked-pr", "list-open-work"],
    "UI and frontend": ["frontend-design", "ui-ux-pro-max", "ui-only", "ui-system", "visual-verify",
                        "vercel-react-best-practices"],
    "SEO and AI search": ["seo-agency", "seo-audit", "ai-seo", "schema", "programmatic-seo", "site-architecture",
                          "link-building", "competitors", "content-strategy"],
    "Writing": ["no-tropes", "humanizer", "copywriting"],
    "Growth and analytics": ["cro", "analytics", "lead-magnets", "almost-paid"],
}
MAX = 150

sys.path.insert(0, str(ROOT / "scripts"))
frontmatter = __import__("check-refs").frontmatter


def summary(skill: Path) -> str:
    desc = re.sub(r"\s+", " ", frontmatter(skill / "SKILL.md").get("description", "")).strip("\"'>|- ")
    first = re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0]
    return (first if len(first) <= MAX else first[: MAX - 1].rsplit(" ", 1)[0] + "…").replace("|", "\\|")


def source_of(cfg: dict) -> dict:
    out = {}
    for src in cfg["sources"]:
        slug = src["repo"].removeprefix("https://github.com/")
        for name in src["skills"]:
            out[name] = f"[{slug}]({src['repo']})"
    return out


def skills_block(cfg: dict) -> tuple[str, list]:
    have = sorted(p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists())
    grouped = [n for names in GROUPS.values() for n in names]
    problems = [f"{n}: not in GROUPS" for n in have if n not in grouped]
    problems += [f"{n}: in GROUPS but not in skills/" for n in grouped if n not in have]
    src = source_of(cfg)
    lines = []
    for title, names in GROUPS.items():
        lines += [f"### {title}", "", "| Skill | What it does | From |", "|---|---|---|"]
        lines += [f"| [{n}](skills/{n}/) | {summary(ROOT / 'skills' / n)} | {src.get(n, 'famiglia')} |"
                  for n in names if n in have]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", problems


def credits_block(cfg: dict) -> str:
    lines = ["| Source | Skills | License | Pinned at |", "|---|---|---|---|"]
    for src in cfg["sources"]:
        slug = src["repo"].removeprefix("https://github.com/")
        names = ", ".join(f"`{n}`" for n in sorted(src["skills"]))
        lines.append(f"| [{slug}]({src['repo']}) | {names} | {src['license']} | `{src['ref'][:7]}` |")
    return "\n".join(lines) + "\n"


def replace(text: str, tag: str, body: str) -> str:
    pat = re.compile(rf"(<!-- {tag}:START -->\n).*?(<!-- {tag}:END -->)", re.S)
    if not pat.search(text):
        sys.exit(f"README.md has no <!-- {tag}:START --> / <!-- {tag}:END --> block")
    return pat.sub(lambda m: m.group(1) + body + m.group(2), text)


def main() -> int:
    cfg = json.loads((ROOT / "vendor.json").read_text())
    readme = ROOT / "README.md"
    skills, problems = skills_block(cfg)
    new = replace(replace(readme.read_text(), "SKILLS", skills), "CREDITS", credits_block(cfg))
    for p in problems:
        print("FAIL", p)
    if "--check" in sys.argv:
        stale = new != readme.read_text()
        print("README.md is stale: run scripts/sync-readme.py" if stale else "README.md is up to date")
        return 1 if stale or problems else 0
    readme.write_text(new)
    print(f"README.md synced ({len(problems)} problem(s))")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
