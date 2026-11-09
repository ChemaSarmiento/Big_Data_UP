(() => {
 const options={warehouse:['Fuentes → BigQuery → BI','Datos estructurados y consumo analítico en SQL.','Operación acotada; requiere contratos claros de carga y métricas.'],lake:['Archivos en GCS → tablas en BigQuery → BI','Conserva originales y sirve datos preparados para consulta.','Gobierna copias, versiones y sincronización entre almacenamiento y tablas.'],lakehouse:['Objetos + tablas abiertas + catálogo → motores → consumo','Varios motores necesitan compartir datos gobernados en formatos compatibles.','Más decisiones de catálogo, permisos y compatibilidad; justificar esa necesidad.']};
 document.querySelectorAll('[data-architecture]').forEach(d=>d.querySelectorAll('[data-arch]').forEach(b=>b.addEventListener('click',()=>{
 const a=options[b.dataset.arch];['title','use','cost'].forEach((k,i)=>d.querySelector(`[data-arch-${k}]`).textContent=a[i]);d.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
 })));
 document.querySelectorAll('[data-scan-model]').forEach(d=>d.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
 const month=b.dataset.scanMode==='month';d.querySelectorAll('.month-blocks>div').forEach((x,i)=>x.classList.toggle('muted-block',month&&i!==2));
 d.querySelector('[data-scan-result]').textContent=month?'Modelo didáctico: el filtro de marzo conserva una de doce particiones.':b.dataset.scanMode==='limit'?'LIMIT 10 reduce la salida; las doce particiones siguen en la lectura de este modelo.':'Modelo didáctico: se leen las doce particiones.';
 d.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
 })));
})();
