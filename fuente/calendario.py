import os, re, datetime as dt, json
S = "/tmp/claude-0/-home-claude/51bbcb85-f720-5650-9a37-2f75843c73b7/scratchpad/site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)
D = lambda y, m, d: dt.date(y, m, d)
FICHA = {"ANDINA-B":"andina-a","ANDINA-A":"andina-a","HABITAT":"habitat","BESALCO":"besalco","ENELGXCH":"enelgxch","PROVIDA":"provida","AFPCAPITAL":"afpcapital",
 "PLANVITAL":"planvital","CHILE":"chile","CENCOSUD":"cencosud","CMPC":"cmpc","COPEC":"copec","FALABELLA":"falabella","RIPLEY":"ripley","VAPORES":"vapores","SK":"sk",
 "IAM":"iam","QUINENCO":"quinenco","COLBUN":"colbun","ENELCHILE":"enelchile","ECL":"ecl","BSANTANDER":"bsantander","CAP":"cap","ITAUCL":"itau","SQM-B":"sqm-b",
 "CGE":"cge","PARAUCO":"parauco","MALLPLAZA":"mallplaza","CENCOMALLS":"cencomalls","AES ANDES":"aes-andes","BCI":"bci","SCHWAGER":"schwager","LTM":"ltm","CCU":"ccu","SONDA":"sonda"}
