# Comparador de AFP con las cifras reales 2T 2026 (tabla común de los 4 videos:
# /mnt/project-files/afp-comparacion-2T26/comparacion-2T26.md). Reemplaza el comparador ilustrativo.
# uso: cd fuente && python3 afp.py   (edita site/; reutiliza los gráficos de malls.py)
import os, re
S = os.environ.get("SITE", os.path.abspath("site"))
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)
def n(v, d=1, suf=""):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + suf

T = ["HABITAT", "PROVIDA", "AFPCAPITAL", "PLANVITAL"]
IDS = ["habitat", "provida", "afpcapital", "planvital"]
NAMES = ["AFP Habitat", "AFP Provida", "AFP Capital", "AFP PlanVital"]
N = None
BLOCKS = [
 ("valoracion", "Valoración",
  "Cuánto paga el mercado por las utilidades y el EBITDA de cada AFP, con precios del 15 al 25 de septiembre de 2026. El EBITDA excluye el encaje (la inversión obligatoria de la AFP en sus propios fondos), que es volátil. AFP Capital no cotiza en bolsa. Ojo: Provida y PlanVital casi no transan, así que sus múltiplos son referenciales.",
  "Habitat es la más barata por utilidades (8,1x), muy cerca de PlanVital (8,2x), que es la más barata por EBITDA (7,3x) y la de mayor flujo de caja libre (9,7%). Provida es la más cara (10,6x; 11,9x sin la venta de AFP Génesis), pero paga el dividendo más alto (7,2%). El FCF yield usa períodos distintos: Habitat el 1S 2026 anualizado, Provida el año 2025 y PlanVital los últimos 12 meses.",
  [("P/E 12 meses", [8.1, 10.6, N, 8.2], 1, "x", "min", False, True),
   ("EV/EBITDA sin encaje", [8.5, 10.9, N, 7.3], 1, "x", "min", False, True),
   ("FCF yield", [3.4, 9.0, N, 9.7], 1, "%", "max", False, True),
   ("Dividend Yield", [7.0, 7.2, N, 6.7], 1, "%", "max", False, True)]),
 ("crecimiento", "Crecimiento del trimestre",
  "Cómo cambiaron los ingresos y la utilidad del 2T 2026 frente al 2T 2025. La utilidad sin encaje (calculada por nosotros: ganancia antes de impuestos menos encaje, por 0,73) muestra cómo anduvo el negocio sin el efecto de los mercados.",
  "PlanVital crece más en ingresos (+5,9%) y Provida es la única que cae (−6,5%) por la fuga de afiliados. Provida tiene la mayor alza de utilidad (+41%), pero por la venta de AFP Génesis y el encaje. Sin encaje, solo Habitat sube (+5,2%): en las otras tres el negocio ganó un poco menos que hace un año.",
  [("Ingresos a/a", [4.2, -6.5, 4.5, 5.9], 1, "%", "max", True, True),
   ("Utilidad a/a", [19.6, 41.0, 13.4, 15.4], 1, "%", "max", True, True),
   ("Utilidad sin encaje a/a", [5.2, -5.1, -3.1, -1.3], 1, "%", "max", True, True),
   ("Utilidad 1S 2026 a/a", [9.8, 28.0, -0.9, 4.7], 1, "%", "max", True, False)]),
 ("eficiencia", "Eficiencia y márgenes",
  "Qué parte de los ingresos queda como resultado operacional sin contar el encaje, cuánto cambió frente al 2T 2025 y cuánto crecieron los gastos operativos.",
  "Habitat tiene por lejos el mejor margen (59,7%) y el que menos bajó (−0,5 puntos). Provida es la única que recortó gastos (−5,3%, sobre todo en personal). Capital y PlanVital perdieron cerca de 4 puntos de margen porque sus gastos crecieron entre 13% y 16%, mucho más que sus ingresos.",
  [("Margen operacional sin encaje", [59.7, 48.8, 46.8, 50.9], 1, "%", "max", False, True),
   ("Cambio del margen (puntos)", [-0.5, -1.5, -3.9, -4.1], 1, "", "max", True, True),
   ("Gastos operativos a/a", [5.7, -5.3, 12.6, 15.6], 1, "%", "min", True, True)]),
 ("balance", "Balance y encaje",
  "Caja neta (o deuda neta, con signo negativo) en miles de millones de pesos, y qué parte de la ganancia antes de impuestos vino del encaje. Más encaje significa una utilidad más expuesta a los mercados; ese indicador es descriptivo y no suma puntos.",
  "Provida tiene la mayor caja neta ($114,9 mil MM) y Habitat la única deuda neta, aunque mínima (≈0,1x EBITDA). En Habitat y Capital el encaje explica 46% de la ganancia antes de impuestos; en Provida y PlanVital, cerca de un tercio.",
  [("Caja neta ($ mil MM)", [-20.9, 114.9, 86.7, 54.8], 1, "", "max", True, True),
   ("Encaje / ganancia antes de impuestos", [46, 32, 46, 34], 0, "%", None, False, False)]),
 ("tamano", "Tamaño y comisión",
  "Escala de cada AFP. Son indicadores descriptivos y no suman puntos: una comisión más alta beneficia al accionista pero perjudica al afiliado.",
  "Provida es la más grande en afiliados (2,49 millones) y la que cobra la comisión más alta (1,45%); Habitat tiene los mayores ingresos con una comisión de 1,27%. PlanVital cobra la más baja (1,16%) y por eso tiene los ingresos más bajos, aunque tiene más afiliados que Capital.",
  [("Afiliados (millones)", [1.70, 2.49, 1.41, 1.59], 2, "", None, False, False),
   ("Comisión (jun-2026)", [1.27, 1.45, 1.44, 1.16], 2, "%", None, False, False),
   ("Ingresos 2T 2026 ($ mil MM)", [67.4, 63.6, 55.6, 34.8], 1, "", None, False, True),
   ("Utilidad 2T 2026 ($ mil MM)", [56.0, 57.5, 38.8, 21.9], 1, "", None, False, True)]),
]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "malls.py")).read()
exec(src[src.index("K = len(T)"):src.index("facts = [")])

