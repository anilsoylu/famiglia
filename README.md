# famiglia

Claude Code skills for two jobs: shipping code from plan to production, and running SEO for a site.

## Install

```bash
git clone https://github.com/anilsoylu/famiglia.git
cp -R famiglia/skills/* ~/.claude/skills/
cp famiglia/skills/review/reviewer.md ~/.claude/agents/   # optional, /review falls back without it
```
Restart Claude Code (or open a new session) so it picks up the new skills.

## Use

Just talk. The right skill picks itself up. You can also call one directly with `/name`.

**Code**

| You say | What runs |
|---|---|
| "let's build team invites" | `dev-flow` → plan: risk review, "what if the server dies / scales" check, plan for approval |
| "feature's done, what's next?" | `dev-flow` → review: inefficiency review, `/review`, `/simplify` |
| "ready to commit" / `/commit-gate` | `/perf` → `/optimize` → `/security-audit` on the diff, one go/no-go report. Never commits |
| "merge to master" / `/cpr` | clean the diff, open or update the PR, and merge it when you ask |
| "is it production ready?" | `dev-flow` → end: full production audit with scorecard, "server dies / scale" answers, offers the full security audit |

**SEO**

| You say | What runs |
|---|---|
| "start SEO for mysite.com" | `seo-agency` → onboarding: asks the stage and your data sources (Search Console, ChatSEO, ...), sets up `agency/` in your project |
| "what should we rank for?" | strategy: keyword patterns with buying intent, page-one read |
| "write a page for <keyword>" | brief → write → fresh-context review → ship list |
| "weekly SEO pass" | Search Console quick wins, respects the 90-day wait, stops for your pick |
| "get us cited by ChatGPT/Claude" | AI visibility, with `/ai-seo` |

`seo-agency` keeps its state in your project's `agency/` folder, so the next session picks up where the last one stopped.

**Other skills in here:** `pr-ready` (rebase, CI, review threads), `pr-triage` (other people's PRs), `list-open-work`
(your open PRs), `no-tropes` (strip AI-sounding prose), `clean`, `pr-update`, `review`.

## Update

- Skills in `skills/` are maintained here. Edit them directly.
- Except `ai-seo`, `seo-audit` and `security-audit`, which are copies pinned in `vendor.json` (licenses in `LICENSES/`).
  Don't edit those. Bump `ref` in `vendor.json` and run `python3 scripts/sync-vendor.py`.
- After any change: `python3 scripts/check-refs.py` checks that every file a skill points to exists.
- Evals live in `evals/<skill>/<case>/`: real failures from past sessions plus routing checks. Run them before and after
  editing a skill, and keep the change only if nothing drops:
  ```bash
  claude plugin eval . --model claude-opus-5-5 --scaffold --trust-plugin --allow-tools Bash Write Edit -j 4 --no-publish
  ```
  Add `--case <name>` for one case, `--runs 1` for a quick pass. macOS needs a real git on PATH (`brew install git`),
  because the eval sandbox blocks the Xcode git shim.
- `python3 scripts/skill-size.py` shows each skill's description size (in context every session) and body size.
- Raw prompts the skills were built from live in `sources/` (git-ignored, local only).
