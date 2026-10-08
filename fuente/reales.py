# AdSense (oct-2026): saca del sitio todo lo que tenía cifras de ejemplo.
# - 10 fichas pasan a cifras reales 2T 2026 (d_reales.py, de los guiones de cada video)
# - 6 fichas sin video (BCI, BSANTANDER, ITAUCL, CAP, SCHWAGER, SQM-B) y 5 comparadores ilustrativos salen del sitio
#   (build_web.sh deja en su URL una página noindex que lleva a la sección; ver RETIRADOS)
# - cinta, chips, listados, rankings, resultados, portada y pie sin menciones a datos ilustrativos
# uso: cd fuente && python3 reales.py   (edita site/; después ./build_web.sh)
import os, re, json, shutil
src = open("energy.py").read().split("old = re.findall")[0]
exec(src)
exec(open("d_reales.py").read())
ROOT = os.path.dirname(os.path.abspath(__file__))
ACC = json.load(open(os.path.join(ROOT, "..", "web", "assets", "mercado.json"), encoding="utf-8"))["acciones"]

RETIRADOS_F = ["bci", "bsantander", "itau", "cap", "schwager", "sqm-b"]
RETIRADOS_C = ["bancos", "cap-cmpc", "chile-santander", "aguas-iam", "sqm-oroblanco"]
AFP = {"habitat", "provida", "afpcapital", "planvital"}
RID = {c["id"]: c for c in R}
for c in R:
    for lbl, v in c["var"].items():
        VAROV[(c["id"], lbl)] = v

NOTE = '<p class="note">Cifras de nuestro video de resultados 2T 2026 (estados financieros, análisis razonado y reportes de la empresa; AFP: estados financieros publicados por la Superintendencia de Pensiones). (c) = cifra calculada por nosotros. No es una recomendación de inversión.</p>'
AFP_LINK = '<p class="small">Compárala con las otras AFP en el <a href="../../comparadores/afp/index.html">comparador de AFP</a>.</p>'
CAL_LINK = '<p class="small">Su próximo reporte (3T 2026) está en el <a href="../../calendario/index.html">calendario de resultados</a>.</p>'

# ---------- orden de las fichas (el del listado), sin las retiradas
lst = rd("acciones/index.html")
ROWS = re.findall(r'<tr><th scope="row"><a href="([\w-]+)/index\.html">([^<]+)</a></th>.*?</tr>', lst)
ORDER = [(i, t) for i, t in ROWS if i not in RETIRADOS_F]
TK = dict(ORDER)

# ---------- borrar fichas y comparadores retirados
for d in RETIRADOS_F:
    shutil.rmtree(os.path.join(S, "acciones", d), ignore_errors=True)
for d in RETIRADOS_C:
    shutil.rmtree(os.path.join(S, "comparadores", d), ignore_errors=True)

# ---------- las 10 fichas con cifras reales
def chips_for(fid):
    return "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in ORDER if i != fid)
for c in R:
    h = ficha(c).replace(f"CHIPS_{c['id']}", chips_for(c["id"]))
    h = h.replace(ENERGY_LINK, AFP_LINK if c["id"] in AFP else CAL_LINK)
    wr(f"acciones/{c['id']}/index.html", h)

# ---------- recorrer todas las páginas: cinta, chips, pie de página
ilist = [(i, t) for i, t in ORDER if i in ACC]
def tape(pre):
    one = "".join(f'<a href="{pre}acciones/{i}/index.html"><b>{t}</b> $0 <span class="up">0% 12m</span></a>' for i, t in ilist)
    return one + one
DISC = ('<p><b>Aviso.</b> Las cifras de las fichas y comparadores provienen de los estados financieros y reportes de cada empresa, '
        'resumidos en nuestros videos de resultados; los precios de cierre se actualizan cada día hábil. Pueden contener errores: '
        'verifica siempre en la <a href="https://www.cmfchile.cl" target="_blank" rel="noopener">CMF</a> y la '
        '<a href="https://www.bolsadesantiago.com" target="_blank" rel="noopener">Bolsa de Santiago</a>. '
        'Nada de lo publicado es una recomendación de compra o venta. <a href="{pre}aviso-legal/index.html">Aviso legal</a>.</p>')
