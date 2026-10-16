#!/usr/bin/env python3
"""Hechos relevantes de las empresas del IBEX 35 (CNMV) para aiacciones.es.

Uso:  python3 espana/hechos.py            (descarga y acumula en espana/datos/hechos.json)
      python3 espana/hechos.py --html DIR (prueba con oir.html / ip.html guardados en DIR)
Corre en GitHub Actions (.github/workflows/hechos-espana.yml), que tiene acceso a cnmv.es.
Fuentes: «Información privilegiada del día» y «Otra información relevante del día» de la CNMV. Cada página
muestra el día en curso y lo recibido desde el cierre de la sesión anterior; por eso la rutina corre dos veces
al día y acumula los avisos (clave: el identificador del documento en la CNMV).
"""
import datetime as dt
import html as H
import json
import re
import sys
import unicodedata
import urllib.request
from urllib.parse import unquote
from pathlib import Path

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "datos" / "hechos.json"
PAGINAS = [("IP", "https://www.cnmv.es/portal/Informacion-Privilegiada/AlDia-IP.aspx", "ip.html"),
           ("OIR", "https://www.cnmv.es/portal/Otra-Informacion-Relevante/AlDia-OIR.aspx", "oir.html")]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
DIAS_GUARDADOS = 400

# Ticker -> nombre del emisor en la CNMV sin la forma jurídica (S.A., N.V., SOCIMI...), normalizado.
EMISORES = {
    "ACS": "ACS ACTIVIDADES DE CONSTRUCCION Y SERVICIOS", "ACX": "ACERINOX", "AENA": "AENA",
    "AMS": "AMADEUS IT GROUP", "ANA": "ACCIONA", "ANE": "CORPORACION ACCIONA ENERGIAS RENOVABLES",
    "BBVA": "BANCO BILBAO VIZCAYA ARGENTARIA", "BKT": "BANKINTER", "CABK": "CAIXABANK", "CLNX": "CELLNEX TELECOM",
    "COL": "INMOBILIARIA COLONIAL", "ELE": "ENDESA", "ENG": "ENAGAS", "FDR": "FLUIDRA", "FER": "FERROVIAL",
    "GRF": "GRIFOLS", "IAG": "INTERNATIONAL CONSOLIDATED AIRLINES GROUP", "IBE": "IBERDROLA", "IDR": "INDRA SISTEMAS",
    "ITX": "INDUSTRIA DE DISENO TEXTIL", "LOG": "COMPANIA DE DISTRIBUCION INTEGRAL LOGISTA HOLDINGS",
    "MAP": "MAPFRE", "MRL": "MERLIN PROPERTIES", "MTS": "ARCELORMITTAL", "NTGY": "NATURGY ENERGY GROUP",
    "PUIG": "PUIG BRANDS", "RED": "REDEIA CORPORACION", "REP": "REPSOL", "ROVI": "LABORATORIOS FARMACEUTICOS ROVI",
    "SAB": "BANCO DE SABADELL", "SAN": "BANCO SANTANDER", "SCYR": "SACYR", "SLR": "SOLARIA ENERGIA Y MEDIO AMBIENTE",
    "TEF": "TELEFONICA", "UNI": "UNICAJA BANCO",
}
FORMAS = {"S", "A", "SA", "SME", "M", "E", "N", "V", "NV", "SE", "PLC", "SOCIMI", "U", "SAU", "SL"}


def norm(t):
    t = unicodedata.normalize("NFD", t.upper())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return " ".join(re.sub(r"[^A-Z0-9]+", " ", t).split())


def nucleo(nombre):
    """Quita la forma jurídica del final: 'MERLIN PROPERTIES, SOCIMI, S.A.' -> 'MERLIN PROPERTIES'."""
    p = norm(nombre).split()
    while p and p[-1] in FORMAS:
        p.pop()
    return " ".join(p)


POR_NUCLEO = {v: k for k, v in EMISORES.items()}


def limpio(x):
    return " ".join(H.unescape(re.sub(r"<[^>]+>", " ", x)).split())


def parsear(html, tipo):
    """Devuelve los avisos de una página «del día» (todas las entidades)."""
    marcas = [(m.start(), "fecha", m) for m in re.finditer(r'labelFecha\w*"[^>]*>\s*(\d\d)/(\d\d)/(\d{4})', html)]
    marcas += [(m.start(), "item", m) for m in re.finditer(r'<li id="[^"]*elementoPrimerNivel"', html)]
    marcas.sort(key=lambda x: x[0])
    out, fecha = [], None
    for n, (pos, clase, m) in enumerate(marcas):
        if clase == "fecha":
            fecha = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            continue
        fin = marcas[n + 1][0] if n + 1 < len(marcas) else len(html)
        b = html[pos:fin]
        hora = re.search(r'class="time">\s*(\d\d:\d\d)', b)
        ent = re.search(r'class="tit-small">(.*?)</span>', b, re.S)
        nif = re.search(r"nif=([A-Z0-9]+)", b)
        cat = re.search(r'class="negrita" lang="es">(.*?)</span>', b, re.S)
        for d in re.finditer(r'href="(https://www\.cnmv\.es/webservices/verdocumento/ver\?t=([^"]+))"[^>]*>(.*?)</a>', b, re.S):
            out.append({"id": unquote(H.unescape(d.group(2))).strip("{}").lower(), "tipo": tipo,
                        "fecha": f"{fecha} {hora.group(1) if hora else '00:00'}" if fecha else "",
                        "entidad": limpio(ent.group(1)) if ent else "", "nif": nif.group(1) if nif else "",
                        "categoria": limpio(cat.group(1)) if cat else "", "titulo": limpio(d.group(3)),
                        "url": H.unescape(d.group(1))})
    return out


def descargar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def main():
    dir_html = Path(sys.argv[2]) if sys.argv[1:2] == ["--html"] else None
    viejo = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"items": []}
    items = {i["id"]: i for i in viejo["items"]}
    vistos, otros, errores = 0, set(), []
    for tipo, url, fichero in PAGINAS:
        try:
            html = (dir_html / fichero).read_text(encoding="utf-8", errors="replace") if dir_html else descargar(url)
        except Exception as ex:  # una página caída no debe tumbar la otra
            errores.append(f"{tipo}: {ex}")
            continue
        avisos = parsear(html, tipo)
        print(f"{tipo}: {len(avisos)} avisos en la página")
        for a in avisos:
            tk = POR_NUCLEO.get(nucleo(a["entidad"]))
            if not tk:
                otros.add(a["entidad"])
                continue
            a["ticker"] = tk
            items[a["id"]] = {**items.get(a["id"], {}), **a}
            vistos += 1
    corte = (dt.date.today() - dt.timedelta(days=DIAS_GUARDADOS)).isoformat()
    lista = sorted((i for i in items.values() if i["fecha"] >= corte), key=lambda i: (i["fecha"], i["id"]), reverse=True)
    nuevo = {"actualizado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "items": lista}
    if lista != viejo["items"] or not OUT.exists():
        OUT.write_text(json.dumps(nuevo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"IBEX 35: {vistos} avisos vistos hoy, {len(lista)} guardados")
    print("Otras entidades (no IBEX 35):", "; ".join(sorted(otros)) or "ninguna")
    if errores:
        print("ERRORES:", " | ".join(errores))
        if len(errores) == len(PAGINAS):
            sys.exit(1)


if __name__ == "__main__":
    main()
