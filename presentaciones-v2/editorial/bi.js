(() => {
 'use strict';
 const rows=[{store:'A',found:5,cost:150},{store:'B',found:5,cost:160},{store:'C',found:3,cost:null}];
 document.querySelectorAll('[data-bi-board]').forEach(d=>{
  const select=d.querySelector('[data-bi-filter]');
  const draw=()=>{const chosen=rows.filter(r=>select.value==='all'||r.store===select.value);const full=chosen.filter(r=>r.cost!==null);const best=full.slice().sort((a,b)=>a.cost-b.cost)[0];
   d.querySelector('[data-bi-title]').textContent=best?`${best.store} tiene el menor costo entre las canastas completas visibles.`:'No hay una canasta completa entre las tiendas visibles.';
   d.querySelector('[data-bi-cost]').textContent=best?`${best.cost} MXN`:'Sin costo completo';
   d.querySelector('[data-bi-count]').textContent=`${full.length} / ${chosen.length}`;
   const body=d.querySelector('[data-bi-rows]');body.replaceChildren();chosen.forEach(r=>{const tr=document.createElement('tr');[r.store,`${r.found}/5`,r.cost===null?'Sin dato completo':`${r.cost} MXN`].forEach(t=>{const td=document.createElement('td');td.textContent=t;tr.append(td)});body.append(tr)});
   d.querySelector('[data-bi-note]').textContent=chosen.some(r=>r.store==='C')?'C: subtotal 54 MXN de tres productos; fuera del ranking completo.':`Selección: ${select.value}. El resultado no describe tiendas excluidas por el filtro.`;
  };select.addEventListener('change',draw);draw();
 });
 document.querySelectorAll('[data-bi-redesign]').forEach(d=>d.querySelector('button').addEventListener('click',e=>{
  const on=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'Ver mensaje defectuoso':'Corregir el mensaje';
  d.querySelector('[data-bi-heading]').textContent=on?'A tiene el menor costo entre las canastas completas del escenario.':'«C ofrece la compra más barata:54 MXN»';
  const area=d.querySelector('[data-bi-evidence]');area.replaceChildren();const big=document.createElement('p');big.className='large signal';big.textContent=on?'A150 · B160 MXN':'54 MXN';const text=document.createElement('p');text.textContent=on?'C:3/5, subtotal 54 MXN; sin costo completo.':'El subtotal se presenta como canasta completa.';area.append(big,text);
  d.querySelector('[data-bi-explanation]').textContent=on?'Mismo catálogo y fecha histórica. La cobertura define qué se puede comparar.':'La cifra existe, pero la conclusión omite dos productos.';
 }));
})();
