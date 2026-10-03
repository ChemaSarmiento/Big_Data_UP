import mermaid from './vendor/mermaid/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base', themeVariables: { primaryColor: '#edf0ff', primaryTextColor: '#172139', primaryBorderColor: '#2345cc', lineColor: '#738096', fontFamily: 'Arial' } });
const $ = id => document.getElementById(id);
let decks = [], current, index = 0, renderVersion = 0;
const titles = html => { const el = document.createElement('div'); el.innerHTML = html; return el.querySelector('h1,h2')?.textContent || 'Diagrama y contexto'; };
function navigate(n) { if (current) location.hash = `${current.id}/${Math.max(0, Math.min(current.slides.length - 1, n)) + 1}`; }
async function route() {
  const [id, page] = location.hash.slice(1).split('/');
  current = decks.find(d => d.id === id);
  $('home').hidden = !!current; $('player').hidden = !current; $('catalog').hidden = !current;
  if (!current) { document.title = 'Big Data · Aula'; return; }
  index = Math.max(0, Math.min(current.slides.length - 1, (Number(page) || 1) - 1));
  document.title = `${current.title} · ${index + 1} · Big Data`;
  $('session-label').textContent = `${current.track === 'base' ? 'BASE COMPARTIDA' : current.track.toUpperCase() + ' / ' + current.number} — ${current.title}`;
  $('phase').textContent = index === 0 ? 'APERTURA' : index < 3 ? 'RUTA DE APRENDIZAJE' : /lab|paso|actividad|práctica/i.test(titles(current.slides[index])) ? 'PRÁCTICA' : /cierra|fin del|→|checkpoint/i.test(titles(current.slides[index])) ? 'CIERRE' : 'CONCEPTOS';
  const slide = $('slide'); slide.replaceChildren(); slide.innerHTML = current.slides[index];
  slide.className = index === 0 ? 'cover' : '';
  slide.querySelectorAll('img').forEach(img => { img.src = './infograficos/' + img.getAttribute('src').split('/').pop(); if (!img.alt) img.alt = img.src.split('/').pop().replace(/[_\.]/g, ' '); });
  slide.querySelectorAll('a').forEach(a => { const href = a.getAttribute('href'); if (href && !/^(https?:|#)/.test(href)) a.href = `https://github.com/ChemaSarmiento/Big_Data_UP/blob/plan2/${new URL(href, `https://source.invalid/${current.source}`).pathname.slice(1)}`; a.target = '_blank'; a.rel = 'noopener noreferrer'; });
  const groups = [...slide.children].filter(e => !e.matches('h1,h2,h3'));
  groups.forEach((e, i) => { e.classList.add('enter'); e.style.setProperty('--delay', `${Math.min(i, 6) * 120 + 100}ms`); });
  slide.querySelectorAll('.grid > div').forEach((e, i) => { e.classList.add('enter'); e.style.setProperty('--delay', `${Math.min(i, 6) * 120 + 180}ms`); });
  slide.querySelectorAll('li').forEach((e, i) => { e.classList.add('enter'); e.style.setProperty('--delay', `${Math.min(i, 8) * 100 + 180}ms`); });
  $('counter').textContent = `${String(index + 1).padStart(2, '0')} / ${String(current.slides.length).padStart(2, '0')}`;
  $('progress').style.width = `${(index + 1) / current.slides.length * 100}%`;
  $('previous').disabled = index === 0; $('next').disabled = index === current.slides.length - 1;
  $('stage').scrollTop = 0;
  const version = ++renderVersion;
  try { await mermaid.run({ nodes: slide.querySelectorAll('.mermaid') }); } catch { if (version === renderVersion) slide.querySelectorAll('.mermaid').forEach(e => e.classList.add('diagram-fallback')); }
  if (version === renderVersion && innerWidth > 800 && $('stage').scrollHeight > $('stage').clientHeight + 3) slide.classList.add('compact');
}
function overview() {
  if (!current) return;
  $('slide-list').replaceChildren(...current.slides.map((html, n) => { const b = document.createElement('button'); b.textContent = `${String(n + 1).padStart(2, '0')}  ${titles(html)}`; b.className = n === index ? 'selected' : ''; b.onclick = () => { $('overview').close(); navigate(n); }; return b; }));
  $('overview').showModal();
}
async function fullscreen() { try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch {} }
$('catalog').onclick = () => { location.hash = ''; };
$('previous').onclick = () => navigate(index - 1); $('next').onclick = () => navigate(index + 1);
$('stage').onclick = e => { if (!e.target.closest('a,button,input,pre')) navigate(index + 1); };
$('overview-button').onclick = overview; $('close-overview').onclick = () => $('overview').close(); $('fullscreen').onclick = fullscreen;
window.addEventListener('hashchange', route);
window.addEventListener('keydown', e => {
  if (!current || $('overview').open || e.target.closest('button,a,input,textarea,select')) return;
  if (['ArrowRight',' ','PageDown','ArrowLeft','PageUp','Home','End'].includes(e.key)) e.preventDefault();
  if (['ArrowRight',' ','PageDown'].includes(e.key)) navigate(index + 1);
  if (['ArrowLeft','PageUp'].includes(e.key)) navigate(index - 1);
  if (e.key === 'Home') navigate(0); if (e.key === 'End') navigate(current.slides.length - 1);
  if (e.key.toLowerCase() === 'o') overview(); if (e.key.toLowerCase() === 'f') fullscreen();
});
try {
  const response = await fetch('./decks.json'); if (!response.ok) throw new Error('No se pudo cargar el curso'); decks = await response.json();
  for (const d of decks) {
    const a = document.createElement('a'); a.className = 'deck'; a.href = `#${d.id}/1`; a.dataset.track = d.track;
    const label = document.createElement('span'); label.className = 'eyebrow'; label.textContent = d.track === 'base' ? 'EL PUNTO DE PARTIDA' : d.track.toUpperCase();
    const num = document.createElement('span'); num.className = 'deck-number'; num.textContent = d.number;
    const h = document.createElement('h2'); h.textContent = d.title;
    const meta = document.createElement('span'); meta.className = 'deck-meta'; meta.textContent = `${d.slides.length} diapositivas · Abrir sesión ↗`;
    a.append(label, num, h, meta); $('decks').append(a);
  }
  $('load-status').hidden = true;
  document.querySelectorAll('[data-track][aria-pressed]').forEach(b => b.onclick = () => { document.querySelectorAll('[data-track][aria-pressed]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); document.querySelectorAll('.deck').forEach(d => { d.hidden = b.dataset.track !== 'all' && d.dataset.track !== b.dataset.track; }); });
  await route();
} catch (error) { $('load-status').textContent = 'No se pudieron cargar las presentaciones. Sirve la carpeta dist mediante un servidor HTTP y recarga.'; console.error(error); }
