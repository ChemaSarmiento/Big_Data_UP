(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const slides = [...document.querySelectorAll('.slide')];
  const counts = slides.map(s => Math.max(0, ...[...s.querySelectorAll('[data-step]')].map(e => Number(e.dataset.step))));
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = -1, step = 0, version = 0, pointerHadSelection = false;
  const clamp = (n, max) => Math.max(0, Math.min(max, n));
  function parseRoute() {
    const parts = location.hash.slice(1).split('/');
    const index = clamp((parseInt(parts[0], 10) || 1) - 1, slides.length - 1);
    return [index, clamp(parseInt(parts[1], 10) || 0, counts[index])];
  }
  function updateSteps() {
    slides[current].querySelectorAll('[data-step]').forEach(el => {
      const hidden = Number(el.dataset.step) > step;
      el.classList.toggle('unrevealed', hidden);
      el.inert = hidden;
      if (hidden) el.setAttribute('aria-hidden', 'true'); else el.removeAttribute('aria-hidden');
    });
    $('counter').textContent = `${String(current + 1).padStart(2, '0')} / ${slides.length}`;
    $('step-counter').textContent = `Revelado ${step} de ${counts[current]}`;
    $('section-label').textContent = slides[current].dataset.title;
    $('previous').disabled = current === 0 && step === 0;
    $('next').disabled = current === slides.length - 1 && step === counts[current];
    const all = step === counts[current];
    $('show-all').textContent = all ? 'Reiniciar pasos' : 'Mostrar todo';
    $('show-all').setAttribute('aria-pressed', String(all));
    $('show-all').disabled = counts[current] === 0;
    $('progress').style.width = `${((current + (step + 1) / (counts[current] + 1)) / slides.length) * 100}%`;
    $('notes-text').textContent = slides[current].dataset.note;
    $('slide-list').querySelectorAll('button').forEach((button, i) => { if (i === current) button.setAttribute('aria-current', 'step'); else button.removeAttribute('aria-current'); });
    document.title = `${current + 1}. ${slides[current].dataset.title} · Big Data`;
  }
  async function render() {
    const token = ++version;
    const [target, targetStep] = parseRoute();
    if (current !== target && current >= 0 && !reduced.matches) {
      slides[current].classList.add('fade-out');
      await new Promise(resolve => setTimeout(resolve, 180));
      if (token !== version) return;
    }
    const changed = current !== target;
    current = target; step = targetStep;
    slides.forEach((s, i) => { s.hidden = i !== current; s.classList.remove('fade-out', 'fade-in'); });
    if (changed) { slides[current].classList.add('fade-in'); $('stage').scrollTop = 0; }
    updateSteps();
  }
  function go(index, newStep = 0) {
    const target = clamp(index, slides.length - 1);
    const hash = `#${target + 1}/${clamp(newStep, counts[target])}`;
    if (location.hash === hash) return;
    location.hash = hash;
  }
  function next() { if (step < counts[current]) go(current, step + 1); else if (current < slides.length - 1) go(current + 1); }
  function previous() { if (step > 0) go(current, step - 1); else if (current > 0) go(current - 1, counts[current - 1]); }
  const openDialog = id => { const d = $(id); if (!d.open) d.showModal(); };
  slides.forEach((slide, i) => {
    const li = document.createElement('li'), button = document.createElement('button');
    button.textContent = slide.dataset.title;
    button.addEventListener('click', () => { $('overview').close(); go(i); });
    li.append(button); $('slide-list').append(li);
  });
  $('next').addEventListener('click', next); $('previous').addEventListener('click', previous);
  $('stage').addEventListener('pointerdown', () => { pointerHadSelection = Boolean(window.getSelection()?.toString()); });
  $('stage').addEventListener('click', e => {
    const hadSelection = pointerHadSelection; pointerHadSelection = false;
    if (e.target.closest('button,a,input,textarea,select,label,pre,code,form') || hadSelection || window.getSelection()?.toString()) return;
    next();
  });
  document.addEventListener('keydown', e => {
    if (e.target.closest('input,textarea,select,pre,code,[contenteditable="true"]') || document.querySelector('dialog[open]') || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest('button,a') && [' ', 'Enter'].includes(e.key)) return;
    if (['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) { e.preventDefault(); previous(); }
    else if (e.key === 'Home') { e.preventDefault(); go(0); }
    else if (e.key === 'End') { e.preventDefault(); go(slides.length - 1, counts.at(-1)); }
    else if (e.key.toLowerCase() === 'o') openDialog('overview');
    else if (e.key.toLowerCase() === 'l') openDialog('lab');
    else if (e.key.toLowerCase() === 'f') toggleFullscreen();
  });
  async function toggleFullscreen() {
    try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); }
    catch { $('section-label').textContent = 'Pantalla completa no disponible en este navegador'; }
  }
  $('fullscreen').addEventListener('click', toggleFullscreen);
  $('index-button').addEventListener('click', () => openDialog('overview'));
  $('notes-button').addEventListener('click', () => openDialog('notes'));
  $('lab-button').addEventListener('click', () => openDialog('lab'));
  document.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', () => b.closest('dialog').close()));
  $('show-all').addEventListener('click', () => go(current, step === counts[current] ? 0 : counts[current]));
  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('[inert]')];
    printState.forEach(e => { e.inert = false; e.removeAttribute('aria-hidden'); });
  });
  window.addEventListener('afterprint', () => { printState.forEach(e => e.inert = true); updateSteps(); });
  $('print-button').addEventListener('click', () => { $('overview').close(); window.print(); });

  function copyText(text, target) {
    navigator.clipboard?.writeText(text).then(()=>{target.textContent='Copiado.';}).catch(()=>{target.textContent='Selecciona y copia el texto manualmente.';});
    if(!navigator.clipboard)target.textContent='Selecciona y copia el texto manualmente.';
  }
  document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>copyText($(b.dataset.copy).textContent,b.parentElement.querySelector('.copy-status'))));
  document.querySelectorAll('[data-timer]').forEach(d=>{
    let remaining=420,running=false;const out=d.querySelector('output');
    const draw=()=>{out.textContent=String(Math.floor(remaining/60)).padStart(2,'0')+':'+String(remaining%60).padStart(2,'0');};
    d.querySelector('[data-timer-start]').addEventListener('click',e=>{running=!running;e.currentTarget.setAttribute('aria-pressed',String(running));});
    d.querySelector('[data-timer-reset]').addEventListener('click',()=>{remaining=420;running=false;d.querySelector('[data-timer-start]').setAttribute('aria-pressed','false');draw();});
    d.querySelector('[data-timer-questions]').addEventListener('click',()=>{remaining=180;running=false;d.querySelector('[data-timer-start]').setAttribute('aria-pressed','false');draw();});
    setInterval(()=>{if(running&&remaining>0){remaining--;draw();}if(remaining===0)running=false;},1000);
  });
  window.addEventListener("hashchange", render); document.body.classList.add("ready"); render();
})();
