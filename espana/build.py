#!/usr/bin/env python3
"""Arma la web de AIAcciones España en espana/web/ (sitio estático, sin dependencias).

Uso:  python3 espana/build.py
Datos: espana/fichas.py (una ficha por empresa, cifras de nuestros vídeos) y espana/datos/calendario-3T26.json.
Al hacer push a main con cambios en espana/web/, .github/workflows/deploy-espana.yml lo publica por FTP.
"""
import datetime as dt
import html
import json
import shutil
from pathlib import Path

from fichas import FICHAS

AQUI = Path(__file__).resolve().parent
WEB = AQUI / "web"
CHILE_CSS = AQUI.parent / "web" / "assets" / "styles.css"

# Rellenar cuando estén: dominio (sin barra final) y datos del titular que exige la LSSI (art. 10).
DOMINIO = "https://aiacciones.es"
TITULAR = {
    "nombre": "Daniel Weinstein",  # nombre y apellidos o razón social
    "empresa": "AIAcciones",       # nombre comercial
    "nif": "",
    "domicilio": "",
    "email": "",
}

YT_CANAL = "https://www.youtube.com/@AIAccionesEspa%C3%B1a"
SITIO = "AIAcciones España"
HOY = dt.date.today()
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

e = html.escape
FICHA_POR_TICKER = {f["ticker"]: f for f in FICHAS}


def fecha_corta(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d.day}-{MESES[d.month - 1]}-{d.year}"


def fecha_dia(iso):
    d = dt.date.fromisoformat(iso)
    return f"{DIAS[d.weekday()]} {d.day} {MESES[d.month - 1]}"


YT_SVG = ('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 '
          '31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8ZM9.7 15.1V8.9l5.8 3.1-5.8 3.1Z"/></svg>')

NAV = [("empresas/index.html", "Empresas"), ("calendario/index.html", "Calendario"),
       ("metodologia/index.html", "Metodología"), ("contacto/index.html", "Contacto")]


def pagina(ruta, titulo, descripcion, cuerpo, actual=None):
    """ruta: carpeta relativa a web/ ('' = portada)."""
    nivel = len([p for p in ruta.split("/") if p])
    r = "../" * nivel
    nav = "".join(f'<a href="{r}{h}"{" aria-current=\"page\"" if t == actual else ""}>{t}</a>' for h, t in NAV)
    canon = ""
    if DOMINIO:
        url = f"{DOMINIO}/{ruta + '/' if ruta else ''}"
        canon = (f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
                 f'<meta property="og:image" content="{DOMINIO}/assets/logo-aiacciones-espana.png">\n')
    titulo_full = titulo if titulo == SITIO else f"{titulo} · {SITIO}"
    return f"""<!doctype html>
<html lang="es-ES">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo_full)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="icon" type="image/png" href="{r}assets/logo-aiacciones-espana-icono.png">
<link rel="apple-touch-icon" href="{r}assets/logo-aiacciones-espana-icono.png">
<link rel="stylesheet" href="{r}assets/styles.css">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITIO}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(titulo_full)}">
<meta property="og:description" content="{e(descripcion)}">
{canon}</head>
<body>
<header class="site-head">
  <div class="bar">
    <a class="brand" href="{r}index.html" aria-label="{SITIO}"><img class="brand-logo" src="{r}assets/logo-aiacciones-espana.png" alt="{SITIO}" width="139" height="44"></a>
    <nav class="nav" aria-label="Secciones">{nav}</nav>
    <a class="xbtn" href="{YT_CANAL}" target="_blank" rel="noopener" aria-label="Canal de YouTube">{YT_SVG}<span>YouTube</span></a>
  </div>
</header>
<main class="wrap">
{cuerpo}
</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <p class="brand-sm">AIACCIONES ESPAÑA</p>
      <p>Resultados de las cotizadas españolas explicados en vídeo, con las cifras que publica cada empresa en la CNMV. Síguenos en <a href="{YT_CANAL}" target="_blank" rel="noopener">YouTube</a> o escríbenos desde <a href="{r}contacto/index.html">Contacto</a>.</p>
    </div>
    <div class="disclaimer">
      <p><b>Aviso.</b> Contenido informativo y educativo. No es una recomendación de inversión ni asesoramiento personalizado, y no emitimos precio objetivo ni opinión sobre si una acción está cara o barata. AIAcciones España no tiene posiciones en las empresas analizadas. Invertir en bolsa implica riesgo de pérdida, incluso de todo el capital. Verifica siempre las cifras en la <a href="https://www.cnmv.es" target="_blank" rel="noopener">CNMV</a>.</p>
      <p><a href="{r}aviso-legal/index.html">Aviso legal</a> · <a href="{r}privacidad/index.html">Privacidad y cookies</a> · <a href="{r}metodologia/index.html">Metodología</a> · <a href="{r}contacto/index.html">Contacto</a></p>
    </div>
  </div>
</footer>
<script src="{r}assets/app.js" defer></script>
</body>
</html>
"""


