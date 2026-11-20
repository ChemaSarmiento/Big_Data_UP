// S3 · explorador de estimaciones de costo (valores de referencia del curso; ver s03.py).
(function(){
  function init(root){
    var items=JSON.parse(root.getAttribute('data-items'));
    var buttons=root.querySelectorAll('[data-q]');
    var sql=root.querySelector('[data-qsql]'),est=root.querySelector('[data-est]'),real=root.querySelector('[data-real]'),verdict=root.querySelector('[data-verdict]');
    function show(i){
      var it=items[i];
      buttons.forEach(function(b,j){b.setAttribute('aria-pressed',j===i?'true':'false')});
      sql.textContent=it.sql;est.textContent=it.est;real.textContent=it.real;verdict.textContent=it.verdict;
    }
    buttons.forEach(function(b,j){b.addEventListener('click',function(ev){ev.stopPropagation();show(j)})});
    show(0);
  }
  function boot(){document.querySelectorAll('[data-demo="costos"]').forEach(init)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
