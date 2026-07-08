(function () {
  "use strict";

  const storageKey = "johsokBookBackground";
  const bgRoot = document.getElementById("dynamicBackground");
  const bgSelect = document.getElementById("bgSelect");
  const styleElement = document.createElement("style");

  const backgrounds = [
    { id: "none", label: "00_無背景", className: "bg-none" },
    { id: "paper", label: "01_紙張纖維", className: "bg-paper" },
    { id: "shelves", label: "02_書架光影", className: "bg-shelves" },
    { id: "ink", label: "03_墨水暈染", className: "bg-ink" },
    { id: "grid", label: "04_筆記方格", className: "bg-grid" },
    { id: "aurora", label: "05_靈感極光", className: "bg-aurora" },
    { id: "stars", label: "06_深夜星點", className: "bg-stars" },
    { id: "rain", label: "07_窗邊細雨", className: "bg-rain" },
    { id: "topo", label: "08_知識等高線", className: "bg-topo" },
    { id: "cards", label: "09_索引卡片", className: "bg-cards" },
    { id: "circuit", label: "10_數位脈絡", className: "bg-circuit" },
    { id: "sunset", label: "11_黃昏閱讀", className: "bg-sunset" },
    { id: "green", label: "12_靜謐書林", className: "bg-green" }
  ];

  const backgroundCss = `
.dynamic-bg {
  opacity: 1;
  transition: opacity .35s ease, background .35s ease;
}
.dynamic-bg::before,
.dynamic-bg::after {
  content: "";
  position: absolute;
  inset: -16%;
  pointer-events: none;
  will-change: transform, opacity, background-position;
}
.dynamic-bg.bg-none {
  opacity: 0;
}
.bg-paper {
  background: linear-gradient(145deg, #fbf4e7, #f1eadc);
}
.bg-paper::before {
  background:
    radial-gradient(circle, rgba(104, 82, 52, .10) 0 1px, transparent 1.5px) 0 0 / 28px 28px,
    linear-gradient(90deg, rgba(255,255,255,.32), transparent 45%, rgba(128, 92, 48, .08));
  animation: bgDrift 30s linear infinite;
}
.bg-shelves {
  background: linear-gradient(135deg, #251b16, #513727 50%, #1f2f2d);
}
.bg-shelves::before {
  background:
    linear-gradient(90deg, rgba(255,220,154,.16) 0 8px, transparent 8px 18px) 0 0 / 86px 100%,
    linear-gradient(0deg, rgba(255,255,255,.06) 0 2px, transparent 2px 92px);
  opacity: .72;
  animation: bgSlide 18s ease-in-out infinite alternate;
}
.bg-shelves::after {
  background:
    radial-gradient(circle at 22% 18%, rgba(255, 212, 129, .34), transparent 18%),
    radial-gradient(circle at 82% 72%, rgba(91, 181, 155, .22), transparent 24%);
  filter: blur(20px);
  animation: bgFloat 12s ease-in-out infinite alternate;
}
.bg-ink {
  background: linear-gradient(135deg, #fff7ec, #edf6f5 46%, #f5effb);
}
.bg-ink::before {
  background:
    radial-gradient(circle at 18% 28%, rgba(41, 116, 157, .22), transparent 18%),
    radial-gradient(circle at 72% 26%, rgba(185, 83, 101, .18), transparent 19%),
    radial-gradient(circle at 42% 78%, rgba(66, 142, 101, .18), transparent 20%);
  filter: blur(18px);
  animation: bgFloat 13s ease-in-out infinite alternate;
}
.bg-grid {
  background: #f8f7f2;
}
.bg-grid::before {
  background:
    linear-gradient(90deg, rgba(56, 74, 90, .11) 1px, transparent 1px) 0 0 / 34px 34px,
    linear-gradient(0deg, rgba(56, 74, 90, .10) 1px, transparent 1px) 0 0 / 34px 34px;
  animation: bgDrift 28s linear infinite;
}
.bg-aurora {
  background: linear-gradient(120deg, #071522, #10213b 45%, #13251f);
}
.bg-aurora::before {
  background:
    linear-gradient(110deg, transparent 12%, rgba(101, 255, 188, .30), transparent 42%),
    linear-gradient(70deg, transparent 20%, rgba(127, 164, 255, .28), transparent 55%),
    linear-gradient(135deg, transparent 18%, rgba(238, 127, 255, .18), transparent 48%);
  filter: blur(18px);
  animation: bgSlide 16s ease-in-out infinite alternate;
}
.bg-stars {
  background: linear-gradient(180deg, #101827, #1d2636);
}
.bg-stars::before {
  background:
    radial-gradient(circle, rgba(255,255,255,.88) 0 1px, transparent 1.7px) 4px 9px / 64px 64px,
    radial-gradient(circle, rgba(204,229,255,.74) 0 1px, transparent 1.8px) 24px 18px / 96px 96px;
  animation: bgStarMove 22s linear infinite;
}
.bg-rain {
  background: linear-gradient(180deg, #f6f8fb, #e9eef7);
}
.bg-rain::before {
  background: repeating-linear-gradient(112deg, rgba(77, 111, 160, .18) 0 1px, transparent 1px 18px);
  animation: bgRain 9s linear infinite;
}
.bg-rain::after {
  background: linear-gradient(180deg, rgba(255,255,255,.35), transparent 58%);
  animation: bgRainGlow 7s ease-in-out infinite alternate;
}
.bg-topo {
  background: linear-gradient(145deg, #fbf7ed, #eef7f2 55%, #f4f7fb);
}
.bg-topo::before {
  background:
    repeating-radial-gradient(ellipse at 30% 40%, rgba(67, 116, 105, .14) 0 2px, transparent 3px 18px),
    repeating-radial-gradient(ellipse at 76% 68%, rgba(82, 126, 170, .12) 0 2px, transparent 3px 20px);
  animation: bgFloat 18s ease-in-out infinite alternate;
}
.bg-cards {
  background: #f6f3ed;
}
.bg-cards::before {
  background:
    linear-gradient(0deg, rgba(0,0,0,.10) 1px, transparent 1px) 0 0 / 120px 80px,
    linear-gradient(90deg, rgba(0,0,0,.08) 1px, transparent 1px) 0 0 / 120px 80px;
  transform: rotate(-4deg);
  animation: bgSlide 20s ease-in-out infinite alternate;
}
.bg-circuit {
  background: linear-gradient(180deg, #07111f, #111827);
}
.bg-circuit::before {
  background:
    linear-gradient(90deg, rgba(96, 165, 250, .16) 1px, transparent 1px) 0 0 / 56px 56px,
    linear-gradient(0deg, rgba(52, 211, 153, .12) 1px, transparent 1px) 0 0 / 56px 56px,
    radial-gradient(circle at 18% 42%, rgba(96, 165, 250, .25), transparent 18%);
  animation: bgCircuit 10s linear infinite;
}
.bg-sunset {
  background: linear-gradient(160deg, #fff0d8, #f0b06e 48%, #445c7a);
}
.bg-sunset::before {
  background:
    radial-gradient(circle at 30% 18%, rgba(255,255,255,.55), transparent 15%),
    linear-gradient(110deg, transparent 24%, rgba(255,255,255,.22), transparent 55%);
  animation: bgSlide 14s ease-in-out infinite alternate;
}
.bg-green {
  background: linear-gradient(145deg, #eef6e8, #dfeee0 52%, #f6f0dd);
}
.bg-green::before {
  background:
    radial-gradient(ellipse at 22% 28%, rgba(69, 128, 80, .20), transparent 22%),
    radial-gradient(ellipse at 78% 70%, rgba(164, 128, 57, .16), transparent 24%);
  filter: blur(12px);
  animation: bgFloat 12s ease-in-out infinite alternate;
}
body[data-dynamic-background]:not([data-dynamic-background="none"]) {
  background: transparent;
}
body[data-dynamic-background]:not([data-dynamic-background="none"]) .book-shell {
  isolation: isolate;
}
@keyframes bgDrift {
  from { transform: translate3d(0, 0, 0); }
  to { transform: translate3d(-42px, -28px, 0); }
}
@keyframes bgSlide {
  from { transform: translateX(-5%) skewX(-4deg); }
  to { transform: translateX(6%) skewX(4deg); }
}
@keyframes bgFloat {
  from { transform: translate3d(-2%, -1%, 0) scale(1); }
  to { transform: translate3d(2%, 2%, 0) scale(1.04); }
}
@keyframes bgStarMove {
  from { transform: translate3d(0, 0, 0); opacity: .72; }
  to { transform: translate3d(-54px, -38px, 0); opacity: 1; }
}
@keyframes bgRain {
  from { transform: translate3d(0, -40px, 0); }
  to { transform: translate3d(-40px, 40px, 0); }
}
@keyframes bgRainGlow {
  from { transform: translateY(-18px); opacity: .35; }
  to { transform: translateY(26px); opacity: .78; }
}
@keyframes bgCircuit {
  from { transform: translate3d(0, 0, 0); opacity: .70; }
  to { transform: translate3d(0, 56px, 0); opacity: .96; }
}
@media (prefers-reduced-motion: reduce) {
  .dynamic-bg,
  .dynamic-bg::before,
  .dynamic-bg::after {
    animation: none !important;
  }
}
`;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  function init() {
    if (!bgRoot || !bgSelect) return;
    document.head.appendChild(styleElement);
    styleElement.textContent = backgroundCss;

    bgSelect.innerHTML = backgrounds.map(function (bg) {
      return `<option value="${escapeAttr(bg.id)}">${escapeHtml(bg.label)}</option>`;
    }).join("");

    const initialBg = getInitialBackground();
    bgSelect.value = initialBg.id;
    applyBackground(initialBg.id);

    bgSelect.addEventListener("change", function () {
      localStorage.setItem(storageKey, bgSelect.value);
      applyBackground(bgSelect.value);
    });
  }

  function getInitialBackground() {
    const params = new URLSearchParams(window.location.search);
    const requested = params.get("bg") || localStorage.getItem(storageKey) || "paper";
    return backgrounds.find(function (bg) { return bg.id === requested; }) || backgrounds[0];
  }

  function applyBackground(id) {
    const bg = backgrounds.find(function (item) { return item.id === id; }) || backgrounds[0];
    bgRoot.className = `dynamic-bg ${bg.className}`;
    document.body.dataset.dynamicBackground = bg.id;
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

  window.BookBackgrounds = {
    backgrounds: backgrounds.slice(),
    applyBackground: applyBackground
  };
}());
