"""Datos de la sesión del IPSA para el vídeo diario de la Bolsa de Santiago (diario/).
Corre en GitHub Actions (el contenedor de Claude no llega a Yahoo ni a TradingView).
uso: python3 diario/datos_mercado.py  -> diario/datos/mercado-<fecha>.json
Fuentes: Yahoo Finance (histórico diario e intradía del IPSA, ^IPSA) y TradingView (cambio del día de las acciones
chilenas, volumen y monto transado, índices MSCI IPSA/IGPA, contexto internacional: Wall Street, Asia, cobre, dólar, bonos)."""
import json, os, datetime, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
YAHOO_IPSA = ["^IPSA", "^SPIPSA"]          # se usa el primero que responda
TV_INDICES = ["BCS:SP_IPSA", "BCS:IPSA", "BCS:MXIPSA", "BCS:MXIPSAGC", "BCS:MXIGPAGC", "BCS:IGPA", "BCS:SP_IGPA"]
CTX = ["SP:SPX", "NASDAQ:NDX", "DJ:DJI", "TVC:NI225", "TVC:HSI", "SSE:000001", "TVC:KOSPI", "BMFBOVESPA:IBOV", "BMV:ME",
       "TVC:SX5E", "XETR:DAX", "FX_IDC:USDCLP", "FX:USDCLP", "COMEX:HG1!", "TVC:UKOIL", "TVC:USOIL", "TVC:GOLD",
       "TVC:US10Y", "TVC:CL10Y", "TVC:DXY", "CAPITALCOM:COPPER", "TVC:COPPER"]
COLS = ["name", "description", "close", "change", "change_abs", "volume", "Value.Traded", "average_volume_10d_calc",
        "market_cap_basic", "time", "Perf.W", "Perf.1M", "Perf.YTD", "type", "country"]


def get(url, data=None, extra=None):
    h = {"User-Agent": UA}
    h.update(extra or {})
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=40).read().decode())


def yahoo(sym, rng, interval):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range={rng}&interval={interval}"
    r = get(u)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    out = [{"t": ts, "o": q["open"][i], "h": q["high"][i], "l": q["low"][i], "c": q["close"][i], "v": q["volume"][i]}
           for i, ts in enumerate(r.get("timestamp") or []) if q["close"][i] is not None]
    return {"simbolo": sym, "meta": {k: r["meta"].get(k) for k in ("currency", "exchangeTimezoneName", "regularMarketPrice", "chartPreviousClose")}, "velas": out}


TVH = {"Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/", "Content-Type": "application/json"}


def tv(tickers):
    r = get("https://scanner.tradingview.com/global/scan", json.dumps({"symbols": {"tickers": tickers}, "columns": COLS}).encode(), TVH)
    return {x["s"]: dict(zip(COLS, x["d"])) for x in r.get("data", [])}


def tv_chile():
    body = {"columns": COLS, "range": [0, 300], "filter": [{"left": "type", "operation": "in_range", "right": ["stock", "dr", "fund"]}],
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}}
    r = get("https://scanner.tradingview.com/chile/scan", json.dumps(body).encode(), TVH)
    return {x["s"]: dict(zip(COLS, x["d"])) for x in r.get("data", [])}


def main():
    res = {"generado": datetime.datetime.utcnow().isoformat() + "Z", "errores": []}
    for sym in YAHOO_IPSA:
        try:
            res["ipsa_diario"] = yahoo(sym, "2y", "1d")
            res["ipsa_intradia"] = yahoo(sym, "5d", "5m")
            break
        except Exception as e:
            res["errores"].append(f"yahoo {sym}: {e}")
    try:
        res["tv"] = tv(TV_INDICES + CTX)
    except Exception as e:
        res["errores"].append(f"tradingview: {e}")
    try:
        res["chile"] = tv_chile()
    except Exception as e:
        res["errores"].append(f"tradingview chile: {e}")
    fecha = (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).date().isoformat()
    try:
        fecha = (datetime.datetime.utcfromtimestamp(res["ipsa_diario"]["velas"][-1]["t"]) - datetime.timedelta(hours=3)).date().isoformat()
    except Exception:
        pass
    os.makedirs(os.path.join(ROOT, "datos"), exist_ok=True)
    p = os.path.join(ROOT, "datos", f"mercado-{fecha}.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    print("escrito", p, "errores:", res["errores"], "chile:", len(res.get("chile", {})), "tv:", sorted(res.get("tv", {})))


if __name__ == "__main__":
    main()
