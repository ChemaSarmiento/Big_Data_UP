import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import assert from 'node:assert/strict';
const browser=await chromium.launch({headless:true});
try{
 const p=await browser.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)errors.push(r.url())});
 const root='http://127.0.0.1:4184';
 await p.goto(root+'/refactor_especialidad/');assert.equal(await p.locator('.course-card').count(),8);
 for(let n=1;n<=8;n++){
  const base=root+`/refactor_especialidad/especialidad-0${n}/`;
  await p.goto(base);await p.waitForSelector('#counter');assert.ok(await p.locator('.slide').count()>10);
  await p.locator('#lab-button').click();const lab=p.locator('#lab a[href="laboratorio.html"]');assert.ok(await lab.count());
  await p.goto(base+'laboratorio.html');
  const links=await p.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(h=>h.startsWith(location.origin)));
  for(const url of links)assert.equal((await p.request.get(url)).status(),200,url);
 }
 await p.goto(root+'/refactor_especialidad/especialidad-07/practica.html');await p.locator('[data-search]').fill('inventario');await p.locator('[data-search-button]').click();assert.match(await p.locator('[data-search-results]').innerText(),/F03/);
 await p.goto(root+'/refactor_especialidad/especialidad-06/practica.html');await p.locator('[data-bi-filter]').selectOption('C');assert.match(await p.locator('[data-bi-cost]').innerText(),/Sin costo completo/);
 for(const url of ['/', '/reto-sql.html','/decks.json'])assert.equal((await p.request.get(root+url)).status(),200);
 assert.deepEqual(errors,[]);console.log('OK: 8 decks, guías y recursos bajo prefijo; prácticas S6/S7; raíz y reto SQL conservados.');
}finally{await browser.close()}
