(() => {
 const claims=[
  ['«C cuesta 54 MXN por la canasta completa [F02].»','F02: C tiene 3/5 productos; 54 MXN es subtotal.','Contradicha. El costo completo de C es desconocido.'],
  ['«A cubre los cinco productos del ejemplo [F02].»','F02: A tiene 5/5 productos y costo completo 150 MXN.','Sustentada para el ejemplo ficticio del 2024-01-15.'],
  ['«Hoy hay existencias en A [F03].»','F03: no se observó inventario ni disponibilidad actual.','Sin respaldo. Hace falta una fuente vigente de existencias.']
 ];
 document.querySelectorAll('[data-audit]').forEach(d=>{
  let selected=0;
  d.querySelectorAll('[data-claim]').forEach(b=>b.addEventListener('click',()=>{
   selected=Number(b.dataset.claim);
   d.querySelectorAll('[data-claim]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
   d.querySelector('[data-claim-text]').textContent=claims[selected][0];
   d.querySelector('[data-claim-evidence]').textContent=claims[selected][1];
   d.querySelector('[data-claim-verdict]').hidden=true;
  }));
  d.querySelector('[data-audit-reveal]').addEventListener('click',()=>{
   const v=d.querySelector('[data-claim-verdict]');v.textContent=claims[selected][2];v.hidden=false;
  });
 });
})();
