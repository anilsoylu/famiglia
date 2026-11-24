# Stepwise

Habit tracker for iOS (React Native / Expo). Solo founder plus one contractor. Live on the App Store since spring 2026; current version 2.5.0 (released 2026-10-15).

## What the app does

- **Habits**: create a habit (name, icon, days of the week), check it off each day.
- **Streaks**: current and best streak per habit, shown on the home list.
- **Reminders**: one daily reminder at a time the user picks (set during onboarding or later in Settings).
- **Weekly report**: Monday summary of last week's check-ins, opened from a push or the home banner.
- **Stats screen**: completion rate per habit, heatmap, best weekday. Lives under Settings > More > Statistics (there is no tab for it).
- **Widgets**: home screen widget with today's habits (no analytics event for widget usage).

## Plans

| | Free | Stepwise Plus |
|---|---|---|
| Habits | 3 | Unlimited |
| Reminders | 1 | Unlimited, per habit |
| Stats screen | Last 7 days | Full history + heatmap |
| Price | | $4.99/month, or $39.99/year with a 7-day free trial (yearly only) |

Product IDs: `stepwise_monthly_499`, `stepwise_yearly_3999`.

Paywall entry points (`source` property on the paywall event): `onboarding` (shown automatically after onboarding), `limit` (trying to add a 4th habit), `settings` (Settings > Upgrade), `stats` (tapping a locked chart on the stats screen).

## Push notifications

Sent from our backend via Expo push. Types: `daily_reminder` (the user's reminder time, every day), `streak_risk` (evening, when a streak is about to break), `weekly_report` (Mondays 08:00 UTC), `winback` (after 14 and 30 days without opening the app). Reminder copy and schedule are server-side; push types are fixed in the app binary.

## Data in this folder

All exports cover 2026-08-23 to 2026-11-20 (UTC). Nothing else is available; there is no live access.

- `data/users.csv`: accounts from our Postgres DB. An account is created on the first onboarding screen. `is_internal` was added in August and is not set consistently.
- `data/events.csv`: PostHog event export (client events). `properties` is JSON.
- `data/subscriptions.csv`: RevenueCat webhook events (USD, gross, before Apple's cut).
- `data/push_log.csv`: our push outbox (sends only, no delivery receipts, no open tracking).
- App Store Connect (not exported, copied from the dashboard): **880 first-time downloads** in the same 90 days.

Team accounts use `@stepwise.app` emails. The App Review demo account is also on that domain.
