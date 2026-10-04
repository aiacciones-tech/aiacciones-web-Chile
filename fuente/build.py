import os, re, json

S = "/tmp/claude-0/-home-claude/51bbcb85-f720-5650-9a37-2f75843c73b7/scratchpad/site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)

def n(v, d=1, suf=""):
    if v is None: return "n/a"
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + suf

def pct(v, d=1, sign=True):
    if v is None: return "n/a"
    return ("+" if (sign and v > 0) else "") + n(v, d, "%")

YT = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-4.8.5-4.8s0-3.2-.5-4.8ZM9.6 15.1V8.9l5.8 3.1-5.8 3.1Z"/></svg>'
XI = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M18.9 2H22l-6.8 7.8L23.2 22h-6.3l-4.9-6.4L6.4 22H3.3l7.3-8.3L1 2h6.4l4.4 5.8L18.9 2Zm-1.1 18h1.7L6.3 3.9H4.5L17.8 20Z"/></svg>'
CH = "https://www.youtube.com/channel/UCDGmimmfYaYYP1jYBo6bA3g"
NOTE = '<p class="note">Cifras de nuestro video de resultados 2T 2026 (estados financieros y análisis razonado en CMF / Bolsa de Santiago). P/BV, ROE y variación 12 meses: StockAnalysis, septiembre 2026.</p>'

