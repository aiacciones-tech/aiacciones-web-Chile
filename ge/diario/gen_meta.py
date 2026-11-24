# Metadatos de YouTube (vídeo y Short), posts (X, Threads, Facebook, LinkedIn, TikTok, Instagram, Telegram) y miniatura del vídeo diario en alemán
# de Wall Street auf Deutsch (portado de nabd/diario/gen_meta.py).
# Uso: python3 gen_meta.py <carpeta del día>   (lee info.json y times.json, que escribe make_video.py)
# Todos los archivos que se entregan terminan en -GE; encolar.sh copia a cola-ge/ el vídeo, el Short, sus metadatos y la miniatura.
# post-telegram lo publica telegram-GE.yml; post-linkedin, post-x, post-tiktok y post-instagram buffer-GE.yml (vía encolar.sh); el resto quedan listos por si se conectan más redes.
import json, sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
import campana
D = sys.argv[1]; I = json.load(open(f"{D}/info.json")); T = dict(json.load(open(f"{D}/times.json")))
slug = f"bolsa-{I['fecha']}"; F = I["fecha"]
# Campaña de comentarios y suscripción (campana.py): se añade sola hasta campana.HASTA y luego desaparece.
CTA = campana.activa()
cta_desc = f"{campana.DESC}\n{CANAL}\n\n" if CTA else ""
cta_post = f"{campana.POST}\n" if CTA else ""
cta_x = f"{campana.POST_X}\n" if CTA else ""
IMPRESSUM = os.environ.get("IMPRESSUM_URL", "")   # § 5 DDG: enlace al Impressum de Daniel cuando exista (también se puede poner en info.json)
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
imp = I.get("impressum") or IMPRESSUM
AVISO = f"""Wichtiger Hinweis / Haftungsausschluss
• Erstellt von Wall Street auf Deutsch am {I['elaborado']} (deutsche Zeit) mit Daten der Sitzung vom {I['fecha_txt']}; erscheint am Morgen nach jeder Sitzung an der Wall Street, vor dem Handelsstart in Europa.
• Nur Information und Bildung auf Basis öffentlicher Informationen. Keine Anlageberatung, keine Anlageempfehlung und keine Aufforderung zum Kauf oder Verkauf von Wertpapieren. Die Inhalte berücksichtigen weder Ihre persönliche Situation noch Ihre Ziele oder Ihre Risikobereitschaft.
• Fakten und Meinungen sind getrennt. Die Zahlen stammen aus Unternehmensveröffentlichungen bei der US-Börsenaufsicht SEC und den genannten Marktquellen ({I['fuentes']}). Eigene Berechnungen sind mit «berechnet» gekennzeichnet. Wir nennen keine Kursziele und bewerten Aktien nicht als günstig oder teuer.
• Charttechnik: Gleitende Durchschnitte, RSI, Stochastik sowie Unterstützungen und Widerstände sind aus öffentlichen Schlusskursen berechnet. Sie beschreiben die vergangene Kursentwicklung, sind keine Kauf- oder Verkaufssignale und sagen die Zukunft nicht voraus.
• Interessenkonflikte: Weder der Kanal noch seine Macher halten Positionen in den genannten Aktien oder erhalten eine Vergütung von den Unternehmen. Die Inhalte wurden vor der Veröffentlichung keinem Unternehmen vorgelegt.
• Risiken: Aktien sind mit Risiken bis zum Totalverlust verbunden. Frühere Wertentwicklungen sind kein verlässlicher Indikator für künftige Ergebnisse. Die Daten können Fehler enthalten; prüfen Sie sie in den Originalquellen.
• Erstellung: Text, Stimme (synthetische Stimme) und Grafiken mit KI erstellt und mit den genannten Quellen abgeglichen.""" + (f"\n• Impressum: {imp}" if imp else "")
# Capítulos: los del info.json si todos existen en times.json; si no, los de las 8 secciones del vídeo largo
CAPS = [("s_title", "Einstieg"), ("s_indices", "Die großen Indizes"), ("s_news", "Warum sich der Markt bewegt hat"), ("s_sectores", "Sektoren"),
        ("s_accion_1", "Aktien des Tages"), ("s_macro", "Zinsen, Dollar, Rohstoffe und Europa"), ("s_tech_spx", "Charttechnik: S&P 500"),
        ("s_tech_ndx", "Charttechnik: Nasdaq 100"), ("s_agenda", "Was heute ansteht"), ("s_fin", "Fazit und Telegram")]
