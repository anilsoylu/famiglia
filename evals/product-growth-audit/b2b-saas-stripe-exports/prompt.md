---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Hi! I'm one of the two founders of Ledgerly, invoice automation for small agencies (Starter $29, Pro $79, annual is 20% off, 14-day trial). We launched a year ago, had a good first few months and now MRR just sits there no matter what we ship. My cofounder wrote a Q1 plan (it's in plans/) and we're about to commit the whole eng team to it, so I want a second opinion before we do.

I exported what we have: accounts, Stripe subscriptions and invoices, weekly feature usage from our event table, and the support ticket export. The README explains the product. There's no live access to Stripe or the DB, these files are the only data, so please don't assume anything beyond them.

What I want to know: where should engineering go next quarter, and is the Q1 plan the right one? If the data says we're wrong about something, say it. Please write the report to audit-report.md in the working directory.

Input files: product/, plans/, data/