CMF = "Fecha informada a la CMF"
# ---------------------------------------------------------------- datos por trimestre (agregar nuevos trimestres aquí)
Q = [dict(
 key="q2026-3t", year=2026, q=3, label="3T 2026",
 intro="Resultados del tercer trimestre de 2026 (julio a septiembre), que las empresas publican entre octubre y noviembre, y los dividendos anunciados o esperados entre octubre de 2026 y enero de 2027.",
 updated="3 de octubre de 2026",
 reports=[
  (D(2026,10,23),"Sonda","SONDA","Tecnología","C",""),
  (D(2026,10,27),"Embotelladora Andina","ANDINA-B","Bebidas","C",""),
  (D(2026,10,27),"AFP Habitat","HABITAT","AFP","C",""),
  (D(2026,10,27),"Colbún","COLBUN","Energía","C",""),
  (D(2026,10,28),"Besalco","BESALCO","Construcción","C",""),
  (D(2026,10,28),"Enel Generación Chile","ENELGXCH","Energía","C",""),
  (D(2026,10,28),"Enel Chile","ENELCHILE","Energía","C",""),
  (D(2026,10,28),"Engie Energía Chile","ECL","Energía","C",""),
  (D(2026,10,29),"Enel Américas","ENELAM","Energía","C",""),
  (D(2026,10,29),"Parque Arauco","PARAUCO","Centros comerciales","C",""),
  (D(2026,10,30),"AFP Provida","PROVIDA","AFP","C",""),
  (D(2026,10,30),"AFP Capital","AFPCAPITAL","AFP","C","No transa en bolsa."),
  (D(2026,10,30),"AFP Cuprum","CUPRUM","AFP","C","No transa en bolsa."),
  (D(2026,10,30),"AFP PlanVital","PLANVITAL","AFP","C",""),
  (D(2026,10,30),"Banco Santander Chile","BSANTANDER","Banca","C","Antes de la apertura; conferencia el 4 de noviembre."),
  (D(2026,11,2),"Entel","ENTEL","Telecomunicaciones","C",""),
  (D(2026,11,2),"Viña Concha y Toro","CONCHATORO","Vinos","C",""),
  (D(2026,11,3),"CCU","CCU","Bebidas","C",""),
  (D(2026,11,3),"Mallplaza","MALLPLAZA","Centros comerciales","C",""),
  (D(2026,11,4),"Banco de Chile","CHILE","Banca","E","El 3T 2025 publicó el 4 de noviembre; podría adelantarse a fines de octubre."),
  (D(2026,11,4),"Cencosud","CENCOSUD","Retail","E","El 3T 2025 publicó el 4 de noviembre."),
  (D(2026,11,5),"CMPC","CMPC","Forestal","C",""),
  (D(2026,11,5),"Empresas Copec","COPEC","Holding","E","El 3T 2025 publicó cerca del 6 de noviembre."),
  (D(2026,11,6),"CAP","CAP","Minería y acero","C",""),
  (D(2026,11,6),"SM SAAM","SMSAAM","Transporte","C",""),
  (D(2026,11,6),"Banco Itaú Chile","ITAUCL","Banca","E","El 3T 2025 tuvo su conferencia el 10 de noviembre."),
  (D(2026,11,9),"SMU","SMU","Supermercados","C",""),
  (D(2026,11,10),"Falabella","FALABELLA","Retail","C",""),
  (D(2026,11,3),"LATAM Airlines","LTM","Aerolínea","C","Adelanta su reporte: el 3T 2025 lo publicó el 14 de noviembre."),
  (D(2026,11,17),"SQM","SQM-B","Minería (litio)","C","Tras el cierre; conferencia el 18 de noviembre."),
  (D(2026,11,18),"Ripley Corp","RIPLEY","Retail","E","El 3T 2025 publicó el 19 de noviembre."),
  (D(2026,11,20),"CSAV (Vapores)","VAPORES","Transporte","C",""),
  (D(2026,11,20),"Sigdo Koppers","SK","Holding industrial","E","El 3T 2025 publicó entre el 20 y el 24 de noviembre."),
  (D(2026,11,26),"IAM","IAM","Sanitarias","C",""),
  (D(2026,11,26),"Aguas Andinas","AGUAS-A","Sanitarias","C",""),
  (D(2026,11,27),"Quiñenco","QUINENCO","Holding","C",""),
 ],
 pending=[("CGE","CGE","Distribución eléctrica","Aún no informa la fecha. El plazo de la CMF para los estados a septiembre vence a fines de noviembre."),
          ("AES Andes","AES ANDES","Energía","No cotiza en bolsa; publica su reporte en su sitio de inversionistas, normalmente en noviembre."),
          ("BCI","BCI","Banca","Aún no informa la fecha."),
          ("Cencosud Shopping","CENCOMALLS","Centros comerciales","Aún no informa la fecha; su matriz Cencosud publicaría cerca del 4 de noviembre."),],
 nodiv="BCI, BSANTANDER, ITAUCL, CENCOSUD, RIPLEY, ECL, CGE, CAP, SQM-B y VAPORES. Banco de Chile paga su dividendo anual en marzo",
 divs=json.load(open(os.path.join(os.path.dirname(S), "divs.json"), encoding="utf-8")),
)]
MES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
def fd(d): return f"{d.day} {MES[d.month]}"
def emp(n, t, pre="../"):
    f = FICHA.get(t)
    return f'<a href="{pre}acciones/{f}/index.html">{n}</a>' if f else n
BADGE = {"C": '<span class="st st-c">Confirmada</span>', "E": '<span class="st st-e">Estimada</span>'}
DBADGE = {"C": '<span class="st st-c">Confirmado</span>', "E": '<span class="st st-e">Estimado</span>'}

