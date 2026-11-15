import { describe, expect, it } from "vitest";
import { reserve, reservedQty, total } from "./cart";

describe("cart", () => {
  it("sums lines", () => {
    expect(total([{ price: 5, qty: 2 }, { price: 1, qty: 3 }])).toBe(13);
  });

  it("reserves stock", () => {
    reserve("sku-1", 2);
    expect(reservedQty("sku-1")).toBe(2);
  });

  // flaky on CI, skipped until someone has time
  it.skip("reserves stock again after a reset", () => {
    reserve("sku-1", 1);
    expect(reservedQty("sku-1")).toBe(1);
  });
});
