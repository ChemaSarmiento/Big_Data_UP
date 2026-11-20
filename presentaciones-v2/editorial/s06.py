"""S6 · Visualización ejecutiva con Data Studio (antes Looker Studio) sobre varias tablas Gold.
Cifras: recursos/tweets/s06_tema_dia.json, s06_gold.json y verdad.json (consultas reales de referencia)."""
import json, html
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guion import slide, p, step, table, flow, code, proof, lablink, source

E = html.escape
ROOT = Path(__file__).resolve().parents[1]
ROWS = json.loads((ROOT / 'recursos/tweets/s06_tema_dia.json').read_text())
V = json.loads((ROOT / 'recursos/tweets/verdad.json').read_text())
G = json.loads((ROOT / 'recursos/tweets/s06_gold.json').read_text())
LAB = json.loads((ROOT / 'especialidad-06/contenido.json').read_text())['lab']['steps']

TITLE = 'Un tablero decide antes de que alguien lo lea'
BIGIDEA = 'Un tablero útil muestra la base de la comparación, qué cubre y lo que el dato no dice, con datos de más de una tabla Gold.'


# ---------- datos ----------
FECHAS = sorted(k for k in V['tweets_por_dia'] if k[0] == '2')
DIA = {f: V['tweets_por_dia'][f] for f in FECHAS}
TEMAS = ['energia', 'sanciones', 'mercados', 'alimentos', 'cadena_suministro', 'aviacion']
NOM = {'energia': 'Energía', 'sanciones': 'Sanciones', 'mercados': 'Mercados', 'alimentos': 'Alimentos',
       'cadena_suministro': 'Cadena de suministro', 'aviacion': 'Aviación'}
GRUPOS = ['en', 'es', 'otro']
RAW = {t: {f: 0 for f in FECHAS} for t in TEMAS}
BYL = {t: {g: {f: [0, 0] for f in FECHAS} for g in GRUPOS} for t in TEMAS}
for r in ROWS:
    RAW[r['tema']][r['fecha']] += int(r['tweets_tema'])
    BYL[r['tema']][r['grupo_idioma']][r['fecha']] = [int(r['tweets_tema']), int(r['tweets_dia'])]
PCT = {t: [100 * RAW[t][f] / DIA[f] for f in FECHAS] for t in TEMAS}
RAWL = {t: [RAW[t][f] for f in FECHAS] for t in TEMAS}
TOT = {t: sum(RAW[t].values()) for t in TEMAS}
BASE = sum(DIA.values())
assert BASE == V['tablas']['tweets_silver.tweets']['filas'] == 6798932
assert TOT['energia'] == V['gold_temas_total']['energia']['tweets'] == 137598
LP = {t: {g: (sum(BYL[t][g][f][0] for f in FECHAS), sum(BYL[t][g][f][1] for f in FECHAS)) for g in GRUPOS} for t in TEMAS}
assert LP['sanciones']['en'] == (67086, 4013172)


def n(x): return f'{x:,}'
def d1(x): return f'{x:.1f}'
def d2(x): return f'{x:.2f}'


EN = PCT['energia']
i16, i17, i20, i23 = 0, 1, 4, 7
ANT = [EN[i] for i in range(0, 7)]
assert d1(min(ANT)) == '1.6' and d1(max(ANT)) == '1.9' and d1(EN[i23]) == '3.1'
ALI = PCT['alimentos']; ALIR = RAWL['alimentos']
K25 = FECHAS.index('2022-03-25')
ali_raw_chg = 100 * (ALIR[K25] / ALIR[1] - 1)       # 17 -> 25 de marzo
ali_pct_chg = 100 * (ALI[K25] / ALI[1] - 1)
dias_energia_top = sum(1 for k in range(12) if max(TEMAS, key=lambda t: RAWL[t][k]) == 'energia')
assert dias_energia_top == 11


# ---------- gráficas reutilizadas ----------

def svg(w, h, inner, label, cls=''):
    return f'<div class="vz-wrap"><svg class="vz {cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{E(label, quote=True)}">{inner}</svg></div>'

def lines(fx, fy, w, h, series, ymax, yticks, fmt, partial=True, clutter=False, xlab=True, ylab=True, dots=False, plabel=False):
    k = len(FECHAS)
    X = lambda i: fx + i * w / (k - 1)
    Y = lambda v: fy + h - v / ymax * h
    o = []
    if partial:
        o.append(f'<rect class="partial" x="{fx - 6}" y="{fy}" width="{w / (k - 1) * 0.5 + 6:.1f}" height="{h}"/>')
        if plabel:
            o.append(f'<text class="sm" x="{fx + 4}" y="{fy + 24}">día parcial</text>')
    for t in yticks:
        y = Y(t)
        o.append(f'<line class="{"grid heavy" if clutter else "grid"}" x1="{fx}" x2="{fx + w}" y1="{y:.1f}" y2="{y:.1f}"/>')
        if ylab:
            o.append(f'<text class="tick" x="{fx - 10}" y="{y + 7:.1f}" text-anchor="end">{fmt(t)}</text>')
    o.append(f'<line class="axis" x1="{fx}" x2="{fx + w}" y1="{fy + h}" y2="{fy + h}"/>')
    if xlab:
        for i, f in enumerate(FECHAS):
            if k > 8 and w < 520 and i % 2 == 1:
                continue
            o.append(f'<text class="tick" x="{X(i):.1f}" y="{fy + h + 28}" text-anchor="middle">{int(f[-2:])}</text>')
    for s in series:
        pts = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(s['v']))
        o.append(f'<polyline class="ln l-{s["c"]}" points="{pts}" style="stroke-width:{s.get("w", 5)}px"/>')
        if dots:
            o.extend(f'<circle class="dot d-{s["c"]}" cx="{X(i):.1f}" cy="{Y(v):.1f}" r="6"/>' for i, v in enumerate(s['v']))
        if s.get('name'):
            ly = Y(s['v'][-1]) + s.get('dy', 8)
            o.append(f'<text class="lb t-{s["c"]}" x="{X(k - 1) + 14:.1f}" y="{ly:.1f}">{s["name"]}</text>')
        for (i, txt, dx, dy) in s.get('pts', []):
            o.append(f'<circle class="dot d-{s["c"]}" cx="{X(i):.1f}" cy="{Y(s["v"][i]):.1f}" r="8"/>')
            o.append(f'<text class="val t-{s["c"]}" x="{X(i) + dx:.1f}" y="{Y(s["v"][i]) + dy:.1f}">{txt}</text>')
    return ''.join(o)

def arr(x1, y1, x2, y2, cls='arrow'):
    import math
    a = math.atan2(y2 - y1, x2 - x1); s = 14
    p1 = (x2 - s * math.cos(a - .45), y2 - s * math.sin(a - .45)); p2 = (x2 - s * math.cos(a + .45), y2 - s * math.sin(a + .45))
    return (f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2 - 4 * math.cos(a):.1f}" y2="{y2 - 4 * math.sin(a):.1f}"/>'
            f'<polygon class="arrowhead" points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"/>')

def hbars(fx, fy, labw, w, rows, vmax, rowh=62, barh=40, fmt=lambda v: f'{v}', unit=''):
    o = []
    for i, (lab, v, c) in enumerate(rows):
        y = fy + i * rowh
        L = max(2, v / vmax * w)
        o.append(f'<text class="lbl" x="{fx}" y="{y + barh * .72:.1f}">{lab}</text>')
        o.append(f'<rect class="b-{c}" x="{fx + labw}" y="{y}" width="{L:.1f}" height="{barh}"/>')
        o.append(f'<text class="val t-{c}" x="{fx + labw + L + 12:.1f}" y="{y + barh * .72:.1f}">{fmt(v)}{unit}</text>')
    o.append(f'<line class="axis" x1="{fx + labw}" x2="{fx + labw}" y1="{fy - 6}" y2="{fy + len(rows) * rowh - 14}"/>')
    return ''.join(o)

def vbars(fx, fy, w, h, vals, ymax, cls, labels, valfmt=None, hatch=None):
    k = len(vals); bw = w / k * 0.62; o = []
    for i, v in enumerate(vals):
        x = fx + i * w / k + (w / k - bw) / 2; hh = v / ymax * h
        c = 'ctx' if hatch is None or i not in hatch else 'partialbar'
        c = cls[i] if isinstance(cls, list) else c
        o.append(f'<rect class="b-{c}" x="{x:.1f}" y="{fy + h - hh:.1f}" width="{bw:.1f}" height="{hh:.1f}"/>')
        o.append(f'<text class="tick" x="{x + bw / 2:.1f}" y="{fy + h + 28}" text-anchor="middle">{labels[i]}</text>')
        if valfmt:
            o.append(f'<text class="sm" x="{x + bw / 2:.1f}" y="{fy + h - hh - 10:.1f}" text-anchor="middle">{valfmt(v)}</text>')
    o.append(f'<line class="axis" x1="{fx}" x2="{fx + w}" y1="{fy + h}" y2="{fy + h}"/>')
    return ''.join(o)

