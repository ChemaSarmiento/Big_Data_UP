// Chromium instalado en slides_maestria. Servir presentaciones-v2 en localhost:4183.
import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const out=process.env.EDITORIAL_QA_DIR||'/tmp/bigdata-editorial';fs.mkdirSync(out,{recursive:true});
const root='http://127.0.0.1:4183';
const manifest=JSON.parse(fs.readFileSync(new URL('../editorial/manifest.json',import.meta.url)));
const report={slides:0,viewports:[],errors:[],requests:[],layout:[],checks:[]};
const b=await chromium.launch({headless:true});
try{
 const p=await b.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
 p.on('pageerror',e=>report.errors.push(e.message));p.on('requestfailed',r=>report.requests.push(r.url()));
 p.on('response',r=>{if(r.status()>=400)report.requests.push(`${r.status()} ${r.url()}`)});
 for(const viewport of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844}]){
  report.viewports.push(viewport);await p.setViewportSize(viewport);
  for(const n of Object.keys(manifest).map(Number)){
   await p.goto(`${root}/especialidad-0${n}/`);await p.evaluate(()=>document.fonts.ready);
   const count=await p.locator('.slide').count();assert.equal(count,manifest[n].slides);if(viewport.width===1440)report.slides+=count;
   assert.equal(await p.locator('.slide h1').count(),count);
   for(let i=1;i<=count;i++){
    await p.evaluate(i=>location.hash=`#${i}/99`,i);await p.waitForFunction(i=>document.querySelector('.slide:not([hidden])')?.dataset.id.endsWith('-'+String(i).padStart(2,'0')),i);
    const r=await p.locator('.slide:not([hidden])').evaluate(s=>{
     const c=s.querySelector('.content'),box=c.getBoundingClientRect(),rect=s.getBoundingClientRect();const children=[...c.children].filter(x=>getComputedStyle(x).display!=='none').map(x=>x.getBoundingClientRect());
     const visible=[...s.querySelectorAll('h1,p,td,th,pre,.node,.eyebrow')].filter(x=>x.getBoundingClientRect().width>0&&getComputedStyle(x).visibility!=='hidden');
     return {horizontal:document.documentElement.scrollWidth>innerWidth+2,slideOverflow:s.scrollHeight>s.clientHeight+2,frame:innerWidth>700&&s.clientHeight!==900,contentOverflow:children.some(x=>x.bottom>box.bottom+3||x.top<box.top-3||x.right>box.right+3||x.left<box.left-3),sourceOverlap:children.some(x=>x.bottom>s.querySelector('.source').getBoundingClientRect().top-5),title:s.dataset.title,darkContrast:s.classList.contains('dark')&&getComputedStyle(s.querySelector('h1')).color!=='rgb(241, 239, 233)',blank:c.innerText.trim().length<8&&!c.querySelector('svg')};
    });
    if(Object.entries(r).some(([k,v])=>k!=='title'&&v===true))report.layout.push({n,i,viewport,...r});
    if(viewport.width===1440&&[1,2,3,7,11,12,19].includes(i))await p.screenshot({path:`${out}/s${n}-${i}.png`});
    if(viewport.width===390&&i===1)await p.screenshot({path:`${out}/s${n}-mobile.png`});
   }
  }
 }
 await p.setViewportSize({width:1440,height:900});
 const go=async(n,i,step=0)=>{await p.goto(`${root}/especialidad-0${n}/#${i}/${step}`);await p.waitForFunction(i=>document.querySelector('.slide:not([hidden])')?.dataset.id.endsWith('-'+String(i).padStart(2,'0')),i)};
 await go(1,2);assert.equal(await p.locator('.slide:not([hidden]) [data-step="1"]').first().getAttribute('aria-hidden'),'true');
 await p.keyboard.press('ArrowRight');await p.waitForFunction(()=>location.hash==='#2/1');await p.waitForTimeout(30);assert.equal(await p.locator('.slide:not([hidden]) [data-step="1"]').first().getAttribute('aria-hidden'),null);
 await p.keyboard.press('ArrowLeft');await p.waitForFunction(()=>location.hash==='#2/0');
 await p.locator('#show-all').click();await p.waitForFunction(()=>location.hash==='#2/2');await p.reload();assert.equal(await p.locator('#counter').textContent(),'02 / 27');
 await p.locator('#index-button').click();assert.equal(await p.locator('#slide-list li').count(),27);await p.locator('#overview [data-close]').click();
 await p.locator('#notes-button').click();assert.match(await p.locator('#notes-text').textContent(),/votar/);await p.locator('#notes [data-close]').click();
 await p.locator('#lab-button').click();assert.equal(await p.locator('#lab a').first().getAttribute('href'),'laboratorio.html');await p.locator('#lab [data-close]').click();
 await go(1,15);await p.locator('[data-quiz] button').first().click();assert.match(await p.locator('.slide:not([hidden]) .answer').textContent(),/medir memoria/);assert.equal(new URL(p.url()).hash,'#15/0');
 await go(2,7);await p.locator('[data-filter-demo]').click();assert.equal(await p.locator('[data-sql-demo] tbody tr:visible').count(),2);assert.match(await p.locator('[data-demo-query]').textContent(),/1995/);await p.locator('[data-reset-demo]').click();assert.equal(await p.locator('[data-sql-demo] tbody tr:visible').count(),4);
 await p.locator('[data-demo-query]').evaluate(el=>{const r=document.createRange();r.selectNodeContents(el);getSelection().removeAllRanges();getSelection().addRange(r)});
 await p.locator('[data-demo-query]').click();assert.equal(new URL(p.url()).hash,'#7/0');
 await go(2,12);assert.equal(await p.locator('[data-employees-join] tbody tr:visible').count(),1);await p.locator('[data-left-demo]').click();assert.equal(await p.locator('[data-employees-join] tbody tr:visible').count(),2);assert.match(await p.locator('[data-join-answer]').textContent(),/NULL/);
 await go(3,13);await p.locator('[data-limit-demo]').click();assert.equal(await p.locator('[data-limit-value]').textContent(),'1');assert.equal(await p.locator('[data-scan-demo] .dots span').count(),16);
 await go(4,2);await p.locator('[data-price-toggle]').click();assert.equal(await p.locator('[data-zero-status]').textContent(),'Excluida');assert.match(await p.locator('[data-price-answer]').textContent(),/A40/);assert.equal(new URL(p.url()).hash,'#2/0');await p.locator('[data-price-toggle]').click();assert.equal(await p.locator('[data-zero-status]').textContent(),'Por revisar');
 await go(4,10);await p.locator('[data-silver-toggle]').click();assert.equal(await p.locator('.row-tokens.classified [data-disposition=accepted]').count(),13);assert.equal(await p.locator('.row-tokens.classified [data-disposition=rejected]').count(),2);assert.equal(await p.locator('.row-tokens.classified [data-disposition=copy]').count(),1);assert.match(await p.locator('[data-ledger-equation]').textContent(),/16 = 13 aceptadas/);await p.screenshot({path:`${out}/s4-reconciliacion.png`});
 await go(4,14);await p.locator('[data-partition-toggle]').click();assert.equal(await p.locator('.partition-drawers .skipped').count(),2);assert.equal(await p.locator('.partition-drawers .selected').count(),1);
 report.checks.push('S4: precio cero, reconciliación16/13/2/1 y selección de particiones');
 await go(5,2);await p.locator('[data-gold-toggle]').click();assert.match(await p.locator('[data-gold-answer]').textContent(),/costo completo NULL/);assert.equal(new URL(p.url()).hash,'#2/0');
 await go(5,8);assert.equal(await p.locator('[data-gold-join] tbody tr:visible').count(),3);await p.locator('[data-gold-join-toggle]').click();assert.equal(await p.locator('[data-gold-join] tbody tr:visible').count(),5);assert.match(await p.locator('[data-gold-join-answer]').textContent(),/3\/5/);
 report.checks.push('S5: elegibilidad de canasta y LEFT JOIN que conserva faltantes');
 await go(6,4);await p.locator('[data-bi-filter]').selectOption('C');assert.match(await p.locator('[data-bi-title]').textContent(),/No hay una canasta completa/);assert.equal(await p.locator('[data-bi-cost]').textContent(),'Sin costo completo');assert.equal(await p.locator('[data-bi-count]').textContent(),'0 / 1');assert.equal(new URL(p.url()).hash,'#4/0');await p.locator('[data-bi-filter]').selectOption('B');assert.equal(await p.locator('[data-bi-cost]').textContent(),'160 MXN');await p.locator('[data-bi-filter]').selectOption('all');assert.equal(await p.locator('[data-bi-rows] tr').count(),3);await p.screenshot({path:`${out}/s6-tablero.png`});
 await go(6,2);await p.locator('[data-bi-redesign-toggle]').click();assert.match(await p.locator('[data-bi-heading]').textContent(),/canastas completas/);
 await p.goto(`${root}/especialidad-06/practica.html`);await p.locator('[data-bi-filter]').selectOption('C');assert.equal(await p.locator('[data-bi-cost]').textContent(),'Sin costo completo');
 report.checks.push('S6: título por filtro, costo desconocido, comparación corregida y práctica independiente');
 await go(7,11);
 const audit=p.locator('.slide:visible [data-audit]');
 for(const [n,expected] of [[0,/Contradicha/],[1,/Sustentada/],[2,/Sin respaldo/]]){
  await audit.locator(`[data-claim="${n}"]`).click();assert.ok(await audit.locator('[data-claim-verdict]').isHidden());
  await audit.locator('[data-audit-reveal]').click();assert.match(await audit.locator('[data-claim-verdict]').innerText(),expected);assert.ok(p.url().endsWith('#11/0'));
 }
 await p.screenshot({path:`${out}/s7-auditoria.png`});
 await p.goto(`${root}/especialidad-07/practica.html`);
 for(const [query,pattern] of [['cobertura',/F0[12]/],['inventario',/F03/]]){
  await p.locator('[data-search]').fill(query);await p.locator('[data-search-button]').click();
  assert.match(await p.locator('[data-search-results]').innerText(),pattern);
 }
 await p.locator('[data-search-results] summary').first().click();assert.ok((await p.locator('[data-search-results] details[open] p').innerText()).length>30);
 await p.locator('[data-search]').fill('temperatura marte');await p.locator('[data-search-button]').click();assert.equal(await p.locator('[data-search-results] details').count(),0);
 assert.match(await p.locator('.demo-answer').innerText(),/No se recuperó/);
 report.checks.push('S7: auditoría de citas, búsqueda pertinente y ausencia de resultados en práctica local');
 report.checks.push('Revelado, retroceso, recarga, índice, notas, guía, copia/selección, filtro, INNER/LEFT y LIMIT');
 // Default motion actually fades; reduced-motion was used for exhaustive layout.
 await p.emulateMedia({reducedMotion:'no-preference'});await go(1,1);await p.keyboard.press('ArrowRight');await p.waitForTimeout(80);assert.ok(await p.locator('.slide.fade-out').count());await p.waitForTimeout(230);assert.equal(await p.locator('#counter').textContent(),'02 / 27');
 await p.emulateMedia({reducedMotion:'reduce'});report.checks.push('Fade manual y prefers-reduced-motion');
 // Links resolve locally and fragments point to existing anchors.
 for(const n of Object.keys(manifest).map(Number)){
  await p.goto(`${root}/especialidad-0${n}/laboratorio.html`);
  const paths=await p.locator('a[href]').evaluateAll(xs=>xs.map(x=>x.href).filter(x=>x.startsWith(location.origin)));
  for(const url of new Set(paths)){const r=await p.request.get(url);assert.equal(r.status(),200,url)}
  assert.equal(await p.locator('section[id^="paso-"]').count(),6);
 }
 await p.goto(`${root}/especialidad-01/ficha-proyecto.html`);await p.locator('[name=dataset]').fill('QA · biblioteca');await p.locator('[name=evidence]').fill('Comparar préstamos por formato durante 2024');await p.locator('[name=map]').fill('Bronze fuente; Silver fechas; Gold por formato');
 const download=p.waitForEvent('download');await p.locator('button[type=submit]').click();const d=await download;assert.equal(d.suggestedFilename(),'registro-h1.json');await d.saveAs(`${out}/registro-h1.json`);await p.reload();assert.equal(await p.locator('[name=dataset]').inputValue(),'QA · biblioteca');
 report.checks.push('Enlaces de guías, ficha H1 persistente y descarga');
 // A PDF is a review artifact, not proof of a cloud run.
 for(const n of Object.keys(manifest).map(Number)){
  await p.goto(`${root}/especialidad-0${n}/`);await p.evaluate(()=>document.fonts.ready);await p.pdf({path:`${out}/sesion-${n}-editorial.pdf`,printBackground:true,preferCSSPageSize:true});
 }
 await p.goto(root);assert.equal(await p.locator('.course-card').count(),8);await p.screenshot({path:`${out}/catalogo.png`,fullPage:true});
 report.checks.push('PDFs de las sesiones editoriales y catálogo de ocho');
}finally{await b.close();fs.writeFileSync(`${out}/report.json`,JSON.stringify(report,null,2))}
assert.deepEqual(report.errors,[]);assert.deepEqual(report.requests,[]);assert.deepEqual(report.layout,[]);console.log(JSON.stringify(report,null,2));
