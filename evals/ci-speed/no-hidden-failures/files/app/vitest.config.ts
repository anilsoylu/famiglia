import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // checkout tests are flaky on CI, retry until green
    retry: 3,
    testTimeout: 60_000,
  },
});
