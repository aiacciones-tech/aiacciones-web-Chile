import os, re, json
src = open("energy.py").read().split("old = re.findall")[0]
exec(src)
C = dict(id="parauco", t="PARAUCO", n="Parque Arauco", s="Centros comerciales (Chile, Perú y Colombia)", px="$3.639,9", chg=84,
  pe=23.1, fpe=24.2, pbv=1.64, ev=16.6, dy=1.2, roe=10.6, epsg=-31, vid="XXTSTOPBMGY", q="Parque Arauco",
  lede="Operador de centros comerciales en Chile, Perú y Colombia (Parque Arauco Kennedy, Kennedy Oriente, MegaPlaza y Minka, entre otros). Gana con los arriendos de sus locatarios. En los malls se mira el FFO (flujo de fondos de la operación) además de la utilidad, porque esta incluye la revalorización de las propiedades y el reajuste de la deuda en UF.",
  vtitle="Parque Arauco: ingresos +18%, pero la utilidad cae 31% (2T 2026)",
  cap="Cifras en CLP miles de millones salvo EPS · 2T 2026 vs. 2T 2025",
  rows=[("Ingresos",88.3,104.2,1),("EBITDA",64.5,74.7,1),("FFO",51.4,56.7,1),("FFO ajustado (sin reajuste UF)",38.7,30.0,1),("Utilidad controladores",26.5,18.4,1),("EPS (CLP por acción)",29.30,20.07,2)],
  derived=("Margen EBITDA","73,1%","71,7%"),
  kpi="Deuda financiera neta / EBITDA: <b>4,5x</b> (5,3x un año antes), tras un aumento de capital de $280 mil MM. EPS de $20,07 vs. ~$39 esperado por el consenso; en el trimestre no hubo revalorización de propiedades y el reajuste por UF restó $22,7 mil MM.",
  tiles=[("P/E","23,1x"),("Forward P/E","24,2x"),("P/FFO","16,0x"),("EV/EBITDA","16,6x"),("FCF yield","3,1%"),("Dividend Yield","1,2%")],
  small="P/BV <b>1,64x</b> · ROE <b>10,6%</b> · FFO por acción $62,0 (+9,4%) · Precio objetivo promedio <b>$4.226</b> (+16%, 10 analistas) · Clasificación AA+.",
  mirar=["Inflación: el reajuste de la deuda en UF golpea la utilidad.","Chile: ventas mismas áreas +2,8% y menos turistas argentinos.","Perú y Colombia, con EBITDA +22% y +28%.","Apertura de Arauco Chicureo (4T 2026) y compra de Mall Paseo Quilín."])
VAROV.update({('parauco','Ingresos'):17.9,('parauco','EBITDA'):15.8,('parauco','FFO'):10.5,('parauco','FFO ajustado (sin reajuste UF)'):-22.5,('parauco','Utilidad controladores'):-30.8})
NEW = [C]
CAL_LINK = '<p class="small">Su próximo reporte (3T 2026) está en el <a href="../../calendario/index.html">calendario de resultados</a>: 29 de octubre.</p>'
old = re.findall(r'<a href="\.\./([a-z0-9-]+)/index\.html">([A-Z0-9 -]+)</a>', tpl.split('class="chips"')[1].split("</span>")[0])
all_chips = [("afpcapital", "AFPCAPITAL")] + old + [("parauco", "PARAUCO")]
ch = "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in all_chips if i != "parauco")
wr("acciones/parauco/index.html", ficha(C).replace("CHIPS_parauco", ch).replace(ENERGY_LINK, CAL_LINK))
for d in os.listdir(os.path.join(S, "acciones")):
    p = f"acciones/{d}/index.html"
    if d == "parauco" or not os.path.isfile(os.path.join(S, p)): continue
    t = rd(p)
    if 'class="chips"' in t and 'href="../parauco/' not in t:
        pre, post = t.split('class="chips">', 1); inner, tail = post.split("</span>", 1)
        wr(p, pre + 'class="chips">' + inner + '<a href="../parauco/index.html">PARAUCO</a></span>' + tail)
def tape_item(prefix, c):
    return f'<a href="{prefix}acciones/{c["id"]}/index.html"><b>{c["t"]}</b> {c["px"]} <span class="up">+{n(c["chg"], 0, "%")} 12m</span></a>'
for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.relpath(os.path.join(root, f), S); t = rd(p)
        m = re.search(r'<div class="tape-in"><a href="([./]*)acciones/cap/index\.html"', t)
        if not m or "<b>PARAUCO</b>" in t: continue
        wr(p, t.replace('<span><b>ORO BLANCO</b>', tape_item(m.group(1), C) + '<span><b>ORO BLANCO</b>'))
p = "index.html"; t = rd(p)
if 'href="acciones/parauco/' not in t:
    card = f'''<a class="stock-card" href="acciones/parauco/index.html">
  <span class="tk">PARAUCO</span>
  <span class="nm">Parque Arauco</span>
  <span class="sc">{C['s']}</span>
  <span class="row"><span>P/E <b>23,1x</b></span><span>Div. <b>1,2%</b></span><span class="up">+84%</span></span>
</a>'''
    t = t.replace('<div class="stock-grid">', '<div class="stock-grid">' + card, 1); wr(p, t)
p = "acciones/index.html"; t = rd(p)
if 'href="parauco/' not in t:
    row = f'<tr><th scope="row"><a href="parauco/index.html">PARAUCO</a></th><td class="txt">Parque Arauco</td><td class="txt">{C["s"]}</td><td>{C["px"]}</td><td>23,1x</td><td>1,2%</td><td class="up">+84%</td></tr>'
    t = t.replace("</tbody></table></div>\n<p class=\"note\">", row + "</tbody></table></div>\n<p class=\"note\">", 1); wr(p, t)
p = "valoraciones/index.html"; t = rd(p)
if "acciones/parauco/" not in t:
    row = f'<tr><th scope="row"><a href="../acciones/parauco/index.html">PARAUCO</a></th><td class="txt">{C["s"]}</td><td>23,1x</td><td>24,2x</td><td>1,64x</td><td>16,6x</td><td>1,2%</td><td>10,6%</td></tr>'
    t = t.replace("</tbody></table></div>", row + "</tbody></table></div>", 1); wr(p, t)
p = "rankings/index.html"; t = rd(p)
m = re.search(r"RANK_DATA=(\[.*?\]);", t, re.S); data = json.loads(m.group(1))
if not any(x["id"] == "parauco" for x in data):
    data.append({"id": "parauco", "t": "PARAUCO", "n": "Parque Arauco", "s": C["s"], "pe": 23.1, "epsg": -31, "dy": 1.2, "chg": 84, "link": True})
    wr(p, t[:m.start(1)] + json.dumps(data, ensure_ascii=False) + t[m.end(1):])
p = "resultados/index.html"; t = rd(p)
if 'id="parauco"' not in t:
    body = ficha(C).split('<h2 class="h-sec">Resultados del segundo trimestre 2026</h2>', 1)[1].split("</section>", 1)[0].replace(NOTE, "")
    t = t.replace("</main>", f'<section id="parauco"><h2 class="h-sec"><a href="../acciones/parauco/index.html">Parque Arauco</a></h2>{body}</section>\n</main>', 1)
    t = re.sub(r'(<p class="chips">.*?)(</p>)', lambda mm: mm.group(1) + '<a href="#parauco">PARAUCO</a>' + mm.group(2), t, count=1, flags=re.S)
    wr(p, t)
print("ok")
