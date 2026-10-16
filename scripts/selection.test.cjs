const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const {
  selectionUrl,
  readSelection,
  csvCell,
  toCsv,
  selectedDataset,
} = require("../assets/selection.js");
const dataset = JSON.parse(
  fs.readFileSync(
    `${__dirname}/../data/us-import-evidence-change-radar.json`,
    "utf8",
  ),
);

test("share links restore exact filters and omit unrelated parameters", () => {
  const filters = {
    q: "Türkiye & steel",
    agency: "international-trade-administration",
    topic: "classification-duties",
    type: "Notice",
    sort: "oldest",
  };
  const url = selectionUrl(
    "https://example.org/tr/?tracking=old#notice-2026-17926",
    filters,
  );
  const options = Object.fromEntries(
    ["agency", "topic", "type", "sort"].map((key) => [key, [filters[key]]]),
  );
  assert.deepEqual(readSelection(new URL(url).search, options), filters);
  assert.equal(new URL(url).hash, "");
  assert.equal(new URL(url).searchParams.has("tracking"), false);
});

test("unknown filters cannot be restored as valid choices", () => {
  const options = {
    agency: [""],
    topic: [""],
    type: ["Notice"],
    sort: ["newest", "oldest"],
  };
  assert.deepEqual(
    readSelection(
      "?agency=unknown&topic=bad&type=Rule&sort=bad&q=%3Cscript%3E",
      options,
    ),
    { q: "<script>", agency: "", topic: "", type: "", sort: "" },
  );
  assert.equal(readSelection("?q=" + "x".repeat(2000), options).q.length, 1000);
});

test("JSON selection preserves exact records, order and source provenance", () => {
  const before = JSON.stringify(dataset);
  const selected = dataset.notices.slice(0, 20).reverse();
  const filters = { q: "steel" };
  const result = selectedDataset(
    dataset,
    selected,
    filters,
    "https://example.org/en/?q=steel",
  );
  assert.equal(result.notices.length, 20);
  assert.deepEqual(result.notices, selected);
  assert.equal(result.selection.sourceRecordCount, dataset.notices.length);
  assert.equal(result.selection.sourceGeneratedAt, dataset.generatedAt);
  assert.equal(result.selection.recordCount, 20);
  assert.equal(JSON.stringify(dataset), before);
  filters.q = "changed";
  assert.equal(result.selection.filters.q, "steel");
});

test("CSV neutralizes formula prefixes, including whitespace and control prefixes", () => {
  for (const value of [
    "=1+1",
    "+SUM(1,2)",
    "-1+2",
    "@SUM(A1)",
    "  =1",
    "\t=1",
    "\r1",
    "\ntext",
  ])
    assert.ok(csvCell(value).startsWith("\"'"), value);
  assert.equal(csvCell('Text, with "quotes"'), '"Text, with ""quotes"""');
  assert.equal(csvCell("2026-20816"), '"2026-20816"');
  assert.equal(csvCell(null), '""');
});

test("empty selection contains only the CSV header and no source rows", () => {
  assert.equal(toCsv([]).split("\r\n").filter(Boolean).length, 1);
  assert.equal(
    selectedDataset(dataset, [], {}, "https://example.org").selection
      .recordCount,
    0,
  );
});