def aviso_ficha(f):
    return f"""<section class="aviso-es" id="aviso">
<h2 class="h-sec">Aviso importante</h2>
<ul>
<li>Elaborado por AIAcciones España el {e(f['elaborado'])} (hora de Madrid). Se actualiza con cada informe trimestral de la empresa.</li>
<li>Contenido informativo y educativo sobre información pública. No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoramiento personalizado: no tiene en cuenta tu situación, objetivos ni perfil de riesgo. Antes de invertir, consulta a una entidad autorizada por la CNMV.</li>
<li>Hechos y opiniones: las cifras proceden de la información que {e(f['nombre'])} publica en la CNMV y en su web, y de las fuentes de mercado indicadas ({e(f['fuentes_corto'])}). Los cálculos propios están marcados como «calculado». No emitimos precio objetivo ni opinión sobre si la acción está cara o barata.</li>
<li>Metodología de valoración: múltiplos (PER, EV/EBITDA, rentabilidad por dividendo y por flujo libre) calculados con el precio de la fecha indicada y comparados con los de la propia empresa en años anteriores. Hipótesis: datos publicados, sin estimaciones propias de resultados futuros.</li>
<li>Conflictos de interés: AIAcciones España y sus autores no tienen posiciones en las empresas analizadas, no reciben pago de ellas y el contenido no se ha enviado a la empresa antes de publicarse. Cualquier cambio se indicará aquí.</li>
<li>Riesgos: invertir en bolsa implica riesgo de pérdida, incluso de todo el capital. Las rentabilidades pasadas no garantizan rentabilidades futuras. Los datos pueden contener errores; verifícalos en las fuentes originales.</li>
<li>Producción: guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas.</li>
</ul>
</section>"""


def videos_html(f):
    return "".join(
        f'<a class="vid" href="https://youtu.be/{v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{e(t)}</span></a>'
        for v, t in f["videos"])


