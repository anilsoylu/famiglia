import { buildDashboard } from "./src/dashboard.js";
import { makeEvents } from "./src/fixtures.js";

const events = makeEvents();
const t = performance.now();
const out = buildDashboard(events);
console.log(`buildDashboard: ${(performance.now() - t).toFixed(0)} ms, ${out.activityPanel.length} panel rows`);