facts = [("Controlador", ["Cámara Chilena de la Construcción y Prudential (50/50)", "MetLife (más del 90%)", "SURA Asset Management (no cotiza)", "Generali"]),
         ("Ingresos 2T26", ["67,4 (+4,2%)", "63,6 (−6,5%)", "55,6 (+4,5%)", "34,8 (+5,9%)"]),
         ("Rentabilidad del encaje 2T26", ["34,3 (+37%)", "24,4 (+36%)", "23,7 (+36%)", "9,7 (+71%)"]),
         ("Utilidad 2T26", ["56,0 (+19,6%)", "57,5 (+41,0%)", "38,8 (+13,4%)", "21,9 (+15,4%)"]),
         ("Hecho del trimestre", ["Mejor margen del sistema", "Vendió AFP Génesis (Ecuador): ~17 de utilidad", "FCF del semestre +26%", "Gastos +15,6%"]),
         ("Precio usado", ["$1.426,3 (25-sep)", "$5.150 (15-sep)", "No cotiza", "$280 (25-sep)"])]
frows = "".join(f'<tr><th scope="row">{a}</th>' + "".join(f'<td class="txt">{v}</td>' for v in vs) + "</tr>" for a, vs in facts)
vids = [("M7fElTXELSA", "AFP Habitat 2T 2026"), ("q_I5RpNMgyM", "AFP Provida 2T 2026"), ("QPJNFBztng8", "AFP Capital 2T 2026"), ("gs9Qtnt98K0", "AFP PlanVital 2T 2026")]
vhtml = "".join(f'<a class="vid" href="https://youtu.be/{v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{t}</span></a>' for v, t in vids)

