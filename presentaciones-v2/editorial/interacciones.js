(() => {
  'use strict';
  const stage=document.getElementById('stage');
  const viewport=document.getElementById('viewport');
  function fit(){
    if(innerWidth<=700){stage.style.transform='none';return;}
    const scale=Math.min(viewport.clientWidth/1600,viewport.clientHeight/900);
    stage.style.transform=`scale(${scale})`;
    stage.style.left=`${(viewport.clientWidth-1600*scale)/2}px`;
    stage.style.top=`${(viewport.clientHeight-900*scale)/2}px`;
  }
  addEventListener('resize',fit);document.fonts.ready.then(fit);fit();
  document.querySelectorAll('[data-quiz]').forEach(q=>q.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
    q.parentElement.querySelector('.answer').textContent=b.dataset.answer;
    q.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  })));
  document.querySelectorAll('[data-sql-demo]').forEach(d=>{
    const rows=[...d.querySelectorAll('tbody tr')];
    const draw=filtered=>{
      rows.forEach((r,i)=>r.hidden=filtered&&(i===0||i===3));
      d.querySelector('[data-demo-query]').textContent=filtered?"SELECT emp_no, hire_date\nFROM employees\nWHERE hire_date >= '1990-01-01'\n  AND hire_date < '1995-01-01';":"SELECT emp_no, hire_date\nFROM employees;";
      d.querySelector('[data-demo-count]').textContent=filtered?'2 filas cumplen el intervalo; 1995 queda fuera.':'4 filas antes del filtro.';
      d.querySelector('[data-filter-demo]').setAttribute('aria-pressed',String(filtered));
    };
    d.querySelector('[data-filter-demo]').addEventListener('click',()=>draw(true));
    d.querySelector('[data-reset-demo]').addEventListener('click',()=>draw(false));
  });
  document.querySelectorAll('[data-employees-join]').forEach(d=>{
    const row=d.querySelector('tbody tr:last-child');row.hidden=true;
    d.querySelector('[data-left-demo]').addEventListener('click',e=>{
      const left=row.hidden;row.hidden=!left;e.currentTarget.setAttribute('aria-pressed',String(left));
      e.currentTarget.textContent=left?'Cambiar a INNER JOIN':'Cambiar a LEFT JOIN';
      d.querySelector('[data-join-answer]').textContent=left?'LEFT JOIN: Luis se conserva; NULL indica ausencia de coincidencia.':'INNER JOIN: Ana aparece; Luis queda fuera.';
    });
  });
  document.querySelectorAll('[data-scan-demo]').forEach(d=>d.querySelector('[data-limit-demo]').addEventListener('click',e=>{
    const one=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(one));
    e.currentTarget.textContent=one?'Restablecer LIMIT 10':'Cambiar LIMIT 10 a LIMIT 1';
    d.querySelector('[data-limit-value]').textContent=one?'1':'10';
    d.querySelector('[data-limit-answer]').textContent=one?'Cambió la salida. Este modelo conserva la lectura para mostrar que LIMIT no la acota.':'El límite de salida no establece un límite de lectura.';
  }));
  addEventListener('hashchange',()=>{viewport.scrollTop=0;});
})();
