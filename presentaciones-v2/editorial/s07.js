(() => {
 document.querySelectorAll('[data-demo="orden"]').forEach(d => {
  const botones = d.querySelectorAll('[data-set]');
  botones.forEach(b => b.addEventListener('click', () => {
   botones.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
   d.querySelectorAll('[data-set-panel]').forEach(p => { p.hidden = p.dataset.setPanel !== b.dataset.set; });
  }));
 });
 document.querySelectorAll('[data-demo="audit"]').forEach(d => {
  const botones = d.querySelectorAll('[data-claim]');
  botones.forEach(b => b.addEventListener('click', () => {
   botones.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
   d.querySelectorAll('[data-claim-panel]').forEach(p => { p.hidden = p.dataset.claimPanel !== b.dataset.claim; });
  }));
 });
})();