def panel(sql, header, rows, meta):
    th = ''.join(f'<th scope="col">{h}</th>' for h in header)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return (f'<div class="qp"><pre tabindex="0"><code>{E(sql)}</code></pre>'
            f'<div class="qres"><table class="matrix"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
            f'<p class="qmeta">{meta}</p></div></div>')

def two_stories():
    left = lines(110, 70, 480, 270, [
        dict(v=RAWL['energia'], c='hl', name='Energía', dy=2),
        dict(v=RAWL['alimentos'], c='alert', name='Alimentos', dy=8, pts=[(1, n(ALIR[1]), -10, -22), (K25, n(ALIR[K25]), -30, -22)])],
        18000, [0, 6000, 12000, 18000], lambda t: f'{t // 1000}k', plabel=False)
    right = lines(830, 70, 440, 270, [
        dict(v=PCT['energia'], c='hl', name='Energía', dy=-2),
        dict(v=PCT['alimentos'], c='alert', name='Alimentos', dy=14, pts=[(1, d2(ALI[1]), -10, -20), (K25, d2(ALI[K25]), -34, -22)])],
        3.5, [0, 1, 2, 3], lambda t: f'{t}', plabel=False)
    inner = (f'<text class="head" x="110" y="34">CONTEO DE TWEETS POR DÍA</text><text class="head" x="830" y="34">% DE LOS TWEETS DE ESE DÍA</text>'
             + left + right
             + f'<g data-step="1"><text class="big alert" x="110" y="440">Alimentos {ali_raw_chg:+.0f} %</text><text class="sm" x="110" y="468">del 17 al 25 de marzo: «casi no cambia»</text></g>'
             + f'<g data-step="1"><text class="big alert" x="830" y="440">Alimentos {ali_pct_chg:+.0f} %</text><text class="sm" x="830" y="468">su peso en la conversación: «sube»</text></g>')
    return svg(1440, 490, inner, 'Dos gráficas de líneas con los mismos tweets: conteo diario y porcentaje del día para energía y alimentos')

def chart_chooser():
    inner = (
        '<g><rect class="box" x="20" y="10" width="640" height="220"/><text class="head" x="44" y="38">¿CÓMO CAMBIA EN EL TIEMPO? → LÍNEA</text>' + lines(80, 62, 540, 120, [dict(v=EN, c='hl')], 3.5, [0, 2], str, xlab=False, partial=False) + '<text class="sm" x="44" y="214">energía, % del día, 16–27 mar</text></g>'
        '<g data-step="1"><rect class="box" x="720" y="10" width="700" height="220"/><text class="head" x="744" y="38">¿QUÉ TEMA ES MÁS GRANDE? → BARRAS</text>' + hbars(744, 62, 190, 340, [(NOM[x], TOT[x] / BASE * 100, 'hl' if x == 'energia' else 'ctx') for x in TEMAS[:4]], 2.6, rowh=38, barh=26, fmt=lambda v: f'{v:.1f}', unit=' %') + '</g>'
        '<g data-step="2"><rect class="box" x="20" y="250" width="640" height="220"/><text class="head" x="44" y="278">¿CUÁL ES EL VALOR EXACTO? → TABLA</text>'
        + ''.join(f'<text class="mono" x="44" y="{y}">{d} mar     {n(RAW["energia"][f"2022-03-{d}"])} tweets</text>' for d, y in zip(['23', '24', '25'], [328, 372, 416]))
        + '<text class="sm" x="44" y="456">energía: los tres días de mayor volumen</text></g>'
        '<g data-step="3"><rect class="box focus" x="720" y="250" width="700" height="220"/><text class="head" x="744" y="278">¿CUÁL ES EL NÚMERO QUE IMPORTA? → TARJETA</text>'
        f'<text class="huge" x="744" y="400">{n(TOT["energia"])}</text><text class="sm" x="744" y="440">tweets de energía en 12 días · {d2(100 * TOT["energia"] / BASE)} % del total</text></g>')
    return svg(1440, 490, inner, 'Cuatro preguntas y el gráfico que corresponde a cada una: línea, barras, tabla y tarjeta, con datos de energía')

def axis_cut():
    a, b = EN[i20], EN[i23]
    H = 300; ymax = 3.5
    left = (f'<text class="head" x="60" y="34">EJE DESDE 0 · las barras dicen la verdad</text>'
            f'<line class="axis" x1="120" x2="640" y1="{60 + H}" y2="{60 + H}"/>'
            f'<rect class="b-ctx" x="190" y="{60 + H - a / ymax * H:.1f}" width="150" height="{a / ymax * H:.1f}"/><text class="val" x="265" y="{60 + H - a / ymax * H - 12:.1f}" text-anchor="middle">{d2(a)}</text>'
            f'<rect class="b-hl" x="420" y="{60 + H - b / ymax * H:.1f}" width="150" height="{b / ymax * H:.1f}"/><text class="val t-hl" x="495" y="{60 + H - b / ymax * H - 12:.1f}" text-anchor="middle">{d2(b)}</text>'
            f'<text class="tick" x="265" y="{60 + H + 30}" text-anchor="middle">20 mar</text><text class="tick" x="495" y="{60 + H + 30}" text-anchor="middle">23 mar</text>'
            f'<text class="big hl" x="120" y="440">La barra crece ×{b / a:.1f}</text>')
    base = 1.4; ymin, ymx = base, 3.2
    ha = (a - ymin) / (ymx - ymin) * H; hb = (b - ymin) / (ymx - ymin) * H
    right = (f'<text class="head" x="800" y="34">EJE CORTADO EN {base} · las barras mienten</text>'
             f'<line class="axis" x1="860" x2="1380" y1="{60 + H}" y2="{60 + H}"/>'
             f'<rect class="b-ctx" x="930" y="{60 + H - ha:.1f}" width="150" height="{ha:.1f}"/><text class="val" x="1005" y="{60 + H - ha - 12:.1f}" text-anchor="middle">{d2(a)}</text>'
             f'<rect class="b-alert" x="1160" y="{60 + H - hb:.1f}" width="150" height="{hb:.1f}"/><text class="val t-alert" x="1235" y="{60 + H - hb - 12:.1f}" text-anchor="middle">{d2(b)}</text>'
             f'<text class="tick" x="1005" y="{60 + H + 30}" text-anchor="middle">20 mar</text><text class="tick" x="1235" y="{60 + H + 30}" text-anchor="middle">23 mar</text>'
             f'<text class="tick" x="850" y="{60 + H + 6}" text-anchor="end">{base}</text>'
             f'<text class="big alert" x="860" y="440">La barra crece ×{hb / ha:.1f}</text>')
    return svg(1440, 470, left + f'<g data-step="1">{right}</g>', 'Dos gráficas de barras con los mismos dos valores: con eje desde cero la diferencia es el doble; con eje cortado parece diez veces')

def emphasis():
    cols = ['hl', 'c1', 'c2', 'c3', 'alert', 'ctx']
    left = lines(90, 66, 520, 240, [dict(v=PCT[t], c=cols[k], w=4) for k, t in enumerate(TEMAS)], 3.5, [0, 1, 2, 3], str, plabel=False)
    leg = ''.join(f'<g><rect class="b-{cols[k]}" x="{70 + (k % 3) * 230}" y="{356 + (k // 3) * 38}" width="22" height="22"/><text class="sm" x="{70 + (k % 3) * 230 + 30}" y="{374 + (k // 3) * 38}">{NOM[t] if t != "cadena_suministro" else "Cadena sumin."}</text></g>' for k, t in enumerate(TEMAS))
    gray = [dict(v=PCT[t], c='ctx', w=4, name=NOM[t] if t in ('sanciones', 'mercados', 'alimentos') else None, dy={'sanciones': -4, 'mercados': 20, 'alimentos': -8}.get(t, 8)) for t in TEMAS[1:]]
    right = lines(830, 66, 400, 240, gray + [dict(v=EN, c='hl', w=7, name='Energía', dy=2, pts=[(7, d1(EN[i23]) + ' %', -34, -22)])], 3.5, [0, 1, 2, 3], str, plabel=False)
    inner = (f'<text class="head" x="90" y="34">SEIS COLORES + LEYENDA</text><text class="head" x="830" y="34">UN ACENTO + ETIQUETAS</text>' + left + leg
             + f'<g data-step="1">{right}<text class="big hl" x="830" y="410">El ojo va solo a energía.</text></g>')
    return svg(1440, 470, inner, 'Seis líneas de colores con leyenda frente a cinco líneas grises y una sola azul con etiquetas directas')

