import os, re
S = "site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t): open(os.path.join(S, p), "w", encoding="utf-8").write(t)
ICMP = ["afp", "aguas-iam", "bancos", "cap-cmpc", "chile-santander", "sqm-oroblanco"]
IFICHAS = ["afpcapital","andina-a","bci","besalco","bsantander","cap","chile","cmpc","copec","habitat","iam","itau","planvital","provida","schwager","sqm-b"]
TK = {"itau": "ITAUCL"}
BOX = lambda txt: f'<div class="period illus"><span class="period-tag">Ilustrativo</span><p>{txt}</p></div>'
OLD_PAGE = '<div class="period"><span class="period-tag">2T 2026</span><p><b>Período analizado: segundo trimestre de 2026 (abril a junio).</b> Este comparador se actualiza cada trimestre.</p></div>'
# comparadores ilustrativos
for d in ICMP:
    p = f"comparadores/{d}/index.html"; t = rd(p)
    t = t.replace(OLD_PAGE, BOX("<b>Datos ilustrativos, no oficiales.</b> Las cifras de este comparador son de ejemplo para mostrar cómo se comparan las empresas; no corresponden a resultados reales. Lo actualizaremos con cifras reales en un próximo trimestre."))
    t = t.replace('<p class="eyebrow">Comparador · 2T 2026</p>', '<p class="eyebrow">Comparador · datos ilustrativos</p>')
    wr(p, t)
p = "comparadores/index.html"; t = rd(p)
for d in ICMP:
    t = re.sub(r'(<a class="cmp-card" href="' + d + r'/index\.html">.*?<span class="cm">)<b class="period-mini">2T 2026</b>', r'\1<b class="period-mini illus-mini">Ilustrativo</b>', t, count=1, flags=re.S)
t = t.replace("Hacemos estos comparadores cada trimestre: cuando salgan los resultados del 3T 2026 los actualizaremos.",
  "Hacemos estos comparadores cada trimestre: cuando salgan los resultados del 3T 2026 los actualizaremos. Los comparadores marcados como <b>Ilustrativo</b> usan datos de ejemplo, no oficiales.")
wr(p, t)
# fichas ilustrativas
for f in IFICHAS:
    p = f"acciones/{f}/index.html"; t = rd(p)
    if "period illus" in t: continue
    t = t.replace("</section>\n<section><h2 class=\"h-sec\">Valoración</h2>", "</section>\n" + BOX("<b>Datos ilustrativos, no oficiales.</b> El precio, los múltiplos y los resultados de esta ficha son de ejemplo; no corresponden a cifras reales. Para datos oficiales revisa los estados financieros en la CMF.") + "\n<section><h2 class=\"h-sec\">Valoración</h2>", 1)
    assert "period illus" in t, f
    wr(p, t)
# páginas de listado
lst = ", ".join(TK.get(f, f.upper()) for f in IFICHAS)
LBOX = BOX(f"<b>Algunas empresas tienen datos ilustrativos, no oficiales:</b> {lst} y ORO BLANCO. Sus cifras son de ejemplo. Las demás usan los resultados reales del 2T 2026 de nuestros videos.")
for p in ["acciones/index.html", "valoraciones/index.html", "rankings/index.html", "resultados/index.html"]:
    t = rd(p)
    if "period illus" in t: continue
    t, k = re.subn(r'(<section class="page-head">.*?</section>)', lambda m: m.group(1) + LBOX, t, count=1, flags=re.S)
    print(p, k); wr(p, t)
p = "assets/styles.css"; t = rd(p)
if ".period.illus" not in t:
    t += ".period.illus { border-left-color: #d9982b; background: rgba(217,152,43,.10); }\n.period.illus .period-tag, .illus-mini { background: #d9982b; color: #1a1a1a; }\n"
    wr(p, t)
