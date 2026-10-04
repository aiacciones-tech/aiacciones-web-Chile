import os, re
S = "/tmp/claude-0/-home-claude/51bbcb85-f720-5650-9a37-2f75843c73b7/scratchpad/site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)

def n(v, d=1, suf=""):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + suf

T = ["FALABELLA", "RIPLEY", "CENCOSUD"]
IDS = ["falabella", "ripley", "cencosud"]
NAMES = ["Falabella", "Ripley Corp", "Cencosud"]

# (indicador, valores, decimales, sufijo, mejor: "min"|"max"|None, signo+, grafico)
BLOCKS = [
 ("valoracion", "Valoración",
  "Cuánto paga el mercado por las utilidades, el patrimonio y el EBITDA de cada empresa. El EV/EBITDA usa la misma fuente para las tres (StockAnalysis) e incluye la deuda de sus bancos, por eso difiere de las cifras de cada video.",
  "Ripley es la más barata en casi todo: P/E de 7,2x y transa bajo su valor libro (0,74x). Cencosud tiene un P/E de 34x porque su utilidad de 12 meses se desplomó; mirando la utilidad esperada (forward) baja a 12,7x. Falabella es la más cara por forward P/E (16,4x), un premio que el mercado le da por el crecimiento de su banco.",
  [("P/E (12 meses)", [11.9, 7.2, 34.3], 1, "x", "min", False, True),
   ("Forward P/E", [16.4, 9.3, 12.7], 1, "x", "min", False, True),
   ("P/BV", [1.48, 0.74, 1.00], 2, "x", "min", False, False),
   ("EV/EBITDA (misma fuente)", [10.7, 14.8, 10.4], 1, "x", "min", False, False),
   ("FCF yield", [8.2, 7.8, 7.1], 1, "%", "max", False, True)]),
 ("rentabilidad", "Rentabilidad y márgenes",
  "Cuánto rinde el capital de los accionistas y qué parte de cada peso vendido queda como ganancia. Márgenes del segundo trimestre 2026.",
  "Falabella gana en todos los indicadores: su margen EBITDA (14,5%) casi duplica el de Ripley y Cencosud, gracias al banco y a Mallplaza. Cencosud tiene el margen bruto más bajo por su peso en supermercados y la guerra de promociones en Chile.",
  [("ROE", [19.0, 10.9, 4.6], 1, "%", "max", False, True),
   ("Margen bruto 2T26", [38.3, 35.7, 28.8], 1, "%", "max", False, False),
   ("Margen EBITDA 2T26", [14.5, 7.8, 7.5], 1, "%", "max", False, True),
   ("Margen operacional 2T26", [11.2, 4.5, 3.9], 1, "%", "max", False, False)]),
 ("deuda", "Deuda y solvencia",
  "Cuántos años de EBITDA tomaría pagar la deuda neta. Se excluye la deuda de los bancos, que es su materia prima. Cencosud incluye arriendos. El cambio del ratio es a un año (Cencosud: frente a dic-2025).",
  "Falabella es la menos endeudada (1,29x) y bajó desde 1,94x en un año. Ripley mejoró desde 4,97x pero sigue sobre 4x; Cencosud subió a 3,6x tras comprar el centro comercial Plaza Central y con deuda en UF.",
  [("Deuda neta / EBITDA", [1.29, 4.28, 3.6], 2, "x", "min", False, True),
   ("Cambio del ratio", [-0.65, -0.69, 0.5], 2, "x", "min", True, False)]),
 ("crecimiento", "Crecimiento y sorpresa del trimestre",
  "Cómo evolucionaron las ventas y el EBITDA frente al 2T 2025, y cuánto se alejó la utilidad por acción de lo que esperaban los analistas (consenso Investing.com).",
  "Falabella creció más en ventas (+9,7%) y fue la única con EBITDA al alza. Ripley superó al consenso (+10%), pero con ayuda de una revalorización de Mall Aventura; su EBITDA cayó 10,5%. Cencosud decepcionó: ventas −1,8%, EBITDA −15,8% y una utilidad por acción muy por debajo de lo esperado.",
  [("Ingresos a/a", [9.7, 5.8, -1.8], 1, "%", "max", True, True),
   ("EBITDA a/a", [7.0, -10.5, -15.8], 1, "%", "max", True, True),
   ("BPA vs. consenso", [31.0, 10.0, -97.0], 0, "%", "max", True, False)]),
 ("dividendos", "Dividendos",
  "Dividendos pagados en 12 meses sobre el precio (para Cencosud, el esperado para 2026).",
  "Ninguna es una acción de dividendos: todas rinden menos de 3%. Ripley paga algo más en proporción a su precio.",
  [("Dividend Yield", [2.5, 2.9, 1.4], 1, "%", "max", False, True)]),
 ("mercado", "Mercado",
  "Cómo se ha movido la acción y cuánto potencial ven los analistas según su precio objetivo promedio.",
  "Falabella es la única que sube en 12 meses (+12%). Cencosud es la que más cae (−26%) y, por lo mismo, la que tiene más espacio frente al precio objetivo de los analistas (+39%), aunque solo 2 de 13 recomiendan comprar.",
  [("Var. precio 12m", [12, -11, -26], 0, "%", "max", True, True),
   ("Potencial al precio objetivo", [7.7, 3.0, 39.0], 1, "%", "max", True, True),
   ("Beta (5 años)", [0.52, 0.35, 0.09], 2, "", None, False, False)]),
]

