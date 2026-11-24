# Brewlog

Coffee journal for iOS (SwiftUI). Log a brew (beans, method, grind, ratio, rating), see your best recipes, get a "dial-in" suggestion for the next cup. Solo developer. Launched on the App Store on 2026-10-20.

## Plans

- Free: up to 10 logged brews, basic stats.
- Brewlog Pro: unlimited brews, recipe comparisons, export.
  - $4.99/month (`brewlog_monthly_499`)
  - $29.99/year with a 7-day free trial (`brewlog_yearly_2999`)

Paywall entry points (`source`): `onboarding` (after onboarding), `limit` (11th brew), `settings`.

## Data in this folder

Exports from launch to 2026-11-23 (UTC). No live access to anything else.

- `data/users.csv`: accounts (Sign in with Apple, email shared).
- `data/events.csv`: TelemetryDeck export.
- `data/purchases.csv`: StoreKit server notifications, simplified.

My own account (`owner@brewlog.app`) is in there too, from TestFlight.
