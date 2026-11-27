#!/usr/bin/env python3
"""Report per-skill usage and context cost from Claude Code session transcripts (~/.claude/projects/**/*.jsonl,
subagent transcripts included). No hooks needed. Prints a markdown table, or with --json the per-call events (ids,
numbers and skill names only, no text), so dumps from several machines can be combined with --events.

A call is `user` when the user typed /skill (a slash command followed by the skill load) or wrote /skill in the prompt
that started the turn. It is `agent` when the model picked the skill through the Skill tool on its own; calls inside
subagent transcripts are always `agent`. `tokens` is the growth in total input tokens (input + cache creation + cache
read) from the assistant message before the skill loaded to the first one after it.
"""
import argparse, hashlib, json, re, statistics, time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMAND = re.compile(r"<command-name>/?([^<]+)</command-name>")
SKILL_LOAD = "Base directory for this skill"
ERROR_WINDOW = 5  # tool calls after the skill whose errors count against it


def short(name: str) -> str:
    """Drop a plugin namespace: `plugin:skill` -> `skill`."""
    return name.rsplit(":", 1)[-1].strip()


def total_input(usage: dict) -> int:
    return sum(usage.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))


def prompt_text(content) -> str | None:
    """Text of a user message, None when it carries tool results."""
    if isinstance(content, str):
        return content
    blocks = [c for c in content or [] if isinstance(c, dict)]
    if any(c.get("type") == "tool_result" for c in blocks):
        return None
    return " ".join(c.get("text", "") for c in blocks)


def scan(path: Path, project: str, since: str) -> list[dict]:
    """Return the skill-call events of one transcript file, streamed line by line."""
    events, watching, watched, skill_calls = [], [], defaultdict(list), {}
    last = (None, None)  # (message id, total input) of the latest assistant message
    prompt, command, subagent = "", None, path.parent.name == "subagents"

    def add(d: dict, skill: str, source: str, model):
        ev = {"session": d.get("sessionId"), "timestamp": d.get("timestamp"), "skill": skill, "source": source,
              "model": model, "project": project, "tokens": None, "errors": 0,
              "_before": last[1], "_trigger": last[0], "_after": None, "_seen": 0}
        events.append(ev)
        watching.append(ev)
        return ev

    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"type":"assistant"' in line:
                d = json.loads(line)
                msg = d.get("message") or {}
                if d.get("type") != "assistant" or not msg.get("usage") or msg.get("model") == "<synthetic>":
                    continue
                if msg.get("id") != last[0]:
                    last = (msg.get("id"), total_input(msg["usage"]))
                    for ev in watching:
                        if ev["_after"] is None and ev["_trigger"] != last[0]:
                            ev["_after"], ev["model"] = last[1], ev["model"] or msg.get("model")
                for c in msg.get("content") or []:
                    if not isinstance(c, dict) or c.get("type") != "tool_use":
                        continue
                    for ev in watching:
                        if ev["_trigger"] != last[0] and ev["_seen"] < ERROR_WINDOW:
                            ev["_seen"] += 1
                            watched[c.get("id")].append(ev)
                    if c.get("name") == "Skill" and d.get("timestamp", "") >= since:
                        skill = short(str((c.get("input") or {}).get("skill", "")))
                        typed = not subagent and re.search(rf"(?<![\w/])/([\w-]+:)?{re.escape(skill)}(?![\w-])", prompt)
                        skill_calls[c.get("id")] = add(d, skill, "user" if typed else "agent", msg.get("model"))
                watching = [ev for ev in watching if ev["_after"] is None or ev["_seen"] < ERROR_WINDOW]
                continue
            # User lines: only command, skill-load, error and prompt lines matter; skip plain tool results unparsed.
            if '"type":"user"' not in line or ("tool_result" in line and '"is_error":true' not in line):
                continue
            d = json.loads(line)
            if d.get("type") != "user":
                continue
            content = (d.get("message") or {}).get("content")
            for c in content if isinstance(content, list) else ():
                if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("is_error"):
                    if c.get("tool_use_id") in skill_calls:
                        skill_calls[c["tool_use_id"]]["failed"] = True
                    for ev in watched.get(c.get("tool_use_id"), ()):
                        ev["errors"] += 1
            text = prompt_text(content)
            if text is None:
                continue
            if d.get("isMeta"):
                if command and SKILL_LOAD in text and not d.get("sourceToolUseID") and d.get("timestamp", "") >= since:
                    add(d, command, "user", None)
                    command = None
                continue
            m = COMMAND.search(text)
            command, prompt = (short(m.group(1)) if m else None), text
    for ev in events:
        before, after = ev.pop("_before"), ev.pop("_after")
        if before is not None and after is not None:
            ev["tokens"] = after - before
        del ev["_trigger"], ev["_seen"]
    return [ev for ev in events if not ev.pop("failed", False)]


