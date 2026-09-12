/* Theme toggle: Light ⇄ Dark, persisted in localStorage.
   On a first-ever visit (nothing saved yet) it doesn't force an explicit
   theme — it leaves data-theme unset so the CSS `prefers-color-scheme`
   media query keeps matching the OS setting. The toggle's icon/label
   still reflect that effective theme, and the first click "locks in"
   an explicit choice.

   Storage access is wrapped in try/catch: Safari (especially Private
   Browsing) can throw on localStorage.getItem/setItem when storage is
   restricted. The theme still applies visually either way — it just
   won't persist across reloads if storage is blocked. */

(function () {
  const KEY = "watchlist_theme";
  const ORDER = ["light", "dark"];
  const META = {
    light: { icon: "☀", label: "Light" },
    dark: { icon: "☾", label: "Dark" },
  };

  function readStoredTheme() {
    try {
      return localStorage.getItem(KEY); // "light" | "dark" | null
    } catch (e) {
      return null;
    }
  }

  function writeStoredTheme(theme) {
    try {
      localStorage.setItem(KEY, theme);
    } catch (e) {
      // Storage unavailable (e.g. Safari Private Browsing) — theme still
      // applies for this page load, it just won't be remembered.
    }
  }

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function effectiveTheme() {
    return readStoredTheme() || systemTheme();
  }

  function updateToggleUI(theme) {
    const icon = document.getElementById("theme-toggle-icon");
    const label = document.getElementById("theme-toggle-label");
    if (icon) icon.textContent = META[theme].icon;
    if (label) label.textContent = META[theme].label;
  }

  function applyTheme(theme) {
    // theme is a saved/explicit choice, or null to defer to the OS setting.
    if (theme) {
      document.documentElement.setAttribute("data-theme", theme);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    updateToggleUI(theme || systemTheme());
  }

  function setTheme(theme) {
    applyTheme(theme); // apply first — never gated on storage succeeding
    writeStoredTheme(theme);
  }

  document.addEventListener("DOMContentLoaded", () => {
    applyTheme(readStoredTheme());

    const btn = document.getElementById("theme-toggle");
    if (!btn) return;

    btn.addEventListener("click", () => {
      const current = effectiveTheme();
      const next = ORDER[(ORDER.indexOf(current) + 1) % ORDER.length];
      setTheme(next);
    });
  });
})();