def fmt(v, d, suf, sign): return ("+" if sign and v > 0 else "") + n(v, d, suf)

def chart(lbl, vals, d, suf, best, sign):
    lo, hi = min(0, min(vals)), max(0, max(vals))
    sc = 176 / (hi - lo); x0 = 92 + (-lo) * sc
    bi = (vals.index(min(vals)) if best == "min" else vals.index(max(vals))) if best else -1
    aria = ", ".join(f"{t} {fmt(v, d, suf, sign)}" for t, v in zip(T, vals))
    out = f'<figure class="bchart"><figcaption>{lbl}<span>{" · menor es mejor" if best == "min" else (" · mayor es mejor" if best == "max" else "")}</span></figcaption><svg viewBox="0 0 320 86" role="img" aria-label="{lbl}: {aria}">'
    for i, (t, v) in enumerate(zip(T, vals)):
        y = 8 + 26 * i; w = max(abs(v) * sc, 1.5)
        x = x0 if v >= 0 else x0 - w
        tx = x0 + w + 6 if v >= 0 else x0 + 6
        col = "#3b86e6" if i == bi else "#5a5a57"
        out += f'<text x="84" y="{y+11}" text-anchor="end" class="bl">{t}</text><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="16" rx="2" fill="{col}"/><text x="{tx:.1f}" y="{y+11}" class="bv{" best" if i == bi else ""}">{fmt(v, d, suf, sign)}</text>'
    out += f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="2" y2="84" class="b0"/></svg></figure>'
    return out

def thead(first): return f'<thead><tr><th scope="col">{first}</th>' + "".join(f'<th scope="col">{t}</th>' for t in T) + "</tr></thead>"

score = {k: [0, 0, 0] for k, *_ in BLOCKS}
secs = ""
for key, title, what, read, inds in BLOCKS:
    charts, trs = "", ""
    for lbl, vals, d, suf, best, sign, gr in inds:
        bi = (vals.index(min(vals)) if best == "min" else vals.index(max(vals))) if best else -1
        if bi >= 0: score[key][bi] += 1
        if gr: charts += chart(lbl, vals, d, suf, best, sign)
        trs += f'<tr><th scope="row">{lbl}</th>' + "".join(f'<td class="{"win" if i == bi else ""}">{fmt(v, d, suf, sign)}</td>' for i, v in enumerate(vals)) + "</tr>"
    secs += f'''<section id="{key}" class="cmp-block"><h2 class="h-sec">{title}</h2>
<p class="cmp-what">{what}</p>
<div class="cmp-read"><b>Lectura.</b> {read}</div>
<div class="bcharts">{charts}</div>
<div class="table-scroll"><table class="data cmp-t3">{thead("Indicador")}<tbody>{trs}</tbody></table></div></section>'''

tot = [sum(score[k][i] for k in score) for i in range(3)]
srows = ""
for key, title, *_ in BLOCKS:
    s = score[key]; m = max(s)
    srows += f'<tr><th scope="row"><a href="#{key}">{title}</a></th>' + "".join(f'<td class="{"win" if v == m and m > 0 else ""}">{v}</td>' for v in s) + "</tr>"
m = max(tot)
srows += '<tr class="tot"><th scope="row">Total</th>' + "".join(f'<td class="{"win" if v == m else ""}">{v}</td>' for v in tot) + "</tr>"

# resumen 2T26 lado a lado
facts = [("Ingresos 2T26 (CLP mil MM)", ["3.486,5", "564,1", "4.094,7"]),
         ("EBITDA 2T26 (CLP mil MM)", ["506,0", "43,9", "307,9"]),
         ("Utilidad controladora 2T26", ["304,3 (−16,5%)", "25,1 (+58,7%)", "−36,5 (vs. +86,5)"]),
         ("Motor del trimestre", ["Banco Falabella", "Perú", "Centros comerciales y online"]),
         ("Punto débil", ["Sodimac y retail Chile", "Retail Chile", "Supermercados Chile"]),
         ("Precio usado en el video", ["$6.299", "$455", "$1.949"])]
