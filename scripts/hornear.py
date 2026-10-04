"""Escribe los datos de web/assets/mercado.json dentro del HTML del sitio.
uso: python3 scripts/hornear.py [carpeta]   (por defecto web/)
- cinta de precios de todas las páginas: precio de cierre y variación 12 meses
- recuadro de precio de cada ficha: precio de cierre, variación del día y 12 meses
- listado acciones/: columna de precio y variación 12 meses
- portada: tabla de índices (IPSA, IGPA) con P/E, forward P/E y promedios de 5 y 10 años"""
import json, os, re, sys, glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "web")
M = json.load(open(os.path.join(ROOT, "web", "assets", "mercado.json"), encoding="utf-8"))
ACC = M["acciones"]
_hp = os.path.join(ROOT, "web", "assets", "hechos.json")
HE = json.load(open(_hp, encoding="utf-8")) if os.path.exists(_hp) else {"items": []}
DESDE = "4-oct-2026"  # desde cuándo seguimos los hechos esenciales
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def num(v, d):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s


def px(v):
    return "$" + num(v, 2 if v < 1000 else 0)


def pct(v, d=1, sign=True):
    if v is None:
        return "n/d"
    return ("+" if sign and v > 0 else "") + num(v, d) + "%"


def cls(v):
    return "up" if (v or 0) >= 0 else "down"


def fecha(iso):
    if not iso:
        return "n/d"
    d = datetime.date.fromisoformat(iso)
    return f"{d.day}-{MESES[d.month - 1]}-{d.year}"


_u = datetime.datetime.strptime(M["actualizado"], "%Y-%m-%dT%H:%MZ") - datetime.timedelta(hours=3)
ACT = f"{_u.day}-{MESES[_u.month - 1]}-{_u.year} a las {_u:%H:%M} (hora de Chile)"
FECHA = fecha(max((a["fecha"] for a in ACC.values() if a.get("fecha")), default=None))


def tape(s):
    def rep(m):
        a = ACC.get(m.group(2))
        if not a:
            return m.group(0)
        return (f'<a href="{m.group(1)}acciones/{m.group(2)}/index.html"><b>{m.group(3)}</b> {px(a["px"])} '
                f'<span class="{cls(a["y1"])}">{pct(a["y1"], 0)} 12m</span></a>')
    s = re.sub(r'<a href="((?:\.\./)*)acciones/([\w-]+)/index\.html"><b>([^<]+)</b> [^<]*<span class="(?:up|down)">[^<]*12m</span></a>', rep, s)
    return re.sub(r'<div class="tape" aria-label="[^"]*">', f'<div class="tape" aria-label="Precios de cierre al {FECHA}">', s)


def ficha(s, fid):
    a = ACC.get(fid)
    m = re.search(r'<div class="quote"( data-video="[^"]*")?>(.*?)</div>', s, re.S)
    if not a or not m:
        return s
    video = m.group(1)
    if not video:  # primera vez: guarda el precio usado en el video
        vp = re.search(r'<span class="px">([^<]+)</span>', m.group(2))
        vn = re.search(r'<span class="note">Precio de cierre usado en el video \(([^)]+)\)</span>', m.group(2))
        video = f' data-video="{vp.group(1) if vp else ""}|{vn.group(1) if vn else ""}"' if vp else ' data-video="|"'
    vpx, vdate = re.search(r'data-video="([^|]*)\|([^"]*)"', video).groups()
    tk = re.search(r'<span class="tk">([^<]+)</span>', m.group(2))
    vid = f'<span class="note">En el video: {vpx} ({vdate})</span>' if vpx else ""
    box = (f'<div class="quote"{video}>\n    <span class="tk">{tk.group(1) if tk else a["t"]}</span>\n'
           f'    <span class="px">{px(a["px"])}</span>\n'
           f'    <span><span class="{cls(a["d1"])}">{pct(a["d1"], 2)}</span> en el día · <span class="{cls(a["y1"])}">{pct(a["y1"], 0)}</span> en 12 meses</span>\n'
           f'    <span class="note">Precio de cierre al {fecha(a["fecha"])}</span>\n    {vid}\n  </div>')
    return s[:m.start()] + box + s[m.end():]


def listado(s):
    s = s.replace('<th scope="col">Precio CLP</th>', '<th scope="col">Precio de cierre</th>')

    def rep(m):
        a = ACC.get(m.group(2))
        if not a:
            return m.group(0)
        return f'{m.group(1)}<td>{px(a["px"])}</td>{m.group(3)}<td class="{cls(a["y1"])}">{pct(a["y1"], 0)}</td></tr>'
    return re.sub(r'(<tr><th scope="row"><a href="([\w-]+)/index\.html">[^<]+</a></th><td class="txt">[^<]*</td><td class="txt">[^<]*</td>)<td>[^<]*</td>(<td>[^<]*</td><td>[^<]*</td>)<td class="(?:up|down)">[^<]*</td></tr>', rep, s)


