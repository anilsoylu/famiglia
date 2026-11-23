# Analysis checklist

Question lists per area. Answer what the data can answer, mark the rest [?] with the missing instrumentation. Every answer carries numbers, date range, n and source.

## Contents
1. Activation and onboarding
2. Retention and churn
3. Feature adoption
4. Monetization
5. Segmentation
6. Messaging and re-engagement
7. Analytics and data quality
8. Existing plan review

## 1. Activation and onboarding
- What share of new users finish onboarding? Create the first core object (portfolio, project, workspace)? Reach the value moment (first real data, first result)?
- Time from signup to the value moment: median and p75. Does activation happen in the first session or never?
- Where does the funnel lose the most people, in absolute and relative terms? Is the loss before or after the account wall?
- Which steps sit between signup and value that the user did not need (forced account, many settings choices, permission prompts, paywall before value, stacked modals)?
- Are auto-created objects empty (a default project nobody fills)?
- Which early actions correlate with later retention (first-3-day feature count, number of items added)? Correlation only.
- What can change without a release (server-driven copy, messages, defaults sent by the API) and what is baked into the binary?

## 2. Retention and churn
- D1, D7, D14, D30 and "D7+/D30+ ever returned" by signup cohort month. WAU/MAU trend.
- Distribution of the last active day relative to signup: is the drop on day 0, or is there a second cliff (end of trial, first bill)?
- New vs returning actives per week.
- Retention by plan (free, trial, paid), by usage depth (items tracked, features used), by acquisition period, by locale/country, by app version where relevant.
- What do retained users do that churned users do not?
- Churn signals: previously regular users silent for N days; how many, reachable by which channel?
- Do users come back on their own or after a message? Compare return on message days with the same users' base daily return.

## 3. Feature adoption
- Inventory every user-facing feature (from code routes/screens and the API, not from marketing copy).
- Per feature: users, share of actives, frequency, free vs paid, retention of users vs non-users, purchase rate of users vs non-users.
- High value, low discoverability: features with strong retention correlation that few find (buried two taps deep, gated behind a condition most users never meet).
- Features nobody uses, features without any tracking ([?]).
- Free-limit pressure: how many users hit each limit, what they did next.

## 4. Monetization
- Paywall views, purchase starts, purchases and revenue by paywall source/entry point. Automatic vs intent-driven entries.
- Trials: count, length, outcome (converted, cancelled and when, billing failure, still running). Monthly vs yearly.
- Cancellations, refunds, expirations, billing issues by currency/country.
- Time from signup to first purchase; behavior before purchase (active days, items, features).
- Active free users who never saw an offer.
- Price level vs category, plan layout, which plan the paywall pushes, discount and loyalty offers: who got them, who could actually see them (app version), and what they produced.
- Store-page vs paywall drop (store "buy" sheet abandonment may be price shock; label it a hypothesis).
- Revenue so far: gross, net, per signup, per install.

## 5. Segmentation
Candidate segments (keep only those the data separates): new (<7 days), activated free and active, not-activated but active, highly engaged free, churn-signal, dormant activated, dormant never-activated, trial, new paid, long-term paid. Assign rules in order so each user lands in one segment. Per segment: size, defining behavior, need, retention pattern, monetization potential, intervention (or "leave alone": messaging people who never activated is often spam).

## 6. Messaging and re-engagement
- Sends by type per week, recipients, share of recipients with no client activity in 14/30 days.
- Same-day and 60-minute return after a send vs those users' base rate. Per type.
- Delivery measurement: are receipts or bounces collected? Can opens from a push be told apart from opens of an inbox screen?
- Content quality: trivial moves, stale data, internal codes instead of names, repeats of the same event, wrong local time.
- Fatigue: opt-outs, uninstalls, activity after heavy weeks.
- Weekend or quiet-day content: only real events (dividend dates, renewals, goal milestones). Invented content costs permission.
- What can ship server-side with existing message types (old clients may render unknown types badly).

## 7. Analytics and data quality
- Events that never fire, duplicates measuring the same thing, inconsistent names (`_view` vs `_viewed`), missing properties (app version, source, variant, locale).
- Identity: anonymous-to-user merge, internal-user flag.
- Attribution: does billing know which offering/paywall source sold? Do message events carry type and variant?
- Data errors that reach users: stale prices, implausible values, jobs that fail or hang.
- Questions that cannot be answered today, and the cheapest instrumentation (server-side first) that would answer each.

## 8. Existing plan review
For each item in the current plan: validated, contradicted, missing, re-prioritized, or new risk. Separate urgent fixes from optional improvements; do not expand scope automatically.