def ficha(f):
    tiles = "".join(f'<div class="tile"><span class="lbl">{e(a)}</span><span class="val">{e(b)}</span></div>' for a, b in f["multiplos"])
    filas = "".join(
        f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td class="{"neg" if c.startswith(("−", "-")) else ""}">{e(c) or "—"}</td></tr>'
        for a, b, c in f["tabla"])
    prox = f"{fecha_dia(f['proximo'])} de {f['proximo'][:4]}" + (" (fecha estimada)" if f.get("proximo_estimado") else "")
    cuerpo = f"""<nav class="crumbs"><a href="../index.html">Empresas</a> / {e(f['ticker'])}</nav>
<section class="page-head stock-head">
  <div>
    <p class="eyebrow">{e(f['sector'])}</p>
    <h1>{e(f['nombre'])}</h1>
    <p class="lede">{e(f['lede'])}</p>
  </div>
  <div class="quote">
    <span class="tk">{e(f['ticker'])}</span>
    <span class="px">{e(f['precio'])}</span>
    <span class="note">Precio usado en el vídeo ({e(f['precio_fecha'])})</span>
    <span class="note">Próximo informe: {e(prox)}</span>
  </div>
</section>
<section><h2 class="h-sec">El titular del {e(f['periodo'])}</h2><p class="kpi-line">{e(f['titular'])}</p></section>
<section><h2 class="h-sec">Resultados del {e(f['periodo_largo'])}</h2><div class="table-scroll"><table class="data">
<caption>{e(f['tabla_titulo'])}</caption>
<thead><tr><th scope="col">Concepto</th><th>{e(f['periodo'])}</th><th>Var. a/a</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="kpi-line">{e(f['kpi'])}</p></section>
<section><h2 class="h-sec">Guía y dividendo</h2><p class="kpi-line">{e(f['guia'])}</p></section>
<section><h2 class="h-sec">Valoración</h2><div class="tiles">{tiles}</div>
<p class="small">{e(f['multiplos_nota'])} Son datos de mercado, no una opinión sobre si la acción está cara o barata.</p></section>
<section class="two">
  <div><h2 class="h-sec">Qué cambió</h2>
  <p class="small"><b>Tres positivos</b></p><ul class="checks">{"".join(f"<li>{e(x)}</li>" for x in f['positivos'])}</ul>
  <p class="small"><b>Tres riesgos</b></p><ul class="checks risks">{"".join(f"<li>{e(x)}</li>" for x in f['riesgos'])}</ul></div>
  <div class="aside-box"><h2 class="h-sec">Vídeos</h2><div class="vids">{videos_html(f)}</div></div>
</section>
<section><h2 class="h-sec">Fuentes</h2><p class="small">{e(f['fuentes'])} Las cifras marcadas como calculadas son cálculos propios.</p></section>
{aviso_ficha(f)}"""
    desc = f"{f['nombre']} ({f['ticker']}): resultados del {f['periodo_largo']}, guía, valoración y vídeo. {f['titular'][:110]}"
    return pagina(f"empresas/{f['id']}", f"{f['nombre']} ({f['ticker']}) resultados {f['periodo']}", desc, cuerpo, "Empresas")


def tarjeta(f, r):
    return (f'<a class="stock-card" href="{r}empresas/{f["id"]}/index.html"><span class="tk">{e(f["ticker"])}</span>'
            f'<span class="nm">{e(f["nombre"])}</span><span class="sc">{e(f["sector"])}</span>'
            f'<span class="row"><span>{e(f["periodo"])}</span><span>Próx. <b>{e(fecha_corta(f["proximo"]))}</b></span></span></a>')


def calendario_tabla(cal, r, solo_proximos=None):
    filas, semana = [], None
    con_fecha = [c for c in cal["empresas"] if c["fecha"]]
    if solo_proximos:
        con_fecha = [c for c in con_fecha if c["fecha"] >= HOY.isoformat()][:solo_proximos]
    for c in con_fecha:
        d = dt.date.fromisoformat(c["fecha"])
        lunes = d - dt.timedelta(days=d.weekday())
        if not solo_proximos and lunes != semana:
            semana = lunes
            filas.append(f'<tr class="wk"><th colspan="5">Semana del {lunes.day} de {MESES[lunes.month - 1]}</th></tr>')
        filas.append(fila_cal(c, r, fecha_dia(c["fecha"])))
    if not solo_proximos:
        pend = [c for c in cal["empresas"] if not c["fecha"]]
        if pend:
            filas.append('<tr class="wk"><th colspan="5">Por confirmar</th></tr>')
            filas += [fila_cal(c, r, "—") for c in pend]
    return ('<div class="table-scroll"><table class="data cal-t"><thead><tr><th scope="col" class="txt">Fecha</th>'
            '<th scope="col" class="txt">Empresa</th><th scope="col" class="txt">Sector</th><th scope="col" class="txt">Estado</th>'
            f'<th scope="col" class="txt">Nota</th></tr></thead><tbody>{"".join(filas)}</tbody></table></div>')


