"""Session data from Bahrain Bourse for the daily Arabic video of @BahrainAIStocks (bahrain/daily-bahrain/).
Runs in GitHub Actions (daily-data-bahrain.yml); TradingView is blocked from Claude's container.
usage: python3 bahrain/daily-bahrain/market-data-bahrain.py  -> bahrain/daily-bahrain/data/market-<date>-bahrain.json
Sources: TradingView (daily and 5-minute candles of the Bahrain All Share Index, BAHRAIN:BAX; change, volume and traded value
of every Bahrain Bourse stock; context: Gulf, Asia, Wall Street, Europe, Brent, gold, bonds). Yahoo Finance as fallback."""
import json, os, datetime, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
INDICES = {"bax": ["BAHRAIN:BHBX", "BHB:BHBX", "BAHRAIN:BAX"]}   # candles: the first one that answers
YAHOO = {"bax": ["^BAX", "BHSEASI.BH"]}
CTX = ["BAHRAIN:BHBX", "BAHRAIN:BIX", "TADAWUL:TASI", "ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "BAHRAIN:BHBX", "TVC:UKOIL", "ICEEUR:BRN1!", "SP:SPX", "NASDAQ:NDX",
       "DJ:DJI", "TVC:NI225", "TVC:HSI", "SSE:000001", "TVC:KOSPI", "EGX:EGX30", "TVC:SX5E", "TVC:UKX", "TVC:GOLD", "TVC:US10Y", "TVC:US02Y", "TVC:DXY"]
CTX_VELAS = ["TADAWUL:TASI", "ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "ICEEUR:BRN1!", "SP:SPX", "NASDAQ:NDX", "TVC:NI225", "TVC:HSI",
             "TVC:KOSPI", "SSE:000001", "TVC:SX5E", "TVC:GOLD", "TVC:US10Y", "KSE:BKP", "MSM:MSX30"]
COLS = ["name", "description", "close", "change", "change_abs", "volume", "Value.Traded", "average_volume_10d_calc",
        "market_cap_basic", "time", "Perf.W", "Perf.1M", "Perf.YTD", "type", "exchange", "sector", "currency"]


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
    return {"simbolo": sym, "fuente": "Yahoo Finance", "velas": out}


TVH = {"Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/", "Content-Type": "application/json"}


def tv(tickers):
    r = get("https://scanner.tradingview.com/global/scan", json.dumps({"symbols": {"tickers": tickers}, "columns": COLS}).encode(), TVH)
    return {x["s"]: dict(zip(COLS, x["d"])) for x in r.get("data", [])}