def titles():
    chart = lines(70, 70, 450, 250, [dict(v=EN, c='hl', w=6, pts=[(7, d1(EN[i23]) + ' %', -34, -22)])], 3.5, [0, 1, 2, 3], str, plabel=True)
    return ('<div class="tw"><div class="titles">'
            '<div class="tt bad"><span class="chip">DESCRIBE</span><p>«Tweets por tema y por día»</p><small>Nombra el gráfico; no dice qué ver.</small></div>'
            '<div class="tt bad" data-step="1"><span class="chip">VAGO</span><p>«Energía subió»</p><small>¿Cuánto? ¿Cuándo? ¿Respecto de qué?</small></div>'
            f'<div class="tt good" data-step="2"><span class="chip">CONCLUYE</span><p>«Energía pasó de {d1(min(ANT))}–{d1(max(ANT))} % a {d1(EN[i23])} % de los tweets el 23 de marzo; el dato no explica por qué»</p><small>Hecho + comparación + límite.</small></div></div>'
            + svg(600, 380, f'<text class="head" x="70" y="34">ENERGÍA · % DE LOS TWEETS DEL DÍA</text>{chart}', 'Serie de energía con el pico del 23 de marzo señalado', 'side') + '</div>')

def partial_day():
    vals = [DIA[f] for f in FECHAS]
    left = (f'<text class="head" x="40" y="30">TWEETS TOTALES POR DÍA</text>'
            + vbars(60, 50, 600, 290, vals, 800000, ['partialbar'] + ['ctx'] * 11, [str(int(f[-2:])) for f in FECHAS], valfmt=lambda v: f'{v // 1000}k')
            + f'<text class="big alert" x="60" y="410">16 de marzo: {n(DIA[FECHAS[0]])}</text><text class="sm" x="60" y="440">17 % de un día completo</text>')
    r1 = RAWL['energia'][1] / RAWL['energia'][0]; p1 = EN[1] / EN[0]
    w0 = 320
    right = ('<text class="head" x="800" y="30">ENERGÍA, 16 → 17 DE MARZO</text>'
             f'<text class="lbl" x="800" y="86">Conteo</text><text class="tick" x="1004" y="86" text-anchor="end">16 mar</text><text class="tick" x="1004" y="128" text-anchor="end">17 mar</text>'
             f'<rect class="b-ctx" x="1016" y="62" width="{RAWL["energia"][0] / RAWL["energia"][1] * w0:.1f}" height="34"/><text class="val" x="{1026 + RAWL["energia"][0] / RAWL["energia"][1] * w0:.1f}" y="88">{n(RAWL["energia"][0])}</text>'
             f'<rect class="b-hl" x="1016" y="104" width="{w0}" height="34"/><text class="val t-hl" x="{1026 + w0}" y="130">{n(RAWL["energia"][1])}</text>'
             f'<text class="big alert" x="800" y="196">×{r1:.1f}</text><text class="sm" x="920" y="196">parece que energía explotó</text>'
             f'<g data-step="1"><text class="lbl" x="800" y="270">% del día</text><text class="tick" x="1004" y="270" text-anchor="end">16 mar</text><text class="tick" x="1004" y="312" text-anchor="end">17 mar</text>'
             f'<rect class="b-ctx" x="1016" y="246" width="{EN[0] / EN[1] * w0:.1f}" height="34"/><text class="val" x="{1026 + EN[0] / EN[1] * w0:.1f}" y="272">{d2(EN[0])}</text>'
             f'<rect class="b-hl" x="1016" y="288" width="{w0}" height="34"/><text class="val t-hl" x="{1026 + w0}" y="314">{d2(EN[1])}</text>'
             f'<text class="big hl" x="800" y="380">+{100 * (p1 - 1):.0f} %</text><text class="sm" x="920" y="380">el peso de energía casi no cambió</text></g>')
    return svg(1440, 470, left + right, 'Barras de tweets por día con el 16 de marzo parcial; y energía del 16 al 17 en conteo y en porcentaje')

def languages():
    rows1 = [(f'{g}', 100 * LP['sanciones'][g][0] / LP['sanciones'][g][1], 'hl' if g == 'en' else 'ctx') for g in GRUPOS]
    rows2 = [(f'{g}', 100 * LP['energia'][g][0] / LP['energia'][g][1], 'hl' if g == 'en' else 'ctx') for g in GRUPOS]
    inner = ('<text class="head" x="40" y="30">SANCIONES · % de los tweets de cada idioma</text>'
             + hbars(40, 60, 140, 330, [({'en': 'inglés', 'es': 'español', 'otro': 'otros'}[a], b, c) for a, b, c in rows1], 2.6, rowh=72, barh=44, fmt=lambda v: f'{v:.2f}', unit=' %')
             + '<text class="head" x="800" y="30">ENERGÍA · % de los tweets de cada idioma</text>'
             + f'<g data-step="1">{hbars(800, 60, 140, 330, [({"en": "inglés", "es": "español", "otro": "otros"}[a], b, c) for a, b, c in rows2], 2.6, rowh=72, barh=44, fmt=lambda v: f"{v:.2f}", unit=" %")}</g>'
             + f'<g data-step="2"><text class="big" x="40" y="330">«Otros» son {n(LP["sanciones"]["otro"][1])} tweets ({100 * LP["sanciones"]["otro"][1] / BASE:.0f} %):</text><text class="big hl" x="40" y="372">mezclarlos diluye el tema.</text></g>')
    return svg(1440, 420, inner, 'Barras del porcentaje de sanciones y de energía en inglés, español y otros idiomas, desde cero')

def keyword():
    words = [('inflación', 28280, 'alert'), ('precios', 9161, 'ctx'), ('mercados', 1121, 'hl'), ('bolsa', 746, 'ctx')]
    inner = ('<text class="head" x="40" y="30">TEMA «MERCADOS» EN ESPAÑOL · tweets por palabra clave</text>'
             + hbars(40, 56, 170, 470, [(a, b, c) for a, b, c in words], 28280, rowh=64, barh=42, fmt=n)
             + '<g data-step="1"><rect class="box focus" x="860" y="40" width="560" height="170"/><text class="head" x="880" y="72">18 DE MARZO · ESPAÑOL</text><text class="huge" x="880" y="140">11,917</text><text class="sm" x="880" y="172">tweets con «inflación»: 11,850 textos distintos,</text><text class="sm" x="880" y="198">9,736 usuarios. No es spam: es una conversación.</text></g>'
             + '<g data-step="2"><rect class="box" x="860" y="232" width="560" height="200"/><text class="head" x="880" y="264">LO QUE DICEN ESOS TWEETS</text>'
             + '<text class="sm" x="880" y="298">«COMENZÓ LA GUERRA CONTRA LA INFLACIÓN. Así lo</text><text class="sm" x="880" y="324">anunció el presidente Alberto Fernández…»</text>'
             + '<text class="sm" x="880" y="366">«Arde uno de los mayores mercados de Europa</text><text class="sm" x="880" y="392">del Este tras los bombardeos…» (un mercado físico)</text></g>'
             + '<g data-step="3"><text class="big alert" x="40" y="388">«inflación»: 25 veces más tweets</text><text class="big alert" x="40" y="428">que la palabra «mercados».</text><text class="sm" x="40" y="462">El tablero hereda las palabras clave de Gold.</text></g>')
    return svg(1440, 480, inner, 'Barras de las palabras que llenan el tema mercados en español, con ejemplos de los tweets del 18 de marzo')

def board_bad():
    mini = lines(84, 100, 580, 250, [dict(v=RAWL[t], c=c, w=3) for t, c in zip(TEMAS, ['hl', 'c1', 'c2', 'c3', 'alert', 'ctx'])], 18000, [0, 6000, 12000, 18000], lambda t: f'{t // 1000}k', partial=False, ylab=True)
    inner = ('<rect class="box bad" x="10" y="8" width="720" height="440"/>'
             '<text class="lbl" x="40" y="58">Tweets por tema</text>'
             '<rect class="box" x="450" y="30" width="240" height="46"/><text class="sm" x="466" y="60">Total: 6,798,932</text>'
             + mini + '<text class="sm" x="84" y="418">Todos los idiomas · todos los días · sin nota</text>'
             '<g data-step="1"><circle class="badge" cx="44" cy="300" r="20"/><text class="badge-t" x="44" y="309" text-anchor="middle">1</text></g>'
             '<g data-step="2"><circle class="badge" cx="360" cy="150" r="20"/><text class="badge-t" x="360" y="159" text-anchor="middle">2</text></g>'
             '<g data-step="3"><circle class="badge" cx="690" cy="410" r="20"/><text class="badge-t" x="690" y="419" text-anchor="middle">3</text></g>')
    right = ('<g transform="translate(780,10)">'
             '<g data-step="1"><text class="lbl" x="0" y="40">1 · Día parcial</text><text class="sm" x="0" y="72">El 16 de marzo tiene 134,871 tweets;</text><text class="sm" x="0" y="100">el 17, 778,608. La línea «arranca».</text></g>'
             '<g data-step="2"><text class="lbl" x="0" y="168">2 · Conteo sin base</text><text class="sm" x="0" y="200">Las series siguen al volumen del día,</text><text class="sm" x="0" y="228">no al peso del tema.</text></g>'
             '<g data-step="3"><text class="lbl" x="0" y="296">3 · Idiomas mezclados</text><text class="sm" x="0" y="328">Sin filtro ni aviso: inglés pesa 59 %,</text><text class="sm" x="0" y="356">y el resto no se ve.</text></g></g>')
    return svg(1440, 470, inner + right, 'Tablero de ejemplo con seis líneas de conteo crudo, sin filtro de idioma ni nota, con tres defectos numerados')

