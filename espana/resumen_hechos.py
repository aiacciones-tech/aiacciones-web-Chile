#!/usr/bin/env python3
"""Resumen diario por correo de los hechos relevantes del IBEX 35 sobre resultados, dividendos y ampliaciones de capital.

Lo pidió Daniel el 17-oct-2026: cada día en danweifis@gmail.com. Lo usa la tarea programada de Claude, que envía el
resultado por Gmail. Lee espana/datos/hechos.json (lo rellena espana/hechos.py) y el calendario de resultados.

Uso:  python3 espana/resumen_hechos.py [--horas 24]   -> imprime JSON {"asunto", "texto", "html", "n"}
"""
import datetime as dt
import html as H
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

AQUI = Path(__file__).resolve().parent
MADRID = ZoneInfo("Europe/Madrid")
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
TITULOS = [("resultados", "Resultados"), ("dividendos", "Dividendos"), ("capital", "Ampliaciones de capital")]
TIPO = {"IP": "Información privilegiada", "OIR": "Otra información relevante"}


def fecha_corta(d):
    return f"{d.day}-{MESES[d.month - 1]}-{d.year}"


def main():
    horas = int(sys.argv[sys.argv.index("--horas") + 1]) if "--horas" in sys.argv else 24
    ahora = dt.datetime.now(MADRID)
    desde = (ahora - dt.timedelta(hours=horas)).strftime("%Y-%m-%d %H:%M")
    hechos = json.loads((AQUI / "datos" / "hechos.json").read_text(encoding="utf-8"))
    cal = json.loads((AQUI / "datos" / "calendario-3T26.json").read_text(encoding="utf-8"))
    nombres = {c["ticker"]: c["empresa"] for c in cal["empresas"]}
    nuevos = [i for i in hechos["items"] if i["fecha"] >= desde and i.get("temas")]
    hoy = ahora.date()
    proximos = [c for c in cal["empresas"] if c.get("fecha") and hoy.isoformat() <= c["fecha"] <= (hoy + dt.timedelta(days=7)).isoformat()]

    texto, html = [], []
    for tema, titulo in TITULOS:
        its = sorted((i for i in nuevos if tema in i["temas"]), key=lambda i: i["fecha"])
        texto.append(f"{titulo.upper()} ({len(its)})")
        html.append(f'<h3 style="margin:18px 0 6px">{H.escape(titulo)} ({len(its)})</h3>')
        if not its:
            texto.append("  Sin comunicaciones nuevas.")
            html.append('<p style="color:#666;margin:0">Sin comunicaciones nuevas.</p>')
        else:
            html.append('<ul style="margin:0;padding-left:18px">')
        for i in its:
            emp = nombres.get(i["ticker"], i["entidad"])
            cab = f'{i["fecha"][8:10]}/{i["fecha"][5:7]} {i["fecha"][11:16]} · {i["ticker"]} {emp} · {TIPO.get(i["tipo"], i["tipo"])}'
            texto.append(f"  - {cab}\n    {i['titulo']}\n    {i['url']}")
            html.append(f'<li style="margin-bottom:8px"><span style="color:#666;font-size:13px">{H.escape(cab)}</span><br>'
                        f'<a href="{H.escape(i["url"])}">{H.escape(i["titulo"])}</a></li>')
        if its:
            html.append("</ul>")

    texto.append("\nPRÓXIMOS RESULTADOS (7 días)")
    html.append('<h3 style="margin:18px 0 6px">Próximos resultados (7 días)</h3>')
    if proximos:
        html.append('<ul style="margin:0;padding-left:18px">')
        for c in proximos:
            lin = f'{fecha_corta(dt.date.fromisoformat(c["fecha"]))} · {c["empresa"]} ({c["ticker"]}) · {c.get("estado", "")}'
            texto.append(f"  - {lin}")
            html.append(f"<li>{H.escape(lin)}</li>")
        html.append("</ul>")
    else:
        texto.append("  Ninguno en el calendario.")
        html.append('<p style="color:#666;margin:0">Ninguno en el calendario.</p>')

    pie = (f"Comunicaciones de las empresas del IBEX 35 a la CNMV desde el {desde} (hora de Madrid), filtradas por resultados, "
           "dividendos y ampliaciones de capital. Fuente: CNMV. Todos los hechos: https://aiacciones.es/hechos/ · "
           "Calendario: https://aiacciones.es/calendario/. Resumen informativo, no es una recomendación de inversión.")
    texto.append("\n" + pie)
    html.append(f'<p style="color:#666;font-size:12px;margin-top:20px">{H.escape(pie)}</p>')
    asunto = f"IBEX 35 · Resultados, dividendos y capital · {fecha_corta(hoy)} ({len(nuevos)} {'aviso' if len(nuevos) == 1 else 'avisos'})"
    cuerpo_html = ('<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.45;color:#111;max-width:680px">'
                   f'<h2 style="margin:0 0 4px">Hechos relevantes del IBEX 35</h2><p style="color:#666;margin:0">{H.escape(fecha_corta(hoy))} · '
                   f'últimas {horas} horas</p>{"".join(html)}</div>')
    print(json.dumps({"asunto": asunto, "texto": "\n".join(texto), "html": cuerpo_html, "n": len(nuevos)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
