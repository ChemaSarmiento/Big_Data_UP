const fs = require("fs");
const path = require("path");
const { iconToPngDataUrl } = require("./icon_helper");
const {
  FaDatabase, FaTachometerAlt, FaThLarge, FaShieldAlt, FaGem,
  FaServer, FaCloud, FaCoins, FaExpandArrowsAlt, FaLock, FaTools, FaMicrochip,
  FaProjectDiagram, FaBrain, FaBoxOpen, FaHandPointRight,
  FaFilm, FaMusic, FaMapMarkedAlt, FaCreditCard, FaChartLine, FaLongArrowAltRight,
} = require("react-icons/fa");

const IN = (v) => `${v * 96}px`; // 1in = 96px, canvas = 13.333in x 7.5in = 1280x720

const PAGE = (bg, children) => `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; box-sizing:border-box; font-family: Arial, "Liberation Sans", sans-serif; }
  body { width:1280px; height:720px; background:${bg}; position:relative; overflow:hidden; }
  .abs { position:absolute; }
  .center { display:flex; align-items:center; justify-content:center; text-align:center; }
</style></head><body>${children}</body></html>`;

const text = (t, { x, y, w, h, size, color, bold, italic, align = "center", valign }) => `
<div class="abs" style="left:${IN(x)};top:${IN(y)};width:${IN(w)};height:${IN(h)};
  font-size:${size}px;color:#${color};font-weight:${bold ? 700 : 400};font-style:${italic ? "italic" : "normal"};
  text-align:${align};display:flex;align-items:${valign === "middle" ? "center" : "flex-start"};
  justify-content:${align === "center" ? "center" : align === "left" ? "flex-start" : "flex-end"};
  line-height:1.25;white-space:pre-wrap;">${t}</div>`;

const rect = ({ x, y, w, h, color, radius = 0 }) => `
<div class="abs" style="left:${IN(x)};top:${IN(y)};width:${IN(w)};height:${IN(h)};
  background:#${color};border-radius:${radius * 96}px;"></div>`;

const ellipse = ({ x, y, w, h, color }) => `
<div class="abs" style="left:${IN(x)};top:${IN(y)};width:${IN(w)};height:${IN(h)};
  background:#${color};border-radius:50%;"></div>`;

const img = (data, { x, y, w, h }) => `
<img class="abs" src="data:${data}" style="left:${IN(x)};top:${IN(y)};width:${IN(w)};height:${IN(h)};" />`;

async function build5vs() {
  const NAVY = "1E2761", ACCENT = "2563EB", ICE = "CADCFC", WHITE = "FFFFFF";
  const cards = [
    { word: "Volumen", icon: FaDatabase, def: "Magnitud masiva de datos — hoy, en petabytes. Reto de almacenamiento y acceso." },
    { word: "Velocidad", icon: FaTachometerAlt, def: "Qué tan rápido se genera y hay que procesarla: tiempo real, casi real o por lotes." },
    { word: "Variedad", icon: FaThLarge, def: "Estructurados, semi-estructurados y no estructurados: texto, imagen, video, audio." },
    { word: "Veracidad", icon: FaShieldAlt, def: "Calidad y confiabilidad del dato. ¿Podemos decidir con base en esto?" },
    { word: "Valor", icon: FaGem, def: "Capacidad de convertir datos en decisiones accionables — el retorno real de la inversión." },
  ];
  let body = "";
  body += text("Las 5 V's de Big Data", { x: 0.5, y: 0.45, w: 12.33, h: 0.8, size: 38, color: WHITE, bold: true });
  body += text("&quot;Grandes conjuntos de datos con tres características principales — hoy, cinco.&quot; — adaptado de Gartner",
    { x: 0.5, y: 1.25, w: 12.33, h: 0.5, size: 14, color: ICE, italic: true });

  const cardW = 2.3, gap = 0.2;
  const totalW = cards.length * cardW + (cards.length - 1) * gap;
  const startX = (13.33 - totalW) / 2;
  const circleY = 2.35, circleD = 1.15;

  for (let i = 0; i < cards.length; i++) {
    const c = cards[i];
    const cx = startX + i * (cardW + gap);
    const circleCx = cx + cardW / 2 - circleD / 2;
    body += ellipse({ x: circleCx, y: circleY, w: circleD, h: circleD, color: ACCENT });
    const iconData = await iconToPngDataUrl(c.icon, { color: "#FFFFFF", size: 256 });
    const iconSize = 0.6;
    body += img(iconData, { x: circleCx + (circleD - iconSize) / 2, y: circleY + (circleD - iconSize) / 2, w: iconSize, h: iconSize });
    body += text(c.word, { x: cx, y: circleY + circleD + 0.25, w: cardW, h: 0.5, size: 20, color: WHITE, bold: true });
    body += text(c.def, { x: cx, y: circleY + circleD + 0.8, w: cardW, h: 2.0, size: 12.5, color: ICE, valign: "top" });
  }
  body += text("Fuente: definición base — Gartner IT Glossary, ampliada con V's de uso común en la industria (2026)",
    { x: 0.5, y: 7.05, w: 12.33, h: 0.35, size: 10, color: ICE });

  fs.writeFileSync(path.join(__dirname, "html", "5vs.html"), PAGE(`#${NAVY}`, body));
}