def demo_payload():
    out = {'fechas': [f[-2:] for f in FECHAS], 'nombres': NOM, 'temas': TEMAS, 'datos': {}}
    for t in TEMAS:
        out['datos'][t] = {}
        for g in GRUPOS:
            out['datos'][t][g] = {'n': [BYL[t][g][f][0] for f in FECHAS], 'dia': [BYL[t][g][f][1] for f in FECHAS]}
        out['datos'][t]['todos'] = {'n': [RAW[t][f] for f in FECHAS], 'dia': [DIA[f] for f in FECHAS]}
    return out

def filter_demo():
    opts_t = ''.join(f'<option value="{t}"{" selected" if t == "energia" else ""}>{NOM[t]}</option>' for t in TEMAS)
    opts_g = '<option value="todos">Todos los idiomas</option><option value="en">Inglés</option><option value="es">Español</option><option value="otro">Otros idiomas</option>'
    return (f'<div class="demo" data-demo="filtro" data-series="{E(json.dumps(demo_payload(), separators=(",", ":")), quote=True)}">'
            f'<div class="demo-bar"><label>Tema <select data-tema>{opts_t}</select></label><label>Idioma <select data-idioma>{opts_g}</select></label></div>'
            '<h2 class="demo-title" data-titulo></h2>'
            '<svg class="vz" data-plot viewBox="0 0 1440 300" role="img" aria-label="Serie del tema seleccionado como porcentaje del día"></svg>'
            '<p class="demo-cover" data-cobertura></p></div>')


# ---------- fuentes ----------
DATA = 'Tablas Gold de tweets · 16–27 mar 2022 · uso académico'
GOLD6 = 'tweets_gold · seis tablas · 16–27 mar 2022 · uso académico'
SDS = source('Storytelling with Data · so what?', 'https://www.storytellingwithdata.com/blog/2017/3/22/so-what')
DUARTE = source('Duarte · Resonate', 'https://www.duarte.com/resources/books/resonate/')
CONN = source('Data Studio (antes Looker Studio) · conector de BigQuery', 'https://docs.cloud.google.com/looker/docs/studio/connect-to-google-bigquery')
CRED = source('Data Studio · credenciales de datos', 'https://docs.cloud.google.com/looker/docs/studio/data-credentials')
COSTS = source('BigQuery · estimar y controlar costos', 'https://docs.cloud.google.com/bigquery/docs/best-practices-costs')
JOBS = source('BigQuery · INFORMATION_SCHEMA.JOBS', 'https://docs.cloud.google.com/bigquery/docs/information-schema-jobs')
CURSO = 'Curso Big Data · Especialidad'

# ---------- datos de las otras cinco tablas Gold ----------
HASH = {}
for r in G['hashtags_top_por_dia']:
    HASH.setdefault(r['hashtag'], {})[r['fecha']] = (int(r['tweets']), float(r['pct_del_dia']))
HORA = {}
for r in G['actividad_hora']:
    HORA.setdefault(r['fecha'], {}).setdefault(int(r['hora_utc']), {})[r['grupo_idioma']] = int(r['tweets'])
APPS = {}
for r in G['aplicaciones_dia']:
    APPS.setdefault(r['fecha'], {})[r['aplicacion']] = int(r['tweets'])
ALC = G['autores_alcance']
CV = V['gold_extra']['conversacion_total']
D23 = '2022-03-23'
H23 = HORA[D23]
assert HASH['ukraine'][D23] == (49393, 8.711)
assert int(ALC[4]['autores']) == 1375 and float(ALC[4]['pct_likes']) == 17.66
assert H23[18]['en'] == 18476 and H23[14]['es'] == 5679
assert sum(sum(h.values()) for h in HORA['2022-03-16'].values()) == 134871 and sorted(HORA['2022-03-16']) == [20, 21, 22, 23]
LIKES_TOT = sum(CV[k]['likes'] for k in CV)
assert LIKES_TOT == V['engagement']['total_likes']
TW_TOT = sum(CV[k]['tweets'] for k in CV)
PCT_TW = {k: 100 * CV[k]['tweets'] / TW_TOT for k in CV}
PCT_LK = {k: 100 * CV[k]['likes'] / LIKES_TOT for k in CV}
APP23 = APPS[D23]; APP23_TOT = sum(APP23.values())
TRES_APPS = sum(APP23[a] for a in ('Twitter Web App', 'Twitter for Android', 'Twitter for iPhone'))
fn = lambda f: int(f[-2:])


# ---------- gráficas nuevas ----------
def hashtags_slide():
    top = sorted(((h, v[D23]) for h, v in HASH.items() if D23 in v), key=lambda x: -x[1][0])[:8]
    rows = [('#' + h, pct, 'hl' if i == 0 else 'ctx') for i, (h, (t, pct)) in enumerate(top)]
    left = ('<text class="head" x="40" y="30">23 DE MARZO · % DE LOS TWEETS DEL DÍA CON ESE HASHTAG</text>'
            + hbars(40, 52, 280, 330, rows, 9.5, rowh=46, barh=32, fmt=lambda v: f'{v:.2f}', unit=' %'))
    ser = [dict(v=[HASH['ukrainewar'].get(f, (0, 0))[1] for f in FECHAS], c='ctx', w=4, name='#ukrainewar', dy=14),
           dict(v=[HASH['standwithukraine'][f][1] for f in FECHAS], c='c1', w=5, name='#standwithukraine', dy=-6, pts=[(7, '4,999', -18, -20)]),
           dict(v=[HASH['nato'][f][1] for f in FECHAS], c='hl', w=6, name='#nato', dy=22, pts=[(7, '4,431', -18, 36)])]
    right = (lines(870, 100, 300, 220, ser, 1.0, [0, .5, 1], lambda t: f'{t:g}', plabel=False)
             + '<text class="head" x="870" y="30">% DEL DÍA · 12 DÍAS</text>'
             + '<text class="sm" x="870" y="60">Dos hashtags tienen su máximo el 24 de marzo.</text>')
    inner = left + f'<g data-step="1">{right}</g>' + '<g data-step="2"><text class="big alert" x="870" y="440">El dato no dice por qué.</text></g>'
    return svg(1440, 470, inner, 'Barras de los ocho hashtags con más tweets el 23 de marzo y líneas diarias de tres hashtags con máximo el 24 de marzo')


def alcance_slide():
    names = ['menos de 1 mil', '1 mil a 10 mil', '10 mil a 100 mil', '100 mil a 1 millón', 'más de 1 millón']
    o = ['<text class="head" x="40" y="30">SEGUIDORES DEL AUTOR</text>',
         '<rect class="b-ctx" x="760" y="14" width="22" height="22"/><text class="sm" x="790" y="32">% de los tweets</text>',
         '<rect class="b-hl" x="1000" y="14" width="22" height="22"/><text class="sm" x="1030" y="32">% de los likes</text>']
    fx, w, vmax = 380, 760, 70
    for i, r in enumerate(ALC):
        y = 62 + i * 76
        pt, pl = float(r['pct_tweets']), float(r['pct_likes'])
        o.append(f'<text class="lbl" x="40" y="{y + 38}">{names[i]}</text>')
        o.append(f'<rect class="b-ctx" x="{fx}" y="{y}" width="{max(3, pt / vmax * w):.1f}" height="30"/><text class="val" x="{fx + pt / vmax * w + 10:.1f}" y="{y + 24}">{pt:.2f} %</text>')
        o.append(f'<g data-step="1"><rect class="b-hl" x="{fx}" y="{y + 34}" width="{max(3, pl / vmax * w):.1f}" height="30"/><text class="val t-hl" x="{fx + pl / vmax * w + 10:.1f}" y="{y + 58}">{pl:.2f} %</text></g>')
    o.append(f'<line class="axis" x1="{fx}" x2="{fx}" y1="52" y2="{62 + 5 * 76 - 8}"/>')
    o.append('<g data-step="2"><text class="big alert" x="40" y="484">1,375 autores con más de 1 millón de seguidores:</text>'
             '<text class="big alert" x="40" y="522">0.84 % de los tweets, 17.66 % de los likes.</text></g>')
    return svg(1440, 540, ''.join(o), 'Barras agrupadas: porcentaje de tweets y porcentaje de likes por tamaño de audiencia del autor, desde cero')


