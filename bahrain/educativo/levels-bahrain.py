"""Ayuda para escribir una lección de «التحليل الفني ببساطة» (Bahrain AI Stocks): a partir de velas.json imprime los máximos y mínimos locales (pivotes)
y los agrupa en zonas de soporte/resistencia candidatas, con número de toques, fechas y distancia al último cierre (todo calculado).
uso: python3 levels-bahrain.py <velas.json> [simbolo] [ventana=5] [tolerancia_pct=2.0] [sesiones=260]"""
import json, sys, datetime as dt

D = json.load(open(sys.argv[1])); s = sys.argv[2] if len(sys.argv) > 2 and ":" in sys.argv[2] else list(D["series"])[0]
args = [a for a in sys.argv[2:] if ":" not in a]
W = int(args[0]) if args else 5; TOL = float(args[1]) if len(args) > 1 else 2.0; N = int(args[2]) if len(args) > 2 else 260
V = D["series"][s]["velas"][-N:]; fd = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
piv = []
for i in range(W, len(V) - W):
    if V[i]["h"] == max(x["h"] for x in V[i - W:i + W + 1]): piv.append((V[i]["h"], "H", fd(V[i]["t"])))
    if V[i]["l"] == min(x["l"] for x in V[i - W:i + W + 1]): piv.append((V[i]["l"], "T", fd(V[i]["t"])))
piv.sort(); Z = []
for p in piv:
    if Z and p[0] <= Z[-1][0][0] * (1 + TOL / 100): Z[-1].append(p)
    else: Z.append([p])
c = V[-1]["c"]
print(s, "sesiones", len(V), fd(V[0]["t"]), "→", fd(V[-1]["t"]), "cierre", c, "máx", max(x["h"] for x in V), "mín", min(x["l"] for x in V))
for z in sorted(Z, key=lambda z: -len(z)):
    if len(z) < 2: continue
    lo, hi = min(p[0] for p in z), max(p[0] for p in z)
    print(f"{lo:8.3f}-{hi:8.3f}  toques {len(z)}  ({(lo + hi) / 2 / c * 100 - 100:+.1f}% vs cierre)  " + ", ".join(f"{p[1]}{p[2]}:{p[0]:.3f}" for p in z))
