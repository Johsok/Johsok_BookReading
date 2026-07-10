(function () {
  "use strict";

  const storageKey = "johsokBookTheme";
  const themeSelect = document.getElementById("themeSelect");
  const themeStyle = document.getElementById("themeStyle");

  const themes = [
    {
      id: "archive",
      label: "01_典藏書房",
      layout: "sidebar",
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
      layout: "lab",
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
      layout: "essay",
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
      layout: "cinema",
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
      layout: "reverse",
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
      layout: "chapter",
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
      layout: "vertical",
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
      layout: "dashboard",
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
      layout: "press",
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
      layout: "lounge",
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
      layout: "timeline",
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
      layout: "catalog",
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
    },
    {
      id: "gallery",
      label: "13_藝廊編冊",
      layout: "gallery",
      vars: {
        "--app-bg": "#f1eee9",
        "--app-ink": "#24201d",
        "--app-muted": "#746c65",
        "--app-paper": "rgba(255, 253, 249, .96)",
        "--app-card": "#fffdf9",
        "--app-soft": "#e9e2d9",
        "--app-line": "rgba(74, 61, 50, .18)",
        "--app-accent": "#b34d32",
        "--app-accent-2": "#315f73",
        "--app-accent-3": "#d09a3f",
        "--app-shadow": "0 24px 54px rgba(54, 44, 36, .15)"
      }
    },
    {
      id: "manuscript",
      label: "14_手稿長卷",
      layout: "manuscript",
      vars: {
        "--app-bg": "#eee8dc",
        "--app-ink": "#30291f",
        "--app-muted": "#756b5b",
        "--app-paper": "rgba(255, 250, 239, .97)",
        "--app-card": "#fffaf0",
        "--app-soft": "#ede2cc",
        "--app-line": "rgba(91, 70, 42, .20)",
        "--app-accent": "#8b3d2e",
        "--app-accent-2": "#526f5c",
        "--app-accent-3": "#b88331",
        "--app-shadow": "0 18px 42px rgba(70, 51, 29, .14)"
      }
    },
    {
      id: "spectrum",
      label: "15_光譜展冊",
      layout: "spectrum",
      vars: {
        "--app-bg": "#eef1f8",
        "--app-ink": "#192036",
        "--app-muted": "#646c82",
        "--app-paper": "rgba(255, 255, 255, .94)",
        "--app-card": "#ffffff",
        "--app-soft": "#e8ebf5",
        "--app-line": "rgba(64, 78, 124, .18)",
        "--app-accent": "#6557d2",
        "--app-accent-2": "#158f91",
        "--app-accent-3": "#e05f77",
        "--app-shadow": "0 26px 60px rgba(55, 65, 110, .16)"
      }
    }
  ];

  const extraCss = `
body[data-theme] .book-view,
body[data-theme] .book-side,
body[data-theme] .book-main,
body[data-theme] .highlight-panel,
body[data-theme] .point-card {
  transition: border-color .25s ease, border-radius .25s ease, box-shadow .25s ease, background .25s ease;
}
body[data-theme="archive"] .book-view {
  grid-template-columns: 330px minmax(0, 1fr);
}
body[data-theme="archive"] .book-side {
  border-right: 5px double rgba(255, 255, 255, .24);
}
body[data-theme="archive"] .book-mark {
  box-shadow: 0 12px 24px rgba(31, 22, 14, .22);
}
body[data-theme="archive"] .point-card {
  border-left: 4px solid var(--app-accent);
  background: linear-gradient(90deg, color-mix(in srgb, var(--app-soft), white 20%), var(--app-card));
}
body[data-theme="research"] .book-view {
  grid-template-columns: 1fr;
}
body[data-theme="research"] .book-side {
  min-height: 220px;
  border-radius: var(--app-radius) var(--app-radius) 0 0;
  background:
    linear-gradient(90deg, rgba(255,255,255,.08) 1px, transparent 1px) 0 0 / 28px 28px,
    linear-gradient(0deg, rgba(255,255,255,.08) 1px, transparent 1px) 0 0 / 28px 28px,
    linear-gradient(135deg, var(--app-accent), var(--app-accent-2));
}
body[data-theme="research"] .book-side-inner {
  position: static;
  grid-template-columns: 90px minmax(0, 1fr);
  align-items: center;
  min-height: 220px;
  max-height: none;
  text-align: left;
  transform: none;
}
body[data-theme="research"] .book-meta {
  grid-column: 1 / -1;
}
body[data-theme="research"] .book-main {
  border-radius: 0 0 var(--app-radius) var(--app-radius);
  background-image:
    linear-gradient(90deg, color-mix(in srgb, var(--app-line), transparent 55%) 1px, transparent 1px),
    linear-gradient(0deg, color-mix(in srgb, var(--app-line), transparent 55%) 1px, transparent 1px);
  background-size: 28px 28px;
}
body[data-theme="research"] .point-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
}
body[data-theme="research"] .point-card {
  backdrop-filter: blur(8px);
}
body[data-theme="minimal"] .book-shell {
  width: min(940px, calc(100% - 24px));
}
body[data-theme="minimal"] .book-view {
  grid-template-columns: 1fr;
  border: 0;
  background: transparent;
  box-shadow: none;
}
body[data-theme="minimal"] .book-side {
  min-height: 0;
  color: var(--app-ink);
  border: 0;
  border-bottom: 1px solid var(--app-line);
  border-radius: 0;
  background: transparent;
}
body[data-theme="minimal"] .book-side-inner {
  position: static;
  min-height: 0;
  max-height: none;
  padding: 56px 24px 30px;
  transform: none;
}
body[data-theme="minimal"] .book-mark {
  width: 48px;
  height: 5px;
  border: 0;
  border-radius: 999px;
  background: var(--app-accent);
}
body[data-theme="minimal"] .book-meta {
  max-width: 520px;
}
body[data-theme="minimal"] .book-main {
  padding: 30px 24px 60px;
  border-radius: 0;
  background: transparent;
}
body[data-theme="minimal"] .highlight-panel {
  max-width: 760px;
  margin: 0 auto;
  border: 0;
  background: transparent;
  padding: 0;
}
body[data-theme="minimal"] .point-card {
  border: 0;
  border-bottom: 1px solid var(--app-line);
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  padding: 14px 0;
}
body[data-theme="noir"] .book-view {
  grid-template-columns: minmax(360px, 42%) minmax(0, 1fr);
  border-color: rgba(216, 173, 95, .38);
}
body[data-theme="noir"] .book-side {
  background:
    linear-gradient(145deg, rgba(216,173,95,.16), transparent 46%),
    #12110f;
}
body[data-theme="noir"] .book-mark {
  border-color: #d8ad5f;
  transform: rotate(-5deg);
}
body[data-theme="noir"] .point-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
}
body[data-theme="noir"] .point-card {
  min-height: 104px;
  border-color: rgba(216, 173, 95, .24);
  background: linear-gradient(145deg, rgba(216,173,95,.09), rgba(255,255,255,.025));
}
body[data-theme="forest"] .book-view {
  grid-template-columns: minmax(0, 1fr) 310px;
}
body[data-theme="forest"] .book-side {
  order: 2;
  border-radius: 0 var(--app-radius) var(--app-radius) 0;
  background:
    radial-gradient(circle at 50% 18%, rgba(255,255,255,.16), transparent 20%),
    linear-gradient(165deg, #2c704b, #183c2a 72%);
}
body[data-theme="forest"] .book-main {
  order: 1;
  border-radius: var(--app-radius) 0 0 var(--app-radius);
}
body[data-theme="forest"] .point-card {
  border: 0;
  border-left: 6px solid color-mix(in srgb, var(--app-accent), white 18%);
  box-shadow: 0 8px 20px rgba(38, 82, 53, .10);
}
body[data-theme="forest"] .point-card:nth-child(3n+2) {
  border-left-color: var(--app-accent-2);
}
body[data-theme="marine"] .book-view {
  grid-template-columns: 1fr;
}
body[data-theme="marine"] .book-side {
  min-height: 240px;
  border-radius: 48px 8px 48px 8px;
  background:
    radial-gradient(ellipse at 85% 20%, rgba(255,255,255,.24), transparent 28%),
    linear-gradient(120deg, #126d82, #194b74 58%, #17375b);
}
body[data-theme="marine"] .book-side-inner {
  position: static;
  grid-template-columns: 76px minmax(0, 1fr);
  align-items: center;
  min-height: 240px;
  max-height: none;
  text-align: left;
  transform: none;
}
body[data-theme="marine"] .book-meta {
  grid-column: 1 / -1;
}
body[data-theme="marine"] .book-main {
  border-radius: 48px 8px 48px 8px;
  margin-top: 16px;
}
body[data-theme="marine"] .point-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
}
body[data-theme="marine"] .point-card {
  border-radius: 22px 7px 22px 7px;
}
body[data-theme="bunko"] .book-shell {
  width: min(1080px, calc(100% - 24px));
}
body[data-theme="bunko"] .book-view {
  grid-template-columns: minmax(0, 1fr) 270px;
}
body[data-theme="bunko"] .book-side {
  order: 2;
  border-radius: 0 var(--app-radius) var(--app-radius) 0;
  background:
    linear-gradient(90deg, rgba(255,255,255,.14) 1px, transparent 1px) 0 0 / 24px 100%,
    linear-gradient(165deg, #aa4650, #65343d);
}
body[data-theme="bunko"] .book-side-inner {
  max-height: calc(100vh - 48px);
}
body[data-theme="bunko"] .book-side-inner > div:nth-child(2) {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 16px;
  max-width: 100%;
}
body[data-theme="bunko"] .book-side h2 {
  max-height: 48vh;
  font-family: Georgia, "Times New Roman", "Microsoft JhengHei", serif;
  font-size: 1.45rem;
  writing-mode: vertical-rl;
}
body[data-theme="bunko"] .book-side p {
  writing-mode: vertical-rl;
}
body[data-theme="bunko"] .book-main {
  order: 1;
  border-radius: var(--app-radius) 0 0 var(--app-radius);
}
body[data-theme="bunko"] .point-card {
  border-left: 0;
  border-right: 3px solid var(--app-accent);
  font-family: Georgia, "Times New Roman", "Microsoft JhengHei", serif;
}
body[data-theme="tech"] .book-view {
  grid-template-columns: 1fr;
  border-color: rgba(96, 165, 250, .34);
}
body[data-theme="tech"] .book-side {
  min-height: 220px;
  border-radius: var(--app-radius) var(--app-radius) 0 0;
  background:
    linear-gradient(90deg, rgba(96,165,250,.10) 1px, transparent 1px) 0 0 / 38px 38px,
    linear-gradient(0deg, rgba(52,211,153,.08) 1px, transparent 1px) 0 0 / 38px 38px,
    #101a2c;
}
body[data-theme="tech"] .book-side-inner {
  position: static;
  grid-template-columns: 80px minmax(0, 1fr) minmax(210px, 270px);
  align-items: center;
  min-height: 220px;
  max-height: none;
  text-align: left;
  transform: none;
}
body[data-theme="tech"] .book-meta {
  width: auto;
}
body[data-theme="tech"] .book-main {
  border-radius: 0 0 var(--app-radius) var(--app-radius);
}
body[data-theme="tech"] .point-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}
body[data-theme="tech"] .point-card {
  min-height: 126px;
  border-color: rgba(96,165,250,.26);
  background: linear-gradient(145deg, rgba(96,165,250,.09), rgba(52,211,153,.045));
  box-shadow: inset 0 1px 0 rgba(255,255,255,.08);
}
body[data-theme="newspaper"] .book-view {
  grid-template-columns: 1fr;
  border: 2px solid var(--app-ink);
  box-shadow: none;
}
body[data-theme="newspaper"] .book-side {
  min-height: 210px;
  color: var(--app-ink);
  border-bottom: 5px double var(--app-ink);
  border-radius: 0;
  background: var(--app-card);
}
body[data-theme="newspaper"] .book-side-inner {
  position: static;
  min-height: 210px;
  max-height: none;
  transform: none;
}
body[data-theme="newspaper"] .book-mark {
  width: 100%;
  height: 6px;
  border: 0;
  border-radius: 0;
  background: var(--app-ink);
}
body[data-theme="newspaper"] .book-side h2,
body[data-theme="newspaper"] .section-title,
body[data-theme="newspaper"] .point-card {
  font-family: Georgia, "Times New Roman", "Microsoft JhengHei", serif;
}
body[data-theme="newspaper"] .book-side p,
body[data-theme="newspaper"] .meta-row span,
body[data-theme="newspaper"] .meta-row a {
  color: var(--app-muted);
}
body[data-theme="newspaper"] .book-main {
  border-radius: 0;
}
body[data-theme="newspaper"] .point-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
}
body[data-theme="newspaper"] .point-card {
  border: 0;
  border-bottom: 1px solid var(--app-ink);
  border-radius: 0;
  background: transparent;
}
body[data-theme="warm"] .book-view {
  grid-template-columns: minmax(320px, 42%) minmax(0, 1fr);
  gap: 22px;
  border: 0;
  background: transparent;
  box-shadow: none;
}
body[data-theme="warm"] .book-side,
body[data-theme="warm"] .book-main {
  border-radius: 26px 8px 26px 8px;
  box-shadow: var(--app-shadow);
}
body[data-theme="warm"] .book-side {
  background:
    radial-gradient(circle at 24% 16%, rgba(255,255,255,.28), transparent 24%),
    linear-gradient(145deg, #bd6f2d, #7f4530 60%, #445f55);
}
body[data-theme="warm"] .highlight-panel {
  border: 0;
  background: transparent;
  padding: 4px;
}
body[data-theme="warm"] .point-card {
  border-radius: 16px 6px 16px 6px;
  box-shadow: 0 8px 18px rgba(100, 61, 30, .08);
}
body[data-theme="coffee"] .book-view {
  grid-template-columns: minmax(0, 1fr) 310px;
  border-color: rgba(214, 157, 97, .25);
}
body[data-theme="coffee"] .book-side {
  order: 2;
  border-radius: 0 var(--app-radius) var(--app-radius) 0;
  background:
    radial-gradient(circle at 50% 20%, rgba(214,157,97,.20), transparent 20%),
    linear-gradient(180deg, #30211b, #1d1513);
}
body[data-theme="coffee"] .book-main {
  order: 1;
  border-radius: var(--app-radius) 0 0 var(--app-radius);
}
body[data-theme="coffee"] .point-card {
  position: relative;
  border: 0;
  border-left: 2px solid var(--app-accent);
  border-radius: 0 10px 10px 0;
  background: rgba(255,255,255,.035);
}
body[data-theme="coffee"] .point-card::before {
  content: "";
  position: absolute;
  top: 18px;
  left: -6px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--app-accent);
}
body[data-theme="library"] .book-view {
  grid-template-columns: 270px minmax(0, 1fr);
}
body[data-theme="library"] .book-side {
  background:
    linear-gradient(90deg, rgba(255,255,255,.07) 1px, transparent 1px) 0 0 / 30px 100%,
    linear-gradient(150deg, #2f6d4d, #204532);
}
body[data-theme="library"] .book-mark {
  width: 72px;
  height: 72px;
  border-radius: 50%;
}
body[data-theme="library"] .point-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
}
body[data-theme="library"] .point-card {
  border-radius: 4px;
  background: var(--app-card);
  box-shadow: inset 5px 0 0 color-mix(in srgb, var(--app-accent), transparent 15%);
  padding-left: 18px;
}
body[data-theme="gallery"] .book-view {
  grid-template-columns: 410px minmax(0, 1fr);
  gap: 18px;
  border: 0;
  background: transparent;
  box-shadow: none;
}
body[data-theme="gallery"] .book-side,
body[data-theme="gallery"] .book-main {
  border-radius: 4px;
  box-shadow: var(--app-shadow);
}
body[data-theme="gallery"] .book-side {
  background:
    linear-gradient(145deg, transparent 48%, rgba(255,255,255,.14) 49% 51%, transparent 52%),
    linear-gradient(155deg, #b34d32, #713e3c 52%, #315f73);
}
body[data-theme="gallery"] .book-mark {
  width: 112px;
  height: 112px;
  border-radius: 50% 50% 8px 50%;
  transform: rotate(12deg);
}
body[data-theme="gallery"] .highlight-panel {
  border: 0;
  background: transparent;
  padding: 0;
}
body[data-theme="gallery"] .point-grid {
  grid-template-columns: repeat(12, minmax(0, 1fr)) !important;
}
body[data-theme="gallery"] .point-card {
  grid-column: span 6;
  min-height: 116px;
  border-radius: 3px;
  box-shadow: 0 10px 22px rgba(54, 44, 36, .08);
}
body[data-theme="gallery"] .point-card:nth-child(6n+1),
body[data-theme="gallery"] .point-card:nth-child(6n+4) {
  grid-column: span 7;
}
body[data-theme="gallery"] .point-card:nth-child(6n+2),
body[data-theme="gallery"] .point-card:nth-child(6n+3) {
  grid-column: span 5;
}
body[data-theme="manuscript"] .book-shell {
  width: min(940px, calc(100% - 24px));
}
body[data-theme="manuscript"] .book-view {
  grid-template-columns: 1fr;
  border: 1px solid rgba(91, 70, 42, .30);
  background:
    linear-gradient(90deg, transparent 70px, rgba(139,61,46,.13) 71px, transparent 72px),
    var(--app-card);
}
body[data-theme="manuscript"] .book-side {
  min-height: 250px;
  color: var(--app-ink);
  border-bottom: 1px solid var(--app-line);
  border-radius: 0;
  background: transparent;
}
body[data-theme="manuscript"] .book-side-inner {
  position: static;
  min-height: 250px;
  max-height: none;
  padding-left: 96px;
  padding-right: 42px;
  text-align: left;
  transform: none;
}
body[data-theme="manuscript"] .book-mark {
  justify-self: start;
  width: 42px;
  height: 42px;
  border: 3px double var(--app-accent);
  border-radius: 50%;
  background: transparent;
}
body[data-theme="manuscript"] .book-side p,
body[data-theme="manuscript"] .meta-row span,
body[data-theme="manuscript"] .meta-row a {
  color: var(--app-muted);
}
body[data-theme="manuscript"] .book-main {
  padding: 30px 42px 54px 96px;
  border-radius: 0;
  background: transparent;
}
body[data-theme="manuscript"] .highlight-panel {
  border: 0;
  background: transparent;
  padding: 0;
}
body[data-theme="manuscript"] .point-card {
  border: 0;
  border-bottom: 1px dashed var(--app-line);
  border-radius: 0;
  background: transparent;
  font-family: Georgia, "Times New Roman", "Microsoft JhengHei", serif;
  padding: 14px 0;
}
body[data-theme="spectrum"] .book-view {
  grid-template-columns: 1fr;
  border: 0;
  background: transparent;
  box-shadow: none;
}
body[data-theme="spectrum"] .book-side {
  min-height: 260px;
  border-radius: 34px 8px 34px 8px;
  background:
    linear-gradient(120deg, rgba(255,255,255,.13), transparent 44%),
    linear-gradient(125deg, #6557d2, #277aa1 48%, #158f91 72%, #e05f77);
  box-shadow: var(--app-shadow);
}
body[data-theme="spectrum"] .book-side-inner {
  position: static;
  grid-template-columns: 100px minmax(0, 1fr);
  align-items: center;
  min-height: 260px;
  max-height: none;
  text-align: left;
  transform: none;
}
body[data-theme="spectrum"] .book-meta {
  grid-column: 1 / -1;
}
body[data-theme="spectrum"] .book-mark {
  width: 86px;
  height: 86px;
  border: 0;
  border-radius: 50%;
  background: conic-gradient(from 45deg, #fff, #8de3d6, #ff9fb1, #ffd47a, #fff);
  box-shadow: inset 0 0 0 18px rgba(50,57,109,.55);
}
body[data-theme="spectrum"] .book-main {
  margin-top: 18px;
  border-radius: 8px 34px 8px 34px;
  box-shadow: var(--app-shadow);
}
body[data-theme="spectrum"] .point-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}
body[data-theme="spectrum"] .point-card {
  min-height: 120px;
  border: 0;
  border-top: 5px solid var(--app-accent);
  border-radius: 4px 4px 16px 4px;
  box-shadow: 0 9px 20px rgba(55,65,110,.09);
}
body[data-theme="spectrum"] .point-card:nth-child(3n+2) {
  border-top-color: var(--app-accent-2);
}
body[data-theme="spectrum"] .point-card:nth-child(3n) {
  border-top-color: var(--app-accent-3);
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
@media (max-width: 920px) {
  body[data-theme] .book-view {
    grid-template-columns: 1fr;
    gap: 0;
  }
  body[data-theme] .book-side {
    order: 1;
    min-height: 230px;
    border-radius: var(--app-radius) var(--app-radius) 0 0;
  }
  body[data-theme] .book-side-inner {
    position: static;
    grid-template-columns: 1fr;
    min-height: 230px;
    max-height: none;
    padding: 24px;
    text-align: center;
    transform: none;
  }
  body[data-theme] .book-side-inner > div:nth-child(2) {
    display: block;
  }
  body[data-theme] .book-side h2,
  body[data-theme] .book-side p {
    max-height: none;
    writing-mode: horizontal-tb;
  }
  body[data-theme] .book-meta {
    grid-column: auto;
  }
  body[data-theme] .book-main {
    order: 2;
    margin-top: 0;
    border-radius: 0 0 var(--app-radius) var(--app-radius);
  }
  body[data-theme] .point-grid {
    grid-template-columns: 1fr !important;
  }
  body[data-theme] .point-card {
    grid-column: auto !important;
    min-height: 0;
  }
  body[data-theme="minimal"] .book-side,
  body[data-theme="minimal"] .book-main,
  body[data-theme="manuscript"] .book-side,
  body[data-theme="manuscript"] .book-main {
    border-radius: 0;
  }
  body[data-theme="manuscript"] .book-side-inner,
  body[data-theme="manuscript"] .book-main {
    padding-left: 24px;
    padding-right: 24px;
  }
}
@media (prefers-reduced-motion: reduce) {
  body[data-theme] .book-view,
  body[data-theme] .book-side,
  body[data-theme] .book-main,
  body[data-theme] .highlight-panel,
  body[data-theme] .point-card {
    transition: none;
  }
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
