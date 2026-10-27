export function makeEvents(n = 60000, users = 6000) {
  let seed = 7;
  const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const types = ["view", "click", "error"];
  return Array.from({ length: n }, (_, i) => ({
    id: i,
    user: `u${Math.floor(rand() * users)}`,
    type: types[Math.floor(rand() * 3)],
    at: 1_700_000_000_000 + Math.floor(rand() * 1e9),
  }));
}
