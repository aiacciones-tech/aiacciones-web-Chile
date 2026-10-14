# Ficha web de Banco Santander (1S 2026) para espana/fichas.py. Los marcadores VIDEO_ID y SHORT_ID los rellena quien sube.
FICHA = {
    "id": "santander",
    "nombre": "Banco Santander",
    "ticker": "SAN",
    "sector": "Banca",
    "lede": "Mayor banco español por capitalización, con negocio en Europa (España, Reino Unido, Portugal) y América (Brasil, Estados Unidos, México). "
            "En 2026 compró TSB en Reino Unido y Webster en Estados Unidos, y vendió su banco en Polonia. En un banco, los ingresos son el margen bruto "
            "y la calidad del balance se mide con la morosidad y el capital.",
    "periodo": "1S 2026",
    "periodo_largo": "primer semestre de 2026",
    "titular": "Beneficio ordinario de 7.328 M€ (+15%), su mayor beneficio semestral; el atribuido, 8.973 M€ (+31%), incluye la plusvalía por la venta de Polonia. "
               "El 2T (3.768 M€) quedó en línea con el consenso: 3.750 M€ en el sondeo de Reuters y 3.771 M€ en el consenso recopilado por el banco.",
    "precio": "12,02 €",
    "precio_fecha": "9-oct-2026",
    "multiplos": [("PER 12 meses", "13,6x"), ("PER forward", "10,5x"), ("Precio / valor en libros", "1,49x"),
                  ("Rentab. dividendo", "2,1%"), ("Capitalización", "~173.090 M€")],
    "multiplos_nota": "Con precio de 12,02 € al 9-oct-2026 (stockanalysis.com); precio / valor tangible 1,91x y recompras equivalentes al 3,5% anual. "
                      "A cierre de 2022, 2023, 2024 y 2025 el PER era 5,1x, 5,7x, 5,7x y 11,0x, y el precio / valor en libros 0,48x, 0,58x, 0,63x y 1,31x. "
                      "En un banco no se usan EV/EBITDA ni flujo de caja libre.",
    "tabla_titulo": "Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025",
    "tabla": [
        ("Margen de intereses", "22.711", "+7%"),
        ("Comisiones netas", "6.851", "+9%"),
        ("Margen bruto", "30.847", "+6%"),
        ("Costes", "13.211", "0%"),
        ("Margen neto", "17.636", "+12%"),
        ("Dotaciones por insolvencias", "6.574", "+9%"),
        ("Beneficio ordinario", "7.328", "+15%"),
        ("Beneficio atribuido", "8.973", "+31%"),
        ("BPA ordinario (calculado)", "~0,51 €", "+20%"),
    ],
    "kpi": "Eficiencia 42,8% (−2,9 pp); RoTE ordinario 15,6% (+0,7 pp). Morosidad 2,93% (−7 pb en el trimestre), cobertura 64%, coste del riesgo 1,15%. "
           "CET1 14,0% tras la compra de TSB (−55 pb). Crédito +9% y recursos de clientes +11% en euros constantes (+5% y +7% sin TSB); 182 M de clientes (+12 M). "
           "Beneficio por países: España 2.534 M€ (+12%), Brasil 1.093 M€ (+10%), EE. UU. 989 M€ (+18%), México 897 M€ (+13%), Reino Unido 725 M€ (+30%, con TSB). "
           "Por negocios: banca comercial 4.124 M€ (+13%), CIB 1.742 M€ (+18%), Wealth 1.083 M€ (+20%), Openbank 827 M€ (−21%).",
    "guia": "Objetivos 2026 reiterados (euros constantes, sin las compras de 2025-26): ingresos creciendo a un dígito medio, costes a la baja y beneficio ordinario por encima "
            "de los 14.101 M€ de 2025 (en el semestre, el 52%, calculado). CET1 entre el 12% y el 13%. Remuneración de ~50% del beneficio, a partes iguales entre dividendo y recompras; "
            "~9.000 M€ de recompras con cargo a 2025-26, incluida una nueva de ~1.800 M€.",
    "positivos": ["Beneficio ordinario récord (+15%) y BPA ordinario +20%, con ayuda de las recompras.",
                  "Costes planos (−1% en euros constantes) y eficiencia del 42,8%, casi 3 puntos mejor.",
                  "CET1 del 14% después de comprar TSB y ~9.000 M€ en recompras 2025-26."],
    "riesgos": ["Las dotaciones suben un 9%, sobre todo por Argentina, y el coste del riesgo (1,15%) sigue alto.",
                "Openbank cae un 21% por la financiación de coches en Reino Unido y el fin de las ayudas al coche eléctrico en EE. UU.",
                "La integración de TSB y Webster tiene costes (250 M€ de reestructuración en TSB) y reduce el capital."],
    "videos": [("-ED5j67j-0g", "Banco Santander resultados 1S 2026: beneficio ordinario récord +15%; el 2T, en línea | BPA +20%"),
               ("ZesAasxjui0", "Banco Santander 1S 2026 en 60 segundos (Short)")],
    "proximo": "2026-10-28",
    "fuentes": "Banco Santander, nota y presentación de resultados del primer semestre 2026 (22-jul-2026, CNMV y santander.com); Reuters / MarketScreener y Benzinga (consenso, 21-22-jul-2026); "
               "Infobae y El Español (desglose por países, 22-jul-2026); stockanalysis.com (precio y múltiplos, 9-oct-2026).",
    "fuentes_corto": "Reuters, Benzinga, Infobae, El Español y stockanalysis.com",
    "elaborado": "13-oct-2026, 19:00",
}
