(() => {
  'use strict';
  document.querySelectorAll('[data-demo="inner-left"]').forEach(d => {
    const btns = [...d.querySelectorAll('[data-mode]')];
    const rows = [...d.querySelectorAll('[data-join-table] tbody tr')];
    const sqls = [...d.querySelectorAll('[data-sql]')];
    const msg = d.querySelector('[data-msg]');
    const set = mode => {
      btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
      rows.forEach(r => { r.hidden = mode === 'inner' && r.dataset.left === '1'; });
      sqls.forEach(s => { s.hidden = s.dataset.sql !== mode; });
      msg.textContent = mode === 'inner'
        ? 'INNER: 3 filas. Quien no es gerente desaparece sin avisar. En la tabla completa: 24 filas de 300,024 personas.'
        : 'LEFT: 6 filas. Quien no es gerente se queda, con NULL en dept_no. En la tabla completa: 300,024 filas, 300,000 con NULL.';
    };
    btns.forEach(b => b.addEventListener('click', () => set(b.dataset.mode)));
    set('inner');
  });
})();