# ---------------------------------------------------------------- datos
NEW = [
 dict(id="falabella", t="FALABELLA", n="Falabella", s="Retail, banca y centros comerciales", px="$6.299", chg=12,
  pe=11.9, fpe=16.4, pbv=1.5, ev=10.7, dy=2.5, roe=19.0, epsg=-16.5, vid="AOdMbPxaeUI", q="Falabella",
  lede="Grupo de retail con tiendas por departamento (Falabella Retail), mejoramiento del hogar (Sodimac), supermercados (Tottus), Banco Falabella y centros comerciales (Mallplaza), en Chile, Perú y Colombia. La utilidad reportada incluye la revalorización de propiedades de inversión (fair value), que puede mover mucho el resultado de un trimestre a otro.",
  vtitle="Falabella: utilidad 31% sobre el consenso gracias al banco (2T 2026)",
  cap="Cifras en CLP miles de millones salvo BPA · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",3178.0,3486.5,1),("EBITDA",472.9,506.0,1),("Utilidad controladora",364.3,304.3,1),("Utilidad sin fair value",196.9,223.6,1),
        ("BPA (CLP por acción)",145.2,121.3,1),("Flujo de caja libre",116.6,237.3,1)],
  derived=("Margen EBITDA","14,9%","14,5%"),
  kpi="Deuda neta no bancaria / EBITDA: <b>1,29x</b> (1,94x un año antes). BPA de $121,3 vs. $92,35 esperado por el consenso.",
  tiles=[("P/E","11,9x"),("P/E sin fair value","17,9x"),("Forward P/E","16,4x"),("EV/EBITDA","10,7x"),("FCF yield","8,2%"),("Dividend Yield","2,5%")],
  small="P/BV <b>1,5x</b> · ROE <b>19,0%</b> · Precio objetivo consenso <b>$6.784</b> (+7,7%).",
  mirar=["Banco Falabella: colocaciones +18% y EBITDA +36%, hoy el motor del grupo.","Sodimac y Falabella Retail en Chile, que siguen débiles.","Costo de riesgo en Chile (+23,5%) si la economía se enfría.","Cuánto de la utilidad viene de revalorizaciones (fair value) y no del negocio."]),
 dict(id="ripley", t="RIPLEY", n="Ripley Corp", s="Retail y banca (Chile y Perú)", px="$455", chg=-11,
  pe=7.2, fpe=9.3, pbv=0.7, ev=7.1, dy=2.9, roe=10.9, epsg=58.7, vid="bbKGplfrAQw", q="Ripley",
  lede="Tiendas por departamento, Banco Ripley y centros comerciales en Chile y Perú (Mall Aventura). Perú ya aporta cerca de dos tercios del EBITDA por segmento, mientras el retail en Chile casi no genera EBITDA.",
  vtitle="Ripley: utilidad +60%, pero el EBITDA cae 10% (2T 2026)",
  cap="Cifras en CLP miles de millones salvo BPA · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",533.2,564.1,1),("EBITDA",49.0,43.9,1),("Utilidad neta",15.7,25.1,1),("BPA (CLP por acción)",8.16,12.95,2)],
  derived=("Margen EBITDA","9,2%","7,8%"),
  kpi="Deuda neta no bancaria / EBITDA ajustado: <b>4,28x</b> (4,97x un año antes). La utilidad incluye +16 mil MM por revalorización de Mall Aventura.",
  tiles=[("P/E","7,2x"),("Forward P/E","9,3x"),("P/BV","0,74x"),("EV/EBITDA no bancario","7,1x"),("FCF yield","7,8%"),("Dividend Yield","2,9%")],
  small="ROE <b>10,9%</b> · EV/EBITDA con deuda bancaria (StockAnalysis) <b>14,8x</b> · Precio objetivo <b>$469</b> (+3%).",
  mirar=["Retail Chile: ventas mismas tiendas −7,3% y EBITDA casi en cero.","Costo de riesgo de Banco Ripley Chile (11,4% vs. 7,7%).","Perú: retail +13,6%, banco con EBITDA +40% y ampliación de Mall Aventura.","Cuánto de la utilidad viene de revalorizaciones y no del EBITDA."]),
 dict(id="cencosud", t="CENCOSUD", n="Cencosud", s="Supermercados y retail", px="$1.949", chg=-26,
  pe=34.3, fpe=12.7, pbv=1.0, ev=8.2, dy=1.4, roe=4.6, epsg=-142.2, vid="WJ2OGQfcN4w", q="Cencosud",
  lede="Supermercados (Jumbo, Santa Isabel), tiendas por departamento (Paris), mejoramiento del hogar (Easy), centros comerciales y servicios financieros en Chile, Argentina, Brasil, Perú, Colombia y EE.UU. (The Fresh Market). Las cifras se reportan con NIC 29, la norma de hiperinflación que se aplica a Argentina.",
  vtitle="Cencosud: pérdida y EBITDA −16%, peor de lo esperado (2T 2026)",
  cap="Cifras en CLP miles de millones salvo BPA · 2T 2026 vs. 2T 2025 · reportadas con NIC 29",
  rows=[("Ingresos",4171.3,4094.7,1),("EBITDA ajustado",365.8,307.9,1),("Utilidad controladores",86.5,-36.5,1),("BPA (CLP por acción)",30.8,-13.0,1),
        ("Flujo de caja libre (semestre)",-24.8,193.7,1)],
  derived=("Margen EBITDA","8,8%","7,5%"),
  kpi="Deuda neta con arriendos / EBITDA: <b>3,6x</b> (3,1x en dic-2025; meta 3,0x). BPA sin NIC 29 de $1,1 vs. $35,6 esperado por el consenso.",
  tiles=[("P/E","34,3x"),("Forward P/E","12,7x"),("P/BV","1,0x"),("EV/EBITDA","8,2x"),("FCF yield","7,1%"),("Dividend Yield","1,4%")],
  small="ROE <b>4,6%</b> · Guía 2026: ingresos +3,0% y EBITDA +13,6% · Precio objetivo <b>$2.710</b> (13 analistas).",
  mirar=["Guerra de promociones en supermercados Chile (margen EBITDA 10,5% vs. 12,7%).","Deuda neta de 3,6x EBITDA, buena parte en UF.","Si alcanza la guía 2026, que exige un EBITDA +42% en el segundo semestre.","Integración de Makro (Colombia) y St. Marché (Brasil)."]),
 dict(id="sk", t="SK", n="Sigdo Koppers", s="Holding industrial (explosivos y minería)", px="$1.587", chg=30,
  pe=13.3, fpe=None, pbv=0.8, ev=6.1, dy=3.1, roe=10.1, epsg=47.8, vid="nHtqz3rSruc", q="Sigdo Koppers",
  lede="Holding industrial con Enaex (explosivos y nitrato de amonio, 57% de los ingresos), Magotteaux (bolas de molienda para minería), SKIC (construcción industrial), SK Comercial (arriendo de maquinaria) y Puerto Ventanas. Reporta en dólares.",
  vtitle="Sigdo Koppers: utilidad +48% impulsada por Enaex (2T 2026)",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",1013.6,1177.4,1),("EBITDA",135.0,148.7,1),("Utilidad controladores",22.3,33.0,1),("EPS (US$ por acción)",0.021,0.031,3)],
  derived=("Margen EBITDA","13,3%","12,6%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>2,0x</b>. Flujo de caja libre del semestre US$71,9 MM (−52%) por capital de trabajo.",
  tiles=[("P/E","13,3x"),("P/BV","0,8x"),("EV/EBITDA","6,1x"),("FCF yield","8,2%"),("Dividend Yield","3,1%"),("ROE","10,1%")],
  small="Precio objetivo <b>$1.830</b> (+15%, un analista). No hay consenso trimestral publicado.",
  mirar=["Enaex: volumen récord (+11,4%) y precio del amoníaco.","Recuperación del flujo operacional, que cayó 36% en el semestre.","SK Comercial, con arriendo débil en Colombia y Perú.","Ritmo de los proyectos mineros en Chile y Perú."]),
 dict(id="vapores", t="VAPORES", n="CSAV (Vapores)", s="Holding naviero (30% de Hapag-Lloyd)", px="$50,3", chg=-7,
  pe=None, fpe=17.0, pbv=0.4, ev=None, dy=24.0, roe=-0.7, epsg=None, vid="PmgeNjbtPAg", q="Vapores",
  lede="Compañía Sud Americana de Vapores ya no opera barcos: su activo es el 30% de la naviera alemana Hapag-Lloyd, que representa 97,5% de sus activos. Su utilidad depende de las tarifas de contenedores. Reporta en dólares y no tiene deuda financiera.",
  vtitle="Vapores (CSAV): Hapag-Lloyd se recupera y sube su guía dos veces (2T 2026)",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos de Hapag-Lloyd (100%)",5271,5840,0),("Participación en Hapag-Lloyd",87.8,20.1,1),("Resultado antes de impuestos",136.0,20.0,1),
        ("Utilidad neta",-19.3,-49.8,1),("EPS (US$ por acción)",-0.0004,-0.0010,4)],
  derived=None,
  kpi="Sin deuda financiera. NAV ≈ $160 por acción: la acción transa con un descuento de <b>~69%</b> (promedio histórico ~65%).",
  tiles=[("P/E","n/a"),("Forward P/E","~17x"),("P/BV","0,41x"),("Descuento vs. NAV","~69%"),("Dividend Yield 12m","~24%"),("EV/EBITDA look-through","2,6x")],
  small="Guía EBITDA 2026 de Hapag-Lloyd subida a US$3.900–4.400 MM. Pérdida de US$132,6 MM en el primer semestre.",
  mirar=["Tarifas de contenedores y costos por la situación en Medio Oriente.","Guía de Hapag-Lloyd, subida dos veces en 2026.","Dividendos de 2027, que serán menores tras la pérdida del semestre.","Descuento sobre el valor de su participación en Hapag-Lloyd."]),
 dict(id="quinenco", t="QUINENCO", n="Quiñenco", s="Holding diversificado", px="$4.510", chg=14,
  pe=11.1, fpe=12.7, pbv=0.5, ev=None, dy=9.1, roe=9.3, epsg=0.0, vid="uoE3TWTdVqk", q="Quiñenco",
  lede="Holding con participaciones en Banco de Chile (vía LQIF), Enex (combustibles), CCU, CSAV, SM SAAM y Nexans. En un holding no se usan EV/EBITDA ni flujo de caja libre: se mira el descuento sobre el NAV (el valor de sus inversiones) y los dividendos.",
  vtitle="Quiñenco: utilidad plana, Enex compensa la pérdida de Vapores (2T 2026)",
  cap="Cifras en CLP miles de millones salvo BPA · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos negocios no bancarios",1336.8,1746.2,1),("Utilidad controladora",131.3,131.3,1),("BPA (CLP por acción)",78.94,78.96,2),
        ("Aporte Banco de Chile / LQIF",76.3,95.7,1),("Aporte Enex",6.6,53.4,1),("Aporte CSAV",-12.1,-29.7,1)],
  derived=None,
  kpi="NAV jun-2026 US$10.600 MM (~$6.184 por acción): descuento de <b>~27%</b> (rango histórico 8–30%).",
  tiles=[("P/E","11,1x"),("Forward P/E","12,7x"),("P/NAV","0,73x"),("Descuento vs. NAV","~27%"),("Dividend Yield","9,1%"),("ROE","9,3%")],
  small="P/BV <b>0,5x</b> · Precio objetivo promedio <b>$5.400</b>. Sin la venta de Nexans el P/E sería ~14x.",
  mirar=["CSAV y Hapag-Lloyd, que restaron $29,7 mil MM en el trimestre.","Enex, cuya ganancia depende del precio del crudo.","Utilidad de Banco de Chile, su principal aporte.","Uso de la caja del holding en nuevas inversiones."]),
]
ORDER_ALL_IDS = None

