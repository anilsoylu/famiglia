#!/usr/bin/env python3
"""Report each skill's context cost in words: its description (in context every session) and its SKILL.md body (loaded
when the skill runs). Vendored skills (vendor.json) are listed but kept out of the maintained totals.
"""
import importlib.util, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_refs", ROOT / "scripts" / "check-refs.py")
check_refs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_refs)


def main() -> None:
    vendored = {n for s in json.loads((ROOT / "vendor.json").read_text())["sources"] for n in s["skills"]}
    rows = []
    for sk in sorted((ROOT / "skills").glob("*/SKILL.md")):
        desc = check_refs.frontmatter(sk).get("description", "").lstrip(">-| ")
        body = re.sub(r"^---\n.*?\n---\n", "", sk.read_text(), count=1, flags=re.S)
        rows.append((sk.parent.name, len(desc.split()), len(body.split()), sk.parent.name in vendored))
    print(f"{'skill':16} {'desc':>5} {'body':>6}")
    for name, d, b, v in rows:
        print(f"{name:16} {d:5} {b:6}{'  (vendored)' if v else ''}")
    own = [r for r in rows if not r[3]]
    print(f"{'maintained':16} {sum(r[1] for r in own):5} {sum(r[2] for r in own):6}")
    print(f"{'all':16} {sum(r[1] for r in rows):5} {sum(r[2] for r in rows):6}")


if __name__ == "__main__":
    main()
