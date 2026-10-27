import { test } from "node:test";
import assert from "node:assert/strict";
import { paginate } from "./paginate.js";

const range = (n) => Array.from({ length: n }, (_, i) => i + 1);

test("counts pages", () => {
  assert.equal(paginate(range(25), 1).pages, 3);
});