def fila_cal(c, r, fecha):
    f = FICHA_POR_TICKER.get(c["ticker"])
    nombre = f'<a href="{r}empresas/{f["id"]}/index.html">{e(c["empresa"])}</a>' if f else e(c["empresa"])
    st = {"Confirmada": "st-c", "Estimada": "st-e"}.get(c["estado"], "st-p")
    return (f'<tr><td class="txt dt">{e(fecha)}</td><th scope="row" class="txt">{nombre} <span class="tkr">{e(c["ticker"])}</span></th>'
            f'<td class="txt">{e(c["sector"])}</td><td class="txt"><span class="st {st}">{e(c["estado"])}</span></td>'
            f'<td class="txt nt">{e(c["nota"])}</td></tr>')


def portada(cal):
    cards = "".join(tarjeta(f, "") for f in FICHAS)
    cuerpo = f"""<section class="hero">
  <p class="eyebrow">IBEX 35 · Mercado Continuo</p>
  <h1>Los resultados de las cotizadas españolas, <b>explicados en vídeo</b>.</h1>
  <p class="lede">Cada vez que una empresa del IBEX 35 publica sus cuentas en la CNMV, lo resumimos en un vídeo de unos cinco minutos: ingresos, beneficio por acción, márgenes, deuda, guía, múltiplos frente a su propia historia, y lo que cambió. Solo cifras publicadas, con sus fuentes.</p>
  <div class="hero-cta"><a class="btn" href="{YT_CANAL}" target="_blank" rel="noopener">Ver el canal de YouTube</a><a class="btn ghost" href="calendario/index.html">Calendario de resultados</a></div>
</section>
<section><h2 class="h-sec">Próximos resultados · {e(cal['trimestre'])}</h2>
{calendario_tabla(cal, "", solo_proximos=8)}
<p class="small">Las empresas suelen publicar antes de la apertura (07:00-08:00, hora de Madrid). <a href="calendario/index.html">Ver el calendario completo</a>.</p></section>
<section><h2 class="h-sec">Últimos análisis</h2><div class="stock-grid">{cards}</div></section>
<section><h2 class="h-sec">Secciones</h2><div class="sec-grid">
<a class="sec-link" href="empresas/index.html"><span class="sec-t">Empresas</span><span class="sec-d">Una ficha por empresa con las cifras del último informe, la guía, los múltiplos y el vídeo.</span></a>
<a class="sec-link" href="calendario/index.html"><span class="sec-t">Calendario</span><span class="sec-d">Fechas de resultados del {e(cal['trimestre'])} de las empresas del IBEX 35, confirmadas y estimadas.</span></a>
<a class="sec-link" href="metodologia/index.html"><span class="sec-t">Metodología</span><span class="sec-d">De dónde salen las cifras, cómo calculamos los múltiplos y qué no hacemos.</span></a>
</div></section>"""
    return pagina("", SITIO, "Resultados de las empresas del IBEX 35 explicados en vídeo: ingresos, beneficio, márgenes, deuda, guía y múltiplos, con fuentes de la CNMV.", cuerpo)


def empresas():
    cards = "".join(tarjeta(f, "../") for f in FICHAS)
    cuerpo = f"""<section class="page-head"><p class="eyebrow">Fichas</p><h1>Empresas analizadas</h1>
<p class="lede">Cada ficha resume nuestro último vídeo de resultados de la empresa. Iremos sumando empresas del IBEX 35 a medida que publiquen sus cuentas del tercer trimestre.</p></section>
<section><div class="stock-grid">{cards}</div></section>"""
    return pagina("empresas", "Empresas", "Fichas de resultados de las empresas del IBEX 35 analizadas por AIAcciones España.", cuerpo, "Empresas")


