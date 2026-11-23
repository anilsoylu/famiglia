---
name: product-growth-audit
description: Read-only, evidence-first audit of a live app or SaaS that finds what holds back activation, retention, engagement and paid conversion, sizes how much the current user base can still give, checks whether paid acquisition can pay back, and ends in a prioritized opportunity list with the build each item needs. Use it whenever someone wants to understand why users don't stay or pay, asks "where should engineering effort go", "why aren't we growing", "how much can we improve without new users", wants a product/growth/data audit from analytics, the production database and billing data, or wants to judge a growth playbook (influencers, paywall redesign, SEO tools) against their own numbers, even if they never say "audit". Works on any product: it discovers the stack, data sources and business model first.
---

# Product growth audit

Find out what is actually happening inside one product, what holds it back, and where engineering effort will create the most measurable value. This is research, not implementation: the deliverable is a report and a prioritized plan, and the run ends by waiting for the owner's approval.

The owner who wrote the brief behind this skill put it this way: "I don't want a generic SaaS growth checklist. Discover what is actually happening inside this product." Every section below serves that. A finding without a number, a date range, a sample size and a source is an opinion, so label it as one.

## Guardrails (read before touching anything)

These protect real users and real money; break one and the audit does more harm than good.

- **Read-only everywhere.** Production databases: open the session read-only (Postgres: `SET default_transaction_read_only = on;` before any query) and run only SELECTs. No migrations, no writes, no "quick fix" of bad rows.
- **No side effects in external services.** Don't change billing, analytics, push or store settings, don't trigger notifications or emails, don't create report requests or experiments, don't deploy. If a tool call would create something (a report request, a tracked keyword, a cohort), say so and ask first.
- **No personal data in output.** Aggregate and anonymize. No emails (including partial ones such as `dana@`), names, user IDs, device tokens or individual purchase histories in the report, because reports get shared. If the owner points you at one user ("look at this paying user"), describe the pattern, not the person. If the owner asks for a list of people (e.g. trial users to thank), keep it out of the report and tell them how to pull it from their own data (a query or one-line command).
- **Secrets stay secret.** Read credentials from env files without printing them, and without `source`-ing the file (tokens can contain shell metacharacters such as `|`); use `grep '^NAME=' .env | cut -d= -f2-`. If an API says "unauthenticated", check how the value was loaded before blaming the credential.
- **Shared quotas.** App Store Connect, Stripe and similar APIs rate-limit per key. Bulk analytics pulls can lock the same key that a release or the billing system needs. Pull the minimum, paginate gently, and never do bulk pulls on a release day.
- **Exclude internal users** (owner, team, test and review accounts) from every metric, and say how many you excluded and how you found them.

## Workflow

Work through the phases in order. Phase 1 decides what the rest can measure; skipping it produces a checklist instead of an audit.

### Phase 1: Recon (what is this product and what can we measure?)

1. **Product and model.** From the repo, docs, store listing or website, establish: platform (iOS/Android/web), business model (subscription, one-off, ads, B2B seats, usage-based), price points and trial, the free/paid boundary (limits in code beat limits in docs; read the code), the core value moment, and the release constraint (what needs a store release, what ships via backend, OTA or a web deploy). Record app versions in the field if old binaries behave differently.
2. **Source map.** List every data source you can actually reach and what each can answer: product analytics (PostHog, Mixpanel, Amplitude, GA4), production DB, billing (RevenueCat, Stripe, Paddle, store reports), messaging (push, email logs), store/ASO data, support inbox, reviews, existing plans and ADRs. For each: access method, date coverage, known gaps. `references/data-sources.md` has safe query patterns per tool. If the owner hands you exports (CSV, JSON, screenshots) instead of live access, those are the sources: the same rules apply, and you state that the audit covers only what the exports contain.
3. **Read the existing plan** if there is one. You will judge it in Phase 5, not adopt it.
4. **Measurement sanity check.** Before you trust a metric, check one thing that would expose a broken measurement: event volume over time (did tracking start late, change name, or break on a version?), duplicate identities, server vs client events. Many "the feature died on date X" findings are a renamed event or a data window that starts that day. Prove a break with a second source before calling it a bug.

Tell the owner in a few lines what you can and cannot measure before the long analysis, so a missing key can be fixed early.

### Phase 2: Define and baseline three north-star metrics

Define these concretely for this product, compute today's value with numerator and denominator, and show the trend by cohort month:

- **Activation rate**: share of new signups who reach the core value moment within N days (for a portfolio app, "first asset added and value shown"; for a SaaS, "first project with real data"). Choose N from the data: where do most activations happen?
- **Weekly retained users**: users active in week N who are active again in week N+1 (or a D7+/D30+ return rate if weekly volume is too small).
- **Free-to-paid conversion**: active free users who start a trial or buy, and trial-to-paid. Split by plan and by entry point (which paywall source).

If the product cannot measure one of them, that is a finding: say which event or field is missing.