# ---------------------------------------------------------------- plantilla de ficha
tpl = rd("acciones/afpcapital/index.html")
head, rest = tpl.split('<main class="wrap">', 1)
_, foot = rest.split("</main>", 1)

def var(a, b):
    if a is None or b is None or a <= 0 or b <= 0: return None
    return (b / a - 1) * 100

VAROV = {('ripley','EBITDA'):-10.5,('ripley','Utilidad neta'):59.8,('falabella','Utilidad sin fair value'):13.5,('sk','EBITDA'):10.2,('sk','Utilidad controladores'):47.8}

def ficha(c):
    h = head.replace("<title>AFPCAPITAL · AI ACCIONES CHILE</title>", f"<title>{c['t']} · AI ACCIONES CHILE</title>")
    h = h.replace("Ficha de AFP Capital: resultados, valoración y claves.", f"Ficha de {c['n']}: resultados 2T 2026, valoración y claves.")
    cls = "up" if c["chg"] >= 0 else "down"
    tiles = "".join(f'<div class="tile"><span class="lbl">{a}</span><span class="val">{b}</span></div>' for a, b in c["tiles"])
    trs = ""
    for lbl, a, b, d in c["rows"]:
        v = VAROV.get((c['id'], lbl), var(a, b))
        vs = pct(v) if v is not None else ("n/a" if (a is None or b is None) else ("a pérdida" if b < 0 <= a else ("a ganancia" if a < 0 <= b else "n/a")))
        vcls = "neg" if (v is not None and v < 0) or vs == "a pérdida" else ""
        trs += f'<tr><th scope="row">{lbl}</th><td class="{"neg" if a < 0 else ""}">{n(a, d)}</td><td class="{"neg" if b < 0 else ""}">{n(b, d)}</td><td class="{vcls}">{vs}</td></tr>'
    if c["derived"]:
        trs += f'<tr class="derived"><th scope="row">{c["derived"][0]}</th><td>{c["derived"][1]}</td><td>{c["derived"][2]}</td><td></td></tr>'
    mirar = "".join(f"<li>{m}</li>" for m in c["mirar"])
    main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Acciones</a> / {c['t']}</nav>
