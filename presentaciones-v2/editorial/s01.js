(() => {
  'use strict';
  document.querySelectorAll('[data-demo="reparto"]').forEach(d => {
    const cells = [...d.querySelectorAll('.s1-cajas i')];
    const out = d.querySelector('[data-par-out]');
    const draw = w => {
      const per = Math.ceil(cells.length / w);
      cells.forEach((c, i) => { c.dataset.k = Math.min(w - 1, Math.floor(i / per)); });
      const tiempo = w === 1 ? `${cells.length} min` : `${per} min + combinar`;
      out.textContent = `${w} ${w === 1 ? 'persona' : 'personas'} · cada una cuenta ${per} de ${cells.length} cajas · ≈ ${tiempo}`;
      d.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.w === w)));
    };
    d.querySelectorAll('button').forEach(b => b.addEventListener('click', () => draw(+b.dataset.w)));
    draw(3);
  });
})();
