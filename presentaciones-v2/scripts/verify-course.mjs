import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const output='/tmp/bigdata-plan3-curso';await fs.mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:900},acceptDownloads:true});
 const errors=[],failed=[],overflow=[],horizontal=[];const origin='http://127.0.0.1:4183';
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failed.push(`${r.status()}: ${r.url()}`);});
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto(origin);assert.equal(await page.locator('.course-card').count(),8);await page.screenshot({path:`${output}/catalogo.png`});
 const manifest=await(await page.request.get(`${origin}/manifest.json`)).json();assert.equal(manifest.slides,manifest.sessions.reduce((a,s)=>a+s.slides,0));
 // S1–S7 tienen un recorrido específico en verify-editorial.mjs.
 for(const session of manifest.sessions.filter(s=>s.id>=8)){
  await page.setViewportSize({width:1440,height:900});
  const base=`${origin}/${session.url}`;await page.goto(base);
  await page.waitForSelector('#counter');
  assert.equal(await page.locator('.slide').count(),session.slides);
  assert.equal(await page.locator('#slide-list button').count(),session.slides);
  const ids=await page.locator('.slide').evaluateAll(nodes=>nodes.map(n=>n.dataset.id));
  assert.equal(new Set(ids).size,session.slides);
  for(const viewport of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844}]){
   await page.setViewportSize(viewport);
   for(let i=1;i<=session.slides;i++){
    await page.evaluate(n=>{location.hash=`${n}/99`;},i);
    await page.waitForFunction(n=>document.querySelector('#counter').textContent.startsWith(String(n).padStart(2,'0')),i);
    const info=await page.evaluate(()=>({horizontal:document.documentElement.scrollWidth>innerWidth||document.querySelector('.slide:not([hidden])').scrollWidth>document.querySelector('#stage').clientWidth,vertical:document.querySelector('#stage').scrollHeight>document.querySelector('#stage').clientHeight+3}));
    if(info.horizontal)horizontal.push({session:session.id,slide:i,width:viewport.width});
    if(info.vertical&&viewport.width>=1280)overflow.push({session:session.id,slide:i,width:viewport.width});
    if(viewport.width===1440&&[1,12,20].includes(i))await page.screenshot({path:`${output}/s${session.id}-${i}.png`});
   }
  }
  await page.setViewportSize({width:1440,height:900});
  await page.goto(`${base}#1/0`);await page.waitForFunction(()=>document.querySelector('#counter').textContent.startsWith('01'));
  await page.keyboard.press('ArrowRight');await page.waitForURL('**/#1/1');
  await page.waitForFunction(()=>document.querySelector('#step-counter').textContent.startsWith('Revelado 1'));
  await page.keyboard.press('ArrowLeft');await page.waitForURL('**/#1/0');
  await page.locator('#index-button').click();assert.ok(await page.locator('#overview').evaluate(d=>d.open));
  await page.locator('#slide-list button').nth(2).click();await page.waitForFunction(()=>document.querySelector('#counter').textContent.startsWith('03'));
  await page.locator('#notes-button').click();assert.ok((await page.locator('#notes-text').innerText()).length>30);await page.locator('#notes [data-close]').click();
  await page.locator('#lab-button').click();assert.ok(await page.locator('#lab').evaluate(d=>d.open));await page.locator('#lab [data-close]').click();
  await page.goto(`${base}#1/0`);await page.waitForFunction(()=>document.querySelector('#counter').textContent.startsWith('01'));
  await page.emulateMedia({media:'print',reducedMotion:'reduce'});
  assert.equal(await page.locator('.slide:visible').count(),session.slides);
  await page.pdf({path:`${output}/sesion-${session.id}.pdf`,printBackground:true,preferCSSPageSize:true});
  await page.emulateMedia({media:'screen',reducedMotion:'reduce'});
  await page.goto(`${base}laboratorio.html`);
  const local=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(n=>n.href).filter(h=>h.startsWith(location.origin)));
  for(const link of local)assert.equal((await page.request.get(link)).status(),200,link);
  if(session.id>1){
   assert.equal(await page.locator('section[id^="paso-"]').count(),6);
   await page.locator('[name="dataset"]').fill(`Dataset propio equipo ${session.id}`);
   await page.locator('[name="evidence"]').fill('Evidencia de revisión local, no ejecución cloud.');
   await page.reload();assert.equal(await page.locator('[name="dataset"]').inputValue(),`Dataset propio equipo ${session.id}`);
   const promise=page.waitForEvent('download');await page.locator('#journal-form button').click();
   const d=await promise;const data=JSON.parse(await fs.readFile(await d.path(),'utf8'));assert.equal(data.hito,`H${session.id}`);
  }
 }
 // Interacciones docentes: el clic no cambia de diapositiva.
 await page.goto(`${origin}/especialidad-07/practica.html`);await page.waitForSelector('[data-search]');
 await page.locator('[data-search]').fill('cobertura');await page.locator('[data-search-button]').click();assert.ok(await page.locator('[data-search-results] details').count()>0);
 await page.locator('[data-search-results] summary').first().click();assert.ok((await page.locator('[data-search-results] details[open] p').innerText()).length>30);
 await page.locator('[data-search]').fill('temperatura marte');await page.locator('[data-search-button]').click();assert.equal(await page.locator('[data-search-results] details').count(),0);assert.match(await page.locator('.demo-answer').innerText(),/No se recuperó/);
 await page.goto(`${origin}/especialidad-08/#3/0`);await page.waitForSelector('.slide:visible [data-timer]');
 await page.locator('.slide:visible [data-timer-questions]').click();assert.equal(await page.locator('.slide:visible output').innerText(),'03:00');await page.locator('.slide:visible [data-timer-reset]').click();assert.equal(await page.locator('.slide:visible output').innerText(),'07:00');
 await page.setViewportSize({width:390,height:844});await page.goto(origin);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:`${output}/catalogo-mobile.png`});
 const result={sessions:1,slides:14,errors,failedRequests:failed,horizontalOverflow:horizontal,projectorScroll:overflow,artifacts:output};
 await fs.writeFile(`${output}/report.json`,JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
 assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);assert.deepEqual(horizontal,[]);assert.deepEqual(overflow,[]);
}finally{await browser.close();}