<section class="page-head stock-head">
  <div>
    <p class="eyebrow">{c['s']}</p>
    <h1>{c['n']}</h1>
    <p class="lede">{c['lede']}</p>
  </div>
  <div class="quote">
    <span class="tk">{c['t']}</span>
    <span class="px">{c['px']}</span>
    <span class="{cls}">{"+" if c['chg'] > 0 else ""}{n(c['chg'], 0, "%")} en 12 meses</span>
    <span class="note">Precio de cierre usado en el video (sep-2026)</span>
  </div>
</section>
<section><h2 class="h-sec">Valoración</h2><div class="tiles">{tiles}</div>
<p class="small">{c['small']} ¿No conoces algún múltiplo? Revisa la sección <a href="../../educacion/index.html">Educación</a>.</p></section>
<section><h2 class="h-sec">Resultados del segundo trimestre 2026</h2><div class="table-scroll"><table class="data">
<caption>{c['cap']}</caption>
<thead><tr><th scope="col">Concepto</th><th>2T 2025</th><th>2T 2026</th><th>Var. a/a</th></tr></thead><tbody>{trs}</tbody></table></div>
<p class="kpi-line">{c['kpi']}</p>{NOTE}</section>
<section class="two">
  <div><h2 class="h-sec">Qué mirar</h2><ul class="checks">{mirar}</ul>{RETAIL_LINK if c['id'] in RETAIL_IDS else ""}</div>
  <div class="aside-box"><h2 class="h-sec">Videos</h2><div class="vids"><a class="vid" href="https://youtu.be/{c['vid']}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{c['vid']}/hqdefault.jpg" alt="" loading="lazy"><span>{c['vtitle']}</span></a></div>
