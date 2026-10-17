# Educación: indicadores clave por industria (educacion/indicadores-por-industria/). Plantilla: comparadores/energia/.
# uso: cd fuente && python3 industrias.py   (edita site/; luego ./build_web.sh)
import os, re
S = os.environ.get("SITE", os.path.abspath("site"))
SLUG = "educacion/indicadores-por-industria"
tpl = open(os.path.join(S, "comparadores/energia/index.html"), encoding="utf-8").read()
head, foot = tpl[:tpl.index("<main")], tpl[tpl.index("</main>") + len("</main>"):]
head = re.sub(r"<title>.*?</title>", "<title>Indicadores clave por industria · AI ACCIONES CHILE</title>", head)
head = re.sub(r'<meta name="description" content=".*?">',
              '<meta name="description" content="Qué indicadores mirar en cada industria de la Bolsa de Santiago: bancos, eléctricas, retail, malls, AFP, minería y más.">', head)
head = head.replace(' aria-current="page"', "").replace('educacion/index.html">Educación', 'educacion/index.html" aria-current="page">Educación', 1)

def emp(*ids):
    return ", ".join(f'<a href="../../acciones/{i}/index.html">{n}</a>' for i, n in ids)

# (ancla, título, bajada, [(indicador, explicación)], múltiplos, ojo, empresas)
IND = [
("bancos", "Bancos", "El negocio es prestar plata más cara de lo que cuesta conseguirla, sin que los clientes dejen de pagar.",
 [("Margen de intereses (NIM)", "lo que el banco gana por intereses cobrados menos intereses pagados, sobre sus activos que generan intereses. Es la principal fuente de ingresos."),
  ("Ingresos por comisiones", "lo que cobra por tarjetas, cuentas, seguros, fondos mutuos y asesorías. Son ingresos más estables que los intereses porque no dependen tanto de las tasas ni de la inflación."),
  ("Gasto en provisiones y costo del riesgo", "lo que reserva para préstamos que podrían no pagarse, dividido por las colocaciones. Si sube rápido, anticipa más morosidad."),
  ("Morosidad y cobertura", "la cartera con atraso de 90 días o más sobre el total, y cuántas veces las provisiones cubren esa cartera."),
  ("Índice de eficiencia", "gastos de apoyo divididos por ingresos operacionales. Mientras más bajo, menos le cuesta al banco generar cada peso."),
  ("ROE y capital (CET1)", "la rentabilidad sobre el patrimonio y el colchón de capital que exige Basilea III. Un capital holgado permite crecer y pagar dividendos.")],
 "P/BV (precio sobre patrimonio) junto al ROE, P/E y dividend yield. El EV/EBITDA y el flujo de caja libre no se usan en bancos.",
 "En Chile la inflación pesa: los bancos tienen más activos que pasivos en UF, así que una UF alta infla el margen de intereses por un tiempo. Separa ese efecto antes de comparar trimestres.",
 emp(("bci", "Bci"), ("chile", "Banco de Chile"), ("bsantander", "Santander Chile"), ("itau", "Itaú Chile"))),
("generadoras", "Generadoras eléctricas", "Venden energía con contratos de largo plazo; el margen depende de cuánto y con qué tecnología producen.",
 [("Generación (GWh)", "la energía que produjo la empresa en el período, y su mezcla: hidroeléctrica, solar, eólica, gas o carbón."),
  ("Hidrología", "un año lluvioso permite generar más con agua, que es la fuente más barata; un año seco obliga a usar gas o diésel, o a comprar energía."),
  ("Ventas físicas y contratos", "cuánta energía vendió a clientes regulados (distribuidoras) y libres (industrias, minería), y cuánto de eso está cubierto con generación propia."),
  ("Costo marginal y precio medio de venta", "el precio spot del sistema y el precio promedio de sus contratos. Si la empresa vende más de lo que genera, compra al costo marginal y su margen se aprieta."),
  ("Margen EBITDA", "el EBITDA sobre los ingresos. Muestra cuánto de cada peso vendido queda antes de depreciación, intereses e impuestos."),
  ("Deuda neta / EBITDA y proyectos", "cuántos años de EBITDA haría falta para pagar la deuda, y el avance de las centrales en construcción.")],
 "EV/EBITDA, dividend yield y P/E. Conviene compararlos con la propia historia de la empresa y con generadoras parecidas.",
 "Un trimestre con buena hidrología no se repite necesariamente. Mira la generación por tecnología, no solo el EBITDA total.",
 emp(("colbun", "Colbún"), ("enelgxch", "Enel Generación"), ("ecl", "Engie Energía Chile"), ("aes-andes", "AES Andes"), ("pehuenche", "Pehuenche"))),
("reguladas", "Distribución eléctrica y sanitarias", "Negocios regulados: el Estado fija la tarifa para que la empresa recupere sus inversiones con un retorno.",
 [("Volumen distribuido", "la energía (GWh) o el agua (m³) entregada a los clientes. Crece con la población, el clima y la actividad económica."),
  ("Número de clientes", "el crecimiento de la base de clientes, que impulsa los ingresos de largo plazo."),
  ("Pérdidas y agua no facturada", "la energía o el agua que se pierde en la red o no se cobra. Una pérdida menor significa una operación más eficiente."),
  ("Procesos tarifarios", "el valor agregado de distribución (VAD) en electricidad y las tarifas que fija la SISS en agua. Un cambio de tarifa mueve los resultados por años."),
  ("Inversión (capex) y deuda", "estas empresas invierten mucho en redes; la tarifa reconoce esas inversiones, pero se financian en buena parte con deuda.")],
 "EV/EBITDA, P/BV y dividend yield. Al ser negocios estables, el mercado suele mirarlos como bonos: les afectan mucho las tasas de interés.",
 "Los atrasos en la fijación de tarifas o en la entrega de subsidios pueden dejar cuentas por cobrar grandes. Revisa el flujo de caja operacional, no solo la utilidad.",
 emp(("cge", "CGE"), ("enelchile", "Enel Chile"), ("aguas-a", "Aguas Andinas"), ("iam", "IAM"))),
("retail", "Retail", "Vender mucho, con buen margen y sin quedarse con inventario; en Chile suele venir con un negocio financiero.",
 [("Ventas mismas tiendas (SSS)", "el crecimiento de las tiendas que ya existían hace un año. Separa el crecimiento orgánico del que viene de abrir tiendas nuevas."),
  ("Margen bruto", "lo que queda de cada venta después del costo de los productos. Baja cuando hay liquidaciones o más competencia."),
  ("Gastos de administración y ventas (SG&A) sobre ventas", "cuánto cuesta operar tiendas, logística y personal por cada peso vendido."),
  ("Ventas online", "el peso del comercio electrónico y su rentabilidad, que suele ser distinta a la de la tienda física."),
  ("Inventarios", "los días de inventario o la rotación. Un inventario que crece más rápido que las ventas anticipa descuentos."),
  ("Cartera y riesgo del negocio financiero", "en las empresas con banco o tarjeta propia, las colocaciones, la morosidad y las provisiones pesan tanto como la tienda.")],
 "EV/EBITDA y P/E. Si la empresa tiene banco, conviene separar el negocio retail del financiero antes de comparar.",
 "El tipo de cambio importa: buena parte de lo que se vende es importado. Un dólar alto encarece los productos y presiona el margen bruto.",
 emp(("falabella", "Falabella"), ("cencosud", "Cencosud"), ("ripley", "Ripley"), ("smu", "SMU"))),
("malls", "Centros comerciales", "Arriendan locales en UF; el ingreso depende de cuántos metros están ocupados y de cuánto venden los locatarios.",
 [("NOI y margen NOI", "el ingreso operacional neto de los arriendos, después de los costos de operar los centros. Es el EBITDA del negocio inmobiliario."),
  ("FFO", "la caja que genera el negocio (funds from operations): la utilidad sin las revalorizaciones de propiedades, más la depreciación."),
  ("Ocupación o vacancia", "el porcentaje de la superficie arrendable (GLA) que está arrendada. Afecta directamente los ingresos."),
  ("Ventas de locatarios", "lo que venden las tiendas en el mall. Si suben, el arriendo variable crece y es más fácil renovar contratos a mejor precio."),
  ("Revalorización de propiedades", "con normas IFRS, el aumento del valor contable de los malls se registra como utilidad, pero no es caja.")],
 "P/FFO, EV/EBITDA y P/BV. El P/E suele verse distorsionado por las revalorizaciones.",
 "Una utilidad que salta de un trimestre a otro muchas veces viene de revalorizar los malls. Mira el NOI y el FFO para ver el negocio recurrente.",
 emp(("mallplaza", "Mall Plaza"), ("parauco", "Parque Arauco"), ("cencomalls", "Cencosud Shopping"))),
("afp", "AFP", "Cobran una comisión sobre el sueldo de sus cotizantes y deben invertir una parte de su propio patrimonio en los fondos.",
 [("Cotizantes y afiliados", "los afiliados son todos los trabajadores con cuenta en la AFP; los cotizantes, los que efectivamente cotizaron. Los ingresos vienen de los cotizantes."),
  ("Ingresos por comisiones", "la comisión sobre la renta imponible de los cotizantes. Crece con el empleo y los sueldos."),
  ("Participación de mercado", "la proporción de cotizantes del sistema que tiene la AFP. Las licitaciones de nuevos afiliados la mueven."),
  ("Rentabilidad del encaje", "el encaje es una reserva que la AFP invierte en sus propios fondos. Sube o baja con los mercados y mueve mucho la utilidad trimestral."),
  ("Utilidad sin encaje", "la utilidad del negocio sin el efecto del encaje. Muestra cómo le fue a la administración en sí.")],
 "P/E y dividend yield. Conviene calcular el P/E también con la utilidad sin encaje.",
 "Las reformas de pensiones pueden cambiar las comisiones o el rol de las AFP. Ese riesgo regulatorio no aparece en los estados financieros.",
 emp(("habitat", "Habitat"), ("provida", "Provida"), ("afpcapital", "AFP Capital"), ("planvital", "PlanVital"))),
("mineria", "Minería y commodities", "El precio no lo pone la empresa: lo pone el mercado mundial. Lo que la empresa controla es cuánto produce y a qué costo.",
 [("Volumen vendido", "las toneladas vendidas de cada producto, por ejemplo litio, yodo o fertilizantes."),
  ("Precio realizado", "el precio promedio que la empresa obtuvo, que puede diferir del precio de referencia por contratos o calidad."),
  ("Costo por unidad (cash cost)", "cuánto cuesta producir cada tonelada. Define cuánto margen queda cuando los precios caen."),
  ("Margen EBITDA", "muy variable en el ciclo: alto con precios altos y bajo cuando el ciclo se da vuelta."),
  ("Capex y contratos", "las inversiones para ampliar la capacidad y los pagos al Estado (arriendos, royalties), que pueden cambiar con nuevos acuerdos.")],
 "EV/EBITDA y P/E, siempre mirando en qué parte del ciclo de precios está el commodity.",
 "En empresas cíclicas el P/E suele verse más bajo justo en el peak de precios, cuando las utilidades están infladas.",
 emp(("sqm-b", "SQM"))),
("forestal", "Forestal y combustibles", "Celulosa, papel y madera por un lado; distribución de combustibles por el otro.",
 [("Precio de la celulosa", "los precios de la celulosa de fibra corta y larga en China y Europa determinan buena parte de los ingresos forestales."),
  ("Volumen de producción y ventas", "las toneladas de celulosa, papel o tableros, y las paradas de planta por mantención."),
  ("Costo caja por tonelada", "cuánto cuesta producir una tonelada de celulosa, incluida la madera, la energía y los químicos."),
  ("Margen de combustibles", "en la distribución de combustibles, el margen por metro cúbico vendido y el volumen de las estaciones de servicio."),
  ("Deuda neta / EBITDA", "estas empresas tienen proyectos grandes y su deuda sube en los años de inversión.")],
 "EV/EBITDA, P/BV y dividend yield.",
 "Los inventarios de combustibles se valorizan a precio de mercado: cuando el petróleo sube o baja fuerte, el margen del trimestre se mueve aunque el negocio no haya cambiado.",
 emp(("cmpc", "CMPC"), ("copec", "Copec"))),
("aerolineas", "Aerolíneas", "Llenar los aviones al mejor precio posible, con costos de combustible y flota bajo control.",
 [("Capacidad (ASK)", "los asientos-kilómetro disponibles: cuánta oferta puso la aerolínea en el período."),
  ("Tráfico (RPK) y factor de ocupación", "los pasajeros-kilómetro transportados y el porcentaje de asientos ocupados (RPK sobre ASK)."),
  ("Ingreso por ASK (RASK)", "el ingreso por cada asiento-kilómetro ofrecido. Combina tarifa y ocupación."),
  ("Costo por ASK sin combustible (CASK ex fuel)", "mide la eficiencia de la operación, aislando el precio del combustible."),
  ("Combustible y carga", "el precio del jet fuel es el mayor costo variable; el negocio de carga aporta ingresos adicionales."),
  ("Deuda y arriendos de flota", "los aviones se financian con deuda y arriendos que figuran como pasivos.")],
 "EV/EBITDA (incluyendo los arriendos en la deuda) y P/E.",
 "Un factor de ocupación alto no basta: si la tarifa media cae, el RASK puede bajar igual.",
 emp(("ltm", "LATAM Airlines"))),
("consumo", "Consumo masivo y bebidas", "Marcas fuertes que venden volumen; la clave es subir precios sin perder volumen y cuidar el costo de las materias primas.",
 [("Volumen", "las cajas unitarias, hectolitros o litros vendidos, por país y por categoría."),
  ("Precio promedio y mix", "el ingreso por unidad vendida. Sube con aumentos de precio o vendiendo productos más caros."),
  ("Costo de materias primas", "azúcar, aluminio, resina PET, cebada o uva, muchas veces en dólares."),
  ("Margen EBITDA por país", "las empresas que operan en varios países muestran márgenes distintos en cada uno."),
  ("Tipo de cambio", "los resultados en Argentina, Brasil o Paraguay se convierten a pesos; las devaluaciones los reducen.")],
 "P/E, EV/EBITDA y dividend yield.",
 "En Argentina la contabilidad usa ajuste por hiperinflación (NIC 29): los crecimientos en moneda local se ven enormes y conviene leerlos en pesos chilenos o en dólares.",
 emp(("andina-a", "Andina"), ("ccu", "CCU"), ("conchatoro", "Concha y Toro"))),
("telecom", "Telecomunicaciones", "Clientes que pagan todos los meses; la competencia y las inversiones en red definen la rentabilidad.",
 [("Suscriptores", "el número de clientes móviles y de hogar (fibra), separando prepago y contrato."),
  ("ARPU", "el ingreso promedio por usuario al mes. Sube cuando los clientes contratan planes más caros."),
  ("Churn", "el porcentaje de clientes que se van cada mes. Un churn alto obliga a gastar más en captar clientes."),
  ("Capex sobre ventas", "cuánto invierte en red (5G, fibra) por cada peso de ingresos."),
  ("Margen EBITDA y deuda", "el margen operacional y la deuda que financia la red.")],
 "EV/EBITDA y dividend yield.",
 "Las guerras de precios entre operadores pueden subir los suscriptores y bajar el ARPU al mismo tiempo. Mira ambos juntos.",
 "Entel"),
("holdings", "Holdings", "Empresas cuyo valor está en las participaciones que tienen en otras compañías.",
 [("Aportes por filial", "cuánto aporta cada filial o coligada a la utilidad del holding, según su porcentaje de propiedad."),
  ("Valor de los activos (NAV)", "la suma del valor de mercado de las participaciones menos la deuda del holding."),
  ("Descuento de holding", "cuánto menos que su NAV vale el holding en bolsa. Suele haber descuento por costos y menor liquidez."),
  ("Dividendos recibidos", "la caja que suben las filiales: es lo que permite al holding pagar su deuda y sus propios dividendos."),
  ("Deuda a nivel holding", "la deuda de la matriz, separada de la de las filiales.")],
 "Descuento sobre NAV, P/E y dividend yield.",
 "La utilidad consolidada mezcla negocios muy distintos (bancos, bebidas, navieras). Revisa cada aporte por separado.",
 emp(("quinenco", "Quiñenco"), ("vapores", "Vapores"))),
("construccion", "Construcción e ingeniería", "Ganan contratos de obras y servicios; los ingresos de mañana dependen de los contratos firmados hoy.",
 [("Backlog", "el monto de contratos por ejecutar. Anticipa los ingresos de los próximos trimestres."),
  ("Adjudicaciones", "los contratos nuevos ganados en el período, que reponen el backlog."),
  ("Margen por contrato", "un contrato mal presupuestado puede generar pérdidas aunque la empresa venda más."),
  ("Capital de trabajo", "las obras se cobran con desfase, así que la caja puede ser negativa un trimestre aunque haya utilidad."),
  ("Ciclo de inversión", "la demanda depende de la inversión pública, la minería y el sector inmobiliario.")],
 "P/E, EV/EBITDA y P/BV.",
 "Un trimestre con flujo de caja negativo no siempre es mala noticia en estas empresas. Mira la tendencia del año.",
 emp(("besalco", "Besalco"), ("sk", "Sigdo Koppers"))),
]

