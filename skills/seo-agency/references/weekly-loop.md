# Weekly loop

One loop, merged from four sources: tweet-5 (six-step checkpointed pass, cheap reads), tweet-1 (Analyst weekly report),
tweet-8 (weekly review flags), tweet-9 (one change at a time, judge search + business together).

## The pass

```text
You run my weekly SEO pass on <site>. Read CLIENT.md, AGENCY.md and HANDOFF.md first. Open other files only when a step needs them

Step 1, due list: from LEDGER.md, list the pages whose "next check" date has come. Skip the rest and write "not due"

Step 2, quick wins: from Search Console (last 28 days, compared with the 28 before), keep only queries in positions 5 to 20 with impressions, for the pages on the due list or never changed. Sort by impressions. Save the filtered table to data/

Step 3, reuse: for each of the top 5 candidates, look for a saved results-page read in data/ that's still valid. Read the first page of results only for the ones that have none or an expired one

Step 4, propose: for each candidate, one change (title, internal links, refresh or new page from the pattern), with the evidence rows. Rank them by business value x impressions x how reachable they are for this site. Write them in HANDOFF.md under "proposed" and STOP. I pick

Step 5, after my pick: the Writer drafts ONLY the picked changes from the template, the Checker runs the checklist, and you give me the drafts with the check results

Step 6, close: update LEDGER.md (what shipped, what failed, next check dates) and HANDOFF.md (the next action), then give me the starter message for next week

Checkpoint after every step. Retry a failed step once, then mark it failed and go on. Stop on any captcha or login wall. Nothing goes live without my yes
```

## What the report must also say (Analyst)

- Pages past their check date: target query, position at publish and now (**exact page + exact query filter**), clicks
  before/after. Verdict: won / progressing / stuck.
- Pages whose impressions jumped: they just entered the top 10. Queue them for a brief. Top 10 → top 3 is the cheapest win.
- Queries with many impressions and few clicks where we're top 5: title rewrite candidates.
- Pages changed 90+ days ago, still outside the top 3, with a good brief: candidates for links (Linker outside).
- Pages edited in the last 60–90 days: "wait". Don't touch them.
- Brand and non-brand reported separately.
- **One recommendation per department at most**, ranked by business value, not traffic.

## Judging changes

- One change per page at a time. Change title, intro and links in the same week and you'll never know which one did the work.
- Ignore moves shorter than a couple of weeks. Positions wiggle and come back on their own.
- Judge search and business together. A page that climbed and brought zero extra conversions is a miss. One that stayed flat
  but converts better after a clearer CTA is a win.
- Don't touch a page that's doing well without a strong reason.
- Keep the instructions frozen during a test. Changing the prompt mid-experiment makes weeks incomparable.

## Keep it cheap

- **Read only what the task needs.** Before opening anything, write the exact questions the step must answer. GSC: filter
  by page and position before reading. Results pages: first page only, 10 results, URL + title + page type + date. Our pages:
  title, meta, H1, H2/H3 list, first 150 words and body links. Read the full body only for a refresh or rewrite. Keep full
  originals in data/ with their date. Never drop evidence the answer depends on.
- **GSC extract script** (build once per project, then never paste raw exports):
  ```text
  Write a small script for my agency folder that takes a Search Console export (CSV, Queries + Pages) and outputs only:
  - the rows for the page I pass as an argument (or all pages if none)
  - positions between 5 and 20
  - impressions above 50
  - sorted by impressions, top 30 rows max
  - columns: query, page, clicks, impressions, CTR, position
  Save the output to data/ with today's date in the file name. Then show me the command to run it. Don't read the CSV yourself
  ```
  Check the extract against the original once for 3 items. If it dropped something that changes the answer, fix the rule.
- **Breakage check** (cheap mode, any week): for every page in LEDGER.md check only HTTP status, still indexed (a GSC row
  with impressions in the last 7 days counts), and whether the SERP title matches ours. Report only what changed,
  otherwise "no breakage". Don't read page bodies.
- **Failure rules:** each step writes its result to data/ and a line to the LEDGER run log (step, status, file, time).
  Retry once. If it fails again, mark it failed with the reason and continue with the steps that don't depend on it. Never
  re-run a step marked done. Stop completely on captcha, login wall, a 403 from Google, or a password prompt, and write it in HANDOFF.md.

## Measure the loop itself (monthly)

```text
Compare the original and the new weekly pass from LEDGER.md, using the same definition of a usable result for both

Report: assignments processed, results shipped, verified no-change, failed, unfinished, usage, and my correction minutes. Include the setup time of the new files

Break it down by task type (title fix, internal links, new page, refresh). Flag missing measurements and weeks that aren't comparable

Tell me which change helped, which one cost quality, and which one needs another week of data
```

## Scheduling

A recurring run (scheduled task / `/schedule` / `/loop`) opens a fresh session that reads HANDOFF.md. Keep it in a
permission mode that stops on anything not allowed, because that pause is the approval step. Cloud routines that run
unattended get read-only access and never the keys to publish.
