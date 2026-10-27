# Agency manual and project files

Sources: sources/seo-prompt/tweet-1.md (AGENCY.md, layout), tweet-5.md (HANDOFF, LEDGER, research expiry), tweet-2.md
(permission gates, process interview), tweet-9.md (state file, running log).

## Folder layout (in the project, never in the skill)

```text
agency/
  AGENCY.md            same for every client (template below)
  clients/
    <site>/
      CLIENT.md        business, buyer, money pages, stage, data sources
      STRATEGY.md      patterns, ranked
      HANDOFF.md       current goal, decisions, open questions, next action (<400 words)
      LEDGER.md        one line per shipped change + next-check date, plus the run log
      LINKS.md         planned internal (and "Outside") links
      TECH.md  REPORT.md
      briefs/          <keyword>.md and <keyword>.serp.md (expires in 30 days)
      pages/           drafts + TEMPLATE
      data/            dated exports: gsc-YYYY-MM-DD.csv, crawl-YYYY-MM-DD.csv, serp/YYYY-MM-DD-<slug>.md
```
A single-site project can drop `clients/<site>/` and keep the files directly in `agency/`. Every task starts with
"Client: <site>". Read AGENCY.md, then that client's folder, and nothing from other clients. Blended notes are how
two sites end up with the same intro.

## AGENCY.md template (verbatim, adapt but keep the shape)

```text
# AGENCY.md (read before every task)

## Who does what
- One department per task. Say which one you're working as in your first line
- STRATEGIST writes STRATEGY.md. WRITER writes briefs/ and pages/. LINKER writes LINKS.md
- TECHNICIAN writes TECH.md. ANALYST writes REPORT.md and LEDGER.md
- Never do the next department's job in the same task

## The five levers, in this order
1. Match the search intent (page one of the results decides the page type)
2. The target keyword in the <title>, first, word for word
3. Internal links to the page: 3 to 5 minimum, from pages on the same topic, exact anchor
4. The site's authority (links to the domain)
5. Links straight to the page, only for competitive searches, sized on the top 3

## Hard rules
- Never create a page before checking one doesn't already exist for that intent
- Before touching a page, list the queries it already gets clicks for. If the change risks them, create a new page instead
- One new page a day, maximum. Two very good pages a week is the normal pace
- The first page of a pattern is made with me, by hand. Later pages are duplicated from pages/TEMPLATE
- After a real change, a page is not touched for 90 days. Write its next check date in LEDGER.md
- A position is only read with an exact page AND exact query filter
- In any "best X" list we publish, we are never number 1. Rank by truth
- No invented numbers, quotes, reviews or screenshots. Ever

## Every page ships with
- title (keyword first, then one promise), meta description, H1
- structured data (Article or the page's type, FAQPage if there's a FAQ, author)
- 3 to 5 internal links pointing TO it, placed in body text of related pages
- an entry in the sitemap, and an indexing request in Search Console
- a named author with a real bio, never "the team"

## Stop and ask me before
- deleting or redirecting any page
- anything that costs money (links, tools, ads)
- publishing the first page of a new pattern
```

Not in there on purpose: keyword density, word counts, "SEO score", heading hierarchy rules, alt-text audits. That's
polish, worth doing once the five levers are right, never the point.

## CLIENT.md template

```text
# CLIENT: <site>
url:              <https://...>
sells:            <what, price range>
buyer:            <who pays, what they search when they're close to buying>
conversion:       <named event, e.g. signup_completed / purchase>, tracked in <tool> (yes/no)
money pages:      <urls that convert>
authority:        <DR / referring domains, or "unknown">
languages:        <en, tr, ... + hreflang yes/no>
cms / deploy:     <code repo | WordPress | Webflow | ...> and how a change goes live
author(s):        <name + one-line bio>

## Stage
current stage:    <0-7 from the skill's stage menu>
updated:          <YYYY-MM-DD>

## Data sources (what this project actually has)
gsc:              <csv export | MCP/API | none>
serp/keywords:    <ChatSEO MCP | DataForSEO | Ahrefs | manual browser | none>
crawl/render:     <Firecrawl | Screaming Frog | local files | none>
conversions:      <PostHog | GA4 | none>
web search:       <Parallel | WebSearch | none>

## Open questions
- ...
```
Anything you couldn't find goes under "Open questions". Don't guess it.

## HANDOFF.md (keeps fresh chats cheap)

```text
Update HANDOFF.md for this site. Include: the goal of this week, the decisions we confirmed, the file paths that matter, the questions still open, and the next action

Keep it under 400 words. Link to the evidence in data/ instead of copying it. Keep every uncertainty and every constraint

Then give me a one-line starter message for a fresh chat that reads SITE.md, RULES.md and HANDOFF.md first, and opens other files only when the task needs them
```
(In this layout SITE.md = CLIENT.md and RULES.md = AGENCY.md.) Test it: a fresh chat that reads only CLIENT.md,
AGENCY.md and HANDOFF.md should be able to say what the site sells, who buys, what happened last week and the next
action. If it needs more than 3 questions, the missing answer belongs in one of those files.

## LEDGER.md

Two parts:

```text
## Pages
<url> | <target query> | changed <YYYY-MM-DD>: <what> | pos at change <n|new> | next check <YYYY-MM-DD>

## Run log (append only, never delete)
2026-10-25 09:04 | step 1 due list   | done   | data/due-2026-10-25.md | 3 not due, 11 due
2026-10-25 09:10 | step 3 serp "..." | failed | -                      | captcha, retried once, stopped
```
Next-check rules: changed in the last 90 days → change date + 90 (unless something broke) · stable → next weekly
pass · lost clicks two weeks running → this week · no impressions for 16 months → next quarterly review.

## Saved research has an expiry date

Every saved read (SERP, competitor page, keyword pull) carries: question, source, checked date, findings, refresh rule
("before writing if older than 30 days, or after a Google update"), unknowns. Before any new research, look in data/
for a saved result that answers the same question. If it's still valid, reuse it and say `reused <file>, checked <date>`.
If it's stale, refresh only the part that expired.

## Permission gates

```
ALLOW
- Read Search Console, analytics and SEO tools
- Create drafts in the CMS / on a branch
- Write to agency/ files

REQUIRE APPROVAL
- Publish a page, or update a live one
- Change a title or meta description on a page that gets clicks
- Add or change a redirect
- Anything that costs money; any outreach

NEVER
- Delete a page or a file on the live site
- Touch robots.txt, the sitemap or canonical tags without an explicit task for it
- Email or contact anyone outside the company
```
Scheduled or cloud runs get read-only access. Trace every recommendation to its evidence: if you couldn't have made the
call yourself from the evidence shown, don't approve it.

## Capture the user's own process (optional)

If the user has a process that isn't written down yet:
```text
Interview me about how I run <a technical SEO audit / this task>.
Ask one question at a time. Ask what I check first, which tool
I use for each check, what threshold makes me flag something,
and what I do when two tools disagree.
When I say "done", write it as a skill: numbered steps,
the tool for each step, the threshold for each flag.
Mark every step where I said "it depends" and ask me to
turn it into a rule.
```
