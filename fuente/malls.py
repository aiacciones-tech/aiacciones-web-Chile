import os, re
S = "/tmp/claude-0/-home-claude/51bbcb85-f720-5650-9a37-2f75843c73b7/scratchpad/site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)
def n(v, d=1, suf=""):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + suf


T = ["MALLPLAZA", "PARAUCO", "CENCOMALLS"]
IDS = ["mallplaza", "parauco", "cencomalls"]
NAMES = ["Mall Plaza", "Parque Arauco", "Cencosud Shopping"]
N = None
BLOCKS = [
 ("valoracion", "Valoración",
  "Cuánto paga el mercado por las utilidades, el EBITDA y el FFO (el flujo recurrente de un dueño de malls) de cada empresa, con precios al 2 de octubre de 2026. El P/E de 12 meses no suma puntos: el de Mall Plaza (6,2x) está inflado por revalorizaciones contables de sus malls; sin ellas ronda 26x.",
  "Cencosud Shopping es la más barata en todos los múltiplos que suman puntos: forward P/E de 13,9x, EV/EBITDA de 12,9x y el FFO yield más alto (6,9%). Mall Plaza y Parque Arauco transan cerca de 17x EBITDA, un múltiplo exigente. Parque Arauco es la más cara por utilidades porque no revaloriza sus malls hasta diciembre.",
  [("P/E (12 meses, contable)", [6.2, 23.1, 10.8], 1, "x", None, False, True),
   ("Forward P/E 2026", [16.8, 24.2, 13.9], 1, "x", "min", False, True),
   ("EV/EBITDA", [16.9, 16.6, 12.9], 1, "x", "min", False, True),
   ("P/FFO", [18.1, 16.0, 14.5], 1, "x", "min", False, True),
   ("FFO yield", [5.5, 6.3, 6.9], 1, "%", "max", False, True),
   ("P/BV", [1.78, 1.64, 1.2], 2, "x", "min", False, False)]),
 ("rentabilidad", "Rentabilidad y márgenes",
  "Qué parte de cada peso de ingresos queda como margen en el segundo trimestre 2026, y cuánto rinde el patrimonio. El ROE de Mall Plaza está inflado por revalorizaciones, por eso no suma puntos.",
  "Cencosud Shopping tiene los márgenes más altos (EBITDA de 90%), porque sus malls son casi solo arriendo y no tiene costos de operación relevantes. Mall Plaza le sigue con 81%. Parque Arauco tiene márgenes más bajos (72%) por la etapa de maduración de sus nuevos proyectos y su mayor peso en Perú y Colombia.",
  [("Margen bruto 2T26", [91.6, 79.5, 97.1], 1, "%", "max", False, False),
   ("Margen operacional 2T26", [79.5, 71.0, 89.4], 1, "%", "max", False, True),
   ("Margen EBITDA 2T26", [80.6, 71.7, 90.4], 1, "%", "max", False, True),
   ("ROE (contable)", [29.7, 10.6, 11.3], 1, "%", None, False, False)]),
 ("deuda", "Deuda y flujo de caja",
  "Cuántos años de EBITDA tomaría pagar la deuda financiera neta, y cuánta caja libre generó cada una en el primer semestre (flujo operacional menos capex, en miles de millones de pesos).",
  "Cencosud Shopping (2,3x) y Mall Plaza (2,4x, clasificación AAA) tienen deuda cómoda. Parque Arauco es la más apalancada (4,5x) por su plan de inversión. Mall Plaza es la que más caja libre genera; Cencosud Shopping quedó negativa en el semestre por la compra de Plaza Central en Bogotá.",
  [("Deuda neta / EBITDA", [2.4, 4.5, 2.3], 1, "x", "min", False, True),
   ("Flujo de caja libre 1S ($ mil MM)", [176.6, 55.4, -24.2], 1, "", "max", True, True)]),
 ("crecimiento", "Crecimiento y sorpresa del trimestre",
  "Cómo evolucionaron los ingresos, el EBITDA, el FFO, la utilidad y las ventas de los locatarios frente al 2T 2025, y cuánto se alejó la utilidad por acción del consenso. Mall Plaza no tiene consenso trimestral publicado (sus ingresos quedaron en línea con el consenso anual).",
  "Parque Arauco es la que más crece en ingresos (+18%), EBITDA (+16%) y ventas de locatarios (+13%), gracias a Kennedy Oriente y Minka. Cencosud Shopping fue la única con utilidad al alza (+27%) y sobre el consenso (+12%). La utilidad de Mall Plaza cayó 45% solo porque el 2T 2025 tuvo una revalorización mucho mayor.",
  [("Ingresos a/a", [8.7, 17.9, 9.3], 1, "%", "max", True, True),
   ("EBITDA a/a", [9.6, 15.8, 9.5], 1, "%", "max", True, True),
   ("FFO a/a", [8.8, 10.5, 13.6], 1, "%", "max", True, True),
   ("Utilidad a/a", [-44.5, -30.8, 26.8], 1, "%", "max", True, True),
   ("Ventas de locatarios a/a", [6.7, 12.6, 0.1], 1, "%", "max", True, False),
   ("EPS vs. consenso", [N, -49.0, 12.0], 0, "%", "max", True, False)]),
 ("dividendos", "Dividendos",
  "Dividendos pagados en 12 meses sobre el precio de la acción.",
  "Cencosud Shopping paga el mayor dividendo (3,3%). Mall Plaza (1,9%) y Parque Arauco (1,2%) reparten menos porque reinvierten en expansión.",
  [("Dividend Yield", [1.9, 1.2, 3.3], 1, "%", "max", False, True)]),
 ("mercado", "Mercado",
  "Cómo se ha movido la acción en 12 meses y cuánto potencial ven los analistas según su precio objetivo.",
  "Parque Arauco (+84%) y Mall Plaza (+39%) subieron fuerte, lo que explica sus múltiplos altos. Cencosud Shopping casi no se movió (+6%) y es la que más potencial tiene al precio objetivo (+25%).",
  [("Var. precio 12m", [39.0, 84.0, 6.2], 0, "%", "max", True, True),
   ("Potencial al precio objetivo", [14.5, 16.0, 25.0], 1, "%", "max", True, True)]),
]
K = len(T)
def fmt(v, d, suf, sign):
    if v is None: return "n/d"
    return ("+" if sign and v > 0 else "") + n(v, d, suf)