def read_transcripts(root: Path, since: str) -> list[dict]:
    cutoff = datetime.fromisoformat(since).replace(tzinfo=timezone.utc).timestamp() if since else 0
    events = []
    for project_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        project = hashlib.sha256(project_dir.name.encode()).hexdigest()[:12]
        for path in sorted(project_dir.glob("*.jsonl")) + sorted(project_dir.glob("*/subagents/*.jsonl")):
            if path.stat().st_mtime >= cutoff:
                events += scan(path, project, since)
    return events


def median(values: list) -> str:
    values = [v for v in values if v is not None]
    return f"{statistics.median(values):,.0f}" if values else "-"


def report(events: list[dict]) -> None:
    by_skill, session_skills = defaultdict(list), defaultdict(set)
    for ev in events:
        by_skill[ev["skill"]].append(ev)
        session_skills[ev["session"]].add(ev["skill"])
    print("| skill | calls | user | agent | sessions | projects | days | retained | ctx tokens (median) "
          "| errors/call | co-used with | models |")
    print("|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|---|")
    for skill, evs in sorted(by_skill.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        sessions = {e["session"] for e in evs}
        days = {e["timestamp"][:10] for e in evs}
        co = Counter(s for sid in sessions for s in session_skills[sid] if s != skill)
        user = sum(e["source"] == "user" for e in evs)
        print(f"| {skill} | {len(evs)} | {user} | {len(evs) - user} | {len(sessions)} "
              f"| {len({e['project'] for e in evs})} | {len(days)} | {'yes' if len(days) >= 3 else 'no'} "
              f"| {median([e['tokens'] for e in evs])} | {sum(e['errors'] for e in evs) / len(evs):.2f} "
              f"| {', '.join(s for s, _ in co.most_common(3)) or '-'} "
              f"| {', '.join(sorted({e['model'] for e in evs if e['model']})) or '-'} |")
    ours = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
    never = [s for s in ours if s not in by_skill]
    print(f"\nNever triggered ({len(never)} of {len(ours)} skills in skills/): {', '.join(never) or 'none'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--days", type=int, default=28, help="window in days, 0 for all history (default 28)")
    ap.add_argument("--root", type=Path, default=Path.home() / ".claude" / "projects", help="transcript folder")
    ap.add_argument("--json", action="store_true", help="dump per-call events instead of the table")
    ap.add_argument("--events", nargs="+", type=Path, metavar="FILE", help="aggregate --json dumps, skip transcripts")
    args = ap.parse_args()
    since = ((datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%Y-%m-%dT%H:%M:%S")
             if args.days else "")
    start = time.monotonic()
    if args.events:
        events = [e for f in args.events for e in json.loads(f.read_text()) if e["timestamp"] >= since]
    else:
        events = read_transcripts(args.root, since)
    # Resumed sessions and overlapping dumps repeat the same call; count it once.
    events = list({(e["session"], e["timestamp"], e["skill"]): e for e in events}.values())
    if args.json:
        print(json.dumps(events, indent=1))
        return
    report(events)
    print(f"\n{len(events)} calls, {len({e['session'] for e in events})} sessions, "
          f"window {args.days or 'all'} days, {time.monotonic() - start:.1f}s")


if __name__ == "__main__":
    main()
