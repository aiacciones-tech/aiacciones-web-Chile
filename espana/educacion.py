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
        "resumen": "Producción y mix, precio de la electricidad, activos regulados, inversiones y deuda.",
        "titulo": "Eléctricas y redes",
        "empresas": ["iberdrola", "endesa", "redeia", "enagas"],
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
        "resumen": "Tráfico y pasajeros, tarifas, ingresos comerciales y dividendos de proyectos.",
        "titulo": "Infraestructuras y concesiones",
        "empresas": ["ferrovial", "aena"],
        "negocio": "Gestionan activos de larga duración, como autopistas de peaje, aeropuertos o aparcamientos, a menudo bajo concesión. "
                   "Cobran tarifas por su uso y reparten la caja que generan los activos. Algunas también construyen.",
        "claves": [
            ("Tráfico y pasajeros", "Vehículos en las autopistas o pasajeros en los aeropuertos: el motor de los ingresos."),
            ("Tarifas", "Cuánto se cobra por uso y cómo se actualiza (por inflación, por regulación o libremente). En aeropuertos regulados, las tarifas las fija el regulador por periodos."),
            ("Ingresos comerciales", "En aeropuertos, tiendas, restauración y aparcamientos: crecen con el gasto por pasajero."),
            ("Dividendos de proyectos", "En grupos con participaciones en concesiones, la caja que reciben de cada activo es más relevante que el beneficio consolidado."),
            ("Margen de construcción y cartera", "Si construyen, el margen suele ser estrecho y la cartera de obra anticipa la actividad futura."),
            ("Vida de las concesiones y deuda", "Cuántos años quedan de concesión y cómo está financiado cada activo: la deuda de proyectos suele ir sin recurso a la matriz."),
        ],
        "valoracion": "EV/EBITDA, rentabilidad por dividendo y, en grupos de concesiones, la suma de las partes (valor de cada activo por separado). "
                      "El PER puede ser muy alto o muy bajo por plusvalías y amortizaciones de las concesiones.",
        "errores": [
            "Valorar por el PER un grupo cuyo beneficio cambia mucho por la venta de activos.",
            "Ignorar las revisiones de tarifas reguladas, que fijan los ingresos durante varios años.",
        ],
    },
]
