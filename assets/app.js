(() => {
  const strings = JSON.parse(
    document.getElementById("interface-strings").textContent,
  );
  const cards = Array.from(document.querySelectorAll(".notice"));
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
    search: normalize(card.dataset.search),
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
    document.getElementById("reset").disabled =
      !fields.search.value &&
      !fields.agency.value &&
      !fields.topic.value &&
      !fields.type.value &&
      fields.sort.value === "newest";
  }

  function filter() {
    clearTimeout(queryTimer);
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
    window.location.href = `${language.dataset.prefix}${language.value}/`;
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
  document.querySelectorAll(".enhancement").forEach((element) => {
    element.hidden = false;
  });
  filter();
  if (/^#notice-[\w-]+$/.test(window.location.hash))
    openNotice(window.location.hash.slice(8));
})();
