// Demostraciones locales del fixture. No ejecuta SQL, modifica datos ni llama GCP.
(() => {
 'use strict';
 document.querySelectorAll('[data-price-rule]').forEach(d=>d.querySelector('[data-price-toggle]').addEventListener('click',e=>{
  const applied=e.currentTarget.getAttribute('aria-pressed')!=='true';
  e.currentTarget.setAttribute('aria-pressed',String(applied));e.currentTarget.textContent=applied?'Volver al precio crudo':'Exigir precio mayor que cero';
  d.querySelector('[data-zero-row]').classList.toggle('excluded',applied);
  d.querySelector('[data-zero-status]').textContent=applied?'Excluida':'Por revisar';
  d.querySelector('[data-price-answer]').textContent=applied?'A40 es el menor precio válido del ejemplo. C queda sin precio válido para p4.':'Ordenar el precio crudo pondría a C primero.';
 }));
 document.querySelectorAll('[data-silver-ledger]').forEach(d=>d.querySelector('[data-silver-toggle]').addEventListener('click',e=>{
  const applied=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(applied));
  e.currentTarget.textContent=applied?'Volver a las filas recibidas':'Aplicar reglas del fixture';d.querySelector('.row-tokens').classList.toggle('classified',applied);
  d.querySelector('[data-ledger-equation]').textContent=applied?'16 = 13 aceptadas + 2 rechazadas + 1 copia':'16 recibidas';
  d.querySelector('[data-ledger-answer]').textContent=applied?'C4: precio inválido. C5: fecha inválida. A1′: copia exacta. Cada fila tiene un destino.':'Todavía no se aplican reglas. A1′ representa la copia exacta de A1.';
 }));
 document.querySelectorAll('[data-partition-demo]').forEach(d=>d.querySelector('[data-partition-toggle]').addEventListener('click',e=>{
  const selected=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(selected));e.currentTarget.textContent=selected?'Ver todos los meses':'Consultar solo enero';
  d.querySelectorAll('[data-month]').forEach(x=>{x.classList.toggle('skipped',selected&&x.dataset.month!=='01');x.classList.toggle('selected',selected&&x.dataset.month==='01');});
  d.querySelector('[data-partition-answer]').textContent=selected?'El filtro elegible conserva enero y permite descartar los otros meses del modelo.':'Sin acotar fecha, esta representación considera los tres meses.';
 }));
})();