<div class="vid-btns"><a class="btn" href="{CH}/search?query={c['q']}" target="_blank" rel="noopener">{YT} Videos de {c['t']} en YouTube</a><a class="btn ghost" href="https://x.com/aiacciones" target="_blank" rel="noopener">{XI} Ver en X</a></div><p class="small">Otras fichas: <span class="chips">CHIPS_{c['id']}</span></p></div>
</section>
</main>'''
    return h + main + foot

RETAIL_IDS = {"falabella", "ripley", "cencosud"}
RETAIL_LINK = '<p class="small">Compárala con sus pares en el <a href="../../comparadores/retail/index.html">comparador de retail: Falabella vs. Ripley vs. Cencosud</a>.</p>'

# lista de fichas existentes (orden de chips en afpcapital + ella misma)
old = re.findall(r'<a href="\.\./([a-z0-9-]+)/index\.html">([A-Z0-9-]+)</a>', tpl.split('class="chips"')[1].split("</span>")[0])
old_ids = [("afpcapital", "AFPCAPITAL")] + old
# SQM-B tiene ficha pero no aparece en chips: se respeta
for c in NEW:
    wr(f"acciones/{c['id']}/index.html", ficha(c))

all_chips = old_ids + [(c["id"], c["t"]) for c in NEW]
new_chip_html = "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in [(c["id"], c["t"]) for c in NEW])
for c in NEW:
    p = f"acciones/{c['id']}/index.html"
    ch = "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in all_chips if i != c["id"])
    wr(p, rd(p).replace(f"CHIPS_{c['id']}", ch))

# chips en fichas existentes
for d in os.listdir(os.path.join(S, "acciones")):
    p = f"acciones/{d}/index.html"
    if d in {c["id"] for c in NEW} or not os.path.isfile(os.path.join(S, p)): continue
    t = rd(p)
    if 'class="chips"' in t and 'href="../falabella/' not in t:
        pre, post = t.split('class="chips">', 1)
        inner, tail = post.split("</span>", 1)
        t = pre + 'class="chips">' + inner + new_chip_html + "</span>" + tail
        wr(p, t)

# arreglo BCI: el video quedó como texto en "Qué mirar"
p = "acciones/bci/index.html"; t = rd(p)
t = t.replace("<li>('BCI: resultados del segundo trimestre 2026', 'https://youtu.be/Ajbcv-O2SSg')</li>",
  "<li>Margen de intereses y sensibilidad a las tasas en Chile y EE.UU.</li><li>Resultado de City National Bank of Florida.</li><li>Gasto en provisiones y morosidad.</li><li>Eficiencia y nivel de capital.</li>")
t = t.replace('<p>Mira nuestros análisis en video de BCI en YouTube y en X.</p><div class="vids"></div>',
  '<div class="vids"><a class="vid" href="https://youtu.be/Ajbcv-O2SSg" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/Ajbcv-O2SSg/hqdefault.jpg" alt="" loading="lazy"><span>BCI: resultados del segundo trimestre 2026</span></a></div>')
wr(p, t)

# ---------------------------------------------------------------- cinta de precios en todas las páginas
def tape_items(prefix):
    out = ""
    for c in NEW:
        cls = "up" if c["chg"] >= 0 else "down"
        out += f'<a href="{prefix}acciones/{c["id"]}/index.html"><b>{c["t"]}</b> {c["px"]} <span class="{cls}">{"+" if c["chg"] > 0 else ""}{n(c["chg"], 0, "%")} 12m</span></a>'
    return out

for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.relpath(os.path.join(root, f), S)
        t = rd(p)
        m = re.search(r'<div class="tape-in"><a href="([./]*)acciones/cap/index\.html"', t)
        if not m or "acciones/falabella/index.html\"><b>FALABELLA" in t: continue
        t = t.replace('<span><b>ORO BLANCO</b>', tape_items(m.group(1)) + '<span><b>ORO BLANCO</b>')
        wr(p, t)

# ---------------------------------------------------------------- portada
p = "index.html"; t = rd(p)
cards = ""
for c in NEW:
    cls = "up" if c["chg"] >= 0 else "down"
    cards += f'''<a class="stock-card" href="acciones/{c['id']}/index.html">
  <span class="tk">{c['t']}</span>
  <span class="nm">{c['n']}</span>
  <span class="sc">{c['s']}</span>
  <span class="row"><span>P/E <b>{n(c['pe'], 1, 'x') if c['pe'] else 'n/a'}</b></span><span>Div. <b>{n(c['dy'], 1, '%')}</b></span><span class="{cls}">{"+" if c['chg'] > 0 else ""}{n(c['chg'], 0, '%')}</span></span>
