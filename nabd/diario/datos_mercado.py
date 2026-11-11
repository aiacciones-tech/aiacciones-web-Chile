"""Datos de la sesión de Wall Street para el vídeo diario en árabe de Nabd Wall Street (نبض وول ستريت, nabd/diario/).
Corre en GitHub Actions (datos-diario-Nabd.yml); el contenedor de Claude no llega a TradingView ni a Yahoo.
uso: python3 nabd/diario/datos_mercado.py  -> nabd/diario/datos/mercado-<fecha>.json
Fuentes: TradingView (velas diarias e intradía del S&P 500, Nasdaq Composite, Dow Jones y Russell 2000; cambio, volumen y valor
negociado de las acciones del S&P 500; contexto: Golfo, Europa, Asia, petróleo, oro, bonos, dólar, VIX, bitcóin). Yahoo Finance como respaldo."""
import json, os, datetime, urllib.request, urllib.parse
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.abspath(__file__))
NY = ZoneInfo("America/New_York")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
INDICES = {"spx": ["SP:SPX"], "ndq": ["NASDAQ:IXIC"], "dji": ["DJ:DJI"], "rut": ["TVC:RUT", "RUSSELL:RUT", "CBOE:RUT"], "ndx": ["NASDAQ:NDX"]}   # velas: el primero que responda
YAHOO = {"spx": ["^GSPC"], "ndq": ["^IXIC"], "dji": ["^DJI"], "rut": ["^RUT"], "ndx": ["^NDX"]}  # respaldo
N_VELAS = 5000   # unos 20 años de sesiones: el máximo histórico del S&P 500, Nasdaq 100 y Dow Jones cae dentro
SECTORES = ["AMEX:XLK", "AMEX:XLF", "AMEX:XLE", "AMEX:XLV", "AMEX:XLY", "AMEX:XLI"]  # ETF sectoriales SPDR (manual de producción, 10-nov-2026)
INTRADIA = ("spx",)
CTX = ["SP:SPX", "NASDAQ:IXIC", "DJ:DJI", "NASDAQ:NDX", "TVC:VIX", "TVC:UKOIL", "TVC:USOIL", "TVC:GOLD", "TVC:US10Y", "TVC:US02Y", "TVC:DXY",
       "BITSTAMP:BTCUSD", "TADAWUL:TASI", "ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "TVC:SX5E", "TVC:UKX", "XETR:DAX", "TVC:NI225", "TVC:HSI"] + SECTORES
CTX_VELAS = ["TVC:VIX", "TVC:UKOIL", "TVC:GOLD", "TVC:US10Y", "TVC:DXY", "BITSTAMP:BTCUSD", "NASDAQ:NDX",
             "TADAWUL:TASI", "ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "TVC:SX5E", "XETR:DAX", "TVC:UKX", "TVC:NI225", "TVC:HSI", "TVC:USOIL"] + SECTORES
COLS = ["name", "description", "close", "change", "change_abs", "volume", "Value.Traded", "average_volume_10d_calc",
        "market_cap_basic", "time", "Perf.W", "Perf.1M", "Perf.YTD", "type", "exchange", "sector"]


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
    """Acciones grandes de EE. UU. (más de 4.000 millones de dólares de capitalización); las del S&P 500 se distinguen por su campo `indexes`."""
    body = {"columns": COLS + ["typespecs", "subtype", "indexes"], "range": [0, 1200],
            "filter": [{"left": "type", "operation": "equal", "right": "stock"}, {"left": "is_primary", "operation": "equal", "right": True},
                       {"left": "market_cap_basic", "operation": "greater", "right": 4e9}],
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}}
    r = get("https://scanner.tradingview.com/america/scan", json.dumps(body).encode(), TVH)
    cols = body["columns"]
    return {x["s"]: dict(zip(cols, x["d"])) for x in r.get("data", [])}


def tv_velas(simbolo, resol="1D", n=500):
    """Velas históricas de TradingView por su websocket público (sin cuenta, datos con el retraso habitual)."""
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
        raise RuntimeError("símbolo no válido en TradingView: " + simbolo)
    for m in re.finditer(r'"s":\[(\{"i":.*?)\],"ns"', buf):
        arr = json.loads("[" + m.group(1) + "]")
        velas = [{"t": int(x["v"][0]), "o": x["v"][1], "h": x["v"][2], "l": x["v"][3], "c": x["v"][4], "v": (x["v"][5] if len(x["v"]) > 5 else None)} for x in arr]
    if not velas:
        raise RuntimeError("sin velas para " + simbolo)
    return {"simbolo": simbolo, "fuente": "TradingView", "velas": velas}


def candidatas(acc, n=8):
    """Acciones del S&P 500 que pueden ser protagonistas del día: las que más suben y bajan (más de 50 millones de dólares negociados),
    las de mayor valor negociado y las de volumen más alto frente a su media de 10 sesiones. De ellas se descargan velas para su gráfico."""
    L = [(t, v) for t, v in acc.items() if any(i.get("proname") == "SP:SPX" for i in (v.get("indexes") or []))
         and v.get("change") is not None and (v.get("Value.Traded") or 0) >= 50e6]
    rel = lambda v: (v.get("volume") or 0) / v["average_volume_10d_calc"] if v.get("average_volume_10d_calc") else 0
    out = []
    for key, rev in ((lambda x: x[1]["change"], True), (lambda x: x[1]["change"], False), (lambda x: x[1].get("Value.Traded") or 0, True),
                     (lambda x: rel(x[1]) if (x[1].get("Value.Traded") or 0) >= 100e6 else 0, True)):
        out += [t for t, _ in sorted(L, key=key, reverse=rev)[:n]]
    return list(dict.fromkeys(out))


def fecha_vela(t):
    """Fecha de la sesión de una vela diaria (TradingView la marca a las 00:00 UTC o a la apertura; las dos caen en el mismo día UTC)."""
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).date()


