import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = lambda m, d: dt.date(2026, m, d)
S25 = "PcBolsa, calendario 3T25 (22-oct-2025), misma semana en 2026"
DFX = "DailyForex, oct-2026"
# (fecha, empresa, ticker, sector, estado, nota, fuente)
rows = [
 (D(10,21),"Iberdrola","IBE","Eléctricas","Confirmada","Antes de apertura.","DailyForex, oct-2026"),
 (D(10,22),"Bankinter","BKT","Banca","Confirmada","",DFX),
 (D(10,28),"Banco Santander","SAN","Banca","Confirmada","",DFX),
 (D(10,29),"BBVA","BBVA","Banca","Confirmada","",DFX),
 (D(10,29),"Repsol","REP","Petróleo y gas","Confirmada","Antes de apertura; presentación 08:00 CET.","repsol.com, calendario del inversor"),
 (D(10,30),"CaixaBank","CABK","Banca","Confirmada","",DFX),
 (D(10,20),"Enagás","ENG","Gas (regulado)","Estimada","3T24: 22-oct-2024 (abre temporada).","Bolsamanía, 21-oct-2024"),
 (D(10,27),"Ferrovial","FER","Infraestructuras","Estimada","3T25: 28-oct-2025.",S25),
 (D(10,28),"Aena","AENA","Aeropuertos","Estimada","3T25: 29-oct-2025.",S25),
 (D(10,28),"Redeia","RED","Eléctricas (red)","Estimada","3T25: 29-oct-2025.",S25),
 (D(10,28),"Endesa","ELE","Eléctricas","Estimada","3T25: 29-oct-2025.",S25),
 (D(10,28),"Naturgy","NTGY","Eléctricas y gas","Estimada","3T25: 29-oct-2025.",S25),
 (D(10,29),"Puig","PUIG","Consumo (belleza)","Estimada","3T25: 30-oct-2025. Publica solo ventas en el 3T.",S25),
 (D(10,29),"Fluidra","FDR","Industrial","Estimada","3T25: 30-oct-2025.",S25),
 (D(10,30),"Unicaja","UNI","Banca","Estimada","3T25: 31-oct-2025.",S25),
 (D(10,30),"Mapfre","MAP","Seguros","Estimada","3T25: 31-oct-2025.",S25),
 (D(10,30),"Acerinox","ACX","Acero","Estimada","3T25: 31-oct-2025.",S25),
 (D(11,3),"Telefónica","TEF","Telecomunicaciones","Estimada","3T25: 4-nov-2025.",S25),
 (D(11,3),"Grifols","GRF","Farmacia","Estimada","3T25: 4-nov-2025.",S25),
 (D(11,5),"ArcelorMittal","MTS","Acero","Estimada","3T25: 6-nov-2025.",S25),
 (D(11,5),"Laboratorios Rovi","ROVI","Farmacia","Estimada","3T25: 6-nov-2025.",S25),
 (D(11,5),"Logista","LOG","Distribución","Estimada","Año fiscal oct-sep: en noviembre publica el año completo, no un 3T.",S25),
 (D(11,6),"Cellnex","CLNX","Telecom (torres)","Estimada","3T25: 7-nov-2025.",S25),
 (D(11,6),"IAG","IAG","Aerolínea","Estimada","3T25: 7-nov-2025.",S25),
 (D(11,6),"Amadeus","AMS","Tecnología","Estimada","3T25: 7-nov-2025.",S25),
 (D(11,12),"Acciona","ANA","Infraestructuras / energía","Estimada","3T25: 13-nov-2025.",S25),
 (D(11,12),"Acciona Energía","ANE","Renovables","Estimada","3T25: 13-nov-2025.",S25),
 (D(11,12),"Banco Sabadell","SAB","Banca","Estimada","3T25: 13-nov-2025, fecha atípica (OPA de BBVA). Puede volver a fines de octubre: revisar.",S25),
 (D(11,13),"Merlin Properties","MRL","Inmobiliario (SOCIMI)","Estimada","3T25: 14-nov-2025.",S25),
 (D(12,2),"Inditex","ITX","Textil","Estimada","Ejercicio feb-ene: en diciembre publica 9M (feb-oct), no el 3T calendario.","PcBolsa (3T25: inicios de diciembre)"),
 (None,"ACS","ACS","Construcción","Por confirmar","Suele publicar a fines de octubre.","Sin fuente de fecha"),
 (None,"Indra","IDR","Defensa / tecnología","Por confirmar","Suele publicar a fines de octubre.","Sin fuente de fecha"),
 (None,"Colonial","COL","Inmobiliario (SOCIMI)","Por confirmar","Suele publicar en noviembre.","Sin fuente de fecha"),
 (None,"Sacyr","SCYR","Construcción / concesiones","Por confirmar","Suele publicar a fines de octubre o inicios de noviembre.","Sin fuente de fecha"),
 (None,"Solaria","SLR","Renovables","Por confirmar","Suele publicar a fines de octubre o inicios de noviembre.","Sin fuente de fecha"),
]
rows.sort(key=lambda r: (r[0] is None, r[0] or dt.date(2099,1,1), r[1]))

