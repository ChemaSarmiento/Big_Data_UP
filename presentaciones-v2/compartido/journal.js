(() => {
 'use strict';
 const form=document.getElementById('journal-form');if(!form)return;
 const session=document.body.dataset.session;
 const key=`bigdata-plan3-h${session}-registro`;
 const fields=[...form.querySelectorAll('input[name],textarea[name]')];
 const status=document.getElementById('journal-status');
 let closedDetails=[];
 window.addEventListener('beforeprint',()=>{closedDetails=[...document.querySelectorAll('details:not([open])')];closedDetails.forEach(d=>d.open=true);});
 window.addEventListener('afterprint',()=>{closedDetails.forEach(d=>d.open=false);});
 const values=()=>Object.fromEntries(fields.map(f=>[f.name,f.value]));
 try{const data=JSON.parse(localStorage.getItem(key)||'{}');fields.forEach(f=>{if(typeof data[f.name]==='string')f.value=data[f.name].slice(0,f.maxLength);});}catch{}
 form.addEventListener('input',()=>{try{localStorage.setItem(key,JSON.stringify(values()));status.textContent='Guardado solo en este navegador.';}catch{status.textContent='Descarga el archivo para conservar tu registro.';}});
 form.addEventListener('submit',e=>{
  e.preventDefault();const data={hito:`H${session}`,fecha:new Date().toISOString(),...values()};
  const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=`registro-h${session}.json`;a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='Registro descargado; no enviado a un servidor.';
 });
})();