</a>'''
if 'acciones/falabella/index.html">\n  <span class="tk">' not in t:
    t = t.replace('<div class="stock-grid">', '<div class="stock-grid">' + cards, 1)
t = t.replace("CAP vs. CMPC, Banco de Chile vs. Santander, Aguas Andinas vs. IAM y SQM vs. Oro Blanco.",
              "Retail (Falabella, Ripley y Cencosud), bancos, AFP, CAP vs. CMPC, Aguas Andinas vs. IAM y SQM vs. Oro Blanco.")
wr(p, t)

# ---------------------------------------------------------------- listado de acciones
p = "acciones/index.html"; t = rd(p)
rows = ""
for c in NEW:
    cls = "up" if c["chg"] >= 0 else "down"
    rows += f'<tr><th scope="row"><a href="{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["n"]}</td><td class="txt">{c["s"]}</td><td>{c["px"]}</td><td>{n(c["pe"], 1, "x") if c["pe"] else "n/a"}</td><td>{n(c["dy"], 1, "%")}</td><td class="{cls}">{"+" if c["chg"] > 0 else ""}{n(c["chg"], 0, "%")}</td></tr>'
if 'href="falabella/index.html"' not in t:
    t = t.replace("</tbody></table></div>\n<p class=\"note\">", rows + "</tbody></table></div>\n<p class=\"note\">", 1)
wr(p, t)

# ---------------------------------------------------------------- valoraciones
p = "valoraciones/index.html"; t = rd(p)
rows = ""
f1 = lambda v, s: n(v, 1, s) if v is not None else "n/a"
for c in NEW:
    rows += f'<tr><th scope="row"><a href="../acciones/{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["s"]}</td><td>{f1(c["pe"], "x")}</td><td>{f1(c["fpe"], "x")}</td><td>{f1(c["pbv"], "x")}</td><td>{f1(c["ev"], "x")}</td><td>{f1(c["dy"], "%")}</td><td>{f1(c["roe"], "%")}</td></tr>'
if "acciones/falabella/" not in t:
    t = t.replace("</tbody></table></div>", rows + "</tbody></table></div>", 1)
wr(p, t)

# ---------------------------------------------------------------- rankings
p = "rankings/index.html"; t = rd(p)
m = re.search(r"RANK_DATA=(\[.*?\]);", t, re.S)
data = json.loads(m.group(1))
if not any(d["id"] == "falabella" for d in data):
    for c in NEW:
        if c["pe"] is None: continue  # sin P/E (pérdida) no entra al ranking
        data.append({"id": c["id"], "t": c["t"], "n": c["n"], "s": c["s"], "pe": c["pe"], "epsg": c["epsg"], "dy": c["dy"], "chg": c["chg"], "link": True})
    t = t[:m.start(1)] + json.dumps(data, ensure_ascii=False) + t[m.end(1):]
wr(p, t)

# ---------------------------------------------------------------- resultados
p = "resultados/index.html"; t = rd(p)
if 'id="falabella"' not in t:
    secs = ""
    for c in NEW:
        body = ficha(c).split("<h2 class=\"h-sec\">Resultados del segundo trimestre 2026</h2>", 1)[1].split("</section>", 1)[0]
        body = body.replace(NOTE, "")
        secs += f'<section id="{c["id"]}"><h2 class="h-sec"><a href="../acciones/{c["id"]}/index.html">{c["n"]}</a></h2>{body}</section>'
    t = t.replace("</main>", secs + "\n</main>", 1)
    chips = "".join(f'<a href="#{c["id"]}">{c["t"]}</a>' for c in NEW)
    t = re.sub(r'(<p class="chips">.*?)(</p>)', lambda mm: mm.group(1) + chips + mm.group(2), t, count=1, flags=re.S)
wr(p, t)

json.dump(NEW, open(os.path.join(S, "../new.json"), "w"), ensure_ascii=False)
print("ok")