DIAS = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
wb = Workbook(); ws = wb.active; ws.title = "Calendario 3T26 España"
ws["A1"] = "Calendario de resultados 3T26 · IBEX 35"; ws["A1"].font = Font(bold=True, size=14)
ws["A2"] = ("Actualizado al 12-oct-2026. Confirmada = fecha publicada por la empresa o la prensa con fecha 2026. "
            "Estimada = misma semana que en 3T25 (el método acierta en las 6 confirmadas salvo Iberdrola, que se adelantó). "
            "Hora Chile: las empresas publican ~07:00-08:00 Madrid = 02:00-03:00 Chile (03:00-04:00 desde el 25-oct).")
ws["A2"].font = Font(italic=True, size=9, color="555555")
hdr = ["Fecha","Día","Semana","Empresa","Ticker","Sector","Estado","Nota","Fuente"]
ws.append([]); ws.append(hdr); H = 4
thin = Side(style="thin", color="DDDDDD")
for c in range(1, len(hdr)+1):
    cell = ws.cell(H, c); cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F3A5F"); cell.alignment = Alignment(vertical="center", wrap_text=True)
fills = {"Confirmada": PatternFill("solid", fgColor="E3F4E6"), "Estimada": PatternFill("solid", fgColor="FFF3D6"),
         "Por confirmar": PatternFill("solid", fgColor="F2F2F2")}
for f, emp, tk, sec, est, nota, fue in rows:
    if f:
        lunes = f - dt.timedelta(days=f.weekday())
        ws.append([f, DIAS[f.weekday()], f"Semana del {lunes.day}-{lunes.month:02d}", emp, tk, sec, est, nota, fue])
        ws.cell(ws.max_row, 1).number_format = "dd-mm-yyyy"
    else:
        ws.append(["", "", "", emp, tk, sec, est, nota, fue])
    r = ws.max_row; ws.cell(r, 7).fill = fills[est]
    for c in range(1, len(hdr)+1):
        ws.cell(r, c).border = Border(bottom=thin); ws.cell(r, c).alignment = Alignment(vertical="top", wrap_text=c in (8, 9))
for i, w in enumerate([12,11,17,22,9,24,13,55,40], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A5"; ws.auto_filter.ref = f"A{H}:I{ws.max_row}"

ws2 = wb.create_sheet("Fuentes")
for line in [
 ["Fuente","Uso"],
 ["https://es.dailyforex.com/stock-market-today/2026/10/santander-bbva-y-caixabank-afrontan-octubre-2026-con-resultados-dividendos-ytipos/250330","Bankinter 22-oct, Santander 28-oct, BBVA 29-oct, CaixaBank 30-oct (3T26)."],
 ["https://es.dailyforex.com/stock-market-today/2026/10/iberdrola-afronta-octubre-con-una-valoracion-exigente-2026/250300","Iberdrola 21-oct (3T26)."],
 ["https://www.repsol.com/es/accionistas-inversores/calendario/2026/presentacion-resultados-tercer-trimestre-2026/index.cshtml","Repsol 29-oct, 08:00 CET (3T26)."],
 ["https://pcbolsa.com/Noticia/13095/Calendario-de-presentacion-de-resultados-del-tercer-trimestre-de-2025-en-bolsa-espanola","Fechas 3T25 usadas para estimar."],
 ["https://www.bolsamania.com/noticias/empresas/enagas-iberdrola-bankinter-inauguran-temporada-resultados-asi-seran-cuentas--17730886.html","Enagás 3T24 (22-oct-2024)."],
 ["https://www.cnmv.es","Publicación oficial: 'Otra información relevante' de cada emisor, el día del resultado."],
]:
    ws2.append(line)
ws2["A1"].font = ws2["B1"].font = Font(bold=True)
ws2.column_dimensions["A"].width = 70; ws2.column_dimensions["B"].width = 70
wb.save("/mnt/project-files/espana/calendario-3T26/calendario-resultados-3T26-espana.xlsx")
print(len(rows), "empresas")
