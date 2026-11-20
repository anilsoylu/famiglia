---
name: start-anil-session
description: Start a work session in a project with Anil's rules (Turkish chat, English repo, anilsoylu commits, subagents write code, local Docker tests, gate → cpr → merge), wired into CLAUDE.md so they survive /clear, and install his subagent roster.
disable-model-invocation: true
metadata:
  version: 0.3.0
---

# Start Anil session

Set up the current project so Anil's working rules apply now and in every later session, then report the environment
in Turkish. The rules live in one file, `references/rules.md` next to this skill. Read it now and follow it for the
rest of this session.

A skill's text disappears from context on `/clear`; `CLAUDE.md` is reloaded every time. That is why step 2 links the
rules file from the project's `CLAUDE.md` instead of relying on this message.

## 1. Find the project

- Project root: `git rev-parse --show-toplevel`. Not a git repo: use the current directory, still do steps 2 to 4,
  skip the git rows, and say in the report that commits and PRs need `git init` and a remote.
- Default branch, first that works: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`,
  `git symbolic-ref --short refs/remotes/origin/HEAD`, `git config init.defaultBranch`, else `main`.
- Remote: `git remote -v`. No remote means `/cpr` and merge can't run yet; put that in the notes.

## 2. Wire the rules into CLAUDE.md

The project-root `CLAUDE.md` must end up with exactly one copy of this block:

```
<!-- start-anil-session:begin -->
@~/.claude/skills/start-anil-session/references/rules.md
<!-- start-anil-session:end -->
```

- File missing: create it with the block.
- Block missing: append it after a blank line (add a trailing newline to the file first if it lacks one). Leave all
  other content untouched.
- Block present but different, or present more than once: replace them with the single block above.
- Block present and identical: nothing to do.

This is a small config edit, so do it directly rather than through a subagent. It goes into the next commit; the
import resolves only on Anil's machine and is ignored for other contributors.

## 3. Install the agents

Claude Code only; other agents skip this step. The roster has six agents. The `references/agents/` folder next to this
skill holds five of them (`worker`, `tester`, `explorer`, `reader`, `researcher`). The sixth, `reviewer`, comes from
the sibling `review` skill: `<skills-dir>/review/reviewer.md` (for a Claude Code user install,
`~/.claude/skills/review/reviewer.md`). `/review` spawns an agent named `reviewer` with that contract, so the installed
one must be the same file. `rules.md` routes work to them.

- Run `mkdir -p ~/.claude/agents`.
- For each file in `references/agents/`, copy it to `~/.claude/agents/<same file name>` only if that path does not
  exist. Use a no-clobber copy such as `cp -n`.
- Copy the `review` skill's reviewer file to `~/.claude/agents/reviewer.md` the same way. If the `review` skill is not
  installed, skip it and say so in the report.
- Never overwrite or merge an existing file, even if it differs. The user's copy wins.
- Note which files you installed and which were already present, for the report.

Do this directly rather than through a subagent, like the `CLAUDE.md` edit. Newly installed agents may only appear
after `/agents` or in a new session.

## 4. Check the environment

Run the checks in parallel where possible. Fix only what the "If wrong" column says to fix; everything else is
reported.

| Check | How | If wrong |
|---|---|---|
| GitHub account | `gh auth status` active account | `gh auth switch -u anilsoylu`; if that account isn't logged in, tell the user to run `gh auth login` |
| Git author | effective `git config user.name` and `user.email` | Name isn't `anilsoylu`: if the global identity is `anilsoylu`, set repo-local name and email from it; otherwise ask the user |
| Branch | current vs default branch | On the default branch: first task starts on a new kebab-case feature branch (note) |
| Docker | `docker info`; `docker compose ps` if `compose.y(a)ml` or `docker-compose.y(a)ml` exists | Report; start services only when a test needs them |
| Test database | DB URLs in `.env*` and config files, host part only | Non-local host: ⚠ in the report plus a note that tests, migrations and seeds stay blocked until it points at local Docker; offer to switch it to the compose DB service. Never print credentials |
| Tracked secrets | `git ls-files` for `.env*` (except `.env.example`-style templates), `.gitignore` coverage | Note it as a security risk; don't untrack or rewrite history without the user's yes |
| Stack | lockfile versions first, manifest ranges if there's no lockfile; DB/service images from compose | Report main frameworks and services with versions, used later for docs research |

## 5. Report in Turkish

Use ✓ for OK, ✗ for missing or failed, ⚠ for works but risky. Then a notes list for anything that needs attention
(only include notes that apply), then ask what to work on.

```
Oturum hazır: <repo> (<current branch>, default: <default branch>)
<✓|✗> GitHub: <active account>
<✓|✗> Git author: <name> <email>
<✓|✗|⚠> Docker: <daemon state>; <compose services and their state>
<✓|⚠> Test DB: <host>
Stack: <framework@version, ...>; servisler: <postgres:17, ...>
CLAUDE.md: kurallar bağlandı | zaten bağlı | güncellendi
Ajanlar: kuruldu <list> | mevcut, dokunulmadı <list>

Notlar:
- <default branch note, remote missing, non-local DB, tracked secrets, CLAUDE.md change goes into next commit>

Ne üzerinde çalışalım?
```

From here on, plan in the main thread and hand work to the agents as `rules.md` routes them.
