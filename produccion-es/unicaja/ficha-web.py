# Ficha web de Unicaja para /home/claude/aiacciones-web-chile/espana/fichas.py (mismas claves que la de Bankinter).
# Los marcadores VIDEO_ID y SHORT_ID los rellena quien sube los vídeos.
FICHA = {
    "id": "unicaja",
    "nombre": "Unicaja",
    "ticker": "UNI",
    "sector": "Banca",
    "lede": "Banco español minorista, con fuerte presencia en Andalucía, Castilla y León, Castilla-La Mancha, Asturias y Extremadura. "
            "En un banco, los ingresos son el margen bruto y la calidad del balance se mide con la morosidad y el capital.",
    "periodo": "1S 2026",
    "periodo_largo": "primer semestre de 2026",
    "titular": "Beneficio neto de 361 M€ (+7,1%). El 2T (201 M€) superó al consenso en un 10% según Investing.com, sobre todo por menores deterioros "
               "(41 M€ frente a 55 esperados); el margen de intereses quedó en línea y las comisiones, un 2% por debajo. Unicaja mejoró su guía de beneficio para 2026.",
    "precio": "3,242 €",
    "precio_fecha": "13-oct-2026",
    "multiplos": [("PER 12 meses", "12,9x"), ("PER forward", "11,8x"), ("Precio / valor en libros", "1,23x"),
                  ("Rentab. dividendo", "5,3%"), ("Capitalización", "~8.330 M€")],
    "multiplos_nota": "Con precio de 3,242 € al 13-oct-2026 (stockanalysis.com). A cierre de 2022, 2023, 2024 y 2025 el PER era 10,1x, 9,1x, 5,7x y 11,4x, "
                      "y el precio / valor en libros 0,42x, 0,36x, 0,48x y 1,01x. En un banco no se usan EV/EBITDA ni flujo de caja libre.",
    "tabla_titulo": "Cifras en millones de euros · 1S 2026 y variación frente al 1S 2025",
    "tabla": [
        ("Margen de intereses", "755", "+1,7%"),
        ("Comisiones netas", "269", "+2,6%"),
        ("Margen bruto", "1.085", "+2,5%"),
        ("Costes (calculado)", "494", "~+5%"),
        ("Margen de explotación", "590", "~+0,5%"),
        ("Beneficio neto", "361", "+7,1%"),
        ("BPA (calculado)", "~0,14 €", "n. d."),
    ],
    "kpi": "Eficiencia 45,6% (44,6% en 1S 2025); ROTE 10,0% (12% ajustado por exceso de capital). Morosidad 1,8% (−38 pb), cobertura de dudosos 82,7%, coste del riesgo 19 pb. "
           "CET1 15,8% (exceso de 2.201 M€ sobre requerimientos). Crédito sano 49.941 M€ (+3,7%); depósitos de clientes 76.264 M€ (+4,1%); recursos fuera de balance +12,7%; "
           "nueva producción hipotecaria +39,5%. Comisiones no bancarias: 53% del total (+11,8%).",
    "guia": "Guía 2026, revisada el 31-jul-2026 (según Investing.com): beneficio creciendo a un dígito medio y margen de intereses a un dígito bajo-medio (antes: superar 2025), "
            "coste del riesgo de 20-25 pb (antes: menos de 30 pb), comisiones a un dígito bajo y costes a un dígito medio. Remuneración del 95% del beneficio en efectivo; "
            "dividendo a cuenta de 8,44 céntimos por acción (+28%), pagado el 24-sep-2026.",
    "positivos": ["El 2T superó al consenso en un 10% y la guía de beneficio sube.",
                  "Morosidad del 1,8% (−38 pb) y coste del riesgo de 19 pb.",
                  "Nueva producción hipotecaria +39,5% y dividendo a cuenta +28%."],
    "riesgos": ["La sorpresa del 2T vino de menos deterioros; las comisiones quedaron un 2% por debajo de lo esperado.",
                "Los costes suben cerca de un 5% y el margen bruto un 2,5%: la eficiencia empeora al 45,6%.",
                "El coste de los depósitos sube tras la subida de tipos del BCE y no hay guía para 2027."],
    "videos": [("QmTUeCVBUk4", "Unicaja resultados 1S 2026: beneficio +7,1%; el 2T supera al consenso un 10% | Guía al alza"),
               ("zoldZTxXavE", "Unicaja 1S 2026 en 60 segundos (Short)")],
    "proximo": "2026-10-30",
    "fuentes": "Unicaja, nota de resultados del primer semestre 2026 (31-jul-2026, CNMV y unicajabanco.com); Investing.com (consenso y guía, 31-jul-2026); "
               "XTB y Bolsamania (desglose trimestral y de costes, 31-jul-2026); stockanalysis.com (precio y múltiplos, 13-oct-2026).",
    "fuentes_corto": "Investing.com, XTB, Bolsamania y stockanalysis.com",
    "elaborado": "13-oct-2026, 19:00",
}
