# Fichas de AIAcciones España: una por empresa, solo con cifras reales de nuestros vídeos.
# Para agregar una empresa: copia un dict, rellénalo con las cifras del vídeo y corre `python3 espana/build.py`.
# Nada de cifras de ejemplo: si un dato no está en el vídeo o en sus fuentes, no va.

FICHAS = [
    {'id': 'iberdrola',
     'nombre': 'Iberdrola',
     'ticker': 'IBE',
     'sector': 'Eléctricas · redes y renovables',
     'lede': 'Eléctrica con redes reguladas en España, Reino Unido, Estados Unidos y Brasil, y generación renovable. Las redes aportan ya el 54% del '
             'EBITDA. En 2026 vendió su negocio en México a Cox.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 5.816 M€ hasta septiembre (+9,6%), con 953 M€ de plusvalía por la venta de México; beneficio neto ajustado de 5.141 '
                'M€ (+8,8%; +12,7% sin divisas). Iberdrola eleva su guía 2026 a un crecimiento del beneficio ajustado de al menos el 10% (antes, más del '
                '8%).',
     'precio': '21,23 €',
     'precio_fecha': '20-oct-2026',
     'multiplos': [('PER 12 meses', '26,0x'),
                   ('PER forward', '20,0x'),
                   ('EV/EBITDA', '13,8x'),
                   ('Precio / valor contable', '2,21x'),
                   ('Rentab. dividendo', '3,2%'),
                   ('FCF yield', '2,2%'),
                   ('Capitalización', '~137.700 M€')],
     'multiplos_nota': 'Con precio de 21,23 € al cierre del 20-oct-2026, último dato de stockanalysis.com al 21-oct-2026. Con el beneficio neto de 12 '
                       'meses a septiembre publicado por la empresa (6.794 M€), el PER sería ~20,3x (calculado). A cierre de 2023, 2024 y 2025 el PER '
                       'era 16,1x, 15,2x y 20,1x, el EV/EBITDA 10,3x, 10,6x y 12,6x y el precio / valor contable 1,23x, 1,35x y 1,92x. La acción subió '
                       'un 25% en 52 semanas.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ventas', '34.405', '+6,2%'),
               ('EBITDA ajustado', '11.891', '+7,5%'),
               ('EBITDA redes', '6.430', '+14,9%'),
               ('EBITDA generación y clientes', '5.359', '-1,5%'),
               ('Beneficio neto ajustado', '5.141', '+8,8%'),
               ('Beneficio neto reportado', '5.816', '+9,6%'),
               ('Beneficio ajustado 3T (calculado)', '1.576', '+11,0%'),
               ('BPA', '0,834 €', '+5,8%')],
     'kpi': 'Margen EBITDA ajustado 34,6% (34,7% en 9M 2025; calculado). Redes por país (EBITDA, en euros): España +18,3%, Reino Unido +18,0%, EE. UU. '
            '+14,3%, Brasil +9,7%. Inversión de 10.087 M€ (+13%; redes 6.277 M€, +28%); base de activos regulados 56.000 M€ (+14%). Deuda neta ajustada '
            '54.561 M€ (+4.379 M€ vs diciembre). Coste medio de la deuda 4,93% (4,71%); resultado financiero ajustado -1.687 M€ (-1.163 M€). Liquidez de '
            'más de 23.000 M€ (unos 20 meses).',
     'guia': 'Guía 2026 mejorada: beneficio neto ajustado +10% o más (antes, más del 8%), al menos ~6.854 M€ sobre los 6.231 M€ de 2025; los nueve meses '
             'ya suman el 75% (calculado). Objetivo de crecimiento medio anual del 10% en los próximos cinco años; Capital Markets Day en marzo de 2027. '
             'Dividendo a cuenta 0,275 € (+8,7%) con Iberdrola Retribución Flexible (importe máximo 1.835 M€): elección del 12 al 25 de enero y pago en '
             'efectivo el 1-feb-2027 (fechas previstas).',
     'positivos': ['Las redes crecen un 14,9%, con alzas en España, Reino Unido, Estados Unidos y Brasil.',
                   'El beneficio ajustado del tercer trimestre sube un 11% (calculado) y la guía 2026 mejora a +10% o más.',
                   'El dividendo a cuenta sube un 8,7%, hasta 0,275 € por acción.'],
     'riesgos': ['Las divisas restaron 186 M€ al beneficio ajustado.',
                 'La deuda sube con la inversión (+4.379 M€ en 2026) y su coste medio llega al 4,93%.',
                 'Generación y clientes retrocede un 1,5% (España -4,6%).'],
     'videos': [('3lbnU5uzBKE', 'Iberdrola resultados 3T 2026: beneficio +9,6% y eleva la guía a +10% o más | Redes +14,9%'),
                ('LpPRcvMZI-4', 'Iberdrola 3T 2026 en 60 segundos (Short)'),
                ('RGgaT31jOxk', 'Iberdrola resultados 1S 2026: beneficio ajustado +7,8%, 5,5% sobre el consenso | Redes +13%')],
     'proximo': '2027-02-24',
     'proximo_estimado': True,
     'fuentes': 'Iberdrola, resultados de los nueve meses de 2026 (informe, presentación y nota de prensa) y dividendo a cuenta Iberdrola Retribución '
                'Flexible (CNMV, 21-oct-2026); Europa Press (Infobae, The Objective), Estrategias de Inversión y Smartkarma (21-oct-2026); Iberdrola, '
                'resultados 1S26 (22-jul-2026) y 2025 (25-feb-2026); stockanalysis.com (precio y múltiplos, oct-2026).',
     'fuentes_corto': 'Europa Press, Estrategias de Inversión, Smartkarma y stockanalysis.com',
     'elaborado': '21-oct-2026, 11:10'},
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
    {'id': 'repsol',
     'nombre': 'Repsol',
     'ticker': 'REP',
     'sector': 'Petróleo y gas · integrada',
     'lede': 'Compañía energética integrada: exploración y producción de petróleo y gas (Upstream), refino y química (Industrial), estaciones de '
             'servicio, electricidad y gas para clientes (Cliente) y generación renovable. En una petrolera, el resultado ajustado a coste de reposición '
             '(CCS) quita el efecto del precio de los inventarios.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Resultado neto ajustado de 2.711 M€ (+134,7%), impulsado por el refino. El beneficio reportado, 2.201 M€ (603 M€ en 1S 2025), incluye '
                '+823 M€ de efecto inventario y -1.333 M€ de deterioros. En el 2T, 1.838 M€ ajustados: un 12,5% sobre el consenso publicado por Repsol '
                '(1.634 M€, según Benzinga; calculado).',
     'precio': '29,11 €',
     'precio_fecha': '7-oct-2026',
     'multiplos': [('PER 12 meses', '9,3x'),
                   ('PER forward', '5,9x'),
                   ('EV/EBITDA', '4,9x'),
                   ('Precio / valor en libros', '1,15x'),
                   ('Rentab. dividendo', '3,7%'),
                   ('Capitalización', '~31.290 M€')],
     'multiplos_nota': 'Con precio de 29,11 € al 7-oct-2026 (stockanalysis.com); EV/EBITDA y precio / valor en libros a 25-sep-2026 (30,75 €). A cierre '
                       'de 2023, 2024 y 2025 el PER era 5,5x, 8,2x y 9,8x, y el EV/EBITDA 3,3x, 4,6x y 4,7x. La acción subió un 100,9% en 12 meses (a '
                       '25-sep-2026).',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ventas', '33.697', '+21,5%'),
               ('EBITDA CCS', '5.006', '+70,6%'),
               ('Resultado ajustado Industrial', '1.683', '235 en 1S25'),
               ('Resultado ajustado Upstream', '673', '+6,7%'),
               ('Resultado ajustado Cliente', '369', '+5,1%'),
               ('Resultado neto ajustado (CCS)', '2.711', '+134,7%'),
               ('Resultado neto reportado', '2.201', '+265%'),
               ('BPA reportado', '1,96 €', '0,50 € en 1S25')],
     'kpi': 'Margen de refino en España 12,4 $/barril (5,6); 14,0 en el 2T. Producción 548 kbep/d (549); 558 en el 2T. Margen EBITDA CCS 14,9% (10,6%, '
            'calculado). Flujo de caja de las operaciones 2.977 M€ (+15,1%) tras 2.400 M€ invertidos en inventarios; flujo de caja libre 1.302 M€ (636). '
            'Deuda neta 3.667 M€ (-1.133 M€ frente a marzo); apalancamiento 11,3%; deuda neta / EBITDA ~0,4x (calculado). Liquidez 10.117 M€.',
     'guia': 'Producción 2026 prevista de 560.000-570.000 bep/d (más de 580.000 a inicios de julio). Dividendo en efectivo 2026 de 1,051 €/acción (+8%) '
             'y 0,53 € en enero de 2027. Recompras de hasta 850 M€ en 2026 y una tercera prevista en octubre, para repartir el 30-40% del flujo de caja '
             'de las operaciones.',
     'positivos': ['El margen de refino se duplicó y el negocio Industrial multiplicó por siete su resultado.',
                   'El 2T superó al consenso; el flujo de caja libre se duplicó y la deuda neta bajó.',
                   'Más retribución: dividendo +8% y recompras de hasta 850 M€.'],
     'riesgos': ['El beneficio depende mucho del precio del crudo y del margen de refino, hoy altos por las tensiones geopolíticas.',
                 'Deterioros y provisiones de 1.333 M€, sobre todo en Química y en renovables en Chile.',
                 'La producción no crece frente a 2025, Upstream quedó por debajo de lo esperado (Bankinter) y hay exposición a Venezuela.'],
     'videos': [('LDjyCZImFpQ', 'Repsol resultados 1S 2026: beneficio ajustado +134,7% por el refino; el 2T supera al consenso'),
                ('OMP1V-cPw9s', 'Repsol 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-29',
     'fuentes': 'Repsol, informe de resultados del segundo trimestre 2026 y nota de prensa (CNMV, 23-jul-2026); Benzinga (consenso de Repsol, '
                '23-jul-2026); Jefferies / Bolsamania y Bankinter Análisis / Capitalbolsa (23-jul-2026); stockanalysis.com (precio y múltiplos, 25-sep y '
                '7-oct-2026).',
     'fuentes_corto': 'Benzinga, Jefferies, Bankinter Análisis y stockanalysis.com',
     'elaborado': '15-oct-2026, 13:30'},
    {'id': 'telefonica',
     'nombre': 'Telefónica',
     'ticker': 'TEF',
     'sector': 'Telecomunicaciones',
     'lede': 'Operadora de telecomunicaciones con cuatro mercados principales: España, Brasil, Alemania y Reino Unido (Virgin Media O2, al 50%). Está '
             'saliendo de Hispanoamérica: Colombia y Chile se vendieron en el 1T 2026 y la venta de México está firmada y pendiente de autorizaciones.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'EBITDA ajustado de 5.768 M€ (+3,8%; +2,3% a tipos constantes), con Brasil (+10% constante) y España (+2,1%) al alza y Alemania a la '
                'baja. Resultado neto atribuido de −338 M€ (pérdida un 75% menor que en el 1S 2025) por el impacto de 1.001 M€ de la venta de Chile. En '
                'el 2T, ingresos y EBITDA ligeramente por encima del consenso recopilado por Telefónica; el beneficio, muy por debajo por una provisión '
                'de 265 M€ en Alemania.',
     'precio': '3,252 €',
     'precio_fecha': '13-oct-2026',
     'multiplos': [('PER 12 meses', 'n/d (pérdidas)'),
                   ('PER forward', '8,9x'),
                   ('EV/EBITDA', '7,4x'),
                   ('Rentab. dividendo 12 m', '9,2%'),
                   ('FCF yield', '19,1%'),
                   ('Capitalización', '~18.300 M€')],
     'multiplos_nota': 'Precio, PER forward, rentabilidad por dividendo (0,30 € en 12 meses) y capitalización a 13-oct-2026; EV/EBITDA y FCF yield a '
                       '25-sep-2026 (stockanalysis.com). Con el dividendo de 2026 (0,15 €) la rentabilidad sería del 4,6% (calculado). A cierre de 2023, '
                       '2024 y 2025 el EV/EBITDA era 8,6x, 6,6x y 8,7x, y el precio / valor contable 0,74x, 0,98x y 1,11x. Sin PER en esos años por '
                       'pérdidas.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025 (operaciones continuadas salvo el resultado total)',
     'tabla': [('Ingresos', '16.392', '+1,7%'),
               ('EBITDA ajustado', '5.768', '+3,8%'),
               ('EBITDA ajustado España', '2.301', '+2,1%'),
               ('EBITDA ajustado Brasil', '2.215', '+15,1%'),
               ('EBITDAaL-CapEx', '2.654', '+4,0%'),
               ('Beneficio neto ajustado (continuadas)', '954', ''),
               ('Resultado neto atribuido (total)', '−338', '−75% de pérdida'),
               ('BPA ajustado continuadas (calculado)', '~0,17 €', '')],
     'kpi': 'Margen EBITDA ajustado 35,2% (34,5% en 1S 2025, calculado). Alemania: ingresos −11% y EBITDA ajustado −7,2% en el 2T por la migración de '
            'clientes de 1&1. Virgin Media O2 (2T): ingresos de servicio −3,9% y EBITDA ajustado −2,9%. CapEx 1.908 M€ (11,6% de los ingresos). Flujo de '
            'caja libre 944 M€. Deuda financiera neta 25.278 M€ (−8,4% a/a; −1.546 M€ desde diciembre), apalancamiento 2,68x EBITDAaL.',
     'guia': 'Guía 2026 (tipos constantes): EBITDAaL-CapEx más de +3% (antes, más de +2%); ingresos y EBITDA ajustado +1,5% a +2,5% (ingresos hacia la '
             'parte baja, según la conferencia); CapEx / ingresos ~12%; flujo de caja libre ~3.000 M€; apalancamiento de 2,5x en 2028. Dividendo 2026 de '
             '0,15 € en efectivo, pagadero en junio de 2027 (0,30 € en el ejercicio 2025).',
     'positivos': ['Brasil (EBITDA +10% constante) y España (bajas de clientes en mínimos) tiran del grupo.',
                   'La deuda neta baja un 8,4% y el apalancamiento cae a 2,68x.',
                   'Sube la previsión de caja operativa para 2026 a más de +3%.'],
     'riesgos': ['Alemania: ingresos −11% en el 2T y unos 155 M€ más de reestructuración previstos en el segundo semestre.',
                 'Reino Unido: competencia intensa y deuda de Virgin Media O2 de unas 5,9 veces el EBITDA.',
                 'La salida de Hispanoamérica resta 812 M€ en el semestre y la venta de México sigue pendiente.'],
     'videos': [('u63YAPRgUtE', 'Telefónica resultados 1S 2026: EBITDA ajustado +3,8% y sube la guía de caja | Brasil +10%'),
                ('0Acp3sPlQZE', 'Telefónica 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-11-12',
     'fuentes': 'Telefónica, nota de resultados del primer semestre 2026 (29-jul-2026, CNMV y telefonica.com) y del 1T 2026; Renta 4 Banco (resultados y '
                'conferencia, 29-jul-2026); Benzinga España (consenso de Telefónica y Alemania, 23 y 30-jul-2026); Investing.com (conferencia, '
                '29-jul-2026); El Conciso (29-jul-2026); Virgin Media O2 (resultados 2T26); stockanalysis.com (precio y múltiplos, 25-sep y '
                '13-oct-2026).',
     'fuentes_corto': 'Renta 4 Banco, Benzinga, Investing.com, El Conciso, Virgin Media O2 y stockanalysis.com',
     'elaborado': '15-oct-2026, 13:30'},
    {'id': 'endesa',
     'nombre': 'Endesa',
     'ticker': 'ELE',
     'sector': 'Eléctricas · redes, generación y comercialización',
     'lede': 'Eléctrica integrada, controlada por Enel, con distribución regulada, generación (renovable, convencional y extrapeninsular) y '
             'comercialización de electricidad y gas en España y Portugal. Las actividades reguladas aportan cerca de la mitad del EBITDA.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 1.470 M€ (+41,2%), un 6,8% por encima del consenso (1.376 M€, Bankinter Análisis; diferencia calculada). Beneficio '
                'ordinario neto 1.480 M€ (+42,2%). Unos 200 M€ del EBITDA fueron no recurrentes.',
     'precio': '42,18 €',
     'precio_fecha': '25-sep-2026',
     'multiplos': [('PER 12 meses', '16,6x'),
                   ('PER forward', '17,8x'),
                   ('EV/EBITDA', '9,3x'),
                   ('Precio / valor contable', '4,7x'),
                   ('Rentab. dividendo', '3,8%'),
                   ('FCF yield', '4,7%'),
                   ('Capitalización', '~43.170 M€')],
     'multiplos_nota': 'Con precio de 42,18 € al 25-sep-2026 (stockanalysis.com). A cierre de 2023, 2024 y 2025 el PER era 26,3x, 11,7x y 14,5x, el '
                       'EV/EBITDA 10,5x, 6,9x y 8,2x y el precio / valor contable 2,7x, 2,4x y 3,3x. La acción subió un 59% en 52 semanas.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ingresos', '10.995', '+1,1%'),
               ('EBITDA', '3.240', '+19,5%'),
               ('EBITDA redes (distribución)', '1.200', '+24%'),
               ('EBITDA generación (redondeado)', '~1.200', ''),
               ('EBITDA clientes (redondeado)', '~800', '+26%'),
               ('EBIT', '2.094', '+31,4%'),
               ('Beneficio neto', '1.470', '+41,2%'),
               ('Beneficio ordinario neto', '1.480', '+42,2%'),
               ('BPA', '1,44 €', '+46%')],
     'kpi': 'Margen EBITDA 29,5% (24,9% en 1S 2025; calculado). Producción 32.708 GWh (+8,5%); ventas de electricidad 35.474 GWh (-2,3%) y de gas 25.591 '
            'GWh (-17,6%); energía distribuida 72.555 GWh (+4,2%). Cash flow operativo 2.272 M€ (-3,6%); inversión bruta 1.062 M€ (+13,6%; redes 600 M€, '
            '+38%). Deuda financiera neta 10.305 M€ (10.110 M€ en diciembre), 1,6x EBITDA. Coste medio de la deuda 3,2%.',
     'guia': 'Guía 2026 al alza: beneficio ordinario neto de más de 2.400 M€ (antes 2.300-2.400 M€); el semestre ya suma el 62% (calculado). Objetivo de '
             'EBITDA de 5.800-6.100 M€ fijado en febrero. Política de dividendo 2026-2028: al menos el 70% del beneficio ordinario neto, lo que supone '
             'más de 1.680 M€ para 2026 (calculado). Recompra de 2.000 M€ ejecutada en más del 50%. Nuevo plan estratégico a principios de 2027.',
     'positivos': ['Las redes crecen un 24% y la inversión en ellas, un 38%.',
                   'El beneficio superó al consenso y la guía anual sube.',
                   'La deuda apenas se mueve pese a la recompra y el apalancamiento baja a 1,6x.'],
     'riesgos': ['Unos 200 M€ del EBITDA del semestre no se repetirán.',
                 'Las ventas de electricidad y gas caen, y la empresa prevé un margen libre de 44-55 €/MWh para el año, por debajo de los 56 del '
                 'semestre.',
                 'El PER y el EV/EBITDA están por encima de los de 2024 y 2025.'],
     'videos': [('hinLi7xl-R8', 'Endesa resultados 1S 2026: beneficio +41%, 6,8% sobre el consenso | Guía 2026 al alza'),
                ('tcyjnI02z7Q', 'Endesa 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-28',
     'proximo_estimado': True,
     'fuentes': 'Endesa, nota de prensa de resultados del primer semestre 2026 (CNMV y endesa.com, 29-jul-2026); Bankinter Análisis (consenso, '
                '29-jul-2026); Investing.com (presentación y conferencia de resultados, 29-jul-2026); Endesa (resultados 1T26, 6-may-2026); El Español y '
                'Bolsamania (plan y política de dividendo, 24-feb-2026); stockanalysis.com (precio y múltiplos, 25-sep-2026).',
     'fuentes_corto': 'Bankinter Análisis, Investing.com, El Español, Bolsamania y stockanalysis.com',
     'elaborado': '15-oct-2026, 13:30'},
    {'id': 'enagas',
     'nombre': 'Enagás',
     'ticker': 'ENG',
     'sector': 'Gas · red de transporte regulada',
     'lede': 'Gestor técnico del sistema gasista español y dueño de la red troncal de gasoductos, almacenamientos y plantas de regasificación. Tiene '
             'participaciones internacionales (TAP, Teréga) y promueve la red troncal de hidrógeno y el corredor H2Med.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio recurrente de 195,8 M€ hasta septiembre (-5,4%); el del tercer trimestre, 77,2 M€, igual que en el 3T 2025 (calculado). El '
                'beneficio neto, 204,1 M€ (-22,3%), compara con unos 9M 2025 que incluían 55,8 M€ de plusvalías por ventas de activos.',
     'precio': '16,81 €',
     'precio_fecha': '16-oct-2026',
     'multiplos': [('PER 12 meses', '15,2x'),
                   ('PER forward', '16,7x'),
                   ('EV/EBITDA', '11,1x'),
                   ('Precio / valor contable', '1,89x'),
                   ('Rentab. dividendo', '5,95%'),
                   ('FCF yield', '0,7%'),
                   ('Capitalización', '~4.380 M€')],
     'multiplos_nota': 'Con precio de 16,81 € al cierre del 16-oct-2026, último dato de stockanalysis.com al 20-oct-2026 (el PER usa el beneficio de 12 '
                       'meses hasta junio; con el de 12 meses a septiembre sería ~15,6x, calculado). A cierre de 2023 y 2025 el PER era 11,6x y 10,1x '
                       '(en 2024 hubo pérdidas por Tallgrass y GSP), el EV/EBITDA 14,1x, 9,8x y 11,5x en 2023, 2024 y 2025, y el precio / valor contable '
                       '1,33x, 1,29x y 1,48x.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '696,7', '-2,0%'),
               ('EBITDA', '491,5', '-2,9%'),
               ('EBIT', '263,9', '-4,1%'),
               ('Beneficio recurrente', '195,8', '-5,4%'),
               ('Beneficio neto', '204,1', '-22,3%'),
               ('Beneficio recurrente 3T (calculado)', '77,2', '+0,1%'),
               ('BPA (calculado)', '~0,78 €', '')],
     'kpi': 'Margen EBITDA 70,5% (71,1% en 9M 2025; calculado). Ingresos regulados 663 M€ (-4,3%), con -45,1 M€ por el marco 2021-2026; participadas '
            '145,8 M€ de EBITDA (+28,1 M€, por TAP y Teréga). FFO 439 M€ (-5,2%), con 127,1 M€ de dividendos de filiales. Deuda neta 2.979 M€, 504 M€ '
            'más que en diciembre, en parte por la compra del 31,5% de Teréga (573 M€); deuda neta / EBITDA ~4,5x (calculado). Coste medio de la deuda '
            '2,1%; más del 80% a tipo fijo; vida media 3,9 años.',
     'guia': 'Objetivos 2026 reiterados: beneficio recurrente ~235 M€ y EBITDA ~620 M€ (los nueve meses ya suman el 83% y el 79%, calculado); los '
             'ingresos regulados de copex se reconocen sobre todo en el cuarto trimestre. Dividendo de 1 € por acción. Acuerdo con Osaka Gas para '
             'comprar otro 20% de Saggas por 31 M€. Marco 2027-2032: la CNMC aprobó el 18-sep-2026 una tasa de retribución financiera del 6,46% para '
             'transporte y regasificación.',
     'positivos': ['El beneficio recurrente del tercer trimestre se mantuvo y los objetivos de 2026 siguen en camino.',
                   'Las participadas aportan 28,1 M€ más de EBITDA, con TAP y Teréga.',
                   'El coste medio de la deuda bajó al 2,1%.'],
     'riesgos': ['Los ingresos regulados siguen bajando y el impacto del marco 2027-2032 no está cuantificado en las fuentes.',
                 'La deuda neta subió 504 M€, hasta ~4,5 veces el EBITDA (calculado).',
                 'El dividendo absorbe cerca del 90% del beneficio y el flujo libre es muy bajo.'],
     'videos': [('vn94fMBvfO8', 'Enagás resultados 3T 2026: beneficio recurrente -5,4%, el del 3T estable | Deuda 2.979 M€ con Teréga'),
                ('ynVGjV7uLis', 'Enagás 3T 2026 en 60 segundos (Short)'),
                ('4D2ENp-JfSE', 'Enagás resultados 1S 2026: beneficio recurrente -8,6%, algo mejor que el consenso | Deuda -170 M€'),
                ('_jFDsjwBsQw', 'Enagás 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-17',
     'proximo_estimado': True,
     'fuentes': 'Enagás, resultados del tercer trimestre 2026 (CNMV, 20-oct-2026), recogidos por Bolsamanía, Europa Press (Infobae, El Español), '
                'Estrategias de Inversión y Smartkarma (20-oct-2026); Enagás, resultados 1S26 (22-jul-2026) y 2025 (feb-2026); CNMC (circulares '
                '2027-2032, 18-sep-2026); stockanalysis.com (precio y múltiplos, oct-2026).',
     'fuentes_corto': 'Bolsamanía, Europa Press, Estrategias de Inversión, Smartkarma, CNMC y stockanalysis.com',
     'elaborado': '20-oct-2026, 10:15'},
    {'id': 'ferrovial',
     'nombre': 'Ferrovial',
     'ticker': 'FER',
     'sector': 'Infraestructuras · autopistas, construcción y aeropuertos',
     'lede': 'Promotor y gestor de infraestructuras de transporte con sede en Países Bajos y cotización en Madrid y en el Nasdaq. Su valor se '
             'concentra en autopistas de peaje (407 ETR en Canadá y Managed Lanes en Estados Unidos); también construye (Budimex, Webber) y '
             'participa en la nueva Terminal Uno del JFK.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'EBITDA ajustado de 746 M€ (+13,9%; +21,6% comparable), empujado por las tarifas de las autopistas de Norteamérica. El '
                'beneficio neto atribuible, 258 M€ (-52%), compara con un 1S 2025 que incluía 275 M€ de desinversiones (AGS y servicios '
                'mineros en Chile).',
     'precio': '44,21 €',
     'precio_fecha': '16-oct-2026',
     'multiplos': [('PER 12 meses', '52,4x'),
                   ('PER forward', '40,9x'),
                   ('EV/EBITDA', '20,4x'),
                   ('Precio / valor contable', '4,21x'),
                   ('Rentab. dividendo', '2,52%'),
                   ('FCF yield', '6,0%'),
                   ('Capitalización', '~31.880 M€')],
     'multiplos_nota': 'Con precio de 44,21 € al 16-oct-2026 (stockanalysis.com). A cierre de 2023, 2024 y 2025 el PER era 71,7x, 9,2x '
                       '(plusvalías de Heathrow e IRB) y 44,8x, el EV/EBITDA 34,2x, 29,8x y 33,7x, el precio / valor contable 4,10x, 3,68x y '
                       '5,19x, y la rentabilidad por dividendo 2,23%, 1,97% y 2,01%.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ingresos', '4.701', '+5,2%'),
               ('EBITDA ajustado', '746', '+13,9%'),
               ('EBIT ajustado', '491', '+13,9%'),
               ('Beneficio neto atribuible', '258', '-52,2%'),
               ('Beneficio neto 2T', '189', '+8,6%'),
               ('Dividendos de proyectos', '378', '+17,0%'),
               ('BPA (calculado)', '~0,36 €', '')],
     'kpi': 'Margen EBITDA 15,9% (14,7% en 1S 2025; calculado). Autopistas: ingreso medio por viaje en la 407 ETR +17,7% con tráfico +1,8%; '
            'ingreso por transacción +18,9% en NTE, +11,7% en LBJ y +17,3% en NTE 35W. Construcción: margen EBIT ajustado 3,5% (3,4%), flujo '
            'operativo 329 M€ y cartera récord de 18.046 M€. Caja neta sin proyectos de infraestructura 1.307 M€ (1.341 M€ en diciembre); '
            'liquidez 4.747 M€; deuda neta consolidada 6.283 M€.',
     'guia': 'Sin guía anual de beneficios: el plan Horizon 24 termina en 2026 y la empresa prepara uno nuevo, sin fecha. La 407 ETR aprobó un '
             'dividendo de 550 M CAD para el 3T (250 M en el 3T25). Objetivo de margen EBIT ajustado de Construcción del 3,5%. Dividendo '
             'flexible de 400 M€ y recompra de hasta 800 M€, ampliada hasta el 3-mar-2027 (357,9 M€ ejecutados a 11-sep-2026). JFK Terminal '
             'Uno: la ocupación de la primera fase pasa a marzo de 2027.',
     'positivos': ['El EBITDA comparable creció un 21,6% gracias a las tarifas de las autopistas de Norteamérica.',
                   'Los dividendos de proyectos subieron a 378 M€ y la 407 ETR aprobó otro de 550 M CAD.',
                   'Construcción mejora el margen, genera caja y tiene una cartera récord.'],
     'riesgos': ['La nueva Terminal Uno del JFK no alcanzó la ocupación prevista en junio; el objetivo pasa a marzo de 2027.',
                 'Tráfico débil en la I-77, la NTE y la 407 ETR en el 2T: el crecimiento depende de las tarifas.',
                 'No hay guía anual y la caja neta bajó ligeramente, por debajo de lo que esperaba Renta 4.'],
     'videos': [('_enk_ZzJWhE', 'Ferrovial resultados 1S 2026: EBITDA comparable +21,6%, beneficio -52% por las plusvalías de 2025'),
                ('jgro0LsOOGs', 'Ferrovial 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-27',
     'proximo_estimado': True,
     'fuentes': 'Ferrovial, resultados del primer semestre 2026 (6-K y CNMV, 28-jul-2026); Capitalbolsa (análisis de Renta 4, 29-jul-2026); '
                'Estrategias de Inversión, El Español y Bolsamanía/Europa Press (28 y 29-jul-2026); MarketBeat e Investing.com (conferencia, '
                '29-jul-2026); Europa Press/Forbes (recompra, 14-sep-2026); stockanalysis.com (precio y múltiplos, 16-oct-2026).',
     'fuentes_corto': 'Capitalbolsa, Estrategias de Inversión, El Español, MarketBeat y stockanalysis.com',
     'elaborado': '16-oct-2026, 16:45'},
    {'id': 'aena',
     'nombre': 'Aena',
     'ticker': 'AENA',
     'sector': 'Aeropuertos · tarifas reguladas y negocio comercial',
     'lede': 'Gestiona 46 aeropuertos y dos helipuertos en España, además de Londres-Luton, Leeds Bradford (vía Augusta) y 17 aeropuertos en '
             'Brasil. Sus tarifas aeroportuarias en España las fija el DORA; el negocio comercial (tiendas, restauración, aparcamientos, salas '
             'VIP) y el inmobiliario completan los ingresos.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 1.002 M€ (+12,1%), por primera vez por encima de 1.000 M€ en un semestre, aunque algo por debajo del '
                'consenso de Bloomberg que recoge XTB (1.019,8 M€; diferencia -1,7%, calculada). La deuda financiera neta sube a 6.724 M€ tras '
                'el dividendo y la compra de Augusta.',
     'precio': '25,22 €',
     'precio_fecha': '14-oct-2026',
     'multiplos': [('PER 12 meses', '17,0x'),
                   ('PER forward', '15,8x'),
                   ('EV/EBITDA', '11,6x'),
                   ('Precio / valor contable', '4,28x'),
                   ('Rentab. dividendo', '4,32%'),
                   ('FCF yield', '5,75%'),
                   ('Capitalización', '~37.830 M€')],
     'multiplos_nota': 'Con precio de 25,22 € al cierre del 14-oct-2026 (stockanalysis.com; 1.500 M de acciones tras el desdoblamiento 10x1 de '
                       '2025). A cierre de 2023, 2024 y 2025 el PER era 15,1x, 15,3x y 16,7x, el EV/EBITDA 11,2x, 10,4x y 11,2x, el precio / '
                       'valor contable 3,26x, 3,49x y 3,90x, y la rentabilidad por dividendo 5,19%, 5,31% y 4,74%.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ingresos', '3.299,6', '+10,1%'),
               ('Ingresos aeronáuticos', '1.702,1', '+8,1% (calculado)'),
               ('Ingresos comerciales', '991,0', '+6,7% (calculado)'),
               ('EBITDA', '1.798,9', '+6,3%'),
               ('Beneficio neto', '1.002,0', '+12,1%'),
               ('Beneficio neto 2T (calculado)', '672,6', '+13,5%'),
               ('BPA (calculado)', '~0,67 €', '+12,1%')],
     'kpi': 'Margen EBITDA 54,5% (56,5% en 1S 2025). Pasajeros: 156,2 M en España (+3,7%), 8,8 M en Luton (+5,1%) y ~22,9 M en Brasil '
            '(calculado); 190 M en el grupo (+3,9%). Ingreso comercial por pasajero en España ~6,34 € (+2,8%, calculado); salas VIP +31,7%, '
            'aparcamientos +9%. Flujo de explotación 1.598,5 M€ (+8,0%, calculado). Deuda financiera neta 6.724 M€ (+1.215 M€ vs diciembre), '
            '1,73x EBITDA, tras 1.646,4 M€ de dividendos pagados y 340 M€ por Augusta.',
     'guia': 'Tráfico en España 2026: alrededor de +3% (desde ~1,3% a inicio de año, según XTB), con poca visibilidad en el segundo semestre. '
             'Política de dividendo del 80% del beneficio; 1,09 € por acción con cargo a 2025. 2026 es el último año del DORA II (tarifa de '
             '11,02 € por pasajero, +6,44%). El DORA III, aprobado el 15-sep-2026, fija subidas medias del 0,33% anual en 2027-2031 (Aena '
             'pedía 3,82%) con unas inversiones cercanas a 13.000 M€.',
     'positivos': ['El beneficio supera por primera vez los 1.000 M€ en un semestre y la previsión de tráfico sube a ~3%.',
                   'El negocio comercial sigue creciendo: salas VIP +31,7% y aparcamientos +9%.',
                   'Crecimiento exterior con Augusta (Leeds Bradford y Newcastle) y la concesión de Río de Janeiro-Galeão.'],
     'riesgos': ['El DORA III deja las tarifas casi congeladas hasta 2031 con un gran plan de inversión.',
                 'Los costes (+13,5%) crecen más que los ingresos y los resultados quedaron algo por debajo del consenso.',
                 'La deuda neta sube 1.215 M€ y la visibilidad del tráfico en el segundo semestre es baja.'],
     'videos': [('QCBLXtjeo3o', 'Aena resultados 1S 2026: beneficio 1.002 M€ (+12,1%), algo por debajo del consenso | Deuda 6.724 M€'),
                ('SuVwEzW7h9I', 'Aena 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-28',
     'proximo_estimado': True,
     'fuentes': 'Aena, nota de prensa de resultados del primer semestre 2026 (CNMV y aena.es, 29-jul-2026), notas del 1T26, 1S25 y 1T25; XTB '
                '(consenso Bloomberg, 29-jul-2026); Investing.com (detalle por negocio, 29-jul-2026); EFE (tarifa 2026, 20-nov-2025); '
                'Hosteltur (DORA III, 15-sep-2026); stockanalysis.com (precio y múltiplos, 14-oct-2026).',
     'fuentes_corto': 'XTB, Investing.com, Hosteltur, EFE y stockanalysis.com',
     'elaborado': '16-oct-2026, 16:55'},
    {'id': 'puig',
     'nombre': 'Puig',
     'ticker': 'PUIG',
     'sector': 'Consumo · belleza premium (perfumes, maquillaje y cuidado de la piel)',
     'lede': 'Grupo barcelonés de belleza premium que cotiza en la Bolsa de Madrid desde mayo de 2024. Tres de cada cuatro euros vienen de perfumes y '
             'moda (Rabanne, Carolina Herrera, Jean Paul Gaultier); el resto, de maquillaje (Charlotte Tilbury) y cuidado de la piel (Uriage, y ISDIN al '
             '50%).',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026 (actualización de ventas)',
     'titular': 'Ventas de 1.391 M€ en el tercer trimestre (+7,2%; +5,6% comparable, el mayor ritmo del año), con Maquillaje +16,1% y Cuidado de la piel '
                '-0,8% comparable. En nueve meses, 3.745 M€ (+4,1%; +4,8% comparable). En el 3T Puig solo publica ventas: beneficio, márgenes y deuda '
                'son los del 1S 2026.',
     'precio': '19,59 €',
     'precio_fecha': '21-oct-2026',
     'multiplos': [('PER 12 meses', '18,7x'),
                   ('PER forward', '16,8x'),
                   ('EV/EBITDA', '11,3x'),
                   ('Precio / valor contable', '2,69x'),
                   ('Rentab. dividendo', '2,15%'),
                   ('FCF yield', '5,4%'),
                   ('Capitalización', '~11.035 M€')],
     'multiplos_nota': 'Precio: cierre del 21-oct-2026 (Bolsamanía), antes de la publicación de las ventas. Múltiplos de stockanalysis.com con 19,57 € '
                       '(16-oct-2026), que con 19,59 € no cambian (calculado); se basan en el beneficio y el EBITDA de 12 meses hasta junio, porque el '
                       '3T no trae beneficio. Puig cotiza desde mayo de 2024, así que solo hay dos cierres de año para comparar: a cierre de 2024 y 2025 '
                       'el PER era 18,9x y 14,1x, el EV/EBITDA 13,5x y 10,3x, el precio / valor contable 2,84x y 2,14x, y la rentabilidad por dividendo '
                       '2,11% y 2,83%.',
     'tabla_titulo': 'Millones de euros · ventas 3T y 9M 2026 (variación comparable a/a) y EBITDA ajustado del 1S 2026 (variación a/a)',
     'tabla': [('Ventas 3T', '1.390,8', '+5,6%'),
               ('Ventas 9M', '3.744,5', '+4,8%'),
               ('Fragancias y Moda 9M', '2.702,0', '+3,8%'),
               ('Maquillaje 9M', '628,5', '+12,0%'),
               ('Cuidado de la piel 9M', '414,1', '+1,3%'),
               ('Asia Pacífico 9M', '430,0', '+17,9%'),
               ('EBITDA ajustado 1S 2026', '459,6', '+3,2%')],
     'kpi': 'Ventas reportadas: 3T +7,2% (divisas +1,7%); 9M +4,1% (divisas -0,7%, sobre todo el dólar). Comparable por trimestre: 1T +4,7%, 2T +4,1%, '
            '3T +5,6%. 3T por negocio (comparable): Fragancias y Moda +3,9%, Maquillaje +16,1%, Cuidado de la piel -0,8%; por región: EMEA +3,8%, '
            'América +6,2%, Asia Pacífico +12,9%. 9M por región: EMEA 1.948,7 M€ (+3,0%), América 1.365,9 M€ (+3,8%), Asia Pacífico 430,0 M€ (+17,9%). '
            'Último dato de rentabilidad y deuda (1S 2026): margen EBITDA ajustado 19,5% (19,4%); beneficio neto ajustado 260,3 M€ (+5,2%); deuda neta '
            '1.589 M€ a 30-jun, 1,5x el EBITDA ajustado.',
     'guia': 'Guía 2026 reiterada el 21-oct-2026: crecer por encima del mercado de belleza premium en términos comparables y mantener estable el margen '
             'EBITDA ajustado (20,7% en 2025); deuda neta / EBITDA ajustado de 2,0x como máximo y payout de ~40% del beneficio neto reportado. En la '
             'conferencia: 4T de fragancias similar a los nueve meses, maquillaje frente a un +26,5% del 4T 2025 y cuidado de la piel plano. ISDIN: '
             'compra del 50% restante por 900 M€ al cierre (previsto a finales del 1T27) y 300 M€ aplazados al 1T29. Capital Markets Day el 28-oct-2026.',
     'positivos': ['El crecimiento comparable se acelera al 5,6% en el 3T, el mayor del año, por encima del +5,0% que esperaba Jefferies (Reuters).',
                   'Maquillaje crece un 16,1% comparable en el 3T y todas las regiones suben; América acelera al +6,2%.',
                   'El dólar suma en el 3T (+1,7%) tras restar en el semestre, y Puig reitera su guía 2026.'],
     'riesgos': ['Cuidado de la piel cae un 0,8% comparable en el 3T y Puig espera un 4T plano por la debilidad del lujo en Norteamérica.',
                 'Maquillaje afronta en el 4T una base exigente (+26,5% en el 4T 2025) y Asia Pacífico se modera (+12,9% en el 3T frente a +20,9% en el '
                 '1S).',
                 'Sin datos de márgenes ni deuda hasta los resultados anuales; la compra de ISDIN supondrá un pago de 900 M€ al cierre (deuda neta de '
                 '1.589 M€ en junio).'],
     'videos': [('9Mf16YKG9Mw', 'Puig ventas 3T 2026: +5,6% comparable, 1.391 M€ | Maquillaje +16,1%, cuidado de la piel -0,8%'),
                ('2wQMF4z2kTM', 'Puig 3T 2026 en 60 segundos (Short)'),
                ('AwK5Blg88WA', 'Puig resultados 1S 2026: ventas +4,4% comparable y beneficio ajustado +5,2% | Deuda neta 1.589 M€'),
                ('hq9OYbh6hSc', 'Puig 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-17',
     'proximo_estimado': True,
     'fuentes': 'Puig, nota de prensa y presentación de la actualización de ventas del 3T 2026 (CNMV y puig.com, 21-oct-2026) y resultados del primer '
                'semestre 2026 (30-jul-2026); Reuters vía FashionNetwork (21-oct-2026); Investing.com (conferencia, 21-oct-2026); Estrategias de '
                'Inversión y Bolsamanía/Europa Press (21-oct-2026); Business Wire (Estée Lauder, 21-may-2026); stockanalysis.com (múltiplos, '
                '16-oct-2026).',
     'fuentes_corto': 'Reuters, Investing.com, Estrategias de Inversión, Bolsamanía y stockanalysis.com',
     'elaborado': '22-oct-2026, 00:18'},
    {'id': 'fluidra',
     'nombre': 'Fluidra',
     'ticker': 'FDR',
     'sector': 'Industrial · equipos para piscina y wellness',
     'lede': 'Fabricante y distribuidor de equipos para piscinas residenciales y comerciales y para bienestar (bombas, filtros, robots limpiafondos, '
             'tratamiento del agua y automatización). Norteamérica es su mayor mercado (41% de las ventas del 1S 2026) y el negocio es estacional: el '
             'primer semestre, y sobre todo el segundo trimestre, es la temporada alta.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Ventas de 1.258 M€ (+2,6%; +5% a tipo de cambio constante) y EBITDA ajustado de 321 M€ (+2,4%; +6% a tipo constante), con un margen '
                'estable del 25,5%. El beneficio neto contable bajó un 7,1%, a 126 M€, por 35 M€ de reestructuración y otros gastos; el ajustado subió '
                'un 2,0%, a 175 M€.',
     'precio': '17,50 €',
     'precio_fecha': '2-oct-2026',
     'multiplos': [('PER 12 meses', '20,0x'),
                   ('PER forward', '12,4x'),
                   ('EV/EBITDA', '11,3x'),
                   ('Precio / valor contable', '2,10x'),
                   ('Rentab. dividendo', '3,71%'),
                   ('FCF yield', '10,1%'),
                   ('Capitalización', '~3.320 M€')],
     'multiplos_nota': 'Con precio de 17,50 € al 2-oct-2026 (stockanalysis.com; EV/EBITDA, P/VC y FCF yield al 11-sep-2026). A cierre de 2023, 2024 y '
                       '2025 el PER era 31,4x, 32,3x y 25,0x, el EV/EBITDA 14,7x, 15,8x y 13,7x, el precio / valor contable 2,27x, 2,69x y 2,75x, y la '
                       'rentabilidad por dividendo 3,09%, 2,64% y 2,84%.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ventas', '1.258', '+2,6%'),
               ('EBITDA ajustado', '321', '+2,4%'),
               ('Beneficio neto ajustado', '175', '+2,0%'),
               ('Beneficio neto', '126', '-7,1%'),
               ('EBITDA ajustado 2T (calculado)', '197', '+7,7%'),
               ('Flujo de caja libre', '16', '-74 en 1S25'),
               ('BPA ajustado', '0,91 €', '')],
     'kpi': 'Margen EBITDA ajustado 25,5% (25,6% en 1S 2025); 28,4% en el 2T (27,6%; calculado). Margen bruto estable, 56,5%. Ventas por región: '
            'Norteamérica 518 M€ (-1,6% en euros; +4% a tipo constante), Sur de Europa 395 M€ (+8,1%), Resto de Europa 179 M€ (+3,1%), Resto del mundo '
            '167 M€ (+3,4%). Flujo de caja libre +16 M€ (-74 M€ en 1S 2025); circulante / ventas 22,5% (-2,3 pp). Deuda neta 1.101 M€ (-1,4%), 2,2x el '
            'EBITDA ajustado (2,3x).',
     'guia': 'Objetivos 2026 mantenidos, a tipo de cambio constante: ventas +3% a +7% (confía en el punto medio), margen EBITDA ajustado 23,3%-24,3% '
             '(ahora en la parte baja o media) y BPA ajustado +4% a +13%. Reestructuración de 50-55 M€ en el año. Dividendo de 0,65 € con cargo a 2025 '
             '(0,32 € en julio y 0,33 € en diciembre) y recompra de 40 M€ lanzada el 30-jul-2026. Compras de Hydrapro (Francia) y Riaan Pool Group '
             '(Sudáfrica) pendientes de cierre.',
     'positivos': ['Las ventas crecen en todas las regiones a tipo constante, con volumen y precio, y el EBITDA superó al consenso (Citi).',
                   'Flujo de caja libre positivo en el semestre, menos circulante y menos deuda.',
                   'Guía 2026 mantenida, plan de ahorro de costes en marcha y recompra de 40 M€.'],
     'riesgos': ['La caída del dólar resta crecimiento: las ventas de Norteamérica bajaron un 1,6% en euros.',
                 'Los costes de reestructuración (50-55 M€ en 2026) pesan sobre el beneficio neto contable.',
                 'Obra nueva de piscinas débil, piscina comercial -10% en el 2T y margen anual en la parte baja o media del rango.'],
     'videos': [('g6FVIzh99x4', 'Fluidra resultados 1S 2026: ventas +5% a tipo constante, EBITDA 321 M€ | Beneficio neto -7%'),
                ('zlALNKgx1Kg', 'Fluidra 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-29',
     'proximo_estimado': True,
     'fuentes': 'Fluidra, nota de prensa de resultados del primer semestre 2026 (CNMV y fluidra.com, 30-jul-2026); Fluidra, resultados 1S 2025, 1T 2025, '
                '1T 2026 y 2025 con guía 2026; Europa Press/Bolsamanía y Estrategias de Inversión (detalle, 30-jul-2026); Investing.com (presentación y '
                'conferencia, 30-jul-2026); Renta 4 (30-jul-2026) y Merca2 (Citi, 31-jul-2026) (consenso); stockanalysis.com (precio y múltiplos, 11-sep '
                'y 2-oct-2026).',
     'fuentes_corto': 'Europa Press, Estrategias de Inversión, Investing.com, Renta 4, Merca2 y stockanalysis.com',
     'elaborado': '17-oct-2026, 08:30'},
    {'id': 'naturgy',
     'nombre': 'Naturgy',
     'ticker': 'NTGY',
     'sector': 'Eléctricas y gas · redes, generación y comercialización',
     'lede': 'Grupo integrado de gas y electricidad con redes de distribución en España y Latinoamérica (México, Brasil, Chile, Argentina y Panamá), '
             'ciclos combinados, nuclear y renovables, gestión del aprovisionamiento de gas (con el contrato de Sonatrach y Medgaz) y comercialización.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 1.215 M€ (+5,9%) y EBITDA de 2.975 M€ (+4,5%), por encima del consenso que recoge Capitalbolsa (1.166 y 2.888 M€; '
                '+4,2% y +3,0%, calculado). Las redes de distribución tiran del grupo (+13,2%) y Naturgy eleva su guía de 2026.',
     'precio': '30,64 €',
     'precio_fecha': '16-oct-2026',
     'multiplos': [('PER 12 meses', '13,5x'),
                   ('PER forward', '14,3x'),
                   ('EV/EBITDA', '8,0x'),
                   ('Precio / valor contable', '2,42x'),
                   ('Rentab. dividendo', '5,78%'),
                   ('FCF yield', '7,6%'),
                   ('Capitalización', '~28.395 M€')],
     'multiplos_nota': 'Con precio de 30,64 € al 16-oct-2026 (stockanalysis.com). A cierre de 2023, 2024 y 2025 el PER era 13,1x, 11,8x y 12,3x, el '
                       'EV/EBITDA 7,9x, 7,6x y 8,1x, el precio / valor contable 2,17x, 1,93x y 2,19x, y la rentabilidad por flujo libre 9,4%, 8,0% y '
                       '9,5%.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ventas', '10.097', '+1,4%'),
               ('EBITDA', '2.975', '+4,5%'),
               ('EBITDA de redes', '1.514', '+13,2%'),
               ('Beneficio neto', '1.215', '+5,9%'),
               ('Beneficio neto 2T (calculado)', '685', '+6,9%'),
               ('Inversiones', '844', '-5,9%'),
               ('BPA (calculado)', '~1,31 €', '')],
     'kpi': 'Margen EBITDA 29,5% (28,6% en 1S 2025; calculado). Redes: España 855 M€ y Latinoamérica 665 M€ de EBITDA (calculado); electricidad España '
            'incluye 74 M€ de ajustes retroactivos no recurrentes. FFO 2.316 M€ (+7,8%) y flujo de caja libre tras minoritarios 1.259 M€ (-1,6%). Deuda '
            'neta 11.745 M€, 572 M€ menos que en diciembre; deuda neta / EBITDA 2,2x. Coste medio de la deuda 4,0%; liquidez 10.210 M€. Capacidad '
            'renovable 8.433 MW (+9,2%), con ~1,3 GW en construcción.',
     'guia': 'Guía 2026 elevada: EBITDA de más de 5.500 M€ (antes, más de 5.300) y beneficio neto de más de 2.100 M€ (antes, más de 1.900); el semestre '
             'ya suma el 54% y el 58% (calculado). Deuda neta de ~13.000 M€ a cierre, con un pago puntual de ~400 M€ a Sonatrach. Dividendo a cuenta de '
             '0,60 € (pagado el 29-jul) y mínimo de 1,80 € por acción con cargo a 2026. En el semestre salieron GIP (11,4%) y CVC (13,8%); el capital '
             'flotante supera el 46%.',
     'positivos': ['Los resultados superaron al consenso y la empresa eleva su guía de 2026.',
                   'Las redes crecen un 13,2% y ya son la mitad del EBITDA.',
                   'La deuda neta bajó 572 M€ y el capital flotante es el mayor de su historia tras la salida de GIP y CVC.'],
     'riesgos': ['La comercialización cae un 17,4% y las renovables un 2,8%.',
                 'Parte del crecimiento de las redes en España son 74 M€ de ajustes que no se repetirán.',
                 'La deuda subirá en el segundo semestre (~13.000 M€) y la empresa anticipa un invierno complejo por el precio del gas.'],
     'videos': [('5YX26YWgemU', 'Naturgy resultados 1S 2026: beneficio +5,9%, por encima del consenso | Redes +13,2% y guía al alza'),
                ('WBGXyA-ix64', 'Naturgy 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-29',
     'fuentes': 'Naturgy, informe de resultados del primer semestre 2026 (CNMV y naturgy.com, 22-jul-2026), nota de prensa del 22-jul-2026, informe 1T26 '
                '(29-abr-2026) y calendario financiero; Capitalbolsa (consenso, 22-jul-2026); XTB e Investing.com (guía anterior y dividendo, '
                '22-jul-2026); Bolsamanía/Europa Press (22-jul-2026); stockanalysis.com (precio y múltiplos, 16-oct-2026).',
     'fuentes_corto': 'Capitalbolsa, XTB, Investing.com, Bolsamanía y stockanalysis.com',
     'elaborado': '17-oct-2026, 08:15'},
]
