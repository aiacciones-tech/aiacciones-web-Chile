"""Sección Educación de aiacciones.es: qué mide cada indicador y en qué fijarse según el sector.

Contenido educativo y general: explica conceptos, no valora ninguna empresa concreta.
Cada indicador: (nombre, qué es, cómo se calcula, cómo se lee, cuidado con).
Cada guía de sector: id, título, empresas (ids de fichas.py como ejemplos), cómo gana dinero,
indicadores clave, valoración habitual en el sector y errores frecuentes.
"""

GENERALES = {
    "id": "valoracion",
    "titulo": "Indicadores de valoración",
    "lede": "Los múltiplos que más se usan para poner en contexto el precio de una acción. Ninguno basta por sí solo: "
            "sirven para comparar a una empresa con su propia historia y con las de su sector, siempre con el mismo criterio de cálculo.",
    "indicadores": [
        ("PER (precio / beneficio)",
         "Cuántas veces paga el mercado el beneficio por acción de la empresa.",
         "Precio de la acción ÷ beneficio por acción (BPA) de los últimos 12 meses.",
         "Un PER de 15x significa que, si el beneficio se mantuviera igual, harían falta 15 años de beneficios para igualar el precio. "
         "Un PER más alto suele reflejar que el mercado espera más crecimiento o más estabilidad; uno más bajo, menos crecimiento o más riesgo.",
         "El beneficio puede incluir partidas extraordinarias (ventas de activos, deterioros) que inflan o hunden el PER. "
         "Mira el beneficio recurrente u ordinario cuando la empresa lo publique. Con pérdidas, el PER no tiene sentido."),
        ("PER forward (PER estimado)",
         "El mismo PER, pero con el beneficio que los analistas esperan para los próximos 12 meses.",
         "Precio de la acción ÷ BPA estimado por el consenso de analistas para el próximo año.",
         "Si el PER forward es menor que el PER de los últimos 12 meses, el consenso espera que el beneficio crezca; si es mayor, que caiga.",
         "Depende de estimaciones, que cambian y a menudo fallan. Conviene saber de qué consenso sale y de qué fecha es."),
        ("BPA (beneficio por acción)",
         "La parte del beneficio neto que corresponde a cada acción.",
         "Beneficio neto atribuido ÷ número medio de acciones en circulación.",
         "Es la base del PER. Puede crecer más que el beneficio si la empresa recompra acciones, porque reparte el beneficio entre menos acciones.",
         "Tras un desdoblamiento (split) o una ampliación de capital, compara siempre con el mismo número de acciones."),
        ("Precio / valor en libros (P/VC)",
         "Cuánto paga el mercado por cada euro de patrimonio contable.",
         "Capitalización ÷ patrimonio neto (o precio ÷ valor contable por acción).",
         "Muy útil en bancos y aseguradoras, cuyo balance está casi todo a valor de mercado. Un P/VC por encima de 1 suele ir unido a una rentabilidad sobre el patrimonio (ROE) alta.",
         "En empresas con muchos activos intangibles o marcas, el valor en libros dice poco del negocio."),
        ("EV/EBITDA",
         "Cuánto vale toda la empresa (acciones más deuda) en relación con su resultado operativo antes de amortizaciones.",
         "Valor de empresa (capitalización + deuda neta) ÷ EBITDA de los últimos 12 meses.",
         "Permite comparar empresas con distinto nivel de deuda, porque incluye a accionistas y acreedores. Se usa mucho en eléctricas, telecos e industria.",
         "No sirve en bancos. El EBITDA ignora la inversión necesaria para mantener el negocio, que en sectores intensivos en capital es muy alta."),
        ("Rentabilidad por dividendo",
         "Qué porcentaje del precio devuelve la empresa en dividendos cada año.",
         "Dividendos por acción de los últimos 12 meses ÷ precio de la acción.",
         "Ayuda a ver cuánto del retorno llega en efectivo. Conviene mirarla junto al pay-out (porcentaje del beneficio que se reparte).",
         "Un dividendo extraordinario puede disparar la cifra un año. Una rentabilidad muy alta a veces refleja que el precio ha caído por dudas sobre el negocio."),
        ("Rentabilidad por flujo de caja libre (FCF yield)",
         "Cuánta caja libre genera la empresa en relación con su valor en bolsa.",
         "Flujo de caja libre (caja operativa − inversiones) ÷ capitalización.",
         "Muestra la caja disponible para dividendos, recompras o reducir deuda. Es más difícil de maquillar que el beneficio contable.",
         "Puede ser baja o negativa durante años de fuerte inversión, sin que eso signifique un problema."),
        ("Deuda neta / EBITDA",
         "Cuántos años de resultado operativo harían falta para pagar la deuda.",
         "(Deuda financiera − caja) ÷ EBITDA de los últimos 12 meses.",
         "Mide el apalancamiento. Por debajo de 2-3x suele considerarse holgado en la mayoría de sectores; las eléctricas y concesiones toleran más por la estabilidad de sus ingresos.",
         "Cada empresa define la deuda neta a su manera (con o sin arrendamientos, híbridos o deuda de proyectos)."),
    ],
}

