// Verificación propia de S1. Servir presentaciones-v2 en 127.0.0.1:4183 y ejecutar:
//   node presentaciones-v2/especialidad-01/verify.mjs
import {chromium} from '../../slides_maestria/node_modules/playwright-chromium/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const out='/tmp/bigdata-plan3-sesion01';await fs.mkdir(out,{recursive:true});
const base='http://127.0.0.1:4183/especialidad-01/';
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
 const errors=[],failures=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()} ${r.url()}`)});
 await page.goto(base);await page.evaluate(()=>document.fonts.ready);
 const total=await page.locator('.slide').count();
 assert.ok(total>=22&&total<=28,`slides ${total}`);
 const ids=await page.locator('.slide').evaluateAll(n=>n.map(x=>x.dataset.id));
 assert.deepEqual(ids,Array.from({length:total},(_,i)=>`E01-${String(i+1).padStart(2,'0')}`));
 // Una sola slide de laboratorio (resumen), no una por paso.
 assert.equal(await page.locator('.slide.kind-lab-taller').count(),1);
 // Demo de reparto: cambia el reparto sin mover la presentación.
 const par=await page.evaluate(()=>[...document.querySelectorAll('.slide')].findIndex(s=>s.querySelector('[data-demo="reparto"]'))+1);
 await page.goto(`${base}#${par}/0`);await page.locator('[data-demo="reparto"] button[data-w="6"]').click();
 assert.match(await page.locator('[data-par-out]').innerText(),/6 personas.*2 de 12 cajas/);assert.equal(new URL(page.url()).hash,`#${par}/0`);
 // Texto visible: sin referencias a docente, equipos, H1 ni fechas de calendario recientes.
 const deck=await page.evaluate(()=>[...document.querySelectorAll('.slide')].map(s=>s.innerText).join('\n'));
 await page.goto(base+'laboratorio.html');
 const guide=await page.evaluate(()=>document.body.innerText);
 for(const [name,txt] of [['deck',deck],['guía',guide]]){
  assert.doesNotMatch(txt,/docente/i,`${name}: menciona al docente`);
  assert.doesNotMatch(txt,/\bequipos?\b/i,`${name}: menciona equipos`);
  assert.doesNotMatch(txt,/\bH1\b/,`${name}: menciona H1`);
  assert.doesNotMatch(txt,/20(2[3-9]|3\d)/,`${name}: contiene una fecha de calendario`);
 }
 // Guía: seis pasos, enlaces locales y scripts descargables.
 assert.equal(await page.locator('section[id^="paso-"]').count(),6);
 for(const url of new Set(await page.locator('a[href]').evaluateAll(a=>a.map(x=>x.href).filter(x=>x.startsWith(location.origin)))))assert.equal((await page.request.get(url)).status(),200,url);
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);
 console.log(JSON.stringify({slides:total,lab:6,errors,failures},null,1));
}finally{await browser.close()}
