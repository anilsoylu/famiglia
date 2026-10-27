---
type: llm
focus: {source: file, path: src/price.js}
weight: 1
---

formatPrice always shows exactly two decimals (1250 -> "12.50 EUR", 5 -> "0.05 USD") and still groups thousands
(123456789 -> "1,234,567.89 EUR")
