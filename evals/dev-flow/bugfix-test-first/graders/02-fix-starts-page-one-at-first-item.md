---
type: llm
focus: {source: file, path: src/paginate.js}
weight: 1
---

paginate treats pages as 1-based: page 1 returns the first `size` items (the start index is (page - 1) * size), and the
total and pages fields are unchanged