def tv_acciones():
    """Every Bahrain Bourse stock (for the 5 biggest gainers and losers)."""
    cols = COLS + ["typespecs", "subtype", "indexes"]
    body = {"columns": cols, "range": [0, 300], "filter": [{"left": "exchange", "operation": "equal", "right": "BAHRAIN"}], "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}}
    err = None
    for mk in ("bahrain", "global"):
        try:
            r = get(f"https://scanner.tradingview.com/{mk}/scan", json.dumps(body).encode(), TVH)
            if r.get("data"):
                return {x["s"]: dict(zip(cols, x["d"])) for x in r["data"]}
        except Exception as e:
            err = e
    raise RuntimeError(f"scanner without Bahrain stocks: {err}")


def tv_buscar(texto, bolsa):
    u = "https://symbol-search.tradingview.com/symbol_search/v3/?" + urllib.parse.urlencode({"text": texto, "exchange": bolsa, "hl": "0", "lang": "en", "domain": "production"})
    try:
        r = get(u, extra={"Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/"})
        return [{k: x.get(k) for k in ("symbol", "description", "type", "exchange")} for x in r.get("symbols", [])]
    except Exception as e:
        return [{"error": str(e)}]


def tv_velas(simbolo, resol="1D", n=500):
    """Historical candles from TradingView's public websocket (no account, usual delay)."""
    import random, string, re, websocket
    ws = websocket.create_connection("wss://data.tradingview.com/socket.io/websocket?type=chart",
                                     header=["Origin: https://www.tradingview.com", "User-Agent: " + UA], timeout=30)
    def send(m, p):
        msg = json.dumps({"m": m, "p": p}, separators=(",", ":"))
        ws.send(f"~m~{len(msg)}~m~{msg}")
    cs = "cs_" + "".join(random.choice(string.ascii_lowercase) for _ in range(12))
    send("set_auth_token", ["unauthorized_user_token"])
    send("chart_create_session", [cs, ""])
    send("resolve_symbol", [cs, "s1", "=" + json.dumps({"symbol": simbolo, "adjustment": "splits"})])
    send("create_series", [cs, "sds_1", "s1", "s1", resol, n, ""])
    buf, velas = "", None
    for _ in range(200):
        r = ws.recv(); buf += r
        for hb in re.findall(r"~m~\d+~m~(~h~\d+)", r):
            ws.send(f"~m~{len(hb)}~m~{hb}")
        if "series_completed" in r or "symbol_error" in r or "series_error" in r:
            break
    ws.close()
    if "symbol_error" in buf or "series_error" in buf:
        import re as _re
        raise RuntimeError("invalid TradingView symbol: " + simbolo + " " + " | ".join(_re.findall(r'"m":"(?:symbol_error|series_error)","p":\[[^\]]*\]', buf))[:300])
    for m in re.finditer(r'"s":\[(\{"i":.*?)\],"ns"', buf):
        arr = json.loads("[" + m.group(1) + "]")
        velas = [{"t": int(x["v"][0]), "o": x["v"][1], "h": x["v"][2], "l": x["v"][3], "c": x["v"][4], "v": (x["v"][5] if len(x["v"]) > 5 else None)} for x in arr]
    if not velas:
        raise RuntimeError("no candles for " + simbolo)
    return {"simbolo": simbolo, "fuente": "TradingView", "velas": velas}


def main():
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    res = {"generado": now.isoformat() + "Z", "errores": []}
    res["busqueda"] = {"bax": tv_buscar("BHBX", "BAHRAIN"), "all_share": tv_buscar("Bahrain All Share", "")}
    for k in INDICES:
        for sym in INDICES[k]:
            try:
                res[f"{k}_diario"] = tv_velas(sym, "1D", 520)
                res[f"{k}_intradia"] = tv_velas(sym, "5", 600)
                break
            except Exception as e:
                res["errores"].append(f"tv velas {sym}: {e}")
        if f"{k}_diario" not in res:
            for sym in YAHOO[k]:
                try:
                    res[f"{k}_diario"] = yahoo(sym, "2y", "1d"); res[f"{k}_intradia"] = yahoo(sym, "5d", "5m"); break
                except Exception as e:
                    res["errores"].append(f"yahoo {sym}: {e}")
    try:
        res["tv"] = tv(CTX)
    except Exception as e:
        res["errores"].append(f"tradingview: {e}")
    # Recent daily candles of the context: same-day change (Gulf, Asia) and previous close (Wall Street, Europe),
    # because the scanner only gives the latest change and Bahrain Bourse closes (13:00 Manama) before Wall Street opens.
    res["ctx_velas"] = {}
    for sym in CTX_VELAS:
        try:
            res["ctx_velas"][sym] = tv_velas(sym, "1D", 15)["velas"]
        except Exception as e:
            res["errores"].append(f"tv ctx {sym}: {e}")
    try:
        res["acciones"] = tv_acciones()
    except Exception as e:
        res["errores"].append(f"tradingview acciones: {e}")
    hoy = (now + datetime.timedelta(hours=3)).date().isoformat()  # Manama time (UTC+3, no DST)
    fecha = hoy
    try:
        fecha = datetime.datetime.utcfromtimestamp(res["bax_diario"]["velas"][-1]["t"] + 3 * 3600).date().isoformat()
    except Exception:
        pass
    res["sesion"] = fecha
    # Video only on days Bahrain Bourse opens (Sunday to Thursday): if the last candle is not today's, it was a holiday and nothing is saved.
    if os.environ.get("SOLO_DIA_DE_SESION") == "1" and fecha != hoy:
        print(f"No session today ({hoy}): last candle is from {fecha}. Bahrain Bourse closed (weekend or holiday); no video."); return
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    p = os.path.join(ROOT, "data", f"market-{fecha}-bahrain.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    print("written", p, "errors:", res["errores"], "stocks:", len(res.get("acciones", {})), "search:", res["busqueda"],
          {k: (res.get(f"{k}_diario", {}).get("simbolo"), len(res.get(f"{k}_diario", {}).get("velas", [])), len(res.get(f"{k}_intradia", {}).get("velas", []))) for k in INDICES})


if __name__ == "__main__":
    main()
