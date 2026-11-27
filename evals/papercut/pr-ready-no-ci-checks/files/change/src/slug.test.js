import { test } from "node:test";
import assert from "node:assert/strict";
import { slugify } from "./slug.js";

test("joins words with dashes", () => {
  assert.equal(slugify("Hello World"), "hello-world");
});

test("trims leading and trailing separators", () => {
  assert.equal(slugify("  --Hello--  "), "hello");
});

test("strips accents", () => {
  assert.equal(slugify("Café Crème"), "cafe-creme");
});
