(function () {
  "use strict";

  const storageKey = "johsokBookBackground";
  const bgRoot = document.getElementById("dynamicBackground");
  const bgSelect = document.getElementById("bgSelect");
  const styleElement = document.createElement("style");

  const backgrounds = [
    { id: "none", label: "00_無背景", className: "bg-none" },
    { id: "ink", label: "01_流體墨水背景", className: "bg-ink" },
    { id: "network", label: "02_粒子連線網絡", className: "bg-network" },
    { id: "ecg", label: "03_脈衝心電圖背景", className: "bg-ecg" },
    { id: "prism", label: "04_科技幾何動態背景", className: "bg-prism" },
    { id: "wireframe", label: "05_漂浮3D幾何線框", className: "bg-wireframe" },
    { id: "contour", label: "06_動態等高線地圖", className: "bg-contour" },
    { id: "lightRain", label: "07_光點雨幕", className: "bg-light-rain" },
    { id: "pulse", label: "08_呼吸式醫療光圈", className: "bg-pulse" },
    { id: "cyberpunk", label: "09_賽博龐克", className: "bg-cyberpunk" },
    { id: "magnetic", label: "10_互動滑鼠磁場", className: "bg-magnetic" },
    { id: "aurora", label: "11_極光帷幕", className: "bg-aurora" },
    { id: "bubbles", label: "12_漂浮光泡", className: "bg-bubbles" },
    { id: "stars", label: "13_星點微光", className: "bg-stars" },
    { id: "waves", label: "14_海浪流線", className: "bg-waves" },
    { id: "rain", label: "15_雨絲光幕", className: "bg-rain" },
    { id: "grid", label: "16_紙感幾何", className: "bg-grid" },
    { id: "dust", label: "17_粒子星座", className: "bg-dust" },
    { id: "paper", label: "18_紙張纖維", className: "bg-paper" },
    { id: "shelves", label: "19_書架光影", className: "bg-shelves" }
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
.bg-ink::after {
  background: linear-gradient(110deg, transparent 22%, rgba(255,255,255,.34), transparent 58%);
  filter: blur(12px);
  animation: bgSlide 11s ease-in-out infinite alternate;
}
.bg-network {
  background: linear-gradient(145deg, #061016, #13202a 45%, #18281f);
}
.bg-network::before {
  background:
    radial-gradient(circle, rgba(133, 229, 215, .46) 0 2px, transparent 2.5px) 0 0 / 72px 72px,
    linear-gradient(90deg, rgba(133, 199, 213, .08) 1px, transparent 1px) 0 0 / 36px 36px,
    linear-gradient(0deg, rgba(126, 177, 142, .07) 1px, transparent 1px) 0 0 / 36px 36px;
  animation: bgDrift 26s linear infinite;
}
.bg-network::after {
  background:
    radial-gradient(circle at 24% 30%, rgba(78, 189, 180, .28), transparent 22%),
    radial-gradient(circle at 72% 68%, rgba(145, 185, 255, .22), transparent 25%);
  filter: blur(14px);
  animation: bgFloat 12s ease-in-out infinite alternate;
}
.bg-ecg {
  background: linear-gradient(180deg, #f6fbf8, #eaf4f2);
}
.bg-ecg::before {
  background:
    linear-gradient(90deg, rgba(65, 130, 115, .09) 1px, transparent 1px) 0 0 / 40px 40px,
    linear-gradient(0deg, rgba(65, 130, 115, .07) 1px, transparent 1px) 0 0 / 40px 40px;
  animation: bgGridShift 30s linear infinite;
}
.bg-ecg::after {
  background:
    linear-gradient(105deg, transparent 0 38%, rgba(39,153,124,.52) 38.3% 38.7%, transparent 39% 43%, rgba(39,153,124,.68) 43.3% 43.7%, transparent 44% 48%, rgba(39,153,124,.52) 48.3% 48.7%, transparent 49%),
    radial-gradient(circle at 22% 72%, rgba(68, 191, 156, .18), transparent 16%),
    radial-gradient(circle at 80% 22%, rgba(82, 132, 200, .14), transparent 16%);
  filter: blur(.2px);
  animation: bgEcgSweep 6s linear infinite;
}
.bg-prism {
  background: radial-gradient(circle at 50% 18%, #10283c, #06111b 48%, #03070f);
}
.bg-prism::before {
  background:
    conic-gradient(from 30deg at 24% 32%, transparent, rgba(0,229,255,.24), transparent 30%),
    conic-gradient(from 210deg at 76% 66%, transparent, rgba(255,46,193,.20), transparent 28%),
    radial-gradient(circle at 52% 82%, rgba(118, 255, 122, .13), transparent 22%);
  filter: blur(8px);
  animation: bgFloat 10s ease-in-out infinite alternate;
}
.bg-prism::after {
  background:
    linear-gradient(90deg, rgba(72, 214, 255, .09) 1px, transparent 1px) 0 0 / 46px 46px,
    linear-gradient(0deg, rgba(72, 214, 255, .065) 1px, transparent 1px) 0 0 / 46px 46px,
    linear-gradient(115deg, transparent 34%, rgba(255,255,255,.10), transparent 47%);
  mix-blend-mode: screen;
  animation: bgDrift 18s linear infinite;
}
.bg-wireframe {
  background: linear-gradient(150deg, #081118, #17252a 55%, #221f28);
}
.bg-wireframe::before {
  background:
    repeating-linear-gradient(60deg, transparent 0 42px, rgba(94,217,190,.14) 43px 44px, transparent 45px 86px),
    repeating-linear-gradient(-60deg, transparent 0 42px, rgba(218,183,111,.12) 43px 44px, transparent 45px 86px);
  animation: bgWireframe 18s ease-in-out infinite alternate;
}
.bg-wireframe::after {
  background:
    linear-gradient(90deg, rgba(255,255,255,.055) 1px, transparent 1px) 0 0 / 68px 68px,
    linear-gradient(0deg, rgba(255,255,255,.045) 1px, transparent 1px) 0 0 / 68px 68px;
  animation: bgDrift 34s linear infinite;
}
.bg-contour {
  background: linear-gradient(145deg, #fbf7ed, #eef7f2 55%, #f4f7fb);
}
.bg-contour::before {
  background:
    repeating-radial-gradient(ellipse at 28% 38%, rgba(79,145,133,.16) 0 2px, transparent 3px 18px),
    repeating-radial-gradient(ellipse at 76% 66%, rgba(82,126,170,.13) 0 2px, transparent 3px 21px);
  animation: bgContour 16s ease-in-out infinite alternate;
}
.bg-contour::after {
  background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,.28), transparent 58%);
  animation: bgSlide 14s ease-in-out infinite alternate;
}
.bg-light-rain {
  background: linear-gradient(180deg, #f7f9fb, #eaf1f5);
}
.bg-light-rain::before {
  background: repeating-linear-gradient(112deg, transparent 0 18px, rgba(72, 128, 154, .13) 19px 21px, transparent 22px 42px);
  animation: bgRain 7s linear infinite;
}
.bg-light-rain::after {
  background:
    radial-gradient(circle, rgba(255,255,255,.82) 0 2px, transparent 2.8px) 0 0 / 58px 74px,
    radial-gradient(circle at 78% 22%, rgba(92, 188, 210, .16), transparent 18%);
  animation: bgRainGlow 5.5s ease-in-out infinite alternate;
}
.bg-pulse {
  background: linear-gradient(145deg, #f6fbf7, #edf6f5 52%, #f8f5ef);
}
.bg-pulse::before {
  background:
    repeating-radial-gradient(circle at 50% 50%, rgba(75,185,143,.15) 0 2px, transparent 3px 38px),
    radial-gradient(circle at 72% 68%, rgba(90, 150, 204, .14), transparent 22%);
  animation: bgPulseGlow 4.8s ease-in-out infinite alternate;
}
.bg-pulse::after {
  background: radial-gradient(circle, rgba(79, 169, 138, .12) 0 1px, transparent 1.5px) 0 0 / 52px 52px;
  animation: bgDrift 28s linear infinite;
}
.bg-cyberpunk {
  background: linear-gradient(180deg, #050611, #0b1024 48%, #160821);
}
.bg-cyberpunk::before {
  background:
    linear-gradient(90deg, rgba(0, 245, 255, .16) 1px, transparent 1px) 0 0 / 56px 56px,
    linear-gradient(0deg, rgba(255, 42, 191, .12) 1px, transparent 1px) 0 0 / 56px 56px,
    repeating-linear-gradient(180deg, rgba(255,255,255,.035) 0 1px, transparent 1px 8px);
  animation: bgCyberGrid 10s linear infinite;
}
.bg-cyberpunk::after {
  background:
    radial-gradient(circle at 14% 42%, rgba(0, 245, 255, .34), transparent 20%),
    radial-gradient(circle at 86% 58%, rgba(255, 42, 191, .30), transparent 22%),
    linear-gradient(110deg, transparent 26%, rgba(255,230,109,.14), transparent 54%);
  filter: blur(12px);
  animation: bgPrismSweep 7.5s ease-in-out infinite alternate;
}
.bg-magnetic {
  background: linear-gradient(145deg, #071015, #172026 50%, #111c1a);
}
.bg-magnetic::before {
  background:
    repeating-radial-gradient(circle at var(--bg-pointer-x, 50%) var(--bg-pointer-y, 50%), rgba(78,198,184,.20) 0 2px, transparent 3px 30px),
    radial-gradient(circle at 78% 72%, rgba(226, 185, 107, .13), transparent 24%);
  transition: background-position .12s linear;
}
.bg-magnetic::after {
  background:
    linear-gradient(90deg, rgba(255,255,255,.055) 1px, transparent 1px) 0 0 / 54px 54px,
    linear-gradient(0deg, rgba(255,255,255,.045) 1px, transparent 1px) 0 0 / 54px 54px;
  animation: bgDrift 24s linear infinite;
}
.bg-bubbles {
  background: #f6fbff;
}
.bg-bubbles::before {
  background:
    radial-gradient(circle at 18% 24%, rgba(111, 164, 255, .34), transparent 8%),
    radial-gradient(circle at 78% 18%, rgba(255, 182, 216, .36), transparent 9%),
    radial-gradient(circle at 28% 78%, rgba(140, 224, 191, .34), transparent 10%),
    radial-gradient(circle at 70% 72%, rgba(245, 214, 122, .30), transparent 9%);
  filter: blur(3px);
  animation: bgFloat 15s ease-in-out infinite alternate;
}
.bg-bubbles::after {
  background:
    radial-gradient(circle, rgba(111, 164, 255, .22) 0 8px, transparent 9px) 0 0 / 86px 86px,
    radial-gradient(circle, rgba(255, 182, 216, .26) 0 6px, transparent 7px) 32px 46px / 118px 118px;
  animation: bgBubbleRise 18s linear infinite;
}
.bg-waves {
  background: linear-gradient(180deg, #eaf7fb, #dff2ee);
}
.bg-waves::before {
  background: repeating-radial-gradient(ellipse at 50% 120%, rgba(44, 129, 156, .16) 0 3px, transparent 4px 20px);
  animation: bgWave 12s ease-in-out infinite alternate;
}
.bg-waves::after {
  background: repeating-linear-gradient(168deg, transparent 0 18px, rgba(61, 145, 171, .12) 19px 21px, transparent 22px 42px);
  filter: blur(1px);
  animation: bgWaterFlow 15s linear infinite;
}
.bg-dust {
  background: linear-gradient(160deg, #18202f, #263648);
}
.bg-dust::before {
  background:
    radial-gradient(circle, rgba(255,255,255,.75) 0 1px, transparent 1.6px) 0 0 / 42px 42px,
    radial-gradient(circle, rgba(255,227,167,.52) 0 1px, transparent 1.7px) 18px 22px / 74px 74px;
  animation: bgDust 14s linear infinite;
}
.bg-dust::after {
  background:
    linear-gradient(28deg, transparent 48%, rgba(255,255,255,.10) 49% 50%, transparent 51%) 0 0 / 150px 120px,
    radial-gradient(circle at 78% 28%, rgba(194, 220, 255, .18), transparent 14%);
  filter: blur(4px);
  animation: bgFloat 10s ease-in-out infinite alternate;
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
@keyframes bgGridShift {
  from { transform: translate3d(0, 0, 0); }
  to { transform: translate3d(-60px, -60px, 0); }
}
@keyframes bgEcgSweep {
  from { transform: translateX(-12%); opacity: .48; }
  to { transform: translateX(12%); opacity: .92; }
}
@keyframes bgWireframe {
  from { transform: perspective(600px) rotateX(3deg) rotateZ(-2deg) scale(1); }
  to { transform: perspective(600px) rotateX(-3deg) rotateZ(2deg) scale(1.04); }
}
@keyframes bgContour {
  from { transform: translate3d(-2%, -1%, 0) scale(1); }
  to { transform: translate3d(3%, 2%, 0) scale(1.05); }
}
@keyframes bgPulseGlow {
  from { transform: scale(.98); opacity: .48; }
  to { transform: scale(1.04); opacity: .88; }
}
@keyframes bgCyberGrid {
  from { transform: translate3d(0, 0, 0); opacity: .72; }
  to { transform: translate3d(0, 56px, 0); opacity: .95; }
}
@keyframes bgPrismSweep {
  from { transform: translate3d(-6%, -2%, 0) skewX(-8deg); opacity: .62; }
  to { transform: translate3d(7%, 3%, 0) skewX(7deg); opacity: .94; }
}
@keyframes bgBubbleRise {
  from { transform: translate3d(0, 36px, 0) scale(1); opacity: .58; }
  to { transform: translate3d(-24px, -74px, 0) scale(1.04); opacity: .86; }
}
@keyframes bgWave {
  from { transform: translateY(0) scale(1); }
  to { transform: translateY(-26px) scale(1.03); }
}
@keyframes bgWaterFlow {
  from { transform: translate3d(-30px, 18px, 0); }
  to { transform: translate3d(46px, -20px, 0); }
}
@keyframes bgDust {
  from { transform: translate3d(0, 0, 0); opacity: .65; }
  to { transform: translate3d(-24px, -52px, 0); opacity: .9; }
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

    window.addEventListener("pointermove", updatePointer);
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

  function updatePointer(event) {
    bgRoot.style.setProperty("--bg-pointer-x", `${event.clientX}px`);
    bgRoot.style.setProperty("--bg-pointer-y", `${event.clientY}px`);
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