TITLE = "AFP: Habitat, Provida, Capital y PlanVital"
SHORT = "AFP"
LEDE = "Las cuatro AFP con resultados públicos que seguimos. Ganan con la comisión sobre el sueldo imponible de sus cotizantes y con el encaje, la inversión obligatoria en sus propios fondos, que hace variar la utilidad con los mercados. En el segundo trimestre de 2026 las cuatro subieron su utilidad gracias al encaje, pero sin él solo Habitat creció."
PERIOD = '<div class="period"><span class="period-tag">2T 2026</span><p><b>Período analizado: segundo trimestre de 2026 (abril a junio).</b> Este comparador se actualiza cada trimestre.</p></div>'

tpl = rd("comparadores/malls/index.html")
head, rest_ = tpl.split('<main class="wrap">', 1)
_, foot = rest_.split("</main>", 1)
head = re.sub(r"<title>.*?</title>", f"<title>{SHORT} · AI ACCIONES CHILE</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Comparador de AFP Habitat, Provida, Capital y PlanVital con los resultados del 2T 2026: valoración, crecimiento, márgenes, encaje y comisiones.">', head)
chips = "".join(f'<a href="#{k}">{t}</a>' for k, t, *_ in BLOCKS)
links = " · ".join(f'<a href="../../acciones/{i}/index.html">{nm}</a>' for i, nm in zip(IDS, NAMES))
order = sorted(range(K), key=lambda i: -tot[i])
main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Comparadores</a> / {SHORT}</nav>
<section class="page-head"><p class="eyebrow">Comparador · 2T 2026</p><h1>{TITLE}</h1>{PERIOD}
<p class="lede">{LEDE}</p>
<p class="small">Empresas: {links}</p>
<p class="chips"><a href="#trimestre">El trimestre</a>{chips}<a href="#videos">Videos</a></p><p class="note">Cifras de nuestros videos de resultados 2T 2026: estados financieros de cada AFP publicados por la Superintendencia de Pensiones (junio de 2026 y diciembre de 2025), comisiones de Rankia y precios de MarketScreener, Investing.com y Bolsamanía. Cifras en miles de millones de pesos salvo indicación. No es una recomendación de inversión.</p></section>
<section class="cmp-block"><h2 class="h-sec">Resumen por bloque</h2>
<p class="cmp-what">Número de indicadores en que cada AFP tiene el mejor valor, por bloque. Los indicadores descriptivos (tamaño, comisión y peso del encaje) no suman puntos. AFP Capital no cotiza, así que no compite en valoración.</p>
<div class="cmp-read"><b>Lectura general.</b> {T[order[0]]} suma más indicadores a favor ({tot[order[0]]}), seguida de {T[order[1]]} ({tot[order[1]]}). Habitat destaca por eficiencia y por ser la única que creció sin el encaje; PlanVital por valoración y crecimiento de ingresos; Provida por caja y dividendo, aunque pierde afiliados. Es un conteo simple, no una recomendación.</div>
<div class="table-scroll"><table class="data cmp-t4 cmp-score">{thead("Bloque")}<tbody>{srows}</tbody></table></div></section>
<section id="trimestre" class="cmp-block"><h2 class="h-sec">El segundo trimestre 2026, lado a lado</h2>
<p class="cmp-what">Cifras reportadas en miles de millones de pesos y variación frente al 2T 2025.</p>
<div class="table-scroll"><table class="data cmp-t4">{thead("Concepto")}<tbody>{frows}</tbody></table></div></section>
{secs.replace("cmp-t3", "cmp-t4")}
<section id="videos" class="cmp-block"><h2 class="h-sec">Mira los videos</h2><div class="vids vids-row">{vhtml}</div></section>
<p class="back"><a class="btn ghost" href="../index.html">Ver todos los comparadores</a></p>
</main>'''
wr("comparadores/afp/index.html", head + main + foot)

p = "comparadores/index.html"; t = rd(p)
card = f'<a class="cmp-card" href="afp/index.html"><span class="ct">{TITLE}</span>\n<span class="cd">{LEDE}</span><span class="cm"><b class="period-mini">2T 2026</b> {len(BLOCKS)} bloques · {nind} indicadores · gráficos comparativos · {len(vids)} videos</span></a>'
t = re.sub(r'<a class="cmp-card" href="afp/index\.html">.*?</a>', lambda _: card, t, count=1, flags=re.S)
wr(p, t)
print(score, tot)
