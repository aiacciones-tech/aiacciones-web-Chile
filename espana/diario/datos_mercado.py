"""Datos de la sesión para el vídeo diario de la bolsa española (corre en GitHub Actions, que tiene internet).
uso: python3 espana/diario/datos_mercado.py  -> espana/diario/datos/mercado-<fecha>.json
Fuentes: Yahoo Finance (histórico diario del IBEX 35 y de sus 35 valores, intradía del índice) y
TradingView (cambio del día, volumen, bono español y alemán a 10 años, contexto internacional)."""
import json, os, sys, datetime, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ROOT))
from hechos import EMISORES
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
YH = {"LOG": "LOG.MC"}


def get(url, data=None, extra=None):
    h = {"User-Agent": UA}
    h.update(extra or {})
    req = urllib.request.Request(url, data=data, headers=h)
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode())


def yahoo(sym, rng, interval):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range={rng}&interval={interval}"
    r = get(u)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(r.get("timestamp") or []):
        if q["close"][i] is None:
            continue
        out.append({"t": ts, "o": q["open"][i], "h": q["high"][i], "l": q["low"][i], "c": q["close"][i], "v": q["volume"][i]})
    return {"meta": {k: r["meta"].get(k) for k in ("currency", "exchangeTimezoneName", "regularMarketPrice", "chartPreviousClose")}, "velas": out}


def tv(tickers, cols):
    body = json.dumps({"symbols": {"tickers": tickers}, "columns": cols}).encode()
    r = get("https://scanner.tradingview.com/global/scan", body,
            {"Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/", "Content-Type": "application/json"})
    return {x["s"]: dict(zip(cols, x["d"])) for x in r.get("data", [])}


def main():
    res = {"generado": datetime.datetime.utcnow().isoformat() + "Z", "errores": []}
    try:
        res["ibex_diario"] = yahoo("^IBEX", "2y", "1d")
    except Exception as e:
        res["errores"].append(f"ibex_diario: {e}")
    try:
        res["ibex_intradia"] = yahoo("^IBEX", "5d", "5m")
    except Exception as e:
        res["errores"].append(f"ibex_intradia: {e}")
    res["valores"] = {}
    for tk in EMISORES:
        try:
            res["valores"][tk] = yahoo(YH.get(tk, tk + ".MC"), "3mo", "1d")
        except Exception as e:
            res["errores"].append(f"{tk}: {e}")
    cols = ["name", "description", "close", "change", "change_abs", "volume", "average_volume_10d_calc", "time", "Perf.W", "Perf.1M", "Perf.YTD"]
    ctx = ["BME:IBC", "TVC:ES10Y", "TVC:DE10Y", "TVC:IT10Y", "TVC:US10Y", "TVC:SX5E", "TVC:DAX", "XETR:DAX", "TVC:CAC40", "TVC:UKX",
           "FTSEMIB:FTSEMIB", "SP:SPX", "NASDAQ:NDX", "DJ:DJI", "FX:EURUSD", "TVC:UKOIL", "TVC:USOIL", "TVC:GOLD", "TVC:NI225", "TVC:HSI"]
    try:
        res["tv"] = tv(ctx + ["BME:" + t for t in EMISORES], cols)
    except Exception as e:
        res["errores"].append(f"tradingview: {e}")
    fecha = datetime.date.today().isoformat()
    try:
        last = res["ibex_diario"]["velas"][-1]["t"]
        fecha = datetime.datetime.utcfromtimestamp(last).date().isoformat()
    except Exception:
        pass
    os.makedirs(os.path.join(ROOT, "datos"), exist_ok=True)
    p = os.path.join(ROOT, "datos", f"mercado-{fecha}.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    print("escrito", p, "errores:", res["errores"])


if __name__ == "__main__":
    main()
