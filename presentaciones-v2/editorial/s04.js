/* S4 · demos: selector de día (partición) y simulador de exclusión por reglas. Sin dependencias. */
(() => {
  'use strict';
  const fmt = v => v.toLocaleString('en-US');

  document.querySelectorAll('[data-demo="s4-particion"]').forEach(root => {
    const total = 1231.6;
    const out = k => root.closest('.slide').querySelector(`[data-out="${k}"]`);
    root.querySelectorAll('button[data-mb]').forEach(btn => btn.addEventListener('click', () => {
      root.querySelectorAll('button[data-mb]').forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
      const mb = parseFloat(btn.dataset.mb);
      out('mb').textContent = mb.toFixed(1);
      out('pct').textContent = (mb / total * 100).toFixed(1);
    }));
  });

  document.querySelectorAll('[data-demo="s4-exclusion"]').forEach(root => {
    const combos = JSON.parse(root.dataset.combos);
    const total = combos.reduce((a, c) => a + c[4], 0);
    const out = k => root.querySelector(`[data-out="${k}"]`);
    const pressed = () => [...root.querySelectorAll('button[data-rule]')].filter(b => b.getAttribute('aria-pressed') === 'true').map(b => Number(b.dataset.rule));
    const paint = () => {
      const on = pressed();
      const left = combos.filter(c => on.every(i => c[i] === 0)).reduce((a, c) => a + c[4], 0);
      out('resto').textContent = fmt(left);
      out('pct').textContent = (left / total * 100).toFixed(1);
      out('fuera').textContent = fmt(total - left);
      out('barra').style.setProperty('--w', (left / total * 100).toFixed(2) + '%');
    };
    root.querySelectorAll('button[data-rule]').forEach(b => b.addEventListener('click', () => {
      b.setAttribute('aria-pressed', String(b.getAttribute('aria-pressed') !== 'true'));
      paint();
    }));
  });
})();
