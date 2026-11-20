# Metadatos de YouTube, posts (Telegram, X, LinkedIn y TikTok) y miniatura de una lección de «Charttechnik einfach erklärt» (Wall Street auf Deutsch).
# Uso: python3 meta_leccion.py <carpeta de la lección>   (lee video.json y times.json de make_leccion.py)
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
SERIE = "Charttechnik einfach erklärt"; BASE = VJ["base"]
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
tg_linea = f"📢 Kostenlos auf Telegram: {TELEGRAM}"
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
AVISO = f"""Wichtiger Hinweis
• Nur Information und Bildung. Keine Anlageberatung und keine Kauf- oder Verkaufsempfehlung für ein Wertpapier. {VJ['nombre']} dient nur als Beispiel.
• Charttechnik beschreibt vergangene Kursverläufe. Sie sagt keine Kurse voraus; eingezeichnete Zonen sind keine Kursziele.
• Kursdaten: TradingView. Zonen und Berechnungen sind eigene und mit «berechnet» bzw. «eingezeichnet» gekennzeichnet.
• Der Kanal und seine Macher halten keine Positionen in den genannten Aktien und erhalten keine Zahlungen der Unternehmen.
• Aktien sind mit Risiken bis zum Totalverlust verbunden.
• Text, Stimme (synthetische Stimme) und Grafiken mit KI erstellt."""
I = VJ["info"]; titulo = I["titulo"]
desc = (f"{I['resumen']}\n\n{tg_linea}\n\n" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nKapitel\n{cap}\n\n"
        f"Quellen: {I['fuentes']}\n\nSerie «{SERIE}»: In jeder Folge ein Begriff der technischen Analyse, erklärt am echten Chart einer bekannten US-Aktie."
        + (f" Nächste Folge: {fin['siguiente']}." if fin.get("siguiente") else "") + f"\n\n{AVISO}\n\n"
        f"#CharttechnikEinfachErklärt #WallStreetAufDeutsch {I['hashtags']}\n\nKanal abonnieren: {CANAL}\n{tg_linea}")
assert len(titulo) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(titulo), len(desc))
tags = [SERIE, "Wall Street auf Deutsch", VJ["nombre"], VJ["ticker"], VJ["tema"], "Charttechnik", "technische Analyse", "Aktien", "Börse"] + I.get("tags", [])
json.dump({"title": titulo, "description": desc, "tags": list(dict.fromkeys(tags)), "privacy": "public", "language": "de", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}-GE.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n\n#Charttechnik · Keine Anlageberatung."
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX") + f"\n{CANAL}") <= 280, largo_x(x)
open(f"{D}/post-x-{BASE}-GE.txt", "w").write(x)
tg = (f"📚 {SERIE} | Folge {VJ['folge']}: {VJ['tema']} (am Beispiel {VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ Die ganze Folge: {{youtube}}\nUnser YouTube-Kanal: {CANAL}\n\nKeine Anlageberatung. Nur Information und Bildung. Mit KI erstellt.")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-GE.txt", "w").write(tg)
# LinkedIn (página del canal, vía Buffer, buffer-GE.yml; conectada el 20-nov-2026): con el enlace a la lección
li = (f"{SERIE} | Folge {VJ['folge']}: {VJ['tema']} (am Beispiel {VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ Die ganze Folge: {{youtube}}\n\nKeine Anlageberatung, nur Information und Bildung. {VJ['nombre']} dient nur als Beispiel. "
      "Aktien sind mit Risiken bis zum Totalverlust verbunden.\nVideo von Wall Street auf Deutsch, mit KI erstellt (Text, Stimme und Grafiken).\n"
      + " ".join(dict.fromkeys(f"#CharttechnikEinfachErklärt #Charttechnik #Börsenwissen {I['hashtags']}".split())))
assert len(li) <= 3000, len(li)
open(f"{D}/post-linkedin-{BASE}-GE.txt", "w").write(li)
tk = (f"{SERIE}, Folge {VJ['folge']}: {VJ['tema']}\n\n{I['x']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ Mehr auf YouTube: Wall Street auf Deutsch\n🤖 Mit KI erstellt (Text, Stimme und Grafiken).\n"
      f"Keine Anlageberatung, nur Information und Bildung. {VJ['nombre']} dient nur als Beispiel. Risiko bis zum Totalverlust.\n"
      + " ".join(dict.fromkeys(f"#WallStreetAufDeutsch #ChartTechnik #Aktien #Börse #Börsenwissen {I['hashtags']}".split())))
assert len(tk) <= 2200 and "{youtube}" not in tk, len(tk)
open(f"{D}/post-tiktok-{BASE}-GE.txt", "w").write(tk)

# Miniatura 1280x720: título de la lección y un recorte del gráfico real con las zonas
th = VJ["miniatura"]; VEL = json.load(open(os.environ.get("VELAS", f"{D}/velas.json")))["series"][VJ["simbolo"]]["velas"]
import datetime as dt
fv = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
g = next((e for e in VJ["escenas"] if e["id"] == th.get("grafico")), next(e for e in VJ["escenas"] if e["tipo"] == "grafico"))
V = [v for v in VEL if g.get("desde", "0") <= fv(v["t"]) <= g.get("hasta", VJ.get("ultima_vela", "9"))]
f = fig(1280, 720)
f.patches.append(plt.Rectangle((0, 0.80), 1.0, 0.20, transform=f.transFigure, color=GOLD, figure=f))
f.text(0.04, 0.90, ar(th["etiqueta"]), color=BG, fontsize=30, weight="bold", va="center")
f.text(0.04, 0.68, ar(th["titulo"]), color=FG, fontsize=58 if len(th["titulo"]) <= 28 else 46, weight="bold", va="center")
f.text(0.04, 0.575, ar(th["sub"]), color=MUTED, fontsize=28, weight="bold", va="center")
ax = f.add_axes([0.04, 0.05, 0.92, 0.46]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
import numpy as np
o = np.array([v["o"] for v in V]); c = np.array([v["c"] for v in V]); h = np.array([v["h"] for v in V]); l = np.array([v["l"] for v in V]); xs = np.arange(len(V))
cc = [TEAL if a >= b else NEG for a, b in zip(c, o)]
ax.vlines(xs, l, h, color=cc, lw=1.6); ax.bar(xs, np.maximum(abs(c - o), 0.3), bottom=np.minimum(o, c), color=cc, width=0.7)
for z in g.get("zonas", []):
    ax.axhspan(z["de"], z["a"], color=col(z.get("color", "gold")), alpha=0.35, lw=0)
ax.set_xlim(-1, len(V)); ax.set_ylim(min(l.min(), *[z["de"] for z in g["zonas"]]) * 0.98, max(h.max(), *[z["a"] for z in g["zonas"]]) * 1.01)
p = f"{D}/miniatura-{BASE}-GE.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((150, 150), Image.LANCZOS); im.alpha_composite(lg, (1280 - 170, 4)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "tg", len(tg), "titulo", len(titulo))