def calendario(cal):
    act = fecha_corta(cal["actualizado"])
    cuerpo = f"""<section class="page-head"><p class="eyebrow">IBEX 35</p><h1>Calendario de resultados {e(cal['trimestre'])}</h1>
<p class="lede">Cuándo publica cada empresa del IBEX 35 sus cuentas del tercer trimestre. <span class="st st-c">Confirmada</span> es una fecha publicada por la empresa o por la prensa este año; <span class="st st-e">Estimada</span> repite la semana en que publicó el año pasado. Las empresas suelen publicar antes de la apertura (07:00-08:00, hora de Madrid) como «Otra información relevante» en la CNMV.</p></section>
<section>{calendario_tabla(cal, "../")}
<p class="note">Actualizado el {e(act)}. Fuentes: calendarios del inversor de cada empresa, DailyForex, PcBolsa y Bolsamanía. Fuente oficial: <a href="https://www.cnmv.es" target="_blank" rel="noopener">CNMV</a>.</p></section>"""
    return pagina("calendario", f"Calendario de resultados {cal['trimestre']} IBEX 35", f"Fechas de presentación de resultados del {cal['trimestre']} de las empresas del IBEX 35.", cuerpo, "Calendario")


def metodologia():
    cuerpo = """<section class="page-head"><p class="eyebrow">Cómo trabajamos</p><h1>Metodología</h1></section>
<section class="prose">
<h2>De dónde salen las cifras</h2>
<p>De la información que cada empresa publica en la CNMV («Otra información relevante») y en su web de accionistas: notas de prensa, presentaciones e informes de resultados. La comparación con el consenso cita siempre a quien lo publica (por ejemplo, Bankinter Análisis, Renta 4 o Investing.com). Precio y múltiplos de mercado salen de proveedores públicos, con la fecha indicada.</p>
<h2>Qué calculamos nosotros</h2>
<p>Algunos datos no vienen directos en el informe: beneficio por acción con el número de acciones, márgenes, deuda neta sobre EBITDA o el porcentaje de la guía ya alcanzado. Los marcamos siempre como «calculado».</p>
<h2>Valoración</h2>
<p>Mostramos múltiplos (PER de los últimos 12 meses y forward, EV/EBITDA, rentabilidad por dividendo y por flujo de caja libre) y los comparamos con los de la propia empresa en años anteriores. No hacemos estimaciones propias de resultados futuros, no emitimos precio objetivo y no decimos si una acción está cara o barata.</p>
<h2>Estructura de cada vídeo</h2>
<p>1) El titular: mejor o peor de lo esperado. 2) Ingresos. 3) Beneficio por acción. 4) Márgenes, inversión y deuda. 5) Guía. 6) Valoración frente a su historia. 7) Qué cambió: tres positivos y tres riesgos.</p>
<h2>Uso de inteligencia artificial</h2>
<p>El guion, los gráficos y la locución (voz sintética) se generan con herramientas de inteligencia artificial y se revisan con las fuentes citadas. Si encuentras un error, avísanos en los comentarios del vídeo y lo corregiremos indicándolo.</p>
</section>"""
    return pagina("metodologia", "Metodología", "De dónde salen las cifras de AIAcciones España, qué calculamos y cómo presentamos la valoración.", cuerpo, "Metodología")


