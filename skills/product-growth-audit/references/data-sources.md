# Data sources: discovery and safe access

Discover first, then query the minimum. Never print secrets; never write.

## Discovery
- Env files: list variable names only (`grep -oE '^[A-Z0-9_]+=' .env*`). Read a value with `grep '^NAME=' .env | cut -d= -f2-` (strip quotes), never `source .env`.
- Code: grep for SDK initializations (`posthog`, `mixpanel`, `amplitude`, `gtag`, `Purchases.configure`, `stripe`, `expo-notifications`, `onesignal`, `sentry`) to learn which tools exist and which events the app sends (`capture(`, `track(`, `logEvent(`).
- Docs and plans: `docs/`, `plans/`, ADRs, README, existing analytics dashboards or admin endpoints (an `admin-insights` service often already holds useful queries).
- Ask the owner only for access you cannot find (a missing API key or role), and say exactly which scope is needed.

## Product analytics
- **PostHog**: HogQL via the query API (`POST /api/projects/:id/query/` with a personal API key scoped read-only). Filter internal users by email domain/known IDs and by `is_internal` if it is actually set (check first). Watch for project region (EU vs US host).
- **Mixpanel / Amplitude**: export or JQL/insights APIs with read-only service accounts.
- **GA4**: Data API; web only, rarely enough for app funnels.
- Always check the earliest event date: a dataset that starts recently makes older comparisons invalid.

## Production database
- Connect through the path the team already uses (SSH tunnel, bastion, read replica). Prefer a replica.
- Postgres: `SET default_transaction_read_only = on;` first, then SELECTs only. Add `statement_timeout` for heavy queries. Aggregate in SQL; never pull user rows into the report.
- Useful tables to look for: users/accounts, sessions or daily `app_open`-style analytics events, core objects (portfolios, projects), subscription/webhook events, notification outbox/logs, job runs.

## Billing
- **RevenueCat**: v2 API with a read-only key (`customers:read`, `subscriptions:read`; metrics/offerings may need more scope and return 403). The app's own webhook table is often the most complete history.
- **Stripe**: restricted read-only key; subscriptions, invoices, checkout sessions (abandoned checkouts), refunds.
- **App Store / Play**: sales and analytics reports (downloads by source and territory, product page conversion). These APIs have hourly quotas shared with release tooling; request only what you need and don't run bulk pulls near a release.

## Messaging
- Push: outbox/log tables, provider receipts (Expo, FCM, APNs). Email: provider event logs (opens are unreliable after privacy changes; clicks are better).

## Store and reviews
- Ratings and reviews (store APIs or an ASO tracker), rating count vs competitors, recent review themes. Keyword tools are for discovery, not the audit's core.

## Recording what you used
For every number in the report keep: source, query or endpoint, date range, filters (internal users excluded, versions), n. Put a short "Sources" section in the report.
