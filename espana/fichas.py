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
    {'id': 'redeia',
     'nombre': 'Redeia',
     'ticker': 'RED',
     'sector': 'Eléctricas · red de transporte',
     'lede': 'Matriz de Red Eléctrica, que opera y transporta la electricidad en alta tensión en España. También tiene negocio internacional '
             '(Latinoamérica) y de fibra óptica (Reintel).',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 410,3 M€ hasta septiembre (+5,3%) y de 129,9 M€ en el tercer trimestre (+8%). La inversión sube un 17,7%, a 1.138,9 '
                'M€, y el consejo aprueba un dividendo a cuenta de 0,2040 € por acción (+2%), pagadero el 7 de enero.',
     'precio': '15,02 €',
     'precio_fecha': '26-oct-2026',
     'multiplos': [('PER 12 meses (calculado)', '15,4x'),
                   ('Precio / valor contable (calculado)', '1,42x'),
                   ('EV/EBITDA (calculado)', '10,5x'),
                   ('EV/EBITDA (stockanalysis, 2-oct-2026)', '11,3x'),
                   ('Rentab. dividendo (calculado)', '5,3%'),
                   ('Capitalización', '~8.125 M€')],
     'multiplos_nota': 'Con precio de 15,02 € al cierre del 26-oct-2026 (Bolsamanía), último cierre disponible en las fuentes consultadas. PER con el '
                       'beneficio de 12 meses a septiembre (526,1 M€), P/VC con valor contable de 10,60 € por acción (stockanalysis), EV/EBITDA con '
                       'deuda neta de septiembre y EBITDA de 12 meses (~1.309 M€) y rentabilidad con el dividendo de 2025 (0,80 €): todo calculado. A '
                       'cierre de 2023, 2024 y 2025 (stockanalysis) el PER era 11,7x, 25,4x y 16,8x, el precio / valor contable 1,46x, 1,69x y 1,54x, la '
                       'rentabilidad por dividendo 7,6%, 5,3% y 5,5%, y el EV/EBITDA 10,4x, 13,9x y 13,3x.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Cifra de negocio', '1.312,9', '+7,8%'),
               ('Gestión y operación de la red en España', '1.176,8', '+9,7%'),
               ('EBITDA', '1.001,4', '+5,3%'),
               ('EBIT', '627,0', '+1,9%'),
               ('Beneficio neto', '410,3', '+5,3%'),
               ('Beneficio neto 3T', '129,9', '+8,0%'),
               ('BPA (calculado)', '~0,76 €', '+5,3%')],
     'kpi': 'Margen EBITDA 76,3% sobre la cifra de negocio (78,1% en 9M 2025; calculado). Con participadas, ingresos de 1.352,4 M€ (+7,2%); transporte '
            'internacional 97,9 M€ (-6,1%) y fibra óptica 104,0 M€ (-7,0%) (variaciones calculadas). Inversión de 1.138,9 M€ (+17,7%), 1.092 M€ en Red '
            'Eléctrica. FFO 823,8 M€ (+15,5%), ~72% de la inversión (calculado). Deuda neta 5.600,8 M€, +2,3% sobre diciembre y +591 M€ en el tercer '
            'trimestre; deuda neta / EBITDA ~4,3x (calculado). Fitch y S&P rebajaron el rating a BBB+ (desde A-) este año.',
     'guia': 'Sin guía numérica de beneficio en el informe. Dividendo a cuenta de 2026: 0,2040 € por acción (+2%), pago el 7 de enero; plan 2026-2029 '
             'con dividendo +2% anual hasta 0,87 € en 2029. Retribución financiera de la red eléctrica: 6,58% en 2026-2031 (CNMC). Golfo de Bizkaia: '
             'todos los cables submarinos tendidos; interconexión Portugal-Galicia en servicio; 43 posiciones para evacuar renovables antes de fin de '
             'año.',
     'positivos': ['El beneficio del tercer trimestre creció un 8%.',
                   'La red en España factura un 9,7% más.',
                   'El FFO sube un 15,5% y el dividendo a cuenta crece un 2%, como marca el plan.'],
     'riesgos': ['La inversión supera a la caja generada: la deuda neta subió 591 M€ en el trimestre y el rating ya es BBB+.',
                 'El transporte internacional y la fibra óptica siguen bajando (calculado).',
                 'Los márgenes se estrechan por la amortización y los costes: el EBIT solo sube un 1,9%.'],
     'videos': [('miVprt1OeNQ', 'Redeia resultados 3T 2026: beneficio +5,3% e inversión +17,7% | Dividendo a cuenta 0,204 €'),
                ('9Q1ek3XWhBE', 'Redeia 3T 2026 en 60 segundos (Short)'),
                ('wbzhyA-076o', 'Redeia resultados 1S 2026: beneficio +4%, en línea con el consenso | Deuda neta −465 M€'),
                ('oFncLSa2iN4', 'Redeia 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Redeia, resultados 9M26 y dividendo a cuenta (CNMV, 28-oct-2026), recogidos por Europa Press (Infobae, elDiario.es, Forbes), '
                'Bolsamanía, Vozpópuli, Business People y El Español (28-oct-2026); Redeia, informes de resultados 9M25 (29-oct-2025) y 1S26 '
                '(29-jul-2026) y resultados 2025 (26-feb-2026); CNMC (18-sep-2026); Bolsamanía (precio) y stockanalysis.com (múltiplos históricos, '
                'oct-2026).',
     'fuentes_corto': 'Europa Press, Bolsamanía, Vozpópuli, Business People, El Español, CNMC y stockanalysis.com',
     'elaborado': '28-oct-2026, 11:25'},
    {'id': 'bankinter',
     'nombre': 'Bankinter',
     'ticker': 'BKT',
     'sector': 'Banca',
     'lede': 'Banco español con negocio en España, Portugal e Irlanda, centrado en banca de empresas, banca privada y gestión de patrimonios; desde '
             'agosto de 2026 incluye Tulp (hipotecas en Países Bajos). En un banco, los ingresos son el margen bruto y la calidad del balance se mide '
             'con la morosidad y el capital.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 901 M€ hasta septiembre (+11%), con un margen de intereses en niveles récord (1.762 M€, +5,7%) y comisiones netas '
                '+12,9%. El beneficio del 3T (~296 M€, +9,5%; calculado) quedó prácticamente en línea con el consenso, pero los ingresos del trimestre, '
                'un 2% por debajo, y la acción caía un 4,8% a media mañana (Bolsamanía).',
     'precio': '14,555 €',
     'precio_fecha': '22-oct-2026, 10:03',
     'multiplos': [('PER 12 meses', '~11,1x'),
                   ('PER forward', '~10,6x'),
                   ('Precio / valor en libros', '~1,95x'),
                   ('Rentab. dividendo', '~4,2%'),
                   ('Capitalización', '~13.080 M€')],
     'multiplos_nota': 'Con precio de 14,555 € el 22-oct-2026 a las 10:03 (Bolsamanía); todos los múltiplos calculados con datos de stockanalysis.com '
                       '(898,69 M de acciones, valor contable 7,46 € por acción, dividendo 0,61 €, PER forward 10,78x a 14,86 €) y el beneficio neto de '
                       '12 meses a septiembre (1.179 M€). A cierre de 2022, 2023, 2024 y 2025 el PER era 10,3x, 6,2x, 7,2x y 11,7x, y el precio / valor '
                       'en libros 1,15x, 0,98x, 1,17x y 1,98x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Margen de intereses', '1.762', '+5,7%'),
               ('Comisiones netas', '651', '+12,9%'),
               ('Margen bruto', '2.397', '+6,5%'),
               ('Costes operativos', '833,9', '+2,3%'),
               ('Margen antes de provisiones', '1.563,6', '+8,8%'),
               ('Beneficio neto', '901', '+11%'),
               ('Beneficio neto 3T (calculado)', '~296', '+9,5%'),
               ('BPA (calculado)', '~1,00 €', '+11%')],
     'kpi': 'Eficiencia 34,8% (36,1% hace un año); ROE 19,2%; ROTE 20,4%. Morosidad 1,84% (−21 pb), cobertura 66,8%, coste del riesgo 33 pb. CET1 13,2% '
            '(mínimo BCE 8,6%). Crédito 87.134 M€ (+5,6%); recursos de clientes y gestionados 163.008 M€ (+7,9%); fuera de balance +15,2%; nueva '
            'producción hipotecaria del 3T, más de 1.500 M€ (+8%). Beneficio antes de impuestos: España 1.050 M€ (+10%), Portugal 178 M€ (+13%), Irlanda '
            '41 M€ (+21%).',
     'guia': 'Guía 2026 (conferencia del 22-oct-2026): margen de intereses subiendo cada trimestre, comisiones con crecimiento de doble dígito bajo (en '
             'julio, un dígito alto), eficiencia por debajo del 35%, coste del riesgo de unos 33 pb, crédito creciendo a un dígito medio y CET1 de '
             'alrededor del 13% a fin de año, tras las compras de Tulp (−16 pb) y de Plenium y Access Capital Partners (unos −25 pb, pendiente). Para '
             'superar el récord de 2025 (1.090 M€) necesita más de 189 M€ en el 4T (calculado).',
     'positivos': ['El margen de intereses sube por sexto trimestre seguido (3T: 602 M€, +6% a/a).',
                   'Comisiones +12,9% y recursos fuera de balance +15,2%; la guía de comisiones mejora.',
                   'Menos morosidad (1,84%) y más capital (CET1 13,2%).'],
     'riesgos': ['Los ingresos del 3T quedaron un 2% por debajo del consenso y la acción caía un 4,8%.',
                 'Sin los 23 M€ extraordinarios del 2T, las comisiones crecen en torno a un 9%.',
                 'El coste de los depósitos sube (86 pb frente a 82 pb) y las compras consumen capital.'],
     'videos': [('O141MKpxQEo', 'Bankinter resultados 3T 2026: beneficio +11% con margen récord; ingresos del 3T bajo el consenso'),
                ('YgVQ-5CaJRA', 'Bankinter 3T 2026 en 60 segundos (Short)'),
                ('k7qJSVY5__k', 'Bankinter resultados 1S 2026: beneficio récord +11,7%; el 2T supera al consenso | Eficiencia 34,3%')],
     'proximo': '2027-01-21',
     'proximo_estimado': True,
     'fuentes': 'Bankinter, nota de resultados de los nueve meses de 2026 (22-oct-2026, CNMV y bankinter.com); presentación y conferencia de resultados '
                '9M26 (Investing.com); EFE (Diario de Santiago), Bolsamanía y Demócrata (22-oct-2026); Bankinter, resultados 1S26 (23-jul-2026); '
                'stockanalysis.com (precio y múltiplos, oct-2026).',
     'fuentes_corto': 'Investing.com, EFE, Bolsamanía y stockanalysis.com',
     'elaborado': '22-oct-2026, 11:15'},
    {'id': 'santander',
     'nombre': 'Banco Santander',
     'ticker': 'SAN',
     'sector': 'Banca',
     'lede': 'Mayor banco español por capitalización, con negocio en Europa (España, Reino Unido, Portugal) y América (Brasil, Estados Unidos, México). '
             'En 2026 vendió su banco en Polonia y compró TSB en Reino Unido (abril) y Webster en Estados Unidos (agosto). En un banco, los ingresos son '
             'el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio ordinario de 11.176 M€ hasta septiembre (+16%), récord; el atribuido (contable), 12.405 M€ (+20%), suma 1.895 M€ de plusvalía '
                'por la venta de Polonia y resta 666 M€ de cargos por TSB y Webster. El ordinario del 3T (3.848 M€, +19%) superó los 3.793 M€ del '
                'consenso recopilado por el banco; la acción cerró el 28-oct-2026 con una caída del 5,6%, con Brasil pesando tras sus elecciones.',
     'precio': '10,638 €',
     'precio_fecha': '28-oct-2026 (cierre)',
     'multiplos': [('PER 12 meses', '~9,5x'),
                   ('PER forward', '~9,3x'),
                   ('Precio / valor en libros', '~1,32x'),
                   ('Rentab. dividendo', '~2,4%'),
                   ('Capitalización', '~153.080 M€')],
     'multiplos_nota': 'Con el cierre de 10,638 € del 28-oct-2026 (Europa Press y The Officer); todos los múltiplos calculados con datos de '
                       'stockanalysis.com (14,39 mil M de acciones; P/VC 1,43x, PER forward 10,05x y dividendo 0,25 € a 11,51 €) y el beneficio '
                       'atribuido de 12 meses a septiembre (16.169 M€, con la plusvalía de Polonia; ~10,2x sin ella ni los cargos). Recompras '
                       'equivalentes al ~3,5% anual. A cierre de 2022, 2023, 2024 y 2025 el PER era 5,1x, 5,7x, 5,7x y 11,0x, y el precio / valor en '
                       'libros 0,48x, 0,58x, 0,63x y 1,31x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Margen de intereses', '34.614', '+10%'),
               ('Comisiones netas', '10.349', '+9%'),
               ('Margen bruto', '46.807', '+8%'),
               ('Costes (calculado)', '19.925', '−1% sin TSB ni Webster'),
               ('Margen neto', '26.882', '+14%'),
               ('Dotaciones por insolvencias', '10.060', '+13%'),
               ('Beneficio ordinario', '11.176', '+16%'),
               ('Beneficio ordinario 3T', '3.848', '+19%'),
               ('Beneficio atribuido', '12.405', '+20%'),
               ('BPA contable', '—', '+25%')],
     'kpi': 'Eficiencia 42,6% (−2,8 pp); RoTE ordinario 16,0% (+1,1 pp). Morosidad 2,90% (−3 pb en el trimestre), cobertura 64%, coste del riesgo 1,16%. '
            'CET1 12,7% (13,1% hace un año), tras restar 147 pb por la compra de Webster. Crédito y recursos de clientes +16% en euros constantes (+6% y '
            '+8% sin compras); 189 M de clientes (+17 M). Beneficio ordinario por países: España 3.695 M€ (+14,3%), Brasil 1.596 M€ (+0,4%), EE. UU. '
            '1.514 M€ (+26,8%, con Webster), México 1.402 M€ (+15,8%), Reino Unido 1.282 M€ (+33,8%, con TSB). Por negocios: banca comercial 6.445 M€ '
            '(+12%), CIB 2.433 M€ (+15%), Wealth 1.651 M€ (+19%), Openbank 1.407 M€, Payments 105 M€.',
     'guia': 'Objetivos 2026 reiterados (euros constantes, sin las compras): ingresos creciendo a un dígito medio, costes a la baja y beneficio por '
             'encima de los 14.101 M€ de 2025 (hasta septiembre, el 79%, calculado); CET1 entre el 12,8% y el 13% a cierre de 2026. Objetivos 2028: RoTE '
             'de más del 20%, beneficio de más de 20.000 M€ y más de 210 M de clientes. Dividendo a cuenta de 12,70 céntimos por acción (+10%), pago el '
             '2-nov-2026, y recompra de ~1.800 M€ (~3.660 M€ en total con cargo al 1S26).',
     'positivos': ['Beneficio ordinario récord (+16%); el del 3T, +19% y por encima del consenso.',
                   'Costes −1% sin TSB ni Webster y eficiencia del 42,6%, casi 3 puntos mejor.',
                   'RoTE ordinario del 16% y BPA contable +25%, con ayuda de las recompras.'],
     'riesgos': ['Brasil apenas crece (+0,4%) y la acción cae tras sus elecciones (−7,85% desde la victoria de Lula).',
                 'Ingresos del 3T algo por debajo de lo esperado; según Jefferies, el margen de intereses sin las compras bajó un 2% frente al 2T.',
                 'CET1 del 12,7%, por debajo de su objetivo de fin de año tras comprar Webster; la integración tiene costes (666 M€ de cargos).'],
     'videos': [('hJdF0dxldqU', 'Banco Santander resultados 3T 2026: beneficio ordinario récord +16%; el atribuido, +20% con Polonia'),
                ('pfCVDRcmU8Q', 'Banco Santander 3T 2026 en 60 segundos (Short)'),
                ('-ED5j67j-0g', 'Banco Santander resultados 1S 2026: beneficio ordinario récord +15%; el 2T, en línea | BPA +20%'),
                ('ZesAasxjui0', 'Banco Santander 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-03',
     'proximo_estimado': True,
     'fuentes': 'Banco Santander, nota de resultados de los nueve meses de 2026 (28-oct-2026, santander.com y CNMV); Bolsamanía, OKDIARIO, roams.es, '
                'Servimedia, Atlántico, Europa Press, The Officer y Rankia (28-oct-2026); Banco Santander, resultados 1S26 (22-jul-2026); '
                'stockanalysis.com (precio y múltiplos, oct-2026).',
     'fuentes_corto': 'Bolsamanía, OKDIARIO, Europa Press y stockanalysis.com',
     'elaborado': '28-oct-2026, 23:30'},
    {'id': 'bbva',
     'nombre': 'BBVA',
     'ticker': 'BBVA',
     'sector': 'Banca',
     'lede': 'Banco español con negocio en España, México, Turquía y América del Sur, además de banca mayorista internacional y banca digital en Italia '
             'y Alemania. En un banco, los ingresos son el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio atribuido récord de 9.066 M€ hasta septiembre (+13,6%; +11,4% a tipos constantes). El 3T (3.015 M€, +19%) quedó en línea con '
                'el consenso (~3.010 M€ según Reuters) y el margen de intereses superó lo esperado, pero la acción caía más de un 5% el 29-oct-2026: '
                'España ganó un 5,5% menos en el trimestre, las dotaciones fueron mayores de lo previsto y el CET1 (12,21%) quedó algo por debajo del '
                'consenso.',
     'precio': '21,27 €',
     'precio_fecha': '29-oct-2026 (~9:30, sesión abierta)',
     'multiplos': [('PER 12 meses', '~10,0x'),
                   ('PER forward', '~9,6x'),
                   ('Precio / valor en libros', '~1,83x'),
                   ('Rentab. dividendo', '~4,6%'),
                   ('Capitalización', '~116.200 M€')],
     'multiplos_nota': 'Con 21,27 € el 29-oct-2026 hacia las 9:30 (Demócrata; Investing.com da 21,26 € a las 9:54). Todos los múltiplos son cálculos '
                       'propios: 5.462 M de acciones (presentación de BBVA), beneficio de 12 meses a septiembre de 11.599 M€, PER forward (9,99x) y P/VC '
                       '(1,91x) de stockanalysis.com a 22,23 € ajustados al precio, y dividendos cobrados en los últimos 12 meses (0,60 € en abril + '
                       '0,37 € en octubre). P/VC tangible ~1,95x (VCT 10,92 €). A cierre de 2022, 2023, 2024 y 2025 el PER era 5,5x, 6,3x, 5,6x y 11,3x, '
                       'y el precio / valor en libros 0,66x, 0,87x, 0,91x y 1,85x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025 (euros corrientes)',
     'tabla': [('Margen de intereses', '23.243', '+20,8%'),
               ('Comisiones netas', '6.909', '+13,8%'),
               ('Margen bruto', '32.072', '+18,2%'),
               ('Gastos de explotación', '12.168', '+17,5% (calculado)'),
               ('Margen neto', '19.904', '+16,5% a tipos constantes'),
               ('Deterioro de activos financieros', '5.444', '+25,8%'),
               ('Beneficio atribuido', '9.066', '+13,6%'),
               ('Beneficio atribuido 3T', '3.015', '+19,1%'),
               ('BPA', '—', '+17,5%')],
     'kpi': 'Eficiencia 37,9% (38,0% en 9M25); ROE 20,8%; ROTE 22%. Morosidad 2,6% (2,8% un año antes), cobertura 84%, coste del riesgo 1,44% (Turquía '
            '2,55%). CET1 12,21% (12,90% en junio: la recompra restó 49 pb, el beneficio sumó 71 pb, el dividendo a cuenta restó 38 pb y los activos '
            'ponderados 44 pb); rango objetivo 11,5%-12%, requerimiento 8,97%. Crédito +20,4% en un año a tipos constantes; préstamos a la clientela '
            '527.455 M€ (+14,6% frente a diciembre). Beneficio atribuido por área: México 4.522 M€ (+8,4% a tipos constantes; +16,9% corrientes), España '
            '3.106 M€ (−0,2%; 3T −5,5%), América del Sur 821 M€ (+42,1%), Resto de negocios 801 M€ (+58,5%), Turquía 789 M€ (+21,8%).',
     'guia': 'Guía 2026 dada en julio: ROTE en torno al 21% (hasta septiembre, 22%) y coste del riesgo en Turquía de unos 220 pb (hasta septiembre, 255 '
             'pb). Objetivos 2025-2028: ~48.000 M€ de beneficio acumulado (llevan 19.600 M€), ROTE medio ~22% y eficiencia ~35% en 2028. Remuneración: '
             'dividendo a cuenta de 0,37 € brutos (+16%), pagado el 15-oct-2026; recompra extraordinaria de 2.000 M€, con el segundo tramo de 1.000 M€ '
             'en marcha desde el 14-oct-2026 (terminará como muy tarde el 4-feb-2027).',
     'positivos': ['Beneficio récord (+13,6%); el 3T, +19% y en línea con el consenso.',
                   'Margen de intereses por encima de lo esperado y crédito +20,4% en un año.',
                   'ROTE del 22%, por encima de su guía, y BPA +17,5% con ayuda de las recompras.'],
     'riesgos': ['España pierde fuerza: beneficio del 3T −5,5% y por debajo de lo esperado.',
                 'Dotaciones mayores de lo previsto; en Turquía, coste del riesgo de 255 pb frente a una guía de ~220 pb.',
                 'CET1 del 12,21%, algo por debajo del consenso: menos capital por encima de su rango objetivo para repartir.'],
     'videos': [('rnaDPgty_Hg', 'BBVA resultados 3T 2026: beneficio récord +13,6%; el 3T, en línea | España y capital pesan en bolsa'),
                ('FKeWVPYcQDk', 'BBVA 3T 2026 en 60 segundos (Short)'),
                ('pUB4hXT_RaQ', 'BBVA resultados 1S 2026: beneficio récord +11,1%; el 2T supera al consenso | ROTE 22,2%'),
                ('9eV_Y5hfj-o', 'BBVA 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-04',
     'proximo_estimado': True,
     'fuentes': 'BBVA, nota y presentación de resultados de los nueve meses de 2026 (29-oct-2026, bbva.com y CNMV); Infobae, Demócrata, Bolsamanía, '
                'Reuters, Investing.com, El Conciso, BilbaoHiria y Economía de Mallorca (29-oct-2026); PressDigital y Merca2 (recompra, 13-oct-2026); '
                'BBVA, resultados 1S26 (30-jul-2026); stockanalysis.com (múltiplos, oct-2026).',
     'fuentes_corto': 'Infobae, Bolsamanía, Reuters, Investing.com y stockanalysis.com',
     'elaborado': '29-oct-2026, 12:00'},
    {'id': 'sabadell',
     'nombre': 'Banco Sabadell',
     'ticker': 'SAB',
     'sector': 'Banca',
     'lede': 'Banco español centrado en empresas y particulares, con negocio también en México. Vendió su filial británica TSB a Banco Santander '
             '(cerrada el 1-may-2026), tras la OPA de BBVA, que quedó desierta en octubre de 2025; desde el 6-oct-2026 el grupo francés BPCE tiene '
             'alrededor del 7% del capital. En un banco, los ingresos son el margen bruto y la calidad del balance se mide con la morosidad y el '
             'capital.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 1.376 M€ hasta septiembre (−1%), marcado por la venta de TSB: aportó 79 M€ en cuatro meses (242 M€ en 9M25) y dejó '
                'una plusvalía neta de 322 M€. Sin TSB, el beneficio pasa de 1.148 a 1.297 M€ (+13%); sin TSB ni extraordinarios, el recurrente fue de '
                '1.096 M€ (−5,3%). El recurrente del 3T subió un 13% frente al 2T, hasta 405 M€, por encima de los 376 M€ del consenso según Bankinter.',
     'precio': '3,512 €',
     'precio_fecha': '29-oct-2026 (cierre)',
     'multiplos': [('PER 12 meses', '~9,5x'),
                   ('PER forward', '~11,4x'),
                   ('Precio / valor en libros', '~1,41x'),
                   ('Rentab. dividendo', '~7,4%'),
                   ('Capitalización', '~16.750 M€')],
     'multiplos_nota': 'Con el cierre de 3,512 € del 29-oct-2026 (−0,23%; MarketScreener y Bolsamanía). Todos los múltiplos son cálculos propios: '
                       '4.768,5 M de acciones tras la amortización de julio, beneficio de 12 meses a septiembre de 1.761 M€ (incluye TSB y su '
                       'plusvalía), PER forward (11,51x) y P/VC (1,42x) de stockanalysis.com a 3,531 € ajustados al cierre. La rentabilidad por '
                       'dividendo usa el dividendo ordinario de los últimos 12 meses (0,26 €) y no incluye el extraordinario de 0,50 € pagado en mayo. A '
                       'cierre de 2022, 2023, 2024 y 2025 el PER era 6,3x, 5,0x, 5,9x y 10,3x, y el precio / valor en libros 0,38x, 0,44x, 0,68x y '
                       '1,19x. Sin TSB el perímetro del grupo cambia. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025 (ingresos y costes sin TSB)',
     'tabla': [('Margen de intereses', '2.694', '−0,6%'),
               ('Comisiones netas', '983', '+2,1%'),
               ('Margen bruto', '3.777', '+1,0%'),
               ('Costes totales', '1.797', '+9,1% (+3,8% sin prejubilaciones)'),
               ('Margen antes de dotaciones', '1.981', '−5,3%'),
               ('Beneficio recurrente', '1.096', '−5,3%'),
               ('Beneficio recurrente 3T', '405', '+13% frente al 2T'),
               ('Beneficio neto', '1.376', '−1,0%'),
               ('BPA recurrente (calculado)', '~0,23 €', '')],
     'kpi': 'ROTE recurrente 14,2% (13,6% en junio). Eficiencia ~47,6% con costes totales y ~45,2% sin prejubilaciones (~44% en 9M25), calculada. '
            'Morosidad 2,40% (2,47% en junio y 2,75% un año antes), cobertura 70,1%, coste del riesgo 40 pb; provisiones −13% en el trimestre. CET1 '
            'fully loaded 13,12% (13,11% en junio; 13,74% en sep-25). Crédito vivo 124.913 M€ (+4%; consumo +12,7%, hipotecas +3,5%); recursos de '
            'clientes 189.449 M€ (+5,6%). En el 3T, margen de intereses 920 M€ (+2% t/t), comisiones 340 M€ (+3,7% t/t) y costes recurrentes −0,1% t/t. '
            'Efecto TSB: aportación 79 M€ (242 M€ en 9M25); extraordinarios netos +201 M€ (plusvalía neta de 322 M€ menos prejubilaciones y otros).',
     'guia': 'Guía 2026 actualizada: margen de intereses en torno a +1% y comisiones en torno a +4% (algo por debajo de la anterior), costes recurrentes '
             'en torno a +2% (antes, menos del 3%), coste del riesgo ~40 pb y ROTE recurrente del 14,5% (16% en 2027). Remuneración: dividendo a cuenta '
             'de 2026 en efectivo de 0,07 € por acción (325 M€), con pago el 29-dic-2026 (fecha ex-dividendo aún no comunicada); quedan 57 M€ de la '
             'recompra de 331 M€ lanzada en julio. BPCE tiene ~7% del capital (6-oct-2026) y no prevé superar el 9,9%.',
     'positivos': ['El beneficio recurrente del 3T sube un 13% frente al 2T y supera el consenso (405 frente a 376 M€, según Bankinter).',
                   'Margen de intereses (+2%) y comisiones (+3,7%) crecen por segundo trimestre seguido, con los costes recurrentes planos.',
                   'Morosidad a la baja (2,40%), coste del riesgo de 40 pb y ROTE recurrente del 14,2%, cerca del objetivo anual.'],
     'riesgos': ['En el acumulado, el beneficio recurrente cae un 5,3% y el margen de intereses un 0,6%.',
                 'La guía de ingresos de 2026 se rebaja ligeramente (margen de intereses ~+1%, comisiones ~+4%).',
                 'Sin TSB el banco es más pequeño (activo −18,5% en un año) y el CET1 es 62 pb más bajo que hace un año.'],
     'videos': [('W3Oth22d-uc', 'Banco Sabadell resultados 3T 2026: beneficio 1.376 M€ (-1%) por TSB | recurrente del 3T +13%'),
                ('MrccAzO5zV4', 'Banco Sabadell 3T 2026 en 60 segundos (Short)'),
                ('wkQGwk63kTE', 'Banco Sabadell resultados 1S 2026: beneficio 971 M€ con TSB; recurrente -14,1% | CET1 13,11%'),
                ('7YzKyAdIs68', 'Banco Sabadell 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-05',
     'proximo_estimado': True,
     'fuentes': 'Banco Sabadell, nota de resultados de los nueve meses de 2026 (29-oct-2026, grupbancsabadell.com y CNMV) y nota conjunta con BPCE '
                '(6-oct-2026); Infobae/EFE, Infobae, El Español, Libre Mercado, Bolsamanía (incluidos Bankinter y Renta 4), Merca2 y Crónica Global '
                '(29-oct-2026); MarketScreener y Bolsamanía (cotización, 29-oct-2026); Europa Press (acciones, 24-jul-2026); Banco Sabadell, resultados '
                '1S26 (24-jul-2026); stockanalysis.com (múltiplos, oct-2026).',
     'fuentes_corto': 'Infobae/EFE, Bolsamanía, El Español, MarketScreener y stockanalysis.com',
     'elaborado': '29-oct-2026, 23:00'},
    {'id': 'unicaja',
     'nombre': 'Unicaja',
     'ticker': 'UNI',
     'sector': 'Banca',
     'lede': 'Banco español minorista, con fuerte presencia en Andalucía, Castilla y León, Castilla-La Mancha, Asturias y Extremadura. En un banco, los '
             'ingresos son el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 543 M€ hasta septiembre (+8,1%). El 3T (182 M€, +10,3%) superó los 171 M€ del sondeo de Reuters; el margen de '
                'intereses del trimestre subió un 3,5% frente al 2T, pero las comisiones quedaron un 4% por debajo de lo esperado (Investing.com). '
                'Unicaja anuncia un segundo dividendo a cuenta de 6,42 céntimos por acción (pago el 17-dic-2026).',
     'precio': '3,170 €',
     'precio_fecha': '30-oct-2026, 10:45',
     'multiplos': [('PER 12 meses', '~12,1x'),
                   ('PER forward', '11,4x'),
                   ('Precio / valor en libros', '~1,21x'),
                   ('Rentab. dividendo', '~5,4%'),
                   ('Capitalización', '~8.150 M€')],
     'multiplos_nota': 'Con precio de 3,170 € el 30-oct-2026 a las 10:45 (stockanalysis.com, retrasado); múltiplos calculados con datos de '
                       'stockanalysis.com (2.570 M de acciones, valor contable 2,63 € por acción, dividendo 0,17 €; PER forward 11,4x de stockanalysis) '
                       'y el beneficio neto de 12 meses a septiembre (672 M€). A cierre de 2022, 2023, 2024 y 2025 el PER era 10,1x, 9,1x, 5,7x y 11,4x, '
                       'y el precio / valor en libros 0,42x, 0,36x, 0,48x y 1,01x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Margen de intereses', '1.151', '+3,0%'),
               ('Comisiones netas', '397', '+1,3%'),
               ('Margen bruto', '1.629', '+3,5%'),
               ('Costes (gastos + amortizaciones)', '746', '~+4,9%'),
               ('Margen antes de provisiones (calculado)', '~883', '~+2,3%'),
               ('Deterioro de activos financieros', '72', '−21,6%'),
               ('Beneficio neto', '543', '+8,1%'),
               ('Beneficio neto 3T', '182', '+10,3%'),
               ('BPA (calculado)', '~0,21 €', '+8%')],
     'kpi': 'Eficiencia 45,8%; ROTE 10,3% (+0,5 pp; 12,2% ajustado por exceso de capital). Morosidad 1,8% (−41 pb), cobertura 84,6% (74% hace un año), '
            'coste del riesgo 19 pb. CET1 fully loaded 15,4% (15,7% en junio; 15,5% phased-in, 6,9 pp sobre lo exigido). Crédito sano 49.371 M€ (+4,9%; '
            'empresas +11,4%, consumo +11,9%); nueva producción hipotecaria 2.851 M€ (+30,5%); recursos minoristas 97.616 M€ (+4,6%); depósitos de '
            'clientes 75.395 M€ (+1,1%); fondos de inversión 19.226 M€ (+13,9%). Margen de intereses del 3T: 395 M€ (+3,5% t/t; +5,5% a/a).',
     'guia': 'Guía 2026 mantenida (Reuters e Investing.com, 30-oct-2026): beneficio creciendo a un dígito medio, margen de intereses a un dígito '
             'bajo-medio, comisiones a un dígito bajo, costes a un dígito medio y coste del riesgo de 20-25 pb. Reparto del 95% del beneficio de 2026 '
             '(70% en 2025): segundo dividendo a cuenta de 6,42 céntimos por acción, pago el 17-dic-2026 (último día con derecho, 14-dic); con el de '
             'septiembre (8,44 céntimos), suman 14,86 céntimos y unos 382 M€. Complementario en abril de 2027, sujeto a la junta.',
     'positivos': ['El beneficio del 3T (182 M€, +10,3%) supera los 171 M€ del sondeo de Reuters.',
                   'El margen de intereses del 3T sube un 3,5% frente al 2T, hasta 395 M€.',
                   'Morosidad del 1,8% (−41 pb), cobertura del 84,6% y nuevo dividendo a cuenta de 6,42 céntimos.'],
     'riesgos': ['Las comisiones crecen un 1,3% y en el 3T quedaron un 4% por debajo de lo esperado.',
                 'Los costes suben cerca de un 4,9%, más que el margen bruto (+3,5%).',
                 'El CET1 fully loaded baja del 15,7% al 15,4% en el trimestre y el coste de los depósitos sube 6 pb.'],
     'videos': [('1N5EZR1nkwo', 'Unicaja resultados 3T 2026: beneficio +8,1%; el 3T supera al consenso | Dividendo de 6,42 céntimos'),
                ('eu2etzVT3G0', 'Unicaja 3T 2026 en 60 segundos (Short)'),
                ('QmTUeCVBUk4', 'Unicaja resultados 1S 2026: beneficio +7,1%; el 2T supera al consenso un 10% | Guía al alza'),
                ('zoldZTxXavE', 'Unicaja 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-02',
     'proximo_estimado': True,
     'fuentes': 'Unicaja, resultados de los nueve meses de 2026 (30-oct-2026, CNMV y unicajabanco.com), según Europa Press (Forbes España, Capital, '
                '101TV) y El Conciso; Reuters e Investing.com (consenso y guía, 30-oct-2026); Bolsamanía (30-oct-2026); Unicaja, resultados 1S26 '
                '(31-jul-2026); stockanalysis.com (precio y múltiplos, 30-oct-2026).',
     'fuentes_corto': 'Europa Press, El Conciso, Reuters, Investing.com y stockanalysis.com',
     'elaborado': '30-oct-2026, 11:30'},
    {'id': 'caixabank',
     'nombre': 'CaixaBank',
     'ticker': 'CABK',
     'sector': 'Banca',
     'lede': 'Mayor banco por clientes en España, con BPI en Portugal y un negocio relevante de seguros y gestión patrimonial. En un banco, los ingresos '
             'son el margen bruto y la calidad del balance se mide con la morosidad y el capital.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 4.962 M€ hasta septiembre (+12,9%). En el 3T ganó 1.759 M€ (+21,7% a/a y +7,8% frente al 2T), por encima de los 1.630 '
                'M€ que esperaban los analistas consultados por Reuters. El banco eleva su objetivo de ROTE para 2026 a alrededor del 19% y pagará el 6 '
                'de noviembre un dividendo a cuenta de 0,1844 € por acción.',
     'precio': '11,18 €',
     'precio_fecha': '30-oct-2026, 10:45',
     'multiplos': [('PER 12 meses', '~12,0x'),
                   ('PER forward', '~11,2x'),
                   ('Precio / valor en libros', '~2,0x'),
                   ('Rentab. dividendo', '~4,5%'),
                   ('Capitalización', '~77.700 M€')],
     'multiplos_nota': 'Con un precio de 11,18 € el 30-oct-2026 a las 10:45 (Bolsamanía; cierre del 29-oct: 11,165 €). Todos los múltiplos son cálculos '
                       'propios: 6.947 M de acciones (1.281 M€ / 0,1844 €), beneficio de 12 meses a septiembre de 6.456 M€ (5.891 - 4.397 + 4.962), PER '
                       'forward de stockanalysis.com (11,62x a 11,62 €) ajustado al precio, valor en libros de 5,56 € por acción (jun-2026) y dividendo '
                       'con cargo a 2025 de 0,50 €. A cierre de 2022, 2023, 2024 y 2025 el PER era 10,1x, 6,1x, 6,8x y 13,0x, y el precio / valor en '
                       'libros 0,86x, 0,77x, 1,02x y 1,90x. En un banco no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Margen de intereses', '8.186', '+2,9%'),
               ('Ingresos por servicios', '4.182', '+7,7%'),
               ('Margen bruto', '12.656', '+4,4%'),
               ('Gastos', '5.004', '+4,3%'),
               ('Margen de explotación', '7.653', '+4,6%'),
               ('Deterioros', '746', '+20,9%'),
               ('Beneficio neto', '4.962', '+12,9%'),
               ('Beneficio neto 3T', '1.759', '+21,7% (+7,8% frente al 2T)'),
               ('BPA 12 meses (calculado)', '~0,93 €', '')],
     'kpi': 'Eficiencia 39,4% (39,2% un año antes); ROTE 18,8% (18,0% en junio; 17,8% un año antes). Morosidad 1,76% (2,07% en dic-2025), cobertura 82%, '
            'coste del riesgo 24 pb. CET1 12,5%, tras restar 20 pb por la recompra. Crédito sano 397.469 M€ (+8%; empresas +11,4%, consumo +9,8%, '
            'vivienda +7%); recursos de clientes 760.353 M€ (+5,6%); activos bajo gestión 216.333 M€ (+10,6%). Gestión patrimonial 1.669 M€ (+12,5%), '
            'seguros de protección 1.000 M€ (+14,5%), comisiones bancarias 1.513 M€ (−0,9%). BPI aportó 339 M€. En el 3T, margen de intereses 2.796 M€ '
            '(+2,5% t/t, algo por debajo del consenso) y margen de clientes 2,87% (−2 pb).',
     'guia': 'Guía 2026: objetivo de ROTE elevado a alrededor del 19% (antes, más del 18%); margen de intereses de más de 11.000 M€ (en el 4T necesita '
             'más de 2.814 M€, calculado) y coste del riesgo por debajo de 25 pb, reiterados (Reuters). Remuneración: dividendo a cuenta de 2026 de '
             '0,1844 € brutos por acción (1.281 M€, el 40% del beneficio del 1S), ex-dividendo el 4-nov (según Finect) y pago el 6-nov-2026; payout del '
             '50-60% con un complementario en abril de 2027; recompra de 500 M€ ampliada hasta el 30-ene-2027.',
     'positivos': ['El beneficio del 3T sube un 21,7% y supera en un 7,9% lo esperado por los analistas (Reuters; calculado).',
                   'Gestión patrimonial (+12,5%) y seguros de protección (+14,5%) siguen creciendo a doble dígito.',
                   'Morosidad en el 1,76% con cobertura del 82%, y objetivo de ROTE elevado a ~19%.'],
     'riesgos': ['El margen de intereses del 3T queda algo por debajo del consenso y el margen de clientes se estrecha 2 pb.',
                 'Los deterioros suben un 20,9% en el acumulado y las comisiones bancarias bajan un 0,9%.',
                 'Parte de la mejora del beneficio viene de menores impuestos y efectos contables (XTB, El Conciso).'],
     'videos': [('syFa1LFf91g', 'CaixaBank resultados 3T 2026: beneficio 4.962 M€ (+12,9%), sobre el consenso | ROTE objetivo ~19%'),
                ('_61uM943I_g', 'CaixaBank 3T 2026 en 60 segundos (Short)'),
                ('GXbYecKtopE', 'CaixaBank resultados 1S 2026: beneficio récord de 3.203 M€ (+8,5%), sobre el consenso | ROTE 18%'),
                ('2UERn_MLK6k', 'CaixaBank 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-01-29',
     'proximo_estimado': True,
     'fuentes': 'CaixaBank, resultados de los nueve meses de 2026 (comunicado a la CNMV, 30-oct-2026), vía Europa Press, Finanzas.com, El Conciso, '
                'Bolsamanía y Capital Madrid; Reuters (MarketScreener, Business Recorder), Investing.com, Finimize y XTB (consenso y guía, 30-oct-2026); '
                'Finect (fechas del dividendo); Bolsamanía (cotización, 30-oct-2026); CaixaBank, resultados 1S26 (29-jul-2026) y 2025 (30-ene-2026); '
                'stockanalysis.com (múltiplos, oct-2026).',
     'fuentes_corto': 'Europa Press, Reuters, Finanzas.com, Bolsamanía y stockanalysis.com',
     'elaborado': '30-oct-2026, 11:30'},
    {'id': 'repsol',
     'nombre': 'Repsol',
     'ticker': 'REP',
     'sector': 'Petróleo y gas · integrada',
     'lede': 'Compañía energética integrada: exploración y producción de petróleo y gas (Upstream), refino y química (Industrial), estaciones de '
             'servicio, electricidad y gas para clientes (Cliente) y generación renovable. En una petrolera, el resultado ajustado a coste de reposición '
             '(CCS) quita el efecto del precio de los inventarios.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Resultado neto ajustado de 5.419 M€ hasta septiembre (+184%), impulsado por el refino; solo en el tercer trimestre, 2.708 M€ (752 M€ en '
                'el 3T 2025). El beneficio neto fue de 5.006 M€ (1.177 M€), con +943 M€ de efecto inventario y -1.356 M€ de resultados específicos. La '
                'deuda neta baja a 2.038 M€ y Repsol lanza una tercera recompra de hasta 950 M€.',
     'precio': '29,33 €',
     'precio_fecha': '29-oct-2026',
     'multiplos': [('PER 12 meses', '5,5x'),
                   ('PER ajustado 12 meses', '5,2x'),
                   ('EV/EBITDA CCS', '3,0x'),
                   ('Precio / valor contable', '1,0x'),
                   ('Rentab. dividendo', '3,6%'),
                   ('Capitalización', '~31.450 M€')],
     'multiplos_nota': 'Calculados con el precio de 29,33 € del 29-oct-2026 hacia las 11:00 (Investing.com), 1.072,2 M de acciones tras la amortización '
                       'del 26-oct (Repsol), beneficio y EBITDA CCS de 12 meses a septiembre, deuda neta de 2.038 M€ (sin minoritarios), patrimonio neto '
                       'total de 30.966 M€ y dividendo en efectivo 2026 de 1,051 €. A cierre de 2023, 2024 y 2025 el PER era 5,5x, 8,1x y 9,6x, el '
                       'EV/EBITDA 3,7x, 4,3x y 6,8x y el precio / valor contable 0,6x, 0,5x y 0,6x (stockanalysis.com, consultado el 29-oct-2026). La '
                       'acción subió un 105% en 52 semanas (stockanalysis.com, 16-oct-2026).',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ventas', '53.620', '+31,3% (calculado)'),
               ('EBITDA CCS', '9.524', '+107,6%'),
               ('Resultado ajustado Industrial', '3.668', '540 en 9M25'),
               ('Resultado ajustado Upstream', '1.088', '+28,6%'),
               ('Resultado ajustado Cliente', '613', '+4,6%'),
               ('Resultado neto ajustado (CCS)', '5.419', '+184,2%'),
               ('Resultado neto', '5.006', '1.177 en 9M25'),
               ('Resultado neto ajustado 3T', '2.708', '+260,1%')],
     'kpi': 'Margen de refino en España 20,6 $/barril (6,7); 36,2 en el 3T (8,8). Producción 557 kbep/d (549); 574 en el 3T y 590 en octubre. Margen '
            'EBITDA CCS 17,8% de las ventas (11,2%; calculado). Flujo de caja de las operaciones 6.503 M€ (+68,8%) pese a ~3.700 M€ invertidos en '
            'existencias; flujo de caja libre 4.195 M€ (1.491). Inversión bruta 2.604 M€ (-21,9%). Deuda neta 2.038 M€ (4.487 M€ en diciembre; caja neta '
            'de 633 M€ sin arrendamientos); apalancamiento 6,2%; deuda neta / EBITDA CCS 12 meses 0,18x (calculado). Liquidez 11.922 M€. BPA 4,51 € '
            '(0,99 €).',
     'guia': 'Producción 2026 prevista de 560.000-570.000 bep/d (sin cambios). Tercer programa de recompra de hasta 950 M€ antes de fin de año: 1.800 M€ '
             'en 2026 y cerca de 3.000 M€ de retribución total (30-40% del flujo de caja de las operaciones). Dividendo en efectivo 2026 de 1,051 '
             '€/acción (0,50 € en enero y 0,551 € en julio); el de enero de 2027 sube de 0,53 € a 0,56 € brutos (0,53 € con cargo a reservas libres y '
             '0,03 € a cuenta de 2026). Compromiso de subir un 3% anual el dividendo en efectivo total en los dos años siguientes. 11.500 M€ en '
             'proyectos en España hasta 2030.',
     'positivos': ['El margen de refino del 3T se multiplica por cuatro y el resultado Industrial es casi siete veces el de 9M 2025.',
                   'El flujo de caja libre casi se triplica y la deuda neta baja a 2.038 M€.',
                   'Más retribución: tercera recompra de hasta 950 M€ y dividendo de enero de 2027 más alto (0,56 €).'],
     'riesgos': ['El beneficio depende de un margen de refino y un precio del crudo excepcionalmente altos, ligados a restricciones de oferta.',
                 'Resultados específicos de -1.356 M€ en 2026 y ~3.700 M€ inmovilizados en existencias.',
                 'Pikka (Alaska) producía 69.000 barriles brutos/día a finales de septiembre, por debajo de su objetivo de 80.000.'],
     'videos': [('B7KnXjbA5h8', 'Repsol resultados 3T 2026: resultado ajustado +184% por el refino | Tercera recompra de 950 M€'),
                ('Bn-mmTXJM-o', 'Repsol 3T 2026 en 60 segundos (Short)'),
                ('LDjyCZImFpQ', 'Repsol resultados 1S 2026: beneficio ajustado +134,7% por el refino; el 2T supera al consenso'),
                ('OMP1V-cPw9s', 'Repsol 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-18',
     'proximo_estimado': True,
     'fuentes': 'Repsol, resultados del tercer trimestre de 2026 (nota de prensa, información de resultados y nota para analistas; CNMV y repsol.com, '
                '29-oct-2026) y del cuarto trimestre de 2025 (19-feb-2026); Bolsamanía, Europa Press y Vozpópuli (29-oct-2026); Investing.com (precio, '
                '29-oct-2026); stockanalysis.com (múltiplos históricos, oct-2026).',
     'fuentes_corto': 'Bolsamanía, Europa Press, Vozpópuli, Investing.com y stockanalysis.com',
     'elaborado': '29-oct-2026, 11:15'},
    {'id': 'telefonica',
     'nombre': 'Telefónica',
     'ticker': 'TEF',
     'sector': 'Telecomunicaciones',
     'lede': 'Operadora de telecomunicaciones con cuatro mercados principales: España, Brasil, Alemania y Reino Unido (Virgin Media O2, al 50%). Está '
             'saliendo de Hispanoamérica: Colombia y Chile se desconsolidaron en febrero de 2026 y la venta de México, firmada en abril, sigue en el '
             'balance como activo en venta a septiembre.',
     'periodo': '3T 2026',
     'periodo_largo': 'tercer trimestre de 2026 (nueve meses)',
     'titular': 'Vuelve a beneficios: resultado neto atribuido de 464 M€ hasta septiembre, frente a una pérdida de 1.080 M€ en 9M 2025; las operaciones '
                'continuadas ganan 1.333 M€ (+21,6%) y las discontinuadas restan 870 M€ (-60%). Ingresos de 24.825 M€ (+2,8%; +1,0% a tipos constantes) '
                'y EBITDA ajustado de 8.846 M€ (+4,6%; +2,5% constante). Sube la guía 2026 de EBITDA ajustado, caja operativa y flujo de caja libre '
                '(~3.100 M€), pero rebaja la de ingresos totales (+1% a +1,5%).',
     'precio': '3,43 €',
     'precio_fecha': '12-nov-2026',
     'multiplos': [('PER 12 meses', 'n/d (pérdidas)'),
                   ('PER forward', '~9,4x'),
                   ('EV/EBITDA', '~7,4x'),
                   ('Precio / valor contable', '~1,06x'),
                   ('Rentab. dividendo 2026', '~4,4%'),
                   ('Capitalización', '~19.310 M€')],
     'multiplos_nota': 'Calculados con 3,43 € (12-nov-2026, intradía hacia las 10:10, tras los resultados; Rankia e Investing.com) y 5.630 M de '
                       'acciones. Sin PER de 12 meses: el resultado atribuido de 12 meses sigue en pérdidas (-4.318 + 464 + 1.080 = -2.774 M€, '
                       'calculado). PER forward, EV/EBITDA y precio / valor contable: datos de stockanalysis.com del 19/20-oct-2026 reescalados al '
                       'precio. Rentabilidad con el dividendo de 2026 (0,15 €); con los 0,30 € pagados en 12 meses, 8,7%. A cierre de 2023, 2024 y 2025 '
                       '(stockanalysis.com) el EV/EBITDA era 8,6x, 6,6x y 8,7x; el PER forward 11,0x, 12,7x y 10,8x; el precio / valor contable 0,74x, '
                       '0,98x y 1,11x, y la rentabilidad por dividendo 9,86%, 8,35% y 8,86%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '24.825', '+2,8%'),
               ('EBITDA ajustado', '8.846', '+4,6%'),
               ('OpCFaL ajustado (EBITDAaL-CapEx)', '4.018', '+6,1%'),
               ('Flujo de caja libre (continuadas)', '1.963', '+10,7%'),
               ('Beneficio neto operaciones continuadas', '1.333', '+21,6%'),
               ('Resultado neto atribuido (total)', '464', '-1.080 en 9M25'),
               ('Resultado neto 3T', '802', '+191,1%'),
               ('Deuda financiera neta (sep-26)', '25.186', '-10,8%')],
     'kpi': 'Margen EBITDA ajustado 35,6% (35,0%); 3T 36,5%. BPA básico 0,04 € (-0,23 €); de continuadas 0,19 € (0,16 €); ajustado de continuadas 0,25 € '
            '(0,29 €) con un beneficio neto ajustado de 1.583 M€ (-14,1%). España: ingresos 9.828 M€ (+2,5%) y EBITDA 3.501 M€ (+2,3%), churn 0,7%. '
            'Brasil: ingresos 7.907 M€ (+7,4% constante) y EBITDA 3.473 M€ (+9,9% constante). Alemania: ingresos 5.597 M€ (-7,6%; 3T -2,9%) y EBITDA '
            '1.745 M€ (-8,5%). Virgin Media O2 (100%): ingresos -6,7% y EBITDA ajustado -3,0%. Por clientes (9M): residencial 14.678 M€, empresas 5.950 '
            'M€, mayorista 4.197 M€ (3T -7,0%). CapEx 3.005 M€ (12,1% de los ingresos). Apalancamiento 2,63x (2,78x en dic-25).',
     'guia': 'Guía 2026 (tipos constantes): EBITDA ajustado algo más de +2,5% (antes +1,5% a +2,5%); OpCFaL ajustado más de +3,5% (antes más de +3%); '
             'flujo de caja libre ~3.100 M€ (antes ~3.000 M€); ingresos totales +1% a +1,5% (antes +1,5% a +2,5%); ingresos de servicio ~+1,5% (nuevo); '
             'CapEx / ingresos ~12%; apalancamiento de 2,5x en 2028. Dividendo con cargo a 2026: 0,15 € en efectivo, a pagar en junio de 2027 (sujeto a '
             'la junta; fecha exacta sin fijar). Con cargo a 2025 pagó 0,30 € (el último tramo, 0,15 €, el 18-jun-2026).',
     'positivos': ['Vuelve a beneficios (464 M€) y el beneficio de las operaciones continuadas sube un 21,6%.',
                   'Sube la guía 2026 de EBITDA ajustado, caja operativa y flujo de caja libre (~3.100 M€).',
                   'La deuda neta baja un 10,8% y el apalancamiento cae a 2,63x.'],
     'riesgos': ['Rebaja la previsión de ingresos totales (+1% a +1,5%) y el negocio mayorista cae un 7% en el 3T.',
                 'Alemania: EBITDA ajustado -8,5% en 9M; Virgin Media O2 pierde ingresos (-6,7%).',
                 'El beneficio neto ajustado de continuadas cae un 14,1% y la venta de México sigue pendiente de cierre.'],
     'videos': [('DdiJ7FHnuAU', 'Telefónica resultados 3T 2026: vuelve a beneficios (464 M€) | Sube la guía de caja, rebaja ingresos'),
                ('tpiuLVcy-rw', 'Telefónica 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Telefónica, informe y nota de prensa de resultados de enero a septiembre de 2026 (CNMV y telefonica.com, 12-nov-2026) y nota de '
                'resultados del primer semestre de 2026; XTB e Investing.com (consenso y reacción, 12-nov-2026), Rankia (precio y dividendo, '
                '12-nov-2026); stockanalysis.com (múltiplos actuales e históricos, oct-2026).',
     'fuentes_corto': 'Telefónica (CNMV), XTB, Investing.com, Rankia y stockanalysis.com',
     'elaborado': '12-nov-2026, 11:30'},
    {'id': 'endesa',
     'nombre': 'Endesa',
     'ticker': 'ELE',
     'sector': 'Eléctricas · redes, generación y comercialización',
     'lede': 'Eléctrica integrada, controlada por Enel, con distribución regulada, generación (renovable, nuclear, convencional y extrapeninsular) y '
             'comercialización de electricidad y gas en España y Portugal. Las redes y la generación extrapeninsular aportan ya cerca de la mitad del '
             'EBITDA.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio ordinario neto de 2.125 M€ hasta septiembre (+22,5%) y beneficio neto de 1.962 M€ (+14,7%). Las redes suben un 24,8% y Endesa '
                'confirma su guía 2026 de más de 2.400 M€ de beneficio ordinario, aunque el EBITDA del tercer trimestre bajó un 11,6% (calculado).',
     'precio': '43,06 €',
     'precio_fecha': '28-oct-2026',
     'multiplos': [('PER 12 meses', '18,0x'),
                   ('PER ordinario 12 meses', '16,1x'),
                   ('EV/EBITDA', '9,0x'),
                   ('Precio / valor contable', '4,8x'),
                   ('Rentab. dividendo', '3,7%'),
                   ('Capitalización', '~44.070 M€')],
     'multiplos_nota': 'Calculados con el precio de 43,06 € del 28-oct-2026 a las 10:41 (Bolsamanía), ~1.023,5 M de acciones (stockanalysis.com), '
                       'beneficio y EBITDA de 12 meses a septiembre, deuda financiera neta de 11.187 M€ y dividendo de 1,584 € con cargo a 2025. A '
                       'cierre de 2023, 2024 y 2025 el PER era 26,3x, 11,7x y 14,5x, el EV/EBITDA 10,5x, 6,9x y 8,2x y el precio / valor contable 2,7x, '
                       '2,4x y 3,3x (stockanalysis.com). La acción subió un 43% en 52 semanas (stockanalysis.com, 20-oct-2026).',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '17.389', '+9,0%'),
               ('EBITDA', '4.577', '+8,4%'),
               ('EBITDA distribución (redes)', '1.747', '+24,8%'),
               ('EBITDA generación y comercialización', '2.889', '+3%'),
               ('EBIT', '2.848', '+11,9%'),
               ('Beneficio neto', '1.962', '+14,7%'),
               ('Beneficio ordinario neto', '2.125', '+22,5%'),
               ('EBITDA 3T (calculado)', '1.337', '-11,6%')],
     'kpi': 'Margen EBITDA 26,3% (26,5% en 9M 2025; calculado). Margen bruto de clientes 1.579 M€ (+16,3%) y de renovables 730 M€ (a la baja). '
            'Producción 49.296 GWh (+6,3%; renovable +7,5%); ventas de electricidad 55.465 GWh (-2,0%) y de gas 38.553 GWh (-8,2%); energía distribuida '
            '114.285 GWh (+4,9%). Cash flow operativo 3.467 M€ (+0,9%); inversión bruta 1.622 M€ (+19,4%; redes ~900 M€, +42%). Deuda financiera neta '
            '11.187 M€ (10.110 M€ en diciembre), 1,8x EBITDA; coste medio 3,2%; liquidez 6.900 M€. Costes fijos 1.481 M€ (-8%) sin una provisión de 202 '
            'M€ por reestructuración de plantilla.',
     'guia': 'Guía 2026 confirmada: beneficio ordinario neto de más de 2.400 M€, pese a unas condiciones de mercado más exigentes en el cuarto '
             'trimestre; los nueve meses ya suman el 88,5% (calculado). Política de dividendo 2026-2028: al menos el 70% del beneficio ordinario neto, '
             'más de 1.680 M€ para 2026 (calculado); el dividendo a cuenta aún no está anunciado. 2.600 M€ al accionista en 2026, con unos 900 M€ de '
             'recompra. Almaraz autorizada hasta junio de 2030. Actualización del plan estratégico en febrero de 2027.',
     'positivos': ['Las redes crecen un 24,8% y la inversión en ellas, un 42%.',
                   'El beneficio ordinario sube un 22,5% y ya cubre el 88,5% de la guía anual (calculado).',
                   'Los costes fijos ajustados bajan un 8%.'],
     'riesgos': ['El tercer trimestre fue más débil: EBITDA -11,6% y beneficio ordinario -7,1% (calculado).',
                 'La deuda neta sube 1.077 M€ desde diciembre y se queda en 1,8x EBITDA.',
                 'Caen las ventas de electricidad (-2,0%) y de gas (-8,2%), y la empresa prevé un cuarto trimestre más exigente.'],
     'videos': [('KHQ8aN7Q7mw', 'Endesa resultados 3T 2026: beneficio ordinario +22,5% y guía confirmada | Redes +24,8%'),
                ('Vl1lgHPunoc', 'Endesa 3T 2026 en 60 segundos (Short)'),
                ('hinLi7xl-R8', 'Endesa resultados 1S 2026: beneficio +41%, 6,8% sobre el consenso | Guía 2026 al alza'),
                ('tcyjnI02z7Q', 'Endesa 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-24',
     'proximo_estimado': True,
     'fuentes': 'Endesa, resultados de los nueve meses de 2026 (presentación en la CNMV y nota de prensa en endesa.com, 28-oct-2026) y del primer '
                'semestre (29-jul-2026); El Español y El Conciso (28-oct-2026); Bolsamanía (precio, 28-oct-2026); stockanalysis.com (acciones y '
                'múltiplos históricos, oct-2026).',
     'fuentes_corto': 'El Español, El Conciso, Bolsamanía y stockanalysis.com',
     'elaborado': '28-oct-2026, 11:15'},
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
     'lede': 'Promotor y gestor de infraestructuras de transporte con sede en Países Bajos y cotización en Madrid y en el Nasdaq. Su valor se concentra '
             'en autopistas de peaje (407 ETR en Canadá y Managed Lanes en Estados Unidos); también construye (Budimex, Webber) y participa en la nueva '
             'Terminal Uno del JFK.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'EBITDA ajustado de 1.210 M€ hasta septiembre (+17,4%; +21,8% comparable) y de 464 M€ en el tercer trimestre (+23,4%, calculado), '
                'empujado por las tarifas de las autopistas de Norteamérica. El informe trimestral no publica beneficio neto: el resultado de '
                'explotación, 848 M€ (-12,2%, calculado), compara con unos 9M 2025 que incluían 274 M€ de desinversiones y deterioros.',
     'precio': '48,84 €',
     'precio_fecha': '27-oct-2026',
     'multiplos': [('PER 12 meses', '~59,8x'),
                   ('PER forward', '~46,7x'),
                   ('EV/EBITDA', '~22,7x'),
                   ('Precio / valor contable', '~4,82x'),
                   ('Rentab. dividendo', '~2,27%'),
                   ('FCF yield', '~5,3%'),
                   ('Capitalización', '~35.220 M€')],
     'multiplos_nota': 'Calculados con el cierre de 48,84 € del 27-oct-2026 (Bolsamanía) y los datos de 12 meses de stockanalysis.com (que a 43,50 €, el '
                       '20-oct-2026, daba PER 53,2x, EV/EBITDA 20,7x, precio / valor contable 4,29x y dividendo 2,56%). A cierre de 2023, 2024 y 2025 el '
                       'PER era 71,7x, 9,2x (plusvalías de Heathrow e IRB) y 44,8x, el EV/EBITDA 34,2x, 29,8x y 33,7x, el precio / valor contable 4,10x, '
                       '3,68x y 5,19x, y la rentabilidad por dividendo 2,35%, 2,08% y 2,05%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '7.402', '+7,1%'),
               ('EBITDA ajustado', '1.210', '+17,4%'),
               ('EBIT ajustado', '823', '+19,1%'),
               ('Resultado de explotación', '848', '-12,2%'),
               ('EBITDA ajustado 3T', '464', '+23,4%'),
               ('Dividendos de proyectos', '604', '+48,8%'),
               ('Caja neta sin proyectos (sep-26)', '1.660', '')],
     'kpi': 'Margen EBITDA 16,3% (14,9% en 9M 2025; calculado). Autopistas: ingreso medio por viaje en la 407 ETR +20,7% con tráfico -1,7% (-7,1% en el '
            '3T); ingreso por transacción +17,1% en NTE, +12,0% en LBJ, +15,6% en NTE 35W, +10,0% en I-66 y +11,0% en I-77. Construcción: margen EBIT '
            'ajustado 4,1% (3,7%), flujo operativo 591 M€ y cartera récord de 18.994 M€ (más 8.745 M€ preadjudicados). Dividendos de proyectos 604 M€ '
            '(315 de la 407 ETR). Caja neta sin proyectos de infraestructura 1.660 M€ (1.341 M€ en diciembre); liquidez 5.071 M€; deuda neta consolidada '
            '5.929 M€.',
     'guia': 'Sin guía numérica anual. Segundo dividendo flexible de 600 M€ (importe por acción el 3-nov-2026; ex-dividendo 5-nov; pago desde el '
             '10-dic). Recompra: 391 M€ ejecutados a 30-sep-2026, de un máximo de 800 M€ hasta el 3-mar-2027. La 407 ETR aprobó un dividendo de 1.050 M '
             'CAD para el 4T. JFK Terminal Uno: la fase A mantiene el objetivo del 31-mar-2027. Nuevas autopistas en EE. UU.: I-24 (Tennessee) e I-285 '
             'Este (Georgia).',
     'positivos': ['El EBITDA comparable creció un 21,8% y el del tercer trimestre un 23,4% (calculado), por las tarifas de las autopistas de '
                   'Norteamérica.',
                   'Los dividendos de proyectos subieron a 604 M€ y la 407 ETR aprobó otros 1.050 M CAD.',
                   'Construcción supera su objetivo de margen (4,1%) y la caja neta sube a 1.660 M€.'],
     'riesgos': ['El tráfico de la 407 ETR cayó un 7,1% en el tercer trimestre: el crecimiento depende de las tarifas.',
                 'La fase A de la nueva Terminal Uno del JFK sigue sin abrir y el bloqueo de dividendos del proyecto se alarga.',
                 'La I-24 prevé 7.700 M USD de pagos nominales a Tennessee en 2027-2033; el informe trimestral no incluye beneficio neto ni guía anual.'],
     'videos': [('a1PNLKZ-FWE', 'Ferrovial resultados 3T 2026: EBITDA comparable +21,8%, el del 3T +23,4% | Caja neta 1.660 M€'),
                ('TNX0A9PcJbg', 'Ferrovial 3T 2026 en 60 segundos (Short)'),
                ('_enk_ZzJWhE', 'Ferrovial resultados 1S 2026: EBITDA comparable +21,6%, beneficio -52% por las plusvalías de 2025'),
                ('jgro0LsOOGs', 'Ferrovial 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Ferrovial, resultados de los nueve primeros meses de 2026 (6-K a la SEC y nota de prensa, 27-oct-2026) y 6-K del segundo dividendo '
                'flexible (27-oct-2026); Bolsamanía y EFE (27-oct-2026); stockanalysis.com (datos de 12 meses y múltiplos históricos, oct-2026).',
     'fuentes_corto': 'Ferrovial (6-K), Bolsamanía, EFE y stockanalysis.com',
     'elaborado': '27-oct-2026, 23:20'},
    {'id': 'aena',
     'nombre': 'Aena',
     'ticker': 'AENA',
     'sector': 'Aeropuertos · tarifas reguladas y negocio comercial',
     'lede': 'Gestiona 46 aeropuertos y dos helipuertos en España, además de Londres-Luton, Leeds Bradford (vía Augusta) y 17 aeropuertos en Brasil, a '
             'los que suma Río de Janeiro-Galeão desde octubre de 2026. Sus tarifas aeroportuarias en España las fija el DORA; el negocio comercial '
             '(tiendas, restauración, aparcamientos, salas VIP) y el inmobiliario completan los ingresos.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 1.774,7 M€ hasta septiembre (+12,4%) y de 772,8 M€ en el tercer trimestre (+12,7%, calculado), con 309,9 M de '
                'pasajeros en el grupo (+4,1%). El margen EBITDA baja al 58,3% (60,2%) porque los gastos operativos crecen un 13,4%; la deuda financiera '
                'neta, 5.845 M€ (1,47x EBITDA), baja 879 M€ desde junio (calculado).',
     'precio': '26,50 €',
     'precio_fecha': '28-oct-2026',
     'multiplos': [('PER 12 meses', '~17,0x'),
                   ('PER forward', '16,6x'),
                   ('EV/EBITDA', '~11,5x'),
                   ('Precio / valor contable', '4,49x'),
                   ('Rentab. dividendo', '~4,11%'),
                   ('Capitalización', '~39.750 M€')],
     'multiplos_nota': 'Precio de 26,50 € el 28-oct-2026 hacia las 09:45 (Europa Press), tras los resultados; 1.500 M de acciones. PER, EV/EBITDA y '
                       'rentabilidad por dividendo calculados con el beneficio (2.332,0 M€) y el EBITDA (3.980,2 M€) de los 12 meses a septiembre y la '
                       'deuda financiera neta de 5.845 M€; PER forward y precio / valor contable, de stockanalysis.com al mismo precio. A cierre de '
                       '2023, 2024 y 2025 el PER era 15,1x, 15,3x y 16,7x, el EV/EBITDA 11,2x, 10,4x y 11,2x, el precio / valor contable 3,26x, 3,49x y '
                       '3,90x, y la rentabilidad por dividendo 5,19%, 5,31% y 4,74%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '5.283,9', '+10,4%'),
               ('Ingresos aeronáuticos', '2.781,3', '+8,8%'),
               ('Ingresos comerciales', '1.574,1', '+7,4%'),
               ('EBITDA', '3.077,9', '+6,8%'),
               ('Beneficio neto', '1.774,7', '+12,4%'),
               ('Beneficio neto 3T (calculado)', '772,8', '+12,7%'),
               ('BPA (calculado)', '~1,18 €', '+12,4%')],
     'kpi': 'Margen EBITDA 58,3% (60,2% en 9M 2025; 60,3% frente a 60,9% sin IFRIC 12 ni el seguro de Luton). Pasajeros: 257,2 M en España (+4,1%), 14,3 '
            'M en Luton (+6,2%), 3,7 M en Leeds Bradford (+2,9%) y ~34,8 M en Brasil (calculado). Comercial en España: salas VIP 197,8 M€ (+30,4%), '
            'aparcamientos 181,3 M€ (+9,8%), restauración 300,9 M€ (+7,5%), tiendas libres de impuestos 404,1 M€ (+0,6%); inmobiliario 108,6 M€ '
            '(+11,6%). Flujo de explotación 2.811,3 M€ (+11,3%); inversión 1.133,5 M€ (343,5 por Augusta); dividendos pagados 1.646,4 M€. Deuda '
            'financiera neta 5.845 M€ (5.509 en diciembre, 6.724 en junio), 1,47x EBITDA. Fitch: A+ desde el 7-oct-2026.',
     'guia': 'Sin guía nueva en el informe de 9M; en julio Aena elevó la previsión de tráfico en España para 2026 a ~+3% (hasta septiembre, +4,1%). '
             'Política de dividendo del 80% del beneficio; 1,09 € por acción con cargo a 2025; sin dividendo nuevo anunciado. Compra del 100% de Río de '
             'Janeiro-Galeão cerrada el 6-oct-2026 (257,2 M€ pagados; el resto, en el 4T). DORA III (2027-2031), aprobado el 15-sep-2026: tarifas +0,33% '
             'anual sobre 2026 e inversión de 12.888 M€ (9.991 M€ regulada).',
     'positivos': ['El beneficio crece un 12,4% hasta septiembre y un 12,7% en el tercer trimestre (calculado).',
                   'El tráfico en España (+4,1%) supera la previsión de Aena y el negocio comercial sigue creciendo: salas VIP +30,4% y aparcamientos '
                   '+9,8%.',
                   'La deuda neta baja 879 M€ desde junio, Fitch sube el rating a A+ y Aena suma Río de Janeiro-Galeão.'],
     'riesgos': ['El DORA III deja las tarifas casi congeladas (+0,33% anual) hasta 2031 con una inversión de 12.888 M€.',
                 'Los gastos operativos (+13,4%) crecen más que los ingresos y el margen EBITDA baja al 58,3%.',
                 'Las tiendas libres de impuestos apenas crecen (+0,6%) y los ingresos quedaron por debajo de la media de los analistas (Reuters).'],
     'videos': [('f8e-rA03fWM', 'Aena resultados 3T 2026: beneficio 1.774,7 M€ (+12,4%) y 309,9 M de pasajeros | Margen EBITDA 58,3%'),
                ('0Hfym0TlkbA', 'Aena 3T 2026 en 60 segundos (Short)'),
                ('QCBLXtjeo3o', 'Aena resultados 1S 2026: beneficio 1.002 M€ (+12,1%), algo por debajo del consenso | Deuda 6.724 M€'),
                ('SuVwEzW7h9I', 'Aena 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-24',
     'proximo_estimado': True,
     'fuentes': 'Aena, presentación de resultados e informe de gestión de los nueve primeros meses de 2026 y nota de prensa (CNMV y aena.es, '
                '28-oct-2026); nota de resultados 2025 (25-feb-2026); Europa Press, Reuters e Investing.com (28-oct-2026); Hosteltur (DORA III, '
                '15-sep-2026); stockanalysis.com (múltiplos, oct-2026).',
     'fuentes_corto': 'Aena (CNMV), Europa Press, Reuters, Investing.com y stockanalysis.com',
     'elaborado': '28-oct-2026, 11:21'},
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
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Ventas de 1.780 M€ hasta septiembre (+3,3%; +4% a tipo de cambio constante) y EBITDA ajustado de 428 M€ (+4,1%; +6% a tipo constante), '
                'con un margen del 24,1% (23,9%). En el tercer trimestre, el EBITDA ajustado subió un 10,3%, a 107 M€ (calculado). El beneficio neto '
                'contable bajó un 5,9%, a 154 M€, por la reestructuración; el ajustado subió a 221 M€ (+6% a tipo constante). Fluidra acota su guía '
                '2026.',
     'precio': '18,62 €',
     'precio_fecha': '29-oct-2026',
     'multiplos': [('PER 12 meses', '~21,3x'),
                   ('PER forward', '~13,2x'),
                   ('EV/EBITDA', '~11,6x'),
                   ('Precio / valor contable', '~2,16x'),
                   ('Rentab. dividendo', '~3,49%'),
                   ('Capitalización', '~3.539 M€')],
     'multiplos_nota': 'Calculados con 18,62 € (29-oct-2026, en sesión, fluidra.com), 190,06 M de acciones tras la amortización del 28-oct, el beneficio '
                       'neto de 12 meses de Fluidra (166 M€) y los datos de stockanalysis.com (PER forward, EV/EBITDA y valor contable, a 17,50 € y '
                       '18,12 €). A cierre de 2023, 2024 y 2025 el PER era 31,4x, 32,3x y 25,0x, el EV/EBITDA 14,7x, 15,8x y 13,7x, el precio / valor '
                       'contable 2,27x, 2,69x y 2,75x, y la rentabilidad por dividendo 3,09%, 2,64% y 2,84%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ventas', '1.780', '+3,3%'),
               ('EBITDA ajustado', '428', '+4,1%'),
               ('Beneficio neto ajustado', '221', '+3,8%'),
               ('Beneficio neto', '154', '-5,9%'),
               ('EBITDA ajustado 3T (calculado)', '107', '+10,3%'),
               ('Flujo de caja libre', '12', '6 en 9M25'),
               ('BPA ajustado', '1,15 €', '+3,6%')],
     'kpi': 'Margen EBITDA ajustado 24,1% (23,9%); 20,5% en el 3T (19,5%; calculado). Margen bruto 56,0% (56,1%); opex 32,0% de las ventas (32,3%); 23 '
            'M€ de ahorros del plan de eficiencia. Ventas a tipo constante y perímetro: Europa +4,2%, Norteamérica +3,5%, Resto del mundo +1,5%. Flujo '
            'de explotación 223 M€ (199), capex 57 M€ (46), flujo de caja libre 12 M€ (6); circulante / ventas 19,1% (20,0%). Deuda neta 1.145 M€ (1.034 '
            'M€ en sep-25), 2,2x el EBITDA ajustado (2,1x).',
     'guia': 'Guía 2026 acotada, a tipo de cambio constante: ventas +3,5% a +5,5% (antes +3% a +7%), margen EBITDA ajustado 23,3%-23,5% (antes '
             '23,3%-24,3%) y BPA ajustado +5% a +9% (antes +4% a +13%). Recompra de 40 M€ completada y 2.071.424 acciones amortizadas (1,1% del '
             'capital). Sin dividendo nuevo: queda pendiente el pago de 0,33 € brutos el 10-dic-2026 (ex-dividendo 8-dic), del dividendo de 0,65 € con '
             'cargo a 2025.',
     'positivos': ['El EBITDA ajustado del tercer trimestre creció un 10,3% y su margen subió un punto, al 20,5% (calculado); según Investing.com, '
                   'superó al consenso.',
                   'El margen EBITDA de los nueve meses mejora al 24,1%, con 23 M€ de ahorros del plan de eficiencia.',
                   'Recompra de 40 M€ completada y 1,1% del capital amortizado.'],
     'riesgos': ['La guía se acota: el margen anual queda en el 23,3%-23,5%, la parte baja del rango anterior.',
                 'La construcción de piscinas nuevas y las reformas siguen débiles, y el margen bruto del 3T bajó (Investing.com).',
                 'La deuda neta sube a 1.145 M€ (+111 M€ a/a) y la reestructuración (45 M€ con pagos en acciones) recorta el beneficio contable un '
                 '5,9%.'],
     'videos': [('9l1pAro0ayM', 'Fluidra resultados 3T 2026: EBITDA ajustado +6% a tipo constante, margen 24,1% | Acota la guía'),
                ('jhD-BfCiy_Y', 'Fluidra 3T 2026 en 60 segundos (Short)'),
                ('g6FVIzh99x4', 'Fluidra resultados 1S 2026: ventas +5% a tipo constante, EBITDA 321 M€ | Beneficio neto -7%'),
                ('zlALNKgx1Kg', 'Fluidra 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Fluidra, nota de prensa y medidas alternativas de rendimiento de los nueve primeros meses de 2026 (CNMV y fluidra.com, 29-oct-2026); '
                'Fluidra, resultados 1S 2026 (30-jul-2026); Europa Press/Bolsamanía (29-oct y 28-oct-2026) e Investing.com (29-oct-2026, consenso y '
                'margen bruto del 3T); stockanalysis.com (múltiplos, sep-oct 2026).',
     'fuentes_corto': 'Fluidra, Europa Press, Bolsamanía, Investing.com y stockanalysis.com',
     'elaborado': '29-oct-2026, 11:15'},
    {'id': 'naturgy',
     'nombre': 'Naturgy',
     'ticker': 'NTGY',
     'sector': 'Eléctricas y gas · redes, generación y comercialización',
     'lede': 'Grupo integrado de gas y electricidad con redes de distribución en España y Latinoamérica (México, Brasil, Chile, Argentina y Panamá), '
             'ciclos combinados, nuclear y renovables, gestión del aprovisionamiento de gas (con el contrato de Sonatrach y Medgaz) y comercialización. '
             'Las redes aportan ya más de la mitad del EBITDA.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 1.758 M€ hasta septiembre (+5,4%) y EBITDA de 4.380 M€ (+3,9%). Las redes de distribución suben un 12,8% y la '
                'comercialización cae un 29,4%. Naturgy eleva por segunda vez su guía de 2026 (EBITDA de más de 5.600 M€ y beneficio de alrededor de '
                '2.200 M€) y paga un segundo dividendo a cuenta de 0,60 € el 5 de noviembre.',
     'precio': '30,28 €',
     'precio_fecha': '29-oct-2026',
     'multiplos': [('PER 12 meses', '13,3x'),
                   ('PER con la guía 2026', '12,8x'),
                   ('EV/EBITDA', '7,7x'),
                   ('Precio / valor contable', '2,4x'),
                   ('Rentab. dividendo', '5,9%'),
                   ('Capitalización', '~28.060 M€')],
     'multiplos_nota': 'Calculados con el precio de 30,28 € del 29-oct-2026 a las 10:42 (Bolsamanía), 926,73 M de acciones (stockanalysis.com), '
                       'beneficio y EBITDA de 12 meses a septiembre (2.113 y 5.500 M€), deuda neta de 12.307 M€ más ~2.150 M€ de minoritarios '
                       '(implícitos en stockanalysis.com) y el dividendo de 1,80 € comprometido para 2026. A cierre de 2023, 2024 y 2025 el PER era '
                       '13,1x, 11,8x y 12,3x, el EV/EBITDA 7,9x, 7,6x y 8,1x y el precio / valor contable 2,17x, 1,93x y 2,19x (stockanalysis.com). La '
                       'acción subió un 14,9% en 52 semanas (stockanalysis.com, 27-oct-2026).',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Cifra de negocios', '15.374', '+5,4%'),
               ('EBITDA', '4.380', '+3,9%'),
               ('EBITDA de redes', '2.354', '+12,8%'),
               ('EBITDA de comercialización', '353', '-29,4%'),
               ('EBIT', '3.092', '+6,2%'),
               ('Beneficio neto', '1.758', '+5,4%'),
               ('Beneficio neto 3T (calculado)', '543', '+4,2%'),
               ('BPA (calculado)', '~1,90 €', '')],
     'kpi': 'Margen EBITDA 28,5% (28,9% en 9M 2025; calculado). Redes: España 1.285 M€ y Latinoamérica 1.080 M€ de EBITDA (calculado); electricidad '
            'España incluye 126 M€ de ajustes retroactivos no recurrentes. Gestión de la energía 676 M€ (-5,8%), generación térmica 601 M€ (+14,9%), '
            'renovable 466 M€ (+3,1%). Fondos generados 3.560 M€ (+7,8%); el circulante absorbió 968 M€, con el pago puntual a Sonatrach; flujo de caja '
            'libre tras minoritarios 1.077 M€ (-49,9%); inversión 1.280 M€ (-7,8%). Deuda neta 12.307 M€ (12.317 M€ en diciembre y 11.745 M€ en junio), '
            '2,2x EBITDA; coste medio 4,0%; liquidez 10.378 M€. Capacidad renovable 8.558 MW (+9,4%).',
     'guia': 'Guía 2026 elevada por segunda vez: EBITDA de más de 5.600 M€ (antes, más de 5.500) y beneficio neto de alrededor de 2.200 M€ (antes, más '
             'de 2.100); los nueve meses ya suman el 78% y el 80% (calculado). Deuda neta por debajo de 13.000 M€ a cierre. Dividendo 2026 de 1,80 € por '
             'acción confirmado: 0,60 € pagados el 29-jul y un segundo dividendo a cuenta de 0,60 € que se paga el 5-nov-2026. Según la prensa, '
             'capacidad de hasta 12.000 M€ para operaciones corporativas sin perder el rating BBB y plan estratégico a 2030 el próximo año.',
     'positivos': ['Eleva su guía por segunda vez en el año y ya lleva el 80% del beneficio previsto (calculado).',
                   'Las redes crecen un 12,8% y ya son el 54% del EBITDA (calculado).',
                   'El tercer trimestre también mejora: beneficio +4,2% y ventas +14,1% (calculado).'],
     'riesgos': ['La comercialización cae un 29,4% y la gestión de la energía un 5,8%.',
                 '126 M€ del EBITDA de las redes eléctricas en España son ajustes que no se repetirán.',
                 'El flujo de caja libre tras minoritarios baja un 49,9% y la deuda neta sube 562 M€ desde junio.'],
     'videos': [('Jd0pBVYB4XI', 'Naturgy resultados 3T 2026: beneficio +5,4% y guía 2026 elevada otra vez | Redes +12,8%'),
                ('CF3v-pP5o-k', 'Naturgy 3T 2026 en 60 segundos (Short)'),
                ('5YX26YWgemU', 'Naturgy resultados 1S 2026: beneficio +5,9%, por encima del consenso | Redes +13,2% y guía al alza'),
                ('WBGXyA-ix64', 'Naturgy 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-18',
     'proximo_estimado': True,
     'fuentes': 'Naturgy, informe de resultados de los nueve primeros meses de 2026 (CNMV y naturgy.com, 29-oct-2026) e informe del primer semestre '
                '(22-jul-2026); El Español, Europa Press y Vozpópuli (29-oct-2026); The Objective (resultados 2025); Bolsamanía (precio, 29-oct-2026); '
                'stockanalysis.com (acciones y múltiplos históricos, oct-2026).',
     'fuentes_corto': 'El Español, Europa Press, Vozpópuli, Bolsamanía y stockanalysis.com',
     'elaborado': '29-oct-2026, 11:30'},
    {'id': 'mapfre',
     'nombre': 'Mapfre',
     'ticker': 'MAP',
     'sector': 'Seguros',
     'lede': 'Mayor aseguradora española, con negocio en Iberia (España y Portugal), Brasil y el resto de Latinoamérica, Norteamérica, EMEA y el '
             'reaseguro de MAPFRE RE. En una aseguradora, los ingresos se miden con las primas y la rentabilidad técnica con el ratio combinado No Vida '
             '(siniestros y gastos sobre primas; por debajo del 100%, el seguro gana dinero); la fortaleza del balance, con el ratio de Solvencia II.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 924,3 M€ hasta septiembre (+11,5%) con primas de 22.827 M€ (+2,0%). En el 3T ganó unos 300 M€ (calculado) pese al '
                'terremoto de Colombia (83 M€ netos), que llevó el ratio combinado No Vida del trimestre al 95,0% y el de los nueve meses al 93,5% (+0,9 '
                'pp). Dividendo a cuenta de 0,08 € (+14,3%), que se paga el 26-nov-2026. Para Capital Madrid cumplió con el consenso y para '
                'Investing.com quedó ligeramente por debajo; la acción caía un 3,2% a media mañana del 28-oct-2026 (Bolsarama).',
     'precio': '4,196 €',
     'precio_fecha': '28-oct-2026, 10:44',
     'multiplos': [('PER 12 meses', '~11,0x'),
                   ('PER forward', '~10,0x'),
                   ('Precio / valor en libros', '~1,16x'),
                   ('Rentab. dividendo', '~4,5%'),
                   ('Capitalización', '~12.880 M€')],
     'multiplos_nota': 'Con precio de 4,196 € el 28-oct-2026 a las 10:44 (Bolsarama) y 3.070 M de acciones (stockanalysis.com). PER con el beneficio de '
                       '12 meses a septiembre (1.174 M€: 1.079 de 2025 - 829,0 de 9M25 + 924,3 de 9M26); PER forward y precio / valor en libros de '
                       'stockanalysis (10,37x y 1,20x a 4,352 €) ajustados al precio; sobre los fondos propios atribuidos de 9.445 M€ el precio / valor '
                       'en libros sería ~1,36x. Rentabilidad por dividendo con lo pagado en 2026 (0,19 €). Todo calculado. A cierre de 2022, 2023, 2024 '
                       'y 2025 el PER era 9,8x, 8,8x, 7,8x y 11,6x, el precio / valor en libros 0,62x, 0,62x, 0,75x y 1,25x, y la rentabilidad por '
                       'dividendo 9,5%, 8,6%, 7,0% y 4,3%. En una aseguradora no se usan EV/EBITDA ni flujo de caja libre.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Primas', '22.827', '+2,0%'),
               ('Primas No Vida', '17.493', '+1,1%'),
               ('Primas Vida', '5.333', '+5,0%'),
               ('Ingresos totales', '27.240', '+3,0%'),
               ('Ratio combinado No Vida', '93,5%', '+0,9 pp'),
               ('Beneficio neto', '924,3', '+11,5%'),
               ('Beneficio neto 3T (calculado)', '~300', '~+16%'),
               ('BPA (calculado)', '~0,30 €', '+11,5%')],
     'kpi': 'ROE 12,8% (+0,4 pp). Fondos propios 9.445 M€ (+5,4% en el año). Solvencia II 208,8% (último dato, a 30-jun-2026; rango objetivo 175%-225%). '
            'Activos gestionados 70.933 M€ (+9,6% en el año). Beneficio por unidad: Iberia 413,2 M€ (+19,0%; ratio combinado 94,2%), MAPFRE RE 286,2 M€ '
            '(+11,8%; 95,3%), Brasil 203,2 M€ (+2,0%; 75,7%), Norteamérica 111,6 M€ (+12,4%; 94,9%), Otros LATAM 100,2 M€ (-28,8%; 101,0%), EMEA -2,4 M€ '
            '(107,3%). Dividendo a cuenta de 2026: 0,08 € brutos por acción (+14,3%); ex-dividendo 24-nov-2026, pago 26-nov-2026; pagado en 2026: 0,19 € '
            '(+15,2%).',
     'guia': 'Objetivos 2026 (Junta General, 13-mar-2026): ROE por encima del 13% y ratio combinado del 93%-94%; hasta septiembre, 12,8% y 93,5%. Para '
             'igualar el beneficio de 2025 (1.079 M€) le bastan ~155 M€ en el 4T (calculado). Compra de Safety Insurance (EE. UU.): según lo previsto '
             '(presentación 9M26), pendiente de la junta de Safety y de los reguladores; cierre estimado en el 1T27 y posibles emisiones de deuda Tier 2 '
             'y senior en el 4T26 o el 1T27.',
     'positivos': ['Beneficio +11,5% pese a los 83 M€ del terremoto de Colombia.',
                   'Iberia (+19,0%) y Norteamérica (+12,4%) ganan más y mejoran su ratio combinado.',
                   'Dividendo a cuenta +14,3% (0,08 €) y ROE al alza, hasta el 12,8%.'],
     'riesgos': ['Ratio combinado del 3T al 95,0% (91,4% en el 3T25) y primas solo +2,0% (+0,7% sin divisas).',
                 'Otros LATAM cae un 28,8% y EMEA sigue en pérdidas (ratio combinado 107,3%).',
                 'Safety traerá más deuda y menos solvencia; la acción caía un 3,2% el día de los resultados.'],
     'videos': [('voydWhRZs2o', 'Mapfre resultados 3T 2026: beneficio 924 M€ (+11,5%) y dividendo a cuenta +14,3% | Sismo en Colombia'),
                ('mz0EHkNGquU', 'Mapfre 3T 2026 en 60 segundos (Short)'),
                ('gNyZYk8oDnM', 'Mapfre resultados 1S 2026: beneficio 624 M€ (+9,4%) y ratio combinado 92,8% | Primas +1,1%; Safety'),
                ('AJZm7q7mTpo', 'Mapfre 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-11',
     'proximo_estimado': True,
     'fuentes': 'Mapfre, informe de actividad, presentación a inversores e información sobre el dividendo a cuenta 2026 de los nueve primeros meses '
                '(CNMV, 28-oct-2026, 07:18-07:23; mapfre.com); Mapfre, resultados 2025 (feb-2026), 9M 2025 (oct-2025) y 1S 2026 (23-jul-2026); Junta '
                'General (13-mar-2026); El Debate, El Español, Capital Madrid e Investing.com (28-oct-2026); Bolsarama (precio, 28-oct-2026); '
                'stockanalysis.com (múltiplos, oct-2026).',
     'fuentes_corto': 'El Debate, El Español, Capital Madrid, Investing.com, Bolsarama y stockanalysis.com',
     'elaborado': '28-oct-2026, 11:16'},
    {'id': 'iag',
     'nombre': 'IAG',
     'ticker': 'IAG',
     'sector': 'Aerolíneas',
     'lede': 'International Airlines Group es el grupo de British Airways, Iberia, Vueling, Aer Lingus y LEVEL, además de IAG Loyalty (Avios) e IAG '
             'Cargo. Cotiza en Madrid (IBEX 35) y Londres. En una aerolínea pesan la capacidad (AKO), la ocupación, el ingreso por asiento-kilómetro y '
             'el combustible.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve meses de 2026 (enero-septiembre)',
     'titular': 'Beneficio neto de 2.264 M€ hasta septiembre (-16,2%) por el encarecimiento del combustible (+30,4% en el 3T). Ingresos récord en el 3T '
                '(9.744 M€, +4,5%), aunque el beneficio operativo del trimestre (1.726 M€, -15,9%) quedó por debajo del consenso. La deuda neta baja a '
                '4.220 M€ (0,6x EBITDA) y IAG pagará el 7 de diciembre un dividendo a cuenta de 0,053 € brutos por acción (+10%).',
     'precio': '5,192 €',
     'precio_fecha': '6-nov-2026, 17:35 (cierre)',
     'multiplos': [('PER 12 meses', '~8,0x'),
                   ('EV/EBITDA', '~3,5x'),
                   ('Rentab. dividendo', '~1,98%'),
                   ('Recompra / capitalización', '~6,6%'),
                   ('Capitalización', '~22.800 M€')],
     'multiplos_nota': 'Con precio de 5,192 € al cierre del BME el 6-nov-2026 (Bolsamanía); múltiplos calculados con ~4.400 M de acciones '
                       '(stockanalysis.com) y datos de 12 meses de IAG: BPA básico 64,7 céntimos (71,3 de 2025 + 50,6 de 9M26 - 57,2 de 9M25), valor '
                       'empresa ~27.100 M€ con la deuda neta de septiembre (4.220 M€) y el EBITDA antes de excepcionales de 12 meses a junio (7.640 M€, '
                       'último publicado), y dividendos anunciados en 12 meses de 0,103 € (0,05 € complementario de 2025 y 0,053 € a cuenta de 2026). A '
                       'cierre de 2023, 2024 y 2025 (stockanalysis, cotización de Londres) el PER era 3,3x, 6,5x y 6,5x, el EV/EBITDA 4,4x, 4,9x y 4,6x, '
                       'y la rentabilidad por dividendo -, 2,54% y 2,08%. La recompra en curso (1.500 M€) equivale a ~6,6% de la capitalización.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '25.808', '+2,3%'),
               ('Ingresos 3T', '9.744', '+4,5%'),
               ('Ingresos de pasaje', '22.662', '+2,9%'),
               ('Beneficio operativo antes de excepcionales', '3.483', '-11,4%'),
               ('Beneficio operativo 3T antes de excepcionales', '1.726', '-15,9%'),
               ('Beneficio neto', '2.264', '-16,2%'),
               ('Beneficio neto 3T', '1.231', '-12,2%'),
               ('BPA básico', '50,6 cts', '-11,5% (calculado)'),
               ('Deuda neta (30-sep-2026)', '4.220', '-472 vs junio (calculado)')],
     'kpi': 'Margen operativo antes de excepcionales 13,5% (15,6%); 3T 17,7% (22,0%). Capacidad (AKO) -0,2%, ocupación 86,1% (+0,3 pp), 92,6 M de '
            'pasajeros (+0,2%). Ingreso de pasaje por AKO 3T +4,1% (Atlántico Norte +11%); 9M +3,0%. Combustible y emisiones 3T 2.444 M€ (+30,4%), 9M '
            '6.400 M€ (+18,6%); coste unitario sin combustible 3T +3,4% (interrupciones del control aéreo), 9M +0,3%. Beneficio operativo de 9M por '
            'aerolínea: British Airways 1.493 M£ (-144), Iberia 978 M€ (-96), Vueling 303 M€ (-64), Aer Lingus 108 M€ (-142), IAG Loyalty 391 M£ (+59). '
            'Excepcionales del 1S de 149 M€ (sin excepcionales en el 3T). Deuda neta 4.220 M€ (-1.728 M€ vs diciembre, calculado), 0,6x EBITDA; liquidez '
            '12.490 M€. El 3T quedó por debajo del consenso recopilado por IAG (~1.810 M€; -4,6%, calculado).',
     'guia': 'Guía 2026: margen operativo antes de excepcionales de al menos el 12% (se mantiene); capacidad algo menor que en 2025 (plana en julio; '
             '~+3% en febrero); combustible ~8.900 M€ (8.300-8.600 M€ en julio); coste unitario sin combustible ~+1% (plano en julio); inversión 3.100 '
             'M€ (3.400 M€) con 12 entregas de aviones (16); 85% de las reservas del 4T aseguradas y 45% del combustible de 2027 cubierto. Dividendo a '
             'cuenta de 2026: 0,053 € brutos por acción (+10%; 0,048 € en 2025), fecha ex-dividendo 3-dic-2026, registro 4-dic y pago desde el '
             '7-dic-2026. Recompra de 1.500 M€: arranca el último tramo, de 500 M€, que terminará en febrero de 2027.',
     'positivos': ['Ingresos récord en el 3T (9.744 M€, +4,5%), con el ingreso de pasaje por AKO un 4,1% arriba y el Atlántico Norte un 11%.',
                   'La deuda neta sigue bajando, hasta 4.220 M€ (0,6x EBITDA), con una liquidez de 12.490 M€.',
                   'El dividendo a cuenta sube un 10% y empieza el último tramo de la recompra de 1.500 M€.'],
     'riesgos': ['El combustible sube un 30,4% en el 3T y la factura prevista para 2026 pasa a ~8.900 M€.',
                 'El coste unitario sin combustible sube un 3,4% en el 3T por las interrupciones del control aéreo, y el beneficio operativo del '
                 'trimestre quedó por debajo del consenso.',
                 'Europa se complica por la competencia: Vueling y Aer Lingus ganan menos y la capacidad de 2026 será algo menor que la de 2025.'],
     'videos': [('yYKwjQjEcJs', 'IAG resultados 3T 2026: beneficio 2.264 M€ (-16,2%) por el combustible | Dividendo a cuenta +10%'),
                ('OMG3liN3o6M', 'IAG 3T 2026 en 60 segundos (Short)'),
                ('ShNA56tU4sY', 'IAG resultados 1S 2026: beneficio 1.033 M€ (-20,6%) por el combustible | Deuda neta -1.256 M€'),
                ('sDSWqb5VGVs', 'IAG 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-26',
     'proximo_estimado': True,
     'fuentes': 'IAG, informe de gestión intermedio de 9M 2026 y presentación (6-nov-2026, CNMV) y dividendo a cuenta (CNMV, 5-nov-2026), según Europa '
                'Press, Aviacionline, Hosteltur, Fly News, The Officer, El Español, Actualidad Aeroespacial y Alliance News/MarketScreener (6-nov-2026); '
                'fechas del dividendo: RNS (Investegate), Finect y Bolsamanía; IAG, informe 1S 2026 y resultados 2025; XTB (consenso); Bolsamanía '
                '(precio, 6-nov-2026); stockanalysis.com (acciones y múltiplos históricos).',
     'fuentes_corto': 'Europa Press, Aviacionline, Hosteltur, Fly News, Alliance News, XTB, Bolsamanía y stockanalysis.com',
     'elaborado': '6-nov-2026, 23:45'},
    {'id': 'acerinox',
     'nombre': 'Acerinox',
     'ticker': 'ACX',
     'sector': 'Siderurgia',
     'lede': 'Fabricante de acero inoxidable (Acerinox Europa en Algeciras, North American Stainless en EE. UU. y Columbus en Sudáfrica) y de aleaciones '
             'de alto rendimiento (VDM Metals y Haynes International). En el acero pesan las toneladas, el precio frente al coste de las materias primas '
             '(níquel, chatarra), la energía y el capital circulante.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 162 M€ hasta septiembre, frente a 7 M€ en los nueve meses de 2025 (x23); EBITDA de 470 M€ (+46%). El EBITDA del 3T, '
                '199 M€ (+13% frente al 2T), superó en un 8% la previsión de los analistas recogida por Investing.com (184 M€). Pero el circulante '
                'absorbió 152 M€ en el trimestre, la deuda neta subió a 1.535 M€ y Acerinox espera un 4T con menos EBITDA.',
     'precio': '16,65 €',
     'precio_fecha': '30-oct-2026, 10:45',
     'multiplos': [('PER 12 meses', '~36x'),
                   ('EV/EBITDA', '~11,3x'),
                   ('Precio / valor contable', '~1,94x'),
                   ('Rentab. dividendo', '~3,72%'),
                   ('Capitalización', '~4.150 M€')],
     'multiplos_nota': 'Con precio de 16,65 € en el BME el 30-oct-2026 a las 10:45 (Bolsarama); múltiplos calculados con 249,3 M de acciones y datos de '
                       '12 meses a septiembre de Acerinox (beneficio neto 115 M€, EBITDA 503 M€, deuda neta 1.535 M€, patrimonio neto de junio 2.140 M€, '
                       'dividendo 0,62 €). El PER sigue alto porque el beneficio de 12 meses incluye la pérdida del 4T 2025. A cierre de 2023, 2024 y '
                       '2025 (stockanalysis.com, datos S&P Global) el PER era 11,6x, 10,5x y - (pérdidas), el EV/EBITDA 4,3x, 7,8x y 12,8x, la '
                       'rentabilidad por dividendo 6,66%, 7,13% y 5,07%, y el precio / valor contable 1,08x, 0,92x y 1,50x.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ventas', '4.556', '+1,9% (calculado)'),
               ('EBITDA', '470', '+46,4% (calculado)'),
               ('EBITDA 3T', '199', '+84% a/a; +13% vs 2T (calculado)'),
               ('EBITDA acero inoxidable', '411', '+88% (calculado)'),
               ('EBITDA aleaciones de alto rendimiento', '59', '-43% (calculado)'),
               ('Beneficio neto', '162', '7 en 9M 2025'),
               ('Deuda financiera neta (sep-26)', '1.535', '+174 vs junio')],
     'kpi': 'Margen EBITDA 10,3% (7,2%; calculado); 3T 12,5% (7,6%). Resultado de explotación 315 M€ (+79%). Beneficio del 3T 85 M€ (25 M€ en el 3T '
            '2025); BPA de 9M ~0,65 € (calculado). Producción de acería 1,53 Mt (+4,9%); 3T 501.000 t (+11% a/a, -7% frente al 2T). Ventas: inoxidable '
            '3.479 M€ (+9,9%), aleaciones 1.096 M€ (-17,1%). Inoxidable con margen EBITDA del 14% en el 3T. EE. UU.: demanda +6% frente al 2T e '
            'importaciones -18%; Europa: demanda -22% frente al 2T e importaciones -42%. Oriente Medio restó 16 M€ en el 3T (24 M€ en 9M) por energía y '
            'transporte. Flujo operativo del 3T -16 M€ tras 152 M€ de circulante; inversiones 80 M€ y flujo libre -96 M€ (Investing.com; calculado); '
            'dividendo pagado en el 3T 77 M€. Deuda neta 1.535 M€ (+346 M€ desde diciembre, calculado), ~3,1x el EBITDA de 12 meses (calculado).',
     'guia': 'Acerinox espera un EBITDA del 4T inferior al del 3T (199 M€), con menos volumen de inoxidable en EE. UU. por la estacionalidad de fin de '
             'año. En aleaciones, aeroespacial, turbinas y nuclear estables y señales de recuperación en petróleo, gas y química. Prevé reducir el '
             'circulante y bajar la deuda neta a final de año. Dividendo: 0,62 € por acción con cargo a 2025 (0,31 € en enero y 0,31 € el 17 de julio de '
             '2026); no se ha anunciado un dividendo nuevo con los resultados del 3T.',
     'positivos': ['El beneficio se multiplica por 23 y el EBITDA del 3T supera en un 8% la previsión de los analistas (Investing.com; calculado).',
                   'El acero inoxidable sigue mejorando: EBITDA +88% en nueve meses y margen del 14% en el 3T, con EE. UU. como motor.',
                   'En Europa, las importaciones de producto plano caen un 42%.'],
     'riesgos': ['El flujo de caja libre vuelve a ser negativo y la deuda neta sube hasta 1.535 M€.',
                 'La empresa espera un 4T con menos EBITDA y la demanda europea sigue débil (-22% frente al 2T).',
                 'Las aleaciones de alto rendimiento ganan un 43% menos y el conflicto de Oriente Medio encarece la energía y el transporte.'],
     'videos': [('kIKdmLvcuKM', 'Acerinox resultados 3T 2026: gana 162 M€ (x23) | EBITDA 3T 199 M€, un 8% sobre lo previsto'),
                ('LqVHIUNhiC8', 'Acerinox 3T 2026 en 60 segundos (Short)'),
                ('IuxWhvplVuQ', 'Acerinox resultados 1S 2026: vuelve a beneficios con 77 M€ | EBITDA 2T 176 M€, +85% trimestral'),
                ('9rnH1TvvMdw', 'Acerinox 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-26',
     'proximo_estimado': True,
     'fuentes': 'Acerinox, presentación de resultados del 3T 2026 (30-oct-2026), informe de gestión intermedio 1S 2026 (24-jul-2026), resultados 2025 '
                '(27-feb-2026) y nota del 3T 2025; Europa Press (vía Forbes, Demócrata y OKDiario) y El Conciso (30-oct-2026); Investing.com (previsión '
                'de los analistas, flujo de caja e inversiones, 30-oct-2026); Bolsarama (precio, 30-oct-2026); stockanalysis.com (múltiplos históricos).',
     'fuentes_corto': 'Europa Press, El Conciso, Investing.com, Bolsarama y stockanalysis.com',
     'elaborado': '30-oct-2026, 11:30'},
    {'id': 'grifols',
     'nombre': 'Grifols',
     'ticker': 'GRF',
     'sector': 'Farmacia y salud · hemoderivados (plasma)',
     'lede': 'Compañía de medicamentos derivados del plasma (Biopharma: inmunoglobulinas, albúmina, alfa-1 y proteínas especiales), con más de 400 '
             'centros de donación, además de diagnóstico (Diagnostic) y Bio Supplies. En el plasma pesan el coste de obtener la materia prima, la mezcla '
             'de productos, el dólar y la deuda. El IBEX 35 incluye la clase A (GRF); la clase B (GRF.P) no tiene voto y cobra un dividendo preferente.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 390 M€ hasta septiembre (+28,4%; +20,2% sin extraordinarios). Ingresos de 5.614 M€ (+4,6% a tipo constante) y un 3T '
                'que acelera: ventas +8,4% a tipo constante y margen EBITDA ajustado del 26,4%. El apalancamiento baja a 3,98x (4,2x hace un año), la '
                'guía 2026 se confirma y Grifols pagará el 4 de diciembre un dividendo a cuenta de 0,15 € por acción.',
     'precio': '11,000 € (clase A)',
     'precio_fecha': '2-nov-2026, 17:35 (cierre)',
     'multiplos': [('PER 12 meses', '~15,3x'),
                   ('EV/EBITDA', '~10,4x'),
                   ('Precio / valor contable', '~0,78x'),
                   ('Rentab. dividendo', '~2,11%'),
                   ('Capitalización', '~6.410 M€')],
     'multiplos_nota': 'Con precio de la clase A de 11,000 € al cierre del BME el 2-nov-2026 (Bolsarama); múltiplos calculados con datos de 12 meses a '
                       'septiembre: BPA 0,72 € (beneficio de 488 M€ y 680,6 M de acciones), dividendos anunciados en 12 meses de 0,2324 € por acción A '
                       '(0,0824 € el 2-jul-2026 y 0,15 € el 4-dic-2026). Capitalización con 422,4 M de acciones A y 258,2 M de acciones B a 6,83 € '
                       '(TradingView, sin fecha). Valor empresa ~17.600 M€ con la deuda neta de balance (8.753 M€) y los minoritarios (2.455 M€); EBITDA '
                       'reportado de 12 meses de Grifols (1.692 M€); con el EBITDA ajustado de 12 meses (1.859 M€), ~9,5x. Precio / valor contable sobre '
                       'el patrimonio neto total a septiembre (8.243 M€). A cierre de 2023, 2024 y 2025 (stockanalysis.com, datos S&P Global) el PER era '
                       '219,8x, 36,2x y 16,3x, el EV/EBITDA 19,1x, 10,8x y 10,5x, el precio / valor contable 1,23x, 0,66x y 0,86x, y la rentabilidad por '
                       'dividendo 0%, 0% y 2,19% (calculada).',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '5.614', '+1,3% (+4,6% a tipo constante)'),
               ('Ingresos 3T', '2.040', '+9,4% (+8,4% a tipo constante)'),
               ('Biopharma', '4.951', '+3,7% (+7,1% a tipo constante)'),
               ('Diagnostic', '431', '-10,0% (-7,0% a tipo constante)'),
               ('EBITDA ajustado', '1.392', '+2,5% (+5,0% a tipo constante)'),
               ('Beneficio neto', '390', '+28,4%'),
               ('Beneficio neto 3T', '162', '+27,9%'),
               ('Flujo de caja libre antes de M&A', '298', '188 en 9M 2025'),
               ('Deuda financiera neta (contrato de crédito, sep-26)', '7.706', '-92 vs junio (calculado)')],
     'kpi': 'Margen EBITDA ajustado 24,8% (24,5%); 3T 26,4% (25,8%). Margen bruto 38,0% (39,2%); 3T 39,6% (39,3%). Biopharma por franquicia (tipo '
            'constante): inmunoglobulinas +11,3% en el 3T y +12,3% en 9M (subcutáneas +40,3% y +25,6%), albúmina -13,2% y -13,9% (China), alfa-1 y '
            'proteínas especiales +18,2% y +4,6%. EE. UU. y Canadá +17,3% en el 3T. Diagnostic sin el negocio conjunto con QuidelOrtho: +2,3% en 9M. BPA '
            'de 9M ~0,57 € (calculado). Flujo libre antes de M&A del 3T 208 M€ (203). Deuda neta 7.706 M€ según el contrato de crédito (8.753 M€ en '
            'balance), 3,98x EBITDA según Grifols; liquidez 2.140 M€; sin vencimientos relevantes hasta el 4T 2028. Egipto: 18 centros (20 en el 1T '
            '2027) y ~1 millón de litros en 2026; Canadá: recogida reanudándose por fases tras la pausa de agosto. Grifols no publica el coste por '
            'litro.',
     'guia': 'Guía 2026 confirmada: EBITDA ajustado +5% a +9% a tipo constante (9M: +5,0%), margen de al menos el 25% (9M: 24,8%) y flujo de caja libre '
             'antes de M&A y dividendos de 500-575 M€ (9M: 298 M€, el 52-60%; calculado). Grifols prevé un 4T más moderado en Biopharma y que se '
             'reviertan efectos de calendario favorables en la caja. Objetivo fijado en febrero: apalancamiento de 3,5x o menos a finales de 2027. '
             'Dividendo a cuenta de 2026: 0,15 € brutos por acción (clase A y clase B), pago el 4 de diciembre de 2026 (el anuncio no indica la fecha '
             'ex-dividendo).',
     'positivos': ['El beneficio neto sube un 28,4%, hasta 390 M€, y el 3T acelera: ventas +8,4% a tipo constante y margen EBITDA ajustado del 26,4%.',
                   'Las inmunoglobulinas crecen un 11,3% en el 3T (subcutáneas +40,3%) y alfa-1 vuelve a crecer (+18,2%).',
                   'El apalancamiento baja a 3,98x y Grifols anuncia un dividendo a cuenta de 0,15 € por acción.'],
     'riesgos': ['La albúmina cae un 13,9% en nueve meses por China; Grifols cree que podría estabilizarse en 2027.',
                 'El margen EBITDA ajustado de 9M (24,8%) está por debajo del objetivo del 25% y la empresa prevé un 4T más moderado.',
                 'La deuda neta sigue en 7.706 M€ y parte de los efectos que ayudaron a la caja se revertirán en el 4T.'],
     'videos': [('HHl1NHMI-RU', 'Grifols resultados 3T 2026: gana 390 M€ (+28,4%) | Deuda por debajo de 4x y dividendo de 0,15 €'),
                ('Ufii2j9Isho', 'Grifols 3T 2026 en 60 segundos (Short)'),
                ('ZmBOEO1agsY', 'Grifols resultados 1S 2026: beneficio +28,7%, hasta 227 M€ | Inmunoglobulinas +12,8%, deuda en 4,2x'),
                ('xrWR9VfrbhY', 'Grifols 1S 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-26',
     'proximo_estimado': True,
     'fuentes': 'Grifols, nota de prensa y presentación de resultados del 3T 2026 (2-nov-2026, CNMV), dividendo a cuenta (otra información relevante, '
                'CNMV/SEC, 2-nov-2026), resultados del 1S 2026 (28-jul-2026) y de 2025 (26-feb-2026); Redacción Médica, El Español y Ara (2-nov-2026); '
                'Investing.com y MarketBeat (presentación y conferencia, 2-nov-2026); Bolsarama (precio, 2-nov-2026); TradingView (precio de la clase '
                'B); stockanalysis.com (múltiplos históricos).',
     'fuentes_corto': 'Redacción Médica, El Español, Investing.com, MarketBeat, Bolsarama y stockanalysis.com',
     'elaborado': '2-nov-2026, 23:30'},
    {'id': 'indra',
     'nombre': 'Indra',
     'ticker': 'IDR',
     'sector': 'Defensa / tecnología',
     'lede': 'Grupo español de defensa, espacio, tráfico aéreo, movilidad y tecnologías de la información (Minsait). Desde 2025-2026 ha integrado TESS '
             'Defence, Hispasat e Hisdesat, y gestiona buena parte de los Programas Especiales de Modernización del Ministerio de Defensa.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 355 M€ hasta septiembre (+22,0%) y de 136 M€ en el tercer trimestre (+77,8%), con ingresos de 4.645 M€ (+28,6%; +16% '
                'orgánico) y una cartera récord de 22.165 M€ (+133%). La caja neta de 1.192 M€ y el flujo libre de 1.692 M€ se deben a los anticipos de '
                'los programas de Defensa; sin ellos, flujo libre de 70 M€.',
     'precio': '64,45 €',
     'precio_fecha': '30-oct-2026',
     'multiplos': [('PER 12 meses', '~22,7x'),
                   ('EV/EBITDA', '~11,7x'),
                   ('EV/EBITDA sin anticipos PEM', '~13,5x'),
                   ('Precio / valor contable', '~5,41x'),
                   ('Rentab. dividendo', '~0,47%'),
                   ('Capitalización', '~11.295 M€')],
     'multiplos_nota': 'Calculados con 64,45 € (30-oct-2026 por la mañana, Investing.com; cierre del 29-oct: 65,40 €, Bolsamanía) y datos de 12 meses de '
                       'Indra (2025 + 9M26 - 9M25: BPA 2,84 €, EBITDA 888 M€); EV con caja neta de 1.192 M€ y 298 M€ de minoritarios. A cierre de 2023, '
                       '2024 y 2025 (stockanalysis.com) el PER era 12,0x, 10,9x y 19,6x, el EV/EBITDA 7,2x, 6,5x y 15,5x (con el EBITDA de '
                       'stockanalysis), el precio / valor contable 2,17x, 2,29x y 4,28x, y la rentabilidad por dividendo 1,82%, 1,48% y 0,62%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '4.645', '+28,6%'),
               ('EBITDA', '657', '+62,1%'),
               ('EBIT', '454', '+42,4%'),
               ('Beneficio neto', '355', '+22,0%'),
               ('Beneficio neto 3T', '136', '+77,8%'),
               ('Cartera (sep-26)', '22.165', '+133,0%'),
               ('Caja neta (sep-26)', '1.192', '')],
     'kpi': 'Margen EBITDA 14,2% (11,2% en 9M 2025) y margen EBIT 9,8% (8,8%). Defensa: ingresos 1.408 M€ (+100,3%), margen EBITDA 19,5% (21,3%); '
            'Espacio 286 M€ (+372,5%, margen EBITDA 40,0%); Tráfico Aéreo 446 M€ (+22,8%); Movilidad 264 M€ (+2,3%); Minsait 2.240 M€ (+0,6%; -3,5% en '
            'el 3T por la venta de BPO). Contratación 8.085 M€ (+81,7%; 3T +139%, con 1.926 M€ de IRIS²). BPA básico 2,02 € (1,66 €). Flujo libre 1.692 '
            'M€ (70 M€ sin anticipos PEM); anticipos PEM en balance 2.118 M€; caja neta 1.192 M€ (deuda neta de 583 M€ en diciembre; 431 M€ sin '
            'anticipos).',
     'guia': 'Guía 2026 confirmada: ingresos en moneda local de más de 7.000 M€, EBIT reportado de más de 700 M€ (sin la plusvalía de BPO) y flujo libre '
             'de más de 375 M€ (sin anticipos PEM, factoring constante). Para cumplirla, el 4T necesita unos 2.355 M€ de ingresos (+28%) y más de 253 M€ '
             'de EBIT (calculado). Nuevo plan estratégico en noviembre de 2026. Sin nuevo dividendo en el informe; el último, 0,30 € por acción con '
             'cargo a 2025, se pagó en julio de 2026.',
     'positivos': ['El beneficio neto se acelera: +2,1% en el 1S, +22,0% en 9M y +77,8% en el tercer trimestre.',
                   'Cartera récord de 22.165 M€ (+133%), con IRIS² (1.926 M€) y los programas de Defensa.',
                   'Defensa duplica sus ingresos y el margen EBITDA del grupo sube 3 puntos, al 14,2%.'],
     'riesgos': ['Minsait apenas crece (+0,6%) y sus ingresos cayeron un 3,5% en el tercer trimestre.',
                 'La caja neta y el flujo libre dependen de los anticipos de Defensa (2.118 M€): sin ellos, flujo libre de 70 M€ y deuda neta de 431 M€.',
                 'Para cumplir la guía, el 4T debe crecer en torno a un 28% (calculado); la contratación de Defensa cayó un 32,7% en el 3T.'],
     'videos': [('ceFqDgJDeNE', 'Indra resultados 3T 2026: beneficio +22%, cartera récord de 22.165 M€ | Defensa duplica ingresos'),
                ('2JZxYyCrZA4', 'Indra 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Indra Group, resultados de los nueve primeros meses de 2026 (CNMV e indragroup.com, 29-oct-2026), del primer semestre (23-jul-2026) y '
                'de 2025 (25-feb-2026); Europa Press, Crónica Global, XTB e Investing.com (29-oct-2026); Bolsamanía (precios); stockanalysis.com '
                '(múltiplos históricos, oct-2026).',
     'fuentes_corto': 'Indra Group (CNMV), Europa Press, XTB, Bolsamanía y stockanalysis.com',
     'elaborado': '30-oct-2026, 11:30'},
    {'id': 'sacyr',
     'nombre': 'Sacyr',
     'ticker': 'SCYR',
     'sector': 'Construcción / concesiones',
     'lede': 'Grupo español de concesiones de infraestructuras (autopistas, hospitales, agua) con negocio de ingeniería y construcción. El 90,5% de su '
             'EBITDA procede de activos concesionales, sobre todo en Sur de Europa y Latinoamérica, y crece en países de habla inglesa (Canadá, EE. UU., '
             'Reino Unido, Australia).',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto atribuible de 116 M€ hasta septiembre (+86,9%), con 118 M€ de Concesiones (49 M€ en 9M 2025), cifra de negocios de 3.777 '
                'M€ (+10,7%) y EBITDA de 1.111 M€ (+9,2%). En el tercer trimestre, el beneficio fue de 38 M€ (+19,8%, calculado). La deuda neta con '
                'recurso subió a 322 M€ (59 M€ en diciembre) por la inversión en nuevas concesiones.',
     'precio': '4,11 €',
     'precio_fecha': '3-nov-2026',
     'multiplos': [('PER 12 meses', '~23,7x'),
                   ('EV/EBITDA', '~7,9x'),
                   ('Precio / patrimonio neto', '~1,43x'),
                   ('Rentab. dividendo', '~3,65%'),
                   ('Capitalización', '~3.312 M€')],
     'multiplos_nota': 'Calculados con el cierre de 4,11 € del 3-nov-2026 (Bolsamanía), antes de los resultados, 805,8 M de acciones y datos de 12 meses '
                       'de Sacyr (2025 + 9M26 - 9M25: beneficio neto 139,9 M€, EBITDA 1.451 M€); EV con la deuda neta total de 6.972 M€ (incluida la '
                       'financiación de proyectos) y 1.245 M€ de minoritarios; precio / patrimonio neto total con minoritarios; dividendo de 0,15 € '
                       'aprobado para 2026. A cierre de 2023, 2024 y 2025 (stockanalysis.com) el PER era 13,2x, 21,7x y 35,7x, el EV/EBITDA 8,0x, 7,5x y '
                       '8,9x, el precio / patrimonio neto 1,16x, 1,20x y 1,39x, y la rentabilidad por dividendo 4,92%, 5,23% y 2,50%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Cifra de negocios', '3.777', '+10,7%'),
               ('EBITDA', '1.111', '+9,2%'),
               ('EBIT', '837', '+13,5%'),
               ('Resultado financiero', '-443', '-0,8%'),
               ('Beneficio neto atribuible', '116', '+86,9%'),
               ('Beneficio neto 3T (calculado)', '38', '+19,8%'),
               ('Flujo de caja operativo', '930', '+21% comparable'),
               ('Deuda neta con recurso (sep-26)', '322', '')],
     'kpi': 'Margen EBITDA 29,4% (29,8% en 9M 2025). Concesiones: ingresos 1.536 M€ (+21,4%; operativos +11,1%), EBITDA 611 M€ (+8,9%; 3T -0,7%, '
            'calculado), margen 62,3% sin construcción (63,6%), beneficio 118 M€. Ingeniería e Infraestructuras: 2.419 M€ (+9,7%), EBITDA 434 M€ '
            '(+6,8%), margen de construcción pura 5,0% (4,8%), cartera 12.801 M€ (+3%). Agua: 323 M€ (+52,6%), EBITDA 55 M€ (+19,7%), cartera 8.089 M€ '
            '(+16%). Deuda neta total 6.972 M€ (6.359 M€ en diciembre), de la que 6.650 M€ es financiación de proyectos y 322 M€ con recurso; ratio con '
            'recurso por debajo de 1x. Valor interno de los activos concesionales 4.316 M€. S&P: BBB-, estable.',
     'guia': 'Sin guía numérica anual en el informe de 9M. Dividendo 2026 aprobado en la junta del 4-jun-2026: 0,15 € brutos por acción en efectivo; '
             '0,10 € pagados el 1-jul-2026 y 0,05 € a pagar en enero de 2027 (fecha exacta sin publicar a 3-nov-2026). Compromiso de repartir al menos '
             '225 M€ en efectivo entre 2025 y 2027; nuevo plan estratégico 2027-2030 en diseño. Nuevas concesiones: Museo de Ciencias de Ontario '
             '(Canadá) y Ruta 57 (Chile, seleccionada, pendiente de adjudicación formal).',
     'positivos': ['El beneficio neto crece un 86,9% y el de Concesiones se multiplica por 2,4, hasta 118 M€.',
                   'El flujo de caja operativo sube a 930 M€ (+21% en términos comparables).',
                   'Nuevas concesiones en Canadá y Chile, cartera de Agua +16% y calificación de grado de inversión (S&P BBB-).'],
     'riesgos': ['La deuda neta con recurso pasa de 59 M€ en diciembre a 322 M€, y la deuda neta total, a 6.972 M€.',
                 'El resultado financiero (-443 M€) absorbe el 53% del EBIT (calculado), y los minoritarios se quedan 99 M€.',
                 'El EBITDA de Concesiones quedó plano en el tercer trimestre (-0,7%, calculado) y el crecimiento del beneficio se modera (+156,7% en el '
                 '1S; +19,8% en el 3T).'],
     'videos': [('k77JV0jp6l4', 'Sacyr resultados 3T 2026: beneficio +86,9%, hasta 116 M€ | Concesiones x2,4 y flujo de caja 930 M€'),
                ('-7TA34Yh_hc', 'Sacyr 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Sacyr, informe de resultados de los primeros nueve meses de 2026 (CNMV y sacyr.com, 3-nov-2026), informes del primer semestre de 2026 y '
                'de 2025, y nota de la junta del 4-jun-2026; Empresa Exterior, Capital Madrid, Vozpópuli y El Debate (3-nov-2026); Bolsamanía (precio); '
                'stockanalysis.com (múltiplos históricos, oct-2026).',
     'fuentes_corto': 'Sacyr (CNMV), Empresa Exterior, Vozpópuli, Bolsamanía y stockanalysis.com',
     'elaborado': '3-nov-2026, 23:30'},
    {'id': 'rovi',
     'nombre': 'Laboratorios Rovi',
     'ticker': 'ROVI',
     'sector': 'Farmacia',
     'lede': 'Farmacéutica española con dos negocios: especialidades farmacéuticas (heparinas de bajo peso molecular, su antipsicótico inyectable Okedi, '
             'Neparvis y agentes de contraste) y fabricación para terceros (CDMO), con plantas en Madrid, Granada y, desde abril de 2026, Phoenix '
             '(Arizona, EE. UU.).',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve primeros meses de 2026',
     'titular': 'Beneficio neto de 162,8 M€ hasta septiembre (+67%), con ingresos totales de 633,7 M€ (+19%) y operativos de 610,2 M€ (+16%), impulsados '
                'por la fabricación para terceros (+45%). El EBITDA de 226,6 M€ (+52%) incluye un badwill provisional de 62,4 M€ por la compra de la '
                'planta de Phoenix; sin él, 164,3 M€ (+10%). Rovi eleva su previsión de ingresos operativos para 2026.',
     'precio': '69,10 €',
     'precio_fecha': '5-nov-2026, 09:47',
     'multiplos': [('PER 12 meses', '~17,2x (24,7x sin badwill)'),
                   ('EV/EBITDA', '~12,1x (15,4x sin badwill)'),
                   ('Precio / patrimonio neto', '~4,9x'),
                   ('Rentab. dividendo', '~1,39%'),
                   ('Capitalización', '~3.534 M€')],
     'multiplos_nota': 'Calculados con 69,10 € (5-nov-2026, hacia las 09:47, Europa Press), ya con los resultados publicados, 51,14 M de acciones '
                       '(stockanalysis) y datos de 12 meses de Rovi (2025 + 9M26 - 9M25: beneficio neto 205,5 M€, EBITDA 293,3 M€; sin el badwill de '
                       '62,4 M€, 143,1 y 230,9 M€); EV con la deuda neta de 27,9 M€; patrimonio neto de 717 M€ a junio de 2026 (stockanalysis); '
                       'dividendo de 0,9594 € pagado en julio. A cierre de 2023, 2024 y 2025 (stockanalysis.com) el PER era 18,9x, 23,5x y 23,1x, el '
                       'EV/EBITDA 13,5x, 16,7x y 17,1x (stockanalysis usa su propio EBITDA: comparación aproximada), el precio / patrimonio neto 5,91x, '
                       '5,54x y 4,81x, y la rentabilidad por dividendo 1,91%, 1,53% y 1,53%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos totales', '633,7', '+19%'),
               ('Ingresos operativos', '610,2', '+16%'),
               ('Fabricación a terceros (CDMO)', '263,9', '+45%'),
               ('Especialidades farmacéuticas', '346,1', '+1%'),
               ('EBITDA', '226,6', '+52%'),
               ('EBITDA sin badwill', '164,3', '+10%'),
               ('Beneficio neto', '162,8', '+67%'),
               ('Beneficio neto 3T (calculado)', '78,3', '+35%'),
               ('Flujo de caja libre', '61,9', '-2%')],
     'kpi': 'Margen bruto 72,7% (67,1%; 68,9% sin otros ingresos, que incluyen una subvención del CDTI). Margen EBITDA 37,1% (28,5%); sin badwill, '
            '26,9%. EBIT 198,7 M€ (+56%). Okedi 53,0 M€ (+29%; +35% en el 3T, calculado). Heparinas 180,9 M€ (-5%): enoxaparina biosimilar 107,0 M€ '
            '(-5%) y bemiparina 66,7 M€ (-6%), por los inventarios de los socios. Neparvis 43,3 M€ (+3%); contrastes y otros hospitalarios 47,8 M€ '
            '(+10%). I+D 58,4 M€ (+136%, fase III de Letrozol SIE); gastos generales 221,2 M€ (+24%). En el 3T (calculado): ingresos operativos 266,0 M€ '
            '(+26%), CDMO 157,6 M€ (+51%), EBITDA 105,4 M€ (+26%). Capex 50,3 M€ (+31%). Deuda neta 27,9 M€ (21,9 M€ en diciembre; caja neta de 22,5 M€ '
            'en junio).',
     'guia': 'Eleva la previsión 2026: ingresos operativos entre la banda media y la alta de la primera decena (0-10%) frente a 2025 (antes, entre la '
             'baja y la media). Heparinas de bajo peso molecular: caída en la banda media de 0-10%; gastos generales sin ROIS Phoenix: subida entre la '
             'banda media y la alta. Previsión 2027 con los resultados anuales, en febrero de 2027. Dividendo con cargo a 2025: 0,9594 € brutos por '
             'acción, pagado el 15-jul-2026 (ex-dividendo 13-jul). Sin dividendos nuevos anunciados en el informe de 9M.',
     'positivos': ['La fabricación para terceros crece un 45%, hasta 263,9 M€, y un 51% en el tercer trimestre (calculado).',
                   'Okedi vende 53,0 M€ (+29%) y acelera en el 3T (+35% interanual y +13% frente al 2T).',
                   'El margen bruto sube 5,7 puntos, hasta el 72,7%, y Rovi eleva su previsión de ingresos operativos para 2026.'],
     'riesgos': ['Las heparinas, su mayor negocio propio, caen un 5% por los inventarios de los socios, y Rovi prevé que sigan bajando en 2026.',
                 'Sin el badwill de 62,4 M€ de Phoenix (provisional), el EBITDA crece un 10%, con I+D +136% y gastos generales +24%.',
                 'El flujo de caja libre baja un 2% por el capex (+31%) y Rovi vuelve a deuda neta (27,9 M€) tras pagar el dividendo.'],
     'videos': [('U2PKODF57do', 'Rovi resultados 3T 2026: beneficio +67%, hasta 162,8 M€ | CDMO +45% y previsión de ingresos al alza'),
                ('jQhfxew8KlU', 'Rovi 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'Rovi, nota de prensa y presentación de resultados de los nueve primeros meses de 2026 (CNMV y rovi.es, 5-nov-2026) y nota del primer '
                'semestre de 2026; Bolsamanía, El Español, Pharmatech, Investing.com y Europa Press (5-nov-2026); stockanalysis.com (múltiplos '
                'históricos y acciones).',
     'fuentes_corto': 'Rovi (CNMV), Bolsamanía, El Español, Investing.com, Europa Press y stockanalysis.com',
     'elaborado': '5-nov-2026, 11:00'},
    {'id': 'arcelormittal',
     'nombre': 'ArcelorMittal',
     'ticker': 'MTS',
     'sector': 'Acero',
     'lede': 'Siderúrgica con sede en Luxemburgo y cotización en el IBEX 35 (además de Ámsterdam, París y Nueva York). Produce acero en Europa (con '
             'plantas en Asturias y el País Vasco), Norteamérica y Brasil, extrae mineral de hierro en Canadá y Liberia y participa en AMNS India con '
             'Nippon Steel. Publica sus cuentas en dólares.',
     'periodo': '3T 2026',
     'periodo_largo': 'tercer trimestre y acumulado a septiembre de 2026',
     'titular': 'Pérdida neta de 391 M$ en el tercer trimestre (377 M$ de beneficio en el 3T25) por la parada de su planta de Kryvyi Rih (Ucrania), con '
                '852 M$ de deterioro y 293 M$ de cargos extraordinarios. Sin esos efectos, el beneficio ajustado sube a 868 M$ (+83%), por encima del '
                'consenso, y el EBITDA a 2.023 M$ (+34%). Hasta septiembre, el beneficio neto es de 867 M$ (-70,9%).',
     'precio': '54,76 €',
     'precio_fecha': '5-nov-2026, cierre',
     'multiplos': [('PER 12 meses', '~44,2x (16,6x ajustado)'),
                   ('EV/EBITDA', '~7,7x'),
                   ('Precio / patrimonio neto', '~0,85x'),
                   ('Rentab. dividendo', '~0,98%'),
                   ('Capitalización', '~41.200 M€')],
     'multiplos_nota': 'Calculados con el cierre de 54,76 € del 5-nov-2026 en la bolsa española (Bolsamanía), ya con los resultados publicados, al '
                       'cambio de 1,1179 $/€ del BCE del 3-nov-2026 (61,22 $), 753 M de acciones (media del 3T26) y datos de 12 meses de ArcelorMittal '
                       '(4T25 + 9M26: beneficio neto 1.044 M$, ajustado 2.780 M$, EBITDA 7.359 M$); EV con la deuda neta de 10.339 M$; patrimonio '
                       'atribuido de 54.123 M$ a septiembre; dividendo base de 0,60 $ en 2026. A cierre de 2023, 2024 y 2025 (stockanalysis.com, '
                       'cotización MT) el PER era 25,9x, 13,6x y 11,1x, el EV/EBITDA 5,2x, 4,4x y 10,6x (con su propio EBITDA; con el EBITDA publicado, '
                       '3,7x en 2024 y 7,1x en 2025, calculado), el precio / patrimonio 0,42x, 0,36x y 0,62x, y la rentabilidad por dividendo 1,82%, '
                       '2,42% y 1,32%.',
     'tabla_titulo': 'Cifras en millones de dólares (M$) · 3T 2026 y 9M 2026 con su variación interanual',
     'tabla': [('Ventas 9M', '48.684', '+5,0%'),
               ('EBITDA 9M', '5.766', '+16,5%'),
               ('Beneficio neto atribuido 9M', '867', '-70,9%'),
               ('Beneficio neto ajustado 9M', '2.126', '-6,9%'),
               ('Ventas 3T', '16.466', '+5,2%'),
               ('EBITDA 3T', '2.023', '+34,2%'),
               ('Beneficio (pérdida) neto 3T', '-391', '377 en el 3T25'),
               ('Beneficio neto ajustado 3T', '868', '+83,1%'),
               ('Flujo de caja libre 9M', '-1.935', '-1.375 en 9M25'),
               ('Deuda neta (sep-26)', '10.339', '7.931 en dic-25')],
     'kpi': 'EBITDA por tonelada 155 $ en el 3T (155 $ en el 2T26 y 111 $ en el 3T25); 147 $ en 9M (121 $). Margen EBITDA 3T 12,3% (9,6%; calculado). '
            'Envíos de acero 13,0 Mt en el 3T (13,6 Mt) y 39,2 Mt en 9M (41,0). EBITDA 3T por región: Norteamérica 487 M$ (+62%), Brasil 506 M$ (+68%), '
            'Europa 548 M$ (+7% a/a; -21% frente al 2T por la energía y el carbono), Soluciones sostenibles 119 M$ (+18%), Minería 128 M$ (-39%); AMNS '
            'India, al 100%, 266 M$ (+23%). Consenso de Visible Alpha publicado por la empresa: EBITDA 1.972 M$ y beneficio ajustado 652 M$. Circulante '
            '-2.473 M$ en 9M; flujo libre subyacente ~500 M$ según la empresa. Deuda neta / EBITDA 12 meses ~1,4x (calculado); liquidez 8.700 M$. '
            'Remuneración en 9M: 341 M$ en dividendos y 760 M$ en recompras.',
     'guia': 'Inversiones 2026 de 4.500-5.000 M$ (1.700-1.900 M$ estratégicas), sin cambios. Envíos de planos en el 4T con crecimiento de doble dígito '
             'a/a y envíos del 2S por encima del 1S. Aportación de los proyectos estratégicos en 2026 rebajada a ~500 M$ de EBITDA (antes ~700 M$) por '
             'Liberia (~16 Mt de hierro, antes ~18). Hornos eléctricos de Gijón (1,1 Mt) y Sestao (1,6 Mt), en marcha en el 4T26. Dividendo base 2026: '
             '0,60 $ por acción en cuatro pagos; el cuarto, de 0,15 $, se anunció el 5-nov-2026, con ex-dividendo el 12-nov, registro el 13-nov y pago '
             'el 2-dic-2026 (importe en euros según el cambio del BCE).',
     'positivos': ['El EBITDA del tercer trimestre sube un 34%, hasta 2.023 M$, con 155 $ por tonelada (+44 $).',
                   'Norteamérica (+62%) y Brasil (+68%) impulsan el beneficio ajustado, que supera en un 33% el consenso.',
                   'Los envíos de planos en Europa suben pese a la estacionalidad con las nuevas cuotas arancelarias de la UE.'],
     'riesgos': ['La parada de Kryvyi Rih (Ucrania) deja una pérdida neta de 391 M$ en el trimestre.',
                 'El EBITDA de Europa cae un 21% frente al 2T por la energía y el carbono, y el de la minería un 28%.',
                 'La deuda neta sube 2.408 M$ desde diciembre, por el circulante, y la empresa rebaja la aportación de sus proyectos en 2026.'],
     'videos': [('FqkZusiRbGM', 'ArcelorMittal 3T 2026: pérdida de 391 M$ por Ucrania, beneficio ajustado +83% | EBITDA +34%'),
                ('_SmyWKk54AU', 'ArcelorMittal 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-04',
     'proximo_estimado': True,
     'fuentes': 'ArcelorMittal, nota de resultados del tercer trimestre de 2026 (GlobeNewswire y CNMV, 5-nov-2026), resultados de 2025 y calendario de '
                'dividendos (corporate.arcelormittal.com); consenso de Visible Alpha publicado por la empresa (2-nov-2026); Bolsamanía, Europa Press y '
                'OKDiario (5-nov-2026); BCE (BOE, 4-nov-2026); stockanalysis.com (múltiplos históricos).',
     'fuentes_corto': 'ArcelorMittal (CNMV), Visible Alpha, Bolsamanía, Europa Press, BCE y stockanalysis.com',
     'elaborado': '5-nov-2026, 23:30'},
    {'id': 'amadeus',
     'nombre': 'Amadeus',
     'ticker': 'AMS',
     'sector': 'Tecnología para viajes',
     'lede': 'Grupo español de tecnología para la industria de viajes: sistema de reservas que usan las agencias para vender vuelos (distribución '
             'aérea), software para aerolíneas y aeropuertos (gestión de pasajeros, embarque) y soluciones para hoteles y de pagos.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve meses de 2026 (enero-septiembre)',
     'titular': 'Beneficio neto de 1.081,6 M€ hasta septiembre (-0,6%) y de 381,4 M€ en el tercer trimestre (+5,7%), con ingresos de 5.075,7 M€ (+3,7%; '
                '+5,2% a tipo de cambio constante). Las reservas aéreas bajan un 2,8% por Oriente Próximo, mientras los negocios de IT para aerolíneas y '
                'hoteles crecen; Amadeus mantiene la guía 2026, aunque espera quedar en la parte baja.',
     'precio': '60,52 €',
     'precio_fecha': '6-nov-2026 (cierre)',
     'multiplos': [('PER 12 meses', '~19,5x (17,7x ajustado)'),
                   ('EV/EBITDA', '~10,7x'),
                   ('Precio / patrimonio neto', '~5,10x'),
                   ('Rentab. dividendo', '~2,54%'),
                   ('Rentab. flujo libre', '~5,4%'),
                   ('Capitalización', '~25.418 M€')],
     'multiplos_nota': 'Calculados con 60,52 € (cierre del 6-nov-2026, Bolsamanía), día de los resultados, 419,99 M de acciones en circulación (emitidas '
                       'menos autocartera a 30-sep) y datos de 12 meses de Amadeus (2025 + 9M26 - 9M25: BPA diluido 3,11 €, ajustado 3,41 €, EBITDA '
                       '2.606 M€, flujo libre 1.383 M€); EV con la deuda financiera neta de 2.536,7 M€; patrimonio neto de 4.985,7 M€; dividendo de 1,54 '
                       '€ con cargo a 2025. A cierre de 2023, 2024 y 2025 (stockanalysis.com) el PER era 25,8x, 23,7x y 20,5x, el EV/EBITDA 15,4x, 14,2x '
                       'y 12,1x, el precio / valor contable 6,43x, 5,87x y 5,63x, y la rentabilidad por dividendo 1,90%, 2,04% y 2,43% (stockanalysis '
                       'usa sus propios datos: comparación aproximada).',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos', '5.075,7', '+3,7%'),
               ('Distribución aérea', '2.391,5', '+0,6%'),
               ('IT para aerolíneas', '1.852,0', '+6,3%'),
               ('Hoteles y otras soluciones', '832,1', '+7,2%'),
               ('EBITDA', '2.028,3', '+5,2%'),
               ('EBIT ajustado', '1.546,6', '+5,2%'),
               ('Beneficio neto', '1.081,6', '-0,6%'),
               ('Beneficio neto 3T', '381,4', '+5,7%'),
               ('Flujo de caja libre', '1.036,3', '+8,5%')],
     'kpi': 'A tipo de cambio constante: ingresos +5,2%, distribución +2,1%, IT para aerolíneas +7,7%, hoteles y otras +9,2%. Margen EBITDA 40,0% '
            '(39,4%, calculado) y margen EBIT ajustado 30,5% (30,0%). Beneficio ajustado 1.147,7 M€ (+3,5%); BPA diluido 2,54 € (+4,2%) y ajustado '
            'diluido 2,69 € (+8,5%). Tercer trimestre: ingresos 1.740,7 M€ (+6,4%), EBITDA 694,1 M€ (+6,3%; consenso LSEG 691,5 M€), BPA ajustado '
            'diluido 0,94 € (+12,8%), flujo libre 564,2 M€ (+15,9%). Reservas aéreas 359,2 M (-2,8%; 3T -0,8%; Oriente Medio y África -7,5%); pasajeros '
            'embarcados 1.708,8 M (+1,3%). Inversión 503,8 M€ (-16,9%). Deuda financiera neta 2.536,7 M€ (1,0x EBITDA; 2.141,4 M€ en diciembre), tras '
            '653 M€ de dividendo y 500 M€ de recompra en 2026.',
     'guia': 'Guía 2026 mantenida (la revisada en julio), aunque Amadeus espera quedar en la parte baja de los rangos por Oriente Próximo: ingresos con '
             'crecimiento de un dígito medio-alto, margen EBIT ajustado estable, BPA ajustado diluido con crecimiento de un dígito alto a doble dígito '
             'bajo y flujo de caja libre de 1.350-1.450 M€ (el mínimo exige unos 314 M€ en el 4T, un 10% menos que en el 4T25; calculado). Sin nuevo '
             'dividendo en el informe; el de 2025, 1,54 € brutos por acción, se pagó en dos partes: 0,53 € el 16-ene-2026 y 1,01 € el 3-jul-2026. El '
             'dividendo a cuenta de 2026 aún no tiene importe ni fecha.',
     'positivos': ['El tercer trimestre acelera: ingresos +6,4% (+2,3% en el 1S) y beneficio neto +5,7% (-3,7% en el 1S).',
                   'El BPA ajustado diluido del 3T sube un 12,8%, con ayuda de las recompras, y el flujo libre del 3T, un 15,9%.',
                   'IT para aerolíneas (+5,7%) y hoteles y otras soluciones (+9,3%) crecen en el 3T a tipo constante, y el margen EBITDA sube al 40,0%.'],
     'riesgos': ['Las reservas aéreas caen un 2,8% en nueve meses (Oriente Medio y África -7,5%), y en octubre el incidente del aeropuerto de Riad frenó '
                 'algo los volúmenes.',
                 'La guía se cumpliría en la parte baja, y el beneficio neto contable de nueve meses aún baja un 0,6%.',
                 'La deuda neta sube 395 M€ desde diciembre, hasta 2.536,7 M€, por el dividendo y las recompras (1,0x EBITDA).'],
     'videos': [('6FaJP-L6oB0', 'Amadeus resultados 3T 2026: beneficio del 3T +5,7%, reservas -2,8% | Guía 2026, en la parte baja'),
                ('iKIslJepgJM', 'Amadeus 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-26',
     'proximo_estimado': True,
     'fuentes': 'Amadeus, nota de prensa, informe de gestión y presentación de resultados de enero a septiembre de 2026 (CNMV y amadeus.com, '
                '6-nov-2026), resultados del primer semestre de 2026 y de 2025; Europa Press, Rankia, Reuters (consenso LSEG), Investing.com y '
                'Bolsamanía (6-nov-2026); stockanalysis.com (múltiplos históricos).',
     'fuentes_corto': 'Amadeus (CNMV), Europa Press, Rankia, Reuters, Bolsamanía y stockanalysis.com',
     'elaborado': '6-nov-2026, 23:30'},
    {'id': 'cellnex',
     'nombre': 'Cellnex',
     'ticker': 'CLNX',
     'sector': 'Infraestructuras de telecomunicaciones',
     'lede': 'Operador europeo de infraestructuras de telecomunicaciones con sede en Barcelona: alquila espacio en sus torres a las operadoras de '
             'telefonía móvil (su negocio principal), y gestiona sistemas de antenas distribuidas y celdas pequeñas, fibra y conectividad, y la difusión '
             'de radio y televisión.',
     'periodo': '3T 2026',
     'periodo_largo': 'nueve meses de 2026 (enero-septiembre)',
     'titular': 'Flujo de caja libre de 474 M€ hasta septiembre, frente a 186 M€ un año antes, con un 22% menos de inversión; ingresos de 3.008 M€ '
                '(+2,4%; +4,9% orgánico) y pérdidas de 219 M€, un 16,7% menos. La deuda financiera neta sube a 21.044 M€ (6,13x EBITDA ajustado) y '
                'Cellnex mantiene la guía de 2026 y 2027.',
     'precio': '26,68 €',
     'precio_fecha': '6-nov-2026 (cierre)',
     'multiplos': [('EV/EBITDA ajustado', '~11,3x'),
                   ('Capitalización / RLFCF', '~8,8x'),
                   ('Rentab. RLFCF', '~11,3%'),
                   ('Rentab. dividendo', '~2,80%'),
                   ('Rentab. flujo libre', '~3,6%'),
                   ('Capitalización', '~17.718 M€')],
     'multiplos_nota': 'Calculados con 26,68 € (cierre del 6-nov-2026, Bolsamanía), día siguiente a los resultados, y la capitalización de 17.718 M€ de '
                       'Bolsamanía (~664 M de acciones), con datos de 12 meses de Cellnex (2025 + 9M26 - 9M25: EBITDA ajustado 3.430 M€, RLFCF 2.003 M€, '
                       'flujo libre 638 M€); EV con la deuda financiera neta de 21.044 M€; dividendo de 0,748 € pagado en 2026. Sin PER: Cellnex tiene '
                       'pérdidas. Con la capitalización de cierre de stockanalysis.com, la capitalización / RLFCF era 16,3x en 2023, 12,0x en 2024 y '
                       '9,4x en 2025, y el EV/EBITDA ajustado, 11,7x en 2025 (calculado); la rentabilidad por dividendo era 0,17% en 2023 y 0,21% en '
                       '2024 (stockanalysis).',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ingresos (sin pass-through)', '3.008', '+2,4%'),
               ('Torres', '2.456', '+5,1% orgánico'),
               ('EBITDA ajustado', '2.549', '+4,6%'),
               ('Flujo recurrente apalancado (RLFCF)', '1.390', '+6,9%'),
               ('Flujo de caja libre', '474', 'x2,5'),
               ('Inversión', '860', '-22,8%'),
               ('Resultado operativo', '410', '+16,1%'),
               ('Resultado neto', '-219', '-16,7% de pérdidas'),
               ('Deuda financiera neta', '21.044', '+226 desde dic.')],
     'kpi': 'Crecimientos orgánicos comparables: ingresos +4,9%, EBITDA ajustado +6,5%, EBITDAaL +8,9%, RLFCF +11,2%. Margen EBITDA ajustado 84,8% '
            '(83,1%) y margen EBITDAaL 62,9% (60,7%). RLFCF por acción 2,09 € (+18,3%). Por negocio (orgánico): torres +5,1%, DAS, small cells y RANaaS '
            '+5,2%, fibra, conectividad y housing +8,0%, difusión +0,9%. 187.693 puntos de presencia (+4,1%) y 1,65 clientes por torre (1,62x); costes '
            'operativos comparables -4,4% y coste por torre -3,5%. Tercer trimestre aislado (calculado con el 1S26): ingresos 1.014 M€, RLFCF 482 M€, '
            'flujo libre 173 M€ y pérdida de ~122 M€ (97 M€ en todo el 1S). Deuda financiera neta 21.044 M€ (20.818 M€ en diciembre): 6,13x EBITDA '
            'ajustado (6,28x); liquidez de ~5.000 M€; Fitch BBB- estable. Retribución 2026: 924 M€ de 1.000 M€ entregados a 30-sep (500 M€ en dividendos '
            'y 424 M€ en recompras).',
     'guia': 'Guía mantenida. 2026: ingresos de 4.075-4.175 M€, EBITDA ajustado de 3.425-3.525 M€, RLFCF de 1.900-2.000 M€ y flujo de caja libre de '
             '600-700 M€ (para el mínimo basta con ~126 M€ en el 4T; calculado). 2027: ingresos de 4.255-4.455 M€, EBITDA ajustado de 3.605-3.805 M€, '
             'RLFCF de 1.945-2.145 M€ y flujo libre comparable de 975-1.175 M€, sin contar ~300 M€ de inversión en Polonia (acuerdo con Polkomtel, 500 '
             'M€ adicionales en 2026-2030); deuda de 5-6x EBITDA en 2027. Sin nuevo dividendo en el informe; el de 2026 (500 M€) ya está pagado: '
             '0,37100958 € brutos por acción (ex-dividendo 13-ene, pago 15-ene-2026) y 0,37687 € (ex-dividendo 13-jul, pago 15-jul-2026). Quedan 76 M€ '
             'de recompras del programa de hasta 200 M€ que termina el 31-dic-2026.',
     'positivos': ['El flujo de caja libre se multiplica por 2,5 (474 M€) porque la inversión baja un 22,8%.',
                   'El RLFCF por acción sube un 18,3%, hasta 2,09 €, con ayuda de las recompras.',
                   'Más eficiencia: costes operativos comparables -4,4% y margen EBITDA ajustado del 84,8% (83,1%).'],
     'riesgos': ['Sigue en pérdidas (-219 M€), y el tercer trimestre aislado pierde unos 122 M€, más que todo el primer semestre (97 M€).',
                 'El proyecto de Polonia exige 500 M€ de inversión adicional hasta 2030 y resta unos 300 M€ al flujo libre de 2027.',
                 'La deuda financiera neta sube a 21.044 M€, 6,13 veces el EBITDA ajustado, por encima del rango de 5-6x que busca para 2027.'],
     'videos': [('8GrLRFxPXqI', 'Cellnex resultados 3T 2026: flujo de caja libre x2,5 y pérdidas -16,7% | Mantiene la guía'),
                ('ceDZRPFw-HE', 'Cellnex 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-26',
     'proximo_estimado': True,
     'fuentes': 'Cellnex, resultados de enero a septiembre de 2026 (cellnex.com, 5-nov-2026), resultados del primer semestre de 2026, de 9M25 y de 2024, '
                'y comunicados de dividendos; Europa Press, Reuters, RTTNews, Business People, Zona Movilidad, Redes&Telecom, El Español, Merca2 y '
                'Estrategias de Inversión; Bolsamanía (cotización); stockanalysis.com (históricos).',
     'fuentes_corto': 'Cellnex, Europa Press, Reuters, Business People, Zona Movilidad, Bolsamanía y stockanalysis.com',
     'elaborado': '7-nov-2026, 23:15'},
    {'id': 'acs',
     'nombre': 'ACS',
     'ticker': 'ACS',
     'sector': 'Construcción e infraestructuras',
     'lede': 'Grupo español de construcción e infraestructuras presidido por Florentino Pérez. Controla Hochtief, y a través de ella Turner (Estados '
             'Unidos) y CIMIC (Australia); tiene además la división de Ingeniería y Construcción (Dragados, entre otras) y la de Infraestructuras '
             '(participación en Abertis, Iridium y ACS Digital & Energy). Los centros de datos son ya una cuarta parte de su cartera.',
     'periodo': '3T 2026',
     'periodo_largo': 'tercer trimestre de 2026 (nueve meses)',
     'titular': 'Beneficio neto atribuible de 789 M€ hasta septiembre (+20,5%); sin los 70 M€ extraordinarios de 2025, el beneficio ordinario crece un '
                '35%, en la parte alta de su objetivo anual (+30% a +35%). Ventas de 41.262 M€ (+12,3%), EBITDA de 2.506 M€ (+13,0%) y cartera récord de '
                '110.994 M€ (+24,3%), con unos 26.000 M€ en centros de datos. La deuda neta es de 908 M€ en septiembre, frente a una caja neta de 1.006 '
                'M€ en junio, tras comprar el resto de Thiess y más acciones de Hochtief.',
     'precio': '92,95 €',
     'precio_fecha': '11-nov-2026',
     'multiplos': [('PER 12 meses', '~22,3x'), ('Precio / valor contable', '~4,1x'), ('Rentab. dividendo', '~2,5%'), ('Capitalización', '~25.760 M€')],
     'multiplos_nota': 'Calculados con el cierre de 92,95 € del 11-nov-2026 (Bolsamanía), antes de los resultados (publicados a las 18:00). PER con el '
                       'BPA de 12 meses (2025 + 9M26 - 9M25: 3,69 + 3,02 - 2,55 = 4,16 €); capitalización con 277,1 M de acciones (stockanalysis.com); '
                       'precio / valor contable con el patrimonio por acción de stockanalysis.com (junio de 2026); rentabilidad con el dividendo con '
                       'cargo a 2025 (0,457 € + 1,866 € = 2,323 €). No usamos EV/EBITDA porque las definiciones de EBITDA de ACS y de la fuente '
                       'histórica no coinciden. A cierre de 2023, 2024 y 2025 (stockanalysis.com) el PER era 13,6x, 14,9x y 22,8x, el precio / valor '
                       'contable 1,88x, 2,41x y 4,19x, y la rentabilidad por dividendo 5,46%, 4,34% y 2,78%.',
     'tabla_titulo': 'Cifras en millones de euros · 9M 2026 y variación frente a 9M 2025',
     'tabla': [('Ventas', '41.262', '+12,3%'),
               ('EBITDA', '2.506', '+13,0%'),
               ('EBIT', '1.807', '+20,7%'),
               ('Beneficio neto atribuible', '789', '+20,5%'),
               ('Beneficio neto ordinario', '789', '+35,0%'),
               ('Beneficio neto 3T (calculado)', '279', '+36,1%'),
               ('Cartera', '110.994', '+24,3%'),
               ('Deuda neta (sep-26)', '908', '-1.319 a/a')],
     'kpi': 'BPA 3,02 € (+18,5%). Beneficio ordinario por división: Turner 524 M€ (+44,2%), CIMIC 157 M€ (+22,1%), Ingeniería y Construcción 192 M€ '
            '(+21,8%), Infraestructuras 131 M€ (-5,9%; el texto de la nota cita 141 M€) y corporación -213 M€. Turner: ventas +23,8% sin divisas, EBITDA '
            '905 M€ (+41%), margen antes de impuestos 4,0% y cartera de 48.947 M€ (+42,4%). CIMIC: ventas 8.208 M€ y BAI ordinario 355 M€ (+12,3%). '
            'Ingeniería y Construcción: ventas +9,5%, EBITDA 544 M€ (+22,6%), margen 6,4% (+81 pb). Abertis: ventas +4% y EBITDA +5%; Iridium: BAI 35 '
            'M€. Contratación 56.228 M€ (+28,2%); centros de datos ~26.000 M€ de cartera (+94%). Flujo neto de las operaciones (12 meses) 2.385 M€; '
            'inversiones 9M 2.172 M€ (Thiess 727, Hochtief 524, centros de datos 644) y desinversiones 598 M€; colocación de acciones de 1.703 M€ en '
            'mayo.',
     'guia': 'Objetivo 2026: crecimiento del beneficio neto ordinario del 30% al 35% (unos 1.114-1.157 M€ sobre los 857 M€ de 2025, calculado); a '
             'septiembre crece un 35%. Dividendo con cargo a 2025: 0,457 € brutos (febrero de 2026) y 1,866 € brutos (dividendo flexible; fecha ex '
             '29-jun-2026 y pago en efectivo el 15-jul-2026), 2,323 € en total. La nota de 9M no anuncia un nuevo dividendo; la remuneración al '
             'accionista de 12 meses (890 M€, con minoritarios de Hochtief) incluye recompras, sin importe detallado.',
     'positivos': ['El beneficio ordinario crece un 35% hasta septiembre, en la parte alta del objetivo, y el del tercer trimestre un 36% (calculado).',
                   'Cartera récord de 110.994 M€ (+24,3%), con los centros de datos en ~26.000 M€ (+94%).',
                   'Mejoran los márgenes: Turner llega al 4,0% antes de impuestos e Ingeniería y Construcción al 6,4% de EBITDA.'],
     'riesgos': ['De caja neta de 1.006 M€ en junio a deuda neta de 908 M€ en septiembre, tras comprar el resto de Thiess (727 M€) y más Hochtief (524 '
                 'M€).',
                 'Infraestructuras gana un 5,9% menos y la corporación resta 213 M€.',
                 'Creciente dependencia de Turner (524 M€ de beneficio) y de los centros de datos, una cuarta parte de la cartera.'],
     'videos': [('W0lEuCDqG0Q', 'ACS resultados 3T 2026: beneficio 789 M€ (+20,5%), ordinario +35% | Cartera récord de 110.994 M€'),
                ('E1iNDgVxGIw', 'ACS 3T 2026 en 60 segundos (Short)')],
     'proximo': '2027-02-25',
     'proximo_estimado': True,
     'fuentes': 'ACS, nota de prensa de resultados de enero a septiembre de 2026 (CNMV y grupoacs.com, 11-nov-2026) y notas de resultados del primer '
                'semestre de 2026 y de 2025; Hochtief (nota 9M26, 5-nov-2026); Europa Press (dividendo flexible, 24-jun-2026), Bolsamanía, Valencia '
                'Plaza, OKDiario y El Conciso (11-nov-2026); stockanalysis.com (acciones, valor contable y múltiplos históricos, sep-2026).',
     'fuentes_corto': 'ACS (CNMV), Europa Press, Bolsamanía y stockanalysis.com',
     'elaborado': '11-nov-2026, 23:30'},
]
