# Respaldo (10-nov-2026): si el websocket de TradingView no entrega series, datos_mercado.py cae en Yahoo Finance, que hoy
# solo da la vela del día para ^TASI.SR y ^NOMUC.SR. Este script rehace el histórico diario con las velas de TradingView
# del mercado.json de la sesión anterior y añade la vela de hoy (apertura, máximo y mínimo de Yahoo; cierre y volumen
# del escáner de TradingView, mismas unidades que el histórico).
# Uso: python3 completar_velas.py <mercado de hoy.json> <mercado de la sesión anterior.json>
import json, sys
hoy, ant = sys.argv[1], sys.argv[2]
N, P = json.load(open(hoy)), json.load(open(ant))
for k, sym in (("tasi", "TADAWUL:TASI"), ("nomu", "TADAWUL:NOMUC")):
    d = N.get(f"{k}_diario") or {}
    if d.get("fuente") == "TradingView" or len(d.get("velas", [])) > 5:
        continue
    y = d["velas"][-1]; tv = N["tv"][sym]; prev = P[f"{k}_diario"]["velas"]
    vela = {"t": prev[-1]["t"] + 86400 * max(1, round((y["t"] - prev[-1]["t"]) / 86400)), "o": y["o"], "h": y["h"], "l": y["l"],
            "c": tv["close"], "v": tv.get("volume")}
    N[f"{k}_diario"] = {"simbolo": sym, "fuente": "TradingView (histórico hasta la sesión anterior) + Yahoo Finance/TradingView (vela de hoy)",
                        "velas": prev[1:] + [vela] if prev[-1]["t"] < vela["t"] else prev}
# Contexto sin histórico en Yahoo (Abu Dabi, Dubái, Qatar): dos velas a partir del cierre y el cambio del escáner de TradingView.
for sym, v in N.get("ctx_velas", {}).items():
    tv = N.get("tv", {}).get(sym)
    if len(v) < 2 and tv and tv.get("close") and tv.get("change") is not None:
        c0 = tv["close"] / (1 + tv["change"] / 100)
        N["ctx_velas"][sym] = [{"t": tv["time"] - 86400, "o": c0, "h": c0, "l": c0, "c": c0, "v": None},
                               {"t": tv["time"], "o": tv["close"], "h": tv["close"], "l": tv["close"], "c": tv["close"], "v": None}]
json.dump(N, open(hoy, "w"), ensure_ascii=False)
print("ok", {k: N[f"{k}_diario"]["velas"][-1] for k in ("tasi", "nomu")})
