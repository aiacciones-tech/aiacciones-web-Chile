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
    {'id': 'santander',
     'nombre': 'Banco Santander',
     'ticker': 'SAN',
     'sector': 'Banca',
     'lede': 'Mayor banco español por capitalización, con negocio en Europa (España, Reino Unido, Portugal) y América (Brasil, Estados Unidos, México). '
             'En 2026 compró TSB en Reino Unido y Webster en Estados Unidos, y vendió su banco en Polonia. En un banco, los ingresos son el margen bruto '
             'y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio ordinario de 7.328 M€ (+15%), su mayor beneficio semestral; el atribuido, 8.973 M€ (+31%), incluye la plusvalía por la venta '
                'de Polonia. El 2T (3.768 M€) quedó en línea con el consenso: 3.750 M€ en el sondeo de Reuters y 3.771 M€ en el consenso recopilado por '
                'el banco.',
     'precio': '12,02 €',
     'precio_fecha': '9-oct-2026',
     'multiplos': [('PER 12 meses', '13,6x'),
                   ('PER forward', '10,5x'),
                   ('Precio / valor en libros', '1,49x'),
                   ('Rentab. dividendo', '2,1%'),
                   ('Capitalización', '~173.090 M€')],
     'multiplos_nota': 'Con precio de 12,02 € al 9-oct-2026 (stockanalysis.com); precio / valor tangible 1,91x y recompras equivalentes al 3,5% anual. A '
                       'cierre de 2022, 2023, 2024 y 2025 el PER era 5,1x, 5,7x, 5,7x y 11,0x, y el precio / valor en libros 0,48x, 0,58x, 0,63x y '
                       '1,31x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Margen de intereses', '22.711', '+7%'),
               ('Comisiones netas', '6.851', '+9%'),
               ('Margen bruto', '30.847', '+6%'),
               ('Costes', '13.211', '0%'),
               ('Margen neto', '17.636', '+12%'),
               ('Dotaciones por insolvencias', '6.574', '+9%'),
               ('Beneficio ordinario', '7.328', '+15%'),
               ('Beneficio atribuido', '8.973', '+31%'),
               ('BPA ordinario (calculado)', '~0,51 €', '+20%')],
     'kpi': 'Eficiencia 42,8% (−2,9 pp); RoTE ordinario 15,6% (+0,7 pp). Morosidad 2,93% (−7 pb en el trimestre), cobertura 64%, coste del riesgo 1,15%. '
            'CET1 14,0% tras la compra de TSB (−55 pb). Crédito +9% y recursos de clientes +11% en euros constantes (+5% y +7% sin TSB); 182 M de '
            'clientes (+12 M). Beneficio por países: España 2.534 M€ (+12%), Brasil 1.093 M€ (+10%), EE. UU. 989 M€ (+18%), México 897 M€ (+13%), Reino '
            'Unido 725 M€ (+30%, con TSB). Por negocios: banca comercial 4.124 M€ (+13%), CIB 1.742 M€ (+18%), Wealth 1.083 M€ (+20%), Openbank 827 M€ '
            '(−21%).',
     'guia': 'Objetivos 2026 reiterados (euros constantes, sin las compras de 2025-26): ingresos creciendo a un dígito medio, costes a la baja y '
             'beneficio ordinario por encima de los 14.101 M€ de 2025 (en el semestre, el 52%, calculado). CET1 entre el 12% y el 13%. Remuneración de '
             '~50% del beneficio, a partes iguales entre dividendo y recompras; ~9.000 M€ de recompras con cargo a 2025-26, incluida una nueva de ~1.800 '
             'M€.',
     'positivos': ['Beneficio ordinario récord (+15%) y BPA ordinario +20%, con ayuda de las recompras.',
                   'Costes planos (−1% en euros constantes) y eficiencia del 42,8%, casi 3 puntos mejor.',
                   'CET1 del 14% después de comprar TSB y ~9.000 M€ en recompras 2025-26.'],
     'riesgos': ['Las dotaciones suben un 9%, sobre todo por Argentina, y el coste del riesgo (1,15%) sigue alto.',
                 'Openbank cae un 21% por la financiación de coches en Reino Unido y el fin de las ayudas al coche eléctrico en EE. UU.',
                 'La integración de TSB y Webster tiene costes (250 M€ de reestructuración en TSB) y reduce el capital.'],
     'videos': [('-ED5j67j-0g', 'Banco Santander resultados 1S 2026: beneficio ordinario récord +15%; el 2T, en línea | BPA +20%'),
                ('ZesAasxjui0', 'Banco Santander 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-28',
     'fuentes': 'Banco Santander, nota y presentación de resultados del primer semestre 2026 (22-jul-2026, CNMV y santander.com); Reuters / '
                'MarketScreener y Benzinga (consenso, 21-22-jul-2026); Infobae y El Español (desglose por países, 22-jul-2026); stockanalysis.com '
                '(precio y múltiplos, 9-oct-2026).',
     'fuentes_corto': 'Reuters, Benzinga, Infobae, El Español y stockanalysis.com',
     'elaborado': '13-oct-2026, 19:00'},
    {'id': 'bbva',
     'nombre': 'BBVA',
     'ticker': 'BBVA',
     'sector': 'Banca',
     'lede': 'Banco español con negocio en España, México, Turquía y América del Sur, además de banca mayorista internacional. En un banco, los ingresos '
             'son el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio atribuido de 6.051 M€ (+11,1%), su mayor beneficio semestral. El 2T (3.062 M€, récord trimestral) superó en un 4,5% al '
                'consenso que recopila el propio banco y en un 2,6% al de Bloomberg (cálculos propios); Jefferies sitúa la sorpresa en torno al 4%.',
     'precio': '23,11 €',
     'precio_fecha': '9-oct-2026',
     'multiplos': [('PER 12 meses', '12,2x'),
                   ('PER forward', '10,4x'),
                   ('Precio / valor en libros', '1,99x'),
                   ('Rentab. dividendo', '4,0%'),
                   ('Capitalización', '~127.090 M€')],
     'multiplos_nota': 'Con precio de 23,11 € al 9-oct-2026 (stockanalysis.com). A cierre de 2022, 2023, 2024 y 2025 el PER era 5,5x, 6,3x, 5,6x y '
                       '11,3x, y el precio / valor en libros 0,66x, 0,87x, 0,91x y 1,85x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025 (euros corrientes)',
     'tabla': [('Margen de intereses', '15.164', '+20,3%'),
               ('Comisiones netas', '4.572', '+14,0%'),
               ('Margen bruto', '21.159', '+17,3%'),
               ('Gastos de explotación', '8.000', '+17,9%'),
               ('Deterioro de activos financieros', '3.497', '+26,6%'),
               ('Beneficio atribuido', '6.051', '+11,1%'),
               ('BPA', '1,04 €', '+14,1%')],
     'kpi': 'Eficiencia 37,8% (37,6% en 1S 2025); ROE 21,1%; ROTE 22,2%. Morosidad 2,6% (2,9% un año antes), cobertura 85%, coste del riesgo 1,43%. CET1 '
            '12,90% (requerimiento 8,98%). Préstamos 509.424 M€ (+10,6% frente a diciembre); depósitos 532.981 M€ (+6,1%). Beneficio atribuido por área '
            '(sin efecto divisa): México 2.979 M€ (+8,2%), España 2.172 M€ (+2,3%), América del Sur 556 M€ (+33,6%), Turquía 532 M€ (+29,1%).',
     'guia': 'Guía 2026 (conferencia de resultados, según Investing.com y Merca2): ROTE en torno al 21% (antes ~20%); España, margen de intereses '
             'creciendo a un dígito bajo-medio y eficiencia por debajo del 35%; México, crédito ~+10%; Turquía, coste del riesgo de unos 220 pb. '
             'Objetivo de 48.000 M€ de beneficio acumulado en 2025-2028. Nueva recompra de 2.000 M€ y dividendo a cuenta 2026 de 0,37 € (+16%).',
     'positivos': ['2T récord (3.062 M€), un 4,5% sobre el consenso de BBVA (calculado).',
                   'ROTE del 22,2% y guía del año elevada a en torno al 21%.',
                   'Menos morosidad (2,6%), nueva recompra de 2.000 M€ y dividendo a cuenta un 16% mayor.'],
     'riesgos': ['Los deterioros suben un 26,6% y los gastos un 17,9%, más que el margen bruto.',
                 'España creció poco: beneficio +2,3%.',
                 'Peso de México, Turquía y América del Sur y riesgo de divisa; en Turquía, coste del riesgo de unos 220 pb.'],
     'videos': [('pUB4hXT_RaQ', 'BBVA resultados 1S 2026: beneficio récord +11,1%; el 2T supera al consenso | ROTE 22,2%'),
                ('9eV_Y5hfj-o', 'BBVA 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-29',
     'fuentes': 'BBVA, informe de resultados del primer semestre 2026 (30-jul-2026, CNMV y bbva.com); Benzinga (consenso de BBVA y de Bloomberg, 27 y '
                '30-jul-2026); Merca2 (Jefferies y Renta 4, 31-jul-2026); Investing.com (conferencia de resultados, 30-jul-2026); El Español (dividendo '
                'a cuenta, 1-oct-2026); stockanalysis.com (precio y múltiplos, 9-oct-2026).',
     'fuentes_corto': 'Benzinga, Merca2, Jefferies, Renta 4, Investing.com, El Español y stockanalysis.com',
     'elaborado': '13-oct-2026, 19:00'},
    {'id': 'sabadell',
     'nombre': 'Banco Sabadell',
     'ticker': 'SAB',
     'sector': 'Banca',
     'lede': 'Banco español centrado en empresas y particulares, con negocio también en México. En 2026 vendió su filial británica TSB a Banco Santander '
             '(cerrada el 1-may-2026), tras la OPA de BBVA, que quedó desierta en octubre de 2025. En un banco, los ingresos son el margen bruto y la '
             'calidad del balance se mide con la morosidad y el capital.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 971 M€ (−0,5%), con cuatro meses de TSB y 322 M€ de plusvalía neta por su venta; el beneficio recurrente fue de 691 '
                'M€ (−14,1%). El 2T (624 M€, calculado) quedó un 2% por debajo del consenso según Renta 4, por mayores provisiones, aunque el margen '
                'bruto lo superó en un 2%.',
     'precio': '3,583 €',
     'precio_fecha': '13-oct-2026',
     'multiplos': [('PER 12 meses', '19,3x'),
                   ('PER forward', '11,5x'),
                   ('Precio / valor en libros', '1,42x'),
                   ('Rentab. dividendo', '7,4%'),
                   ('Capitalización', '~17.510 M€')],
     'multiplos_nota': 'Con precio de 3,583 € al 13-oct-2026 (stockanalysis.com). La rentabilidad por dividendo usa el dividendo ordinario (0,26 €) y no '
                       'incluye el extraordinario de 0,50 € pagado en mayo. A cierre de 2022, 2023, 2024 y 2025 el PER era 6,3x, 5,0x, 5,9x y 10,3x, y '
                       'el precio / valor en libros 0,38x, 0,44x, 0,68x y 1,19x. Sin TSB el perímetro del grupo cambia. En un banco no se usan EV/EBITDA '
                       'ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Margen de intereses', '1.774', '−2,0%'),
               ('Comisiones netas', '643', '−0,9%'),
               ('Margen bruto', '2.463', '−2,8%'),
               ('Costes', '1.227', '+13%'),
               ('Margen antes de dotaciones', '1.236', '−14,7%'),
               ('Beneficio neto', '971', '−0,5%'),
               ('Beneficio recurrente', '691', '−14,1%'),
               ('BPA (calculado)', '~0,20 €', '')],
     'kpi': 'ROTE recurrente 13,6% (objetivo 14,5% en 2026). Eficiencia ~46% sin prejubilaciones (~43% en 1S 2025, calculado); costes recurrentes +4,9%. '
            'Morosidad 2,47% (2,55% en el 1T), cobertura 68,7%, coste del riesgo 40 pb. CET1 13,11% (+20 pb en el trimestre). Crédito vivo 125.184 M€ '
            '(+5,5%); recursos de clientes 188.110 M€ (+6,4%). En el 2T, margen de intereses 902 M€ (+3,4% t/t) y comisiones 328 M€ (+4% t/t).',
     'guia': 'Guía 2026 mantenida: margen de intereses creciendo más de un 1%, comisiones a un dígito medio, costes recurrentes por debajo del +3%, '
             'coste del riesgo ~40 pb y ROTE recurrente del 14,5% (16% en 2027). Nueva recompra de 331 M€, tras un dividendo extraordinario de 0,50 € '
             'por acción pagado en mayo.',
     'positivos': ['El margen de intereses (+3,4%) y las comisiones (+4%) vuelven a crecer en el 2T frente al 1T.',
                   'Crédito vivo +5,5% y morosidad a la baja (2,47%).',
                   'CET1 del 13,11%, recompra de 331 M€ y dividendo extraordinario por la venta de TSB.'],
     'riesgos': ['El beneficio recurrente cae un 14,1% y el del 2T quedó algo por debajo del consenso.',
                 'Los costes recurrentes suben un 4,9%, por encima de la guía anual (<3%).',
                 'Las comisiones caen un 1% en el semestre, frente a una guía de crecimiento de un dígito medio.'],
     'videos': [('wkQGwk63kTE', 'Banco Sabadell resultados 1S 2026: beneficio 971 M€ con TSB; recurrente -14,1% | CET1 13,11%'),
                ('7YzKyAdIs68', 'Banco Sabadell 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-29',
     'fuentes': 'Banco Sabadell, nota de resultados del primer semestre 2026 (24-jul-2026, CNMV y grupbancsabadell.com); Europa Press, Estrategias de '
                'Inversión y Merca2 (24-jul-2026); Renta 4 Banco (consenso y guía, 24-jul-2026); Capitalbolsa / Bolsamania (24-jul-2026); OCU (OPA, '
                '17-oct-2025); Ara (venta de TSB, 1-may-2026); stockanalysis.com (precio y múltiplos, 13-oct-2026).',
     'fuentes_corto': 'Renta 4 Banco, Europa Press, Capitalbolsa, Merca2 y stockanalysis.com',
     'elaborado': '13-oct-2026, 19:00'},
    {'id': 'unicaja',
     'nombre': 'Unicaja',
     'ticker': 'UNI',
     'sector': 'Banca',
     'lede': 'Banco español minorista, con fuerte presencia en Andalucía, Castilla y León, Castilla-La Mancha, Asturias y Extremadura. En un banco, los '
             'ingresos son el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 361 M€ (+7,1%). El 2T (201 M€) superó al consenso en un 10% según Investing.com, sobre todo por menores deterioros '
                '(41 M€ frente a 55 esperados); el margen de intereses quedó en línea y las comisiones, un 2% por debajo. Unicaja mejoró su guía de '
                'beneficio para 2026.',
     'precio': '3,242 €',
     'precio_fecha': '13-oct-2026',
     'multiplos': [('PER 12 meses', '12,9x'),
                   ('PER forward', '11,8x'),
                   ('Precio / valor en libros', '1,23x'),
                   ('Rentab. dividendo', '5,3%'),
                   ('Capitalización', '~8.330 M€')],
     'multiplos_nota': 'Con precio de 3,242 € al 13-oct-2026 (stockanalysis.com). A cierre de 2022, 2023, 2024 y 2025 el PER era 10,1x, 9,1x, 5,7x y '
                       '11,4x, y el precio / valor en libros 0,42x, 0,36x, 0,48x y 1,01x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Margen de intereses', '755', '+1,7%'),
               ('Comisiones netas', '269', '+2,6%'),
               ('Margen bruto', '1.085', '+2,5%'),
               ('Costes (calculado)', '494', '~+5%'),
               ('Margen de explotación', '590', '~+0,5%'),
               ('Beneficio neto', '361', '+7,1%'),
               ('BPA (calculado)', '~0,14 €', 'n. d.')],
     'kpi': 'Eficiencia 45,6% (44,6% en 1S 2025); ROTE 10,0% (12% ajustado por exceso de capital). Morosidad 1,8% (−38 pb), cobertura de dudosos 82,7%, '
            'coste del riesgo 19 pb. CET1 15,8% (exceso de 2.201 M€ sobre requerimientos). Crédito sano 49.941 M€ (+3,7%); depósitos de clientes 76.264 '
            'M€ (+4,1%); recursos fuera de balance +12,7%; nueva producción hipotecaria +39,5%. Comisiones no bancarias: 53% del total (+11,8%).',
     'guia': 'Guía 2026, revisada el 31-jul-2026 (según Investing.com): beneficio creciendo a un dígito medio y margen de intereses a un dígito '
             'bajo-medio (antes: superar 2025), coste del riesgo de 20-25 pb (antes: menos de 30 pb), comisiones a un dígito bajo y costes a un dígito '
             'medio. Remuneración del 95% del beneficio en efectivo; dividendo a cuenta de 8,44 céntimos por acción (+28%), pagado el 24-sep-2026.',
     'positivos': ['El 2T superó al consenso en un 10% y la guía de beneficio sube.',
                   'Morosidad del 1,8% (−38 pb) y coste del riesgo de 19 pb.',
                   'Nueva producción hipotecaria +39,5% y dividendo a cuenta +28%.'],
     'riesgos': ['La sorpresa del 2T vino de menos deterioros; las comisiones quedaron un 2% por debajo de lo esperado.',
                 'Los costes suben cerca de un 5% y el margen bruto un 2,5%: la eficiencia empeora al 45,6%.',
                 'El coste de los depósitos sube tras la subida de tipos del BCE y no hay guía para 2027.'],
     'videos': [('QmTUeCVBUk4', 'Unicaja resultados 1S 2026: beneficio +7,1%; el 2T supera al consenso un 10% | Guía al alza'),
                ('zoldZTxXavE', 'Unicaja 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-30',
     'fuentes': 'Unicaja, nota de resultados del primer semestre 2026 (31-jul-2026, CNMV y unicajabanco.com); Investing.com (consenso y guía, '
                '31-jul-2026); XTB y Bolsamania (desglose trimestral y de costes, 31-jul-2026); stockanalysis.com (precio y múltiplos, 13-oct-2026).',
     'fuentes_corto': 'Investing.com, XTB, Bolsamania y stockanalysis.com',
     'elaborado': '13-oct-2026, 19:00'},
    {'id': 'caixabank',
     'nombre': 'CaixaBank',
     'ticker': 'CABK',
     'sector': 'Banca',
     'lede': 'Mayor banco por clientes en España, con BPI en Portugal y un negocio relevante de seguros y gestión patrimonial. En un banco, los ingresos '
             'son el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 3.203 M€ (+8,5%), su mayor beneficio semestral. El 2T (1.631 M€) superó en un 4,6% el consenso que publica el banco '
                '(XTB; calculado), aunque la acción cayó un 7,1% el día de los resultados con la guía 2026 sin cambios.',
     'precio': '12,36 €',
     'precio_fecha': '6-oct-2026',
     'multiplos': [('PER 12 meses', '14,7x'),
                   ('PER forward', '12,1x'),
                   ('Precio / valor en libros', '~2,2x'),
                   ('Rentab. dividendo', '4,1%'),
                   ('Capitalización', '~85.040 M€')],
     'multiplos_nota': 'Con precio de 12,36 € al 6-oct-2026 (stockanalysis.com); precio / valor en libros calculado con un valor contable de 5,56 € por '
                       'acción (jun-2026). A cierre de 2022, 2023, 2024 y 2025 el PER era 10,1x, 6,1x, 6,8x y 13,0x, y el precio / valor en libros '
                       '0,86x, 0,77x, 1,02x y 1,90x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Margen de intereses', '5.390', '+2,0%'),
               ('Ingresos por servicios', '2.772', '+7,4%'),
               ('Margen bruto', '8.338', '+3,7%'),
               ('Gastos', '3.320', '+4,5%'),
               ('Margen de explotación', '5.018', '+3,2%'),
               ('Deterioros', '480', '+28,8%'),
               ('Beneficio neto', '3.203', '+8,5%'),
               ('BPA 12 meses', '0,88 €', '+6%')],
     'kpi': 'Eficiencia 39,6% (38,6%); ROE 15,4%; ROTE 18,0%. Morosidad 1,78% (2,07% en dic-2025), cobertura 81%, coste del riesgo 24 pb. CET1 12,54%, '
            'tras la recompra. Crédito sano 398.835 M€ (+8,2%; empresas +10,6%, consumo +11,5%); recursos de clientes 771.943 M€ (+7,6%). Gestión '
            'patrimonial 1.091 M€ (+12,1%), seguros de protección 658 M€ (+14,5%), comisiones bancarias 1.023 M€ (−1,1%). BPI aportó 218 M€.',
     'guia': 'Guía 2026 reiterada (Renta 4 y Capitalbolsa): margen de intereses de más de 11.000 M€ (en el 2S necesita más de 5.610 M€, calculado), '
             'ingresos por servicios creciendo a un dígito medio, coste del riesgo por debajo de 25 pb y ROTE por encima del 18%. Dividendo a cuenta en '
             'noviembre del 30-40% del beneficio del semestre (961-1.281 M€) y recompra de 500 M€ en curso.',
     'positivos': ['Crédito sano +8,2%, con empresas +10,6% y consumo +11,5%.',
                   'Gestión patrimonial +12,1% y seguros de protección +14,5%.',
                   'Morosidad en mínimo histórico (1,78%) con cobertura del 81%.'],
     'riesgos': ['Los gastos suben un 4,5% y el margen bruto un 3,7%: la eficiencia empeora al 39,6%.',
                 'Las comisiones bancarias caen un 1,1% (las recurrentes, un 2,4%).',
                 'Los deterioros suben un 28,8% y el margen de intereses debe acelerar en el 2S para cumplir la guía.'],
     'videos': [('GXbYecKtopE', 'CaixaBank resultados 1S 2026: beneficio récord de 3.203 M€ (+8,5%), sobre el consenso | ROTE 18%'),
                ('2UERn_MLK6k', 'CaixaBank 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-30',
     'fuentes': 'CaixaBank, nota de prensa y presentación de resultados del primer semestre 2026 (29-jul-2026, CNMV y caixabank.com); XTB (consenso, '
                '29-jul-2026); Renta 4 (guía, 30-abr-2026) y Capitalbolsa (guía reiterada, 29-jul-2026); stockanalysis.com (precio y múltiplos, '
                '6-oct-2026).',
     'fuentes_corto': 'XTB, Renta 4, Capitalbolsa y stockanalysis.com',
     'elaborado': '13-oct-2026, 19:00'},
]