def x(v):
    return num(v, 1) + "x" if v else "—"


def indices(s):
    I, F, W = M.get("indices", {}), M.get("fwd") or {}, M.get("wpe") or {}
    if not I:
        return s
    rows = ""
    for k in ("ipsa", "igpa"):
        i = I.get(k)
        if not i:
            continue
        val = k == "ipsa"
        rows += (f'<tr><th scope="row">{i["n"]}<span class="sub">{i["full"]}</span></th><td>{num(i["v"], 2)}</td>'
                 f'<td class="{cls(i["d1"])}">{pct(i["d1"], 2)}</td><td class="{cls(i["ytd"])}">{pct(i["ytd"])}</td>'
                 f'<td class="{cls(i["y1"])}">{pct(i["y1"])}</td>'
                 f'<td>{x(W.get("pe")) if val else "—"}</td><td>{x(F.get("v")) + "*" if val and F.get("v") else "—"}</td>'
                 f'<td>{x(W.get("avg5")) if val else "—"}</td><td>{x(W.get("avg10")) if val else "—"}</td></tr>')
    pe = W.get("pe")
    lect = ""
    if pe and W.get("avg5") and W.get("avg10"):
        lect = (f'<div class="cmp-read"><b>Lectura.</b> El mercado chileno transa a {x(pe)} sus utilidades, '
                f'{"sobre" if pe > W["avg5"] else "bajo"} su promedio de 5 años ({x(W["avg5"])}) y '
                f'{"sobre" if pe > W["avg10"] else "bajo"} su promedio de 10 años ({x(W["avg10"])}).</div>')
    box = f'''<!--indices--><section class="mkt" id="indices"><h2 class="h-sec">Índices de la Bolsa de Santiago</h2>
<p class="small">Cierre al {fecha(I.get("ipsa", {}).get("fecha"))} · actualizado el {ACT}. Se actualiza solo cada día hábil después del cierre de la Bolsa. Prom. 5a y 10a = P/E promedio de 5 y 10 años.</p>
<div class="table-scroll"><table class="data idx-t"><thead><tr><th scope="col">Índice</th><th scope="col">Valor</th><th scope="col">Día</th><th scope="col">En el año</th><th scope="col">12 meses</th><th scope="col">P/E</th><th scope="col">Forward P/E</th><th scope="col" title="P/E promedio de 5 años">Prom. 5a</th><th scope="col" title="P/E promedio de 10 años">Prom. 10a</th></tr></thead><tbody>{rows}</tbody></table></div>
{lect}
<p class="note">Valores: TradingView, índices MSCI IPSA y MSCI IGPA con dividendos reinvertidos. P/E y promedios de 5 y 10 años: mercado chileno (índice MSCI Chile, vía el ETF ECH) según worldperatio.com al {fecha(W.get("fecha"))}; usamos esa base para el IPSA porque reúne a las mismas grandes empresas y no hay una serie pública del P/E del IPSA. *Forward P/E: estimación propia de AI Acciones Chile, ponderada por capitalización, con la utilidad que esperan los analistas para el próximo año fiscal en las {F.get("empresas", 30)} mayores empresas chilenas de la Bolsa (cubre {F.get("cobertura", "n/d")}% de su capitalización). El IGPA no tiene una serie pública de P/E.</p></section><!--/indices-->'''
    if "<!--indices-->" in s:
        return re.sub(r"<!--indices-->.*?<!--/indices-->", lambda _: box, s, flags=re.S)
    i = s.find("</section>", s.find('<section class="hero">'))
    return s[:i + 10] + "\n" + box + s[i + 10:]


def act(iso):
    u = datetime.datetime.strptime(iso, "%Y-%m-%dT%H:%MZ") - datetime.timedelta(hours=3)
    return f"{u.day}-{MESES[u.month - 1]}-{u.year} a las {u:%H:%M}"


def li_hecho(i, prefix, con_tk):
    d = datetime.date.fromisoformat(i["fecha"][:10])
    div = any("dividendo" in m.lower() for m in i["materias"])
    tk = ""
    if con_tk:
        t = ACC.get(i["id"], {}).get("t") or i["id"].upper()
        tk = f'<a class="tkr" href="{prefix}acciones/{i["id"]}/index.html">{t}</a> '
    mats = " · ".join(i["materias"]) or "Hecho esencial"
    badge = '<b class="hdiv">Dividendo</b> ' if div else ""
    return (f'<li><span class="hf">{d.day}-{MESES[d.month - 1]}-{d.year}</span> {tk}'
            f'{badge}<a href="{i["url"]}" target="_blank" rel="noopener">{mats}</a></li>')