SECTORES = [
    {
        "id": "bancos",
        "ibex": "Santander, BBVA, CaixaBank, Sabadell, Bankinter y Unicaja",
        "resumen": "Margen de intereses, comisiones, eficiencia, ROTE, morosidad y capital (CET1).",
        "titulo": "Bancos",
        "empresas": ["santander", "bbva", "caixabank", "sabadell", "bankinter", "unicaja"],
        "negocio": "Un banco gana dinero sobre todo con la diferencia entre lo que cobra por los créditos y lo que paga por los depósitos "
                   "(margen de intereses), y con las comisiones por servicios: cuentas, tarjetas, fondos, seguros y gestión de patrimonios. "
                   "Su materia prima es el capital: por eso lo que más importa es cuánto gana con él y cuánto riesgo asume.",
        "claves": [
            ("Margen de intereses", "La principal fuente de ingresos. Depende del volumen de crédito y de los tipos de interés: sube con tipos altos y se estrecha cuando bajan."),
            ("Comisiones netas", "Ingresos más estables que el margen de intereses porque no dependen de los tipos. Las de gestión de activos y seguros suelen crecer más que las bancarias tradicionales."),
            ("Ratio de eficiencia", "Gastos ÷ margen bruto. Indica cuántos céntimos gasta el banco para ingresar un euro: cuanto más bajo, mejor. Los grandes bancos españoles se mueven entre el 35% y el 50%."),
            ("ROE y ROTE", "Beneficio sobre el patrimonio (ROE) o sobre el patrimonio tangible, sin fondos de comercio (ROTE). Es el indicador central: un banco que gana más de lo que le cuesta su capital (en torno al 10%) crea valor."),
            ("Morosidad y cobertura", "Morosidad: créditos dudosos ÷ créditos totales. Cobertura: provisiones dotadas ÷ créditos dudosos. Una morosidad baja con cobertura alta indica un balance sano."),
            ("Coste del riesgo", "Provisiones por insolvencias del periodo ÷ crédito medio. Si sube, el banco espera más impagos."),
            ("CET1", "Capital de máxima calidad ÷ activos ponderados por riesgo. Es el colchón de solvencia que vigila el supervisor; el exceso sobre el mínimo exigido es lo que permite repartir dividendos y recompras."),
        ],
        "valoracion": "En banca se usan el PER, el precio / valor en libros (P/VC) frente al ROTE y la rentabilidad por dividendo. "
                      "No se usan EV/EBITDA ni flujo de caja libre, porque la deuda es la materia prima del negocio.",
        "errores": [
            "Comparar el margen de intereses sin mirar en qué momento del ciclo de tipos está el banco.",
            "Fijarse solo en el beneficio: un salto puntual puede venir de menos provisiones o de una plusvalía.",
            "Comparar el ROTE de bancos con criterios distintos (ordinario, recurrente o contable).",
        ],
    },
    {
        "id": "electricas",
        "ibex": "Iberdrola, Endesa, Naturgy, Redeia y Enagás",
        "resumen": "Producción y mix, precio de la electricidad, activos regulados, inversiones y deuda.",
        "titulo": "Eléctricas y redes",
        "empresas": ["iberdrola", "endesa", "naturgy", "redeia", "enagas"],
        "negocio": "Hay dos negocios muy distintos. Las redes (transporte y distribución de electricidad o gas) están reguladas: el regulador fija "
                   "cuánto pueden ganar sobre los activos que construyen. La generación y la comercialización dependen de cuánta energía producen, "
                   "a qué precio la venden y cuánto les cuesta producirla. Muchas empresas combinan ambos.",
        "claves": [
            ("Producción (GWh) y mix", "Cuánta electricidad genera la empresa y con qué tecnología: renovables, nuclear, ciclos combinados. Una mayor parte renovable reduce el coste variable y las emisiones, pero depende de la lluvia y el viento."),
            ("Precio de la electricidad y margen unitario", "El precio del mercado mayorista (pool) y los contratos de venta a largo plazo (PPA) determinan cuánto se ingresa por cada MWh; el margen depende también del coste del gas y del CO₂."),
            ("Base de activos regulados (RAB)", "En las redes, el beneficio crece cuando crece la base de activos sobre la que el regulador reconoce una retribución. Las revisiones regulatorias (por ejemplo, la tasa de retribución financiera) son clave."),
            ("EBITDA por negocio", "Separa redes, generación y comercialización: cada uno tiene riesgos distintos y el mercado los valora de forma diferente."),
            ("Inversiones", "Son negocios intensivos en capital. El plan de inversiones anticipa el crecimiento futuro de la base de activos y de la capacidad instalada."),
            ("Deuda neta / EBITDA y FFO / deuda", "Mide si la empresa puede financiar su plan de inversión y mantener su calificación crediticia. Las agencias de rating vigilan sobre todo el FFO / deuda."),
            ("Dividendo y pay-out", "Suelen tener políticas de dividendo explícitas; conviene comprobar que la caja después de inversiones las sostiene."),
        ],
        "valoracion": "Se usan el PER, el EV/EBITDA, la rentabilidad por dividendo y, en las redes, la prima sobre la base de activos regulados. "
                      "El flujo de caja libre suele ser bajo o negativo en años de mucha inversión.",
        "errores": [
            "Olvidar que un año seco o con poco viento reduce la producción renovable aunque la empresa no haya hecho nada mal.",
            "Mezclar el negocio regulado con el liberalizado al leer el EBITDA total.",
            "No mirar los cambios regulatorios, que pueden mover el beneficio de las redes durante años.",
        ],
    },
    {
        "id": "petroleo-gas",
        "ibex": "Repsol",
        "resumen": "Producción, Brent, margen de refino, resultado ajustado y transición energética.",
        "titulo": "Petróleo y gas",
        "empresas": ["repsol"],
        "negocio": "Una petrolera integrada extrae crudo y gas (upstream), lo refina y lo vende en estaciones de servicio y a la industria (downstream). "
                   "Sus resultados dependen mucho de precios que no controla: el del barril, el del gas y el margen de refino.",
        "claves": [
            ("Producción (barriles equivalentes al día)", "Volumen de crudo y gas extraído. Junto al precio, determina los ingresos del upstream."),
            ("Precio del Brent y del gas", "La referencia de ingresos de la exploración y producción. Las empresas suelen publicar cuánto cambia su resultado por cada dólar que varía el barril."),
            ("Margen de refino", "Diferencia entre el valor de los productos refinados y el coste del crudo. Es muy volátil y explica gran parte del resultado del downstream."),
            ("Resultado ajustado (CCS)", "El resultado a coste de reposición elimina el efecto de la variación del precio de los inventarios y permite comparar periodos."),
            ("Inversión en transición energética", "Qué parte del capital va a renovables, biocombustibles o hidrógeno, y con qué rentabilidad esperada."),
            ("Deuda neta y retribución al accionista", "Con precios volátiles, una deuda baja da margen para mantener dividendos y recompras en años malos."),
        ],
        "valoracion": "PER, EV/EBITDA, rentabilidad por dividendo y por flujo de caja libre. Conviene mirar los múltiplos con el precio del crudo de cada momento.",
        "errores": [
            "Comparar trimestres sin tener en cuenta el precio del barril y del margen de refino de cada uno.",
            "Leer el resultado contable sin ajustar el efecto de los inventarios.",
        ],
    },
    {
        "id": "telecomunicaciones",
        "ibex": "Telefónica",
        "resumen": "Clientes, ARPU, bajas (churn), EBITDA menos inversiones y deuda.",
        "titulo": "Telecomunicaciones",
        "empresas": ["telefonica"],
        "negocio": "Una operadora cobra cuotas mensuales por móvil, fibra y televisión a millones de clientes. El ingreso es recurrente, "
                   "pero la red exige inversiones constantes y la competencia presiona los precios.",
        "claves": [
            ("Accesos y clientes", "Líneas móviles, accesos de fibra y televisión. Crecer en clientes de valor (contrato, fibra, convergente) importa más que el número total."),
            ("ARPU", "Ingreso medio por usuario. Muestra si la empresa sube precios o vende servicios de mayor valor."),
            ("Churn (tasa de bajas)", "Porcentaje de clientes que se van cada mes. Un churn bajo indica clientes fieles y menos gasto comercial."),
            ("EBITDA menos inversiones (EBITDAaL − CapEx)", "Aproxima la caja operativa después de mantener y ampliar la red; es el indicador que más siguen las operadoras."),
            ("Deuda neta / EBITDA", "Las telecos suelen estar endeudadas; la evolución de la deuda y de los costes financieros condiciona el dividendo."),
            ("Efecto divisa", "Las operadoras con negocio en Latinoamérica ven sus resultados en euros afectados por la evolución de las monedas locales."),
        ],
        "valoracion": "EV/EBITDA, rentabilidad por flujo de caja libre y rentabilidad por dividendo. El PER puede verse distorsionado por deterioros y ventas de activos.",
        "errores": [
            "Fijarse en el EBITDA sin restar la inversión, que en este sector es muy elevada.",
            "Comparar crecimientos sin separar el efecto de la divisa y de las ventas de filiales.",
        ],
    },
    {
        "id": "infraestructuras",
        "ibex": "Ferrovial, Aena y Cellnex (torres de telecomunicaciones)",
        "resumen": "Tráfico y pasajeros, tarifas, ingresos comerciales y dividendos de proyectos.",
        "titulo": "Infraestructuras y concesiones",
        "empresas": ["ferrovial", "aena", "cellnex"],
        "negocio": "Gestionan activos de larga duración, como autopistas de peaje, aeropuertos o torres de telecomunicaciones, a menudo bajo concesión. "
                   "Cobran tarifas por su uso y reparten la caja que generan los activos. Algunas también construyen.",
        "claves": [
            ("Tráfico y pasajeros", "Vehículos en las autopistas o pasajeros en los aeropuertos: el motor de los ingresos."),
            ("Tarifas", "Cuánto se cobra por uso y cómo se actualiza (por inflación, por regulación o libremente). En aeropuertos regulados, las tarifas las fija el regulador por periodos."),
            ("Ingresos comerciales", "En aeropuertos, tiendas, restauración y aparcamientos: crecen con el gasto por pasajero."),
            ("Dividendos de proyectos", "En grupos con participaciones en concesiones, la caja que reciben de cada activo es más relevante que el beneficio consolidado."),
            ("Margen de construcción y cartera", "Si construyen, el margen suele ser estrecho y la cartera de obra anticipa la actividad futura."),
            ("Inquilinos por emplazamiento", "En torres de telecomunicaciones, cuántos operadores alquilan cada torre: un segundo o tercer inquilino añade ingresos casi sin coste adicional."),
            ("Vida de las concesiones y deuda", "Cuántos años quedan de concesión y cómo está financiado cada activo: la deuda de proyectos suele ir sin recurso a la matriz."),
        ],
        "valoracion": "EV/EBITDA, rentabilidad por dividendo y, en grupos de concesiones, la suma de las partes (valor de cada activo por separado). "
                      "El PER puede ser muy alto o muy bajo por plusvalías y amortizaciones de las concesiones.",
        "errores": [
            "Valorar por el PER un grupo cuyo beneficio cambia mucho por la venta de activos.",
            "Ignorar las revisiones de tarifas reguladas, que fijan los ingresos durante varios años.",
        ],
    },
    {
        "id": "renovables",
        "ibex": "Acciona Energía y Solaria",
        "resumen": "Capacidad instalada, producción, precio capturado, PPA, cartera de proyectos y deuda.",
        "titulo": "Renovables",
        "empresas": ["acciona-energia", "solaria"],
        "negocio": "Construyen y operan parques eólicos, solares o hidráulicos y venden la electricidad que producen, en el mercado mayorista "
                   "o con contratos a largo plazo (PPA). Sus ingresos dependen de cuántos megavatios tienen en funcionamiento, del recurso "
                   "natural (sol, viento, agua) y del precio al que consiguen vender cada MWh.",
        "claves": [
            ("Capacidad instalada (MW o GW)", "Potencia en funcionamiento. Conviene distinguir la capacidad total de la atribuible (la parte que corresponde a la empresa según su participación en cada proyecto)."),
            ("Producción (GWh) y horas equivalentes", "Cuánta energía han producido los parques. Las horas equivalentes (producción ÷ capacidad) muestran si ha sido un periodo con buen o mal recurso natural."),
            ("Precio capturado", "El precio medio que la empresa obtiene por cada MWh vendido. En solar suele ser inferior al precio medio del mercado, porque todas las plantas producen a la vez en las horas centrales del día."),
            ("Energía contratada (PPA y coberturas)", "Qué parte de la producción tiene el precio asegurado con contratos. Más contratación da ingresos más previsibles, a cambio de renunciar a parte de las subidas de precio."),
            ("Cartera de proyectos (pipeline)", "Proyectos en construcción, con permisos o en desarrollo. Anticipa el crecimiento, pero solo una parte llegará a construirse."),
            ("Inversión por MW y rotación de activos", "Cuánto cuesta construir cada MW y si la empresa vende participaciones en parques para recuperar capital y reinvertirlo."),
            ("Deuda neta / EBITDA", "Son negocios con mucha inversión inicial; la deuda y el coste de financiarla pesan mucho cuando suben los tipos de interés."),
        ],
        "valoracion": "Se usan el EV/EBITDA, el EV por MW instalado y el PER. El valor depende mucho de los precios de la electricidad esperados y de los tipos de interés, "
                      "porque los parques generan caja durante décadas.",
        "errores": [
            "Atribuir a la gestión una caída de beneficio que viene de un año con poco viento, poca lluvia o precios bajos.",
            "Contar como crecimiento seguro toda la cartera de proyectos, incluidos los que aún no tienen permisos.",
            "Comparar el precio capturado de una empresa solar con el precio medio del mercado sin tener en cuenta las horas en que produce.",
        ],
    },
    {
        "id": "construccion",
        "ibex": "ACS, Acciona y Sacyr",
        "resumen": "Cartera de obra, ventas, margen, caja de la actividad, concesiones y deuda.",
        "titulo": "Construcción e ingeniería",
        "empresas": ["acs", "acciona", "sacyr"],
        "negocio": "Construyen obra civil, edificios, plantas industriales o centros de datos por encargo de clientes públicos y privados. "
                   "El margen de cada obra es estrecho y el riesgo está en los sobrecostes, por eso muchos grupos combinan la construcción "
                   "con concesiones (autopistas, hospitales, agua) que aportan ingresos más estables.",
        "claves": [
            ("Cartera de obra (backlog)", "Contratos firmados pendientes de ejecutar. Anticipa las ventas de los próximos años; suele compararse con las ventas de un año (meses de actividad asegurada)."),
            ("Adjudicaciones y ratio book-to-bill", "Nuevos contratos ganados ÷ ventas del periodo. Por encima de 1 la cartera crece; por debajo, se consume."),
            ("Margen EBITDA y EBIT", "En construcción pura suele estar entre el 3% y el 8%. Una caída puede anticipar sobrecostes o litigios en obras concretas."),
            ("Flujo de caja operativo y circulante", "Las constructoras cobran por avance de obra y a veces con anticipos: el capital circulante puede mover mucho la caja entre trimestres."),
            ("Peso de las concesiones", "Qué parte del EBITDA viene de concesiones, con ingresos a largo plazo, frente a la construcción, más cíclica."),
            ("Deuda neta con y sin recurso", "La deuda de los proyectos concesionales suele ir sin recurso a la matriz; conviene mirar por separado la deuda corporativa."),
        ],
        "valoracion": "Se usan el PER, el EV/EBITDA y, en grupos con concesiones o participaciones, la suma de las partes. "
                      "En constructoras con caja neta, el EV/EBITDA es más representativo que el PER.",
        "errores": [
            "Mirar solo el crecimiento de la cartera sin comprobar su margen esperado y el riesgo de los contratos.",
            "Leer la caja de un trimestre aislado, muy afectada por cobros y pagos puntuales.",
            "Sumar la deuda de proyectos sin recurso a la deuda corporativa como si fueran lo mismo.",
        ],
    },
    {
        "id": "seguros",
        "ibex": "Mapfre",
        "resumen": "Primas, ratio combinado, resultado financiero, solvencia (Solvencia II) y ROE.",
        "titulo": "Seguros",
        "empresas": ["mapfre"],
        "negocio": "Una aseguradora cobra primas por adelantado y paga siniestros después. Gana dinero de dos formas: suscribiendo bien "
                   "(que las primas cubran los siniestros y los gastos) e invirtiendo las primas mientras no se pagan.",
        "claves": [
            ("Primas emitidas", "Volumen de negocio. Conviene separar No Vida (autos, hogar, salud, empresas) de Vida (ahorro y riesgo), que tienen dinámicas distintas."),
            ("Ratio combinado", "(Siniestros + gastos) ÷ primas, en No Vida. Por debajo del 100% la aseguradora gana dinero con el negocio asegurador en sí; por encima, pierde antes de contar las inversiones."),
            ("Siniestralidad", "La parte del ratio combinado que corresponde a los siniestros. Sube con fenómenos meteorológicos extremos o con la inflación de reparaciones y salarios."),
            ("Resultado financiero", "Lo que rinden las inversiones (sobre todo renta fija). Mejora cuando suben los tipos de interés."),
            ("Ratio de solvencia (Solvencia II)", "Capital disponible ÷ capital exigido por la regulación europea. Por encima del 100% se cumple el mínimo; los grupos grandes suelen moverse entre el 180% y el 220%."),
            ("ROE", "Beneficio sobre el patrimonio: cuánto gana la aseguradora con el capital de sus accionistas."),
            ("Efecto divisa", "Las aseguradoras con negocio en Latinoamérica ven sus primas y beneficios en euros afectados por las monedas locales."),
        ],
        "valoracion": "Se usan el PER, el precio / valor en libros frente al ROE y la rentabilidad por dividendo. Como en banca, no se usan EV/EBITDA ni deuda neta / EBITDA.",
        "errores": [
            "Comparar el ratio combinado de dos aseguradoras con distinto peso de ramos (autos, salud, empresas, reaseguro).",
            "Atribuir a la gestión un año con muchos siniestros por catástrofes naturales, o al revés.",
            "Fijarse solo en el crecimiento de primas: crecer con un ratio combinado peor puede destruir valor.",
        ],
    },
    {
        "id": "consumo",
        "ibex": "Inditex, Puig, Fluidra y Logista",
        "resumen": "Ventas comparables, margen bruto, tiendas, inventarios y caja.",
        "titulo": "Consumo y distribución",
        "empresas": ["inditex", "puig", "fluidra", "logista"],
        "negocio": "Venden productos al consumidor final, directamente (tiendas propias y online) o a través de distribuidores. "
                   "El negocio depende de la marca, de acertar con el producto, del precio que el cliente está dispuesto a pagar y de la eficiencia "
                   "en compras, logística e inventario.",
        "claves": [
            ("Ventas a tipo de cambio constante", "Crecimiento sin el efecto de las divisas; muestra mejor la evolución real del negocio que la cifra en euros."),
            ("Ventas comparables (like-for-like) y crecimiento orgánico", "Crecimiento en las mismas tiendas o sin adquisiciones. Separa la mejora del negocio existente de la que viene de abrir tiendas o comprar empresas."),
            ("Margen bruto", "Ventas menos coste de lo vendido, sobre ventas. Refleja el poder de marca y de precio: un margen alto y estable indica que la empresa no necesita rebajar para vender."),
            ("Gastos operativos sobre ventas", "Alquileres, personal, logística y marketing. Si crecen menos que las ventas, el margen EBIT mejora (apalancamiento operativo)."),
            ("Inventarios", "Si crecen mucho más que las ventas puede haber exceso de producto, que más tarde obligue a hacer rebajas."),
            ("Caja neta y conversión en caja", "Muchas empresas de consumo no tienen deuda; importa cuánta caja generan con su beneficio y cómo la reparten."),
        ],
        "valoracion": "Se usan el PER y el PER forward, el EV/EBIT y la rentabilidad por flujo de caja libre. Las empresas con marcas fuertes y caja neta "
                      "suelen cotizar con múltiplos altos, por lo que conviene compararlas con su propia historia.",
        "errores": [
            "Mirar las ventas en euros sin descontar el efecto divisa o las aperturas y adquisiciones.",
            "Ignorar la estacionalidad: en moda o en productos de piscina, cada trimestre es muy distinto del anterior.",
            "Comparar márgenes de empresas con modelos distintos (fabricante, distribuidor mayorista, tienda propia).",
        ],
    },
    {
        "id": "salud",
        "ibex": "Grifols y Rovi",
        "resumen": "Ventas por producto, margen bruto, I+D, cartera de medicamentos, patentes y deuda.",
        "titulo": "Farmacia y salud",
        "empresas": ["grifols", "rovi"],
        "negocio": "Desarrollan, fabrican y venden medicamentos, derivados del plasma o productos de diagnóstico, o fabrican para terceros. "
                   "Las barreras de entrada son altas (regulación, patentes, plantas certificadas) y los márgenes también, pero el éxito depende "
                   "de la investigación y de que los reguladores aprueben cada producto.",
        "claves": [
            ("Ventas por producto y área", "Qué productos generan los ingresos y cuánto depende la empresa de unos pocos. La concentración en un producto aumenta el riesgo."),
            ("Margen bruto", "Suele ser alto en farmacia. En negocios como el plasma depende mucho del coste de obtener la materia prima (donantes y centros de recogida)."),
            ("Gasto en I+D", "Inversión en investigación sobre ventas. Es el futuro del negocio, pero gran parte de los proyectos no llega al mercado."),
            ("Cartera de desarrollo (pipeline)", "Productos en fase de ensayo o pendientes de aprobación. Los hitos regulatorios (ensayos, aprobaciones) pueden mover mucho la cotización."),
            ("Patentes y genéricos", "Cuándo expiran las patentes de los productos clave: a partir de entonces llegan competidores con precios más bajos."),
            ("Fabricación para terceros (CDMO)", "Ingresos por fabricar medicamentos de otras compañías: depende de la ocupación de las plantas y de los contratos firmados."),
            ("Deuda neta / EBITDA", "Algunas compañías del sector han crecido con adquisiciones financiadas con deuda; su evolución condiciona el margen de maniobra."),
        ],
        "valoracion": "Se usan el PER, el EV/EBITDA y la rentabilidad por flujo de caja libre. En empresas endeudadas, el EV/EBITDA es más representativo que el PER.",
        "errores": [
            "Dar por hecho que un producto en ensayos llegará al mercado y en las fechas previstas.",
            "Comparar márgenes de un laboratorio innovador con los de un fabricante para terceros.",
            "Ignorar la deuda y las partidas fuera del balance al leer el beneficio.",
        ],
    },
    {
        "id": "inmobiliario",
        "ibex": "Merlin Properties e Inmobiliaria Colonial",
        "resumen": "Rentas, ocupación, like-for-like, valor de los activos (NTA), LTV y FFO.",
        "titulo": "Inmobiliarias (SOCIMI)",
        "empresas": ["merlin", "colonial"],
        "negocio": "Son propietarias de edificios (oficinas, centros comerciales, naves logísticas, centros de datos) y cobran alquileres. "
                   "Como SOCIMI, están obligadas a repartir la mayor parte de su beneficio como dividendo a cambio de un régimen fiscal especial.",
        "claves": [
            ("Rentas brutas y like-for-like", "Ingresos por alquileres y su crecimiento en los mismos edificios, sin compras ni ventas. Muestra si suben las rentas de verdad."),
            ("Ocupación (EPRA)", "Superficie alquilada sobre la disponible. Una ocupación alta da poder para subir rentas al renovar contratos."),
            ("Release spread", "Diferencia entre la renta de los contratos nuevos o renovados y la anterior: indica si el mercado acepta subidas."),
            ("FFO o resultado recurrente", "Beneficio de la actividad de alquiler sin revalorizaciones de los activos. Es la base del dividendo."),
            ("Valor de los activos y NTA por acción", "Valor de tasación de la cartera y valor neto de los activos por acción (EPRA NTA). Las revalorizaciones no son caja, pero cambian el patrimonio."),
            ("LTV (loan to value)", "Deuda neta ÷ valor de los activos. Mide el apalancamiento; por debajo del 40% suele considerarse prudente en el sector."),
        ],
        "valoracion": "Se usan el precio frente al NTA por acción (prima o descuento), el PER sobre el FFO y la rentabilidad por dividendo. "
                      "El beneficio contable no sirve para valorar porque incluye revalorizaciones de los edificios.",
        "errores": [
            "Valorar por el beneficio neto, que sube o baja con las tasaciones.",
            "Olvidar que un descuento sobre el NTA puede reflejar dudas del mercado sobre las tasaciones o sobre la deuda.",
            "Comparar la ocupación de oficinas en el centro de las ciudades con la de la periferia.",
        ],
    },
    {
        "id": "aerolineas",
        "ibex": "IAG",
        "resumen": "Capacidad (AKO), ocupación, ingreso y coste unitario, combustible y deuda.",
        "titulo": "Aerolíneas",
        "empresas": ["iag"],
        "negocio": "Una aerolínea vende asientos. Su resultado depende de cuántos asientos ofrece, cuántos llena, a qué precio los vende y cuánto "
                   "le cuesta volar, sobre todo el combustible y el personal. Es un negocio muy cíclico y con costes fijos altos.",
        "claves": [
            ("Capacidad (AKO / ASK)", "Asientos-kilómetro ofertados: asientos disponibles por kilómetros volados. Indica cuánto crece la oferta."),
            ("Factor de ocupación", "Pasajeros-kilómetro ÷ asientos-kilómetro: qué parte de los asientos se llena. Por encima del 80% suele considerarse alto."),
            ("Ingreso unitario (RASK o ingreso por pasajero-km)", "Cuánto ingresa por cada asiento-kilómetro. Sube si la aerolínea vende más caro o llena más."),
            ("Coste unitario sin combustible (CASK ex-fuel)", "Cuánto le cuesta cada asiento-kilómetro sin contar el combustible: mide la eficiencia que la empresa controla."),
            ("Combustible y coberturas", "El queroseno es uno de los mayores costes. Las coberturas fijan parte del precio y suavizan las subidas (y las bajadas)."),
            ("Deuda neta y arrendamientos", "La flota suele estar financiada con deuda o alquilada; los arrendamientos cuentan como deuda en el balance."),
        ],
        "valoracion": "Se usan el PER, el EV/EBITDA (incluyendo arrendamientos en la deuda) y la rentabilidad por flujo de caja libre. "
                      "Al ser un negocio cíclico, los múltiplos pueden parecer bajos en los mejores años del ciclo.",
        "errores": [
            "Comparar trimestres consecutivos: el verano y el invierno son muy distintos en este sector.",
            "Leer el beneficio sin el efecto del combustible y del tipo de cambio entre el euro, la libra y el dólar.",
            "Olvidar los arrendamientos de aviones al medir la deuda.",
        ],
    },
    {
        "id": "tecnologia",
        "ibex": "Amadeus e Indra",
        "resumen": "Ingresos recurrentes, volumen de transacciones, cartera de contratos, margen e I+D.",
        "titulo": "Tecnología y defensa",
        "empresas": ["amadeus", "indra"],
        "negocio": "Venden software, plataformas o sistemas a empresas y administraciones. Algunas cobran por transacción procesada "
                   "(por ejemplo, cada reserva de viaje), otras por proyectos y contratos plurianuales, como los de defensa o tráfico aéreo.",
        "claves": [
            ("Ingresos recurrentes", "Qué parte de los ingresos se repite cada año (licencias, transacciones, mantenimiento). Más recurrencia da resultados más previsibles."),
            ("Volumen de transacciones", "En plataformas de pago por uso, el número de reservas, pasajeros embarcados u operaciones procesadas es el motor de los ingresos."),
            ("Cartera de pedidos y contratación", "En empresas de proyectos, los contratos firmados pendientes de ejecutar; la ratio contratación ÷ ventas anticipa el crecimiento."),
            ("Margen EBITDA y EBIT", "Las plataformas con mucha escala tienen márgenes altos; los negocios de consultoría y proyectos, más bajos."),
            ("I+D y software capitalizado", "Cuánto se invierte en desarrollo y qué parte se registra como activo en lugar de como gasto, lo que eleva el EBITDA."),
            ("Flujo de caja libre", "Muestra si el beneficio se convierte en caja después de la inversión en tecnología."),
        ],
        "valoracion": "Se usan el PER y el PER forward, el EV/EBITDA y la rentabilidad por flujo de caja libre. En empresas que capitalizan mucho desarrollo, "
                      "el EV/EBIT o el flujo de caja libre son más representativos que el EV/EBITDA.",
        "errores": [
            "Fijarse en el EBITDA sin tener en cuenta el desarrollo capitalizado.",
            "Tomar la cartera de pedidos como ingresos asegurados: los contratos pueden retrasarse o cancelarse.",
            "Olvidar que el volumen de viajes o el gasto en defensa dependen del ciclo económico y de decisiones políticas.",
        ],
    },
    {
        "id": "siderurgia",
        "ibex": "Acerinox y ArcelorMittal",
        "resumen": "Toneladas, precio del acero, coste de materias primas, margen por tonelada y circulante.",
        "titulo": "Acero y materiales",
        "empresas": ["acerinox", "arcelormittal"],
        "negocio": "Fabrican acero común o inoxidable y lo venden a la construcción, la automoción y la industria. Es un negocio cíclico: "
                   "el resultado depende de la diferencia entre el precio de venta y el coste de las materias primas (mineral de hierro, chatarra, "
                   "níquel) y de la energía.",
        "claves": [
            ("Toneladas producidas y vendidas", "El volumen de actividad. Cae cuando la demanda industrial se frena o hay importaciones baratas."),
            ("Precio de venta y spread", "La diferencia entre el precio del acero y el coste de las materias primas por tonelada explica la mayor parte del margen."),
            ("EBITDA por tonelada", "Margen unitario: permite comparar periodos con volúmenes distintos."),
            ("Coste de la energía y del CO₂", "La electricidad, el gas y los derechos de emisión pesan mucho en la producción, sobre todo en Europa."),
            ("Capital circulante e inventarios", "Con precios volátiles, los inventarios pueden generar ganancias o pérdidas contables y mover mucho la caja."),
            ("Aranceles y competencia exterior", "Las medidas de protección comercial en Europa y Estados Unidos influyen en los precios de cada mercado."),
            ("Deuda neta", "En un negocio cíclico, una deuda baja permite atravesar los años malos sin recortar inversión ni dividendos."),
        ],
        "valoracion": "Se usan el EV/EBITDA, el precio / valor en libros y la rentabilidad por flujo de caja libre. El PER es poco útil en la parte baja del ciclo, "
                      "cuando el beneficio es muy bajo o negativo.",
        "errores": [
            "Valorar con el beneficio del mejor año del ciclo como si fuera a repetirse.",
            "Olvidar el efecto de los inventarios cuando los precios del níquel o del acero cambian bruscamente.",
            "Comparar márgenes de acero inoxidable con los de acero común.",
        ],
    },
]