def besti(vals, best):
    ok = [(v, i) for i, v in enumerate(vals) if v is not None]
    if not best or not ok: return -1
    return (min(ok) if best == "min" else max(ok))[1]

def chart(lbl, vals, d, suf, best, sign):
    vv = [v for v in vals if v is not None]
    lo, hi = min(0, min(vv)), max(0, max(vv))
    sc = 170 / (hi - lo); x0 = 92 + (-lo) * sc
    bi = besti(vals, best)
    H = 8 + 26 * K
    aria = ", ".join(f"{t} {fmt(v, d, suf, sign)}" for t, v in zip(T, vals))
    out = f'<figure class="bchart"><figcaption>{lbl}<span>{" · menor es mejor" if best == "min" else (" · mayor es mejor" if best == "max" else "")}</span></figcaption><svg viewBox="0 0 320 {H}" role="img" aria-label="{lbl}: {aria}">'
    for i, (t, v) in enumerate(zip(T, vals)):
        y = 8 + 26 * i
        out += f'<text x="84" y="{y+11}" text-anchor="end" class="bl">{t}</text>'
        if v is None:
            out += f'<text x="{x0+6:.1f}" y="{y+11}" class="bv">n/d</text>'; continue
        w = max(abs(v) * sc, 1.5)
        x = x0 if v >= 0 else x0 - w
        tx = x0 + w + 6 if v >= 0 else x0 + 6
        col = "#3b86e6" if i == bi else "#5a5a57"
        out += f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="16" rx="2" fill="{col}"/><text x="{tx:.1f}" y="{y+11}" class="bv{" best" if i == bi else ""}">{fmt(v, d, suf, sign)}</text>'
    out += f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="2" y2="{H-2}" class="b0"/></svg></figure>'
    return out

def thead(first): return f'<thead><tr><th scope="col">{first}</th>' + "".join(f'<th scope="col">{t}</th>' for t in T) + "</tr></thead>"

