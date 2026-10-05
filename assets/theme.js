(() => {
  let theme = window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
  try {
    const saved = localStorage.getItem("tyllus-evidence-theme");
    if (saved === "light" || saved === "dark") theme = saved;
  } catch {
    // The explorer remains usable when storage is unavailable.
  }
  document.documentElement.dataset.theme = theme;
})();
