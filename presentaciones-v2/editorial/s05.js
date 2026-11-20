// S5 · demo del umbral de hashtags: solo cambia las cifras mostradas; no mueve la presentación.
document.querySelectorAll('[data-demo="s5-umbral"]').forEach(root => {
  const datos = {
    25:   ['2,261', '10,636', '2,397,514', '71.8 %', 71.8],
    100:  ['525', '2,809', '2,040,484', '61.1 %', 61.1],
    500:  ['97', '614', '1,587,781', '47.5 %', 47.5],
    2000: ['21', '128', '1,115,421', '33.4 %', 33.4]
  };
  const campos = ['hashtags', 'filas', 'menciones', 'pct'];
  root.querySelectorAll('[data-u]').forEach(boton => {
    boton.addEventListener('click', () => {
      const d = datos[boton.dataset.u];
      root.querySelectorAll('[data-u]').forEach(b => b.setAttribute('aria-pressed', String(b === boton)));
      campos.forEach((c, i) => { root.querySelector(`[data-out="${c}"]`).textContent = d[i]; });
      root.querySelector('[data-bar]').style.width = d[4] + '%';
    });
  });
});
