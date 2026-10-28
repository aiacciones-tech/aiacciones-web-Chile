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
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 1.033 M€ (-20,6%) por el encarecimiento del combustible; beneficio operativo antes de excepcionales de 1.757 M€ '
                '(-6,4%), con un 2T (1.406 M€) un 2,8% por encima del consenso que recoge Renta 4 (calculado). Flujo de caja libre de 2.905 M€ y deuda '
                'neta de 4.692 M€ (0,6x EBITDA).',
     'precio': '4,78 €',
     'precio_fecha': '23-oct-2026, 11:52',
     'multiplos': [('PER 12 meses', '~7,1x'),
                   ('EV/EBITDA', '~3,4x'),
                   ('Rentab. dividendo', '~2,05%'),
                   ('FCF yield', '~18,8%'),
                   ('Capitalización', '~21.000 M€')],
     'multiplos_nota': 'Con precio de 4,78 € en el BME el 23-oct-2026 a las 11:52 (Bolsamanía); múltiplos calculados con ~4.400 M de acciones '
                       '(stockanalysis.com) y datos de 12 meses de IAG (BPA básico 66,9 céntimos, EBITDA 7.640 M€, deuda neta 4.692 M€, dividendo 2025 '
                       'de 0,098 €, flujo libre 3.954 M€). A cierre de 2023, 2024 y 2025 (stockanalysis, cotización de Londres) el PER era 3,3x, 6,5x y '
                       '6,5x, el EV/EBITDA 4,4x, 4,9x y 4,6x, la rentabilidad por dividendo -, 2,54% y 2,08%, y la rentabilidad por flujo libre 15,0%, '
                       '20,1% y 14,5%. La recompra en curso (1.500 M€) equivale a ~7% de la capitalización.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ingresos', '16.064', '+1,0%'),
               ('Ingresos de pasaje', '14.082', '+2,3%'),
               ('Beneficio operativo antes de excepcionales', '1.757', '-6,4%'),
               ('Beneficio operativo 2T antes de excepcionales', '1.406', '-16,3%'),
               ('Beneficio neto', '1.033', '-20,6%'),
               ('BPA básico', '22,9 cts', '-16,1%'),
               ('Flujo de caja libre', '2.905', '+38,5% (calculado)')],
     'kpi': 'Margen operativo antes de excepcionales 10,9% (11,8%); 2T 15,8% (19,0%). Capacidad (AKO) -0,1%, ocupación 85,0% (+0,9 pp), 57,9 M de '
            'pasajeros. Ingreso de pasaje por AKO +2,4% (+6,2% a tipo de cambio constante); coste unitario sin combustible -1,3%; combustible y '
            'emisiones 3.956 M€ (+12,3%). Beneficio operativo por aerolínea: British Airways 1.020 M€ (+44), Iberia 526 M€ (-38), Vueling 46 M€ (-49), '
            'Aer Lingus -34 M€ (-114), IAG Loyalty 275 M€ (+48). Excepcionales 149 M€ (ERE voluntario de Iberia y reestructuración de BA). Deuda neta '
            '4.692 M€ (-1.256 M€ vs diciembre), 0,6x EBITDA; liquidez 11.873 M€.',
     'guia': 'Guía 2026: capacidad plana frente a 2025 (cerca de +3% en febrero); combustible 8.300-8.600 M€ (unos 9.000 M€ en mayo), con la meta de '
             'recuperar ~60% del sobrecoste; margen operativo dentro del objetivo del 12%-15%; coste unitario sin combustible plano; inversión ~3.400 '
             'M€. Recompra de 1.500 M€ con ~800 M€ ejecutados, a terminar antes de finales de febrero de 2027; dividendo 2025 de 0,098 € por acción '
             '(+8,9%); el dividendo a cuenta de 2026 se decidirá con los resultados del 3T.',
     'positivos': ['Flujo de caja libre de 2.905 M€ y deuda neta de solo 0,6x EBITDA.',
                   'El ingreso de pasaje por AKO sube un 6,2% a tipo de cambio constante y el beneficio operativo del 2T supera el consenso.',
                   'British Airways e IAG Loyalty mejoran, y la recompra de 1.500 M€ sigue adelante.'],
     'riesgos': ['El combustible sube un 12,3% en el semestre y un 22,8% en el 2T.',
                 'Aer Lingus pasa a pérdidas y Vueling gana la mitad que hace un año.',
                 'La capacidad de 2026 queda plana por las rutas suspendidas en Oriente Medio y la competencia en el corto radio europeo.'],
     'videos': [('ShNA56tU4sY', 'IAG resultados 1S 2026: beneficio 1.033 M€ (-20,6%) por el combustible | Deuda neta -1.256 M€'),
                ('sDSWqb5VGVs', 'IAG 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-11-06',
     'proximo_estimado': False,
     'fuentes': 'IAG, informe semestral 1S 2026 (31-jul-2026, CNMV y LSE), resultados 2025 (27-feb-2026) y calendario financiero; XTB (31-jul-2026); '
                'Renta 4 Banco / Capitalbolsa (consenso, 31-jul-2026); Estrategias de Inversión (1T26, 8-may-2026); Bolsamanía (precio, 23-oct-2026); '
                'stockanalysis.com (acciones y múltiplos históricos).',
     'fuentes_corto': 'XTB, Renta 4 Banco, Estrategias de Inversión, Bolsamanía y stockanalysis.com',
     'elaborado': '23-oct-2026, 12:35'},
    {'id': 'acerinox',
     'nombre': 'Acerinox',
     'ticker': 'ACX',
     'sector': 'Siderurgia',
     'lede': 'Fabricante de acero inoxidable (Acerinox Europa en Algeciras, North American Stainless en EE. UU. y Columbus en Sudáfrica) y de aleaciones '
             'de alto rendimiento (VDM Metals y Haynes International). En el acero pesan las toneladas, el precio frente al coste de las materias primas '
             '(níquel, chatarra), la energía y el capital circulante.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 77 M€, frente a pérdidas de 18 M€ en el 1S 2025; EBITDA de 271 M€ (+27%). El EBITDA del 2T (176 M€, +85% frente al '
                '1T) superó en un 16,6% el consenso elaborado por la compañía (calculado). Flujo de caja libre de -105 M€ y deuda neta de 1.361 M€.',
     'precio': '16,64 €',
     'precio_fecha': '23-oct-2026, 15:30',
     'multiplos': [('PER 12 meses', '~75x'),
                   ('EV/EBITDA', '~13,4x'),
                   ('Precio / valor contable', '~1,94x'),
                   ('Rentab. dividendo', '~3,73%'),
                   ('Capitalización', '~4.150 M€')],
     'multiplos_nota': 'Con precio de 16,64 € en el BME el 23-oct-2026 a las 15:30 (Bolsarama); múltiplos calculados con 249,3 M de acciones y datos de '
                       '12 meses a junio de Acerinox (beneficio neto 55 M€, EBITDA 411 M€, deuda neta 1.361 M€, patrimonio neto 2.140 M€, dividendo 0,62 '
                       '€). El PER es muy alto porque el beneficio de 12 meses incluye las pérdidas del 2S 2025. A cierre de 2023, 2024 y 2025 '
                       '(stockanalysis.com, datos S&P Global) el PER era 11,6x, 10,5x y - (pérdidas), el EV/EBITDA 4,3x, 7,8x y 12,8x, la rentabilidad '
                       'por dividendo 6,66%, 7,13% y 5,07%, y el precio / valor contable 1,08x, 0,92x y 1,50x.',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ventas', '2.966', '-3,0%'),
               ('EBITDA', '271', '+26,6%'),
               ('EBITDA 2T', '176', '+57% (calculado)'),
               ('EBITDA acero inoxidable', '236', '+66% (calculado)'),
               ('EBITDA aleaciones de alto rendimiento', '35', '-51% (calculado)'),
               ('Beneficio neto', '77', '-18 en 1S 2025'),
               ('Flujo de caja libre', '-105', '+91 en 1S 2025')],
     'kpi': 'Margen EBITDA 9,1% (7,0%; calculado); 2T 11%. Producción de acería 1,03 Mt (+2%); 2T 540.000 t (+8%); laminación en frío del inoxidable '
            '615.000 t (-1%). Ventas: inoxidable 2.246 M€ (+3,2%), aleaciones 729 M€ (-18,4%). EE. UU. (North American Stainless) es el motor, con su '
            'ampliación de 244 M$ terminada; en Europa las importaciones caen un 31% y Acerinox Europa logra EBITDA positivo en junio; VDM Metals lastra '
            'las aleaciones. Flujo operativo 43 M€ tras 146 M€ de circulante; inversiones 148 M€. Deuda neta 1.361 M€ (+172 M€ desde diciembre, '
            'calculado), 2,5x EBITDA anualizado.',
     'guia': 'Acerinox espera un EBITDA del 3T "ligeramente superior" al del 2T (176 M€), pese a la estacionalidad y las paradas de mantenimiento, con '
             'EE. UU. fuerte y Europa mejorando con las nuevas cuotas (-55%) y el arancel del 50% fuera de cuota desde julio. La bajada del níquel '
             'afectará a los precios; prevé reducir el circulante. Beyond Excellence: 112 M€ acumulados (93% del objetivo de 120 M€). Dividendo con '
             'cargo a 2025: 0,62 € por acción (0,31 € en enero y 0,31 € el 17 de julio).',
     'positivos': ['Vuelve a beneficios y el EBITDA del 2T supera en un 16,6% el consenso de la compañía (calculado).',
                   'El acero inoxidable dispara su EBITDA (+66%), con EE. UU. como motor.',
                   'Europa mejora con menos importaciones y la empresa espera un 3T algo mejor que el 2T.'],
     'riesgos': ['El flujo de caja libre es negativo (-105 M€) y la deuda neta sube hasta 1.361 M€.',
                 'Las aleaciones de alto rendimiento ganan la mitad que hace un año, con VDM por debajo de lo esperado.',
                 'La bajada del níquel y un consumo de planos en EE. UU. un 8% menor en el semestre.'],
     'videos': [('IuxWhvplVuQ', 'Acerinox resultados 1S 2026: vuelve a beneficios con 77 M€ | EBITDA 2T 176 M€, +85% trimestral'),
                ('9rnH1TvvMdw', 'Acerinox 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-10-30',
     'proximo_estimado': False,
     'fuentes': 'Acerinox, nota de prensa, informe de gestión intermedio y presentación de resultados 1S 2026 (24-jul-2026), resultados 2025 '
                '(27-feb-2026) y agenda del inversor; Investing.com (consenso, 24-jul-2026); XTB y Bolsamanía (24-jul-2026); conferencia con analistas '
                '(GuruFocus/Yahoo Finance); Bolsarama (precio, 23-oct-2026); stockanalysis.com (múltiplos históricos).',
     'fuentes_corto': 'Investing.com, XTB, Bolsamanía, Bolsarama y stockanalysis.com',
     'elaborado': '23-oct-2026, 15:50'},
    {'id': 'grifols',
     'nombre': 'Grifols',
     'ticker': 'GRF',
     'sector': 'Farmacia y salud · hemoderivados (plasma)',
     'lede': 'Compañía de medicamentos derivados del plasma (Biopharma: inmunoglobulinas, albúmina, alfa-1 y proteínas especiales), con más de 400 '
             'centros de donación, además de diagnóstico (Diagnostic) y Bio Supplies. En el plasma pesan el coste de obtener la materia prima, la mezcla '
             'de productos, el dólar y la deuda. El IBEX 35 incluye la clase A (GRF); la clase B (GRF.P) no tiene voto y cobra un dividendo preferente.',
     'periodo': '1S 2026',
     'periodo_largo': 'primer semestre de 2026',
     'titular': 'Beneficio neto de 227 M€ (+28,7%; +13,6% sin extraordinarios). Ingresos de 3.574 M€ (-2,8% en euros; +2,6% a tipo constante), con las '
                'inmunoglobulinas +12,8%. Flujo de caja libre antes de M&A de 91 M€ (-12 M€ en el 1S 2025) y apalancamiento de 4,2x según Grifols; guía '
                '2026 confirmada.',
     'precio': '10,055 € (clase A)',
     'precio_fecha': '23-oct-2026, 16:25',
     'multiplos': [('PER 12 meses', '~15,1x'),
                   ('EV/EBITDA', '~10,4x'),
                   ('Precio / valor contable', '~0,74x'),
                   ('Rentab. dividendo', '~2,31%'),
                   ('Capitalización', '~5.920 M€')],
     'multiplos_nota': 'Con precio de la clase A de 10,055 € en el BME el 23-oct-2026 a las 16:25 (Bolsarama); múltiplos calculados con datos de 12 '
                       'meses a junio: BPA 0,66 € (beneficio de 452 M€ y 680,6 M de acciones), dividendo con cargo a 2025 de 0,2324 € por acción A (0,15 '
                       '+ 0,0824). Capitalización con 422,4 M de acciones A y 258,2 M de acciones B a 6,48 € (stockanalysis, 1-oct-2026). Valor empresa '
                       '~17.200 M€ con la deuda neta de balance (8.843 M€) y los minoritarios (2.434 M€); EBITDA de 12 meses de stockanalysis (1.650 '
                       'M€); con el EBITDA ajustado de Grifols (1.803 M€), ~9,5x. Precio / valor contable sobre el patrimonio neto total (7.980 M€). A '
                       'cierre de 2023, 2024 y 2025 (stockanalysis.com, datos S&P Global) el PER era 219,8x, 36,2x y 16,3x, el EV/EBITDA 19,1x, 10,8x y '
                       '10,5x, el precio / valor contable 1,23x, 0,66x y 0,86x, y la rentabilidad por dividendo 0%, 0% y 2,19% (calculada).',
     'tabla_titulo': 'Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025',
     'tabla': [('Ingresos', '3.574', '-2,8% (+2,6% a tipo constante)'),
               ('Biopharma', '3.148', '-0,2% (+5,4% a tipo constante)'),
               ('Diagnostic', '284', '-14,3% (-9,7% a tipo constante)'),
               ('Bio Supplies', '50', '-27,0% (-21,7% a tipo constante)'),
               ('EBITDA ajustado', '854', '-2,5% (+2,4% a tipo constante)'),
               ('Beneficio neto', '227', '+28,7%'),
               ('BPA', '0,33 €', '+27% (calculado)'),
               ('Flujo de caja libre antes de M&A', '91', '-12 en 1S 2025')],
     'kpi': 'Margen EBITDA ajustado 23,9% (23,8%; calculado); 2T 25,2%. Biopharma por franquicia (tipo constante): inmunoglobulinas +12,8% (intravenosas '
            '+12,5%, subcutáneas +17,7%), albúmina -14,2% (precios en China), alfa-1 y proteínas especiales -2,6% (+2,0% en el 2T). Margen bruto 37,1% '
            '(39,1%), con ~40 M€ de costes puntuales por el cierre de 29 centros en EE. UU. Red: ~280 centros en EE. UU. y más de 130 en el resto del '
            'mundo; Grifols no publica el coste por litro. Deuda neta 7.798 M€ según el contrato de crédito (8.843 M€ en balance), 4,2x EBITDA según '
            'Grifols; liquidez 2.030 M€. Vencimientos de 2027 refinanciados y 500 M€ del bono 2030 amortizados: sin vencimientos relevantes hasta el 4T '
            '2028.',
     'guia': 'Guía 2026 confirmada: EBITDA ajustado +5% a +9% a tipo constante, margen de al menos el 25% y flujo de caja libre antes de M&A y '
             'dividendos de 500-575 M€ (el 1S lleva 91 M€, el 16-18%; calculado). Objetivo de apalancamiento de 3,5x o menos a finales de 2027. Egipto: '
             '180 M€ más hasta 2029 para llegar a 3 millones de litros de plasma al año. Dividendo con cargo a 2025: ~0,23 € brutos por acción A (0,15 € '
             'en agosto de 2025 y 0,082 € el 2 de julio de 2026).',
     'positivos': ['El beneficio neto sube un 28,7%, hasta 227 M€, y el margen EBITDA ajustado del 2T llega al 25,2%.',
                   'Las inmunoglobulinas crecen un 12,8% a tipo constante (subcutáneas +17,7%).',
                   'Flujo de caja libre positivo (91 M€) y vencimientos de 2027 refinanciados.'],
     'riesgos': ['El apalancamiento sigue en 4,2x, frente al objetivo de 3,5x o menos a finales de 2027.',
                 'La albúmina cae un 14,2% y el dólar resta crecimiento en euros.',
                 'Para cumplir la guía de caja necesita más de 400 M€ en el segundo semestre (calculado).'],
     'videos': [('ZmBOEO1agsY', 'Grifols resultados 1S 2026: beneficio +28,7%, hasta 227 M€ | Inmunoglobulinas +12,8%, deuda en 4,2x'),
                ('xrWR9VfrbhY', 'Grifols 1S 2026 en 60 segundos (Short)')],
     'proximo': '2026-11-03',
     'proximo_estimado': True,
     'fuentes': 'Grifols, nota de prensa, presentación y estados financieros intermedios del 1S 2026 (28-jul-2026, CNMV y SEC), resultados 2025 '
                '(26-feb-2026) y dividendos (CNMV/SEC, jun-2025 y jun-2026); Investing.com (presentación y conferencia, 28-jul-2026); Europa '
                'Press/Bolsamanía (28-jul-2026); Benzinga España (29-jul-2026); Bolsarama (precio, 23-oct-2026); stockanalysis.com (múltiplos '
                'históricos).',
     'fuentes_corto': 'Investing.com, Europa Press, Bolsamanía, Benzinga España, Bolsarama y stockanalysis.com',
     'elaborado': '23-oct-2026, 17:00'},
]
