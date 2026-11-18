# Metadatos de YouTube, posts (Telegram y X) y miniatura de un episodio de «Die Wall-Street-Giganten» (Wall Street auf Deutsch).
# Uso: python3 meta_episodio.py <carpeta del episodio>   (lee video.json y times.json de make_episodio.py)
# Sin Short: la serie sube como máximo 3 vídeos al día y así el canal no pasa del límite de YouTube (~10 subidas en 24 h) con el diario.
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
SERIE = "Die Wall-Street-Giganten"; BASE = f"serie20-{VJ['ticker'].lower()}-{VJ['fecha_resultados']}"
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
CAPS = [("e_portada", "Einstieg"), ("e_resultados", "Das Quartal in Zahlen"), ("e_ingresos", "Umsatz und Marge"), ("e_balance", "Bilanz"),
        ("e_flujo", "Cashflow"), ("e_expectativas", "Im Vergleich zu den Schätzungen"), ("e_fin", "Fazit")]
cap = "\n".join(f"{mmss(T_[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate(CAPS) if k in T_)
tg_linea = f"📢 Kostenlos auf Telegram: {TELEGRAM}"
AVISO = """Wichtiger Hinweis
• Nur Information und Bildung. Keine Anlageberatung und keine Kauf- oder Verkaufsempfehlung für ein Wertpapier.
• Die Zahlen stammen von TradingView (Fundamentaldaten aus den Unternehmensberichten), aus der Mitteilung des Unternehmens und den genannten Quellen. Eigene Berechnungen sind mit «berechnet» gekennzeichnet.
• Wir nennen keine Kursziele und bewerten keine Aktie als günstig oder teuer. Der Kanal und seine Macher halten keine Positionen in den genannten Aktien und erhalten keine Zahlungen der Unternehmen.
• Aktien sind mit Risiken bis zum Totalverlust verbunden. Vergangene Entwicklungen sind kein Indikator für künftige Ergebnisse.
• Text, Stimme (synthetische Stimme) und Grafiken mit KI erstellt."""
I = VJ["info"]
titulo = I["titulo"]
desc = (f"{I['resumen']}\n\n{tg_linea}\n\n" + "\n".join("• " + c for c in VJ["claves"]) + f"\n\nKapitel\n{cap}\n\n"
        f"Quellen: {I['fuentes']}\n\nSerie «{SERIE}»: eine Folge zu jedem der 20 größten US-Unternehmen nach seinen Quartalszahlen.\n\n{AVISO}\n\n"
        f"#WallStreetGiganten #WallStreetAufDeutsch {I['hashtags']}\n\nKanal abonnieren: {CANAL}\n{tg_linea}")
assert len(titulo) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(titulo), len(desc))
tags = [SERIE, "Wall Street auf Deutsch", VJ["nombre"], VJ["ticker"], "Quartalszahlen", "Aktien", "US-Aktien", "Börse", "Bilanz",
        "earnings"] + I.get("tags", [])
json.dump({"title": titulo, "description": desc, "tags": tags, "privacy": "public", "language": "de", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}-GE.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n\n#WallStreetGiganten · Keine Anlageberatung."
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX") + f"\n{CANAL}") <= 280, largo_x(x)
open(f"{D}/post-x-{BASE}-GE.txt", "w").write(x)
tg = (f"📊 {SERIE} | {VJ['nombre']} ({VJ['ticker']}) · {VJ['trimestre']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in VJ["claves"]) +
      f"\n\n▶️ Die ganze Folge: {{youtube}}\nUnser YouTube-Kanal: {CANAL}\n\nKeine Anlageberatung. Nur Information und Bildung. Mit KI erstellt.")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-GE.txt", "w").write(tg)
# TikTok (vía Buffer, buffer-GE.yml): el episodio entero (horizontal, 2-4 min) con aviso de IA en el texto; sin {youtube}, que no es clicable allí
tk = (f"{SERIE}: {VJ['nombre']} ({VJ['ticker']}) · {VJ['trimestre']}\n\n{I['x']}\n\n" + "\n".join("• " + c for c in VJ["claves"]) +
      f"\n\n▶️ Mehr auf YouTube: Wall Street auf Deutsch\n🤖 Mit KI erstellt (Text, Stimme und Grafiken).\n"
      "Keine Anlageberatung, nur Information und Bildung. Keine Positionen in den genannten Aktien. Risiko bis zum Totalverlust.\n"
      f"#WallStreetAufDeutsch #WallStreetGiganten #Quartalszahlen #Aktien #Börse {I['hashtags']}")
assert len(tk) <= 2200 and "{youtube}" not in tk, len(tk)
open(f"{D}/post-tiktok-{BASE}-GE.txt", "w").write(tk)

# Miniatura 1280x720
th = VJ["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="left", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=GOLD, figure=f))
TT(0.045, 0.905, f"{SERIE} · {VJ['trimestre']}", BG, 24, va="center")
TT(0.045, 0.775, VJ["nombre"], BG, 56 if len(VJ["nombre"]) <= 16 else 44, va="center")
f.text(0.70, 0.775, VJ["ticker"], color=BG, fontsize=40, weight="bold", ha="right", va="center")
TT(0.045, 0.55, th["etiqueta"], MUTED, 30)
f.text(0.045, 0.33, th["cifra"], color=col(th.get("color", "gold")), fontsize=96, weight="bold", ha="left")
TT(0.045, 0.15, th["sub"], FG, 30)
p = f"{D}/miniatura-{BASE}-GE.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((190, 190), Image.LANCZOS); im.alpha_composite(lg, (1280 - 215, 12)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "tg", len(tg), "titulo", len(titulo))
