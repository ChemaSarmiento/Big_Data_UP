import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import MarkdownIt from 'markdown-it';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'presentaciones/dist');
const visuals = new Map(await Promise.all((await fs.readdir(path.join(root, 'presentaciones/infograficos'))).filter(n => n.endsWith('.svg')).map(async n => [n.slice(0, -4), await fs.readFile(path.join(root, 'presentaciones/infograficos', n), 'utf8')])));
const md = new MarkdownIt({ html: true, linkify: true });
md.renderer.rules.html_block = (tokens, i) => tokens[i].content.split('\n').map(line => {
  if (!line.trim().startsWith('<') && /[`*]/.test(line)) return md.renderInline(line);
  return line;
}).join('\n');
const originalFence = md.renderer.rules.fence;
md.renderer.rules.fence = (tokens, i, options, env, self) => {
  if (tokens[i].info.startsWith('mermaid')) return `<pre class="mermaid">${md.utils.escapeHtml(tokens[i].content)}</pre>`;
  tokens[i].info = tokens[i].info.split(/[ {]/)[0];
  return originalFence(tokens, i, options, env, self);
};
const read = p => fs.readFile(path.join(root, p), 'utf8');
function split(source) {
  source = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
  // Slide metadata is delimited like a slide; fenced code is never split.
  const slides = []; let lines = [], fenced = false;
  for (const line of source.split('\n')) {
    if (/^```/.test(line)) fenced = !fenced;
    if (!fenced && /^---\s*$/.test(line)) { slides.push(lines.join('\n')); lines = []; }
    else lines.push(line);
  }
  slides.push(lines.join('\n'));
  return slides.filter(s => s.trim() && !/^(layout|class|transition):/.test(s.trim()));
}
function render(source) {
  source = source.replace(/^::right::\s*$/gm, '');
  if (!/^# /m.test(source)) source = source.replace(/^## /m, '# ');
  return md.render(source.replace(/<\/?v-clicks[^>]*>/g, '').replace(/\s+v-click(?:="[^"]*")?/g, '').replace(/<span v-mark[^>]*>/g, '<span>')).replace(/<figure data-infographic="([a-z0-9-]+)"><\/figure>/g, (_, name) => {
    if (!visuals.has(name)) throw new Error(`Missing infographic: ${name}`);
    return `<figure class="infographic" data-infographic="${name}">${visuals.get(name)}</figure>`;
  });
}
function section(source, heading) {
  return source.match(new RegExp(`^## ${heading}[^\\n]*\\n([\\s\\S]*?)(?=^## |$(?![\\s\\S]))`, 'm'))?.[1]?.trim() || '';
}
const scopes = JSON.parse(await read('presentaciones/ambitos.json'));
function scopeSlide(id) {
  const s = scopes[id];
  if (!s) throw new Error(`Missing scope: ${id}`);
  return `# Big Data y cloud computing: el foco de esta sesión

| Ámbito | Contenido |
|---|---|
| **Big Data** | ${s.bigData || 'Sin contenido específico en esta sesión.'} |
| **Cloud computing** | ${s.cloud || 'No es el foco: estos conceptos también pueden trabajarse localmente.'} |
| **Complementario** | ${s.complementario || 'La práctica conecta procesamiento e infraestructura.'} |

> Big Data aborda la escala y el procesamiento de datos. Cloud computing aporta recursos y servicios bajo demanda. Usar cloud no convierte por sí solo una tarea en Big Data.`;
}
const decks = [];
const intro = await read('intro-big-data/slides.md');
decks.push({ id: 'introduccion', track: 'base', number: 'BASE', title: 'Introducción a Big Data', source: 'intro-big-data/slides.md', slides: [...split(intro).slice(0,1), scopeSlide('introduccion'), ...split(intro).slice(1)].map(render) });
for (const track of ['especialidad', 'maestria']) {
  const syllabus = await read(`${track}/TEMARIO.md`);
  for (let n = 0; n <= (track === 'maestria' ? 13 : 9); n++) {
    const number = String(n).padStart(2, '0');
    const source = track === 'maestria' ? `slides_maestria/sesion-${number}.md` : `${track}/sesion-${number}/slides.md`;
    const raw = await read(source);
    const notes = await read(`${track}/sesion-${number}/README.md`);
    const title = notes.match(/^# Sesión \d+\s*[—–-]\s*(.+)/m)?.[1] || `Sesión ${number}`;
    const topics = syllabus.match(new RegExp(`^## (?:Módulo 0 — )?Sesión ${number}:[^\\n]*\\n([\\s\\S]*?)(?=^## |^---|$(?![\\s\\S]))`, 'm'))?.[1] || '';
    const objectives = topics.split('\n').filter(l => /^\d+\./.test(l)).map(l => l.replace(/^\d+\.\s*/, ''));
    const slides = split(raw);
    slides.splice(1, 0, `# La ruta de hoy\n\n${objectives.map(t => `- ${t}`).join('\n')}\n\n> Del concepto a la práctica: explica la decisión, compruébala con evidencia y documenta el resultado.`);
    const lab = section(notes, 'Lab') || section(notes, 'Actividad') || section(notes, 'Taller');
    if (lab) slides.splice(2, 0, `# Lo que podrás demostrar\n\n${lab}`);
    const supplement = `presentaciones/complementos/${track}-${number}.md`;
    try {
      const extra = split(await read(supplement));
      const practice = slides.findIndex((s, i) => i > 2 && /^#.*(?:Lab de hoy|Actividad|Taller|Paso 1)/m.test(s));
      slides.splice(practice < 0 ? slides.length - 1 : practice, 0, ...extra);
    } catch (error) { if (error.code !== 'ENOENT') throw error; }
    const deliverable = section(notes, 'Entregable');
    slides.splice(Math.max(1, slides.length - 1), 0, `# Cierra el ciclo\n\n- ¿Qué problema resuelve lo que aprendiste hoy?\n- ¿Qué alternativa elegirías y bajo qué condiciones?\n- ¿Qué evidencia mostrarías para justificar tu decisión?${deliverable ? `\n\n## Evidencia de aprendizaje\n\n${deliverable}` : ''}`);
    slides.splice(3, 0, scopeSlide(`${track}-${number}`));
    decks.push({ id: `${track}-${number}`, track, number, title, source, slides: slides.map(render) });
  }
}
for (const d of decks) { d.scope = scopes[d.id]; d.areas = ['Big Data', ...(d.scope.cloud ? ['Cloud computing'] : [])]; }
await fs.mkdir(output, { recursive: true });
for (const name of ['index.html', 'styles.css', 'app.js']) await fs.copyFile(path.join(root, 'presentaciones', name), path.join(output, name));
await fs.writeFile(path.join(output, 'decks.json'), JSON.stringify(decks));
await fs.cp(path.join(root, 'presentaciones/infograficos'), path.join(output, 'infograficos'), { recursive: true });
await fs.cp(path.join(root, 'intro-big-data/public/infograficos'), path.join(output, 'infograficos'), { recursive: true });
await fs.cp(path.join(root, 'slides_maestria/node_modules/mermaid/dist'), path.join(output, 'vendor/mermaid'), { recursive: true });
console.log(`Built ${decks.length} decks / ${decks.reduce((n, d) => n + d.slides.length, 0)} slides in ${output}`);