def quarter(qd):
    k = qd["key"]
    # reportes agrupados por semana
    rows = sorted(qd["reports"], key=lambda r: (r[0], r[1]))
    weeks = {}
    for r in rows:
        mon = r[0] - dt.timedelta(days=r[0].weekday()); weeks.setdefault(mon, []).append(r)
    tb = ""
    for mon, rs in weeks.items():
        tb += f'<tr class="wk"><th colspan="5" scope="rowgroup">Semana del {fd(mon)}</th></tr>'
        for d, n, t, sec, st, note in rs:
            tb += f'<tr><td class="txt dt">{DIAS[d.weekday()][:3]} {fd(d)}</td><th scope="row" class="txt">{emp(n, t)} <span class="tkr">{t}</span></th><td class="txt">{sec}</td><td class="txt">{BADGE[st]}</td><td class="txt nt">{note}</td></tr>'
    nC = sum(1 for r in rows if r[4] == "C"); nE = len(rows) - nC
    pend = "".join(f'<li>{emp(n, t)}{"" if t.upper() == n.upper() else f" <span class=tkr>{t}</span>"} · {sec}. {note}</li>' for n, t, sec, note in qd["pending"])
    # dividendos
    dv = sorted(qd["divs"], key=lambda x: (x["sort"], x["n"]))
    dtb = ""
    for x in dv:
        dtb += f'<tr><th scope="row" class="txt">{emp(x["n"], x["t"])} <span class="tkr">{x["t"]}</span></th><td>{x["monto"]}</td><td class="txt">{x["tipo"]}</td><td class="txt">{x["limite"]}</td><td class="txt">{x["pago"]}</td><td class="txt">{DBADGE[x["st"]]}</td><td class="txt nt">{x["nota"]}</td></tr>'
    return f'''<section class="cal-q" id="{k}">
<h2 class="cal-title">{qd["label"]}</h2>
<p class="cmp-what">{qd["intro"]} Actualizado al {qd["updated"]}.</p>
<p class="chips"><a href="#{k}-reportes">Reportes de resultados</a><a href="#{k}-dividendos">Dividendos próximos</a></p>
<section id="{k}-dividendos" class="cmp-block"><h3 class="h-sec">Dividendos próximos</h3>
<p class="cmp-what"><b>Confirmado</b>: aprobado por el directorio o la junta, con monto y fechas. <b>Estimado</b>: la empresa suele pagar en estas fechas, pero aún no lo anuncia; el monto es el del año anterior, como referencia. Para recibir el dividendo hay que tener la acción al cierre de la fecha límite.</p>
<div class="table-scroll"><table class="data cal-t"><thead><tr><th scope="col" class="txt">Empresa</th><th scope="col">Monto por acción</th><th scope="col" class="txt">Tipo</th><th scope="col" class="txt">Fecha límite</th><th scope="col" class="txt">Pago</th><th scope="col" class="txt">Estado</th><th scope="col" class="txt">Nota</th></tr></thead><tbody>{dtb}</tbody></table></div>
<p class="small">Sin dividendo esperado en este período (suelen pagar una vez al año, en abril o mayo, o no han pagado recientemente): {qd["nodiv"]}.</p></section>
<section id="{k}-reportes" class="cmp-block"><h3 class="h-sec">Calendario de reportes de resultados</h3>
<p class="cmp-what">{len(rows)} empresas: {nC} con fecha <b>confirmada</b> (informada por la empresa a la CMF o en su sitio de inversionistas) y {nE} con fecha <b>estimada</b> a partir de la fecha del mismo trimestre de 2025. Las estimadas pueden cambiar.</p>
<div class="table-scroll"><table class="data cal-t"><thead><tr><th scope="col" class="txt">Fecha</th><th scope="col" class="txt">Empresa</th><th scope="col" class="txt">Sector</th><th scope="col" class="txt">Estado</th><th scope="col" class="txt">Nota</th></tr></thead><tbody>{tb}</tbody></table></div>
<h3 class="h-sec cal-sub">Sin fecha todavía</h3><ul class="checks">{pend}</ul></section>
</section>'''

# trimestres: el más reciente primero
years = sorted({q["year"] for q in Q}, reverse=True)
tabs = ""
for y in years:
    have = {q["q"]: q for q in Q if q["year"] == y}
    cells = ""
    for n in range(1, 5):
        if n in have: cells += f'<a class="qt on" href="#{have[n]["key"]}">{n}T</a>'
        elif y == 2026 and n < 3: cells += f'<span class="qt off" title="Antes del inicio del calendario">{n}T</span>'
        else: cells += f'<span class="qt off" title="Próximamente">{n}T</span>'
    tabs += f'<div class="cal-year"><span class="yr">{y}</span>{cells}</div>'