frows = "".join(f'<tr><th scope="row">{a}</th>' + "".join(f'<td>{v}</td>' for v in vs) + "</tr>" for a, vs in facts)

vids = [("AOdMbPxaeUI", "Falabella 2T 2026"), ("bbKGplfrAQw", "Ripley 2T 2026"), ("WJ2OGQfcN4w", "Cencosud 2T 2026")]
vhtml = "".join(f'<a class="vid" href="https://youtu.be/{v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{t}</span></a>' for v, t in vids)

TITLE = "Retail: Falabella vs. Ripley vs. Cencosud"
LEDE = "Los tres grandes del retail chileno. Los tres tienen tiendas, bancos o tarjetas y centros comerciales, pero con mezclas distintas: Falabella depende cada vez más de su banco y de Mallplaza, Ripley de Perú y Cencosud de los supermercados en seis países. En el segundo trimestre de 2026 los tres sufrieron en Chile por promociones y menor consumo."

tpl = rd("comparadores/afp/index.html")
head, rest = tpl.split('<main class="wrap">', 1)
_, foot = rest.split("</main>", 1)
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} · AI ACCIONES CHILE</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="Comparador de Falabella, Ripley y Cencosud con los resultados del 2T 2026: valoración, márgenes, deuda, crecimiento y dividendos.">', head)

chips = "".join(f'<a href="#{k}">{t}</a>' for k, t, *_ in BLOCKS)
main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Comparadores</a> / {TITLE}</nav>
<section class="page-head"><p class="eyebrow">Comparador</p><h1>{TITLE}</h1>
<p class="lede">{LEDE}</p>
<p class="small">Empresas: <a href="../../acciones/falabella/index.html">Falabella</a> · <a href="../../acciones/ripley/index.html">Ripley Corp</a> · <a href="../../acciones/cencosud/index.html">Cencosud</a></p>
<p class="chips"><a href="#trimestre">El trimestre</a>{chips}<a href="#videos">Videos</a></p><p class="note">Cifras de nuestros videos de resultados 2T 2026 (estados financieros y análisis razonado). P/BV, ROE, EV/EBITDA comparable, beta y variación 12 meses: StockAnalysis, septiembre 2026. No es una recomendación de inversión.</p></section>
<section class="cmp-block"><h2 class="h-sec">Resumen por bloque</h2>
<p class="cmp-what">Número de indicadores en que cada empresa tiene el mejor valor, por bloque. La beta es descriptiva y no suma puntos.</p>
<div class="cmp-read"><b>Lectura general.</b> Falabella suma más indicadores a favor ({tot[0]}): mejores márgenes, menos deuda y el mayor crecimiento. Ripley ({tot[1]}) es la más barata por múltiplos, con un negocio en Chile debilitado. Cencosud ({tot[2]}) viene del trimestre más difícil, y por eso es la que más espacio tiene frente al precio objetivo de los analistas. Es un conteo simple, no una recomendación: una acción barata puede estarlo por un riesgo mayor.</div>
<div class="table-scroll"><table class="data cmp-t3 cmp-score">{thead("Bloque")}<tbody>{srows}</tbody></table></div></section>
<section id="trimestre" class="cmp-block"><h2 class="h-sec">El segundo trimestre 2026, lado a lado</h2>
<p class="cmp-what">Cifras reportadas en pesos chilenos. Cencosud reporta con NIC 29 (hiperinflación en Argentina).</p>
<div class="table-scroll"><table class="data cmp-t3">{thead("Concepto")}<tbody>{frows}</tbody></table></div></section>
{secs}
<section id="videos" class="cmp-block"><h2 class="h-sec">Mira los videos</h2><div class="vids vids-row">{vhtml}</div></section>
<p class="back"><a class="btn ghost" href="../index.html">Ver todos los comparadores</a></p>
</main>'''
wr("comparadores/retail/index.html", head + main + foot)

# tarjeta en el índice de comparadores (primera)
p = "comparadores/index.html"; t = rd(p)
if "retail/index.html" not in t:
    card = f'<a class="cmp-card" href="retail/index.html"><span class="ct">{TITLE}</span>\n<span class="cd">{LEDE}</span><span class="cm">6 bloques · 18 indicadores · gráficos comparativos · 3 videos</span></a>'
    t = t.replace('<div class="cmp-cards">', '<div class="cmp-cards">' + card, 1)
    wr(p, t)

# CSS para tablas de 3 columnas y fila de videos
p = "assets/styles.css"; t = rd(p)
if ".cmp-t3" not in t:
    t += "\n.cmp-t3 th:not(:first-child), .cmp-t3 td { width: 22%; }\n.vids-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }\n"
    wr(p, t)
print(score, tot)
