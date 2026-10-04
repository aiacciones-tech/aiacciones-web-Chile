import os, re, json, sys
src = open("energy.py").read().split("old = re.findall")[0]
exec(src)
exec(open(sys.argv[1]).read())
NEW = [C]
ID, TK = C['id'], C['t']

CAL_LINK = f'<p class="small">Su próximo reporte (3T 2026) está en el <a href="../../calendario/index.html">calendario de resultados</a>: {C["next"]}.</p>'
old = re.findall(r'<a href="\.\./([a-z0-9-]+)/index\.html">([A-Z0-9 -]+)</a>', tpl.split('class="chips"')[1].split("</span>")[0])
all_chips = [("afpcapital", "AFPCAPITAL")] + old + [(ID, TK)]
ch = "".join(f'<a href="../{i}/index.html">{t}</a>' for i, t in all_chips if i != ID)
wr(f"acciones/{ID}/index.html", ficha(C).replace(f"CHIPS_{ID}", ch).replace(ENERGY_LINK, CAL_LINK))
for d in os.listdir(os.path.join(S, "acciones")):
    p = f"acciones/{d}/index.html"
    if d == ID or not os.path.isfile(os.path.join(S, p)): continue
    t = rd(p)
    if 'class="chips"' in t and f'href="../{ID}/' not in t:
        pre, post = t.split('class="chips">', 1); inner, tail = post.split("</span>", 1)
        wr(p, pre + 'class="chips">' + inner + f'<a href="../{ID}/index.html">{TK}</a></span>' + tail)
def tape_item(prefix, c):
    return f'<a href="{prefix}acciones/{c["id"]}/index.html"><b>{c["t"]}</b> {c["px"]} <span class="{"up" if c["chg"] >= 0 else "down"}">{chg_s(c)} 12m</span></a>'
for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.relpath(os.path.join(root, f), S); t = rd(p)
        m = re.search(r'<div class="tape-in"><a href="([./]*)acciones/cap/index\.html"', t)
        if not m or f"<b>{TK}</b>" in t: continue
        wr(p, t.replace('<span><b>ORO BLANCO</b>', tape_item(m.group(1), C) + '<span><b>ORO BLANCO</b>'))
f1 = lambda v, s, d=1: n(v, d, s) if v is not None else "n/a"
cls = "up" if C["chg"] >= 0 else "down"
p = "index.html"; t = rd(p)
if f'class="stock-card" href="acciones/{ID}/' not in t:
    card = f'''<a class="stock-card" href="acciones/{ID}/index.html">
  <span class="tk">{TK}</span>
  <span class="nm">{C['n']}</span>
  <span class="sc">{C['s']}</span>
  <span class="row"><span>P/E <b>{f1(C['pe'], 'x')}</b></span><span>Div. <b>{f1(C['dy'], '%')}</b></span><span class="{cls}">{chg_s(C)}</span></span>
</a>'''
    t = t.replace('<div class="stock-grid">', '<div class="stock-grid">' + card, 1); wr(p, t)
p = "acciones/index.html"; t = rd(p)
if f'href="{ID}/' not in t:
    row = f'<tr><th scope="row"><a href="{ID}/index.html">{TK}</a></th><td class="txt">{C["n"]}</td><td class="txt">{C["s"]}</td><td>{C["px"]}</td><td>{f1(C["pe"], "x")}</td><td>{f1(C["dy"], "%")}</td><td class="{cls}">{chg_s(C)}</td></tr>'
    t = t.replace("</tbody></table></div>\n<p class=\"note\">", row + "</tbody></table></div>\n<p class=\"note\">", 1); wr(p, t)
p = "valoraciones/index.html"; t = rd(p)
if f"acciones/{ID}/" not in t:
    row = f'<tr><th scope="row"><a href="../acciones/{ID}/index.html">{TK}</a></th><td class="txt">{C["s"]}</td><td>{f1(C["pe"], "x")}</td><td>{f1(C["fpe"], "x")}</td><td>{f1(C["pbv"], "x", 2)}</td><td>{f1(C["ev"], "x")}</td><td>{f1(C["dy"], "%")}</td><td>{f1(C["roe"], "%")}</td></tr>'
    t = t.replace("</tbody></table></div>", row + "</tbody></table></div>", 1); wr(p, t)
p = "rankings/index.html"; t = rd(p)
m = re.search(r"RANK_DATA=(\[.*?\]);", t, re.S); data = json.loads(m.group(1))
if not any(x["id"] == ID for x in data) and C["pe"] is not None:
    data.append({"id": ID, "t": TK, "n": C["n"], "s": C["s"], "pe": C["pe"], "epsg": C["epsg"], "dy": C["dy"], "chg": C["chg"], "link": True})
    wr(p, t[:m.start(1)] + json.dumps(data, ensure_ascii=False) + t[m.end(1):])
p = "resultados/index.html"; t = rd(p)
if f'id="{ID}"' not in t:
    body = ficha(C).split('<h2 class="h-sec">Resultados del segundo trimestre 2026</h2>', 1)[1].split("</section>", 1)[0].replace(NOTE, "")
    t = t.replace("</main>", f'<section id="{ID}"><h2 class="h-sec"><a href="../acciones/{ID}/index.html">{C["n"]}</a></h2>{body}</section>\n</main>', 1)
    t = re.sub(r'(<p class="chips">.*?)(</p>)', lambda mm: mm.group(1) + f'<a href="#{ID}">{TK}</a>' + mm.group(2), t, count=1, flags=re.S)
    wr(p, t)
print("ok", ID)
