"""Calendario de dividendos del IBEX 35 (página /dividendos/).

Solo dividendos ya aprobados o anunciados por la empresa, con su fuente; nunca estimaciones de terceros.
- ex: fecha ex-dividendo (ISO). ex_calc=True si la empresa no la publicó y la calculamos (dos días hábiles antes del pago).
- pago: fecha de pago (ISO) o None si la empresa solo dio el mes; entonces pago_txt lo dice ("enero de 2027").
- La página separa solos los próximos de los ya pagados según la fecha de hoy, así que basta con añadir filas.
Cuando una empresa anuncie un dividendo (resultados o hecho relevante con tema "dividendos"), añadirlo aquí
y, si estaba en POR_ANUNCIAR, quitarlo de allí.
"""

DIVIDENDOS = [
    {"ticker": "BBVA", "importe": "0,37 €", "tipo": "A cuenta 2026, en efectivo",
     "ex": "2026-10-13", "ex_calc": True, "pago": "2026-10-15",
     "fuente": "BBVA (CNMV); Estrategias de Inversión", "url": "https://www.estrategiasdeinversion.com/actualidad/dividendos/bbva-dispara-un-16-su-dividendo-fechas-clave-para-n-956005"},
    {"ticker": "SAN", "importe": "0,127 €", "tipo": "A cuenta 2026, en efectivo (+10%)",
     "ex": "2026-10-29", "pago": "2026-11-02",
     "fuente": "Banco Santander, información privilegiada del 29-sep-2026",
     "url": "https://www.santander.com/content/dam/santander-com/es/documentos/informacion-privilegiada/2026/09/hr-2026-09-29-aprobacion-por-el-consejo-de-administracion-del-pago-de-un-dividendo-a-cuenta-en-efectivo-es.pdf"},
    {"ticker": "ITX", "importe": "0,875 €", "tipo": "Complementario 2025: 0,325 € ordinario + 0,55 € extraordinario",
     "ex": "2026-10-29", "ex_calc": True, "pago": "2026-11-02",
     "fuente": "Inditex (junta del 7-jul-2026); Finect", "url": "https://www.finect.com/usuario/eduardogarcia/articulos/inditex-logra-un-beneficio-record-de-2980-millones-y-pagara-un-dividendo-de-0875-euros-el-2-de-noviembre"},
    {"ticker": "FDR", "importe": "0,33 €", "tipo": "Segundo pago con cargo a 2025 (total 0,65 €)",
     "ex": "2026-12-08", "ex_calc": True, "pago": "2026-12-10",
     "fuente": "Fluidra (junta del 6-may-2026); Estrategias de Inversión", "url": "https://www.estrategiasdeinversion.com/actualidad/dividendos/fluidra-eleva-un-8-el-dividendo-hasta-los-065-n-902709"},
    {"ticker": "REP", "importe": "0,56 €", "tipo": "En efectivo: 0,53 € de reservas + 0,03 € a cuenta de 2026",
     "ex": None, "pago": None, "pago_txt": "enero de 2027",
     "fuente": "Repsol, nota de prensa de resultados del 3T 2026 (CNMV, 29-oct-2026)",
     "url": "https://www.repsol.com/content/dam/repsol-corporate/es/accionistas-e-inversores/cnmv/2026/oir29102026-nota-prensa-resultados-3t-2026.pdf"},
    {"ticker": "NTGY", "importe": "0,60 €", "tipo": "Segundo a cuenta 2026, en efectivo (total 2026: 1,80 €)",
     "ex": "2026-11-03", "ex_calc": True, "pago": "2026-11-05",
     "fuente": "Naturgy, informe de resultados 9M 2026 (29-oct-2026)",
     "url": "https://stproportalcorporativo.blob.core.windows.net/uploads/2026/10/Naturgy-Rdos-9M26.pdf"},
    {"ticker": "IBE", "importe": "0,275 €", "tipo": "A cuenta 2026 (+8,7%), Iberdrola Retribución Flexible: efectivo o acciones nuevas",
     "ex": "2027-01-12", "pago": "2027-02-01",
     "fuente": "Iberdrola, hecho relevante del 21-oct-2026 (fechas previstas; elección del 12 al 25 de enero)",
     "url": "https://www.cnmv.es/webservices/verdocumento/ver?t=%7bfd187aa5-63b0-47ef-a0a0-ea1b75d0f62e%7d"},
    {"ticker": "MAP", "importe": "0,08 €", "tipo": "A cuenta 2026, en efectivo (+14,3%)",
     "ex": "2026-11-24", "pago": "2026-11-26",
     "fuente": "Mapfre, información sobre el dividendo a cuenta 2026 (CNMV, 28-oct-2026)",
     "url": "https://www.cnmv.es/webservices/verdocumento/ver?t=%7b71fa2436-f101-41ca-90c5-e1612a6f0ca9%7d"},
    {"ticker": "RED", "importe": "0,204 €", "tipo": "A cuenta 2026, en efectivo (+2%)",
     "ex": "2027-01-05", "ex_calc": True, "pago": "2027-01-07",
     "fuente": "Redeia, acuerdo del consejo (CNMV, 28-oct-2026); Europa Press",
     "url": "https://www.cnmv.es/webservices/verdocumento/ver?t=%7b257f9041-bc4d-464f-a465-142e355c07a0%7d"},
    {"ticker": "TEF", "importe": "0,15 €", "tipo": "Dividendo 2026, en efectivo",
     "ex": None, "pago": None, "pago_txt": "junio de 2027",
     "fuente": "Telefónica, resultados del 1S 2026", "url": None},
]

# Dividendos que la empresa ha anunciado sin importe o sin fecha todavía (texto de su última comunicación).
POR_ANUNCIAR = [
    ("CABK", "Dividendo a cuenta en noviembre del 30-40% del beneficio del primer semestre (961-1.281 M€).", "CaixaBank, resultados del 1S 2026"),
    ("IAG", "El dividendo a cuenta de 2026 se decidirá con los resultados del tercer trimestre.", "IAG, resultados del 1S 2026"),
    ("ENG", "Dividendo de 1 € por acción con cargo a 2026; falta el calendario del pago a cuenta.", "Enagás, resultados de 9M 2026"),
    ("FER", "Nuevo dividendo flexible (scrip) de 600 M€: el importe por acción se conocerá el 3-nov, ex-dividendo el 5-nov y pago desde el 10-dic de 2026.", "Ferrovial, resultados de 9M 2026"),
]
