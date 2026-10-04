import os, re, json
exec(open("build.py").read().split("# ---------------------------------------------------------------- datos")[0])
NOTE = '<p class="note">Cifras de nuestro video de resultados 2T 2026 (estados financieros, análisis razonado y reportes de la empresa). P/BV y ROE: StockAnalysis, septiembre 2026. (c) = cifra calculada por nosotros.</p>'

NEW = [
 dict(id="colbun", t="COLBUN", n="Colbún", s="Generación eléctrica (Chile y Perú)", px="$146,18", chg=-4,
  pe=22.5, fpe=12.0, pbv=0.82, ev=7.3, dy=3.9, roe=3.5, epsg=-16, vid="GhovLULVg08", q="Colbun",
  lede="Generadora eléctrica del grupo Matte, con centrales hidroeléctricas, térmicas (gas y carbón), eólicas y solares en Chile, más la central Fenix en Perú. Vende energía a clientes libres y distribuidoras con contratos de largo plazo; en años secos genera menos con agua y su resultado depende del costo del respaldo térmico. Reporta en dólares.",
  vtitle="Colbún: EBITDA +12% en un año seco, pero la utilidad cae 24% (2T 2026)",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",402.6,449.2,1),("EBITDA",140.6,156.9,1),("Resultado operacional",82.7,89.5,1),("Utilidad neta",48.2,36.6,1),("Utilidad controladores",44.4,36.7,1),("EPS (US$ por acción)",0.0025,0.0021,4)],
  derived=("Margen EBITDA","34,9%","34,9%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>2,8x</b> (2,3x en dic-2025). Ingresos 10,9% sobre el consenso, pero EPS ~16% bajo lo esperado por el costo de terminar contratos de carbón.",
  tiles=[("P/E","22,5x"),("Forward P/E","~12x"),("EV/EBITDA","7,3x"),("FCF yield","~11%"),("Dividend Yield","3,9%"),("P/BV","0,82x")],
  small="ROE <b>3,5%</b> · Precio objetivo consenso <b>$156</b> (+7%) · Capex 2S26 ~US$200 MM, la mitad en baterías.",
  mirar=["Hidrología: los embalses mejoraron con las lluvias de julio.","Entrada de las baterías Celda Solar y Diego de Almagro Sur (228 MW cada una).","Perú (Fenix): EBITDA +26% con nuevos contratos regulados.","Deuda neta que sube a 2,8x EBITDA y gasto financiero +27%."]),
 dict(id="ecl", t="ECL", n="Engie Energía Chile", s="Generación y transmisión eléctrica", px="$1.847", chg=36,
  pe=8.3, fpe=6.6, pbv=1.11, ev=6.2, dy=3.2, roe=15.2, epsg=-20, vid="xrTDtUxANNI", q="Engie",
  lede="Generadora y transmisora eléctrica del grupo francés Engie, con foco en el norte de Chile y clientes mineros. Está reemplazando sus centrales a carbón por eólica, solar y baterías. Reporta en dólares.",
  vtitle="Engie Energía Chile: le gana al consenso (+36% en EPS) y confirma su guía (2T 2026)",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",582.2,521.6,1),("Ventas de energía y potencia",436.9,477.6,1),("EBITDA",202.0,184.6,1),("Resultado operacional",160.2,139.7,1),("Utilidad neta",107.7,86.6,1),("EPS (US$ por acción)",0.102,0.082,3)],
  derived=("Margen EBITDA","34,7%","35,4%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>3,53x</b> (3,87x en dic-2025). EPS de US$0,082 vs. US$0,0586 esperado por el consenso (+36%). El 2T 2025 incluía US$101 MM por el arbitraje de GNL.",
  tiles=[("P/E","8,3x"),("Forward P/E","6,6x"),("EV/EBITDA","6,2x"),("FCF yield","12,3%"),("Dividend Yield","~3,2%"),("P/BV","1,11x")],
  small="ROE <b>15,2%</b> · Guía 2026 sin cambios: EBITDA US$690–760 MM · Precio objetivo promedio <b>$1.936</b> (+5%).",
  mirar=["Si sube la guía de EBITDA 2026: el primer semestre ya cubre 53% del punto medio.","Baterías: más almacenamiento comprime los precios de la tarde.","Eólicos Chequenes y Pampa Fidelia (471 MW), que entran en 2027.","Capex alto que mantiene la deuda cerca de 3,5x EBITDA."]),
 dict(id="aes-andes", t="AES ANDES", n="AES Andes", s="Generación eléctrica (no cotiza en bolsa)", px="No cotiza", chg=None,
  pe=None, fpe=None, pbv=None, ev=None, dy=None, roe=None, epsg=None, vid="EnQHavuXcrY", q="AES Andes",
  pxnote="Valor implícito por múltiplos de pares: ~$187 por acción",
  lede="Ex AES Gener. Generadora eléctrica en Chile, Colombia (Chivor) y Argentina, controlada en 99,6% por la estadounidense AES Corp. No cotiza desde abril de 2024, por eso su valor se estima con los múltiplos de sus pares. Reporta en dólares.",
  vtitle="AES Andes: EBITDA +38% por Colombia y cuánto valdría fuera de bolsa (2T 2026)",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",498.2,633.4,1),("Ganancia bruta",127.9,171.4,1),("EBITDA",157.9,218.6,1),("Utilidad atribuible",20.7,107.1,1),("EPS (US$ por acción)",0.0020,0.0103,4)],
  derived=("Margen EBITDA","31,7%","34,5%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>3,3x</b> (c). Sin ítems no recurrentes (impuestos y venta de JK 1&amp;2), la utilidad del trimestre habría sido ~US$67 MM (c).",
  tiles=[("EV/EBITDA de pares","6,0x"),("Valor implícito US$ MM","~2.000"),("Por acción","~$187"),("P/E implícito","9,2x"),("FCF yield implícito","14%"),("Div. yield implícito","6,7%")],
  small="Rango con 5,5x–6,5x EBITDA: <b>$152–$222</b> por acción. No hay consenso de analistas: se compara contra el 2T 2025.",
  mirar=["Colombia: la sequía y los precios spot explican la mayor parte del alza.","Utilidad con ítems no recurrentes.","Deuda neta de 3,3x EBITDA tras asumir la deuda de Cochrane.","Venta de AES Corp al consorcio GIP/EQT y qué pasa con AES Andes."]),
 dict(id="cge", t="CGE", n="CGE", s="Distribución eléctrica", px="$215,1", chg=-27,
  pe=13.6, fpe=None, pbv=0.29, ev=9.3, dy=1.0, roe=2.2, epsg=141, vid="PJcS0kL5VXQ", q="CGE",
  lede="Compañía General de Electricidad: la mayor distribuidora eléctrica de Chile por número de clientes (3,46 millones), de Arica a Los Lagos, además de transmisión zonal. Su ingreso depende de las tarifas reguladas (VAD). La controla la china State Grid con 97,1%. Reporta en pesos.",
  vtitle="",
  cap="Cifras en CLP miles de millones salvo BPA · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",608.7,593.3,1),("Ganancia bruta",63.9,66.4,1),("EBITDA",46.5,52.8,1),("Resultado operacional",24.8,28.4,1),("Utilidad atribuible",3.08,7.43,2),("BPA (CLP por acción)",1.52,3.68,2)],
  derived=("Margen EBITDA","7,6%","8,9%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>6,8x</b> (7,0x en dic-2025). Los costos financieros del semestre casi se duplicaron (73,9 vs. 37,6).",
  tiles=[("P/E","13,6x"),("P/E 1S anualizado","~8,2x"),("EV/EBITDA","9,3x"),("P/BV","0,29x"),("Dividend Yield","~1%"),("FCF 12 meses","Negativo")],
  small="ROE <b>2,2%</b> · State Grid tiene el 97,1% y la acción casi no transa (~10 mil acciones al día). Sin consenso de analistas.",
  mirar=["Deuda de 6,8x EBITDA, 44% de corto plazo.","Aplicación de la Ley 21.833 y del convenio por los saldos de la Ley 21.423.","Pérdidas de energía (12,25%) e incobrables.","Liquidez: con 97% en manos de State Grid, comprar o vender es difícil."]),
 dict(id="enelchile", t="ENELCHILE", n="Enel Chile", s="Generación y distribución eléctrica", px="$81,35", chg=26,
  pe=10.4, fpe=9.3, pbv=1.08, ev=6.5, dy=4.3, roe=11.0, epsg=54, vid="khEkiKu6VaQ", q="Enel Chile",
  lede="Holding eléctrico del grupo italiano Enel: controla Enel Generación Chile (~93,6%) y Enel Distribución, que abastece Santiago. Cotiza en Santiago y como ADS en Nueva York (1 ADS = 50 acciones). Reporta en dólares.",
  vtitle="",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos operacionales",1177,1071,0),("Margen de contribución",415,374,0),("EBITDA",293,262,0),("EBIT",166,186,0),("Utilidad atribuible",71,110,0),("EPS por ADS (US$)",0.051,0.080,3)],
  derived=("Margen EBITDA","24,9%","24,5%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>2,3x</b> (c). EPS por ADS en línea con el consenso (−2%). Sin deterioros ni su reversión (Bocamina II), la utilidad habría caído ~5% (c).",
  tiles=[("P/E","10,4x"),("Forward P/E","9,3x"),("EV/EBITDA","6,5x"),("FCF yield","10,7%"),("Dividend Yield","4,3%"),("P/BV","1,08x")],
  small="ROE <b>11,0%</b> · Guía 2026 confirmada: EBITDA US$1,3–1,5 mil MM y utilidad US$0,5–0,7 mil MM · Renta4: compra, objetivo <b>$91</b> (+12%).",
  mirar=["Hidrología: la generación cayó 7,5% en el trimestre.","Utilidad apoyada en no recurrentes (Shell US$140 MM en el 1T y Bocamina II).","Distribución: EBITDA a la baja y pérdidas de energía de 6,6%.","Capex que se duplicó y la meta de deuda ≤2,0x EBITDA en 2028."]),
 dict(id="enelgxch", t="ENELGXCH", n="Enel Generación Chile", s="Generación eléctrica", px="$594,74", chg=30,
  pe=9.1, fpe=10.0, pbv=1.84, ev=5.9, dy=6.9, roe=20.4, epsg=0, vid="Rmt5ooXcaG4", q="Enel Generacion",
  lede="Generadora eléctrica filial de Enel Chile (~93,6%), del grupo italiano Enel. Opera centrales hidroeléctricas y térmicas a gas, y vende energía a distribuidoras y clientes libres con contratos de largo plazo. Sus resultados dependen de la hidrología y del precio del gas. Reporta en dólares.",
  vtitle="Enel Generación Chile: la sequía golpea el EBITDA (−23%) (2T 2026)",
  cap="Cifras en US$ millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos totales",800,693,0),("Margen de contribución",218,173,0),("EBITDA",173,134,0),("EBIT",155,143,0),("Utilidad atribuible",106,106,0),("EPS (US$ por acción)",0.013,0.013,3)],
  derived=("Margen EBITDA","21,6%","19,3%"),
  kpi="Deuda neta / EBITDA 12 meses: <b>0,3x</b> (c). Sin la reversión del deterioro de Bocamina II, la utilidad habría sido ~US$83 MM (c). No hay consenso publicado.",
  tiles=[("P/E","9,1x"),("Forward P/E","~10x"),("EV/EBITDA","5,9x"),("FCF yield","10,2%"),("Dividend Yield","6,9%"),("P/BV","1,84x")],
  small="ROE <b>20,4%</b> · Sin los US$140 MM de Shell del 1T, el EV/EBITDA sube a 6,9x y el FCF yield baja a 4,7%.",
  mirar=["Hidrología: la generación cayó 15,9% en el trimestre.","Gas argentino hasta abril de 2027 y compras de GNL.","Utilidad apoyada en no recurrentes (Shell y Bocamina II).","Baja liquidez (Enel Chile tiene ~93,6%) y dividend yield a la baja."]),
]
VAROV = {('colbun','Ingresos'):11.6,('colbun','EBITDA'):11.6,('colbun','Utilidad neta'):-24.0,('aes-andes','EBITDA'):38.4,('aes-andes','Utilidad atribuible'):417.0,
         ('cge','EBITDA'):13.4,('cge','Utilidad atribuible'):141.0,('enelchile','Utilidad atribuible'):54.2,('enelgxch','Utilidad atribuible'):0.0,('ecl','EBITDA'):-8.6}
ENERGY_LINK = '<p class="small">Compárala con sus pares en el <a href="../../comparadores/energia/index.html">comparador de empresas de energía</a>.</p>'
NEWIDS = [c["id"] for c in NEW if c["id"] != "enelgxch"]

tpl = rd("acciones/afpcapital/index.html")
head, rest = tpl.split('<main class="wrap">', 1)
_, foot = rest.split("</main>", 1)

def var(a, b):
    if a is None or b is None or a <= 0 or b <= 0: return None
    return (b / a - 1) * 100

def chg_s(c): return f'{"+" if c["chg"] > 0 else ""}{n(c["chg"], 0, "%")}'

def ficha(c):
    h = head.replace("<title>AFPCAPITAL · AI ACCIONES CHILE</title>", f"<title>{c['t']} · AI ACCIONES CHILE</title>")
    h = h.replace("Ficha de AFP Capital: resultados, valoración y claves.", f"Ficha de {c['n']}: resultados 2T 2026, valoración y claves.")
    if c["chg"] is None:
        q = f'<span class="tk">{c["t"]}</span>\n    <span class="px">{c["px"]}</span>\n    <span class="note">{c["pxnote"]}</span>'
    else:
        q = f'<span class="tk">{c["t"]}</span>\n    <span class="px">{c["px"]}</span>\n    <span class="{"up" if c["chg"] >= 0 else "down"}">{chg_s(c)} en 12 meses</span>\n    <span class="note">Precio de cierre usado en el video (sep-2026)</span>'
    tiles = "".join(f'<div class="tile"><span class="lbl">{a}</span><span class="val">{b}</span></div>' for a, b in c["tiles"])
    trs = ""
    for lbl, a, b, d in c["rows"]:
        v = VAROV.get((c['id'], lbl), var(a, b))
        vs = pct(v) if v is not None else "n/a"
        if v == 0: vs = "0,0%"
        trs += f'<tr><th scope="row">{lbl}</th><td class="{"neg" if a < 0 else ""}">{n(a, d)}</td><td class="{"neg" if b < 0 else ""}">{n(b, d)}</td><td class="{"neg" if v is not None and v < 0 else ""}">{vs}</td></tr>'
    if c["derived"]:
        trs += f'<tr class="derived"><th scope="row">{c["derived"][0]}</th><td>{c["derived"][1]}</td><td>{c["derived"][2]}</td><td></td></tr>'
    mirar = "".join(f"<li>{m}</li>" for m in c["mirar"])
    if c["vid"]:
        vids = f'<div class="vids"><a class="vid" href="https://youtu.be/{c["vid"]}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{c["vid"]}/hqdefault.jpg" alt="" loading="lazy"><span>{c["vtitle"]}</span></a></div>'
    else:
        vids = f'<p>El video de resultados 2T 2026 de {c["n"]} se publicará pronto en nuestro canal.</p>'
    main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Acciones</a> / {c['t']}</nav>
<section class="page-head stock-head">
  <div>
    <p class="eyebrow">{c['s']}</p>
    <h1>{c['n']}</h1>
    <p class="lede">{c['lede']}</p>
  </div>
  <div class="quote">
    {q}
  </div>
</section>
<section><h2 class="h-sec">Valoración</h2><div class="tiles">{tiles}</div>
<p class="small">{c['small']} ¿No conoces algún múltiplo? Revisa la sección <a href="../../educacion/index.html">Educación</a>.</p></section>
<section><h2 class="h-sec">Resultados del segundo trimestre 2026</h2><div class="table-scroll"><table class="data">
<caption>{c['cap']}</caption>
<thead><tr><th scope="col">Concepto</th><th>2T 2025</th><th>2T 2026</th><th>Var. a/a</th></tr></thead><tbody>{trs}</tbody></table></div>
<p class="kpi-line">{c['kpi']}</p>{NOTE}</section>
<section class="two">
  <div><h2 class="h-sec">Qué mirar</h2><ul class="checks">{mirar}</ul>{ENERGY_LINK}</div>
  <div class="aside-box"><h2 class="h-sec">Videos</h2>{vids}
<div class="vid-btns"><a class="btn" href="{CH}/search?query={c['q'].replace(' ', '+')}" target="_blank" rel="noopener">{YT} Videos de {c['t']} en YouTube</a><a class="btn ghost" href="https://x.com/aiacciones" target="_blank" rel="noopener">{XI} Ver en X</a></div><p class="small">Otras fichas: <span class="chips">CHIPS_{c['id']}</span></p></div>
</section>
</main>'''
    return h + main + foot

old = re.findall(r'<a href="\.\./([a-z0-9-]+)/index\.html">([A-Z0-9 -]+)</a>', tpl.split('class="chips"')[1].split("</span>")[0])
old_ids = [("afpcapital", "AFPCAPITAL")] + old
new_pairs = [(c["id"], c["t"]) for c in NEW if c["id"] != "enelgxch"]
all_chips = old_ids + new_pairs
new_chip_html = "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in new_pairs)
for c in NEW:
    p = f"acciones/{c['id']}/index.html"
    ch = "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in all_chips if i != c["id"])
    wr(p, ficha(c).replace(f"CHIPS_{c['id']}", ch))

for d in os.listdir(os.path.join(S, "acciones")):
    p = f"acciones/{d}/index.html"
    if d in {c["id"] for c in NEW} or not os.path.isfile(os.path.join(S, p)): continue
    t = rd(p)
    if 'class="chips"' in t and 'href="../colbun/' not in t:
        pre, post = t.split('class="chips">', 1)
        inner, tail = post.split("</span>", 1)
        wr(p, pre + 'class="chips">' + inner + new_chip_html + "</span>" + tail)

# cinta: ENELGXCH actualizada + nuevas (AES Andes no cotiza)
def tape_item(prefix, c):
    return f'<a href="{prefix}acciones/{c["id"]}/index.html"><b>{c["t"]}</b> {c["px"]} <span class="{"up" if c["chg"] >= 0 else "down"}">{chg_s(c)} 12m</span></a>'
for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.relpath(os.path.join(root, f), S)
        t = rd(p)
        m = re.search(r'<div class="tape-in"><a href="([./]*)acciones/cap/index\.html"', t)
        if not m or "<b>COLBUN</b>" in t: continue
        pre = m.group(1)
        t = re.sub(r'<a href="[./]*acciones/enelgxch/index\.html"><b>ENELGXCH</b>.*?</a>', lambda _: tape_item(pre, NEW[-1]), t)
        t = t.replace('<span><b>ORO BLANCO</b>', "".join(tape_item(pre, c) for c in NEW if c["chg"] is not None and c["id"] != "enelgxch") + '<span><b>ORO BLANCO</b>')
        wr(p, t)

# portada
def card(c):
    if c["chg"] is None:
        row = '<span>No cotiza</span><span>Valor por múltiplos de pares</span>'
    else:
        row = f'<span>P/E <b>{n(c["pe"], 1, "x")}</b></span><span>Div. <b>{n(c["dy"], 1, "%")}</b></span><span class="{"up" if c["chg"] >= 0 else "down"}">{chg_s(c)}</span>'
    return f'''<a class="stock-card" href="acciones/{c['id']}/index.html">
  <span class="tk">{c['t']}</span>
  <span class="nm">{c['n']}</span>
  <span class="sc">{c['s']}</span>
  <span class="row">{row}</span>
</a>'''
p = "index.html"; t = rd(p)
if 'href="acciones/colbun/index.html">\n' not in t:
    t = re.sub(r'<a class="stock-card" href="acciones/enelgxch/index\.html">.*?</a>', "", t, flags=re.S)
    t = t.replace('<div class="stock-grid">', '<div class="stock-grid">' + "".join(card(c) for c in NEW), 1)
    t = t.replace("Retail (Falabella, Ripley y Cencosud), bancos,", "Energía (Colbún, Engie, AES Andes, CGE, Enel Chile y Enel Generación), retail (Falabella, Ripley y Cencosud), bancos,")
wr(p, t)

# listado de acciones
p = "acciones/index.html"; t = rd(p)
def arow(c):
    if c["chg"] is None:
        return f'<tr><th scope="row"><a href="{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["n"]}</td><td class="txt">{c["s"]}</td><td>No cotiza</td><td>n/a</td><td>n/a</td><td>n/a</td></tr>'
    return f'<tr><th scope="row"><a href="{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["n"]}</td><td class="txt">{c["s"]}</td><td>{c["px"]}</td><td>{n(c["pe"], 1, "x")}</td><td>{n(c["dy"], 1, "%")}</td><td class="{"up" if c["chg"] >= 0 else "down"}">{chg_s(c)}</td></tr>'
if 'href="colbun/index.html"' not in t:
    t = re.sub(r'<tr><th scope="row"><a href="enelgxch/.*?</tr>', lambda _: arow(NEW[-1]), t, flags=re.S)
    t = t.replace("</tbody></table></div>\n<p class=\"note\">", "".join(arow(c) for c in NEW[:-1]) + "</tbody></table></div>\n<p class=\"note\">", 1)
wr(p, t)

# valoraciones (AES Andes no cotiza: fuera)
p = "valoraciones/index.html"; t = rd(p)
f1 = lambda v, s: n(v, 1, s) if v is not None else "n/a"
def vrow(c): return f'<tr><th scope="row"><a href="../acciones/{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["s"]}</td><td>{f1(c["pe"], "x")}</td><td>{f1(c["fpe"], "x")}</td><td>{n(c["pbv"], 2, "x")}</td><td>{f1(c["ev"], "x")}</td><td>{f1(c["dy"], "%")}</td><td>{f1(c["roe"], "%")}</td></tr>'
if "acciones/colbun/" not in t:
    t = re.sub(r'<tr><th scope="row"><a href="\.\./acciones/enelgxch/.*?</tr>', lambda _: vrow(NEW[-1]), t, flags=re.S)
    t = t.replace("</tbody></table></div>", "".join(vrow(c) for c in NEW[:-1] if c["pe"]) + "</tbody></table></div>", 1)
wr(p, t)

# rankings
p = "rankings/index.html"; t = rd(p)
m = re.search(r"RANK_DATA=(\[.*?\]);", t, re.S)
data = json.loads(m.group(1))
for c in NEW:
    if c["pe"] is None: continue
    d = {"id": c["id"], "t": c["t"], "n": c["n"], "s": c["s"], "pe": c["pe"], "epsg": c["epsg"], "dy": c["dy"], "chg": c["chg"], "link": True}
    ex = [i for i, x in enumerate(data) if x["id"] == c["id"]]
    if ex: data[ex[0]] = d
    else: data.append(d)
t = t[:m.start(1)] + json.dumps(data, ensure_ascii=False) + t[m.end(1):]
wr(p, t)

# resultados
p = "resultados/index.html"; t = rd(p)
def rsec(c):
    body = ficha(c).split("<h2 class=\"h-sec\">Resultados del segundo trimestre 2026</h2>", 1)[1].split("</section>", 1)[0].replace(NOTE, "")
    return f'<section id="{c["id"]}"><h2 class="h-sec"><a href="../acciones/{c["id"]}/index.html">{c["n"]}</a></h2>{body}</section>'
if 'id="colbun"' not in t:
    t = re.sub(r'<section id="enelgxch">.*?</section>', lambda _: rsec(NEW[-1]), t, count=1, flags=re.S)
    t = t.replace("</main>", "".join(rsec(c) for c in NEW[:-1]) + "\n</main>", 1)
    chips = "".join(f'<a href="#{c["id"]}">{c["t"]}</a>' for c in NEW[:-1])
    t = re.sub(r'(<p class="chips">.*?)(</p>)', lambda mm: mm.group(1) + chips + mm.group(2), t, count=1, flags=re.S)
wr(p, t)
print("ok")
