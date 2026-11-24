"""Datos de la sesión de Xetra para el Short diario «DAX am Abend» de Wall Street auf Deutsch (prueba de 4-6 semanas desde el 24-nov-2026).
Corre en GitHub Actions (datos-dax-GE.yml); el contenedor de Claude no llega a TradingView.
uso: python3 ge/dax/datos_dax.py  -> ge/dax/datos/dax-<fecha>.json  (el workflow lo guarda en la rama datos-dax-ge)
Fuente: TradingView (velas diarias del DAX; cotizaciones del DAX, MDAX, TecDAX, Euro Stoxx 50, EUR/USD y Bund a 10 años;
las 40 acciones del DAX con cambio, volumen y media de volumen). Reutiliza tv_velas() de nabd/diario/datos_mercado.py (solo lo importa)."""
import json, os, sys, datetime
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "..", "..", "nabd", "diario"))
from datos_mercado import tv_velas, get, TVH, UA  # noqa: E402
BERLIN = ZoneInfo("Europe/Berlin")
CTX = ["XETR:DAX", "XETR:MDAX", "XETR:TDXP", "TVC:SX5E", "FX:EURUSD", "TVC:DE10Y", "SP:SPX", "NASDAQ:NDX"]
COLS = ["name", "description", "close", "change", "change_abs", "volume", "Value.Traded", "average_volume_10d_calc",
        "market_cap_basic", "Perf.W", "Perf.1M", "Perf.YTD", "sector", "exchange", "type"]
# Respaldo por si el campo `indexes` de TradingView no trae el DAX: composición del DAX 40 a noviembre de 2026 según TradingView.
# Si cambia la composición (revisiones de marzo, junio, septiembre y diciembre), el campo `indexes` manda.
DAX40 = ["ADS", "AIR", "ALV", "BAS", "BAYN", "BEI", "BMW", "BNR", "CBK", "CON", "DB1", "DBK", "DHL", "DTE", "DTG", "ENR", "EOAN", "FRE",
         "G1A", "HEI", "HEN3", "HNR1", "IFX", "MBG", "MRK", "MTX", "MUV2", "P911", "PAH3", "QIA", "RHM", "RWE", "SAP", "SHL", "SIE",
         "SRT3", "SY1", "VNA", "VOW3", "ZAL"]


def tv(tickers, cols=COLS):
    r = get("https://scanner.tradingview.com/global/scan", json.dumps({"symbols": {"tickers": tickers}, "columns": cols}).encode(), TVH)
    return {x["s"]: dict(zip(cols, x["d"])) for x in r.get("data", [])}


def miembros_dax():
    """Acciones de Xetra cuyo campo `indexes` incluye el DAX. Si salen menos de 35, se usa la lista DAX40 de respaldo."""
    cols = COLS + ["indexes"]
    body = {"columns": cols, "range": [0, 400],
            "filter": [{"left": "exchange", "operation": "equal", "right": "XETR"}, {"left": "type", "operation": "equal", "right": "stock"}],
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}}
    r = get("https://scanner.tradingview.com/germany/scan", json.dumps(body).encode(), TVH)
    todos = {x["s"]: dict(zip(cols, x["d"])) for x in r.get("data", [])}
    dax = {s: v for s, v in todos.items() if any((i or {}).get("proname") == "XETR:DAX" for i in (v.get("indexes") or []))}
    if len(dax) >= 35:
        return dax, "indexes"
    return tv(["XETR:" + t for t in DAX40]), "lista"


def main():
    res = {"generado": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z", "errores": []}
    try:
        res["dax_diario"] = tv_velas("XETR:DAX", "1D", 5000)
    except Exception as e:
        res["errores"].append(f"tv velas DAX: {e}")
    try:
        res["tv"] = tv(CTX)
    except Exception as e:
        res["errores"].append(f"tradingview ctx: {e}")
    res["ctx_velas"] = {}
    for s in ["XETR:MDAX", "XETR:TDXP", "TVC:SX5E", "FX:EURUSD", "TVC:DE10Y"]:
        try:
            res["ctx_velas"][s] = [{k: v[k] for k in "tohlc"} for v in tv_velas(s, "1D", 15)["velas"]]
        except Exception as e:
            res["errores"].append(f"tv ctx {s}: {e}")
    try:
        res["acciones"], res["acciones_origen"] = miembros_dax()
    except Exception as e:
        res["errores"].append(f"tradingview acciones: {e}")
    hoy = datetime.datetime.now(BERLIN).date().isoformat(); fecha = hoy
    try:
        fecha = datetime.datetime.fromtimestamp(res["dax_diario"]["velas"][-1]["t"], datetime.timezone.utc).date().isoformat()
    except Exception:
        pass
    res["sesion"] = fecha
    if os.environ.get("SOLO_DIA_DE_SESION") == "1" and fecha != hoy:
        print(f"Sin sesión en Xetra hoy ({hoy}): la última vela del DAX es del {fecha}. No hay Short."); return
    os.makedirs(os.path.join(ROOT, "datos"), exist_ok=True)
    p = os.path.join(ROOT, "datos", f"dax-{fecha}.json")
    json.dump(res, open(p, "w"), ensure_ascii=False)
    print("escrito", p, "errores:", res["errores"], "acciones:", len(res.get("acciones", {})), res.get("acciones_origen"),
          "velas DAX:", len(res.get("dax_diario", {}).get("velas", [])))


if __name__ == "__main__":
    main()
