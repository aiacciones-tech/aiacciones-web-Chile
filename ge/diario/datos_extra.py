"""Datos extra de Wall Street auf Deutsch que no trae datos-diario-nabd (que no se modifica). Corre en GitHub Actions (datos-extra-GE.yml):
el contenedor de Claude no llega a TradingView.

uso: python3 ge/diario/datos_extra.py fx      -> ge/diario/extra/fx/fx-<fecha NY>.json
     python3 ge/diario/datos_extra.py logos   -> ge/diario/extra/logos/{us,de}/<TICKER>.png + logos/indice.json

- fx: EUR/USD (y EUR/CHF para Suiza) al cierre de Nueva York, para el «Deutscher Blick» del Tagesbericht
  (precios también en euros y el S&P 500 medido en euros, «berechnet»).
- logos: logos de las ~900 mayores empresas de EE. UU. y las ~200 mayores de Xetra (los de TradingView, los mismos que ve cualquiera en su web),
  en PNG de 256 px para las miniaturas (ge/diario/miniatura.py). Se refresca cada semana.
El workflow guarda la carpeta extra/ en la rama datos-extra-ge (no en main)."""
import json, os, sys, datetime, urllib.request
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "..", "..", "nabd", "diario"))
from datos_mercado import get, TVH, UA  # noqa: E402
OUT = os.path.join(ROOT, "extra")
NY = ZoneInfo("America/New_York")
FX = ["FX:EURUSD", "FX_IDC:EURCHF"]
COLS = ["name", "description", "close", "change", "change_abs", "Perf.W", "Perf.1M", "Perf.YTD"]


def fx():
    r = get("https://scanner.tradingview.com/global/scan", json.dumps({"symbols": {"tickers": FX}, "columns": COLS}).encode(), TVH)
    d = {x["s"]: dict(zip(COLS, x["d"])) for x in r.get("data", [])}
    assert "FX:EURUSD" in d and d["FX:EURUSD"]["close"], f"sin EUR/USD: {r}"
    ahora = datetime.datetime.now(datetime.timezone.utc)
    fecha = ahora.astimezone(NY).date().isoformat()
    os.makedirs(f"{OUT}/fx", exist_ok=True)
    p = f"{OUT}/fx/fx-{fecha}.json"
    json.dump({"generado": ahora.isoformat(timespec="seconds"), "fecha": fecha, "fuente": "TradingView", "fx": d}, open(p, "w"), indent=1)
    print("ok", p, d["FX:EURUSD"]["close"], d["FX:EURUSD"]["change"])


def scan(mercado, n):
    body = {"columns": ["name", "logoid", "market_cap_basic", "exchange"], "range": [0, n],
            "filter": [{"left": "type", "operation": "equal", "right": "stock"}],
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}}
    r = get(f"https://scanner.tradingview.com/{mercado}/scan", json.dumps(body).encode(), TVH)
    return [(x["s"], dict(zip(body["columns"], x["d"]))) for x in r.get("data", [])]


def logos():
    import cairosvg
    os.makedirs(f"{OUT}/logos", exist_ok=True)
    idx, hechos, fallos = {}, {}, 0
    for mercado, n, sub in (("america", 900, "us"), ("germany", 200, "de")):
        os.makedirs(f"{OUT}/logos/{sub}", exist_ok=True)
        for sym, d in scan(mercado, n):
            lid = d.get("logoid")
            if not lid or lid.startswith("country/"):
                continue
            if mercado == "germany" and d.get("exchange") != "XETR":
                continue
            rel = f"{sub}/{d['name'].replace('/', '.')}.png"
            if rel in idx.values():
                continue
            try:
                if lid not in hechos:
                    svg = urllib.request.urlopen(urllib.request.Request(f"https://s3-symbol-logo.tradingview.com/{lid}--big.svg",
                                                                        headers={"User-Agent": UA}), timeout=30).read()
                    hechos[lid] = cairosvg.svg2png(bytestring=svg, output_width=256, output_height=256)
                open(f"{OUT}/logos/{rel}", "wb").write(hechos[lid])
                idx[sym] = rel
            except Exception as e:  # un logo que falta no para el resto: la miniatura usa la insignia con el ticker
                fallos += 1; print("sin logo", sym, lid, e)
    json.dump({"generado": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "fuente": "TradingView (s3-symbol-logo)",
               "logos": idx}, open(f"{OUT}/logos/indice.json", "w"), indent=0, sort_keys=True)
    print("ok logos", len(idx), "fallos", fallos)


if __name__ == "__main__":
    {"fx": fx, "logos": logos}[sys.argv[1]]()
