#!/usr/bin/env python3
"""Log friction with a skill or tool as one JSON line, and group the logged papercuts for triage.

  papercut.py log --ref cpr --kind skill --signature no-ci-checks --blocked false --tried ... --ran ... \
      --expected ... --happened ... --instead ... --fix ... [--agent claude-code] [--model ...]
  papercut.py triage [--since YYYY-MM]

Records go to ~/.claude/papercuts/YYYY-MM.jsonl, or to $PAPERCUT_DIR when it is set.
"""
import argparse, json, os, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ("tried", "ran", "expected", "happened", "instead", "fix")
KINDS = ("skill", "tool", "env", "docs", "input")


def log_dir() -> Path:
    return Path(os.environ.get("PAPERCUT_DIR") or "~/.claude/papercuts").expanduser()


def log(a) -> int:
    now = datetime.now(timezone.utc)
    rec = {"ts": now.isoformat(timespec="seconds"), "repo": Path.cwd().name, "ref": a.ref, "kind": a.kind,
           "signature": a.signature, "blocked": a.blocked == "true", **{f: getattr(a, f) for f in FIELDS},
           "agent": a.agent, "model": a.model}
    line = json.dumps(rec, ensure_ascii=False) + "\n"
    path = log_dir() / f"{now:%Y-%m}.jsonl"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(fd, line.encode())  # one O_APPEND write per record, so concurrent sessions don't interleave
        finally:
            os.close(fd)
    except OSError as e:
        print(f"could not write {path}: {e}\nsave this line by hand:\n{line}", end="", file=sys.stderr)
        return 1
    print(f"logged to {path}")
    return 0


def triage(a) -> int:
    groups = defaultdict(list)
    for f in sorted(log_dir().glob("*.jsonl")):
        if a.since and f.stem < a.since:
            continue
        for n, raw in enumerate(f.read_text().splitlines(), 1):
            try:
                rec = json.loads(raw)
                groups[(rec["ref"], rec["signature"])].append(rec)
            except (ValueError, KeyError, TypeError):
                print(f"skipped {f.name}:{n}: not a papercut record", file=sys.stderr)
    if not groups:
        print(f"no papercuts in {log_dir()}" + (f" since {a.since}" if a.since else ""))
        return 0
    ranked = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for i, ((ref, sig), recs) in enumerate(ranked, 1):
        last = max(recs, key=lambda r: r.get("ts", ""))
        blocked = sum(1 for r in recs if r.get("blocked"))
        repos = ", ".join(sorted({r.get("repo", "?") for r in recs}))
        print(f"## {i}. {ref} / {sig}: {len(recs)}x, blocked {blocked}, last {last.get('ts', '?')}, kind "
              f"{last.get('kind', '?')}, repos: {repos}")
        for f in FIELDS:
            print(f"  {f}: {last.get(f, '')}")
        print()
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    lg = sub.add_parser("log", help="append one papercut record")
    lg.add_argument("--ref", required=True, help="skill or tool that caused the friction")
    lg.add_argument("--kind", required=True, choices=KINDS)
    lg.add_argument("--signature", required=True, help="short stable kebab-case slug for this problem")
    lg.add_argument("--blocked", required=True, choices=("true", "false"))
    for f in FIELDS:
        lg.add_argument(f"--{f}", required=True)
    lg.add_argument("--agent", default="", help="claude-code, codex, cursor, ...")
    lg.add_argument("--model", default="")
    tr = sub.add_parser("triage", help="group logged papercuts, most frequent first")
    tr.add_argument("--since", help="first month to include, YYYY-MM")
    a = p.parse_args()
    return log(a) if a.cmd == "log" else triage(a)


if __name__ == "__main__":
    sys.exit(main())
