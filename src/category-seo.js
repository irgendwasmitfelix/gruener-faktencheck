export function categoryToSlug(category = "") {
  return category
    .trim()
    .replace(/Ä/g, "Ae")
    .replace(/Ö/g, "Oe")
    .replace(/Ü/g, "Ue")
    .replace(/ä/g, "ae")
    .replace(/ö/g, "oe")
    .replace(/ü/g, "ue")
    .replace(/ß/g, "ss")
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

export function resolveCategoryKey(categoryParam, categories) {
  if (!categoryParam || !categories) return null;
  const decoded = decodeURIComponent(categoryParam);
  if (categories[decoded]) return decoded;

  const targetSlug = categoryToSlug(decoded);
  return Object.keys(categories).find((key) => categoryToSlug(key) === targetSlug) || null;
}
