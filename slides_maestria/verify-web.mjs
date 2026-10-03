import { chromium } from 'playwright-chromium';
import fs from 'node:fs/promises';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
const errors = []; page.on('pageerror', e => errors.push(e.message));
await page.goto('http://localhost:4173');
await page.waitForSelector('.deck');
if (await page.locator('.deck').count() !== 25) throw new Error('Missing decks');
await page.screenshot({path:'/tmp/big-data-catalog.png'});
await page.getByRole('button', {name:'Especialidad',exact:true}).click();
if (await page.locator('.deck:visible').count() !== 10) throw new Error('Filter failed');
await page.goto('http://localhost:4173/#maestria-01/1');
await page.waitForSelector('#slide h1');
await page.keyboard.press('ArrowRight');
await page.waitForFunction(() => location.hash.endsWith('/2'));
await page.locator('#stage').click({position:{x:20,y:20}});
await page.waitForFunction(() => location.hash.endsWith('/3'));
await page.keyboard.press('o');
await page.waitForSelector('dialog[open]');
await page.locator('#close-overview').click();
const decks = JSON.parse(await fs.readFile('../presentaciones/dist/decks.json','utf8'));
for (const d of decks) {
 if (!d.scope || !d.areas?.length || !d.slides.some(s => s.includes('Big Data y cloud computing:'))) throw new Error(`Missing classification: ${d.id}`);
 if (d.slides.some(s => /presentador|facilitador|profesor|instructor|docente/i.test(s))) throw new Error(`Presenter reference: ${d.id}`);
}
let diagrams = 0, overflow = [], images = [];
const visualNames = new Set();
let visualErrors = [];
for (const d of decks) {
 for (let i=0; i<d.slides.length; i++) {
  await page.goto(`http://localhost:4173/#${d.id}/${i+1}`);
  await page.waitForFunction(n => document.querySelector('#counter')?.textContent.startsWith(String(n).padStart(2,'0') + ' /'), i+1);
  if (d.slides[i].includes('class="mermaid"')) { await page.waitForSelector('#slide .mermaid svg'); diagrams++; }
  await page.waitForFunction(() => [...document.querySelectorAll('#slide img')].every(i => i.complete));
  await page.waitForFunction(id => document.querySelector('#session-label')?.textContent.includes(id), d.title);
  const graphics = await page.evaluate(() => [...document.querySelectorAll('figure[data-infographic]')].map(f => ({name:f.dataset.infographic, bad:[...f.querySelectorAll('text')].filter(t => { const b=t.getBBox(); const vb=f.querySelector('svg').viewBox.baseVal; return b.x<0 || b.y<0 || b.x+b.width>vb.width+1 || b.y+b.height>vb.height+1; }).map(t => t.textContent)})));
  for(const g of graphics) { visualNames.add(g.name); if(g.bad.length) visualErrors.push(g); }
  const info = await page.evaluate(() => ({horizontal: document.documentElement.scrollWidth > innerWidth, vertical: document.querySelector('#stage').scrollHeight > document.querySelector('#stage').clientHeight + 3, images:[...document.querySelectorAll('#slide img')].filter(i=>!i.complete || !i.naturalWidth).map(i=>i.src)}));
  if (info.horizontal || info.vertical) overflow.push(`${d.id}/${i+1}:${info.horizontal?'horizontal':'vertical'}`);
  images.push(...info.images);
 }
}
const architecture = decks.find(d => d.id === 'maestria-01');
await page.goto(`http://localhost:4173/#maestria-01/${architecture.slides.findIndex(s => s.includes('class="mermaid"')) + 1}`);
await page.waitForSelector('.mermaid svg');
await page.waitForTimeout(1200);
await page.screenshot({path:'/tmp/big-data-slide.png'});
await page.setViewportSize({width:390,height:844});
await page.goto('http://localhost:4173');
await page.waitForSelector('.deck');
if (await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth)) throw new Error('Mobile catalog overflows');
await page.goto('http://localhost:4173/#especialidad-01/2');
await page.waitForSelector('#slide h1');
await page.waitForTimeout(1200);
await page.screenshot({path:'/tmp/big-data-mobile.png'});
await page.emulateMedia({reducedMotion:'reduce'});
if (await page.locator('.enter').first().evaluate(e=>getComputedStyle(e).animationName) !== 'none') throw new Error('Reduced motion failed');
console.log(JSON.stringify({decks:decks.length,slides:decks.reduce((n,d)=>n+d.slides.length,0),diagrams,infographics:[...visualNames],visualErrors,errors,overflow,images},null,2));
await browser.close();
if (errors.length || images.length || visualErrors.length || visualNames.size !== 8) process.exitCode=1;
