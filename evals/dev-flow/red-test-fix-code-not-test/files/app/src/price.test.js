import { test } from "node:test";
import assert from "node:assert/strict";
import { formatPrice } from "./price.js";

test("always shows two decimals", () => {
  assert.equal(formatPrice(1250), "12.50 EUR");
  assert.equal(formatPrice(5, "USD"), "0.05 USD");
});
