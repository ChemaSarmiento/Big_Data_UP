import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const output='/tmp/bigdata-plan3-sesion01';
await fs.mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:1440,height:900},acceptDownloads:true});
 const errors=[],failures=[],scroll=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()} ${r.url()}`);});
 const base='http://127.0.0.1:4183/especialidad-01/';
 async function settled(n,s) {
  await page.waitForFunction(({n,s})=>{
   const slide=document.querySelector('.slide:not([hidden])');
   if(!slide)return false;
   const max=Math.max(0,...[...slide.querySelectorAll('[data-step]')].map(e=>Number(e.dataset.step)));
   return document.querySelector('#counter').textContent.startsWith(String(n).padStart(2,'0')) && document.querySelector('#step-counter').textContent===`Revelado ${Math.min(s,max)} de ${max}`;
  },{n,s});
 }
 async function route(n,s=0) {await page.goto(`${base}#${n}/${s}`);await settled(n,s);await page.waitForTimeout(250);}
 await route(1);
 assert.equal(await page.locator('.slide').count(),28);
 assert.equal(await page.locator('#slide-list button').count(),28);
 assert.deepEqual(await page.locator('.slide').evaluateAll(nodes=>nodes.map(n=>n.dataset.id)),Array.from({length:28},(_,i)=>`E01-${String(i+1).padStart(2,'0')}`));
 await page.screenshot({path:`${output}/01-portada.png`});
 await page.keyboard.press('ArrowRight');await settled(1,1);
 await page.keyboard.press('ArrowRight');await settled(2,0);
 await page.locator('#previous').click();await settled(1,1);
 // Las flechas funcionan también después de usar el botón de navegación.
 await page.keyboard.press('ArrowRight');await settled(2,0);
 await page.locator('#show-all').click();await settled(2,2);
 assert.equal(await page.locator('.slide:visible .unrevealed').count(),0);
 await page.locator('#show-all').click();await settled(2,0);
 await route(7);
 await page.locator('#compute-toggle').click();
 assert.equal(await page.locator('#compute-toggle').getAttribute('aria-pressed'),'false');
 assert.equal(new URL(page.url()).hash,'#7/0');
 await route(19);
 await page.locator('#project-code').click();
 assert.equal(new URL(page.url()).hash,'#19/0');
 await page.keyboard.press('ArrowRight');assert.equal(new URL(page.url()).hash,'#19/0');
 await page.evaluate(()=>{const r=document.createRange();r.selectNodeContents(document.querySelector('#project-code'));const s=getSelection();s.removeAllRanges();s.addRange(r);});
 await page.locator('#stage').click({position:{x:10,y:10}});
 assert.equal(new URL(page.url()).hash,'#19/0');
 await page.evaluate(()=>getSelection().removeAllRanges());
 const scriptPromise=page.waitForEvent('download');await page.locator('.code-actions a').click();
 assert.equal((await scriptPromise).suggestedFilename(),'verificar-proyecto.sh');
 await route(24);
 await page.locator('#dataset').selectOption({label:'Biblioteca · Checkouts_by_Title_20250207.csv'});
 await page.locator('#audience').fill('Responsable de colección');
 await page.locator('#scope').fill('Comparar uso histórico por formato para revisar prioridades.');
 await page.locator('#evidence').fill('Conteos por periodo y cobertura documentados.');
 assert.equal(new URL(page.url()).hash,'#24/0');
 await page.reload();await settled(24,0);
 assert.equal(await page.locator('#audience').inputValue(),'Responsable de colección');
 assert.match(await page.locator('#dataset').inputValue(),/Biblioteca/);
 const jsonPromise=page.waitForEvent('download');await page.locator('#decision-form button').click();
 const file=await jsonPromise;const payload=JSON.parse(await fs.readFile(await file.path(),'utf8'));
 assert.match(payload.dataset,/Biblioteca/);assert.equal(payload.ejemploGuiado,'PROFECO');
 assert.match(payload.estado,/pendiente/);assert.match(payload.mapa.gold,/dominio/);
 await page.locator('#index-button').click();assert.ok(await page.locator('#overview').evaluate(e=>e.open));
 await page.locator('#slide-list button').nth(12).click();await settled(13,0);
 await page.locator('#notes-button').click();assert.match(await page.locator('#notes-text').innerText(),/Tres fichas/);
 await page.locator('#notes [data-close]').click();
 await page.locator('#lab-button').click();assert.ok(await page.locator('#lab').evaluate(e=>e.open));
 await page.locator('#lab [data-close]').click();
 // Verificar todos los revelados y resolución de proyección antes del recorrido móvil.
 for(const viewport of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844}]){
  await page.setViewportSize(viewport);
  for(let n=1;n<=28;n++){
   await route(n,99);
   const info=await page.evaluate(()=>({horizontal:document.documentElement.scrollWidth>innerWidth,wide:document.querySelector('.slide:not([hidden])').scrollWidth>document.querySelector('#stage').clientWidth,vertical:document.querySelector('#stage').scrollHeight>document.querySelector('#stage').clientHeight+2}));
   assert.ok(!info.horizontal&&!info.wide,`Overflow horizontal ${viewport.width}, slide ${n}`);
   if(info.vertical)scroll.push({width:viewport.width,slide:n});
   if(viewport.width>=1280)assert.ok(!info.vertical,`Overflow vertical ${viewport.width}, slide ${n}`);
   if(viewport.width===1440&&[9,13,19,24].includes(n))await page.screenshot({path:`${output}/${String(n).padStart(2,'0')}.png`});
  }
 }
 await route(24);await page.screenshot({path:`${output}/24-mobile.png`});
 await page.setViewportSize({width:1440,height:900});
 await page.emulateMedia({reducedMotion:'reduce'});await route(10,2);
 assert.equal(await page.locator('.slide:visible').evaluate(e=>getComputedStyle(e).animationName),'none');
 await page.keyboard.press('ArrowRight');await settled(10,3);
 await page.keyboard.press('ArrowLeft');await settled(10,2);
 await page.goBack();await settled(10,3);
 await page.reload();await settled(10,3);
 await route(1);
 await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('.slide:visible').count(),28);
 assert.equal(await page.locator('.slide [data-step]').first().evaluate(e=>getComputedStyle(e).visibility),'visible');
 await page.pdf({path:`${output}/sesion-01.pdf`,printBackground:true,preferCSSPageSize:true});
 await page.emulateMedia({media:'screen'});
 await page.goto(`${base}laboratorio.html`);
 assert.equal(await page.locator('section[id^="paso-"]').count(),6);
 assert.match(await page.locator('body').innerText(),/dataset distinto/);
 const links=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(n=>n.href).filter(h=>h.startsWith(location.origin)));
 for(const link of links)assert.equal((await page.request.get(link)).status(),200,link);
 const catalog=await (await page.request.get(`${base}catalogo-candidatos.json`)).json();assert.equal(catalog.activos.length,8);
 const response=await page.request.get('http://127.0.0.1:4183/piloto/');assert.equal(response.status(),200);
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);
 const result={slides:28,ids:'E01-01…E01-28',errors,failedRequests:failures,verticalScroll:scroll,checks:['navegación por pasos','teclado tras clic en control','selección y teclado en código','índice/guía/notas','descargas shell/JSON','dataset propio y persistencia','historial/recarga','1440×900 y 1280×720 sin recortes','móvil sin desbordamiento horizontal','movimiento reducido','impresión de todos los revelados','guía de seis pasos y recursos locales','piloto conservado'],artifacts:output};
 await fs.writeFile(`${output}/report.json`,JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
}finally{await browser.close();}
