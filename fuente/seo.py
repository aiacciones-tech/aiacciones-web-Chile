# SEO / IA para la versión zip (aiacciones.cl). Se ejecuta desde mkzip.sh sobre web/.
import re, os, glob, json, html, datetime
W = os.environ.get("WEB", "web")
BASE = "https://aiacciones.cl/"
TODAY = datetime.date.today().isoformat()
LOGO = BASE + "assets/logo-aiacciones-chile.png"
DESC = {
 "index.html": "Resultados trimestrales de las principales acciones chilenas explicados en simple: fichas por empresa, valoraciones, comparadores, rankings, calendario de reportes y dividendos, y videos.",
 "acciones/index.html": "Fichas de acciones chilenas del IPSA y más: resultados del último trimestre, múltiplos de valoración, dividendos y video de análisis de cada empresa.",
 "resultados/index.html": "Resultados trimestrales de empresas chilenas: ingresos, EBITDA y utilidad frente al año anterior y frente al consenso de analistas.",
 "valoraciones/index.html": "Múltiplos de valoración de acciones chilenas: P/E, forward P/E, P/BV, EV/EBITDA, dividend yield y ROE en una sola tabla.",
 "rankings/index.html": "Ranking y filtro de acciones chilenas por P/E, crecimiento de utilidades, dividend yield y caída de precio.",
 "comparadores/index.html": "Comparadores de acciones chilenas por sector: bancos, retail, energía, centros comerciales, AFP y más, con gráficos y resultados trimestrales.",
 "educacion/index.html": "Conceptos para analizar acciones explicados en simple: P/E, EBITDA, flujo de caja libre, dividend yield, deuda y más.",
 "contacto/index.html": "Escríbenos para sugerir empresas, reportar un error o proponer una colaboración con AI Acciones Chile.",
 "privacidad/index.html": "Política de privacidad de AI Acciones Chile: uso de cookies, Google Analytics y Google AdSense.",
 "nosotros/index.html": "Quiénes somos: AI Acciones Chile explica en simple los resultados trimestrales de las empresas de la Bolsa de Santiago. Qué publicamos, de dónde salen las cifras y cómo hacemos cada análisis.",
 "aviso-legal/index.html": "Aviso legal de AI Acciones Chile: el contenido es informativo y educativo, no una recomendación de inversión. Fuentes, riesgos, publicidad y uso del contenido.",
}
TITLE = {"index.html": "AI Acciones Chile · Resultados y análisis de acciones chilenas"}
DEFAULT_GENERIC = "Análisis de acciones chilenas: resultados, valoraciones, comparadores, rankings y educación financiera."

def url_of(rel):
    d = os.path.dirname(rel)
    return BASE + (d + "/" if d else "")

def meta_of(s, name):
    m = re.search(r'<meta name="%s" content="(.*?)">' % name, s)
    return m.group(1) if m else ""

