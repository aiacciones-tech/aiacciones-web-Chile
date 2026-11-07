"""Datos de la sesión de Tadawul para el vídeo diario en árabe de @SaudiArabiaAIStocks (saudi/diario/).
Corre en GitHub Actions (datos-diario-saudi.yml); también funciona desde el contenedor de Claude si llega a TradingView.
uso: python3 saudi/diario/datos_mercado.py  -> saudi/diario/datos/mercado-<fecha>.json
Fuentes: TradingView (velas diarias e intradía de TASI, TADAWUL:TASI, y de Nomu, TADAWUL:NOMUC; cambio, volumen y valor negociado
de todas las acciones del mercado principal y de Nomu; contexto: Brent, Wall Street, Asia, Golfo, bonos, oro). Yahoo Finance como respaldo."""
import json, os, datetime, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
INDICES = {"tasi": ["TADAWUL:TASI"], "nomu": ["TADAWUL:NOMUC"]}   # velas: el primero que responda
YAHOO = {"tasi": ["^TASI.SR"], "nomu": ["^NOMUC.SR"]}  # respaldo
CTX = ["TADAWUL:TASI", "TADAWUL:NOMUC", "TADAWUL:2222", "ADX:FADGI", "DFM:DFMGI", "TVC:UKOIL", "TVC:USOIL", "ICEEUR:BRN1!", "NYMEX:CL1!", "FX:UKOIL", "OANDA:BCOUSD", "SP:SPX", "NASDAQ:NDX", "DJ:DJI", "TVC:NI225", "TVC:HSI", "SSE:000001",
       "TVC:KOSPI", "QSE:GNRI", "BAHRAIN:BAX", "EGX:EGX30", "TVC:SA10Y", "TVC:SX5E", "TVC:UKX", "TVC:GOLD", "TVC:US10Y", "TVC:US02Y", "TVC:DXY", "FX_IDC:USDSAR"]
CTX_VELAS = ["ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "ICEEUR:BRN1!", "SP:SPX", "NASDAQ:NDX", "TVC:NI225", "TVC:HSI", "TVC:KOSPI", "SSE:000001",
             "TVC:SX5E", "TVC:GOLD", "TVC:US10Y", "TADAWUL:2222"]
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
    """Todas las acciones de Tadawul, mercado principal y Nomu (para los 5 que más suben y bajan del TASI)."""
    body = {"columns": COLS + ["typespecs", "subtype", "indexes"], "range": [0, 600], "filter": [{"left": "type", "operation": "equal", "right": "stock"},
            {"left": "exchange", "operation": "equal", "right": "TADAWUL"}], "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}}
    r = get("https://scanner.tradingview.com/ksa/scan", json.dumps(body).encode(), TVH)
    cols = body["columns"]
    return {x["s"]: dict(zip(cols, x["d"])) for x in r.get("data", [])}
    return {x["s"]: dict(zip(COLS, x["d"])) for x in r.get("data", [])}


def tv_buscar(texto, bolsa):
    u = "https://symbol-search.tradingview.com/symbol_search/v3/?" + urllib.parse.urlencode({"text": texto, "exchange": bolsa, "hl": "0", "lang": "en", "domain": "production"})
    try:
        r = get(u, extra={"Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/"})
        return [{k: x.get(k) for k in ("symbol", "description", "type", "exchange")} for x in r.get("symbols", [])]
    except Exception as e:
        return [{"error": str(e)}]


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


def main():
    res = {"generado": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z", "errores": []}
    res["busqueda"] = {"tasi": tv_buscar("TASI", "TADAWUL"), "nomu": tv_buscar("NOMUC", "TADAWUL")}
    for k in ("tasi", "nomu"):
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
    # Velas diarias recientes del contexto: el cambio del día de la sesión (Golfo y Asia) y del cierre anterior (Wall Street, Europa),
    # porque el escáner solo da el último cambio y la sesión de Tadawul cierra antes de que abra Wall Street.
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
    fecha = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=3)).date().isoformat()
    try:
        fecha = datetime.datetime.utcfromtimestamp(res["tasi_diario"]["velas"][-1]["t"] + 3 * 3600).date().isoformat()  # vela diaria: fecha de la sesión (hora de Riad)
    except Exception:
        pass
    # Solo hay video los días en que abre Tadawul (domingo a jueves): si la última vela no es de hoy (hora de Riad), fue festivo y no se guarda nada.
    hoy = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=3)).date().isoformat()
    res["sesion"] = fecha
    if os.environ.get("SOLO_DIA_DE_SESION") == "1" and fecha != hoy:
        print(f"Sin sesión hoy ({hoy}): la última vela es del {fecha}. Tadawul cerrado (fin de semana o festivo); no hay video."); return
    os.makedirs(os.path.join(ROOT, "datos"), exist_ok=True)
    p = os.path.join(ROOT, "datos", f"mercado-{fecha}.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    print("escrito", p, "errores:", res["errores"], "acciones:", len(res.get("acciones", {})), "busqueda:", res["busqueda"],
          {k: (res.get(f"{k}_diario", {}).get("simbolo"), len(res.get(f"{k}_diario", {}).get("velas", [])), len(res.get(f"{k}_intradia", {}).get("velas", []))) for k in ("tasi", "nomu")})


if __name__ == "__main__":
    main()
