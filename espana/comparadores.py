"""Comparadores de AIAcciones España: la misma métrica, lado a lado, para empresas de un mismo sector.

Las cifras salen de las fichas (espana/fichas.py), es decir, de los informes del periodo indicado.
Cada indicador: (nombre, unidad, qué mide, sentido, {id_ficha: (valor numérico, texto, nota opcional)}).
sentido: "alto" o "bajo" indica qué lectura es más favorable para el banco (solo en indicadores de negocio);
None en valoración, donde no ordenamos ni juzgamos.
"""

COMPARADORES = [
    {
        "id": "bancos",
        "titulo": "Bancos del IBEX 35",
        "eyebrow": "Banca · 1S 2026",
        "lede": "Los seis bancos del IBEX 35 frente a frente con sus cifras del primer semestre de 2026: crecimiento, rentabilidad, "
                "eficiencia, calidad del crédito, capital y datos de mercado. Cada barra es una cifra publicada por el banco o un cálculo propio indicado.",
        "empresas": ["santander", "bbva", "caixabank", "sabadell", "bankinter", "unicaja"],
        "grupos": [
            ("Crecimiento", [
                ("Beneficio neto 1S 2026", "M€", "Beneficio atribuido a los accionistas en el semestre.", None, {
                    "santander": (8973, "8.973", "Incluye extraordinarios; el ordinario fue 7.328 M€ (+15%)."),
                    "bbva": (6051, "6.051", None),
                    "caixabank": (3203, "3.203", None),
                    "sabadell": (971, "971", "Incluye TSB; el recurrente fue 691 M€."),
                    "bankinter": (605, "605", None),
                    "unicaja": (361, "361", None),
                }),
                ("Variación del beneficio", "%", "Cambio del beneficio neto frente al 1S 2025.", "alto", {
                    "santander": (31, "+31%", "Ordinario: +15%."),
                    "bbva": (11.1, "+11,1%", None),
                    "caixabank": (8.5, "+8,5%", None),
                    "sabadell": (-0.5, "−0,5%", "Recurrente: −14,1%."),
                    "bankinter": (11.7, "+11,7%", None),
                    "unicaja": (7.1, "+7,1%", None),
                }),
                ("Variación del margen de intereses", "%", "Lo que gana el banco entre lo que cobra por los créditos y lo que paga por los depósitos, frente al 1S 2025.", "alto", {
                    "santander": (7, "+7%", None),
                    "bbva": (20.3, "+20,3%", "En euros corrientes; muy influido por México, Turquía y América del Sur."),
                    "caixabank": (2.0, "+2,0%", None),
                    "sabadell": (-2.0, "−2,0%", None),
                    "bankinter": (5.4, "+5,4%", None),
                    "unicaja": (1.7, "+1,7%", None),
                }),
            ]),
            ("Rentabilidad y eficiencia", [
                ("ROTE", "%", "Beneficio sobre el patrimonio tangible: cuánto gana el banco con el capital de sus accionistas.", "alto", {
                    "santander": (15.6, "15,6%", "RoTE ordinario."),
                    "bbva": (22.2, "22,2%", None),
                    "caixabank": (18.0, "18,0%", None),
                    "sabadell": (13.6, "13,6%", "ROTE recurrente."),
                    "bankinter": (20.4, "20,4%", None),
                    "unicaja": (10.0, "10,0%", "12% ajustado por exceso de capital, según el banco."),
                }),
                ("Ratio de eficiencia", "%", "Gastos sobre ingresos (margen bruto): cuántos céntimos gasta para ingresar un euro. Menos es mejor.", "bajo", {
                    "santander": (42.8, "42,8%", None),
                    "bbva": (37.8, "37,8%", None),
                    "caixabank": (39.6, "39,6%", None),
                    "sabadell": (46, "≈46%", "Sin prejubilaciones."),
                    "bankinter": (34.3, "34,3%", None),
                    "unicaja": (45.6, "45,6%", None),
                }),
            ]),
            ("Calidad del crédito", [
                ("Morosidad", "%", "Créditos dudosos sobre el total de créditos. Menos es mejor.", "bajo", {
                    "santander": (2.93, "2,93%", None),
                    "bbva": (2.6, "2,6%", None),
                    "caixabank": (1.78, "1,78%", None),
                    "sabadell": (2.47, "2,47%", None),
                    "bankinter": (1.92, "1,92%", None),
                    "unicaja": (1.8, "1,8%", None),
                }),
                ("Cobertura de la morosidad", "%", "Provisiones dotadas sobre los créditos dudosos. Más es más colchón.", "alto", {
                    "santander": (64, "64%", None),
                    "bbva": (85, "85%", None),
                    "caixabank": (81, "81%", None),
                    "sabadell": (68.7, "68,7%", None),
                    "bankinter": (69.2, "69,2%", None),
                    "unicaja": (82.7, "82,7%", None),
                }),
                ("Coste del riesgo", "pb", "Provisiones por insolvencias del periodo sobre el crédito, en puntos básicos (100 pb = 1%). Menos es mejor.", "bajo", {
                    "santander": (115, "115 pb", "Con peso de Brasil y Argentina."),
                    "bbva": (143, "143 pb", "Con peso de México y Turquía."),
                    "caixabank": (24, "24 pb", None),
                    "sabadell": (40, "40 pb", None),
                    "bankinter": (32, "32 pb", None),
                    "unicaja": (19, "19 pb", None),
                }),
            ]),
            ("Capital", [
                ("CET1", "%", "Capital de máxima calidad sobre activos ponderados por riesgo: la solvencia del banco. Más es más colchón.", "alto", {
                    "santander": (14.0, "14,0%", "Tras la compra de TSB."),
                    "bbva": (12.90, "12,90%", None),
                    "caixabank": (12.54, "12,54%", "Tras la recompra."),
                    "sabadell": (13.11, "13,11%", None),
                    "bankinter": (12.91, "12,91%", None),
                    "unicaja": (15.8, "15,8%", None),
                }),
            ]),
            ("Datos de mercado", [
                ("Capitalización", "M€", "Valor en bolsa de todas las acciones.", None, {
                    "santander": (173090, "≈173.090", None),
                    "bbva": (127090, "≈127.090", None),
                    "caixabank": (85040, "≈85.040", None),
                    "sabadell": (17510, "≈17.510", None),
                    "bankinter": (13480, "≈13.480", None),
                    "unicaja": (8330, "≈8.330", None),
                }),
                ("PER 12 meses", "x", "Precio de la acción entre el beneficio por acción de los últimos 12 meses.", None, {
                    "santander": (13.6, "13,6x", None),
                    "bbva": (12.2, "12,2x", None),
                    "caixabank": (14.7, "14,7x", None),
                    "sabadell": (19.3, "19,3x", "El beneficio de 12 meses incluye la caída del recurrente."),
                    "bankinter": (12.2, "12,2x", None),
                    "unicaja": (12.9, "12,9x", None),
                }),
                ("Precio / valor en libros", "x", "Precio de la acción entre el patrimonio contable por acción.", None, {
                    "santander": (1.49, "1,49x", None),
                    "bbva": (1.99, "1,99x", None),
                    "caixabank": (2.2, "≈2,2x", None),
                    "sabadell": (1.42, "1,42x", None),
                    "bankinter": (2.0, "≈2,0x", None),
                    "unicaja": (1.23, "1,23x", None),
                }),
                ("Rentabilidad por dividendo", "%", "Dividendos de los últimos 12 meses entre el precio. Puede incluir dividendos extraordinarios.", None, {
                    "santander": (2.1, "2,1%", None),
                    "bbva": (4.0, "4,0%", None),
                    "caixabank": (4.1, "4,1%", None),
                    "sabadell": (7.4, "7,4%", "Incluye el dividendo extraordinario por la venta de TSB."),
                    "bankinter": (4.0, "4,0%", None),
                    "unicaja": (5.3, "5,3%", None),
                }),
            ]),
        ],
        "nota_mercado": "Precios del 6 al 13 de octubre de 2026, según la ficha de cada banco. Los múltiplos dependen del precio de cada día, "
                        "del negocio y del país de cada banco: un PER distinto no indica por sí solo que una acción esté cara o barata, "
                        "y aquí no los ordenamos ni los juzgamos.",
        "nota": "Cada banco calcula sus ratios con criterios propios (por ejemplo, ROTE ordinario o recurrente, o eficiencia con o sin prejubilaciones), "
                "así que las comparaciones son orientativas. Santander y BBVA tienen gran parte del negocio fuera de España, con más morosidad y "
                "coste del riesgo por su exposición a Latinoamérica y Turquía. Fuentes: informes de resultados del 1S 2026 de cada banco en la CNMV "
                "y las fuentes citadas en su ficha.",
    },
]
