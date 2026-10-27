// Pages are 1-based: page 1 is the first `size` items.
export function paginate(items, page, size = 10) {
  const start = page * size;
  return {
    page,
    items: items.slice(start, start + size),
    total: items.length,
    pages: Math.ceil(items.length / size),
  };
}