tpl = rd("rankings/index.html")
head, rest = tpl.split('<main class="wrap">', 1)
_, foot = rest.split("</main>", 1)
head = re.sub(r"<title>.*?</title>", "<title>Calendario · AI ACCIONES CHILE</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Calendario de reportes de resultados y dividendos próximos de acciones chilenas, por año y trimestre.">', head)
def navfix(t):
    t = t.replace(' aria-current="page"', '')
    return t
head = navfix(head)
main = f'''<main class="wrap">
<section class="page-head"><p class="eyebrow">Calendario</p><h1>Calendario de resultados y dividendos</h1>
<p class="lede">Cuándo publica resultados cada empresa y qué dividendos vienen, ordenado por año y trimestre. Cada fecha indica si está confirmada o es una estimación nuestra.</p>
<nav class="cal-years" aria-label="Año y trimestre">{tabs}</nav></section>
{"".join(quarter(q) for q in Q)}
<p class="note">Fuentes: fechas de divulgación informadas a la CMF (vía findata.cl), sitios de inversionistas de cada empresa, Bolsa de Santiago y prensa financiera. Revisa siempre el hecho esencial de la empresa antes de operar. No es una recomendación de inversión.</p>
</main>'''
page = head + main + foot
page = page.replace('<a href="../calendario/index.html">Calendario</a>', '<a href="../calendario/index.html" aria-current="page">Calendario</a>')
wr("calendario/index.html", page)

# enlace en el menú de todas las páginas (después de Rankings)
for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.relpath(os.path.join(root, f), S); t = rd(p)
        if "calendario/index.html\"" in t and p != "calendario/index.html": continue
        m = re.search(r'<a href="([./]*)rankings/index\.html"( aria-current="page")?>Rankings</a>', t)
        if not m: continue
        cur = ' aria-current="page"' if p == "calendario/index.html" else ""
        if 'calendario/index.html' in t.split('class="nav"', 1)[1].split("</nav>", 1)[0]: continue
        t = t.replace(m.group(0), m.group(0) + f'<a href="{m.group(1)}calendario/index.html"{cur}>Calendario</a>', 1)
        wr(p, t)

css = rd("assets/styles.css")
if ".cal-q" not in css:
    css += """
.cal-years { display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 18px; }
.cal-year { display: flex; align-items: center; gap: 6px; }
.cal-year .yr { font: 700 15px/1 var(--f-mono); margin-right: 4px; }
.qt { font: 600 13px/1 var(--f-mono); padding: 8px 11px; border: 1px solid var(--line); border-radius: 4px; text-decoration: none; }
.qt.on { background: var(--copper); border-color: var(--copper); color: #fff; }
.qt.off { color: var(--muted); opacity: .55; }
.cal-q { margin-top: 28px; }
.cal-title { font-size: 28px; margin: 0 0 8px; }
.cal-sub { margin-top: 26px; }
.cal-t .tkr { font: 500 11px/1 var(--f-mono); color: var(--muted); margin-left: 4px; white-space: nowrap; }
.cal-t .dt { min-width: 90px; font-family: var(--f-mono); font-size: 14px; }
.cal-t .nt { min-width: 220px; font-size: 14px; color: var(--muted); }
.cal-t th.txt, .cal-t td.txt { text-align: left; }
.cal-t tr.wk th { background: var(--copper-soft); text-align: left; font: 600 12px/1 var(--f-mono); text-transform: uppercase; letter-spacing: .06em; color: var(--copper); }
.st { display: inline-block; font: 600 11px/1 var(--f-mono); padding: 5px 7px; border-radius: 3px; }
.st-c { background: rgba(70,170,110,.18); color: #5cc68a; }
.st-e { background: rgba(217,152,43,.18); color: #e0a845; }
"""
    wr("assets/styles.css", css)
print("ok", len(Q[0]["reports"]), len(Q[0]["divs"]))