### Phase 3: Analyze

Cover each area, using the question lists in `references/analysis-checklist.md`. Prefer depth on the areas the data says matter over even coverage.

1. Activation and onboarding: funnel by step, time to value, where people drop, which steps stand between signup and the value moment.
2. Retention and churn: D1/D7/D14/D30, last-active-day distribution (when do people stop?), retention by cohort, by plan, by usage depth, churn signals, natural returns vs returns after a message.
3. Feature adoption: an inventory of features with users, share of actives, frequency, free vs paid, link to retention and to purchase; mark high-value features that are hard to find and features nobody uses.
4. Monetization: paywall views, starts and purchases by source; trial outcomes; monthly vs yearly; cancellations, refunds, billing failures; time from signup to purchase; what payers did before paying; limit pressure (how many users actually hit each free limit).
5. Segmentation: build segments from behavior, assign each user to exactly one, and give each segment its size, defining behavior, need and intervention. Keep segments only if the data separates them.
6. Messaging and re-engagement: volume by type, recipients' activity, same-day/60-minute return after a message vs the same users' base rate, fatigue (opt-outs, activity after), content quality (stale or trivial content is worse than none).
7. Analytics gaps: questions you could not answer and the instrumentation that would answer them, especially changes that need no app release.

Throughout, separate correlation from causation: "users with 4+ assets retain better" does not mean forcing 4 assets helps.

### Phase 4: Size the upside and check acquisition

- **Upside from existing users.** Answer "how much can revenue and retention improve without new users?" with a scenario table: lever, target group size, assumption as a range, resulting change in the north-star metrics and in money per year. Be honest when the base is too small for meaningful revenue; often the real lever is not losing the next new users on day 0.
- **Acquisition fit.** Before recommending any paid channel (influencers, ads), compute revenue per install (lifetime revenue / installs or signups, with the conversion steps in between) and compare it with a realistic cost per install for the category. If revenue per install is below cost, paid acquisition loses money until activation or conversion improves; say so and say what would need to change. `references/growth-playbooks.md` holds the influencer and SaaS playbooks with their preconditions.
- **Paywall and onboarding fit.** Review the onboarding and paywall against `references/paywall-onboarding.md` (value before account, a paywall that remembers why the user came, an honest trial timeline, a real reminder, a visible close, a path after "no"). Mark which fixes need a store release.

### Phase 5: Opportunities, priorities and the existing plan

For each opportunity give: the problem, the evidence (numbers, range, n, source), the proposal, expected impact, confidence, complexity, build requirement (backend-only, OTA, web deploy, or store release) and how success will be measured. Aim for 10 or more only if the data supports that many; never invent features to fill the list. Prefer making existing features more valuable or more visible before proposing new ones, and prefer changes that ship server-side.

Prioritize:
- **P0**: bugs or data errors that lose money, users or trust (wrong numbers shown, broken flows, offers that misfire).
- **P1**: high impact, low cost.
- **P2**: valuable, medium term.
- **P3**: experiments and long shots.

Then review the existing plan item by item: validated, contradicted, missing, re-prioritized or risky. Call out where the new data argues against something the owner already decided, give the evidence, and leave the decision to them.

Also list what **not** to do, with the reason: for example A/B tests when the traffic cannot reach significance (estimate the sample needed and the weeks it would take), discounts that only raise purchase starts, more notifications when the problem is content.

### Phase 6: Report and stop

Before writing, recompute the headline numbers (the ones in the executive summary and the north-star table) a second way, for example with a separate query or by counting from the raw rows, and fix any that don't match. A wrong headline number undoes the trust the rest of the report earns.

Fit the length to the question. A full audit uses `references/report-template.md`; a narrow question (one rate, one test, one decision) gets a short answer with only the sections it needs, still with numbers, n and labels. Write in the language the owner writes in. Put it where the owner will read it (a plan file, a doc, or the reply). Then stop: present the findings, ask for the decisions that are genuinely theirs (money, scope, product direction), and wait for approval before any implementation.

## Evidence labels

Tag every important finding:
- **[D] Verified**: measured directly, with numbers, range and source.
- **[GH] Strong hypothesis**: consistent signals from more than one angle, not proven.
- **[ZH] Weak hypothesis**: plausible, thin data or one signal.
- **[?] Unknown**: cannot be measured yet; name the missing instrumentation.

State sample sizes next to every rate ("2/11 trials", not "18%"). Below roughly 30 in a group, say the result is directional only.

## Related skills

Load these for depth when a finding calls for it, after the audit, not instead of it: `onboarding-optimization`, `retention-optimization`, `paywall-optimization`, `subscription-lifecycle`, `monetization-strategy`, `almost-paid` (users who nearly paid), `app-analytics` or `analytics` (instrumentation), `creator-ugc-marketing` and `ua-campaign` (only after the acquisition-fit check passes), `aso-audit` (store discovery).
