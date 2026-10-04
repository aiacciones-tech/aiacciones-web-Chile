import os, re
S = "/tmp/claude-0/-home-claude/51bbcb85-f720-5650-9a37-2f75843c73b7/scratchpad/site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)
def n(v, d=1, suf=""):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + suf

T = ["COLBUN", "ECL", "AES ANDES", "CGE", "ENELCHILE", "ENELGXCH"]
IDS = ["colbun", "ecl", "aes-andes", "cge", "enelchile", "enelgxch"]
NAMES = ["Colbún", "Engie Energía Chile", "AES Andes", "CGE", "Enel Chile", "Enel Generación Chile"]
N = None
BLOCKS = [
 ("valoracion", "Valoración",
  "Cuánto paga el mercado por las utilidades, el patrimonio, el EBITDA y la caja de cada empresa. AES Andes no cotiza en bolsa, así que no tiene múltiplos de mercado (en su ficha está su valor estimado con los múltiplos de estos pares). El FCF yield es el del primer semestre anualizado.",
  "Engie es la más barata por utilidades (P/E de 8,3x y forward de 6,6x) y tiene el FCF yield más alto. Enel Generación es la más barata por EV/EBITDA (5,9x), pero su P/BV es el más alto. Colbún es la más cara por P/E (22,5x) porque su utilidad de 12 meses cayó; con la utilidad que espera el consenso baja a ~12x. CGE transa a 0,29 veces su valor libro, pero con flujo de caja negativo.",
  [("P/E (12 meses)", [22.5, 8.3, N, 13.6, 10.4, 9.1], 1, "x", "min", False, True),
   ("Forward P/E", [12.0, 6.6, N, N, 9.3, 10.0], 1, "x", "min", False, True),
   ("EV/EBITDA (12 meses)", [7.3, 6.2, N, 9.3, 6.5, 5.9], 1, "x", "min", False, True),
   ("P/BV", [0.82, 1.11, N, 0.29, 1.08, 1.84], 2, "x", "min", False, False),
   ("FCF yield", [11.0, 12.3, N, -11.1, 10.7, 10.2], 1, "%", "max", False, True)]),
 ("rentabilidad", "Rentabilidad y márgenes",
  "Cuánto rinde el capital de los accionistas y qué parte de cada dólar vendido queda como EBITDA o resultado operacional en el segundo trimestre 2026. CGE es distribuidora: compra la energía y la revende, por eso sus márgenes son estructuralmente más bajos que los de las generadoras.",
  "Engie, Colbún y AES Andes tienen márgenes EBITDA parecidos, cerca de 35%. Enel Generación tiene el mejor ROE (20,4%) pese a un margen más bajo, porque casi no tiene deuda y reparte mucho. Colbún y CGE tienen ROE bajos (3,5% y 2,2%).",
  [("ROE", [3.5, 15.2, N, 2.2, 11.0, 20.4], 1, "%", "max", False, True),
   ("Margen EBITDA 2T26", [34.9, 35.4, 34.5, 8.9, 24.5, 19.3], 1, "%", "max", False, True),
   ("Margen operacional 2T26", [19.9, 26.8, 24.0, 4.8, 17.4, 20.6], 1, "%", "max", False, False)]),
 ("deuda", "Deuda y solvencia",
  "Cuántos años de EBITDA tomaría pagar la deuda neta, con EBITDA de los últimos 12 meses a junio de 2026.",
  "Enel Generación casi no tiene deuda (0,3x). Enel Chile (2,3x) y Colbún (2,8x) están en un nivel cómodo, aunque Colbún subió desde 2,3x. Engie y AES Andes rondan 3,3–3,5x por sus planes de inversión. CGE es el caso más exigido: 6,8x, con 44% de la deuda a corto plazo.",
  [("Deuda neta / EBITDA", [2.8, 3.53, 3.3, 6.79, 2.3, 0.3], 1, "x", "min", False, True)]),
 ("crecimiento", "Crecimiento y sorpresa del trimestre",
  "Cómo evolucionaron las ventas, el EBITDA y la utilidad frente al 2T 2025, y cuánto se alejó la utilidad por acción de lo que esperaban los analistas. AES Andes, CGE y Enel Generación no tienen consenso publicado.",
  "AES Andes fue la que más creció (EBITDA +38%) gracias a la sequía y los altos precios en Colombia. En Chile el año seco golpeó a las generadoras con más agua: Enel Generación (EBITDA −23%) y Enel Chile (−11%). Colbún subió su EBITDA 12% vendiendo en el mercado spot, pero su utilidad cayó 24%. Engie fue la gran sorpresa positiva frente al consenso (+36%).",
  [("Ingresos a/a", [11.6, -10.4, 27.1, -2.5, -9.0, -13.4], 1, "%", "max", True, True),
   ("EBITDA a/a", [11.6, -8.6, 38.4, 13.4, -10.9, -22.7], 1, "%", "max", True, True),
   ("Utilidad a/a", [-24.0, -19.6, 417.0, 141.0, 54.2, 0.0], 0, "%", "max", True, False),
   ("EPS vs. consenso", [-16.0, 36.5, N, N, -2.0, N], 0, "%", "max", True, False)]),
 ("dividendos", "Dividendos",
  "Dividendos pagados en 12 meses sobre el precio de la acción.",
  "Enel Generación paga el mayor dividendo (6,9%), aunque viene bajando desde 11% en 2025. Enel Chile (4,3%) y Colbún (3,9%) le siguen; CGE casi no reparte (~1%) por su deuda.",
  [("Dividend Yield", [3.9, 3.2, N, 1.0, 4.3, 6.9], 1, "%", "max", False, True)]),
 ("mercado", "Mercado",
  "Cómo se ha movido la acción en 12 meses y cuánto potencial ven los analistas según su precio objetivo.",
  "Engie (+36%), Enel Generación (+30%) y Enel Chile (+26%) subieron fuerte en el año; Colbún quedó plana y CGE cae 27%. Enel Chile es la que más potencial tiene al precio objetivo (+12%). Todas tienen betas muy bajas: se mueven poco con el mercado.",
  [("Var. precio 12m", [-3.8, 36.0, N, -27.1, 26.0, 29.7], 0, "%", "max", True, True),
   ("Potencial al precio objetivo", [7.0, 4.8, N, N, 11.7, N], 1, "%", "max", True, False),
   ("Beta (5 años)", [0.06, 0.32, N, 0.18, 0.44, 0.57], 2, "", None, False, False)]),
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
<div class="table-scroll"><table class="data cmp-t6">{thead("Indicador")}<tbody>{trs}</tbody></table></div></section>'''

tot = [sum(score[k][i] for k in score) for i in range(K)]
srows = ""
for key, title, *_ in BLOCKS:
    s = score[key]; m = max(s)
    srows += f'<tr><th scope="row"><a href="#{key}">{title}</a></th>' + "".join(f'<td class="{"win" if v == m and m > 0 else ""}">{v}</td>' for v in s) + "</tr>"
m = max(tot)
srows += '<tr class="tot"><th scope="row">Total</th>' + "".join(f'<td class="{"win" if v == m else ""}">{v}</td>' for v in tot) + "</tr>"

facts = [("Negocio", ["Generación Chile y Perú", "Generación y transmisión, norte de Chile", "Generación Chile, Colombia y Argentina", "Distribución eléctrica", "Generación y distribución", "Generación (filial de Enel Chile)"]),
         ("Moneda", ["US$ MM", "US$ MM", "US$ MM", "CLP mil MM", "US$ MM", "US$ MM"]),
         ("Ingresos 2T26", ["449,2", "521,6", "633,4", "593,3", "1.071", "693"]),
         ("EBITDA 2T26", ["156,9", "184,6", "218,6", "52,8", "262", "134"]),
         ("Utilidad 2T26", ["36,6 (−24%)", "86,6 (−20%)", "107,1 (+417%)", "7,4 (+141%)", "110 (+54%)", "106 (0%)"]),
         ("Motor del trimestre", ["Ventas spot y Perú", "Ventas a clientes regulados (+21%)", "Colombia (sequía y precios spot)", "Menos incobrables y multas", "Reversión de deterioro (Bocamina II)", "Reversión de deterioro (Bocamina II)"]),
         ("Punto débil", ["Hidro −21% y costo de salir del carbón", "Base alta por el arbitraje de GNL", "Dependencia de Colombia", "Deuda de 6,8x y liquidez casi nula", "Hidrología (generación −7,5%)", "Hidrología (generación −15,9%)"]),
         ("Precio usado en el video", ["$146,18", "$1.847", "No cotiza", "$215,1", "$81,35", "$594,74"])]
frows = "".join(f'<tr><th scope="row">{a}</th>' + "".join(f'<td class="txt">{v}</td>' for v in vs) + "</tr>" for a, vs in facts)

vids = [("GhovLULVg08", "Colbún 2T 2026"), ("xrTDtUxANNI", "Engie Energía Chile 2T 2026"), ("EnQHavuXcrY", "AES Andes 2T 2026"), ("Rmt5ooXcaG4", "Enel Generación Chile 2T 2026")]
vhtml = "".join(f'<a class="vid" href="https://youtu.be/{v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{t}</span></a>' for v, t in vids)

TITLE = "Empresas de energía: Colbún, Engie, AES Andes, CGE, Enel Chile y Enel Generación"
SHORT = "Empresas de energía"
LEDE = "Cinco generadoras y una distribuidora. En el segundo trimestre de 2026 el año seco marcó la diferencia: las que dependen más del agua en Chile (Enel Generación, Enel Chile) vieron caer su EBITDA, mientras AES Andes creció por Colombia y Colbún compensó vendiendo en el mercado spot. CGE, la distribuidora, tiene un negocio regulado distinto y la deuda más alta."

tpl = rd("comparadores/retail/index.html")
head, rest = tpl.split('<main class="wrap">', 1)
_, foot = rest.split("</main>", 1)
head = re.sub(r"<title>.*?</title>", f"<title>{SHORT} · AI ACCIONES CHILE</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Comparador de Colbún, Engie Energía Chile, AES Andes, CGE, Enel Chile y Enel Generación con los resultados del 2T 2026: valoración, márgenes, deuda, crecimiento y dividendos.">', head)
chips = "".join(f'<a href="#{k}">{t}</a>' for k, t, *_ in BLOCKS)
links = " · ".join(f'<a href="../../acciones/{i}/index.html">{nm}</a>' for i, nm in zip(IDS, NAMES))
ranked = sorted(range(K), key=lambda i: -tot[i])
main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Comparadores</a> / {SHORT}</nav>
<section class="page-head"><p class="eyebrow">Comparador</p><h1>{TITLE}</h1>
<p class="lede">{LEDE}</p>
<p class="small">Empresas: {links}</p>
<p class="chips"><a href="#trimestre">El trimestre</a>{chips}<a href="#videos">Videos</a></p><p class="note">Cifras de nuestros videos de resultados 2T 2026 (estados financieros, análisis razonado y reportes de cada empresa). P/BV, ROE, beta y variación 12 meses de Enel Chile: StockAnalysis, septiembre 2026. No es una recomendación de inversión.</p></section>
<section class="cmp-block"><h2 class="h-sec">Resumen por bloque</h2>
<p class="cmp-what">Número de indicadores en que cada empresa tiene el mejor valor, por bloque. La beta es descriptiva y no suma puntos. AES Andes no cotiza, por lo que solo compite en márgenes, deuda y crecimiento.</p>
<div class="cmp-read"><b>Lectura general.</b> Engie suma más indicadores a favor ({tot[1]}): la más barata por utilidades, el mejor FCF yield y margen, y la mayor sorpresa frente al consenso. Enel Generación ({tot[5]}) destaca por deuda casi nula, el mejor ROE y el mayor dividendo, aunque fue la más golpeada por la sequía. AES Andes ({tot[2]}) tuvo el mejor trimestre por crecimiento. CGE es barata frente a su patrimonio, pero con mucha deuda y una acción que casi no transa. Es un conteo simple, no una recomendación.</div>
<div class="table-scroll"><table class="data cmp-t6 cmp-score">{thead("Bloque")}<tbody>{srows}</tbody></table></div></section>
<section id="trimestre" class="cmp-block"><h2 class="h-sec">El segundo trimestre 2026, lado a lado</h2>
<p class="cmp-what">Cifras reportadas. Todas reportan en dólares salvo CGE, que reporta en pesos chilenos (miles de millones).</p>
<div class="table-scroll"><table class="data cmp-t6">{thead("Concepto")}<tbody>{frows}</tbody></table></div></section>
{secs}
<section id="videos" class="cmp-block"><h2 class="h-sec">Mira los videos</h2><div class="vids vids-row">{vhtml}</div><p class="small">Los videos de CGE y Enel Chile se publicarán pronto en nuestro canal.</p></section>
<p class="back"><a class="btn ghost" href="../index.html">Ver todos los comparadores</a></p>
</main>'''
wr("comparadores/energia/index.html", head + main + foot)

p = "comparadores/index.html"; t = rd(p)
if "energia/index.html" not in t:
    card = f'<a class="cmp-card" href="energia/index.html"><span class="ct">{TITLE}</span>\n<span class="cd">{LEDE}</span><span class="cm">{len(BLOCKS)} bloques · {nind} indicadores · gráficos comparativos · {len(vids)} videos</span></a>'
    t = t.replace('<div class="cmp-cards">', '<div class="cmp-cards">' + card, 1)
    wr(p, t)
p = "assets/styles.css"; t = rd(p)
if ".cmp-t6" not in t:
    t += "\n.cmp-t6 { min-width: 720px; }\n.cmp-t6 td.txt { min-width: 110px; font-size: 14px; }\n.cmp-t6 th:not(:first-child), .cmp-t6 td { width: 13%; }\n"
    wr(p, t)
print(score, tot)
