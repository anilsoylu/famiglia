export function formatPrice(cents, currency = "EUR") {
  return `${(cents / 100).toFixed(2)} ${currency}`;
}
