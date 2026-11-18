"""Velas diarias de TradingView para una lección de la serie educativa «Charttechnik einfach erklärt» (Wall Street auf Deutsch, ge/educativo/).
Corre en GitHub Actions (educativo-GE.yml), porque el contenedor de Claude no llega a TradingView. Reutiliza tv_velas() de nabd/diario/datos_mercado.py
(solo lectura). Las velas se congelan: si <salida>/velas.json ya existe, no se vuelve a pedir (las cifras de la locución no cambian).
uso: python3 datos_leccion.py <video.json> <carpeta de salida>   (video.json → "simbolo", p. ej. "NASDAQ:NVDA"; "velas_n" opcional, 520 por defecto)"""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nabd", "diario"))
from datos_mercado import tv_velas

VJ = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); p = os.path.join(out, "velas.json")
if os.path.exists(p) and not os.environ.get("REFRESCAR"):
    print("velas ya congeladas:", p); sys.exit()
simbolos = [VJ["simbolo"]] + VJ.get("simbolos_extra", [])
D = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "series": {}}
for s in simbolos:
    D["series"][s] = tv_velas(s, "1D", VJ.get("velas_n", 520))
    v = D["series"][s]["velas"]; print(s, len(v), "velas, última", dt.datetime.fromtimestamp(v[-1]["t"], dt.timezone.utc).date(), v[-1]["c"])
json.dump(D, open(p, "w"))
