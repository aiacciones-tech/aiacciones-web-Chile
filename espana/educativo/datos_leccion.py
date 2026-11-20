"""Velas diarias de TradingView para una lección de «Análisis técnico, explicado fácil» (serie educativa semanal de @AIAccionesEspaña, espana/educativo/).
Corre en GitHub Actions (educativo-espana.yml): el contenedor de Claude no llega a TradingView. Las velas se congelan: si <salida>/velas.json
ya existe no se vuelven a pedir (las cifras dichas no cambian), salvo con REFRESCAR=1. Si TradingView no entrega la serie, usa Yahoo Finance
(<ticker>.MC) y lo deja escrito en "fuente" (el vídeo lo dice en pantalla).
uso: python3 datos_leccion.py <video.json> <carpeta de salida>   (video.json → "simbolo", p. ej. "BME:ITX"; "velas_n" opcional, 760)"""
import json, os, sys, time, random, string, re, urllib.request, urllib.parse, datetime as dt

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def tv_velas(simbolo, resol="1D", n=760):
    """Velas históricas de TradingView por su websocket público (sin cuenta), igual que el resto de canales."""
    import websocket
    ws = websocket.create_connection("wss://data.tradingview.com/socket.io/websocket?type=chart",
                                     header=["Origin: https://www.tradingview.com", "User-Agent: " + UA], timeout=30)
    def send(m, p):
        msg = json.dumps({"m": m, "p": p}, separators=(",", ":")); ws.send(f"~m~{len(msg)}~m~{msg}")
    cs = "cs_" + "".join(random.choice(string.ascii_lowercase) for _ in range(12))
    send("set_auth_token", ["unauthorized_user_token"]); send("chart_create_session", [cs, ""])
    send("resolve_symbol", [cs, "s1", "=" + json.dumps({"symbol": simbolo, "adjustment": "splits"})])
    send("create_series", [cs, "sds_1", "s1", "s1", resol, n, ""])
    buf, velas, fin = "", None, time.time() + 45
    for _ in range(300):
        if time.time() > fin: ws.close(); raise RuntimeError("TradingView no devolvió la serie a tiempo: " + simbolo)
        r = ws.recv(); buf += r
        for hb in re.findall(r"~m~\d+~m~(~h~\d+)", r): ws.send(f"~m~{len(hb)}~m~{hb}")
        if "series_completed" in r or "symbol_error" in r or "series_error" in r: break
    ws.close()
    if "symbol_error" in buf or "series_error" in buf: raise RuntimeError("símbolo no válido en TradingView: " + simbolo)
    for m in re.finditer(r'"s":\[(\{"i":.*?)\],"ns"', buf):
        arr = json.loads("[" + m.group(1) + "]")
        velas = [{"t": int(x["v"][0]), "o": x["v"][1], "h": x["v"][2], "l": x["v"][3], "c": x["v"][4], "v": (x["v"][5] if len(x["v"]) > 5 else None)} for x in arr]
    if not velas: raise RuntimeError("sin velas para " + simbolo)
    return {"simbolo": simbolo, "fuente": "TradingView", "velas": velas}


def yahoo(sym, rng="3y"):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range={rng}&interval=1d"
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    return {"simbolo": sym, "fuente": "Yahoo Finance", "velas": [{"t": ts, "o": q["open"][i], "h": q["high"][i], "l": q["low"][i], "c": q["close"][i], "v": q["volume"][i]}
                                                         for i, ts in enumerate(r.get("timestamp") or []) if q["close"][i] is not None]}


if __name__ == "__main__":
    VJ = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); p = os.path.join(out, "velas.json")
    if os.path.exists(p) and not os.environ.get("REFRESCAR"):
        print("velas ya congeladas:", p); sys.exit()
    D = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "series": {}}
    for s in [VJ["simbolo"]] + VJ.get("simbolos_extra", []):
        try:
            D["series"][s] = tv_velas(s, "1D", VJ.get("velas_n", 760))
        except Exception as e:
            print("TradingView falló:", e, "-> Yahoo"); D["series"][s] = yahoo(s.split(":")[1] + ".MC"); D["series"][s]["simbolo"] = s
        v = D["series"][s]["velas"]
        print(s, D["series"][s]["fuente"], len(v), "velas, última", dt.datetime.fromtimestamp(v[-1]["t"], dt.timezone.utc).date(), v[-1]["c"])
    json.dump(D, open(p, "w"))