async function buildOnpremCloud() {
  const SLATE = "475569", SLATE_BG = "F1F5F9", ACCENT = "2563EB", ACCENT_BG = "EFF6FF", INK = "1E2761", WHITE = "FFFFFF", GRAY_ROW = "F8FAFC";
  const rows = [
    { icon: FaCoins, label: "Costo inicial", onprem: "Alto — hardware, espacio, licencias", cloud: "Se paga por consumo, sin inversión inicial" },
    { icon: FaExpandArrowsAlt, label: "Elasticidad y escalabilidad", onprem: "Limitada al hardware ya adquirido", cloud: "Prácticamente ilimitada — se escala en minutos" },
    { icon: FaLock, label: "Control y propiedad", onprem: "Total — control físico y lógico completo", cloud: "Compartido — el proveedor gestiona el hardware" },
    { icon: FaTools, label: "Mantenimiento", onprem: "Alto overhead — tu equipo responde a fallas", cloud: "El proveedor gestiona infraestructura y plataforma" },
    { icon: FaMicrochip, label: "Tecnología", onprem: "Sujeta al ciclo de vida del hardware propio", cloud: "Acceso inmediato a tecnología nueva" },
  ];
  let body = "";
  body += text("On-Premise vs. Cloud Computing", { x: 0.5, y: 0.3, w: 12.33, h: 0.65, size: 34, color: INK, bold: true });
  body += text("En Big Data, la elasticidad de la nube es lo que hace posible responder a picos de Volumen y Velocidad",
    { x: 0.5, y: 0.95, w: 12.33, h: 0.4, size: 14, color: SLATE, italic: true });

  const labelW = 2.6, colW = 4.75, gap = 0.15, startX = 0.55;
  const col1X = startX + labelW + gap, col2X = col1X + colW + gap;
  const headerY = 1.5, headerH = 1.0;

  body += rect({ x: col1X, y: headerY, w: colW, h: headerH, color: SLATE_BG, radius: 0.1 });
  body += rect({ x: col2X, y: headerY, w: colW, h: headerH, color: ACCENT_BG, radius: 0.1 });

  const serverIcon = await iconToPngDataUrl(FaServer, { color: "#475569", size: 256 });
  const cloudIcon = await iconToPngDataUrl(FaCloud, { color: "#2563EB", size: 256 });
  body += img(serverIcon, { x: col1X + 0.3, y: headerY + 0.25, w: 0.55, h: 0.55 });
  body += text("On-Premise", { x: col1X + 1.0, y: headerY, w: colW - 1.2, h: headerH, size: 22, color: SLATE, bold: true, align: "left", valign: "middle" });
  body += img(cloudIcon, { x: col2X + 0.3, y: headerY + 0.25, w: 0.55, h: 0.55 });
  body += text("Cloud Computing", { x: col2X + 1.0, y: headerY, w: colW - 1.2, h: headerH, size: 22, color: ACCENT, bold: true, align: "left", valign: "middle" });

  let rowY = headerY + headerH + 0.2;
  const rowH = 0.8;
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    if (i % 2 === 0) {
      body += rect({ x: startX, y: rowY, w: labelW + gap + colW + gap + colW, h: rowH, color: GRAY_ROW });
    }
    const rowIcon = await iconToPngDataUrl(r.icon, { color: "#1E2761", size: 256 });
    body += img(rowIcon, { x: startX + 0.15, y: rowY + (rowH - 0.4) / 2, w: 0.4, h: 0.4 });
    body += text(r.label, { x: startX + 0.7, y: rowY, w: labelW - 0.75, h: rowH, size: 13, color: INK, bold: true, align: "left", valign: "middle" });
    body += text(r.onprem, { x: col1X + 0.2, y: rowY, w: colW - 0.4, h: rowH, size: 13, color: SLATE, align: "left", valign: "middle" });
    body += text(r.cloud, { x: col2X + 0.2, y: rowY, w: colW - 0.4, h: rowH, size: 13, color: INK, align: "left", valign: "middle" });
    rowY += rowH;
  }
  fs.writeFileSync(path.join(__dirname, "html", "onprem_vs_cloud.html"), PAGE("#FFFFFF", body));
}

