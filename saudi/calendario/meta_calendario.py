# Metadatos del Short de YouTube, posts (X, Threads, Facebook, LinkedIn, TikTok, Instagram, Telegram) y portada del
# «تقويم النتائج الأسبوعي» de Saudi Arabia AI Stocks. Todo en árabe; archivos terminados en -saudi (regla de Daniel, 3-nov-2026).
# Cada post enlaza el canal; si hay empresas de EE. UU., recomienda @NabdWallStreet (Daniel, 22-nov-2026).
# Uso: python3 meta_calendario.py <carpeta de la semana>
import json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "educativo"), os.path.join(HERE, "..", "diario")]
from comun_leccion import *
import campana

D = os.path.abspath(sys.argv[1]); SJ = json.load(open(f"{D}/short.json")); BASE = SJ["base"]; I = SJ["info"]
CTA = campana.activa(dt.date.fromisoformat(SJ["publicar"]))
cta_post = f"{campana.POST}\n" if CTA else ""; cta_x = f"{campana.POST_X}\n" if CTA else ""
TITULO = "تقويم النتائج الأسبوعي"
NABD = "https://www.youtube.com/@NabdWallStreet"
EEUU = any(e["tipo"] == "empresa" and e.get("mercado", "us") == "us" for e in SJ["escenas"])
nabd = f"🇺🇸 لأخبار وول ستريت بالعربية: قناة نبض وول ستريت {NABD}\n" if EEUU else ""
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
AVISO_C = "محتوى إعلامي وليس توصية استثمارية."
AVISO = ("محتوى إعلامي وليس توصية استثمارية. التوقعات من متوسط تقديرات المحللين (ربحية السهم المعدّلة) كما نشرتها مصادر علنية، "
         "والمواعيد من إعلانات الشركات وقد تتغير. لا نملك مراكز في الأسهم المذكورة. صُنع بأدوات الذكاء الاصطناعي.")
lineas = "\n".join("• " + l for l in I["lineas"])
fuentes = "، ".join(dict.fromkeys(re.split(r"[;،(]", f["fuente"])[0].strip() for f in SJ["fuentes"] if f.get("url") and not f["dato"].startswith("FUERA")))
desc = (f"{I['resumen']}\n\n{lineas}\n\n{cta_post}{nabd}{AVISO}\nالمصادر: {fuentes}. البيانات حتى {SJ['datos_al']}.\n"
        f"اشترك في القناة: {CANAL}\n{I['hashtags']}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
tags = [TITULO, "Saudi Arabia AI Stocks", "تقويم النتائج", "نتائج الشركات", "وول ستريت", "تداول", "أسهم السعودية", "Shorts"] + \
       [e["latino"] for e in SJ["escenas"] if e["tipo"] == "empresa"]
json.dump({"title": I["titulo"], "description": desc, "tags": list(dict.fromkeys(tags)), "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-short-{BASE}-saudi.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
URL = "https://youtu.be/XXXXXXXXXXX"
x = f"{I['x']}\n\n▶️ {{youtube}}\n{cta_x}{AVISO_C}"
if cta_x and largo_x(x.replace("{youtube}", URL)) > 280: x = x.replace(cta_x, "")
assert largo_x(x.replace("{youtube}", URL)) <= 280, largo_x(x.replace("{youtube}", URL))
# El enlace del canal: buffer.py lo añade solo en X si falta y cabe; aquí lo ponemos si cabe y, en Threads, siempre (500 caracteres)
xc = x.replace(AVISO_C, f"{canal_linea}\n{AVISO_C}")
if largo_x(xc.replace("{youtube}", URL)) <= 280: x = xc
th = xc if len(xc.replace("{youtube}", URL)) <= 500 else x
open(f"{D}/post-x-{BASE}-saudi.txt", "w").write(x); open(f"{D}/post-threads-{BASE}-saudi.txt", "w").write(th)
fb = (f"📅 {TITULO} | {SJ['semana']}\n\n{I['resumen']}\n\n{lineas}\n\n▶️ الفيديو: {{youtube}}\n{cta_post}{canal_linea}\n{nabd}\n{AVISO}\n\n{I['hashtags']}")
assert len(fb.replace("{youtube}", URL)) <= 2950
open(f"{D}/post-facebook-{BASE}-saudi.txt", "w").write(fb)
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4
lk = (f"{L['titulo']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      "محتوى إعلامي وليس توصية استثمارية. التوقعات من متوسط تقديرات المحللين.\n"
      f"فيديو من إعداد قناة Saudi Arabia AI Stocks.\n{CANAL}")
assert len(lk) <= 2950 and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-{BASE}-saudi.txt", "w").write(lk)
tk = f"📅 {TITULO} | {SJ['semana']}\n{lineas}\n{cta_post}{canal_linea}\n{nabd}{AVISO_C}\n{I['hashtags']}"
assert len(tk) <= 2200
open(f"{D}/post-tiktok-{BASE}-saudi.txt", "w").write(tk); open(f"{D}/post-instagram-{BASE}-saudi.txt", "w").write(tk)
tg = f"📅 {TITULO} | {SJ['semana']}\n\n{lineas}\n\n▶️ الفيديو: {{youtube}}\n{cta_post}{canal_linea}\n{nabd}\n{AVISO_C}"
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-saudi.txt", "w").write(tg)

# Portada 1080x1920 (miniatura del Short en YouTube y foto del post de Telegram): la semana entera de un vistazo
f = fig(1080, 1920); XR = 0.92
f.patches.append(plt.Rectangle((0, 0.86), 1.0, 0.10, transform=f.transFigure, color=GOLD, figure=f))
f.text(XR, 0.91, ar(TITULO), color=BG, fontsize=62, weight="bold", va="center", ha="right")
f.text(XR, 0.82, ar(SJ["semana"]), color=FG, fontsize=40, weight="bold", va="center", ha="right")
y = 0.74; dia = None
tasi = next((e for e in SJ["escenas"] if e["tipo"] == "tasi"), None)
if tasi:
    f.text(XR, y, ar("تداول"), color=GOLD, fontsize=38, weight="bold", ha="right", va="center")
    f.text(XR, y - 0.04, ar(tasi.get("portada", "لا نتائج مرتقبة لكبرى الشركات")), color=MUTED, fontsize=32, weight="bold", ha="right", va="center"); y -= 0.11
for e in SJ["escenas"]:
    if e["tipo"] != "empresa": continue
    if e["dia"] != dia:
        dia = e["dia"]; f.text(XR, y, ar(dia), color=GOLD, fontsize=38, weight="bold", ha="right", va="center"); y -= 0.045
    f.text(XR, y, ar(e["nombre"]), color=FG, fontsize=44, weight="bold", ha="right", va="center")
    f.text(0.08, y, e["ticker"], color=BLUE, fontsize=40, weight="bold", ha="left", va="center"); y -= 0.05
    y -= 0.01
f.text(0.5, 0.06, "Saudi Arabia AI Stocks", color=FG, fontsize=40, weight="bold", ha="center")
p = f"{D}/thumbnail-{BASE}-saudi.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((150, 150), Image.LANCZOS); im.alpha_composite(lg, (40, 1600)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "fb", len(fb), "tg", len(tg), "x", largo_x(x.replace("{youtube}", URL)), "titulo", len(I["titulo"]))
