// Chromium instalado en slides_maestria. Servir presentaciones-v2 en localhost:4183.
import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const out=process.env.EDITORIAL_QA_DIR||'/tmp/bigdata-editorial';fs.mkdirSync(out,{recursive:true});
const root='http://127.0.0.1:4183';
const manifest=JSON.parse(fs.readFileSync(new URL('../editorial/manifest.json',import.meta.url)));
const only=(process.env.ONLY||'').split(',').filter(Boolean).map(Number);const ids=only.length?only:Object.keys(manifest).map(Number);const report={slides:0,viewports:[],errors:[],requests:[],layout:[],checks:[]};
const b=await chromium.launch({headless:true});
try{
 const p=await b.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
 p.on('pageerror',e=>report.errors.push(e.message));p.on('requestfailed',r=>report.requests.push(r.url()));
 p.on('response',r=>{if(r.status()>=400)report.requests.push(`${r.status()} ${r.url()}`)});
 for(const viewport of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844}]){
  report.viewports.push(viewport);await p.setViewportSize(viewport);
  for(const n of ids){
   await p.goto(`${root}/especialidad-0${n}/`);await p.evaluate(()=>document.fonts.ready);
   const count=await p.locator('.slide').count();if(!only.length)assert.equal(count,manifest[n].slides);if(viewport.width===1440)report.slides+=count;
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
 const has=n=>ids.includes(n);let cur=0;
 const go=async(n,i,step=0)=>{cur=i;await p.goto(`${root}/especialidad-0${n}/#${i}/${step}`);await p.waitForFunction(i=>document.querySelector('.slide:not([hidden])')?.dataset.id.endsWith('-'+String(i).padStart(2,'0')),i)};
 const goSel=async(n,sel)=>{await p.goto(`${root}/especialidad-0${n}/`);await p.evaluate(()=>document.fonts.ready);const i=await p.evaluate(s=>[...document.querySelectorAll('.slide')].findIndex(x=>x.querySelector(s))+1,sel);assert.ok(i>0,'sin slide con '+sel);await go(n,i);return i};
 const nav=ids[0];let tot=0;{const i=await goSel(nav,'[data-step="2"]');tot=await p.locator('.slide').count();assert.equal(await p.locator('.slide:not([hidden]) [data-step="1"]').first().getAttribute('aria-hidden'),'true');
 await p.keyboard.press('ArrowRight');await p.waitForFunction(i=>location.hash===`#${i}/1`,i);await p.waitForTimeout(30);assert.equal(await p.locator('.slide:not([hidden]) [data-step="1"]').first().getAttribute('aria-hidden'),null);
 await p.keyboard.press('ArrowLeft');await p.waitForFunction(i=>location.hash===`#${i}/0`,i);
 const maxStep=await p.evaluate(()=>Math.max(...[...document.querySelectorAll('.slide:not([hidden]) [data-step]')].map(x=>+x.dataset.step||0)));await p.locator('#show-all').click();await p.waitForFunction(a=>location.hash===`#${a[0]}/${a[1]}`,[i,maxStep]);await p.reload();assert.equal(await p.locator('#counter').textContent(),`${String(i).padStart(2,'0')} / ${tot}`);
 await p.locator('#index-button').click();assert.equal(await p.locator('#slide-list li').count(),tot);await p.locator('#overview [data-close]').click();
 await p.locator('#notes-button').click();assert.ok((await p.locator('#notes-text').textContent()).length>40);await p.locator('#notes [data-close]').click();}
 // Humo genérico: cada componente interactivo ([data-demo]) debe responder a un clic sin errores y sin cambiar de slide.
 for(const n of ids){await p.goto(`${root}/especialidad-0${n}/`);await p.evaluate(()=>document.fonts.ready);
  const idx=await p.evaluate(()=>[...document.querySelectorAll('.slide')].map((s,i)=>s.querySelector('[data-demo]')?i+1:0).filter(Boolean));
  for(const i of idx){await go(n,i);const slide=p.locator('.slide:not([hidden])');const demo=slide.locator('[data-demo]').first();
   const ctl=demo.locator('button, select, summary').first();if(await ctl.count()){const before=await demo.innerText();
    if((await ctl.evaluate(e=>e.tagName))==='SELECT'){const opts=await ctl.locator('option').evaluateAll(o=>o.map(x=>x.value));await ctl.selectOption(opts[opts.length-1])}else await ctl.click();
    assert.equal(new URL(p.url()).hash,`#${i}/0`,`S${n} slide ${i}: el demo no debe mover la presentación`);}
   report.checks.push(`S${n} #${i}: demo interactivo responde`)}}
 report.checks.push('Revelado, retroceso, recarga, índice, notas y guía');
 // Default motion actually fades; reduced-motion was used for exhaustive layout.
 await p.emulateMedia({reducedMotion:'no-preference'});await go(nav,1);await p.keyboard.press('ArrowRight');await p.waitForTimeout(80);assert.ok(await p.locator('.slide.fade-out').count());await p.waitForTimeout(230);assert.equal(await p.locator('#counter').textContent(),`02 / ${tot}`);
 await p.emulateMedia({reducedMotion:'reduce'});report.checks.push('Fade manual y prefers-reduced-motion');
 // Links resolve locally and fragments point to existing anchors.
 for(const n of ids){
  await p.goto(`${root}/especialidad-0${n}/laboratorio.html`);
  const paths=await p.locator('a[href]').evaluateAll(xs=>xs.map(x=>x.href).filter(x=>x.startsWith(location.origin)));
  for(const url of new Set(paths)){const r=await p.request.get(url);assert.equal(r.status(),200,url)}
  assert.equal(await p.locator('section[id^="paso-"]').count(),6);
 }
 report.checks.push('Enlaces de guías');
 // A PDF is a review artifact, not proof of a cloud run.
 for(const n of ids){
  await p.goto(`${root}/especialidad-0${n}/`);await p.evaluate(()=>document.fonts.ready);await p.pdf({path:`${out}/sesion-${n}-editorial.pdf`,printBackground:true,preferCSSPageSize:true});
 }
 await p.goto(root);assert.equal(await p.locator('.course-card').count(),8);await p.screenshot({path:`${out}/catalogo.png`,fullPage:true});
 report.checks.push('PDFs de las sesiones editoriales y catálogo de ocho');
}finally{await b.close();fs.writeFileSync(`${out}/report.json`,JSON.stringify(report,null,2))}
assert.deepEqual(report.errors,[]);assert.deepEqual(report.requests,[]);assert.deepEqual(report.layout,[]);console.log(JSON.stringify(report,null,2));