def hechos_ficha(s, fid):
    its = [i for i in HE["items"] if i["id"] == fid][:6]
    if its:
        body = '<ul class="hechos-l">' + "".join(li_hecho(i, "../../", False) for i in its) + "</ul>"
    else:
        body = f'<p class="small">No hay hechos esenciales nuevos desde el {DESDE}, cuando empezamos a seguirlos.</p>'
    box = (f'<!--hechos--><section class="hechos" id="hechos"><h2 class="h-sec">Hechos esenciales recientes</h2>{body}'
           f'<p class="note">Fuente: CMF (Comisión para el Mercado Financiero). Actualizado el {act(HE.get("actualizado", M["actualizado"]))}. '
           f'Los dividendos anunciados también aparecen en el <a href="../../calendario/index.html">calendario</a>.</p></section><!--/hechos-->')
    if "<!--hechos-->" in s:
        return re.sub(r"<!--hechos-->.*?<!--/hechos-->", lambda _: box, s, flags=re.S)
    m = re.search(r'<section class="page-head stock-head">.*?</section>', s, re.S)
    return s[:m.end()] + "\n" + box + s[m.end():] if m else s


def hechos_home(s):
    its = HE["items"][:8]
    body = ('<ul class="hechos-l">' + "".join(li_hecho(i, "", True) for i in its) + "</ul>") if its else \
        f'<p class="small">Sin hechos esenciales nuevos de las empresas del sitio desde el {DESDE}.</p>'
    box = (f'<!--hechos--><section class="hechos" id="hechos"><h2 class="h-sec">Últimos hechos esenciales</h2>{body}'
           f'<p class="note">Fuente: CMF. Actualizado el {act(HE.get("actualizado", M["actualizado"]))}. '
           f'Solo empresas con ficha en el sitio.</p></section><!--/hechos-->')
    if "<!--hechos-->" in s:
        return re.sub(r"<!--hechos-->.*?<!--/hechos-->", lambda _: box, s, flags=re.S)
    i = s.find("<!--/indices-->")
    return s[:i + 15] + "\n" + box + s[i + 15:] if i >= 0 else s


CSS = """/*mercado*/
.hechos-l { list-style: none; margin: 0 0 8px; padding: 0; }
.hechos-l li { padding: 8px 0; border-bottom: 1px solid var(--line); font-size: 15px; }
.hechos-l .hf { display: inline-block; min-width: 92px; font: 500 13px/1 var(--f-mono); color: var(--muted); }
.hechos-l .tkr { font: 600 13px/1 var(--f-mono); margin-right: 4px; }
.hdiv { font: 600 11px/1 var(--f-mono); padding: 3px 6px; border-radius: 3px; background: #4cc38a; color: #10241a; margin-right: 4px; }
.hero { overflow: hidden; }
.mkt .idx-t { min-width: 640px; }
.idx-t th, .idx-t td { padding-left: 8px; padding-right: 8px; }
.idx-t th .sub { display: block; font: 400 12px/1.3 var(--f-body); color: var(--muted); }
.quote .note + .note { margin-top: 2px; }
/*/mercado*/"""

for p in glob.glob(os.path.join(DIR, "**", "*.html"), recursive=True):
    rel = os.path.relpath(p, DIR).replace(os.sep, "/")
    s0 = s = open(p, encoding="utf-8").read()
    s = tape(s)
    m = re.match(r"acciones/([\w-]+)/index\.html$", rel)
    if m:
        s = ficha(s, m.group(1))
        s = hechos_ficha(s, m.group(1))
    if rel == "acciones/index.html":
        s = listado(s)
    if rel == "index.html":
        s = indices(s)
        s = hechos_home(s)
    if s != s0:
        open(p, "w", encoding="utf-8").write(s)
css = os.path.join(DIR, "assets", "styles.css")
c = open(css, encoding="utf-8").read()
c2 = re.sub(r"\n?/\*mercado\*/.*?/\*/mercado\*/", "", c, flags=re.S)
c2 = re.sub(r"\n\.mkt \.idx-t \{ min-width: 760px; \}\n\.idx-t th \.sub .*?\n\.quote \.note \+ \.note \{ margin-top: 2px; \}\n", "\n", c2, flags=re.S)
if c2 + "\n" + CSS != c:
    open(css, "w", encoding="utf-8").write(c2 + "\n" + CSS)
print("horneado", DIR, "cierre", FECHA, len(ACC), "acciones")
