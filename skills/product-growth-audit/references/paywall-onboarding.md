# Onboarding and paywall review

Source: Tobia Donadon (@tobiadonadon_), "How to Build App Paywalls and Onboardings with Claude", 2026-11-13, https://x.com/tobiadonadon_/status/2121382249392464083 (paraphrased). For a full redesign use the `paywall-optimization` skill or the author's paywall-designer skill; this file is the audit checklist.

## Onboarding
- **Value before the account.** A cold signup form first ("create your account") makes people decide before they have seen anything. Better: promise, a few personal choices (goal, level, reason), a real first win (a lesson, a first result), then the account ("after the win"), with "later" allowed where the platform permits.
- **One job per screen.** Each step does one thing: promise, pick, reason, goal, schedule, first win, account, close.
- **Show the notification they will get** when asking for permission (the time and the text), not a generic prompt.
- Audit questions: how many decisions before value? Is the account wall before value? Does anything in onboarding feed the paywall later?

## Paywall
Three layers to check:
1. **Price and plans.** What is charged, how many plans, monthly vs yearly, trial or not, which plan is pre-selected and shown per month, how it compares with what similar apps charge.
2. **The conversation, not one screen.** What the user was promised before, when the paywall appears, the doubts at that moment and the line that answers each, and what happens after "no" (smaller plan, reminder, a way back later).
3. **The screen.** Headline tied to the user's own reason ("Spanish for your trip", not "Unlock Plus").

Honesty checklist (each "no" is a finding; dark patterns get apps rejected and break consumer rules in the EU):
- Visible close button.
- Real trial with a timeline that names the price and the charge date ("today: everything unlocked; day 12: reminder; day 14: $69.99").
- A reminder before the charge that is on by default, not a toggle the user must enable in Settings.
- The honest line under the button: "Free until <date>, then <price>/year. Cancel anytime."
- Restore, terms, privacy present.
- No fake timers, invented reviews or false claims; every claim true of the product.
- A confirmation after purchase that repeats the deal and the reminder date.

Teardown lessons (big apps): Headspace names price and date but lacks the line under the button; Strava's timeline says "the subscription amount" instead of the number; Calm discloses renewal but leaves the reminder off. Each fix is a missing line, not a trick.

## In the audit
Map each finding to data where possible (paywall source conversion, trial cancellations in the first hours, store-sheet abandonment) and to the build requirement: most onboarding and paywall layout changes need a store release; copy, offers and reminders may ship server-side if the app reads them remotely. Check what the app actually supports before promising a server-only fix.