caps = I.get("capitulos") if I.get("capitulos") and all(k in T for k, _ in I["capitulos"]) else [c for c in CAPS if c[0] in T]
cap = "\n".join(f"{mmss(T[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate(caps))
MIN = max(1, round(T.get("_total", 180) / 60))
tg_linea = f"📢 Kostenlos unserem Telegram-Kanal folgen: {TELEGRAM}"
imp_linea = f"\nImpressum: {imp}" if imp else ""
desc = (f"{I['resumen']}\n\n{tg_linea}\n\n{cta_desc}" + "\n\n".join("• " + c for c in I["claves"]) +
        f"\n\nKapitel\n{cap}\n\nQuellen: {I['fuentes']}. Keine Positionen in den genannten Aktien.\n\n{AVISO}\n\n{I['hashtags']}\n\nKanal abonnieren: {CANAL}\n{tg_linea}{imp_linea}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
json.dump({"title": I["titulo"], "description": desc, "tags": I["tags"], "privacy": "public", "language": "de", "categoryId": "27"}, open(f"{D}/meta-youtube-{F}-GE.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['resumen']}\nDas ganze Video (Nachrichten, Fundamentales und Charttechnik): {{video:{slug}}}\n"
      f"Quellen: {I['fuentes']}. Erstellt von Wall Street auf Deutsch am {I['elaborado']} (deutsche Zeit). Keine Anlageberatung, nur Information und Bildung. "
      f"Charttechnik sind Daten, keine Kauf- oder Verkaufssignale. Keine Positionen in den genannten Aktien. Risiko bis zum Totalverlust. Text, Stimme und Grafiken mit KI erstellt.\n"
      f"{cta_post}Kanal abonnieren: {CANAL}{imp_linea}\n#Shorts #WallStreet #Börse #Aktien #Nasdaq")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": I["tags"][:6] + ["Shorts"], "privacy": "public", "language": "de", "categoryId": "27"}, open(f"{D}/meta-short-{F}-GE.json", "w"), ensure_ascii=False, indent=1)
canal_linea = f"Unser YouTube-Kanal: {CANAL}"
x = f"{I['x']}\n\n▶️ {{youtube}}\n{cta_x}{canal_linea}\n\nKeine Anlageberatung. Mit KI erstellt."
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
if cta_x and largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) > 280: x = x.replace(cta_x, "")  # sin sitio en X: va sin la línea de la campaña
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX"))
open(f"{D}/post-x-{F}-GE.txt", "w").write(x); open(f"{D}/post-threads-{F}-GE.txt", "w").write(x)
li = (f"Wall Street auf Deutsch | Sitzung vom {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n\n".join("• " + c for c in I["claves"]) +
      f"\n\n▶️ Das ganze Video ({MIN} Minuten): {{youtube}}\n{cta_post}{canal_linea}\n\n"
      f"Quellen: {I['fuentes']}.\nKeine Anlageberatung, nur Information und Bildung. Charttechnik beschreibt Daten und ist kein Kauf- oder Verkaufssignal. Keine Positionen in den genannten Aktien. "
      f"Aktien sind mit Risiken bis zum Totalverlust verbunden. Text, Stimme und Grafiken mit KI erstellt.\n\n" + I["hashtags"])
assert len(li.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 2950, len(li)
open(f"{D}/post-facebook-{F}-GE.txt", "w").write(li)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short subido como vídeo nativo (no enlace), con un resumen con valor
# (3-4 datos clave con cifras y qué cambió + una conclusión, sin relleno), la autoría transparente y al final el enlace al canal.
L = I["linkedin"]
assert 3 <= len(L["datos"]) <= 4, "LinkedIn: 3 o 4 datos clave"
lk = (f"Wall Street auf Deutsch | Sitzung vom {I['fecha_txt']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nFazit: {L['conclusion']}\n\n"
      "Keine Anlageberatung, nur Information. Charttechnik beschreibt Daten und ist kein Kauf- oder Verkaufssignal.\n"
      f"Video von Wall Street auf Deutsch, mit KI erstellt (Text, Stimme und Grafiken).\n{CANAL}")
assert len(lk) <= 2950 and "{youtube}" not in lk and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-{F}-GE.txt", "w").write(lk)
# TikTok e Instagram (Reels): sin #Shorts (es de YouTube) y con el aviso de IA en el texto, porque el canal es 100% IA
tags_tk = " ".join(t for t in I["hashtags_short"].split() if t.lower() != "#shorts")
tags_tk = ("#WallStreetAufDeutsch " + tags_tk).strip() if "#wallstreetaufdeutsch" not in tags_tk.lower() else tags_tk
tk = (f"{I['tiktok']}\n{cta_post}{canal_linea}\n🤖 Mit KI erstellt (Text, Stimme und Grafiken).\n"
      f"Keine Anlageberatung, nur Information und Bildung. Keine Positionen in den genannten Aktien. Risiko bis zum Totalverlust.\n{tags_tk}")
assert len(tk) <= 2200, len(tk)
open(f"{D}/post-tiktok-{F}-GE.txt", "w").write(tk); open(f"{D}/post-instagram-{F}-GE.txt", "w").write(tk)
tg = (f"📊 Wall Street auf Deutsch | {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in I["claves_cortas"]) +
      f"\n\n▶️ Das ganze Video: {{youtube}}\n{cta_post}{canal_linea}\n\nKeine Anlageberatung. Keine Positionen in den genannten Aktien. Mit KI erstellt.")
open(f"{D}/post-telegram-{F}-GE.txt", "w").write(tg)

# Shorts extra del mismo guion (desde el 24-nov-2026): short-2.json («Aktie des Tages», 12:15 Berlín) y short-3.json («Die Marken für heute», 15:05 Berlín).
# info.json → "shorts_extra": [{"n": 2, "titulo": "... #Shorts", "resumen": "...", "tiktok": "...", "hashtags": "#... #Shorts", "tags": [...]}, ...]
# Salen meta-short<n>-<fecha>-GE.json y post-tiktok/instagram-short<n>-<fecha>-GE.txt; encolar.sh los deja en cola-ge-espera/ y cola-espera-GE.yml los publica a su hora.
for X in I.get("shorts_extra", []):
    n = X["n"]; assert n in (2, 3) and len(X["titulo"]) <= 100, X.get("titulo")
    sx = (f"{X['resumen']}\nDas ganze Video zur Sitzung (Nachrichten, Fundamentales und Charttechnik): {{video:{slug}}}\n"
          f"Quellen: {I['fuentes']}. Erstellt von Wall Street auf Deutsch am {I['elaborado']} (deutsche Zeit). Keine Anlageberatung, nur Information und Bildung. "
          f"Charttechnik sind Daten, keine Kauf- oder Verkaufssignale. Keine Positionen in den genannten Aktien. Risiko bis zum Totalverlust. Text, Stimme und Grafiken mit KI erstellt.\n"
          f"{cta_post}Kanal abonnieren: {CANAL}{imp_linea}\n{X.get('hashtags', '#Shorts #WallStreet #Börse #Aktien')}")
    assert len(sx) < 5000 and "<" not in sx and ">" not in sx
    json.dump({"title": X["titulo"], "description": sx, "tags": (X.get("tags") or I["tags"])[:8] + ["Shorts"], "privacy": "public", "language": "de", "categoryId": "27"},
              open(f"{D}/meta-short{n}-{F}-GE.json", "w"), ensure_ascii=False, indent=1)
    tx = " ".join(t for t in X.get("hashtags", I["hashtags_short"]).split() if t.lower() != "#shorts")
    tx = ("#WallStreetAufDeutsch " + tx).strip() if "#wallstreetaufdeutsch" not in tx.lower() else tx
    tkx = (f"{X['tiktok']}\n{cta_post}{canal_linea}\n🤖 Mit KI erstellt (Text, Stimme und Grafiken).\n"
           f"Keine Anlageberatung, nur Information und Bildung. Keine Positionen in den genannten Aktien. Risiko bis zum Totalverlust.\n{tx}")
    assert len(tkx) <= 2200, len(tkx)
    open(f"{D}/post-tiktok-short{n}-{F}-GE.txt", "w").write(tkx); open(f"{D}/post-instagram-short{n}-{F}-GE.txt", "w").write(tkx)
    print("short extra", n, X["titulo"])

# Miniatura 1280x720 (de izquierda a derecha): la fecha de la sesión en destacado y dos índices; logo arriba a la derecha
th = I["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="left", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=GOLD, figure=f))
TT(0.045, 0.905, "Wall Street · Sitzung vom", BG, 26, va="center")
TT(0.045, 0.775, th["fecha"], BG, 46 if len(th["fecha"]) > 24 else 50, va="center")
for i, (nom, big, c) in enumerate(th["indices"]):
    xx = 0.045 + i * 0.47
    TT(xx, 0.56, nom, MUTED, 26)
    f.text(xx, 0.35, big, color=col(c), fontsize=78, weight="bold", ha="left")
TT(0.045, 0.17, th["sub"], FG, 28)
TT(0.045, 0.05, th["pie"], BLUE, 22)
p = f"{D}/miniatura-{F}-GE.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((190, 190), Image.LANCZOS); im.alpha_composite(lg, (1280 - 190 - 25, 12)); im.convert("RGB").save(p)
print("ok", slug, "desc", len(desc), "li", len(li), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")))
