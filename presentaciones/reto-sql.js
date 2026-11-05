import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js';
import { getFirestore, doc, runTransaction, writeBatch, serverTimestamp } from 'https://www.gstatic.com/firebasejs/12.19.0/firebase-firestore.js';
import { firebaseConfig, MATRICULA } from './firebase-config.js';

const $ = id => document.getElementById(id);
const db = getFirestore(initializeApp(firebaseConfig));
const TOTAL = 100;
let preguntas = [], matricula = null, asignacion = null;

// ---------- Tema (mismo comportamiento que las presentaciones) ----------
const systemDark = matchMedia('(prefers-color-scheme: dark)');
const activeTheme = () => document.documentElement.dataset.theme || (systemDark.matches ? 'dark' : 'light');
const labelTheme = () => { $('theme').textContent = activeTheme() === 'dark' ? 'Tema claro' : 'Tema oscuro'; };
$('theme').onclick = () => { const next = activeTheme() === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = next; try { localStorage.setItem('theme', next); } catch {} labelTheme(); };
systemDark.addEventListener('change', labelTheme); labelTheme();

const estado = (texto, tipo = '') => { $('estado').textContent = texto; $('estado').dataset.tipo = tipo; };
const fecha = ts => ts?.toDate ? ts.toDate().toLocaleString('es-MX', { dateStyle: 'long', timeStyle: 'short' }) : 'hace un momento';

// Solo lectura: debe empezar con SELECT o WITH y no contener instrucciones que modifiquen datos o estructura.
function validarSQL(sql) {
  const sinComentarios = sql.replace(/--[^\n]*/g, ' ').replace(/\/\*[\s\S]*?\*\//g, ' ').trim();
  if (sinComentarios.length < 10) return 'La consulta está vacía o es demasiado corta.';
  if (!/^(select|with)\b/i.test(sinComentarios)) return 'La consulta debe empezar con SELECT o WITH.';
  // Se revisa el texto completo, comentarios incluidos, igual que en firestore.rules.
  if (/\b(insert|update|delete|drop|alter|create|truncate|grant|revoke)\b/i.test(sql)) return 'Solo se aceptan consultas de lectura. Quita INSERT, UPDATE, DELETE o cualquier cambio de estructura, también de los comentarios.';
  if (sinComentarios.replace(/;\s*$/, '').includes(';')) return 'Entrega una sola consulta, sin varias sentencias separadas por punto y coma.';
  if (sql.length > 5000) return 'La consulta pasa de 5,000 caracteres. Recórtala.';
  return null;
}

function mostrar() {
  const p = preguntas.find(q => q.id === asignacion.preguntaId);
  $('pregunta-meta').textContent = `Pregunta ${String(p.id).padStart(3, '0')} · ${p.tema} · Matrícula ${matricula}`;
  $('pregunta-texto').textContent = p.pregunta;
  const entregada = !!asignacion.respondidaEn;
  $('bloque-respuesta').hidden = entregada;
  $('bloque-entregada').hidden = !entregada;
  if (entregada) $('texto-entregada').textContent = `Entregaste tu respuesta el ${fecha(asignacion.respondidaEn)}. Ya no se puede cambiar.`;
  $('panel-pregunta').hidden = false;
}

$('form-matricula').onsubmit = async e => {
  e.preventDefault();
  const m = $('matricula').value.trim().toUpperCase();
  if (!MATRICULA.test(m)) { estado('Esa matrícula no tiene el formato esperado: letras y números, de 4 a 12 caracteres.', 'error'); return; }
  $('btn-matricula').disabled = true; estado('Buscando tu pregunta…');
  try {
    if (!preguntas.length) preguntas = await (await fetch('./preguntas-sql.json')).json();
    const ref = doc(db, 'asignaciones', m);
    asignacion = await runTransaction(db, async tx => {
      const snap = await tx.get(ref);
      if (snap.exists()) return snap.data();
      const nueva = { matricula: m, preguntaId: 1 + Math.floor(Math.random() * TOTAL), asignadaEn: serverTimestamp() };
      tx.set(ref, nueva);
      return nueva;
    });
    matricula = m;
    $('matricula').readOnly = true;
    mostrar();
    estado('');
  } catch (err) {
    console.error(err);
    estado('Esto no salió. Revisa tu conexión e inténtalo otra vez; si vuelve a fallar, avísale a tu profesor qué viste.', 'error');
    $('btn-matricula').disabled = false;
  }
};

$('btn-entregar').onclick = async () => {
  const sql = $('sql').value.trim();
  const problema = validarSQL(sql);
  if (problema) { estado(problema, 'error'); return; }
  if (!confirm('Solo puedes entregar una vez. ¿Entregar esta consulta?')) return;
  $('btn-entregar').disabled = true; estado('Guardando tu respuesta…');
  try {
    const batch = writeBatch(db);
    batch.set(doc(db, 'respuestas', matricula), { matricula, preguntaId: asignacion.preguntaId, sql, respondidaEn: serverTimestamp() });
    batch.update(doc(db, 'asignaciones', matricula), { respondidaEn: serverTimestamp() });
    await batch.commit();
    asignacion = { ...asignacion, respondidaEn: { toDate: () => new Date() } };
    mostrar();
    estado('Respuesta guardada.', 'ok');
  } catch (err) {
    console.error(err);
    const yaEntregada = err?.code === 'permission-denied';
    estado(yaEntregada ? 'No se pudo guardar. Lo más probable es que esta matrícula ya tenga una respuesta entregada.' : 'Esto no salió. Tu consulta sigue en el cuadro; revisa tu conexión e inténtalo otra vez.', 'error');
    $('btn-entregar').disabled = false;
  }
};
