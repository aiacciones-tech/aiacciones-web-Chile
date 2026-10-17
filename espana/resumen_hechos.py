#!/usr/bin/env python3
"""Resumen diario por correo de los hechos relevantes del IBEX 35 sobre resultados, dividendos y ampliaciones de capital.

Lo pidió Daniel el 17-oct-2026: cada día en danweifis@gmail.com, con los últimos 7 días y en una tabla como el correo
de hechos esenciales de la CMF chilena (Fecha/Hora, Entidad, Asunto/Categoría, documento). Lo usa la tarea programada
de Claude, que lo envía por Gmail. Lee espana/datos/hechos.json (lo rellena espana/hechos.py) y el calendario de resultados.

Uso:  python3 espana/resumen_hechos.py [--dias 7]   -> imprime JSON {"asunto", "texto", "html", "n"}
"""
import datetime as dt
import html as H
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from hechos import temas

AQUI = Path(__file__).resolve().parent
MADRID = ZoneInfo("Europe/Madrid")
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
NOMBRE_TEMA = {"resultados": "Resultados", "dividendos": "Dividendos", "capital": "Ampliación de capital"}
TIPO = {"IP": "Información privilegiada", "OIR": "Otra información relevante"}
TD = 'style="border:1px solid #999;padding:6px;vertical-align:top"'
TH = 'style="border:1px solid #999;padding:6px;background:#eee;text-align:left"'


def fecha_corta(d):
    return f"{d.day}-{MESES[d.month - 1]}-{d.year}"


def main():
    dias = int(sys.argv[sys.argv.index("--dias") + 1]) if "--dias" in sys.argv else 7
    ahora = dt.datetime.now(MADRID)
    desde = (ahora - dt.timedelta(days=dias)).strftime("%Y-%m-%d %H:%M")
    hechos = json.loads((AQUI / "datos" / "hechos.json").read_text(encoding="utf-8"))
    cal = json.loads((AQUI / "datos" / "calendario-3T26.json").read_text(encoding="utf-8"))
    nombres = {c["ticker"]: c["empresa"] for c in cal["empresas"]}
    for i in hechos["items"]:
        i["temas"] = temas(i)  # recalculado aquí: los avisos antiguos pueden no traerlo guardado
    its = sorted((i for i in hechos["items"] if i["fecha"] >= desde and i["temas"]), key=lambda i: i["fecha"], reverse=True)
    hoy = ahora.date()
    proximos = [c for c in cal["empresas"] if c.get("fecha") and hoy.isoformat() <= c["fecha"] <= (hoy + dt.timedelta(days=7)).isoformat()]
    desde_txt = f"{desde[8:10]}/{desde[5:7]}/{desde[:4]} {desde[11:16]}"

    intro = (f"Se encontraron {len(its)} hechos relevantes del IBEX 35 sobre resultados, dividendos o ampliaciones de capital "
             f"en los últimos {dias} días (desde el {desde_txt}, hora de Madrid), ordenados del más reciente al más antiguo.")
    filas_t, filas_h = [], []
    for i in its:
        fh = f'{i["fecha"][8:10]}/{i["fecha"][5:7]}/{i["fecha"][:4]} {i["fecha"][11:16]}'
        ent = f'{nombres.get(i["ticker"], i["entidad"])} ({i["ticker"]})'
        tema = ", ".join(NOMBRE_TEMA[t] for t in i["temas"])
        asunto = f'{i["titulo"]} — {i["categoria"]} · {TIPO.get(i["tipo"], i["tipo"])}'
        filas_t.append(f"{fh} | {ent} | {tema} | {asunto} | {i['url']}")
        filas_h.append(f'<tr><td {TD}>{H.escape(fh)}</td><td {TD}>{H.escape(ent)}</td><td {TD}>{H.escape(tema)}</td>'
                       f'<td {TD}>{H.escape(i["titulo"])}<br><span style="color:#666">{H.escape(i["categoria"])} · {H.escape(TIPO.get(i["tipo"], i["tipo"]))}</span></td>'
                       f'<td {TD}><a href="{H.escape(i["url"])}">Ver en la CNMV</a></td></tr>')
    cab = ["Fecha/Hora", "Entidad", "Tema", "Asunto/Categoría", "Documento"]
    if its:
        tabla_t = " | ".join(cab) + "\n" + "\n".join(filas_t)
        tabla_h = ('<table cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:13px">'
                   "<tr>" + "".join(f'<th {TH}>{c}</th>' for c in cab)
                   + "</tr>" + "".join(filas_h) + "</table>")
    else:
        tabla_t = "Sin comunicaciones de estos temas en el periodo."
        tabla_h = "<p><em>Sin comunicaciones de estos temas en el periodo.</em></p>"

    prox_t = "\n".join(f'{fecha_corta(dt.date.fromisoformat(c["fecha"]))} | {c["empresa"]} ({c["ticker"]}) | {c.get("estado", "")}' for c in proximos) or "Ninguno en el calendario."
    prox_h = ('<table cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:13px">'
              f'<tr><th {TH}>Fecha</th><th {TH}>Empresa</th><th {TH}>Estado</th></tr>' 
              + "".join(f'<tr><td {TD}>{fecha_corta(dt.date.fromisoformat(c["fecha"]))}</td><td {TD}>{H.escape(c["empresa"])} ({c["ticker"]})</td>'
                        f'<td {TD}>{H.escape(c.get("estado", ""))}</td></tr>' for c in proximos)
              + "</table>") if proximos else "<p><em>Ninguno en el calendario.</em></p>"

    pie = ("Fuente: CNMV (Información privilegiada y Otra información relevante), seguida por AIAcciones España desde el 16-oct-2026. "
           "Todos los hechos: https://aiacciones.es/hechos/ · Calendario: https://aiacciones.es/calendario/. "
           "Resumen informativo, no es una recomendación de inversión.")
    texto = f"{intro}\n\n{tabla_t}\n\nPróximos resultados (7 días):\n{prox_t}\n\n{pie}"
    html = (f'<div style="font-family:Arial,sans-serif;font-size:14px;color:#111"><p>{H.escape(intro)}</p>{tabla_h}'
            f'<p style="margin-top:18px"><strong>Próximos resultados (7 días)</strong></p>{prox_h}'
            f'<p style="color:#666;font-size:12px;margin-top:18px">{H.escape(pie)}</p></div>')
    asunto = f"Hechos relevantes IBEX 35 — {len(its)} en {dias} días (resultados, dividendos, capital) — {fecha_corta(hoy)}"
    print(json.dumps({"asunto": asunto, "texto": texto, "html": html, "n": len(its)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
