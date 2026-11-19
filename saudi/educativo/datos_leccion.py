"""Velas diarias de TradingView para una lección de «التحليل الفني ببساطة» (serie educativa de @SaudiArabiaAIStocks, saudi/educativo/).
Reutiliza tv_velas() de saudi/diario/datos_mercado.py. Corre en GitHub Actions (educativo-saudi.yml) y también desde el contenedor de Claude
si llega a TradingView. Las velas se congelan: si <salida>/velas.json ya existe no se vuelven a pedir (las cifras dichas no cambian).
Si el websocket de TradingView no entrega la serie (pasó el 10-nov-2026), usa Yahoo Finance (<código>.SR) y lo deja escrito en "fuente".
uso: python3 datos_leccion.py <video.json> <carpeta de salida>   (video.json → "simbolo", p. ej. "TADAWUL:1120"; "velas_n" opcional, 520)"""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diario"))
from datos_mercado import tv_velas, yahoo

VJ = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); p = os.path.join(out, "velas.json")
if os.path.exists(p) and not os.environ.get("REFRESCAR"):
    print("velas ya congeladas:", p); sys.exit()
D = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "series": {}}
for s in [VJ["simbolo"]] + VJ.get("simbolos_extra", []):
    try:
        D["series"][s] = tv_velas(s, "1D", VJ.get("velas_n", 520))
    except Exception as e:
        print("TradingView falló:", e, "-> Yahoo"); D["series"][s] = yahoo(s.split(":")[1] + ".SR", "2y", "1d"); D["series"][s]["simbolo"] = s
    v = D["series"][s]["velas"]; print(s, D["series"][s]["fuente"], len(v), "velas, última", dt.datetime.fromtimestamp(v[-1]["t"], dt.timezone.utc).date(), v[-1]["c"])
json.dump(D, open(p, "w"))