def aviso_legal():
    datos = [("Titular", TITULAR["nombre"] or SITIO), ("Empresa", TITULAR.get("empresa", "")), ("NIF", TITULAR["nif"]), ("Domicilio", TITULAR["domicilio"]),
             ("Correo de contacto", TITULAR["email"])]
    filas = "".join(f"<li><b>{a}:</b> {e(b)}</li>" for a, b in datos if b)
    cuerpo = f"""<section class="page-head"><p class="eyebrow">Información legal</p><h1>Aviso legal</h1></section>
<section class="prose">
<h2>Titular del sitio</h2>
<ul>{filas}</ul>
<p>En cumplimiento de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI).</p>
<h2>Naturaleza del contenido</h2>
<p>Contenido informativo y educativo sobre información pública. No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoramiento personalizado: no tiene en cuenta tu situación, objetivos ni perfil de riesgo. Antes de invertir, consulta a una entidad autorizada por la CNMV.</p>
<h2>Hechos y opiniones</h2>
<p>Las cifras proceden de la información que cada empresa publica en la CNMV y en su web, y de las fuentes de mercado indicadas en cada ficha y vídeo. Los cálculos propios están marcados como «calculado». No emitimos precio objetivo ni opinión sobre si una acción está cara o barata. Cada ficha indica la fecha y hora (de Madrid) en que se elaboró y sus fuentes.</p>
<h2>Metodología de valoración</h2>
<p>Múltiplos (PER, EV/EBITDA, rentabilidad por dividendo y por flujo libre) calculados con el precio de la fecha indicada y comparados con los de la propia empresa en años anteriores. Hipótesis: datos publicados, sin estimaciones propias de resultados futuros. Más detalle en <a href="../metodologia/index.html">Metodología</a>.</p>
<h2>Conflictos de interés</h2>
<p>AIAcciones España y sus autores no tienen posiciones en las empresas analizadas, no reciben pago de ellas y el contenido no se ha enviado a la empresa antes de publicarse. Cualquier cambio se indicará en esta página y en la ficha correspondiente.</p>
<h2>Riesgos</h2>
<p>Invertir en bolsa implica riesgo de pérdida, incluso de todo el capital. Las rentabilidades pasadas no garantizan rentabilidades futuras. Los datos pueden contener errores; verifícalos en las fuentes originales.</p>
<h2>Producción</h2>
<p>Guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, gráficos y vídeos de AIAcciones España son de su titular. Las marcas y logotipos de las empresas analizadas pertenecen a sus dueños y se citan solo para identificarlas.</p>
</section>"""
    return pagina("aviso-legal", "Aviso legal", "Aviso legal de AIAcciones España: titular, naturaleza informativa del contenido, conflictos de interés y riesgos.", cuerpo, "Aviso legal")


def privacidad():
    responsable = ", ".join(x for x in (TITULAR["nombre"], TITULAR.get("empresa", "")) if x) or SITIO
    cuerpo = f"""<section class="page-head"><p class="eyebrow">Información legal</p><h1>Privacidad y cookies</h1></section>
<section class="prose">
<h2>Formulario de contacto</h2>
<p>Si nos escribes desde la página de <a href="../contacto/index.html">Contacto</a>, tratamos tu nombre, tu correo y tu mensaje con un único fin: responderte. Responsable: {e(responsable)}{" (" + e(TITULAR["email"]) + ")" if TITULAR["email"] else ""}. Base legal: tu consentimiento, que das al marcar la casilla del formulario (art. 6.1.a del RGPD). El mensaje llega a nuestro correo de Gmail (Google), por lo que Google actúa como proveedor de correo. Conservamos los mensajes el tiempo necesario para responderte y, como máximo, un año; no los cedemos a terceros ni los usamos para enviarte publicidad.</p>
<p>Puedes pedir el acceso, la rectificación o la supresión de tus datos, oponerte a su tratamiento o retirar tu consentimiento escribiéndonos desde el mismo formulario. Si crees que no hemos atendido bien tu solicitud, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" target="_blank" rel="noopener">aepd.es</a>).</p>
<h2>Otros datos</h2>
<p>Este sitio no tiene registro de usuarios. El servidor de alojamiento puede guardar registros técnicos de acceso (como la dirección IP) por seguridad, durante el tiempo que fije el proveedor.</p>
<h2>Cookies</h2>
<p>Este sitio no usa cookies propias ni de terceros, ni herramientas de analítica o publicidad. Las tipografías son las del sistema y los vídeos se enlazan a YouTube sin incrustarlos: solo al abrir un vídeo pasas a YouTube, que aplica su propia política de privacidad.</p>
<p>Si en el futuro añadimos analítica o publicidad, lo indicaremos aquí y pediremos tu consentimiento antes de activar cualquier cookie no necesaria.</p>
</section>"""
    return pagina("privacidad", "Privacidad y cookies", "Política de privacidad y cookies de AIAcciones España.", cuerpo)