def hourly(fx, fy, w, h, series, ymax, yticks):
    X = lambda i: fx + i * w / 23
    Y = lambda v: fy + h - v / ymax * h
    o = []
    for t in yticks:
        o.append(f'<line class="grid" x1="{fx}" x2="{fx + w}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text class="tick" x="{fx - 10}" y="{Y(t) + 7:.1f}" text-anchor="end">{t // 1000}k</text>')
    o.append(f'<line class="axis" x1="{fx}" x2="{fx + w}" y1="{fy + h}" y2="{fy + h}"/>')
    for i in range(0, 24, 3):
        o.append(f'<text class="tick" x="{X(i):.1f}" y="{fy + h + 28}" text-anchor="middle">{i:02d}</text>')
    o.append(f'<text class="sm" x="{fx + w}" y="{fy + h + 58}" text-anchor="end">hora UTC</text>')
    for s in series:
        pts = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(s['v']))
        o.append(f'<polyline class="ln l-{s["c"]}" points="{pts}" style="stroke-width:{s.get("w", 5)}px"/>')
        i, v = s['peak']
        o.append(f'<g data-step="1"><circle class="dot d-{s["c"]}" cx="{X(i):.1f}" cy="{Y(v):.1f}" r="8"/>'
                 f'<text class="lb t-{s["c"]}" x="{X(i) + s["dx"]:.1f}" y="{Y(v) + s["dy"]:.1f}">{s["name"]} · {n(v)} a las {i:02d}</text></g>')
    return ''.join(o)


def hora_slide():
    ser = []
    for g, c, name, dx, dy, w in [('otro', 'c2', 'otros idiomas', -300, 52, 5), ('es', 'c1', 'español', 20, 38, 5), ('en', 'hl', 'inglés', -150, -24, 6)]:
        v = [H23[h][g] for h in range(24)]
        ser.append(dict(v=v, c=c, w=w, name=name, dx=dx, dy=dy, peak=(max(range(24), key=lambda h: v[h]), max(v))))
    inner = ('<text class="head" x="60" y="30">23 DE MARZO · TWEETS POR HORA UTC Y GRUPO DE IDIOMA</text>'
             + hourly(110, 56, 1240, 290, ser, 20000, [0, 5000, 10000, 15000, 20000])
             + '<g data-step="2"><text class="big alert" x="60" y="440">El 16 de marzo solo tiene las horas 20 a 23 UTC: 134,871 tweets.</text></g>')
    return svg(1440, 480, inner, 'Tres líneas de tweets por hora el 23 de marzo, para inglés, español y otros idiomas, con su hora de máximo marcada')