score = {k: [0]*K for k, *_ in BLOCKS}
secs = ""; nind = 0
for key, title, what, read, inds in BLOCKS:
    charts, trs = "", ""
    for lbl, vals, d, suf, best, sign, gr in inds:
        nind += 1
        bi = besti(vals, best)
        if bi >= 0: score[key][bi] += 1
        if gr: charts += chart(lbl, vals, d, suf, best, sign)
        trs += f'<tr><th scope="row">{lbl}</th>' + "".join(f'<td class="{"win" if i == bi else ""}">{fmt(v, d, suf, sign)}</td>' for i, v in enumerate(vals)) + "</tr>"
    secs += f'''<section id="{key}" class="cmp-block"><h2 class="h-sec">{title}</h2>
<p class="cmp-what">{what}</p>
<div class="cmp-read"><b>Lectura.</b> {read}</div>
<div class="bcharts">{charts}</div>
<div class="table-scroll"><table class="data cmp-t3">{thead("Indicador")}<tbody>{trs}</tbody></table></div></section>'''

tot = [sum(score[k][i] for k in score) for i in range(K)]
srows = ""
for key, title, *_ in BLOCKS:
    s = score[key]; m = max(s)
    srows += f'<tr><th scope="row"><a href="#{key}">{title}</a></th>' + "".join(f'<td class="{"win" if v == m and m > 0 else ""}">{v}</td>' for v in s) + "</tr>"
m = max(tot)
srows += '<tr class="tot"><th scope="row">Total</th>' + "".join(f'<td class="{"win" if v == m else ""}">{v}</td>' for v in tot) + "</tr>"


facts = [("Perfil", ["Escala y calidad", "Crecimiento", "Valor y dividendo"]),
         ("Países (ABL o ingresos)", ["Chile 62% · Perú 26% · Colombia 12%", "Chile 58% · Perú 25% · Colombia 22%", "Chile 94% · Colombia 3% · Perú 2%"]),
         ("Ingresos 2T26", ["174,1 (+8,7%)", "104,2 (+17,9%)", "99,4 (+9,3%)"]),
         ("EBITDA 2T26", ["140,3 (+9,6%)", "74,7 (+15,8%)", "89,8 aj. (+9,5%)"]),
         ("FFO 2T26", ["~108,5 (+8,8%)", "56,7 (+10,5%)", "72,8 (+13,6%)"]),
         ("Utilidad controladores 2T26", ["234,1 (−44,5%)", "18,4 (−30,8%)", "80,4 (+26,8%)"]),
         ("Revalorización de malls en el 2T", ["216,2 (470,8 en 2T25)", "0 (revaloriza en diciembre)", "35,0 (26,9 en 2T25)"]),
         ("Ocupación", ["s/d", "96,1% retail", "97,0%"]),
         ("Crecimiento anunciado", ["Plan US$600 MM al 2028; Gran Plaza (Colombia) y 6 Open Plaza", "Cartera US$1.137 MM; capex US$250–300 MM/año", "Más de 100 mil m² en obra; Plaza Central (Bogotá)"]),
         ("Clasificación de riesgo", ["AAA (Feller)", "AA+ (Feller)", "s/d"]),
         ("Precio (2-oct-2026)", ["$3.589", "$3.640", "$2.240"])]
frows = "".join(f'<tr><th scope="row">{a}</th>' + "".join(f'<td class="txt">{v}</td>' for v in vs) + "</tr>" for a, vs in facts)

vids = [("pVY2wAaedu8", "Mall Plaza 2T 2026"), ("XXTSTOPBMGY", "Parque Arauco 2T 2026"), ("MlyDIDtxRtc", "Cencosud Shopping 2T 2026")]
vhtml = "".join(f'<a class="vid" href="https://youtu.be/{v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{t}</span></a>' for v, t in vids)

TITLE = "Centros comerciales: Mall Plaza, Parque Arauco y Cencosud Shopping"
SHORT = "Centros comerciales"
LEDE = "Los tres grandes dueños de malls de Chile. En el segundo trimestre de 2026 los tres subieron sus rentas entre 9% y 18% con márgenes muy altos. Parque Arauco es la que más crece, Mall Plaza la más grande y con mejor clasificación de riesgo, y Cencosud Shopping la más barata y con mayor dividendo."
PERIOD = '<div class="period"><span class="period-tag">2T 2026</span><p><b>Período analizado: segundo trimestre de 2026 (abril a junio).</b> Este comparador se actualiza cada trimestre.</p></div>'

