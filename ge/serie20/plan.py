"""Qué episodios de la serie «Die Wall-Street-Giganten» (Wall Street auf Deutsch) tocan hoy. Adaptación de nabd/serie20/plan.py.
Regla de Daniel (13 y 18-nov-2026): un episodio por empresa de las 20 mayores de EE. UU. tras cada informe de resultados, como máximo
3 vídeos de la serie al día; si coinciden más, pasan a los días siguientes (el más antiguo primero y, a igual fecha, la empresa más grande).
Lee los datos de la rama datos-serie20-nabd (los escribe serie20-datos-Nabd.yml; aquí solo se leen).
Además lee, si se pasa, la rama datos-serie20-ge (empresas extra del canal alemán: ANT y SPCX, Daniel 21-nov-2026; serie20-datos-GE.yml).
uso: python3 plan.py <rama datos-serie20-nabd> <carpeta cola-ge de youtube-cola> [<rama datos-serie20-ge>]
Cada episodio lleva "datos": la carpeta de datos de la que copiar <TICKER>/datos.json.
Imprime el calendario y, en la última línea, JSON con "hoy": [{ticker, fecha, carpeta}] (0 a 3) y "pendientes"."""
import json, os, sys, datetime as dt
from zoneinfo import ZoneInfo

MAX_DIA = 3
INICIO = os.environ.get("INICIO_GE", "2026-11-17")   # primer informe que cubre el canal alemán (Nvidia, 17-nov-2026)
BERLIN = ZoneInfo("Europe/Berlin")


def main():
    datos, cola = sys.argv[1], sys.argv[2]; cal = json.load(open(os.path.join(datos, "calendario.json")))
    for e in cal["empresas"]: e["_datos"] = datos
    if len(sys.argv) > 3 and os.path.exists(os.path.join(sys.argv[3], "calendario.json")):
        extra = json.load(open(os.path.join(sys.argv[3], "calendario.json")))
        for e in extra["empresas"]: e["_datos"] = sys.argv[3]
        cal["empresas"] += extra["empresas"]
    hoy = dt.datetime.now(BERLIN).date().isoformat()
    hechos, hoy_n = set(), 0
    for d in sorted(os.listdir(cola)) if os.path.isdir(cola) else []:
        if not d.startswith("serie20-"): continue
        hechos.add(d)
        p = os.path.join(cola, d, "encolado.txt")
        if os.path.exists(p) and open(p).read().strip()[:10] == hoy: hoy_n += 1
    pend = []
    for e in cal["empresas"]:
        ev = e.get("evento")
        if not ev or not ev.get("datos_listos") or ev["fecha"] < INICIO: continue   # sin cifras en TradingView todavía, o anterior al inicio
        carpeta = f"serie20-{e['ticker'].lower()}-{ev['fecha']}"
        if carpeta in hechos: continue
        pend.append({"ticker": e["ticker"], "fecha": ev["fecha"], "periodo": ev.get("periodo"), "carpeta": carpeta, "cap": e.get("cap") or 0, "datos": e["_datos"]})
    pend.sort(key=lambda x: (x["fecha"], -x["cap"]))
    libres = max(0, MAX_DIA - hoy_n)
    print(f"datos de {cal['generado']} · ya encolados hoy ({hoy}, Berlín): {hoy_n} · huecos hoy: {libres} · desde {INICIO}")
    print("hechos:", ", ".join(sorted(hechos)) or "ninguno")
    for i, p in enumerate(pend): print(f"{'HOY ' if i < libres else '    '}{p['ticker']:6} resultados {p['fecha']} (periodo fiscal {p['periodo']})")
    prox = sorted((e["proxima_ny"], e["ticker"]) for e in cal["empresas"] if e.get("proxima_ny") and e["proxima_ny"] >= hoy)
    esperando = [e["ticker"] for e in cal["empresas"] if e.get("evento") and e["evento"]["fecha"] >= INICIO and not e["evento"].get("datos_listos")]
    if esperando: print("con resultados pero sin cifras en TradingView todavía:", ", ".join(esperando))
    print("próximos resultados (TradingView):", ", ".join(f"{t} {f}" for f, t in prox))
    print(json.dumps({"hoy": pend[:libres], "pendientes": pend[libres:], "proximos": prox}, ensure_ascii=False))


if __name__ == "__main__":
    main()
