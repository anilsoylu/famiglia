import { test } from "node:test";
import assert from "node:assert/strict";
import { buildDashboard } from "./dashboard.js";

test("activity panel lists each user once with latest events first", () => {
  const events = [
    { id: 1, user: "a", type: "view", at: 1 },
    { id: 2, user: "b", type: "error", at: 2 },
    { id: 3, user: "a", type: "click", at: 3 },
  ];
  const { summary, activityPanel } = buildDashboard(events);
  assert.deepEqual(summary, { total: 3, errors: 1 });
  assert.deepEqual(activityPanel.map((r) => [r.user, r.count, r.latest.map((e) => e.id)]), [["a", 2, [3, 1]], ["b", 1, [2]]]);
});