for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.relpath(os.path.join(root, f), S); t0 = t = rd(p)
        pre = "../" * p.count("/")
        t = re.sub(r'(<div class="tape"[^>]*><div class="tape-in">).*?(</div></div>)', lambda m: m.group(1) + tape(pre) + m.group(2), t, count=1, flags=re.S)
        if 'class="chips"' in t and p.startswith("acciones/") and p.count("/") == 2:
            fid = p.split("/")[1]
            t = re.sub(r'(<p class="small">Otras fichas: <span class="chips">).*?(</span>)', lambda m: m.group(1) + chips_for(fid) + m.group(2), t, count=1, flags=re.S)
        t = re.sub(r'<p><b>Aviso\.</b>.*?</p>', lambda _: DISC.replace("{pre}", pre), t, count=1, flags=re.S)
        t = t.replace(f'<p><a href="{pre}privacidad/index.html">Política de privacidad</a> · ',
                      f'<p><a href="{pre}nosotros/index.html">Quiénes somos</a> · <a href="{pre}privacidad/index.html">Política de privacidad</a> · <a href="{pre}aviso-legal/index.html">Aviso legal</a> · ')
        t = t.replace(f'escríbenos desde la página de <a href="{pre}contacto/index.html">Contacto</a>.</p>',
                      f'escríbenos desde la página de <a href="{pre}contacto/index.html">Contacto</a>. <a href="{pre}nosotros/index.html">Quiénes somos y cómo trabajamos</a>.</p>')
        # enlaces que quedarían rotos (calendario, comparadores reales, etc.): se deja solo el texto
        t = re.sub(r'<a href="(?:\.\./)*acciones/(?:' + "|".join(RETIRADOS_F) + r')/index\.html">([^<]*)</a>', r"\1", t)
        t = re.sub(r'<a class="tkr" href="(?:\.\./)*acciones/(?:' + "|".join(RETIRADOS_F) + r')/index\.html">([^<]*)</a>', r"\1", t)
        if t != t0: wr(p, t)

# ---------- portada
p = "index.html"; t = rd(p)
for d in RETIRADOS_F:
    t = re.sub(r'<a class="stock-card" href="acciones/' + d + r'/index\.html">.*?</a>', "", t, flags=re.S)
def card_row(c):
    if c["chg"] is None:
        return '<span class="row"><span>No cotiza</span><span>Valor por múltiplos de pares</span></span>'
    return f'<span class="row"><span>P/E <b>{n(c["pe"], 1, "x")}</b></span><span>Div. <b>{n(c["dy"], 1, "%") if c["dy"] is not None else "n/d"}</b></span><span class="up">0%</span></span>'
for c in R:
    t = re.sub(r'(<a class="stock-card" href="acciones/' + c["id"] + r'/index\.html">.*?)<span class="row">.*?</span></span>\n</a>',
               lambda m: m.group(1) + card_row(c) + "\n</a>", t, count=1, flags=re.S)
t = re.sub(r'<p class="note">\s*Las fichas de las empresas con video 2T 2026.*?</p>',
           '<p class="note">Todas las fichas usan los resultados reales del 2T 2026 de nuestros videos. Fuente oficial: estados financieros en CMF.</p>', t, count=1, flags=re.S)
t = t.replace("retail (Falabella, Ripley y Cencosud), bancos, AFP, CAP vs. CMPC, Aguas Andinas vs. IAM y SQM vs. Oro Blanco.",
              "retail (Falabella, Ripley y Cencosud), centros comerciales y AFP.")
wr(p, t)

# ---------- listado de acciones
p = "acciones/index.html"; t = rd(p)
for d in RETIRADOS_F:
    t = re.sub(r'<tr><th scope="row"><a href="' + d + r'/index\.html">.*?</tr>', "", t)
def arow(c):
    if c["chg"] is None:
        return f'<tr><th scope="row"><a href="{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["n"]}</td><td class="txt">{c["s"]}</td><td>No cotiza</td><td>n/a</td><td>n/a</td><td>n/a</td></tr>'
    dy = n(c["dy"], 1, "%") if c["dy"] is not None else "n/d"
    return f'<tr><th scope="row"><a href="{c["id"]}/index.html">{c["t"]}</a></th><td class="txt">{c["n"]}</td><td class="txt">{c["s"]}</td><td>{c["px"]}</td><td>{n(c["pe"], 1, "x")}</td><td>{dy}</td><td class="up">0%</td></tr>'
for c in R:
    t = re.sub(r'<tr><th scope="row"><a href="' + c["id"] + r'/index\.html">.*?</tr>', lambda _: arow(c), t, count=1)
ILL = r'<div class="period illus">.*?</div>'
t = re.sub(ILL, "", t, count=1, flags=re.S)
t = t.replace('<p class="note">Datos ilustrativos · septiembre 2026 · no oficiales. Fuente oficial: estados financieros en CMF.</p>',
              '<p class="note">Precio de cierre y variación de 12 meses: TradingView, se actualizan cada día hábil. P/E y dividend yield: de nuestros videos de resultados 2T 2026 (precios de septiembre de 2026). Fuente oficial: estados financieros en CMF.</p>')
wr(p, t)