tpl = rd("comparadores/energia/index.html")
head, rest_ = tpl.split('<main class="wrap">', 1)
_, foot = rest_.split("</main>", 1)
head = re.sub(r"<title>.*?</title>", f"<title>{SHORT} · AI ACCIONES CHILE</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Comparador de Mall Plaza, Parque Arauco y Cencosud Shopping con los resultados del 2T 2026: valoración, márgenes, deuda, crecimiento y dividendos.">', head)
chips = "".join(f'<a href="#{k}">{t}</a>' for k, t, *_ in BLOCKS)
links = " · ".join(f'<a href="../../acciones/{i}/index.html">{nm}</a>' for i, nm in zip(IDS, NAMES))
main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Comparadores</a> / {SHORT}</nav>
<section class="page-head"><p class="eyebrow">Comparador · 2T 2026</p><h1>{TITLE}</h1>{PERIOD}
<p class="lede">{LEDE}</p>
<p class="small">Empresas: {links}</p>
<p class="chips"><a href="#trimestre">El trimestre</a>{chips}<a href="#videos">Videos</a></p><p class="note">Cifras de nuestros videos de resultados 2T 2026 (análisis razonados y estados financieros IFRS a junio de 2026, comunicados de cada empresa, Simply Wall St, Investing y TradingView). Precios al 2 de octubre de 2026. Cifras en miles de millones de pesos salvo indicación. Las definiciones de FFO difieren entre empresas. No es una recomendación de inversión.</p></section>
<section class="cmp-block"><h2 class="h-sec">Resumen por bloque</h2>
<p class="cmp-what">Número de indicadores en que cada empresa tiene el mejor valor, por bloque. El P/E de 12 meses y el ROE son contables (inflados por revalorizaciones en Mall Plaza) y no suman puntos.</p>
<div class="cmp-read"><b>Lectura general.</b> Cencosud Shopping suma más indicadores a favor ({tot[2]}): la más barata, con los mejores márgenes, la menor deuda, el mayor dividendo y la única que creció en utilidad. Parque Arauco ({tot[1]}) gana en crecimiento, pero es la más cara y la más endeudada. Mall Plaza ({tot[0]}) es la más grande, con clasificación AAA y la mayor caja libre. Es un conteo simple, no una recomendación.</div>
<div class="table-scroll"><table class="data cmp-t3 cmp-score">{thead("Bloque")}<tbody>{srows}</tbody></table></div></section>
<section id="trimestre" class="cmp-block"><h2 class="h-sec">El segundo trimestre 2026, lado a lado</h2>
<p class="cmp-what">Cifras reportadas en miles de millones de pesos y variación frente al 2T 2025.</p>
<div class="table-scroll"><table class="data cmp-t3">{thead("Concepto")}<tbody>{frows}</tbody></table></div></section>
{secs}
<section id="videos" class="cmp-block"><h2 class="h-sec">Mira los videos</h2><div class="vids vids-row">{vhtml}</div></section>
<p class="back"><a class="btn ghost" href="../index.html">Ver todos los comparadores</a></p>
</main>'''
wr("comparadores/malls/index.html", head + main + foot)

p = "comparadores/index.html"; t = rd(p)
if "malls/index.html" not in t:
    card = f'<a class="cmp-card" href="malls/index.html"><span class="ct">{TITLE}</span>\n<span class="cd">{LEDE}</span><span class="cm"><b class="period-mini">2T 2026</b> {len(BLOCKS)} bloques · {nind} indicadores · gráficos comparativos · {len(vids)} videos</span></a>'
    t = t.replace('<div class="cmp-cards">', '<div class="cmp-cards">' + card, 1)
    wr(p, t)
p = "assets/styles.css"; t = rd(p)
if ".cmp-t3" not in t:
    t += "\n.cmp-t3 { min-width: 560px; }\n.cmp-t3 td.txt { min-width: 150px; font-size: 14px; }\n.cmp-t3 th:not(:first-child), .cmp-t3 td { width: 26%; }\n"
    wr(p, t)
print(score, tot)
