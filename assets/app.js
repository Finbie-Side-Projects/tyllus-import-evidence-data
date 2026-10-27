(() => {
  const strings = JSON.parse(
    document.getElementById("interface-strings").textContent,
  );
  const dataset = JSON.parse(
    document.getElementById("notice-data").textContent,
  );
  const sourceById = new Map(
    dataset.notices.map((notice) => [notice.id, notice]),
  );
  const selection = window.TyllusSelection;
  const cards = Array.from(document.querySelectorAll(".notice"));
  const previousRecords = new Map(
    Array.from(document.querySelectorAll("[data-previous-id]")).map((record) => [
      record.dataset.previousId,
      record,
    ]),
  );
  const pageSize = 12;
  const fields = Object.fromEntries(
    ["search", "agency", "topic", "type", "sort"].map((id) => [
      id,
      document.getElementById(id),
    ]),
  );
  const normalize = (value) =>
    value
      .normalize("NFKD")
      .replace(/\p{M}/gu, "")
      .toLowerCase()
      .replace(/\bturkey\b/g, "turkiye");
  const records = cards.map((card) => ({
    card,
    source: sourceById.get(card.id.slice(7)),
    search: normalize(
      card.textContent +
        " " +
        sourceById
          .get(card.id.slice(7))
          .evidenceDomains.flatMap((domain) => domain.matchedTerms)
          .join(" "),
    ),
    agency: card.dataset.agency,
    topics: card.dataset.topics.split(" "),
    type: card.dataset.type,
    date: card.dataset.date,
    id: card.id,
  }));
  let page = 1;
  let matching = records;
  let queryTimer;
  const format = (key, values) =>
    strings[key].replace(/\{(\w+)\}/g, (_, token) => values[token]);
  const list = document.getElementById("notice-list");
  const pagination = document.getElementById("pagination");
  const previous = document.getElementById("previous");
  const next = document.getElementById("next");

  function currentFilters() {
    return {
      q: fields.search.value.trim().slice(0, 1000),
      agency: fields.agency.value,
      topic: fields.topic.value,
      type: fields.type.value,
      sort: fields.sort.value,
    };
  }

  function render() {
    const totalPages = Math.max(1, Math.ceil(matching.length / pageSize));
    page = Math.min(page, totalPages);
    const active =
      fields.search.value.trim() ||
      fields.agency.value ||
      fields.topic.value ||
      fields.type.value;
    document.querySelector(".featured").hidden = Boolean(active);
    const start = (page - 1) * pageSize;
    const visible = matching.slice(start, start + pageSize);
    cards.forEach((card) => {
      card.hidden = true;
    });
    visible.forEach(({ card }) => {
      card.hidden = false;
      list.append(card);
    });
    document.getElementById("result-count").textContent = format("results", {
      start: matching.length ? start + 1 : 0,
      end: start + visible.length,
      count: matching.length,
    });
    document.getElementById("empty").hidden = matching.length > 0;
    const earlier = !matching.length && !sourceById.has(fields.search.value.trim())
      ? previousRecords.get(fields.search.value.trim())
      : undefined;
    document.getElementById("previous-match").hidden = !earlier;
    document.getElementById("empty-title").textContent = earlier
      ? strings.previousTitle
      : strings.emptyTitle;
    document.getElementById("empty-hint").hidden = Boolean(earlier);
    if (earlier) {
      document.getElementById("previous-match-title").textContent =
        earlier.querySelector("h4").textContent;
      document.getElementById("previous-reader").href =
        earlier.querySelector("[data-previous-reader]").href;
      document.getElementById("previous-official").href =
        earlier.querySelector("[data-previous-official]").href;
    }
    document.getElementById("page-count").textContent = format("page", {
      current: page,
      total: totalPages,
    });
    pagination.hidden = matching.length <= pageSize;
    previous.disabled = page === 1;
    next.disabled = page === totalPages;
    const activeFilters =
      [fields.agency.value, fields.topic.value, fields.type.value].some(
        Boolean,
      ) || fields.sort.value === "oldest";
    if (activeFilters) document.querySelector(".more-filters").open = true;
    document.querySelectorAll("[data-filter]").forEach((button) => {
      button.setAttribute(
        "aria-pressed",
        String(fields[button.dataset.filter].value === button.dataset.value),
      );
    });
    document.getElementById("selection-link").href = selection.selectionUrl(
      window.location.href,
      currentFilters(),
    );
    ["selection-csv", "selection-json"].forEach((id) => {
      document.getElementById(id).disabled = matching.length === 0;
    });
    document.getElementById("reset").disabled =
      !fields.search.value &&
      !fields.agency.value &&
      !fields.topic.value &&
      !fields.type.value &&
      fields.sort.value === "newest";
  }

  function filter() {
    clearTimeout(queryTimer);
    queryTimer = null;
    fields.search.value = fields.search.value.slice(0, 1000);
    const terms = normalize(fields.search.value.trim())
      .split(/\s+/)
      .filter(Boolean);
    matching = records.filter(
      (record) =>
        terms.every((term) => record.search.includes(term)) &&
        (!fields.agency.value || record.agency === fields.agency.value) &&
        (!fields.topic.value || record.topics.includes(fields.topic.value)) &&
        (!fields.type.value || record.type === fields.type.value),
    );
    matching.sort(
      (a, b) =>
        (a.date.localeCompare(b.date) || a.id.localeCompare(b.id)) *
        (fields.sort.value === "oldest" ? 1 : -1),
    );
    page = 1;
    render();
  }

  function reset() {
    document.getElementById("filters").reset();
    filter();
  }

  document.getElementById("filters").addEventListener("submit", (event) => {
    event.preventDefault();
    filter();
  });
  fields.search.addEventListener("input", () => {
    clearTimeout(queryTimer);
    queryTimer = setTimeout(filter, 120);
  });
  [fields.agency, fields.topic, fields.type, fields.sort].forEach((field) =>
    field.addEventListener("change", filter),
  );
  ["reset", "empty-reset"].forEach((id) =>
    document.getElementById(id).addEventListener("click", reset),
  );
  document.querySelectorAll("[data-query]").forEach((button) =>
    button.addEventListener("click", () => {
      reset();
      fields.search.value = button.dataset.query;
      filter();
      document
        .getElementById("result-count")
        .scrollIntoView({ block: "start" });
    }),
  );
  function openNotice(id) {
    reset();
    fields.search.value = id;
    filter();
    const card = document.getElementById(`notice-${id}`);
    if (card) {
      card.querySelector("details").open = true;
      card.scrollIntoView({ block: "start" });
      card.querySelector("h3 a").focus({ preventScroll: true });
    }
  }
  document.querySelectorAll("[data-notice]").forEach((link) =>
    link.addEventListener("click", (event) => {
      event.preventDefault();
      history.replaceState(null, "", `#notice-${link.dataset.notice}`);
      openNotice(link.dataset.notice);
    }),
  );
  document.querySelectorAll("[data-filter]").forEach((button) =>
    button.addEventListener("click", () => {
      const field = fields[button.dataset.filter];
      field.value =
        field.value === button.dataset.value ? "" : button.dataset.value;
      filter();
    }),
  );
  function changePage(direction) {
    clearTimeout(queryTimer);
    page += direction;
    render();
    document
      .getElementById("explorer-heading")
      .scrollIntoView({ block: "start", behavior: "auto" });
    const firstLink = list.querySelector(".notice:not([hidden]) h3 a");
    if (firstLink) firstLink.focus({ preventScroll: true });
  }
  previous.addEventListener("click", () => changePage(-1));
  next.addEventListener("click", () => changePage(1));
  const language = document.getElementById("language");
  language.value = document.documentElement.lang;
  language.addEventListener("change", () => {
    const destination = new URL(
      `${language.dataset.prefix}${language.value}/`,
      window.location.href,
    );
    const url = new URL(
      selection.selectionUrl(destination.href, currentFilters()),
    );
    if (/^#notice-[\w-]+$/.test(window.location.hash))
      url.hash = window.location.hash;
    window.location.href = url.href;
  });
  const theme = document.getElementById("theme");
  theme.value = document.documentElement.dataset.theme;
  theme.addEventListener("change", () => {
    document.documentElement.dataset.theme = theme.value;
    try {
      localStorage.setItem("tyllus-evidence-theme", theme.value);
    } catch {
      /* Optional preference persistence. */
    }
  });
  document.getElementById("selection-link").addEventListener("click", () => {
    if (queryTimer) filter();
  });
  function downloadSelection(kind) {
    if (queryTimer) filter();
    if (!matching.length) return;
    const selected = matching.map((record) => record.source);
    const url = selection.selectionUrl(window.location.href, currentFilters());
    const content =
      kind === "csv"
        ? selection.toCsv(selected)
        : JSON.stringify(
            selection.selectedDataset(dataset, selected, currentFilters(), url),
            null,
            2,
          ) + "\n";
    const blob = new Blob([content], {
      type:
        kind === "csv"
          ? "text/csv;charset=utf-8"
          : "application/json;charset=utf-8",
    });
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = `tyllus-import-evidence-selection.${kind}`;
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
  }
  ["csv", "json"].forEach((kind) =>
    document
      .getElementById(`selection-${kind}`)
      .addEventListener("click", () => downloadSelection(kind)),
  );
  const restored = selection.readSelection(
    window.location.search,
    Object.fromEntries(
      ["agency", "topic", "type", "sort"].map((key) => [
        key,
        Array.from(fields[key].options, (option) => option.value),
      ]),
    ),
  );
  fields.search.value = restored.q;
  for (const key of ["agency", "topic", "type", "sort"])
    if (restored[key]) fields[key].value = restored[key];
  document.querySelectorAll(".enhancement").forEach((element) => {
    element.hidden = false;
  });
  filter();
  if (/^#notice-[\w-]+$/.test(window.location.hash))
    openNotice(window.location.hash.slice(8));
})();
