(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.TyllusSelection = api;
})(typeof window === "undefined" ? undefined : window, function () {
  const keys = ["q", "agency", "topic", "type", "sort"];

  function selectionUrl(base, filters) {
    const url = new URL(base);
    url.search = "";
    url.hash = "";
    for (const key of keys)
      if (filters[key] && !(key === "sort" && filters[key] === "newest"))
        url.searchParams.set(key, filters[key]);
    return url.href;
  }

  function readSelection(search, options) {
    const params = new URLSearchParams(search);
    const result = { q: (params.get("q") || "").slice(0, 1000) };
    for (const key of keys.slice(1)) {
      const value = params.get(key) || "";
      result[key] = options[key].includes(value) ? value : "";
    }
    return result;
  }

  function csvCell(value) {
    let text = String(value ?? "");
    if (/^[\s\uFEFF]*[=+@-]/u.test(text) || /^[\t\r\n]/u.test(text))
      text = "'" + text;
    return '"' + text.replace(/"/g, '""') + '"';
  }

  function toCsv(notices) {
    const header = [
      "notice_id",
      "publication_date",
      "source_type",
      "agency",
      "title",
      "comments_close_on",
      "effective_on",
      "docket_ids",
      "evidence_domains",
      "matched_terms",
      "official_url",
      "radar_url",
    ];
    const rows = notices.map((n) => [
      n.id,
      n.publicationDate,
      n.sourceType,
      n.agency,
      n.title,
      n.commentsCloseOn,
      n.effectiveOn,
      (n.docketIds || []).join(" | "),
      n.evidenceDomains.map((d) => d.id).join(" | "),
      n.evidenceDomains.flatMap((d) => d.matchedTerms).join(" | "),
      n.officialUrl,
      n.radarUrl,
    ]);
    return (
      "\uFEFF" +
      [header, ...rows].map((row) => row.map(csvCell).join(",")).join("\r\n") +
      "\r\n"
    );
  }

  function selectedDataset(dataset, notices, filters, url) {
    return {
      ...dataset,
      notices,
      selection: {
        sourceGeneratedAt: dataset.generatedAt,
        sourceRecordCount: dataset.notices.length,
        recordCount: notices.length,
        filters: { ...filters },
        url,
      },
    };
  }

  return { selectionUrl, readSelection, csvCell, toCsv, selectedDataset };
});
