export function formatPrice(cents, currency = "EUR") {
  const amount = (cents / 100).toLocaleString("en-US");
  return `${amount} ${currency}`;
}