pages = []
for p in sorted(glob.glob(W + "/**/*.html", recursive=True)):
    rel = os.path.relpath(p, W)
    s = open(p, encoding="utf-8").read()
    if rel in DESC:
        s = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % DESC[rel], s, count=1)
    if rel in TITLE:
        s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE[rel], s, count=1)
    title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).replace("AI ACCIONES CHILE", "AI Acciones Chile")
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % html.escape(title, quote=False), s, count=1)
    desc = meta_of(s, "description")
    lede = re.search(r'<p class="lede">(.*?)</p>', s, re.S)
    if desc.startswith("Ficha de") and lede:
        first = re.split(r"(?<=\.)\s", re.sub("<[^>]+>", "", lede.group(1)).strip())[0]
        nd = desc.rstrip(".") + ". " + first
        if len(nd) <= 200:
            s = s.replace('<meta name="description" content="%s">' % desc, '<meta name="description" content="%s">' % nd.replace('"', "&quot;"), 1)
            desc = meta_of(s, "description")
    assert desc and desc != DEFAULT_GENERIC, rel
    url = url_of(rel)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    h1 = re.sub("<[^>]+>", "", h1.group(1)).strip() if h1 else title
    kind = "Article" if rel.startswith(("acciones/", "comparadores/", "analisis-tecnico/")) and rel.count("/") == 2 else "WebPage"
    crumbs = [("Inicio", BASE)]
    parts = rel.split("/")[:-1]
    for i, part in enumerate(parts):
        crumbs.append((h1 if i == len(parts) - 1 else part.replace("-", " ").capitalize(), BASE + "/".join(parts[:i + 1]) + "/"))
    graph = [{"@type": kind, "@id": url + "#page", "url": url, "name": title, "headline": h1, "description": desc,
              "inLanguage": "es-CL", "dateModified": TODAY, "isPartOf": {"@id": BASE + "#website"},
              "publisher": {"@id": BASE + "#org"}, "image": LOGO}]
    if kind == "Article":
        graph[0]["author"] = {"@id": BASE + "#org"}
    if len(crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    if rel == "index.html":
        graph += [{"@type": "Organization", "@id": BASE + "#org", "name": "AI Acciones Chile", "url": BASE, "logo": LOGO,
                   "sameAs": ["https://www.youtube.com/channel/UCDGmimmfYaYYP1jYBo6bA3g", "https://x.com/aiacciones"]},
                  {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "AI Acciones Chile", "inLanguage": "es-CL", "publisher": {"@id": BASE + "#org"}}]
    vid = re.search(r"youtube(?:-nocookie)?\.com/embed/([\w-]{11})", s)
    if vid:
        graph.append({"@type": "VideoObject", "name": h1, "description": desc, "thumbnailUrl": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid.group(1),
                      "embedUrl": "https://www.youtube.com/embed/%s" % vid.group(1), "contentUrl": "https://www.youtube.com/watch?v=%s" % vid.group(1), "inLanguage": "es-CL"})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    et = html.escape(title); ed = html.escape(html.unescape(desc))
    tags = (f'<link rel="canonical" href="{url}">\n<meta name="robots" content="index, follow, max-image-preview:large">\n'
            f'<meta property="og:type" content="{"article" if kind == "Article" else "website"}">\n<meta property="og:site_name" content="AI Acciones Chile">\n'
            f'<meta property="og:locale" content="es_CL">\n<meta property="og:title" content="{et}">\n<meta property="og:description" content="{ed}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{LOGO}">\n'
            f'<meta name="twitter:card" content="summary">\n<meta name="twitter:site" content="@aiacciones">\n<meta name="twitter:title" content="{et}">\n'
            f'<meta name="twitter:description" content="{ed}">\n<meta name="twitter:image" content="{LOGO}">\n'
            f'<script type="application/ld+json">{ld}</script>\n')
    if 'rel="canonical"' not in s:
        s = s.replace("</head>", tags + "</head>", 1)
    # Rankings: tabla prerenderizada para buscadores e IA sin JavaScript (app.js la reemplaza al cargar)
    if rel == "rankings/index.html" and '<tbody></tbody>' in s:
        data = json.loads(re.search(r"window.RANK_DATA=(\[.*?\]);?</script>", s, re.S).group(1))
        def f(v, suf):
            if v is None: return "n/a"
            return ("−" if v < 0 else "") + f"{abs(v):,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") + suf
        lk = lambda d: '<a href="../acciones/%s/index.html">%s</a>' % (d["id"], d["t"]) if d.get("link") else d["t"]
        rows = sorted(data, key=lambda d: (d["pe"] is None, d["pe"] or 0))
        tb = "".join(f'<tr><td>{i+1}</td><th scope="row">{lk(d)}</th><td class="txt">{d["s"]}</td><td>{f(d["pe"],"x")}</td><td class="{"neg" if (d["epsg"] or 0) < 0 else ""}">{f(d["epsg"],"%")}</td><td>{f(d["dy"],"%")}</td><td class="{"down" if (d["chg"] or 0) < 0 else "up"}">{"+" if (d["chg"] or 0) > 0 else ""}{f(d["chg"],"%")}</td></tr>' for i, d in enumerate(rows))
        s = s.replace("<tbody></tbody>", "<tbody>" + tb + "</tbody>", 1)
    open(p, "w", encoding="utf-8").write(s)
    pages.append((rel, url, title, html.unescape(desc)))

# sitemap.xml
pri = lambda rel: "1.0" if rel == "index.html" else ("0.8" if rel.count("/") == 1 else "0.6")
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for rel, url, _, _ in pages:
    if rel in ("privacidad/index.html", "aviso-legal/index.html"): continue
    sm += f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>{pri(rel)}</priority></url>\n"
open(W + "/sitemap.xml", "w").write(sm + "</urlset>\n")

# robots.txt: todo abierto, incluidos buscadores de IA
open(W + "/robots.txt", "w").write("User-agent: *\nAllow: /\nDisallow: /enviar.php\n\n# Buscadores e IA bienvenidos\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: " + BASE + "sitemap.xml\n")

# llms.txt: mapa del sitio para asistentes de IA
groups = [("Secciones principales", lambda r: r.count("/") == 1 and r != "privacidad/index.html"),
          ("Fichas de empresas (resultados 2T 2026)", lambda r: r.startswith("acciones/") and r.count("/") == 2),
          ("Comparadores por sector", lambda r: r.startswith("comparadores/") and r.count("/") == 2),
          ("Curso de análisis técnico", lambda r: r.startswith("analisis-tecnico/") and r.count("/") == 2)]
lt = ("# AI Acciones Chile\n\n> Sitio en español sobre acciones chilenas: resultados trimestrales explicados en simple, múltiplos de valoración, comparadores sectoriales, rankings, calendario de reportes y dividendos, y videos en YouTube. Las cifras salen de estados financieros, análisis razonados y fuentes de mercado. No es recomendación de inversión.\n\n"
      "- Período actual: segundo trimestre de 2026 (se actualiza cada trimestre).\n- YouTube: https://www.youtube.com/channel/UCDGmimmfYaYYP1jYBo6bA3g\n- X: https://x.com/aiacciones\n\n")
for g, cond in groups:
    lt += f"## {g}\n\n" + "".join(f"- [{t.replace(' · AI Acciones Chile', '')}]({u}): {d}\n" for r, u, t, d in pages if cond(r)) + "\n"
open(W + "/llms.txt", "w").write(lt)
print("seo ok", len(pages), "pages")
