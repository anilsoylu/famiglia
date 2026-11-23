# Ledgerly

Invoice automation for small agencies and studios (2-15 people). Web app (Next.js + Postgres), billing through Stripe. Two founders, one engineer, one part-time support person.

## Core flow

1. Sign up, start a 14-day trial (card required at signup, Stripe subscription created in `trialing`).
2. Add clients, send invoices from templates (`invoices_sent`).
3. Connect the business bank account (`bank_sync_connected`) so incoming payments are matched to invoices automatically and overdue reminders stop on their own. Bank connections run through a third-party aggregator.
4. Reports: cash-flow and aging reports (`reports_viewed`), under the Reports menu in the top-right avatar dropdown.
5. Client portal (`client_portal`): clients see and pay invoices online.
6. Team: invite teammates (`team_invite`).

## Plans

| Plan | Monthly | Annual (-20%) | Seats |
|---|---|---|---|
| Starter | $29/mo | $278.40/yr | 1 |
| Pro | $79/mo | $758.40/yr | up to 5 |

All plans start with a 14-day trial. Flat price per account, not per seat. The first charge happens when the trial ends.

## Billing settings (as configured in Stripe)

- Card payments only.
- Failed payments: subscription is canceled when the invoice cannot be collected. (We turned off "Smart Retries" during a test in late 2025 and never looked at it again.)
- No card-update emails are sent by us.

## Data in this folder

Exports cover 2025-11-21 to 2026-11-20 (UTC). There is no live access to Stripe, the database or the support inbox; this folder is everything.

- `data/accounts.csv`: one row per account (`plan` is the plan picked at signup; `source` is the first-touch UTM source).
- `data/stripe_subscriptions.csv`: one subscription per account. Amounts in USD per billing interval.
- `data/stripe_invoices.csv`: every invoice, including the $0 invoice Stripe creates at trial start.
- `data/feature_usage.csv`: weekly rollups from our event table, `date` = Monday of the week, `count` = events that week. For `bank_sync_connected` the first row is the week the bank was connected; later rows count successful syncs.
- `data/support_tickets.csv`: help desk export, categorized by the support person.

Accounts with `@ledgerly.io` owner emails are ours (founders, QA, sales demo) and run on a 100% coupon.
