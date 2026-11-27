---
name: papercut
description: >-
  Log a record when a skill or tool gives you friction: a step that doesn't fit the repo, a retry loop, a missing
  fallback, a wrong assumption, a tool error you worked around, then carry on. For "/papercut", "papercut triage".
---

# Papercut

A papercut is friction an agent hit with a skill or tool. Logging it takes one command and turns a failure nobody
noticed into an eval case later. Two modes: **log** (you, mid-task, quick) and **triage** (the user asks for it).

Run the script by its path from the repo you are working in, without changing directory: the record's `repo` field is
the current folder's name. In Claude Code the path is `"${CLAUDE_SKILL_DIR}/scripts/papercut.py"`; elsewhere use
`scripts/papercut.py` inside this skill's folder. Records go to `~/.claude/papercuts/YYYY-MM.jsonl`, one JSON line
each, or to the folder in the `PAPERCUT_DIR` environment variable when it is set.

## Log mode

Use it when a skill or tool got in the way of the task: a skill step that doesn't fit this repo, a command you had to
retry or poll with no progress, a missing fallback, an instruction built on a wrong assumption, a tool error you had to
work around. Don't log the user's own bugs or a failing test the task is meant to fix.

1. Stop the loop first. If you have run the same command three times with no progress, that is the papercut.
2. Log it once:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/papercut.py" log --ref <skill-or-tool> --kind <skill|tool|env|docs|input> \
     --signature <short-stable-slug> --blocked <true|false> \
     --tried "<what I was trying to do>" --ran "<what I ran>" --expected "<what I expected>" \
     --happened "<what happened>" --instead "<what I did instead>" --fix "<what would fix it>" \
     --agent <claude-code|codex|cursor> --model <model id>
   ```

   - `--ref`: the skill or tool at fault (`pr-ready`, `gh`, `docker`), not the repo you work in.
   - `--signature`: a kebab-case slug that names the problem, not this instance (`no-ci-checks`, not
     `pr-7-no-checks`), so repeats group together in triage.
   - `--blocked true` only if you could not finish the task because of it.
   - One or two sentences per field. No prompt text, no file contents, no secrets, no URLs with tokens.
3. Check the output says `logged to <path>`. Then go back to the task and finish it the way you said in `--instead`.

Log once per distinct problem per session. Mention it in one line in your final reply ("logged a papercut for
`pr-ready`: no-ci-checks").

## Triage mode

1. Group the records:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/papercut.py" triage [--since YYYY-MM]
   ```

   It prints one group per (ref, signature), most frequent first: count, blocked count, last seen, repos, and the
   latest record's six fields. If it prints `no papercuts`, tell the user and stop.
2. Show the groups to the user as a short numbered list and ask which ones to turn into eval cases (one question, with
   AskUserQuestion in Claude Code; a plain question elsewhere).
3. For each group the user picks, draft a case in `evals/<ref>/<case>/` of the skills repo that owns the ref. Read two
   or three existing cases there first and copy their exact format: case.yaml (schema version, name,
   `expected_outcome`, `scaffold_script`), prompt.md (frontmatter, then the user's prompt), a graders folder (numbered
   files, `type: llm` or `type: tool_used`, same keys as the neighbours), and place-files.sh with its files folder. The case
   recreates the papercut's situation; the graders check the behaviour from `--fix`. Run the repo's own checks after
   (in famiglia: `python3 scripts/check-refs.py`).
4. Say where the fix belongs, per group:
   - **Our own skill**: fix its SKILL.md directly.
   - **A vendored skill** (listed in the repo's vendor.json): never edit it. Add a rule to the own skill that calls it
     (for example `dev-flow` or `commit-gate`), or draft an upstream issue for the user to file.
   - **A tool or the environment**: name the setup change, or say it needs no skill change.
5. Report: the cases written (paths), the fix location per group, and the groups left alone.

## If something fails

| Failure | Fix |
|---|---|
| `could not write <path>` | Paste the JSON line the script printed into the chat so the user can save it, then continue the task. |
| No `python3` | Write the same JSON line in your reply, with the fields `ts`, `repo`, `ref`, `kind`, `signature`, `blocked` and the six report fields. |
| A field needs a secret or file contents to make sense | Describe it in general words (`an API key in .env`), never the value. |
| `triage` prints `skipped <file>:<n>` | A broken line. Report it and triage the rest. |
| `no papercuts` | Say so and stop. Nothing to draft. |
| The ref is no longer a skill in the repo | Report the group as stale; don't draft a case. |
