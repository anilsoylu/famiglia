# Money page and the four-pass checkup

Source: sources/seo-prompt/tweet-9.md. Use when the user wants "the one page worth this week", or before a sitewide audit (which
this replaces for most sites).

## Find the money page

1. From GSC, pull every page with impressions, clicks and average position over the last few weeks.
2. From conversion tracking (PostHog/GA4, per CLIENT.md), pull conversions per landing page and line them up page by page.
3. Look for a page that already converts the visitors it gets and already shows in search, but sits just low enough that
   most searchers never see it. That's the money page.
4. A page with lots of impressions and zero conversions is a trap. Flag it as one, don't recommend it.
5. For 2–3 candidates, check the queries behind each page (volume, who ranks top), then look at the live SERP for the
   main query. If the top spots are how-to guides and the candidate is a pricing page, the query wants something else. Drop it.
6. Each candidate gets one call: **keep**, **keep once <one condition> is fixed**, or **drop**, explained with links to what you looked at.
7. Output: one page, one main query, a short written reason.

No conversion tracking? Say so. The first fix is a named conversion event. Without it no SEO work can be judged.

GSC caveats: data lands 2–3 days late, page+query breakdowns drop rows, AI Overview appearances can flatter average
position. Pull day by day into the state file to avoid quota walls and keep a history.

## Four-pass checkup on that page

1. **Access.** Googlebot not blocked, normal status code, real indexable text (URL Inspection / Page Indexing). JS-heavy
   site: compare the rendered text with the raw HTML. Speed: PageSpeed Insights, mobile first, only failures big enough to
   hurt a real visitor.
2. **Competition.** Pull the top 10 for the main query and read each page **in full** (Firecrawl or fetch), side by side
   with ours. Return what the winners cover that we don't, questions they answer that we skip, and what ours says better.
   Every claim cites the URL it came from. Missing data is written as missing, never guessed.
3. **Answer engines.** No special trick: answer the question in the first line under each heading, make headings match
   how people ask, make each section stand on its own, keep business details identical everywhere online. Schema only when
   the page fits a rich result, not as an AI shortcut. More in `ai-visibility.md`.
4. **Path to conversion.** Read it like a buyer. Is there one obvious next step, does it show early enough, does the page
   answer the last doubts before signing up? Is the conversion tracked as its own named event? Which pages that already
   get traffic should link to this one?

End with one report in the client folder that ranks the fixes and recommends **one** change to make first. Then it goes
through brief → write → review → close like any other change, and into LEDGER.md.
