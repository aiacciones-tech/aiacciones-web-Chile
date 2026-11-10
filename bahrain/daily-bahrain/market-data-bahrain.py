"""Session data from Bahrain Bourse for the daily Arabic video of @BahrainAIStocks (bahrain/daily-bahrain/).
Runs in GitHub Actions (daily-data-bahrain.yml); these hosts are blocked from Claude's container.
usage: python3 bahrain/daily-bahrain/market-data-bahrain.py  -> bahrain/daily-bahrain/data/market-<date>-bahrain.json
Sources: Mubasher (daily candles of the Bahrain All Share Index BHBX since 2006, 1-minute intraday of the session, and price, change,
volume and turnover of every Bahrain Bourse stock); CNBC (.BAX daily candles) as fallback; TradingView scanner (BHBX close,
currency of each stock, and context: Gulf, Asia, Wall Street, Europe, Brent, gold, bonds). TradingView charts of Bahrain
need a paid data package ("permission denied, group bahrain_dly"), so the index candles do not come from there."""
import json, os, datetime, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
MUB = "https://static.mubasher.info/File.MubasherCharts/File.{}_Charts_Dir/33182be0c5cdcd5072bb1864cdee4d3d6e.csv"  # BHBX on Mubasher
MUB_HIST, MUB_INTRA = MUB.format("Historical_Index"), MUB.format("Delay_Index_Intraday")
MUB_PRICES = "https://english.mubasher.info/api/1/stocks/prices/all?country=bh"
CNBC = "https://ts-api.cnbc.com/harmony/app/charts/1Y.json?symbol=.BAX"
TZH = 3 * 3600  # Manama, UTC+3
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


def txt(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")


def mub_csv(url, fuente):
    """Mubasher chart CSV: 'YYYY-MM-DD/HH:MM:SS,open,high,low,close,volume' in Manama time -> candles with t in UTC epoch."""
    out = []
    for l in txt(url).splitlines():
        p = l.strip().split(",")
        if len(p) < 6: continue
        d = datetime.datetime.strptime(p[0], "%Y-%m-%d/%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        out.append({"t": int(d.timestamp()) - TZH, "o": float(p[1]), "h": float(p[2]), "l": float(p[3]), "c": float(p[4]), "v": float(p[5])})
    if not out: raise RuntimeError("empty CSV " + url)
    return {"simbolo": "BHBX", "fuente": fuente, "velas": out}


def cnbc():
    bars = get(CNBC)["barData"]["priceBars"]
    out = [{"t": int(b["tradeTimeinMills"]) // 1000, "o": float(b["open"]), "h": float(b["high"]), "l": float(b["low"]), "c": float(b["close"]), "v": b.get("volume")} for b in bars]
    return {"simbolo": ".BAX", "fuente": "CNBC", "velas": out}


def mub_acciones():
    """Every Bahrain Bourse stock on Mubasher: last price, change, turnover, volume and the time of the last trade (updatedAt, Manama)."""
    r = get(MUB_PRICES)
    num = lambda x: None if x in (None, "", "-") else float(str(x).replace(",", "").replace("%", ""))
    return {"lastUpdate": r.get("lastUpdate"), "acciones": [{"code": x["code"], "name": x["name"], "close": num(x["value"]), "change_abs": num(x["change"]),
            "change": num(x["changePercentage"]), "turnover": num(x["turnover"]), "volume": num(x["volume"]), "open": num(x["open"]),
            "high": num(x["high"]), "low": num(x["low"]), "updatedAt": x.get("updatedAt")} for x in r.get("prices", [])]}


TVH = {"Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/", "Content-Type": "application/json"}


def tv(tickers):
    r = get("https://scanner.tradingview.com/global/scan", json.dumps({"symbols": {"tickers": tickers}, "columns": COLS}).encode(), TVH)
    return {x["s"]: dict(zip(COLS, x["d"])) for x in r.get("data", [])}


def tv_acciones():
    """Every Bahrain Bourse stock (for the 5 biggest gainers and losers)."""
    # Technical columns of each stock as TradingView's scanner computes them (daily), for the stocks scene of the technical analysis.
    cols = COLS + ["typespecs", "subtype", "indexes", "RSI", "SMA50", "SMA200", "Stoch.K", "Stoch.D", "Perf.3M", "Perf.6M",
                   "price_52_week_high", "price_52_week_low", "ATR", "Volatility.M"]
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
    for k, fn in (("bax_diario", lambda: mub_csv(MUB_HIST, "Mubasher")), ("bax_diario", cnbc), ("bax_intradia", lambda: mub_csv(MUB_INTRA, "Mubasher"))):
        if k in res: continue
        try:
            res[k] = fn()
        except Exception as e:
            res["errores"].append(f"{k}: {e}")
    try:
        res["mubasher"] = mub_acciones()
    except Exception as e:
        res["errores"].append(f"mubasher acciones: {e}")
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
    dia = lambda v: datetime.datetime.utcfromtimestamp(v["t"] + TZH).date().isoformat()
    # Mubasher adds the day's daily candle hours after the close; the 1-minute intraday has it right away. If the intraday
    # has a later session than the daily candles, build that day's candle from the intraday (open, high, low, close, volume).
    try:
        d_ult = dia(res["bax_diario"]["velas"][-1])
        intra = [v for v in res["bax_intradia"]["velas"] if dia(v) == dia(res["bax_intradia"]["velas"][-1])]
        if intra and dia(intra[-1]) > d_ult:
            t0 = int(datetime.datetime.fromisoformat(dia(intra[-1])).replace(tzinfo=datetime.timezone.utc).timestamp()) - TZH
            res["bax_diario"]["velas"].append({"t": t0, "o": intra[0]["o"], "h": max(v["h"] for v in intra), "l": min(v["l"] for v in intra),
                                               "c": intra[-1]["c"], "v": sum(v["v"] or 0 for v in intra), "de_intradia": True})
    except Exception as e:
        res["errores"].append(f"daily candle from intraday: {e}")
    fecha = hoy
    try:
        fecha = datetime.datetime.utcfromtimestamp(res["bax_diario"]["velas"][-1]["t"] + TZH).date().isoformat()
    except Exception:
        pass
    res["sesion"] = fecha
    # Video only on days Bahrain Bourse opens (Sunday to Thursday): if the last candle is not today's, it was a holiday and nothing is saved.
    if os.environ.get("SOLO_DIA_DE_SESION") == "1" and fecha != hoy:
        print(f"No session today ({hoy}): last candle is from {fecha}. Bahrain Bourse closed (weekend or holiday); no video."); return
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    p = os.path.join(ROOT, "data", f"market-{fecha}-bahrain.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    print("written", p, "errors:", res["errores"], "stocks (TradingView, Mubasher):", len(res.get("acciones", {})), len(res.get("mubasher", {}).get("acciones", [])),
          {k: (res.get(k, {}).get("fuente"), len(res.get(k, {}).get("velas", []))) for k in ("bax_diario", "bax_intradia")})


if __name__ == "__main__":
    main()