async function buildQueHayEnLaNube() {
  const INK = "1E2761", SLATE = "475569", WHITE = "FFFFFF", CARD_BG = "F8FAFC";
  const AWS = "FF9900", AZURE = "0078D4", GCP = "4285F4";
  const columns = [
    { title: "Almacenamiento", icon: FaDatabase, rows: [
      { provider: "AWS", color: AWS, service: "Amazon S3" },
      { provider: "Azure", color: AZURE, service: "Azure Data Lake Storage" },
      { provider: "Google Cloud", color: GCP, service: "Google Cloud Storage" },
    ]},
    { title: "Procesamiento", icon: FaMicrochip, rows: [
      { provider: "AWS", color: AWS, service: "Amazon EMR" },
      { provider: "Azure", color: AZURE, service: "Azure HDInsight" },
      { provider: "Google Cloud", color: GCP, service: "Managed Service for Apache Spark" },
    ]},
    { title: "Orquestación", icon: FaProjectDiagram, rows: [
      { provider: "AWS", color: AWS, service: "Amazon MWAA (Airflow)" },
      { provider: "Azure", color: AZURE, service: "Azure Data Factory" },
      { provider: "Google Cloud", color: GCP, service: "Cloud Composer" },
    ]},
  ];
  let body = "";
  body += text("¿Y qué hay en la nube?", { x: 0.5, y: 0.3, w: 12.33, h: 0.65, size: 34, color: INK, bold: true });
  body += text("Categorización no extensiva, pero relevante para Big Data — nombres de servicio vigentes en 2026",
    { x: 0.5, y: 0.95, w: 12.33, h: 0.4, size: 14, color: SLATE, italic: true });

  const colW = 3.9, gap = 0.15, startX = 0.665, cardY = 1.6, cardH = 4.9;
  for (let i = 0; i < columns.length; i++) {
    const col = columns[i];
    const cx = startX + i * (colW + gap);
    body += rect({ x: cx, y: cardY, w: colW, h: cardH, color: CARD_BG, radius: 0.12 });
    const circleD = 0.9;
    body += ellipse({ x: cx + (colW - circleD) / 2, y: cardY + 0.3, w: circleD, h: circleD, color: "E0E7FF" });
    const iconData = await iconToPngDataUrl(col.icon, { color: "#1E2761", size: 256 });
    body += img(iconData, { x: cx + (colW - 0.5) / 2, y: cardY + 0.3 + (circleD - 0.5) / 2, w: 0.5, h: 0.5 });
    body += text(col.title, { x: cx, y: cardY + 1.35, w: colW, h: 0.5, size: 19, color: INK, bold: true });

    let rowY = cardY + 2.05;
    const rowH = 0.9;
    for (const r of col.rows) {
      body += rect({ x: cx + 0.25, y: rowY, w: 0.9, h: 0.32, color: r.color, radius: 0.06 });
      body += text(r.provider, { x: cx + 0.25, y: rowY, w: 0.9, h: 0.32, size: 9.5, color: WHITE, bold: true, valign: "middle" });
      body += text(r.service, { x: cx + 0.25, y: rowY + 0.36, w: colW - 0.5, h: 0.5, size: 12.5, color: SLATE, align: "left" });
      rowY += rowH;
    }
  }
  body += text("+ Terraform — infraestructura como código, multicloud, para desplegar cualquiera de estos servicios de forma reproducible",
    { x: 0.5, y: 6.75, w: 12.33, h: 0.4, size: 11.5, color: SLATE, italic: true });

  fs.writeFileSync(path.join(__dirname, "html", "que_hay_en_la_nube.html"), PAGE("#FFFFFF", body));
}

