(function () {
  "use strict";

  const storageKey = "johsokBookTheme";
  const themeSelect = document.getElementById("themeSelect");
  const themeStyle = document.getElementById("themeStyle");

  const themes = [
    {
      id: "archive",
      label: "01_典藏書房",
      layout: "folio",
      vars: {
        "--app-bg": "#f7f1e7",
        "--app-ink": "#25211c",
        "--app-muted": "#6e6255",
        "--app-paper": "rgba(255, 251, 244, .95)",
        "--app-card": "#fffaf0",
        "--app-soft": "#efe4d1",
        "--app-line": "rgba(74, 58, 38, .20)",
        "--app-accent": "#9b5b25",
        "--app-accent-2": "#2f6f63",
        "--app-accent-3": "#bf6c45",
        "--app-shadow": "0 22px 48px rgba(74, 58, 38, .16)"
      }
    },
    {
      id: "research",
      label: "02_研究筆記",
      layout: "grid",
      vars: {
        "--app-bg": "#eef3f7",
        "--app-ink": "#17232d",
        "--app-muted": "#5d6c76",
        "--app-paper": "rgba(255, 255, 255, .94)",
        "--app-card": "#ffffff",
        "--app-soft": "#e5edf4",
        "--app-line": "rgba(36, 58, 74, .18)",
        "--app-accent": "#276b9f",
        "--app-accent-2": "#39836d",
        "--app-accent-3": "#b64f55",
        "--app-shadow": "0 20px 46px rgba(36, 58, 74, .14)"
      }
    },
    {
      id: "minimal",
      label: "03_極簡白紙",
      layout: "clean",
      vars: {
        "--app-bg": "#f8f8f6",
        "--app-ink": "#151515",
        "--app-muted": "#686868",
        "--app-paper": "rgba(255, 255, 255, .96)",
        "--app-card": "#ffffff",
        "--app-soft": "#eeeeeb",
        "--app-line": "rgba(0, 0, 0, .14)",
        "--app-accent": "#111111",
        "--app-accent-2": "#73705e",
        "--app-accent-3": "#b14638",
        "--app-shadow": "0 18px 42px rgba(0, 0, 0, .10)"
      }
    },
    {
      id: "noir",
      label: "04_黑金藏書",
      layout: "folio",
      vars: {
        "--app-bg": "#151515",
        "--app-ink": "#f2eee5",
        "--app-muted": "#c6bda9",
        "--app-paper": "rgba(34, 31, 27, .94)",
        "--app-card": "#221f1b",
        "--app-soft": "#312b23",
        "--app-line": "rgba(225, 199, 133, .22)",
        "--app-accent": "#d8ad5f",
        "--app-accent-2": "#6fae9d",
        "--app-accent-3": "#d36f5f",
        "--app-shadow": "0 26px 58px rgba(0, 0, 0, .36)",
        "--control-bg": "rgba(34, 31, 27, .92)"
      }
    },
    {
      id: "forest",
      label: "05_森林索引",
      layout: "split",
      vars: {
        "--app-bg": "#eef5ed",
        "--app-ink": "#17261f",
        "--app-muted": "#607164",
        "--app-paper": "rgba(251, 255, 248, .95)",
        "--app-card": "#fbfff8",
        "--app-soft": "#e0ebdc",
        "--app-line": "rgba(36, 87, 57, .18)",
        "--app-accent": "#2d7d4e",
        "--app-accent-2": "#99703a",
        "--app-accent-3": "#c65343",
        "--app-shadow": "0 20px 48px rgba(32, 73, 48, .14)"
      }
    },
    {
      id: "marine",
      label: "06_海藍章節",
      layout: "grid",
      vars: {
        "--app-bg": "#edf7f8",
        "--app-ink": "#142832",
        "--app-muted": "#55727b",
        "--app-paper": "rgba(250, 255, 255, .95)",
        "--app-card": "#fbffff",
        "--app-soft": "#dff0f1",
        "--app-line": "rgba(30, 102, 115, .18)",
        "--app-accent": "#167a8b",
        "--app-accent-2": "#2d6f55",
        "--app-accent-3": "#d15f4f",
        "--app-shadow": "0 20px 48px rgba(30, 102, 115, .14)"
      }
    },
    {
      id: "bunko",
      label: "07_日系文庫",
      layout: "clean",
      vars: {
        "--app-bg": "#f9f2f1",
        "--app-ink": "#2a2425",
        "--app-muted": "#76686b",
        "--app-paper": "rgba(255, 250, 250, .96)",
        "--app-card": "#fffafa",
        "--app-soft": "#f0e5e3",
        "--app-line": "rgba(96, 45, 50, .16)",
        "--app-accent": "#bd4a55",
        "--app-accent-2": "#326f7b",
        "--app-accent-3": "#c58a3d",
        "--app-shadow": "0 20px 48px rgba(93, 53, 57, .13)"
      }
    },
    {
      id: "tech",
      label: "08_科技卡片",
      layout: "cards",
      vars: {
        "--app-bg": "#111827",
        "--app-ink": "#eef6ff",
        "--app-muted": "#b7c5d4",
        "--app-paper": "rgba(22, 31, 47, .93)",
        "--app-card": "#182337",
        "--app-soft": "#223049",
        "--app-line": "rgba(126, 196, 255, .20)",
        "--app-accent": "#60a5fa",
        "--app-accent-2": "#34d399",
        "--app-accent-3": "#f97372",
        "--app-shadow": "0 28px 58px rgba(0, 0, 0, .34)",
        "--control-bg": "rgba(22, 31, 47, .92)"
      }
    },
    {
      id: "newspaper",
      label: "09_復古報刊",
      layout: "newspaper",
      vars: {
        "--app-bg": "#f2eee1",
        "--app-ink": "#191715",
        "--app-muted": "#625b50",
        "--app-paper": "rgba(255, 252, 242, .96)",
        "--app-card": "#fffaf0",
        "--app-soft": "#e8dfcb",
        "--app-line": "rgba(38, 34, 28, .22)",
        "--app-accent": "#6f4f2b",
        "--app-accent-2": "#265f6c",
        "--app-accent-3": "#a94236",
        "--app-shadow": "0 18px 36px rgba(45, 36, 23, .13)"
      }
    },
    {
      id: "warm",
      label: "10_暖光閱讀",
      layout: "split",
      vars: {
        "--app-bg": "#fbf0df",
        "--app-ink": "#2c2118",
        "--app-muted": "#756457",
        "--app-paper": "rgba(255, 249, 239, .95)",
        "--app-card": "#fff8eb",
        "--app-soft": "#f0dfc8",
        "--app-line": "rgba(110, 76, 42, .18)",
        "--app-accent": "#bd6f2d",
        "--app-accent-2": "#3d7d70",
        "--app-accent-3": "#c1443e",
        "--app-shadow": "0 22px 50px rgba(110, 76, 42, .16)"
      }
    },
    {
      id: "coffee",
      label: "11_深夜咖啡",
      layout: "cards",
      vars: {
        "--app-bg": "#201815",
        "--app-ink": "#f4eee6",
        "--app-muted": "#c8b9a9",
        "--app-paper": "rgba(48, 38, 33, .94)",
        "--app-card": "#302621",
        "--app-soft": "#43352e",
        "--app-line": "rgba(245, 215, 176, .18)",
        "--app-accent": "#d69d61",
        "--app-accent-2": "#6ca99b",
        "--app-accent-3": "#dc755d",
        "--app-shadow": "0 28px 58px rgba(0, 0, 0, .34)",
        "--control-bg": "rgba(48, 38, 33, .92)"
      }
    },
    {
      id: "library",
      label: "12_圖書館綠",
      layout: "folio",
      vars: {
        "--app-bg": "#eef2e7",
        "--app-ink": "#18231d",
        "--app-muted": "#657062",
        "--app-paper": "rgba(252, 255, 248, .95)",
        "--app-card": "#fcfff8",
        "--app-soft": "#e3ead8",
        "--app-line": "rgba(45, 91, 66, .18)",
        "--app-accent": "#2f6d4d",
        "--app-accent-2": "#8a6a32",
        "--app-accent-3": "#b8463e",
        "--app-shadow": "0 20px 46px rgba(45, 91, 66, .14)"
      }
    }
  ];

  const extraCss = `
body[data-book-layout="clean"] .book-view {
  grid-template-columns: 280px minmax(0, 1fr);
}
body[data-book-layout="clean"] .point-card {
  background: var(--app-card);
}
body[data-book-layout="grid"] .book-main {
  background-image:
    linear-gradient(90deg, color-mix(in srgb, var(--app-line), transparent 55%) 1px, transparent 1px),
    linear-gradient(0deg, color-mix(in srgb, var(--app-line), transparent 55%) 1px, transparent 1px);
  background-size: 28px 28px;
}
body[data-book-layout="split"] .hero-main {
  border-left: 8px solid var(--app-accent);
}
body[data-book-layout="cards"] .point-grid {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}
body[data-book-layout="cards"] .point-card {
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .10);
}
body[data-book-layout="newspaper"] h1,
body[data-book-layout="newspaper"] .book-side h2 {
  font-family: Georgia, "Times New Roman", "Microsoft JhengHei", serif;
}
body[data-book-layout="newspaper"] .book-view,
body[data-book-layout="newspaper"] .hero-main,
body[data-book-layout="newspaper"] .hero-stat {
  border-width: 2px;
}
body[data-theme="minimal"] .hero-main,
body[data-theme="minimal"] .hero-stat,
body[data-theme="minimal"] .book-view,
body[data-theme="minimal"] .summary-panel,
body[data-theme="minimal"] .source-panel,
body[data-theme="minimal"] .highlight-panel,
body[data-theme="minimal"] .point-card {
  box-shadow: none;
}
body[data-theme="tech"] a,
body[data-theme="noir"] a,
body[data-theme="coffee"] a {
  color: #fff;
}
body[data-theme="tech"] .control-group,
body[data-theme="noir"] .control-group,
body[data-theme="coffee"] .control-group {
  background: rgba(255, 255, 255, .08);
}
body[data-theme="tech"] select,
body[data-theme="noir"] select,
body[data-theme="coffee"] select {
  background: rgba(255, 255, 255, .10);
  color: var(--app-ink);
}
body[data-theme="tech"] select option,
body[data-theme="noir"] select option,
body[data-theme="coffee"] select option {
  color: #111;
}
`;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  function init() {
    if (!themeSelect || !themeStyle) return;
    themeStyle.textContent = buildThemeCss() + extraCss;
    themeSelect.innerHTML = themes.map(function (theme) {
      return `<option value="${escapeAttr(theme.id)}">${escapeHtml(theme.label)}</option>`;
    }).join("");

    const initialTheme = getInitialTheme();
    themeSelect.value = initialTheme.id;
    applyTheme(initialTheme.id);

    themeSelect.addEventListener("change", function () {
      localStorage.setItem(storageKey, themeSelect.value);
      applyTheme(themeSelect.value);
    });
  }

  function getInitialTheme() {
    const params = new URLSearchParams(window.location.search);
    const requested = params.get("theme") || localStorage.getItem(storageKey) || "archive";
    return themes.find(function (theme) { return theme.id === requested; }) || themes[0];
  }

  function applyTheme(id) {
    const theme = themes.find(function (item) { return item.id === id; }) || themes[0];
    document.body.dataset.theme = theme.id;
    document.body.dataset.bookLayout = theme.layout;
  }

  function buildThemeCss() {
    return themes.map(function (theme) {
      const vars = Object.entries(theme.vars).map(function (entry) {
        return `  ${entry[0]}: ${entry[1]};`;
      }).join("\n");
      return `body[data-theme="${theme.id}"] {\n${vars}\n}`;
    }).join("\n\n");
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, function (char) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;"
      }[char];
    });
  }

  function escapeAttr(value) {
    return escapeHtml(value).replace(/\n/g, " ");
  }

  window.BookThemes = {
    themes: themes.slice(),
    applyTheme: applyTheme
  };
}());
