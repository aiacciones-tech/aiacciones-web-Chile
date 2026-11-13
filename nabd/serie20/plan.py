"""Qué episodios de «عمالقة وول ستريت» tocan hoy. Regla de Daniel (13-nov-2026): un episodio por empresa tras cada informe de resultados,
a partir de este trimestre, y como máximo 3 vídeos de la serie al día; si coinciden más, pasan a los días siguientes (el más antiguo primero,
y a igual fecha la empresa más grande).
uso: python3 plan.py <rama datos-serie20-nabd> <carpeta cola-nabd de youtube-cola>
Imprime el calendario y, en la última línea, JSON con "hoy": [{ticker, fecha, carpeta}] (0 a 3) y "pendientes"."""
import json, os, sys, datetime as dt

MAX_DIA = 3
RIAD = dt.timezone(dt.timedelta(hours=3))


def main():
    datos, cola = sys.argv[1], sys.argv[2]; cal = json.load(open(os.path.join(datos, "calendario.json")))
    hoy = dt.datetime.now(RIAD).date().isoformat()
    hechos, hoy_n = set(), 0
    for d in sorted(os.listdir(cola)) if os.path.isdir(cola) else []:
        if not d.startswith("serie20-") or d.startswith("serie20-intro"): continue
        hechos.add(d)
        p = os.path.join(cola, d, "encolado.txt")
        if os.path.exists(p) and open(p).read().strip()[:10] == hoy: hoy_n += 1
    pend = []
    for e in cal["empresas"]:
        ev = e.get("evento")
        if not ev: continue
        carpeta = f"serie20-{e['ticker'].lower()}-{ev['fecha']}"
        if carpeta in hechos: continue
        pend.append({"ticker": e["ticker"], "fecha": ev["fecha"], "periodo": ev.get("periodo"), "tipo": ev["tipo"], "carpeta": carpeta, "cap": e.get("cap") or 0})
    pend.sort(key=lambda x: (x["fecha"], -x["cap"]))
    libres = max(0, MAX_DIA - hoy_n)
    print(f"datos de {cal['generado']} · ya encolados hoy ({hoy}, Riad): {hoy_n} · huecos hoy: {libres}")
    print("hechos:", ", ".join(sorted(hechos)) or "ninguno")
    for i, p in enumerate(pend): print(f"{'HOY ' if i < libres else '    '}{p['ticker']:6} resultados {p['fecha']} ({p['tipo']}, periodo {p['periodo']})")
    prox = sorted((e["proxima"][:10], e["ticker"]) for e in cal["empresas"] if e.get("proxima") and e["proxima"][:10] >= hoy)
    print("próximos resultados (TradingView):", ", ".join(f"{t} {f}" for f, t in prox))
    print(json.dumps({"hoy": pend[:libres], "pendientes": pend[libres:], "proximos": prox}, ensure_ascii=False))


if __name__ == "__main__":
    main()
