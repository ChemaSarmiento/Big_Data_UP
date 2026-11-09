import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import fs from 'node:fs';import assert from 'node:assert/strict';
const root=process.env.COURSE_ORIGIN||'http://127.0.0.1:4183';const base=root+'/clase-bigquery/';const out='/tmp/bigdata-clase-bigquery';fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch({headless:true});const result={errors:[],layout:[],slides:26};
try{
 const p=await b.newPage({reducedMotion:'reduce'});p.on('pageerror',e=>result.errors.push(e.message));p.on('response',r=>{if(r.status()>=400)result.errors.push(r.url())});
 for(const v of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844}]){
  await p.setViewportSize(v);await p.goto(base);await p.evaluate(()=>document.fonts.ready);assert.equal(await p.locator('.slide').count(),26);
  for(let i=1;i<=26;i++){
   await p.evaluate(n=>location.hash=`${n}/99`,i);await p.waitForFunction(n=>document.querySelector('#counter').textContent.startsWith(String(n).padStart(2,'0')),i);
   const check=await p.evaluate(()=>{const s=document.querySelector('.slide:not([hidden])'),c=s.querySelector('.content'),box=c.getBoundingClientRect();const cs=[...c.children].map(x=>x.getBoundingClientRect());return {horizontal:document.documentElement.scrollWidth>innerWidth+2,overflow:innerWidth>700&&cs.some(x=>x.bottom>box.bottom+3||x.top<box.top-3||x.right>box.right+3||x.left<box.left-3),source:innerWidth>700&&cs.some(x=>x.bottom>s.querySelector('.source').getBoundingClientRect().top-5)};});
   if(Object.values(check).some(Boolean))result.layout.push({i,v,...check});
   if(v.width===1440&&[1,6,7,12,20,24].includes(i))await p.screenshot({path:`${out}/slide-${i}.png`});
  }
 }
 await p.setViewportSize({width:1440,height:900});await p.goto(base+'#6/0');await p.locator('[data-scan-mode="limit"]').click();assert.match(await p.locator('[data-scan-result]').innerText(),/doce/);assert.equal(await p.locator('.muted-block').count(),0);await p.locator('[data-scan-mode="month"]').click();assert.equal(await p.locator('.muted-block').count(),11);assert.ok(p.url().endsWith('#6/0'));
 await p.goto(base+'#7/0');await p.locator('[data-arch="lakehouse"]').click();assert.match(await p.locator('[data-arch-title]').innerText(),/tablas abiertas/);assert.ok(p.url().endsWith('#7/0'));
 await p.locator('#notes-button').click();assert.ok((await p.locator('#notes-text').innerText()).length>50);await p.locator('#notes [data-close]').click();
 await p.goto(base);await p.emulateMedia({media:'print'});await p.pdf({path:`${out}/clase-bigquery.pdf`,printBackground:true,preferCSSPageSize:true});await p.emulateMedia({media:'screen'});
 for(const file of ['laboratorio.html','tarea.html']){
  await p.goto(base+file);const urls=await p.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(x=>x.startsWith(location.origin)));
  for(const url of urls)assert.equal((await p.request.get(url)).status(),200,url);
  await p.setViewportSize({width:390,height:844});assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await p.setViewportSize({width:1440,height:900});
 }
 fs.writeFileSync(`${out}/report.json`,JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));assert.deepEqual(result.errors,[]);assert.deepEqual(result.layout,[]);
}finally{await b.close()}