# ---------- rankings
p = "rankings/index.html"; t = rd(p)
m = re.search(r"RANK_DATA=(\[.*?\]);", t, re.S); data = json.loads(m.group(1))
data = [d for d in data if d["id"] not in RETIRADOS_F and d.get("link")]
for d in data:
    c = RID.get(d["id"])
    if c:
        d.update(pe=c["pe"], epsg=c["epsg"], dy=c["dy"])
    if d["id"] in ACC and ACC[d["id"]].get("y1") is not None:
        d["chg"] = round(ACC[d["id"]]["y1"])
data = [d for d in data if d["pe"] is not None]
t = t[:m.start(1)] + json.dumps(data, ensure_ascii=False) + t[m.end(1):]
t = re.sub(ILL, "", t, count=1, flags=re.S)
t = t.replace('<p class="note">Datos ilustrativos · septiembre 2026 · no oficiales. Fuente oficial: estados financieros en CMF.</p>',
              '<p class="note">P/E, crecimiento del EPS (2T 2026 frente al 2T 2025) y dividend yield: de nuestros videos de resultados 2T 2026. Variación de 12 meses: TradingView, al último cierre disponible al publicar. No incluye empresas que no cotizan (AES Andes y AFP Capital). Fuente oficial: estados financieros en CMF.</p>')
wr(p, t)

# ---------- valoraciones (hornear.py arma la tabla)
p = "valoraciones/index.html"; t = rd(p)
t = re.sub(ILL, "", t, count=1, flags=re.S)
t = t.replace('<p class="note">Datos ilustrativos · septiembre 2026 · no oficiales. Fuente oficial: estados financieros en CMF.</p>',
              '<p class="note">Múltiplos de nuestros videos de resultados 2T 2026. Fuente oficial: estados financieros en CMF.</p>')
wr(p, t)

# ---------- resultados
p = "resultados/index.html"; t = rd(p)
for d in RETIRADOS_F:
    t = re.sub(r'<section id="' + d + r'">.*?</section>\n?', "", t, count=1, flags=re.S)
    t = re.sub(r'<a href="#' + d + r'">[^<]*</a>', "", t)
for c in R:
    body = ficha(c).split('<h2 class="h-sec">Resultados del segundo trimestre 2026</h2>', 1)[1].split("</section>", 1)[0].replace(NOTE, "")
    t = re.sub(r'<section id="' + c["id"] + r'">.*?</section>',
               lambda _: f'<section id="{c["id"]}"><h2 class="h-sec"><a href="../acciones/{c["id"]}/index.html">{c["n"]}</a></h2>{body}</section>', t, count=1, flags=re.S)
t = re.sub(ILL, "", t, count=1, flags=re.S)
t = t.replace('<p class="note">Datos ilustrativos · septiembre 2026 · no oficiales. Fuente oficial: estados financieros en CMF.</p>',
              '<p class="note">Cifras de nuestros videos de resultados 2T 2026 (estados financieros, análisis razonados y reportes de cada empresa). (c) = cifra calculada por nosotros. Fuente oficial: estados financieros en CMF.</p>')
t = t.replace("Ingresos, EBITDA, utilidad, EPS, deuda y flujo de caja de los últimos cuatro trimestres informados.",
              "Ingresos, EBITDA, utilidad y EPS del segundo trimestre de 2026 frente al mismo trimestre de 2025, con deuda y sorpresa frente al consenso cuando la hay.")
wr(p, t)

# ---------- comparadores (índice)
p = "comparadores/index.html"; t = rd(p)
for d in RETIRADOS_C:
    t = re.sub(r'<a class="cmp-card" href="' + d + r'/index\.html">.*?</a>', "", t, count=1, flags=re.S)
t = t.replace(" Los comparadores marcados como <b>Ilustrativo</b> usan datos de ejemplo, no oficiales.", "")
t = t.replace('<p class="note">Datos ilustrativos · septiembre 2026 · no oficiales. Fuente oficial: estados financieros en CMF.</p>',
              '<p class="note">Cifras de nuestros videos de resultados 2T 2026. Fuente oficial: estados financieros en CMF.</p>')
wr(p, t)

# ---------- educación: el ejemplo usaba cifras inventadas de CAP
p = "educacion/index.html"; t = rd(p)
t = t.replace("En el ejemplo de CAP, el EBITDA del último trimestre (128) sobre ingresos (445) da un margen de 28,8%.",
              "Por ejemplo, Colbún tuvo en el 2T 2026 un EBITDA de US$156,9 millones sobre ingresos de US$449,2 millones: un margen EBITDA de 34,9%.")
wr(p, t)
print("ok", len(R), "fichas reales;", len(ORDER), "fichas en el sitio;", len(data), "en rankings")
