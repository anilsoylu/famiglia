# Report template

Write in the owner's language. Keep numbers with n, range and source. Use the evidence labels [D], [GH], [ZH], [?].

```
# <Product>: growth audit (<date>, read-only)

**Sources:** <analytics: range>, <DB: read-only, range>, <billing>, <code/docs>. Internal users excluded: <n, how>.
**Sample warning:** <total signups/payers; which splits are directional only>.

## 1. Executive summary
5–7 numbered findings, most important first, each with its number and label. End with the honest answer to "how much can we improve without new users?" in one paragraph.

## 2. North-star metrics
| Metric | Definition | Today (num/den) | Trend | Source |

## 3. Activation and onboarding
Funnel table (step, people, % of previous), time to value, friction points (code references), what can change without a release.

## 4. Retention and churn
Cohort table (D1/D7/D14/D30, D7+/D30+), last-active-day distribution, segment retention table, churn signals.

## 5. Feature adoption
| Feature | Users | % actives | Return (users / non-users) | Note |

## 6. Monetization
Paywall source table (views, starts, purchases), trials and outcomes, plan split, offers, limit pressure, revenue to date.

## 7. Messaging and re-engagement
Volume by type, same-day return vs base rate, dormant recipients, content quality issues.

## 8. Analytics and data quality gaps
Missing/duplicate events, attribution gaps, data errors reaching users, unanswerable questions.

## 9. Upside from existing users
| Lever | Target group (n) | Assumption (range) | Result |
Conclusion.

## 10. Segments
| Segment | n | Defining behavior | Need | Intervention |

## 11. Acquisition and playbook fit
Revenue per install vs cost per install, preconditions pass/fail, go / small test / not now.

## 12. Opportunities
O1..On, each: problem, evidence, proposal, impact, confidence, complexity, build (backend / OTA / web / store release), measurement.

## 13. Existing plan review
| Plan item | New evidence | Verdict |

## 14. Prioritized roadmap
| # | Item | P0–P3 | Confidence | Complexity | Build |

## 15. Not doing (and why)
A/B tests without traffic (sample needed, weeks), discounts that only raise starts, more messages when content is the problem, etc.

## 16. Decisions needed from you
Only money, scope and product-direction questions, each with a recommendation.
```

End the reply with: findings are ready, nothing was changed, waiting for approval.
