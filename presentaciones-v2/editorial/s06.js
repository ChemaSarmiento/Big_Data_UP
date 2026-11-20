(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs = {}, text) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (text !== undefined) e.textContent = text; return e; };
  const fmt = (x) => x.toLocaleString('en-US');
  const nice = (m) => { const steps = [0.5, 1, 2, 2.5, 5, 10]; let mag = Math.pow(10, Math.floor(Math.log10(m))); for (const s of steps) if (s * mag >= m) return s * mag; return 10 * mag; };

  function initFiltro(root) {
    const data = JSON.parse(root.dataset.series);
    const selT = root.querySelector('[data-tema]'), selG = root.querySelector('[data-idioma]');
    const title = root.querySelector('[data-titulo]'), cover = root.querySelector('[data-cobertura]');
    const svg = root.querySelector('[data-plot]');
    const gname = { todos: 'de todos los idiomas', en: 'de los tweets en inglés', es: 'de los tweets en español', otro: 'de los tweets en otros idiomas' };
    function draw() {
      const t = selT.value, g = selG.value, d = data.datos[t][g];
      const pct = d.n.map((n, i) => 100 * n / d.dia[i]);
      const nTot = d.n.reduce((a, b) => a + b, 0), base = d.dia.reduce((a, b) => a + b, 0);
      const mx = Math.max(...pct) * 1.08, step = nice(mx / 4), ymax = Math.ceil(mx / step) * step;
      const fx = 70, fy = 20, w = 1260, h = 230, k = pct.length;
      const X = (i) => fx + i * w / (k - 1), Y = (v) => fy + h - v / ymax * h;
      svg.replaceChildren();
      svg.appendChild(el('rect', { class: 'partial', x: fx - 6, y: fy, width: w / (k - 1) * 0.5 + 6, height: h }));
      svg.appendChild(el('text', { class: 'sm', x: fx + 4, y: fy + 24 }, 'día parcial'));
      for (let v = 0; v <= ymax + 1e-9; v += step) {
        const y = Y(v);
        svg.appendChild(el('line', { class: 'grid', x1: fx, x2: fx + w, y1: y, y2: y }));
        svg.appendChild(el('text', { class: 'tick', x: fx - 10, y: y + 7, 'text-anchor': 'end' }, (step < 1 ? v.toFixed(2) : v.toFixed(1))));
      }
      svg.appendChild(el('line', { class: 'axis', x1: fx, x2: fx + w, y1: fy + h, y2: fy + h }));
      data.fechas.forEach((f, i) => svg.appendChild(el('text', { class: 'tick', x: X(i), y: fy + h + 30, 'text-anchor': 'middle' }, f)));
      svg.appendChild(el('polyline', { class: 'ln l-hl', style: 'stroke-width:6px', points: pct.map((v, i) => `${X(i)},${Y(v)}`).join(' ') }));
      const im = pct.indexOf(Math.max(...pct));
      svg.appendChild(el('circle', { class: 'dot d-hl', cx: X(im), cy: Y(pct[im]), r: 9 }));
      svg.appendChild(el('text', { class: 'val t-hl', x: Math.min(X(im) + 14, fx + w - 90), y: Y(pct[im]) - 14 }, pct[im].toFixed(2) + ' %'));
      title.textContent = `${data.nombres[t]}: ${(100 * nTot / base).toFixed(2)} % ${gname[g]} del periodo (${fmt(nTot)} de ${fmt(base)})`;
      cover.textContent = `Cobertura: 16–27 mar 2022 · el 16 es día parcial · eje desde 0, máximo ${ymax.toFixed(step < 1 ? 2 : 1)} % · pico el ${data.fechas[im]} de marzo · palabras clave, no temas verificados`;
    }
    selT.addEventListener('change', draw); selG.addEventListener('change', draw); draw();
  }

  function initAuditoria(root) {
    const btns = [...root.querySelectorAll('[data-claim]')], ver = [...root.querySelectorAll('[data-verdict]')];
    btns.forEach((b) => b.addEventListener('click', () => {
      btns.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      ver.forEach((v) => { v.hidden = v.dataset.verdict !== b.dataset.claim; });
    }));
  }

  const start = () => {
    document.querySelectorAll('[data-demo="filtro"]').forEach(initFiltro);
    document.querySelectorAll('[data-demo="auditoria"]').forEach(initAuditoria);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
