# Fichas de AIAcciones España: una por empresa, solo con cifras reales de nuestros vídeos.
# Para agregar una empresa: copia un dict, rellénalo con las cifras del vídeo y corre `python3 espana/build.py`.
# Nada de cifras de ejemplo: si un dato no está en el vídeo o en sus fuentes, no va.

FICHAS = [
    {
        "id": "iberdrola",
        "nombre": "Iberdrola",
        "ticker": "IBE",
        "sector": "Eléctricas · redes y renovables",
        "lede": "Eléctrica con redes reguladas en España, Reino Unido, Estados Unidos y Brasil, y generación renovable. "
                "Las redes aportan ya más de la mitad del EBITDA. En el primer semestre de 2026 vendió su negocio en México.",
        "periodo": "1S 2026",
        "periodo_largo": "primer semestre de 2026",
        "titular": "Beneficio neto ajustado de 3.565 M€ (+7,8%), un 5,5% por encima del consenso (3.380 M€, Bankinter Análisis). "
                   "El beneficio reportado, 4.336 M€ (+21,7%), incluye 953 M€ de plusvalía por la venta de México.",
        "precio": "21,35 €",
        "precio_fecha": "9-oct-2026",
        "multiplos": [("PER 12 meses", "25,9x"), ("PER forward", "19,9x"), ("EV/EBITDA", "13,7x"),
                      ("Rentab. dividendo", "3,2%"), ("FCF yield", "2,2%"), ("Capitalización", "~138.500 M€")],
        "multiplos_nota": "Con precio de 21,35 € al 9-oct-2026 (stockanalysis.com). A cierre de 2023, 2024 y 2025 el PER era 16,1x, 15,2x y 20,1x. "
                          "La acción subió un 30% en 12 meses.",
        "tabla_titulo": "Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025",
        "tabla": [
            ("Ingresos", "22.469", "+1,7%"),
            ("EBITDA ajustado", "8.050", "+7,4%"),
            ("EBITDA redes", "4.213", "+13%"),
            ("EBITDA generación y clientes", "3.790", "+1%"),
            ("Beneficio neto ajustado", "3.565", "+7,8%"),
            ("Beneficio neto reportado", "4.336", "+21,7%"),
            ("BPA ajustado (calculado)", "~0,55 €", ""),
        ],
        "kpi": "Margen EBITDA 35,8% (34,8% en 1S 2025 comparable). Ingresos +4,2% comparables sin México; EBITDA +8,8% sin divisas. "
               "Inversión de 7.010 M€ (+25%; redes +42%). Deuda neta ajustada 54.000 M€ (3,5x EBITDA), con previsión de ~56.000 M€ a cierre de año. "
               "Coste medio de la deuda 5,1%. Liquidez 21.500 M€.",
        "guia": "Guía 2026 reafirmada: beneficio neto ajustado +8% o más (más de 6.700 M€). Compra del 80% de Caruna (Finlandia) por ~2.000 M€, "
                "con cierre previsto en el 1T 2027. Dividendo total del ejercicio 0,685 € (+6,2%). Nuevo plan estratégico en 2027.",
        "positivos": ["Las redes crecen un 13% y su base de activos regulados, un 11%.",
                      "El beneficio ajustado superó al consenso y la guía anual se mantiene.",
                      "La venta de México dejó 953 M€ de plusvalía y el dividendo del ejercicio sube un 6,2%."],
        "riesgos": ["Las divisas: la debilidad del dólar y la libra resta resultados.",
                    "La deuda sube con la inversión y su coste ya supera el 5%.",
                    "Buena parte del beneficio depende de decisiones regulatorias en Reino Unido, Estados Unidos y Brasil."],
        "videos": [("RGgaT31jOxk", "Iberdrola resultados 1S 2026: beneficio ajustado +7,8%, 5,5% sobre el consenso | Redes +13%")],
        "proximo": "2026-10-21",
        "fuentes": "Iberdrola, presentación de resultados del primer semestre 2026 (CNMV, 22-jul-2026); Bankinter Análisis (consenso, 22-jul-2026); "
                   "stockanalysis.com (precio y múltiplos, 9-oct-2026).",
        "fuentes_corto": "Bankinter Análisis y stockanalysis.com",
        "elaborado": "12-oct-2026, 08:00",
    },
    {
        "id": "redeia",
        "nombre": "Redeia",
        "ticker": "RED",
        "sector": "Eléctricas · red de transporte",
        "lede": "Matriz de Red Eléctrica, que opera y transporta la electricidad en alta tensión en España. "
                "También tiene negocio internacional (Latinoamérica) y de fibra óptica y satélites (Reintel, Hispasat).",
        "periodo": "1S 2026",
        "periodo_largo": "primer semestre de 2026",
        "titular": "Beneficio neto de 280,4 M€ (+4,0%), en línea con lo esperado según Renta 4 e Investing.com. "
                   "El EBITDA (+5,8%) incluye 24 M€ de un cambio contable regulatorio; sin él crece cerca de un 2% (calculado).",
        "precio": "14,80 €",
        "precio_fecha": "2-oct-2026",
        "multiplos": [("PER 12 meses", "16,6x"), ("PER forward", "15,6x"), ("EV/EBITDA", "11,3x"),
                      ("Rentab. dividendo", "5,4%"), ("FCF yield", "−6,8%"), ("Capitalización", "~8.006 M€")],
        "multiplos_nota": "Con precio de 14,80 € al 2-oct-2026 (stockanalysis.com). A cierre de 2023, 2024 y 2025 el PER era 11,7x, 25,4x y 16,8x, "
                          "y el EV/EBITDA 10,4x, 13,9x y 13,3x. Capitalización calculada con 540,9 M de acciones.",
        "tabla_titulo": "Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025",
        "tabla": [
            ("Ingresos", "869,2", "+7,1%"),
            ("Transporte y operación en España", "779,6", "+9,1%"),
            ("EBITDA", "672,6", "+5,8%"),
            ("EBIT", "422,6", "+1,6%"),
            ("Beneficio neto", "280,4", "+4,0%"),
            ("BPA (calculado)", "~0,52 €", "+4%"),
        ],
        "kpi": "Margen EBITDA 77,4% (calculado). EBITDA por negocio: España 554,5 M€ (+10%), internacional 57,7 M€, fibra óptica 51,1 M€ (57,8 en 1S 2025). "
               "Inversión de 657 M€ (+9%), 551 M€ en la red de transporte. Deuda neta 5.009 M€, 465 M€ menos que en diciembre; "
               "deuda neta / EBITDA ~3,9x (calculado). Coste medio de la deuda 2,35%.",
        "guia": "Guía 2026: beneficio neto ~510 M€ y EBITDA superior a 1.250 M€; el primer semestre ya suma el 55% del beneficio objetivo (calculado). "
                "Plan 2026-2029: 6.500 M€ de inversión y dividendo +2% anual hasta 0,87 € en 2029. Apagón de abril de 2025: sin provisiones; "
                "Redeia ha presentado alegaciones al expediente de la CNMC.",
        "positivos": ["Transporte en España: EBITDA +10% y nueva tasa de retribución del 6,58%.",
                      "La deuda neta bajó 465 M€ en el semestre.",
                      "El beneficio lleva el 55% de la guía anual."],
        "riesgos": ["El expediente de la CNMC por el apagón sigue abierto.",
                    "La fibra óptica y el negocio internacional pierden peso.",
                    "La inversión récord deja el flujo de caja libre en negativo y la deuda subirá en los próximos años."],
        "videos": [("wbzhyA-076o", "Redeia resultados 1S 2026: beneficio +4%, en línea con el consenso | Deuda neta −465 M€"),
                   ("oFncLSa2iN4", "Redeia 1S 2026 en 60 segundos (Short)")],
        "proximo": "2026-10-28",
        "proximo_estimado": True,
        "fuentes": "Redeia, nota de prensa de resultados del primer semestre 2026 (29-jul-2026, CNMV y redeia.com); Renta 4 Banco / Capitalbolsa e Investing.com "
                   "(comparación con el consenso, 29-jul-2026); Estrategias de Inversión y elDiario.es (detalle por negocio y deuda, 29-jul-2026); "
                   "Bankinter Análisis (guía 2026, 29-abr-2026); Merca2 (plan 2026-2029, 27-feb-2026); stockanalysis.com (precio y múltiplos, 2-oct-2026).",
        "fuentes_corto": "Renta 4 Banco, Investing.com, Bankinter Análisis, Estrategias de Inversión, elDiario.es, Merca2 y stockanalysis.com",
        "elaborado": "12-oct-2026, 16:00",
    },
    {
        "id": "bankinter",
        "nombre": "Bankinter",
        "ticker": "BKT",
        "sector": "Banca",
        "lede": "Banco español con negocio en España, Portugal e Irlanda, centrado en banca de empresas, banca privada y gestión de patrimonios. "
                "En un banco, los ingresos son el margen bruto y la calidad del balance se mide con la morosidad y el capital.",
        "periodo": "1S 2026",
        "periodo_largo": "primer semestre de 2026",
        "titular": "Beneficio neto de 605 M€ (+11,7%), su mayor beneficio semestral. El 2T (315 M€) superó al consenso en un 8% según Renta 4; "
                   "Jefferies señala 23 M€ de comisiones extraordinarias y, sin ellas, un resultado antes de impuestos prácticamente en línea.",
        "precio": "15,00 €",
        "precio_fecha": "9-oct-2026",
        "multiplos": [("PER 12 meses", "12,2x"), ("PER forward", "10,8x"), ("Precio / valor en libros", "~2,0x"),
                      ("Rentab. dividendo", "4,0%"), ("Capitalización", "~13.480 M€")],
        "multiplos_nota": "Con precio de 15,00 € al 9-oct-2026 (stockanalysis.com); precio / valor en libros calculado. A cierre de 2022, 2023 y 2024 el PER era 10,3x, 6,2x y 7,2x, "
                          "y el precio / valor en libros 1,15x, 0,98x y 1,17x. En un banco no se usan EV/EBITDA ni flujo de caja libre.",
        "tabla_titulo": "Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025",
        "tabla": [
            ("Margen de intereses", "1.160", "+5,4%"),
            ("Comisiones netas", "440,4", "~+16%"),
            ("Margen bruto", "1.603", "+7,3%"),
            ("Costes", "550,6", "+2,7%"),
            ("Margen de explotación", "1.052,4", "+9,8%"),
            ("Beneficio neto", "605", "+11,7%"),
            ("BPA (calculado)", "~0,67 €", "+11,7%"),
        ],
        "kpi": "Eficiencia 34,3% (35,9% en 1S 2025, calculado); ROE 19,1%; ROTE 20,4%. Morosidad 1,92% (−22 pb), cobertura 69,2%, coste del riesgo 32 pb. "
               "CET1 12,91% (mínimo BCE 8,58%). Crédito 87.153 M€ (+4,6%); recursos de clientes y gestionados 162.085 M€ (+9,6%); nueva producción hipotecaria −16%. "
               "Beneficio antes de impuestos: España 716 M€ (+11%), Portugal 114 M€ (+9%); Irlanda, crédito 5.200 M€ (+24%).",
        "guia": "Guía 2026 (según Renta 4): margen de intereses creciendo en línea con el crédito, diferencial de clientes ~2,7%, comisiones con crecimiento de un dígito alto, "
                "eficiencia por debajo del 35%, coste del riesgo 33 pb y crédito creciendo a un dígito medio (en el semestre, algo menos del 4%).",
        "positivos": ["Comisiones netas ~+16% y fondos de terceros casi +24%.",
                      "Eficiencia del 34,3%: los costes suben un 2,7% y el margen bruto un 7,3%.",
                      "Menos morosidad (1,92%) y más capital (CET1 12,91%)."],
        "riesgos": ["Parte de la sorpresa del 2T vino de 23 M€ de comisiones extraordinarias.",
                    "El crédito crece por debajo de la guía y la nueva producción hipotecaria cae un 16%.",
                    "Según Jefferies, el margen de intereses tiene menos recorrido de mejora que en otros bancos."],
        "videos": [("k7qJSVY5__k", "Bankinter resultados 1S 2026: beneficio récord +11,7%; el 2T supera al consenso | Eficiencia 34,3%"),
                   ("oboYRN0_OH4", "Bankinter 1S 2026 en 60 segundos (Short)")],
        "proximo": "2026-10-22",
        "fuentes": "Bankinter, nota de resultados del primer semestre 2026 (23-jul-2026, CNMV y bankinter.com); Renta 4 Banco / Capitalbolsa (consenso y guía, 23-jul-2026); "
                   "Jefferies / Bolsamania (extraordinarios, 23-jul-2026); stockanalysis.com (precio y múltiplos, 9-oct-2026).",
        "fuentes_corto": "Renta 4 Banco, Jefferies, Capitalbolsa, Bolsamania y stockanalysis.com",
        "elaborado": "13-oct-2026, 17:00",
    },
]