async function buildProductoDeDatos() {
  const INK = "1E2761", SLATE = "475569", ACCENT = "2563EB", ACCENT_BG = "EFF6FF", WHITE = "FFFFFF", CARD_BG = "F8FAFC";
  const steps = [
    { icon: FaDatabase, label: "Datos crudos", desc: "Transacciones, clics, sensores, texto" },
    { icon: FaBrain, label: "Modelo", desc: "Aprende patrones sobre datos históricos" },
    { icon: FaBoxOpen, label: "Producto de datos", desc: "Predicción, score o recomendación" },
    { icon: FaHandPointRight, label: "Decisión", desc: "El usuario actúa con esa información" },
  ];
  const examples = [
    { icon: FaFilm, name: "Netflix", desc: "Recomienda qué ver" },
    { icon: FaMusic, name: "Spotify", desc: "Arma tu playlist semanal" },
    { icon: FaMapMarkedAlt, name: "Google Maps", desc: "Elige la ruta más rápida" },
    { icon: FaCreditCard, name: "FICO Score", desc: "Califica tu riesgo crediticio" },
    { icon: FaChartLine, name: "Trading algorítmico", desc: "Genera señales de compra/venta" },
  ];
  let body = "";
  body += text("Anatomía de un producto de datos", { x: 0.5, y: 0.28, w: 12.33, h: 0.6, size: 32, color: INK, bold: true });
  body += text("El mismo patrón se repite sin importar la industria", { x: 0.5, y: 0.85, w: 12.33, h: 0.35, size: 14, color: SLATE, italic: true });

  const boxW = 2.6, boxH = 1.7, arrowW = 0.5, boxY = 1.7;
  const flowTotalW = steps.length * boxW + (steps.length - 1) * arrowW;
  const flowStartX = (13.33 - flowTotalW) / 2;
  const arrowIcon = await iconToPngDataUrl(FaLongArrowAltRight, { color: "#94A3B8", size: 256 });

  for (let i = 0; i < steps.length; i++) {
    const s = steps[i];
    const bx = flowStartX + i * (boxW + arrowW);
    body += rect({ x: bx, y: boxY, w: boxW, h: boxH, color: i === 2 ? ACCENT_BG : CARD_BG, radius: 0.1 });
    const circleD = 0.6;
    body += ellipse({ x: bx + (boxW - circleD) / 2, y: boxY + 0.2, w: circleD, h: circleD, color: i === 2 ? ACCENT : "94A3B8" });
    const stepIcon = await iconToPngDataUrl(s.icon, { color: "#FFFFFF", size: 256 });
    body += img(stepIcon, { x: bx + (boxW - 0.35) / 2, y: boxY + 0.2 + (circleD - 0.35) / 2, w: 0.35, h: 0.35 });
    body += text(s.label, { x: bx + 0.1, y: boxY + 0.95, w: boxW - 0.2, h: 0.35, size: 14.5, color: INK, bold: true });
    body += text(s.desc, { x: bx + 0.15, y: boxY + 1.32, w: boxW - 0.3, h: 0.36, size: 10.5, color: SLATE });
    if (i < steps.length - 1) {
      body += img(arrowIcon, { x: bx + boxW + (arrowW - 0.3) / 2, y: boxY + boxH / 2 - 0.15, w: 0.3, h: 0.3 });
    }
  }

  body += text("Mismo patrón, cinco industrias", { x: 0.5, y: 3.75, w: 12.33, h: 0.35, size: 16, color: INK, bold: true });

  const exCardW = 2.3, exGap = 0.2, exCardH = 1.9, exY = 4.25;
  const exTotalW = examples.length * exCardW + (examples.length - 1) * exGap;
  const exStartX = (13.33 - exTotalW) / 2;
  for (let i = 0; i < examples.length; i++) {
    const ex = examples[i];
    const ex_x = exStartX + i * (exCardW + exGap);
    body += rect({ x: ex_x, y: exY, w: exCardW, h: exCardH, color: CARD_BG, radius: 0.1 });
    const circleD = 0.65;
    body += ellipse({ x: ex_x + (exCardW - circleD) / 2, y: exY + 0.25, w: circleD, h: circleD, color: ACCENT });
    const exIcon = await iconToPngDataUrl(ex.icon, { color: "#FFFFFF", size: 256 });
    body += img(exIcon, { x: ex_x + (exCardW - 0.38) / 2, y: exY + 0.25 + (circleD - 0.38) / 2, w: 0.38, h: 0.38 });
    body += text(ex.name, { x: ex_x + 0.1, y: exY + 1.05, w: exCardW - 0.2, h: 0.4, size: 13, color: INK, bold: true });
    body += text(ex.desc, { x: ex_x + 0.15, y: exY + 1.46, w: exCardW - 0.3, h: 0.42, size: 10.5, color: SLATE });
  }

  body += text("El término &quot;producto de datos&quot; se formalizó con Data Mesh (Zhamak Dehghani, O'Reilly, 2022) — tratar el dato con la misma disciplina de producto que el software.",
    { x: 0.5, y: 6.35, w: 12.33, h: 0.5, size: 11, color: SLATE, italic: true });

  fs.writeFileSync(path.join(__dirname, "html", "producto_de_datos.html"), PAGE("#FFFFFF", body));
}

async function main() {
  fs.mkdirSync(path.join(__dirname, "html"), { recursive: true });
  await build5vs();
  await buildOnpremCloud();
  await buildQueHayEnLaNube();
  await buildProductoDeDatos();
  console.log("HTML generado en ./html/");
}

main().catch((e) => { console.error(e); process.exit(1); });
