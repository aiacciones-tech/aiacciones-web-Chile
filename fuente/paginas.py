# Páginas institucionales: Quiénes somos (nosotros/) y Aviso legal (aviso-legal/). Plantilla: privacidad/.
# uso: cd fuente && python3 paginas.py   (edita site/)
import os, re
S = os.environ.get("SITE", os.path.abspath("site"))
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(os.path.join(S, p)), exist_ok=True)
    open(os.path.join(S, p), "w", encoding="utf-8").write(t)

tpl = rd("privacidad/index.html")
head, rest = tpl.split('<main class="wrap">', 1)
_, foot = rest.split("</main>", 1)

PAGES = {
"nosotros": ("Quiénes somos", "Nosotros",
 "Qué es AI Acciones Chile, qué publicamos y cómo hacemos cada análisis.",
 """<h2>Qué es AI Acciones Chile</h2>
<p>AI Acciones Chile es un proyecto independiente que explica en simple los resultados trimestrales de las empresas que cotizan en la Bolsa de Santiago. Cada vez que una empresa publica sus estados financieros hacemos un video de análisis, que publicamos en <a href="https://www.youtube.com/channel/UCDGmimmfYaYYP1jYBo6bA3g" target="_blank" rel="noopener">YouTube</a> y en <a href="https://x.com/aiacciones" target="_blank" rel="noopener">X (@aiacciones)</a>, y este sitio reúne todas esas cifras en un solo lugar.</p>
<h2>Qué encontrarás en el sitio</h2>
<ul>
<li><a href="../acciones/index.html">Fichas por empresa</a>: resultados del trimestre frente al año anterior, múltiplos de valoración, deuda, qué mirar y el video del análisis.</li>
<li><a href="../comparadores/index.html">Comparadores por sector</a>: energía, retail, centros comerciales y AFP, con gráficos y una lectura de cada bloque.</li>
<li><a href="../valoraciones/index.html">Valoraciones</a> y <a href="../rankings/index.html">rankings</a> para filtrar empresas por P/E, crecimiento, dividendo o caída de precio.</li>
<li><a href="../calendario/index.html">Calendario</a> de entrega de resultados y de dividendos.</li>
<li>Los índices IPSA e IGPA, los precios de cierre y los hechos esenciales de la CMF, que se actualizan solos cada día hábil.</li>
<li>Un curso de <a href="../educacion/index.html">conceptos financieros</a> y otro de <a href="../analisis-tecnico/index.html">análisis técnico</a>, explicados con ejemplos.</li>
</ul>
<h2>Cómo hacemos cada análisis</h2>
<p>Todos los análisis siguen la misma estructura, para que puedas comparar una empresa con otra:</p>
<ol>
<li><b>El titular:</b> si el trimestre fue mejor o peor de lo esperado y qué cambió.</li>
<li><b>Ingresos:</b> cuánto vendió, cuánto creció frente al año anterior y frente a lo que esperaban los analistas.</li>
<li><b>Utilidad por acción:</b> cuánto ganó y la sorpresa frente al consenso.</li>
<li><b>Márgenes y flujo de caja:</b> margen bruto, operacional y EBITDA, flujo de caja libre y deuda.</li>
<li><b>Guía de la empresa:</b> si subió, mantuvo o bajó sus proyecciones.</li>
<li><b>Valoración:</b> P/E, forward P/E, EV/EBITDA, FCF yield y dividendo, comparados con su historia y con sus pares.</li>
<li><b>Qué cambió:</b> tres puntos positivos y tres riesgos a vigilar.</li>
</ol>
<h2>De dónde salen las cifras</h2>
<p>Usamos fuentes públicas: los estados financieros y análisis razonados que las empresas entregan a la <a href="https://www.cmfchile.cl" target="_blank" rel="noopener">CMF</a>, sus comunicados y presentaciones a inversionistas y, en el caso de las AFP, los estados financieros que publica la <a href="https://www.spensiones.cl" target="_blank" rel="noopener">Superintendencia de Pensiones</a>. El consenso de analistas y los múltiplos históricos vienen de servicios como Investing.com y MarketScreener, y los precios diarios de TradingView. Cuando una cifra la calculamos nosotros (por ejemplo, un trimestre como la diferencia entre el semestre y el primer trimestre) la marcamos con <b>(c)</b>. Cada video cita sus fuentes.</p>
<h2>Por qué “AI”</h2>
<p>Usamos herramientas de inteligencia artificial para leer reportes extensos, hacer los cálculos, preparar los gráficos y producir la locución de los videos. Eso nos permite cubrir más empresas y publicar poco después de cada entrega de resultados. Las cifras siempre salen de las fuentes públicas que citamos, para que puedas verificarlas.</p>
<h2>Correcciones</h2>
<p>Si encuentras un error, escríbenos desde la página de <a href="../contacto/index.html">Contacto</a> eligiendo “Corrección de datos”. Revisamos cada aviso y corregimos la ficha o el comparador afectado.</p>
<h2>Lo que no somos</h2>
<p>No somos asesores de inversión ni intermediarios de valores, y nada de lo que publicamos es una recomendación de compra o venta. Lee el <a href="../aviso-legal/index.html">aviso legal</a>.</p>"""),
"aviso-legal": ("Aviso legal", "Legal",
 "Condiciones de uso de la información publicada en AI Acciones Chile.",
 """<h2>Solo información, no asesoría</h2>
<p>El contenido de AI Acciones Chile (sitio web, videos y publicaciones en redes sociales) tiene fines informativos y educativos. No es una recomendación de compra, venta o mantención de ningún valor, ni una asesoría de inversión, tributaria o legal adaptada a tu situación. AI Acciones Chile no es un asesor de inversiones ni un intermediario de valores. Antes de invertir, evalúa tu situación y, si lo necesitas, consulta a un asesor autorizado.</p>
<h2>Riesgos</h2>
<p>Invertir en acciones implica riesgo, incluida la pérdida del capital invertido. Las rentabilidades pasadas no garantizan rentabilidades futuras. Los múltiplos, comparaciones y estimaciones que publicamos describen la situación de una empresa en un momento dado y pueden cambiar rápido.</p>
<h2>Exactitud de la información</h2>
<p>Las cifras provienen de fuentes públicas (estados financieros y análisis razonados entregados a la CMF, reportes de las empresas, Superintendencia de Pensiones y proveedores de datos de mercado) y de cálculos propios, que marcamos con (c). Aunque las revisamos, pueden contener errores u omisiones y no siempre reflejan la última información disponible. Los precios de cierre se actualizan una vez por día hábil y no son datos en tiempo real. La fuente oficial son siempre los estados financieros publicados en la <a href="https://www.cmfchile.cl" target="_blank" rel="noopener">CMF</a>. Si encuentras un error, avísanos desde <a href="../contacto/index.html">Contacto</a>.</p>
<h2>Publicidad y enlaces externos</h2>
<p>El sitio muestra anuncios de Google AdSense. Los anuncios los elige Google y no son una recomendación nuestra de los productos o servicios anunciados. Los enlaces a sitios de terceros (CMF, Bolsa de Santiago, empresas, YouTube, X) se incluyen como referencia; no controlamos su contenido. El uso de cookies se explica en la <a href="../privacidad/index.html">política de privacidad</a>.</p>
<h2>Propiedad del contenido</h2>
<p>Los textos, tablas, gráficos y videos de AI Acciones Chile son de nuestra autoría. Puedes citarlos indicando la fuente y enlazando a la página original. Las marcas y nombres de las empresas analizadas pertenecen a sus dueños.</p>
<h2>Ley aplicable</h2>
<p>Este aviso se rige por las leyes de la República de Chile.</p>"""),
}
for slug, (title, eyebrow, lede, body) in PAGES.items():
    h = re.sub(r"<title>.*?</title>", f"<title>{title} · AI ACCIONES CHILE</title>", head)
    main = f'''<main class="wrap">
<section class="page-head"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1>
<p class="lede">{lede}</p></section>
<div class="prose">
{body}
<p class="small">Última actualización: octubre 2026.</p>
</div>
</main>'''
    wr(f"{slug}/index.html", h + main + foot)
print("ok", list(PAGES))