def mercado_cerrado(ahora=None):
    """True fuera del horario de la bolsa (antes de las 9:30 o después de las 16:15 en Nueva York, o en fin de semana)."""
    a = ahora or datetime.datetime.now(NY)
    return a.weekday() >= 5 or not (datetime.time(9, 30) <= a.time() <= datetime.time(16, 15))


def main():
    res = {"generado": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z", "errores": []}
    for k in INDICES:
        for sym in INDICES[k]:
            try:
                res[f"{k}_diario"] = tv_velas(sym, "1D", N_VELAS)
                if k in INTRADIA: res[f"{k}_intradia"] = tv_velas(sym, "5", 600)
                break
            except Exception as e:
                res["errores"].append(f"tv velas {sym}: {e}")
        if f"{k}_diario" not in res:
            for sym in YAHOO[k]:
                try:
                    res[f"{k}_diario"] = yahoo(sym, "max", "1d")
                    if k in INTRADIA: res[f"{k}_intradia"] = yahoo(sym, "5d", "5m")
                    break
                except Exception as e:
                    res["errores"].append(f"yahoo {sym}: {e}")
    try:
        res["tv"] = tv(CTX)
    except Exception as e:
        res["errores"].append(f"tradingview: {e}")
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
    res["acciones_velas"] = {}
    for t in candidatas(res.get("acciones", {})):
        try:
            res["acciones_velas"][t] = [{k_: v[k_] for k_ in "tohlcv"} for v in tv_velas(t, "1D", 70)["velas"]]
        except Exception as e:
            res["errores"].append(f"tv velas {t}: {e}")
    hoy = datetime.datetime.now(NY).date().isoformat()
    fecha = hoy
    try:
        fecha = fecha_vela(res["spx_diario"]["velas"][-1]["t"]).isoformat()
    except Exception:
        pass
    res["sesion"] = fecha
    # Solo hay video los días en que abre la bolsa de Nueva York: si la última vela no es de hoy (hora de Nueva York), fue festivo y no se guarda nada.
    if os.environ.get("SOLO_DIA_DE_SESION") == "1" and fecha != hoy:
        print(f"Sin sesión hoy ({hoy}): la última vela es del {fecha}. Bolsa de Nueva York cerrada (fin de semana o festivo); no hay video."); return
    os.makedirs(os.path.join(ROOT, "datos"), exist_ok=True)
    p = os.path.join(ROOT, "datos", f"mercado-{fecha}.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    n500 = sum(1 for v in res.get("acciones", {}).values() if any(i.get("proname") == "SP:SPX" for i in (v.get("indexes") or [])))
    print("escrito", p, "errores:", res["errores"], "acciones:", len(res.get("acciones", {})), "en el S&P 500:", n500,
          {k: (res.get(f"{k}_diario", {}).get("simbolo"), len(res.get(f"{k}_diario", {}).get("velas", [])), len(res.get(f"{k}_intradia", {}).get("velas", []))) for k in INDICES})
    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        open(gh, "a").write(f"cerrado={'1' if mercado_cerrado() else '0'}\n")


if __name__ == "__main__":
    main()
