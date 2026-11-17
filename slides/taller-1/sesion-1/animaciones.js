/* Explicadores locales: las minipoblaciones son ilustraciones, no los CSV. */
(() => {
  "use strict";
  const mean = values => values.reduce((a, b) => a + b, 0) / values.length;
  function rng(seed) {
    return () => {
      let t = seed += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function normal(random) {
    return Math.sqrt(-2 * Math.log(Math.max(random(), Number.EPSILON)))
      * Math.cos(2 * Math.PI * random());
  }
  function sampleIndices(size, n, random) {
    if (!Number.isInteger(n) || n < 1 || n > size) throw new Error("Tamaño muestral inválido");
    const indices = Array.from({length: size}, (_, i) => i);
    for (let i = 0; i < n; i++) {
      const j = i + Math.floor(random() * (size - i));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    return indices.slice(0, n);
  }
  function fitLine(points) {
    const mx = mean(points.map(p => p[0])), my = mean(points.map(p => p[1]));
    const denominator = points.reduce((s, [x]) => s + (x - mx) ** 2, 0);
    if (!denominator) throw new Error("Se necesita variación en X");
    const slope = points.reduce((s, [x, y]) => s + (x - mx) * (y - my), 0) / denominator;
    return {intercept: my - slope * mx, slope};
  }
  const sse = (points, a, b) => points.reduce((s, [x, y]) => s + (y - a - b * x) ** 2, 0);
  const critical95 = 1.959963984540054;
  const interval95 = (average, sigma, n) => [average - critical95 * sigma / Math.sqrt(n), average + critical95 * sigma / Math.sqrt(n)];
  const mathematics = {mean, rng, normal, sampleIndices, fitLine, sse, interval95};
  // Permite comprobar las operaciones con Node sin DOM ni dependencias.
  if (typeof module !== "undefined" && module.exports) module.exports = mathematics;
  if (typeof document === "undefined") return;

  const NS = "http://www.w3.org/2000/svg";
  const palette = {ink: "#1B2A4A", teal: "#007279", amber: "#B26A00", grey: "#B5C0CD", miss: "#B24735"};
  const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const format = (value, digits = 2) => value.toLocaleString("es-MX", {minimumFractionDigits: digits, maximumFractionDigits: digits});
  const controllers = [];
  let instance = 0;

  function node(tag, attrs = {}, text = null) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, String(value)));
    if (text !== null) el.textContent = text;
    return el;
  }
  function add(svg, tag, attrs, text) { const el = node(tag, attrs, text); svg.append(el); return el; }
  function text(svg, x, y, value, attrs = {}) {
    return add(svg, "text", {x, y, fill: palette.ink, "font-size": 16, ...attrs}, value);
  }
  function line(svg, x1, y1, x2, y2, attrs = {}) {
    return add(svg, "line", {x1, y1, x2, y2, stroke: palette.grey, "stroke-width": 1, ...attrs});
  }
  function xAxis(svg, scale, values, left, right, bottom, label) {
    line(svg, left, bottom, right, bottom, {stroke: palette.ink});
    values.forEach(value => {
      line(svg, scale(value), bottom, scale(value), bottom + 5, {stroke: palette.ink});
      text(svg, scale(value), bottom + 24, format(value, 0), {"text-anchor": "middle"});
    });
    text(svg, (left + right) / 2, bottom + 47, label, {"text-anchor": "middle"});
  }
  function base(root, caption, controls, note, label) {
    root.dataset.demoReady = "true";
    root.innerHTML = `<p class="demo-caption">${caption}</p><div class="demo-controls">${controls}</div><svg class="demo-chart" viewBox="0 0 1100 265" role="img" aria-label="${label}"></svg><p class="demo-metrics" aria-live="polite" aria-atomic="true"></p><p class="demo-note">${note}</p>`;
    root.addEventListener("keydown", event => {
      if (event.key !== "Escape" && event.target.closest("input, select, button")) event.stopPropagation();
    });
    return {svg: root.querySelector("svg"), metrics: root.querySelector(".demo-metrics")};
  }
  function visible(root) {
    const slide = root.closest("section.slide");
    return !document.hidden && root.getClientRects().length > 0 && (!slide || slide.classList.contains("present") || !window.Reveal);
  }
  function sequence(root, button, step, count, delay = 420) {
    let timer = null, remaining = 0;
    const label = button.textContent;
    const pause = () => { window.clearTimeout(timer); timer = null; button.textContent = label; button.setAttribute("aria-pressed", "false"); };
    const tick = () => {
      if (!visible(root) || remaining <= 0 || step() === false) { pause(); return; }
      remaining -= 1;
      timer = window.setTimeout(tick, delay);
    };
    button.setAttribute("aria-pressed", "false");
    button.addEventListener("click", () => {
      if (timer !== null) { pause(); return; }
      remaining = count(); button.textContent = "Pausar"; button.setAttribute("aria-pressed", "true"); tick();
    });
    controllers.push({root, pause});
    return pause;
  }

  function sampling(root) {
    const id = `demo-n-${++instance}`;
    const {svg, metrics} = base(root,
      "Minipoblación ilustrativa de 400 clientes, distinta del CSV del laboratorio.",
      `<label for="${id}">Tamaño de muestra <select id="${id}"><option value="40">40</option><option value="200">200</option></select></label><button type="button" data-action="next">Extraer otra muestra</button><button type="button" data-action="play">Animar 20 muestras</button><button type="button" data-action="reset">Reiniciar</button>`,
      "Puntos verdes: muestra sin reemplazo. Línea ámbar: media de la población. Al cambiar n, reiniciamos las repeticiones.",
      "Población y muestra de saldos, junto a un histograma de medias muestrales");
    const populationRng = rng(202609);
    const population = Array.from({length: 400}, () => 25 + 8 * normal(populationRng)).map(x => Math.max(1, x));
    const mu = mean(population);
    let random = rng(42), selected = new Set(), means = [];
    const select = root.querySelector("select");
    const ticks = [0, 10, 20, 30, 40, 50, 60];
    const xmin = Math.min(0, ...population), xmax = Math.max(60, ...population);
    const popScale = value => 45 + (value - xmin) / (xmax - xmin) * 440;
    function draw() {
      svg.replaceChildren();
      text(svg, 260, 22, "Personas: saldos individuales", {"text-anchor": "middle", "font-weight": 650});
      population.forEach((value, i) => add(svg, "circle", {cx: popScale(value), cy: 45 + i % 12 * 12, r: selected.has(i) ? 3.3 : 2.5, fill: selected.has(i) ? palette.teal : palette.grey, opacity: selected.has(i) ? 1 : .55}));
      line(svg, popScale(mu), 36, popScale(mu), 198, {stroke: palette.amber, "stroke-width": 3});
      xAxis(svg, popScale, ticks, 45, 485, 205, "Saldo (miles de MXN)");

      // Mantener la misma escala al comparar n, expandiéndola solo si hace falta.
      const halfRange = Math.max(4, ...means.map(m => Math.abs(m - mu) + .5));
      const lo = mu - halfRange, hi = mu + halfRange;
      const histScale = value => 610 + (value - lo) / (hi - lo) * 440;
      const bins = Array(20).fill(0);
      means.forEach(value => bins[Math.min(19, Math.floor((value - lo) / (hi - lo) * 20))]++);
      const maxCount = Math.max(1, ...bins);
      text(svg, 830, 22, "Muestras: distribución de sus medias", {"text-anchor": "middle", "font-weight": 650});
      bins.forEach((count, i) => add(svg, "rect", {x: 610 + i * 22, y: 205 - count / maxCount * 156, width: 20, height: count / maxCount * 156, fill: palette.teal, opacity: .85}));
      line(svg, histScale(mu), 36, histScale(mu), 205, {stroke: palette.amber, "stroke-width": 3});
      text(svg, 604, 52, `${maxCount}`, {"text-anchor": "end", "font-size": 13});
      text(svg, 604, 204, "0", {"text-anchor": "end", "font-size": 13});
      text(svg, 610, 38, "Frecuencia", {"font-size": 13});
      const histTicks = [lo, mu - halfRange / 2, mu, mu + halfRange / 2, hi];
      xAxis(svg, histScale, histTicks, 610, 1050, 205, "Media de cada muestra (miles de MXN)");
      const last = means.length ? `Última media: ${format(means.at(-1))}` : "Extrae una muestra para comenzar";
      const range = means.length > 1 ? ` · Medias entre ${format(Math.min(...means))} y ${format(Math.max(...means))}` : "";
      metrics.textContent = `Media poblacional: ${format(mu)} · ${last} · Muestras: ${means.length}${range}`;
    }
    const next = () => { selected = new Set(sampleIndices(population.length, Number(select.value), random)); means.push(mean([...selected].map(i => population[i]))); draw(); };
    const pause = sequence(root, root.querySelector('[data-action="play"]'), next, () => 20);
    root.querySelector('[data-action="next"]').addEventListener("click", () => { pause(); next(); });
    function reset() { pause(); random = rng(42); selected = new Set(); means = []; draw(); }
    select.addEventListener("change", reset);
    root.querySelector('[data-action="reset"]').addEventListener("click", reset);
    draw();
  }

  function intervals(root) {
    const id = `demo-reps-${++instance}`;
    const {svg, metrics} = base(root,
      "Experimento ilustrativo: saldo normal con media 25 y DE poblacional conocida σ = 10 miles de MXN; n = 25 por muestra.",
      `<label for="${id}">Repeticiones <select id="${id}"><option value="40">40</option><option value="80">80</option></select></label><button type="button" data-action="next">Un intervalo más</button><button type="button" data-action="play">Animar intervalos</button><button type="button" data-action="reset">Reiniciar</button>`,
      "σ es la DE poblacional conocida; σ/√n es el EE de la media. IC = media ± 1.96 × EE. Verde: cubre 25; rojo discontinuo: no cubre. 95% describe el procedimiento, no una cuota garantizada.",
      "Intervalos de confianza repetidos y línea fija en la media poblacional");
    const random = rng(6172), mu = 25, sigma = 10, n = 25;
    const intervals = Array.from({length: 80}, () => {
      const average = mean(Array.from({length: n}, () => mu + sigma * normal(random)));
      const [lo, hi] = interval95(average, sigma, n);
      return {average, lo, hi, covers: lo <= mu && mu <= hi};
    });
    const loAxis = Math.floor(Math.min(...intervals.map(x => x.lo))) - 1;
    const hiAxis = Math.ceil(Math.max(...intervals.map(x => x.hi))) + 1;
    const x = value => 100 + (value - loAxis) / (hiAxis - loAxis) * 900;
    let shown = 0;
    const select = root.querySelector("select");
    function draw() {
      svg.replaceChildren();
      const total = Number(select.value), step = 177 / total;
      line(svg, x(mu), 20, x(mu), 207, {stroke: palette.amber, "stroke-width": 3});
      text(svg, x(mu), 15, "μ = 25", {"text-anchor": "middle", fill: palette.amber});
      intervals.slice(0, shown).forEach((item, i) => {
        const y = 25 + (i + .5) * step, color = item.covers ? palette.teal : palette.miss;
        line(svg, x(item.lo), y, x(item.hi), y, {stroke: color, "stroke-width": total === 80 ? 1.6 : 2.4, "stroke-dasharray": item.covers ? "none" : "5 3"});
        add(svg, "circle", {cx: x(item.average), cy: y, r: total === 80 ? 1.9 : 2.7, fill: color});
      });
      if (!shown) text(svg, 550, 108, "Cada línea será el intervalo de una muestra distinta.", {"text-anchor": "middle"});
      const ticks = Array.from({length: Math.floor((hiAxis - loAxis) / 5) + 1}, (_, i) => Math.ceil(loAxis / 5) * 5 + i * 5).filter(v => v <= hiAxis);
      xAxis(svg, x, ticks, 100, 1000, 210, "Media estimada e intervalo (miles de MXN)");
      const covered = intervals.slice(0, shown).filter(item => item.covers).length;
      metrics.textContent = shown ? `Intervalos: ${shown}/${total} · Cubren μ: ${covered} · No cubren: ${shown - covered} · Cobertura observada: ${format(100 * covered / shown, 1)}%` : "La media poblacional permanece fija; cambian la muestra y su intervalo.";
    }
    const next = () => { if (shown >= Number(select.value)) return false; shown++; draw(); return true; };
    const pause = sequence(root, root.querySelector('[data-action="play"]'), next, () => Number(select.value) - shown, 220);
    root.querySelector('[data-action="next"]').addEventListener("click", () => { pause(); next(); });
    function reset() { pause(); shown = 0; draw(); }
    select.addEventListener("change", reset);
    root.querySelector('[data-action="reset"]').addEventListener("click", reset);
    draw();
  }

  function ols(root) {
    const id = ++instance, clipId = `ols-clip-${id}`;
    const {svg, metrics} = base(root,
      "12 clientes ilustrativos, distintos del CSV. Ajusta la recta y observa los residuos verticales.",
      `<label>Intercepto <input type="range" data-param="a" min="-4" max="12" step="0.1" value="10" aria-label="Intercepto de la recta"><output data-value="a">10.00</output></label><label>Pendiente <input type="range" data-param="b" min="0" max="0.8" step="0.01" value="0.2" aria-label="Pendiente de la recta"><output data-value="b">0.20</output></label><label class="demo-checkbox"><input type="checkbox" data-action="squares"> Ver cuadrados</label><button type="button" data-action="fit">Encontrar la recta</button><button type="button" data-action="reset">Reiniciar</button>`,
      "Elevar los residuos al cuadrado evita que sus signos se cancelen y da más peso a discrepancias grandes. Residuo = observado − ajustado. Buscamos reducir la suma para todos los puntos.",
      "Nube de saldos y abonos, recta ajustable y residuos verticales");
    const points = [8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52].map((x, i) => [x, [8, 7, 13, 11, 18, 16, 22, 19, 27, 23, 29, 31][i]]);
    const fitted = fitLine(points);
    let a = 10, b = .2, frame = null;
    const aSlider = root.querySelector('[data-param="a"]'), bSlider = root.querySelector('[data-param="b"]');
    const squareToggle = root.querySelector('[data-action="squares"]');
    const x = value => 90 + value / 60 * 900, y = value => 207 - value / 60 * 178;
    function draw() {
      svg.replaceChildren();
      const defs = add(svg, "defs", {}), clip = add(defs, "clipPath", {id: clipId});
      add(clip, "rect", {x: 90, y: 20, width: 900, height: 188});
      [0, 15, 30, 45, 60].forEach(value => {
        line(svg, 90, y(value), 990, y(value), {stroke: "#DDE3E9"});
        text(svg, 80, y(value) + 5, value, {"text-anchor": "end"});
      });
      text(svg, 90, 16, "Saldo promedio (miles de MXN)");
      const plot = add(svg, "g", {"clip-path": `url(#${clipId})`});
      points.forEach(([vx, vy]) => {
        const prediction = a + b * vx, residual = vy - prediction, size = Math.abs(y(vy) - y(prediction));
        if (squareToggle.checked) add(plot, "rect", {x: x(vx), y: Math.min(y(vy), y(prediction)), width: size, height: size, fill: palette.amber, opacity: .13, stroke: palette.amber, "stroke-width": 1});
        line(plot, x(vx), y(vy), x(vx), y(prediction), {stroke: palette.amber, "stroke-width": 2.5});
        add(plot, "circle", {cx: x(vx), cy: y(vy), r: 5, fill: palette.teal});
        const title = node("title", {}, `Abonos ${vx}; saldo ${vy}; residuo ${format(residual)}`);
        plot.lastChild.append(title);
      });
      line(plot, x(0), y(a), x(60), y(a + b * 60), {stroke: palette.ink, "stroke-width": 3});
      xAxis(svg, x, [0, 10, 20, 30, 40, 50, 60], 90, 990, 210, "Abonos mensuales (miles de MXN)");
      root.querySelector('[data-value="a"]').textContent = format(a);
      root.querySelector('[data-value="b"]').textContent = format(b);
      const current = sse(points, a, b), minimum = sse(points, fitted.intercept, fitted.slope);
      metrics.textContent = `Recta: Ŷ = ${format(a)} + ${format(b)}X · Suma de residuos²: ${format(current)} · Menor suma posible: ${format(minimum)} (miles de MXN)²`;
    }
    const stop = () => { if (frame !== null) cancelAnimationFrame(frame); frame = null; };
    controllers.push({root, pause: stop});
    function readSliders() { stop(); a = Number(aSlider.value); b = Number(bSlider.value); draw(); }
    aSlider.addEventListener("input", readSliders); bSlider.addEventListener("input", readSliders);
    squareToggle.addEventListener("change", draw);
    root.querySelector('[data-action="fit"]').addEventListener("click", () => {
      stop(); const startA = a, startB = b, startTime = performance.now();
      const duration = reducedMotion() ? 0 : 850;
      function move(time) {
        if (!visible(root)) { stop(); return; }
        const progress = duration ? Math.min(1, (time - startTime) / duration) : 1;
        const eased = 1 - (1 - progress) ** 3;
        a = startA + (fitted.intercept - startA) * eased;
        b = startB + (fitted.slope - startB) * eased;
        aSlider.value = a; bSlider.value = b; draw();
        frame = progress < 1 ? requestAnimationFrame(move) : null;
      }
      frame = requestAnimationFrame(move);
    });
    root.querySelector('[data-action="reset"]').addEventListener("click", () => { stop(); a = 10; b = .2; aSlider.value = a; bSlider.value = b; squareToggle.checked = false; draw(); });
    draw();
  }

  function initialize() {
    document.querySelectorAll(".concept-demo[data-demo]:not([data-demo-ready])").forEach(root => {
      ({muestreo: sampling, intervalos: intervals, ols})[root.dataset.demo]?.(root);
    });
    if (window.Reveal && !window.Reveal.__conceptAnimationsBound) {
      window.Reveal.on("slidechanged", () => controllers.forEach(item => { if (!visible(item.root)) item.pause(); }));
      window.Reveal.__conceptAnimationsBound = true;
    }
  }
  document.addEventListener("visibilitychange", () => { if (document.hidden) controllers.forEach(item => item.pause()); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize, {once: true});
  else initialize();
  if (window.Reveal?.on) window.Reveal.on("ready", initialize);
})();
