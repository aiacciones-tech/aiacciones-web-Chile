# Metadatos de la emisión (directo.json), posts de anuncio (X, Threads, Facebook, Telegram) y miniatura 1280x720 de un directo de
# Saudi Arabia AI Stocks. Todo en árabe; archivos terminados en -saudi (regla de Daniel). Cada post enlaza el canal.
# Los posts anuncian el directo antes de empezar ({youtube} = enlace de la emisión, que scripts/directo-saudi.py escribe al programarla).
# Uso: python3 meta_directo.py <carpeta del evento>   (después de make_directo.py: usa times.json para los capítulos)
import json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "educativo"), os.path.join(HERE, "..", "diario")]
from comun_leccion import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); BASE = VJ["base"]; I = VJ["info"]
RIAD = dt.timezone(dt.timedelta(hours=3))
INI = dt.datetime.fromisoformat(VJ["inicio"].replace("Z", "+00:00")); HORA = INI.astimezone(RIAD).strftime("%H:%M")
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
AVISO_C = "محتوى إعلامي وليس توصية استثمارية."
AVISO = ("محتوى إعلامي وليس توصية استثمارية. بث مُعدّ مسبقًا: النص والصوت (صوت اصطناعي) والرسوم من إعداد أدوات الذكاء الاصطناعي، "
         "والأرقام من المصادر المذكورة. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.")
lineas = "\n".join("• " + l for l in I["lineas"])
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap = ""
if os.path.exists(f"{D}/times.json"):
    T_ = dict((k, v) for k, v in json.load(open(f"{D}/times.json")))
    caps = [(T_[e["id"]], e["capitulo"]) for e in VJ["escenas"] if e.get("capitulo") and e.get("id") in T_]
    if len(caps) >= 2: cap = "\n".join([f"0:00 العد التنازلي"] + [f"{mmss(t)} {c}" for t, c in caps]) + "\n\n"
fuentes = "\n".join(f"• {f['dato']}: {f['fuente']} {f['url']}" for f in I["fuentes"])
desc = (f"🔴 بث مباشر الساعة {HORA} بتوقيت الرياض | {VJ['fecha_ar']}\n{I['resumen']}\n\n{lineas}\n\n{cap}"
        f"المصادر:\n{fuentes}\n\n{AVISO}\nاشترك في القناة: {CANAL}\n{I['hashtags']}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
tags = ["بث مباشر", "Saudi Arabia AI Stocks", "تاسي", "تداول", "أسهم السعودية", "السوق السعودية"] + I.get("tags", [])
json.dump({"title": I["titulo"], "description": desc, "tags": list(dict.fromkeys(tags)), "inicio": VJ["inicio"], "privacy": "public", "categoryId": "25"},
          open(f"{D}/directo-{BASE}-saudi.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
URL = "https://youtu.be/XXXXXXXXXXX"
x = f"🔴 بث مباشر اليوم الساعة {HORA} (الرياض)\n{I['x']}\n\n▶️ {{youtube}}\n{AVISO_C}"
xc = x.replace(AVISO_C, f"{canal_linea}\n{AVISO_C}")
if largo_x(xc.replace("{youtube}", URL)) <= 280: x = xc
assert largo_x(x.replace("{youtube}", URL)) <= 280, largo_x(x.replace("{youtube}", URL))
th = xc if len(xc.replace("{youtube}", URL)) <= 500 else x
open(f"{D}/post-x-{BASE}-saudi.txt", "w").write(x); open(f"{D}/post-threads-{BASE}-saudi.txt", "w").write(th)
fb = (f"🔴 بث مباشر | {VJ['titulo']}\n🕘 الساعة {HORA} بتوقيت الرياض، {VJ['fecha_ar']}\n\n{I['resumen']}\n\n{lineas}\n\n"
      f"▶️ رابط البث (فعّل التذكير): {{youtube}}\n💬 شاركنا أسئلتك في الدردشة المباشرة.\n{canal_linea}\n\n{AVISO}\n\n{I['hashtags']}")
assert len(fb.replace("{youtube}", URL)) <= 2950
open(f"{D}/post-facebook-{BASE}-saudi.txt", "w").write(fb)
tg = f"🔴 بث مباشر الساعة {HORA} (الرياض) | {VJ['titulo']}\n\n{lineas}\n\n▶️ {{youtube}}\n{canal_linea}\n\n{AVISO_C}"
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-saudi.txt", "w").write(tg)

# Miniatura 1280x720: etiqueta roja «بث مباشر», el evento y la hora
M = VJ.get("miniatura", {}); W_, H_ = 1280, 720
f = fig(W_, H_)
f.patches.append(plt.Rectangle((0.66, 0.80), 0.30, 0.13, transform=f.transFigure, color=NEG, figure=f))
f.text(0.81, 0.865, ar("● بث مباشر"), color=FG, fontsize=40, weight="bold", ha="center", va="center")
f.text(0.95, 0.62, ar(M.get("linea1", VJ["titulo"])), color=FG, fontsize=88 if len(M.get("linea1", VJ["titulo"])) <= 16 else 62, weight="bold", ha="right", va="center")
f.text(0.95, 0.43, ar(M.get("linea2", VJ["evento"])), color=GOLD, fontsize=66, weight="bold", ha="right", va="center")
f.text(0.95, 0.24, ar(f"{VJ['fecha_ar']} · {HORA} الرياض"), color=MUTED, fontsize=34, weight="bold", ha="right", va="center")
f.text(0.04, 0.06, "Saudi Arabia AI Stocks", color=FG, fontsize=26, weight="bold", ha="left")
p = f"{D}/thumbnail-{BASE}-saudi.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((170, 170), Image.LANCZOS); im.alpha_composite(lg, (40, 40)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "fb", len(fb), "tg", len(tg), "x", largo_x(x.replace("{youtube}", URL)), "titulo", len(I["titulo"]), "capitulos", bool(cap))