def stack(y, label, pct, sub, step_n=None):
    cols = [('original', 'b-hl', 'originales'), ('respuesta', 'b-ctx', 'respuestas'), ('cita', 'b-c2', 'citas')]
    x, w, o = 300, 920, []
    for k, cls, name in cols:
        ww = pct[k] / 100 * w
        o.append(f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{ww:.1f}" height="74"/>')
        if ww > 130:
            o.append(f'<text class="lbl" x="{x + 14:.1f}" y="{y + 34}" style="fill:{"#fff" if cls != "b-ctx" else "#14213d"}">{pct[k]:.1f} %</text><text class="sm" x="{x + 14:.1f}" y="{y + 62}" style="fill:{"#fff" if cls != "b-ctx" else "#14213d"}">{name}</text>')
        else:
            o.append(f'<text class="lbl" x="{x + ww + 12:.1f}" y="{y + 34}" style="fill:#14213d">{pct[k]:.1f} %</text><text class="sm" x="{x + ww + 12:.1f}" y="{y + 62}">{name}</text>')
        x += ww
    head = f'<text class="lbl" x="40" y="{y + 36}">{label}</text><text class="sm" x="40" y="{y + 64}">{sub}</text>'
    g = head + ''.join(o)
    return g if step_n is None else f'<g data-step="{step_n}">{g}</g>'


def conversacion_slide():
    inner = ('<text class="head" x="40" y="30">TODO EL PERIODO · PARTES DE UN TODO (100 %)</text>'
             + stack(60, 'Tweets', PCT_TW, f'{n(TW_TOT)}')
             + stack(170, 'Likes', PCT_LK, f'{n(LIKES_TOT)}', 1)
             + '<g data-step="2"><text class="big alert" x="40" y="330">Las respuestas son la mitad de los tweets y reúnen solo el '
             + f'{PCT_LK["respuesta"]:.0f} % de los likes.</text><text class="sm" x="40" y="368">Mediana de likes por tipo, el 27 de marzo: 0 en originales, respuestas y citas.</text></g>')
    return svg(1440, 400, inner, 'Dos barras apiladas al cien por ciento: tweets y likes repartidos entre originales, respuestas y citas')


def dashboard_layout():
    def page(x, title, tag, items, st):
        o = f'<rect class="box focus" x="{x}" y="20" width="450" height="380"/><text class="lbl" x="{x + 22}" y="66">{title}</text><text class="head" x="{x + 22}" y="100">{tag}</text>'
        for j, (chart, table_) in enumerate(items):
            y = 134 + j * 82
            o += f'<rect class="box" x="{x + 22}" y="{y}" width="406" height="68"/><text class="sm" x="{x + 36}" y="{y + 30}">{chart}</text><text class="mono" style="font-size:21px;fill:#1f4f8f" x="{x + 36}" y="{y + 56}">{table_}</text>'
        return f'<g data-step="{st}">{o}</g>' if st else o
    inner = (page(10, '1 · Panorama', 'UNA PREGUNTA DE NEGOCIO', [('Serie del tema, % del día', 'tema_dia'), ('Tres tarjetas con su base', 'tema_dia'), ('Filtro de idioma + nota del día parcial', 'tema_dia')], 0)
             + page(490, '2 · Dentro del tema', 'DE QUÉ SE HABLA Y DESDE DÓNDE', [('Hashtags más frecuentes del día', 'hashtags_dia'), ('Aplicación desde la que se publica', 'aplicaciones_dia'), ('Filtro de fecha dentro de cada gráfica', 'hashtags_dia + aplicaciones_dia')], 1)
             + page(970, '3 · Quién, cuándo y cómo', 'QUIÉN HABLA, CUÁNDO, CÓMO', [('Tweets y likes por audiencia', 'autores_alcance'), ('Ritmo por hora y grupo de idioma', 'actividad_hora'), ('Originales, respuestas y citas', 'conversacion_dia')], 2))
    return svg(1440, 420, inner, 'Esquema de un tablero de tres páginas, cada una con tres elementos y la tabla Gold que los alimenta')


def connector():
    tablas = [('tema_dia', '12 KB'), ('hashtags_dia', '457 KB'), ('autores_alcance', '0.3 KB'), ('aplicaciones_dia', '3 KB'), ('actividad_hora', '23 KB'), ('conversacion_dia', '1.4 KB')]
    t = ''.join(f'<text class="mono" style="font-size:20px" x="1112" y="{140 + i * 40}">{a}</text><text class="sm" x="1418" y="{140 + i * 40}" text-anchor="end" style="font-size:19px">{b}</text>' for i, (a, b) in enumerate(tablas))
    inner = ('<rect class="box focus" x="20" y="40" width="380" height="330"/><text class="lbl" x="44" y="90">Tablero</text><text class="sm" x="44" y="122">Data Studio (antes Looker Studio)</text>'
             '<text class="sm" x="44" y="226">Cada gráfica y cada tarjeta</text><text class="sm" x="44" y="254">es una consulta distinta.</text>'
             '<g data-step="1">' + arr(410, 140, 600, 140) + '<text class="sm" x="424" y="122">consulta SQL</text>' + arr(600, 260, 410, 260) + '<text class="sm" x="446" y="296">resultado</text>'
             '<rect class="box" x="610" y="40" width="400" height="330"/><text class="lbl" x="634" y="90">Conector BigQuery</text><text class="sm" x="634" y="122">una fuente de datos por tabla:</text><text class="sm" x="634" y="150">proyecto · dataset · tabla</text></g>'
             '<g data-step="2">' + arr(1020, 205, 1090, 205) + '<rect class="box focus" x="1090" y="40" width="340" height="330"/><text class="head" x="1120" y="86">TU DATASET tweets_gold</text>' + t + '</g>'
             '<g data-step="3"><text class="big hl" x="20" y="420">Roles: BigQuery Data Viewer (leer) y BigQuery Job User (consultar).</text></g>')
    return svg(1440, 450, inner, 'Tablero de Data Studio que envía consultas al conector de BigQuery, que lee seis tablas Gold pequeñas')


def cost_bars():
    gb = V['tablas']['tweets_bronze.entrada']['escaneo_completo_facturable_bytes'] / 1e9
    sel = V['bytes_consulta_silver']['select_star'] / 1e9
    txt = V['bytes_consulta_silver']['solo_texto_un_dia'] / 1e9
    gold = 10485760 / 1e9
    rows = [('Bronze completo', gb, 'alert'), ('Silver · SELECT *', sel, 'ctx'), ('Silver · texto de un día', txt, 'ctx'), ('Gold · cualquier tabla', gold, 'hl')]
    inner = ('<text class="head" x="40" y="30">BYTES FACTURADOS POR UNA CONSULTA (GB)</text>'
             + hbars(40, 56, 360, 700, rows, gb, rowh=70, barh=46, fmt=lambda v: f'{v:.2f}' if v >= 0.1 else f'{v:.3f}')
             + f'<g data-step="1"><text class="big hl" x="40" y="400">Gold cuesta {gb * 1e9 / 10485760:,.0f} veces menos que Bronze.</text></g>'
             + '<g data-step="2"><text class="sm" x="40" y="434">Cada gráfica envía su propia consulta: apunta el tablero a la tabla más pequeña que responda.</text></g>')
    return svg(1440, 460, inner, 'Barras de bytes facturados por consulta: Bronze completo, Silver, Silver de un día y una tabla Gold')


def audit():
    claims = [
        ('«Los autores con más de 1 millón de seguidores escriben menos del 1 % de los tweets y reciben casi 18 % de los likes.»', 'Sustentada',
         'autores_alcance: 0.84 % de los tweets y 17.66 % de los likes en el segmento de más de 1 millón de seguidores (1,375 autores). Es lo que dice la tabla; no dice que esos autores «influyan» en nadie.'),
        ('«#nato fue tendencia el 24 de marzo por la cumbre de ese día.»', 'Sin respaldo',
         'hashtags_dia: #nato tiene su máximo el 24 de marzo (4,431 tweets, 0.76 % del día). La tabla muestra el pico, no la causa: el archivo no trae motivos ni eventos.'),
        ('«El 16 de marzo casi no se habló de energía (2,169 tweets).»', 'Contradicha',
         'El 16 es un día parcial: solo existen las horas 20 a 23 UTC y 134,871 tweets en total. En porcentaje, energía pesa 1.61 % ese día, igual que los días siguientes (1.57–1.89 %).')]
    btns = ''.join(f'<button type="button" data-claim="{i}">{c[0]}</button>' for i, c in enumerate(claims))
    ver = ''.join(f'<div class="verdict" data-verdict="{i}" hidden><span class="v v-{["ok", "no", "bad"][i]}">{c[1]}</span><p>{c[2]}</p></div>' for i, c in enumerate(claims))
    return (f'<div class="demo audit" data-demo="auditoria"><p class="sm">Elige una afirmación y decide antes de ver el veredicto.</p><div class="claims">{btns}</div>'
            '<div class="chips"><span class="v v-ok">SUSTENTADA</span><span class="v v-no">SIN RESPALDO</span><span class="v v-bad">CONTRADICHA</span></div>' + ver + '</div>')


# ---------- slides ----------
SL = []


def add(title, body, note, layout='plain', phase='Comprender · 15–50 min', src=DATA):
    SL.append(slide(title, body, note, layout, phase, src))


# =====================================================================
# ABRIR 0–15
# =====================================================================
add('Un tablero decide antes de que alguien lo lea.',
    '<div><p class="overline">Visualización ejecutiva · Data Studio sobre BigQuery</p><h1>Un tablero decide<br>antes de que alguien<br>lo lea.</h1>'
    '<p class="lede">Seis tablas Gold, una historia.<br>Un tablero que informa y otro que engaña.</p></div>'
    f'<div class="stack"><p class="large signal">{d1(EN[i23])} %</p><p>de los tweets del 23 de marzo de 2022 hablaban de energía</p>'
    f'<p class="caption">frente a {d1(min(ANT))}–{d1(max(ANT))} % los siete días anteriores<br>Hoy aprendes a mostrarlo sin exagerar.</p></div>',
    '0–3 min. Abrir con una pregunta: si te muestran un tablero con una línea que sube, ¿qué necesitas ver para creerlo? [pausa 3 s] Recoge dos respuestas (la base, el periodo, el idioma). Hoy el dato son las seis tablas Gold que construiste en la sesión anterior; el trabajo es de diseño y de criterio, no de SQL nuevo.',
    'cover dark', 'Abrir · 0–15 min', CURSO)

add('El mismo dato cuenta dos historias según cómo lo midas.', two_stories(),
    f'3–8 min. Muestra solo las dos gráficas y pide que cada persona escriba qué le pasó a alimentos entre el 17 y el 25 de marzo. [pausa 3 s] Al clic aparecen los números. En conteo, alimentos pasó de {n(ALIR[1])} a {n(ALIR[K25])} tweets ({ali_raw_chg:+.0f} %): parece que no cambió. Como porcentaje del día pasó de {d2(ALI[1])} % a {d2(ALI[K25])} % ({ali_pct_chg:+.0f} %): su peso en la conversación sube casi la mitad. Las dos gráficas son correctas; responden preguntas distintas. La medida decide la historia, por eso Gold guarda el porcentaje y su base.',
    'vz-two', 'Abrir · 0–15 min')

add('La pregunta del comité decide el tablero, no al revés.',
    flow([('Pregunta', '¿Qué temas vigilar?'), ('Medida', '% de los tweets del día'),
          ('Gráfico', 'Línea por día, eje desde 0'), ('Título', f'Energía pasó de {d1(min(ANT))}–{d1(max(ANT))} % a {d1(EN[i23])} %'),
          ('Acción', 'Leer los tweets del 23 y contrastar')])
    + p('Primero decide qué harías con la respuesta. Después elige el gráfico que la hace visible.', 'callout'),
    '8–11 min. Recorre la cadena de izquierda a derecha, un clic por eslabón. La medida (porcentaje del día) viene de Gold: el tablero no puede inventar una base que Gold no calculó. El título se escribe al final, con el número que el gráfico muestra. Pregunta al grupo: ¿qué acción cambiaría si el 23 de marzo hubiera sido 2.0 % en vez de 3.1 %? Si ninguna, el tablero no responde a una decisión.',
    'path', 'Abrir · 0–15 min', SDS)

SEIS = [['tema_dia', '¿Cómo cambia un tema?', 'Línea, % del día', f'Energía: {d1(min(ANT))}–{d1(max(ANT))} % → {d1(EN[i23])} % el 23'],
        ['hashtags_dia', '¿De qué se habla?', 'Barras ordenadas', '#ukraine en 8.71 % de los tweets del 23'],
        ['autores_alcance', '¿Quién concentra la atención?', 'Barras comparadas', '0.84 % de tweets, 17.66 % de likes'],
        ['aplicaciones_dia', '¿Desde dónde se publica?', 'Barras ordenadas', f'3 apps = {100 * TRES_APPS / APP23_TOT:.0f} % de los tweets'],
        ['actividad_hora', '¿Cuándo se publica?', 'Línea por hora', 'Máximo en inglés 18 UTC; español 14'],
        ['conversacion_dia', '¿Cómo conversa la gente?', 'Barras apiladas 100 %', f'Respuestas: {PCT_TW["respuesta"]:.0f} % tweets, {PCT_LK["respuesta"]:.0f} % likes']]
add('Seis tablas Gold, seis preguntas, seis gráficos.',
    table(['Tabla Gold', 'Pregunta que responde', 'Gráfico adecuado', 'Qué verás'], SEIS),
    '11–15 min. Esta tabla es el mapa de la sesión: cada tabla Gold que construiste responde una pregunta distinta y, por eso, pide un gráfico distinto. Recórrela fila por fila sin explicar aún los gráficos; cada uno se explica en el bloque siguiente. Los números de la última columna salen de las tablas; los comprobarás tú con SQL en el laboratorio. Hoy construyes un tablero de tres páginas con datos de las seis.',
    'choices', 'Abrir · 0–15 min', GOLD6)

# =====================================================================
# COMPRENDER 15–50
# =====================================================================
r23 = [r for r in ROWS if r['fecha'] == D23 and (r['tema'] == 'energia' or (r['tema'] == 'sanciones' and r['grupo_idioma'] == 'en'))]
r23.sort(key=lambda r: (r['tema'], GRUPOS.index(r['grupo_idioma'])))
add('Un tablero solo puede mostrar lo que Gold ya definió.',
    '<div class="tags"><span class="tag dim">DIMENSIONES · el grano: fecha, tema, grupo_idioma</span><span class="tag med">MEDIDAS · tweets_tema, likes_tema</span><span class="tag den" data-step="1">BASE · tweets_dia → pct_del_dia</span></div>'
    + panel("SELECT fecha, tema, grupo_idioma, tweets_tema, tweets_dia, pct_del_dia\nFROM tweets_gold.tema_dia\nWHERE fecha = '2022-03-23'",
            ['fecha', 'tema', 'grupo_idioma', 'tweets_tema', 'tweets_dia', 'pct_del_dia'],
            [[r['fecha'], r['tema'], r['grupo_idioma'], n(int(r['tweets_tema'])), n(int(r['tweets_dia'])), r['pct_del_dia']] for r in r23],
            'Procesados: 10 MiB facturables (mínimo por tabla) · tabla de 216 filas · fragmento del resultado')
    + step(2, p('Lo que no está en la tabla, el tablero no lo puede mostrar: ni hora, ni usuario, ni texto. Para eso hay otras tablas Gold.', 'callout')),
    '15–18 min. Esta es la tabla que alimenta el panorama: 216 filas = 12 días × 6 temas × 3 grupos de idioma. Dimensiones dicen por qué cortamos; medidas, qué contamos; la base permite comparar días con volúmenes distintos. Lo que el tablero no puede mostrar no se arregla en el tablero: se arregla en Gold. Las otras cinco tablas existen justamente porque responden otras preguntas.',
    'result', 'Comprender · 15–50 min', GOLD6)

add('La pregunta elige el gráfico.', chart_chooser(),
    '18–21 min. Un clic por cuadro. Línea para tiempo continuo; barras (desde cero) para comparar categorías; tabla cuando se consultan valores exactos; tarjeta cuando una cifra importa más que su forma. Evita pastel y dona: el ojo compara mal los ángulos. Cada una de las seis tablas Gold sugiere uno de estos cuatro; lo veremos con datos reales.',
    'chooser', 'Comprender · 15–50 min', SDS)

a_, b_ = EN[i20], EN[i23]
add('Un eje cortado convierte 2× en 10×.', axis_cut(),
    f'21–24 min. Mismos dos valores: energía el 20 de marzo ({d2(a_)} %) y el 23 ({d2(b_)} %), una razón de ×{b_ / a_:.2f}. Con el eje cortado en 1.4 la segunda barra se ve ×{(b_ - 1.4) / (a_ - 1.4):.1f} más alta. Las barras codifican el valor con su longitud, así que deben partir de cero. En una línea sí puedes acotar el eje, pero dilo en la etiqueta.',
    'bars', 'Comprender · 15–50 min', SDS)

add('Un color de énfasis; todo lo demás, contexto.', emphasis(),
    '24–27 min. Izquierda: cada serie con su color y una leyenda que obliga a ir y venir con la vista. Derecha: las series de contexto en gris con la etiqueta pegada a la línea y un solo acento en la serie que importa. Pregunta: ¿adónde miras primero en cada lado? Es el principio de Knaflic: el color es una instrucción de atención, no decoración.',
    'emphasis', 'Comprender · 15–50 min', SDS)

add('El título dice la conclusión, no el contenido del gráfico.', titles(),
    f'27–30 min. Tres títulos para la misma gráfica. El primero describe, el segundo promete sin medir, el tercero lleva hecho (de {d1(min(ANT))}–{d1(max(ANT))} % a {d1(EN[i23])} %), comparación (los siete días anteriores) y límite (el dato no explica por qué). El título es lo que el comité recuerda; si el gráfico lo contradice, el comité cree al título.',
    'titles', 'Comprender · 15–50 min', SDS)

add('Los hashtags dicen de qué se habla; no por qué.', hashtags_slide(),
    '30–33 min. Tabla hashtags_dia: solo incluye hashtags con al menos 25 tweets ese día. Izquierda, el 23 de marzo: #ukraine aparece en 8.71 % de los tweets (49,393); #putin en 2.52 %, #russia en 2.35 %. Barras horizontales ordenadas, desde cero, con el valor al final. Clic: dos hashtags, #standwithukraine y #nato, tienen su máximo el 24 de marzo (4,999 y 4,431 tweets). Clic: el dato no dice por qué. No escribas «por la cumbre» ni «por el discurso»: el archivo contiene tweets, no eventos.',
    'hashtags', 'Comprender · 15–50 min', 'tweets_gold.hashtags_dia · 16–27 mar 2022 · uso académico')

add('Los autores grandes concentran los likes.', alcance_slide(),
    '33–36 min. Tabla autores_alcance: cinco segmentos por seguidores del autor. Barras agrupadas con el mismo eje para poder comparar dos medidas del mismo segmento. Los autores con menos de 1 mil seguidores escriben 67.02 % de los tweets y reciben 8.72 % de los likes. Clic: el segmento de 100 mil a 1 millón escribe 2.15 % y recibe 35.93 %. Clic: los 1,375 autores de más de 1 millón escriben 0.84 % y reciben 17.66 %. Cuidado con la lectura: es concentración de likes, no influencia ni persuasión.',
    'reach', 'Comprender · 15–50 min', 'tweets_gold.autores_alcance · 16–27 mar 2022 · uso académico')

add('El idioma cambia el ritmo del día.', hora_slide(),
    '36–39 min. Tabla actividad_hora: tweets por hora UTC y grupo de idioma. Tres líneas del 23 de marzo con la etiqueta pegada al máximo. Clic: inglés 18,476 a las 18 UTC; español 5,679 a las 14; otros idiomas 9,769 a las 14. Esa hora es UTC, no la hora local de quien escribe: los otros idiomas suben desde las 6 UTC por la mañana europea. Clic: el 16 de marzo solo tiene las horas 20 a 23 UTC, así que un tablero por hora que lo incluya parece que el día empezó tarde.',
    'hours', 'Comprender · 15–50 min', 'tweets_gold.actividad_hora · 16–27 mar 2022 · uso académico')

add('Las respuestas son la mitad de los tweets y reúnen 15 % de los likes.', conversacion_slide(),
    f'39–42 min. Tabla conversacion_dia: cada tweet es original, respuesta o cita. Dos barras apiladas al 100 %: partes de un todo. Tweets: originales {PCT_TW["original"]:.1f} %, respuestas {PCT_TW["respuesta"]:.1f} %, citas {PCT_TW["cita"]:.1f} %. Clic: likes: originales {PCT_LK["original"]:.1f} %, respuestas {PCT_LK["respuesta"]:.1f} %, citas {PCT_LK["cita"]:.1f} %. Clic: la mediana de likes es 0 en los tres tipos el 27 de marzo, así que decir «promedio de likes por tweet» mezcla un puñado de tweets enormes con millones de ceros.',
    'thread', 'Comprender · 15–50 min', 'tweets_gold.conversacion_dia · 16–27 mar 2022 · uso académico')

add('El 16 de marzo no es el inicio del tema: es medio día.', partial_day(),
    f'42–44 min. Izquierda: tweets por día, con barras desde cero; el 16 de marzo tiene {n(DIA[FECHAS[0]])}, un {100 * DIA[FECHAS[0]] / DIA[FECHAS[1]]:.0f} % del 17. El archivo empieza esa tarde. Derecha: energía del 16 al 17 en conteo se ve multiplicada por {RAWL["energia"][1] / RAWL["energia"][0]:.1f}; en porcentaje del día casi no cambia. Un tablero debe marcar el día parcial o excluirlo, y decirlo.',
    'partial', 'Comprender · 15–50 min')

s_en = 100 * LP['sanciones']['en'][0] / LP['sanciones']['en'][1]; s_es = 100 * LP['sanciones']['es'][0] / LP['sanciones']['es'][1]
add('Mezclar idiomas diluye o infla el tema.', languages(),
    f'44–47 min. El mismo tema se ve distinto según el idioma: sanciones pesa {s_en:.2f} % en inglés, {s_es:.2f} % en español y {100 * LP["sanciones"]["otro"][0] / LP["sanciones"]["otro"][1]:.2f} % en el resto. El grupo «otros» agrupa un cuarto de todos los tweets: mezclarlos diluye el tema. Un filtro de idioma no es un adorno: define de qué población habla el título.',
    'languages', 'Comprender · 15–50 min')

add('Una palabra clave no es un tema: «mercados» lo llena la inflación.', keyword(),
    '47–50 min. Hallazgo real: el tema «mercados» en español se compone de 28,280 tweets con «inflación», 9,161 con «precios», solo 1,121 con «mercados» y 746 con «bolsa» (un tweet puede contar más de una vez). El 18 de marzo hay 11,917 tweets en español con «inflación»; muchos son «guerra contra la inflación», no Ucrania. Un tablero que muestre «mercados» como tema debe decir que es una lista de palabras, no una clasificación verificada.',
    'keyword', 'Comprender · 15–50 min', 'Consultas SQL sobre tweets_silver y tweets_gold · textos citados del dato, uso académico')

# =====================================================================
# APLICAR 50–70
# =====================================================================
add('Un tablero puede engañar con datos correctos.', board_bad(),
    '50–53 min. Este tablero no tiene un solo número falso: todos vienen de tema_dia. Aun así tiene tres defectos. 1) El 16 de marzo es un día parcial: cualquier línea de conteo arranca baja y parece una subida. 2) Conteo sin base: las seis series siguen al volumen del día, no al peso del tema. 3) Idiomas mezclados sin aviso: el inglés pesa 59 %. Pide que encuentren un cuarto defecto: título descriptivo y seis colores.',
    'bad-board', 'Aplicar · 50–70 min')

add('Un filtro útil cambia el título y dice qué cubre.', filter_demo(),
    '53–57 min. Cambia tema e idioma y lee en voz alta el título, que cambia con el filtro: porcentaje del periodo, tweets del tema y base. Sin filtro de idioma el tablero cubre todo; con «es» la base baja a 1,056,425. Energía el 23 de marzo sube en los tres grupos. Un título fijo con un filtro variable deja de ser cierto en cuanto el lector toca el control.',
    'filter', 'Aplicar · 50–70 min')

add('Un tablero de tres páginas: panorama, dentro del tema, quién y cuándo.', dashboard_layout(),
    '57–60 min. Esquema del tablero del laboratorio. Página 1: la pregunta de negocio, la serie del tema, tres tarjetas con su base, filtro de idioma y la nota del día parcial. Página 2: de qué se habla (hashtags) y desde dónde (aplicaciones), con el filtro de fecha puesto dentro de cada gráfica (son dos fuentes distintas). Página 3: quién (alcance del autor), cuándo (hora UTC) y cómo (originales, respuestas y citas). Cada página responde una pregunta y cada elemento sale de una tabla Gold distinta. Recuerda la lectura en Z: título arriba, cifras, serie, límites abajo.',
    'z', 'Aplicar · 50–70 min', SDS)

add('El tablero no guarda los datos: cada gráfica es una consulta a BigQuery.', connector(),
    '60–63 min. Un tablero de Data Studio no contiene los datos: cada gráfica o tarjeta pide los suyos a BigQuery a través del conector (proyecto, dataset y tabla, o una consulta personalizada). Seis tablas Gold son seis fuentes de datos. Para que el tablero funcione necesitas leer el dataset y poder lanzar consultas en el proyecto que factura. Las credenciales de la fuente deciden quién ve los datos: del propietario (predeterminado), del lector o de una cuenta de servicio.',
    'connector', 'Aplicar · 50–70 min', CONN)

add('Conecta el tablero a Gold: cada gráfica lee kilobytes, no gigabytes.', cost_bars(),
    '63–66 min. Números de referencia del curso: leer Bronze completo cuesta 23.67 GB facturables; SELECT * de Silver, 2.45 GB; el texto de un solo día en Silver, 0.11 GB por la partición por fecha; y una consulta sobre cualquiera de las tablas Gold, el mínimo de 10 MiB. Cada gráfica del tablero es una consulta, y abrir una página puede lanzar varias. Con un tablero que apunte a Silver, abrirlo cuesta cientos de MiB cada vez.',
    'cost', 'Aplicar · 50–70 min', COSTS)

add('Audita tres afirmaciones contra las tablas.', audit(),
    '66–70 min. Auditoría breve con las tablas a la vista. Decide antes de pulsar: sustentada, sin respaldo o contradicha. 1) Segmento de más de 1 millón: 0.84 % de los tweets y 17.66 % de los likes: sustentada, sin hablar de influencia. 2) #nato por la cumbre: la tabla muestra el pico del 24 de marzo, no la causa: sin respaldo. 3) «Casi no se habló de energía el 16»: es medio día; en porcentaje pesa lo mismo: contradicha.',
    'audit', 'Aplicar · 50–70 min', GOLD6)

# =====================================================================
# PAUSA
# =====================================================================
add('Vuelve con Data Studio y BigQuery abiertos.',
    '<p class="time">10 min</p><p>Al volver: Data Studio y BigQuery Studio en dos pestañas, y la guía del laboratorio abierta.</p>',
    '70–80 min. Pausa real. Al volver comprueba que tienes tus seis tablas Gold en tu proyecto, los permisos de lectura y de consulta sobre ellas, y el presupuesto con alerta que configuraste en la primera sesión. Si falta una tabla, vuelve al laboratorio de la sesión anterior antes de seguir.',
    'statement dark', 'Pausa · 70–80 min', CURSO)

# =====================================================================
# LABORATORIO 80–150
# =====================================================================
QH = ['Comprobar tus tablas y conectar tema_dia', 'Página 1: panorama de energía', 'Página 2: hashtags y aplicaciones', 'Página 3: alcance, hora y conversación', 'Revisar con siete preguntas', 'Compartir y medir el costo']
OKS = ['Siete tablas listadas; 216 registros en tema_dia', '3.10 % el 23 de marzo; 137,598 · 6,798,932 · 2.02 %', '#ukraine 49,393 tweets (8.71 %) el 23', '0.84 % de tweets y 17.66 % de likes', 'Títulos con hecho y límite en las tres páginas', 'Cada gráfica factura 10.0 MiB y lee Gold']
LABROWS = [[str(s['n']), f'{s["minutes"]}', QH[i], OKS[i]] for i, s in enumerate(LAB)]
add('Laboratorio: un tablero de tres páginas.',
    '<div class="check-grid">' + ''.join(f'<div class="check-item"><b>{s["n"]} · {s["minutes"]} min · {QH[i]}</b><span>{OKS[i]}</span></div>' for i, s in enumerate(LAB)) + '</div>' + lablink(1),
    '80–150 min. Los seis pasos están en la guía, con el código completo, la salida esperada y el error frecuente de cada uno. Primero verificas tus tablas y las conectas; luego construyes una página por paso (panorama; dentro del tema; quién, cuándo y cómo); después revisas el tablero con la lista de siete preguntas, y al final lo compartes y compruebas cuánto cuesta. La interfaz de Data Studio no se ensayó desde la preparación de esta guía: los nombres de menús pueden variar; las comprobaciones numéricas con SQL son las que mandan.',
    'lab-code', 'Laboratorio · 80–150 min', CONN)

# =====================================================================
# CERRAR 150–180
# =====================================================================
add('Tres ejercicios para practicar solo.',
    '<div class="three">'
    '<div class="stack"><p class="caption">1 · TÍTULO</p><p>Escribe un título para: 1,375 autores de más de 1 millón de seguidores, 0.84 % de los tweets, 17.66 % de los likes.</p>'
    + step(1, '<p class="callout">«Menos de 1 % de los tweets, casi 18 % de los likes; la tabla no dice por qué»</p>') + '</div>'
    '<div class="stack"><p class="caption">2 · GRÁFICO</p><p>Quieres mostrar cómo se reparte una semana entre respuestas, originales y citas. ¿Qué gráfico eliges?</p>'
    + step(2, '<p class="callout">Barras apiladas al 100 %: partes de un todo</p>') + '</div>'
    '<div class="stack"><p class="caption">3 · TRAMPA</p><p>Alguien grafica tweets por hora del 16 de marzo y dice «ese día empezó a las 20». ¿Qué le respondes?</p>'
    + step(3, '<p class="callout">Es un día parcial: solo hay horas 20 a 23 UTC</p>') + '</div>'
    '</div>',
    '150–165 min. Práctica individual. Resuelve cada ejercicio en papel antes de pulsar la pista (un clic por pista). El ejercicio 1 practica título con hecho y límite; el 2, la elección del gráfico para partes de un todo; el 3, la trampa del día parcial. Si te sobra tiempo, repite el ejercicio 1 con otro segmento de autores_alcance y escribe qué cambia en el título.',
    'practice', 'Cerrar · 150–180 min', GOLD6)

add('Qué puedes afirmar con este tablero y qué no.',
    '<div class="two"><div class="sheet"><p class="caption">PUEDES AFIRMAR</p><ul class="yn">'
    f'<li>Energía fue {d1(min(ANT))}–{d1(max(ANT))} % de los tweets del 16 al 22 de marzo y {d1(EN[i23])} % el 23, en los tres grupos de idioma.</li>'
    '<li>El 0.84 % de los tweets, de autores con más de 1 millón de seguidores, reúne el 17.66 % de los likes.</li>'
    f'<li>Las respuestas son {PCT_TW["respuesta"]:.0f} % de los tweets y {PCT_LK["respuesta"]:.0f} % de los likes.</li>'
    '<li>El inglés llega a su máximo a las 18 UTC y el español a las 14 UTC.</li></ul></div>'
    '<div class="stack"><p class="caption">NO PUEDES AFIRMAR</p><ul class="yn no">'
    '<li>Que la guerra causó el aumento, ni que #nato subió por un evento.</li><li>Que los tweets miden opinión pública ni influencia.</li>'
    '<li>Que la hora UTC es la hora local de quien escribió.</li><li>Que el 16 de marzo fue un día tranquilo.</li><li>Que otro periodo se comporte igual.</li></ul></div></div>',
    '165–175 min. Cierre con lo que sostiene el tablero y lo que no. Cada afirmación de la izquierda tiene evidencia en una tabla Gold; cada una de la derecha, una razón por la que el dato no alcanza: causa, representatividad, hora local, día parcial, un solo periodo. Pide que cada persona escriba una afirmación más de cada lado con sus propias palabras.',
    'limits', 'Cerrar · 150–180 min', GOLD6)

add('Siguiente: ¿puede un modelo leer estas tablas sin inventar?',
    '<p class="huge">S7</p><p>Las mismas tablas Gold, ahora como contexto para un modelo de lenguaje. La habilidad es la que usaste hoy: auditar afirmaciones contra la evidencia.</p><p class="caption">Ten a mano tus seis tablas y el título de tu tablero.</p>',
    '175–180 min. Puente a la sesión 7. Los títulos y cifras del tablero serán la evidencia contra la que se audite un texto generado. Cierra pidiendo una pregunta que el tablero no puede responder y que un modelo tampoco debería responder sin evidencia.',
    'statement dark', 'Cerrar · 150–180 min', CURSO)

SLIDES = SL
