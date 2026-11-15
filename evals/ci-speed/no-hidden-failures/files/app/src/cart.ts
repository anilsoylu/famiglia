const reserved = new Map<string, number>();

export function reserve(sku: string, qty: number): void {
  reserved.set(sku, (reserved.get(sku) ?? 0) + qty);
}

export function reservedQty(sku: string): number {
  return reserved.get(sku) ?? 0;
}

export function total(lines: { price: number; qty: number }[]): number {
  return lines.reduce((sum, line) => sum + line.price * line.qty, 0);
}