def contacto():
    cuerpo = """<section class="page-head"><p class="eyebrow">Contacto</p><h1>Escríbenos</h1>
<p class="lede">Propón una empresa para el próximo vídeo, envía una corrección o haz una pregunta. Te respondemos al correo que nos dejes.</p></section>
<div class="two">
<form id="contact" class="contact" action="../enviar.php" method="POST">
  <input type="hidden" name="_t" value="">
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label for="c-nombre">Nombre<input id="c-nombre" name="nombre" required maxlength="100" autocomplete="name"></label>
  <label for="c-email">Correo electrónico<input id="c-email" name="email" type="email" required maxlength="150" autocomplete="email"></label>
  <label for="c-asunto">Asunto<select id="c-asunto" name="asunto">
    <option>Propuesta de empresa para analizar</option><option>Pregunta sobre un vídeo</option><option>Corrección de datos</option><option>Otro</option></select></label>
  <label for="c-mensaje">Mensaje<textarea id="c-mensaje" name="mensaje" rows="6" required maxlength="5000"></textarea></label>
  <label class="chk"><input type="checkbox" name="privacidad" value="si" required> <span>He leído la <a href="../privacidad/index.html">política de privacidad</a> y acepto que usen mis datos para responderme.</span></label>
  <button class="btn" type="submit" id="c-send">Enviar mensaje</button>
  <p class="form-msg" id="c-msg" role="status" hidden></p>
</form>
<aside class="aside-box"><h2 class="h-sec">Antes de escribir</h2>
<p>No damos recomendaciones de inversión ni asesoramiento personalizado, así que no podemos responder si debes comprar o vender una acción.</p>
<p>Si encuentras un error en una cifra, indícanos la empresa, el dato y la fuente: lo corregiremos indicándolo en la ficha y en el vídeo.</p></aside>
</div>"""
    return pagina("contacto", "Contacto", "Escribe a AIAcciones España: propuestas de empresas, preguntas y correcciones.", cuerpo, "Contacto")


EXTRA_CSS = """
/* ---------- AIAcciones España: tipografías del sistema (sin Google Fonts) y piezas propias */
:root {
  --f-display: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --f-body: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --f-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}
.st-p { background: rgba(255,255,255,.08); color: var(--muted); }
.checks.risks li::before { border-color: var(--down); }
.aviso-es { padding: 18px 20px; border: 1px dashed var(--line); border-radius: 4px; font-size: 14px; color: var(--muted); }
.aviso-es ul { margin: 0; padding-left: 18px; display: grid; gap: 6px; }
.prose ul { padding-left: 18px; }
.contact .chk { display: flex; gap: 10px; align-items: flex-start; font-weight: 400; font-size: 14px; color: var(--muted); }
.contact .chk input { margin-top: 4px; }
"""


def escribir(ruta, contenido):
    p = WEB / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")


def main():
    cal = json.loads((AQUI / "datos" / "calendario-3T26.json").read_text(encoding="utf-8"))
    css = CHILE_CSS.read_text(encoding="utf-8")
    escribir("assets/styles.css", css + EXTRA_CSS)
    escribir("index.html", portada(cal))
    escribir("empresas/index.html", empresas())
    for f in FICHAS:
        escribir(f"empresas/{f['id']}/index.html", ficha(f))
    escribir("calendario/index.html", calendario(cal))
    escribir("metodologia/index.html", metodologia())
    escribir("aviso-legal/index.html", aviso_legal())
    escribir("privacidad/index.html", privacidad())
    escribir("contacto/index.html", contacto())
    for nombre, destino in (("enviar.php", "enviar.php"), ("app.js", "assets/app.js")):
        shutil.copyfile(AQUI / "extra" / nombre, WEB / destino)
    if DOMINIO:
        rutas = ["", "empresas/", "calendario/", "metodologia/", "aviso-legal/", "privacidad/", "contacto/"] + [f"empresas/{f['id']}/" for f in FICHAS]
        urls = "".join(f"<url><loc>{DOMINIO}/{r}</loc><lastmod>{HOY.isoformat()}</lastmod></url>" for r in rutas)
        escribir("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
        escribir("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    else:
        escribir("robots.txt", "User-agent: *\nAllow: /\n")
    print("Web de España armada en", WEB)


if __name__ == "__main__":
    main()