chips = "".join(f'<a href="#{a}">{t}</a>' for a, t, *_ in IND)
cards = []
for a, t, bajada, inds, mult, ojo, emps in IND:
    li = "".join(f"<li><b>{n}:</b> {d}</li>" for n, d in inds)
    cards.append(f'''<article id="{a}" class="lesson"><h2>{t}</h2><p class="lede-sm">{bajada}</p>
<ul class="ind-list">{li}</ul>
<p class="formula">Múltiplos más usados: {mult}</p>
<p class="warn"><b>Ojo:</b> {ojo}</p>
<p class="small">En el sitio: {emps}.</p></article>''')

main = f'''<main class="wrap">
<nav class="crumbs"><a href="../index.html">Educación</a> / Indicadores por industria</nav>
<section class="page-head"><p class="eyebrow">Educación</p><h1>Indicadores clave por industria</h1>
<p class="lede">Cada industria se mide distinto. En un banco importan las comisiones y la morosidad; en una eléctrica, cuánta energía produjo y con qué tecnología. Esta guía resume qué mirar en cada sector de la Bolsa de Santiago.</p>
<p class="chips">{chips}</p></section>
<div class="lessons">
{chr(10).join(cards)}
</div>
<p class="small">Los conceptos generales (P/E, EBITDA, flujo de caja libre, valoración) están en <a href="../index.html">Educación</a>. Este contenido es educativo y no es una recomendación de inversión.</p>
</main>'''
os.makedirs(os.path.join(S, SLUG), exist_ok=True)
open(os.path.join(S, SLUG, "index.html"), "w", encoding="utf-8").write(head + main + foot)
print("ok", SLUG, len(IND), "industrias")
