# Metadatos de YouTube (vídeo y Short), posts (X, Threads, Facebook, LinkedIn, TikTok, Instagram, Telegram) y miniatura de un vídeo
# evergreen «دليل المستثمر في السوق السعودية» (Saudi Arabia AI Stocks). Todos los archivos terminan en -saudi (regla de Daniel, 3-nov-2026).
# Título y tags pensados para la búsqueda: el título empieza por la pregunta que la gente escribe ("palabra_clave" en video.json).
# Uso: [VELAS=<velas.json>] python3 meta_guia.py <carpeta de la guía>   (lee video.json y times.json de make_guia.py)
import json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "educativo")); sys.path.insert(0, HERE)
from comun_leccion import *
import campana

SERIE = "دليل المستثمر في السوق السعودية"
D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
BASE = VJ["base"]; I = VJ["info"]; slug = f"guide-{BASE}"
CTA = campana.activa()
cta_desc = f"{campana.DESC}\n{CANAL}\n\n" if CTA else ""; cta_post = f"{campana.POST}\n" if CTA else ""; cta_x = f"{campana.POST_X}\n" if CTA else ""
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
AVISO = f"""إخلاء مسؤولية مهم
• هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية. استشر جهة مرخصة من هيئة السوق المالية قبل أي قرار استثماري.
• الأرقام والقواعد المذكورة صحيحة حسب المصادر في تاريخ إعداد الفيديو، وقد تتغير؛ تحقق منها لدى هيئة السوق المالية وتداول السعودية.
• المصادر: {I['fuentes']}.
• لا تملك القناة ولا معدّوها مراكز في الأوراق المالية المذكورة، ولا يتلقون أي مقابل من أي شركة أو جهة وساطة.
• الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال كاملًا، والأداء السابق لا يضمن النتائج المستقبلية.
• النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي."""
serie_txt = f"سلسلة «{SERIE}»: أدلة عملية بالعربية عن السوق السعودية، مرتين في الأسبوع." + (f" الدليل القادم: {fin['siguiente']}." if fin.get("siguiente") else "")
desc = (f"{I['resumen']}\n\n{cta_desc}" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nالفصول\n{cap}\n\n{serie_txt}\n\n{AVISO}\n\n"
        f"#دليل_المستثمر {I['hashtags']}\n\nاشترك في القناة: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
tags = I.get("tags", []) + [SERIE, "Saudi Arabia AI Stocks", "أسهم السعودية", "تداول"]
tags = list(dict.fromkeys(tags))
while len(",".join(tags)) > 480: tags.pop()
json.dump({"title": I["titulo"], "description": desc, "tags": tags, "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}-saudi.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['tiktok']}\nالدليل الكامل: {{video:{slug}}}\n{cta_post}"
      f"محتوى تعليمي وليس توصية استثمارية. صُنع بأدوات الذكاء الاصطناعي.\nاشترك في القناة: {CANAL}\n{I['hashtags_short']}")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": tags[:8] + ["Shorts"], "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-short-{BASE}-saudi.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
URL = "https://youtu.be/XXXXXXXXXXX"
x = f"{I['x']}\n\n▶️ {{youtube}}\n{cta_x}{canal_linea}\n\nمحتوى تعليمي وليس توصية استثمارية."
if cta_x and largo_x(x.replace("{youtube}", URL)) > 280: x = x.replace(cta_x, "")
assert largo_x(x.replace("{youtube}", URL)) <= 280, largo_x(x.replace("{youtube}", URL))
assert len(x.replace("{youtube}", URL)) <= 500
open(f"{D}/post-x-{BASE}-saudi.txt", "w").write(x); open(f"{D}/post-threads-{BASE}-saudi.txt", "w").write(x)
MIN = max(1, round(T_["_total"] / 60))
fb = (f"📘 {SERIE}: {VJ['tema']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ الدليل الكامل ({MIN} دقائق): {{youtube}}\n{cta_post}{canal_linea}\n\n"
      f"محتوى تعليمي وإعلامي فقط ولا يُعد توصية استثمارية. الاستثمار ينطوي على مخاطر.\n\n{I['hashtags']}")
assert len(fb.replace("{youtube}", URL)) <= 2950
open(f"{D}/post-facebook-{BASE}-saudi.txt", "w").write(fb)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short como vídeo nativo, 3-4 datos + conclusión, autoría transparente y el enlace al canal al final
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4
lk = (f"{SERIE}: {VJ['tema']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      "محتوى تعليمي وليس توصية استثمارية.\n"
      f"فيديو من إعداد قناة Saudi Arabia AI Stocks.\n{CANAL}")
assert len(lk) <= 2950 and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-{BASE}-saudi.txt", "w").write(lk)
tk = (f"{I['tiktok']}\n{cta_post}{canal_linea}\nمحتوى تعليمي وليس توصية استثمارية. صُنع بأدوات الذكاء الاصطناعي.\n{I['hashtags_short']}")
assert len(tk) <= 2200
open(f"{D}/post-tiktok-{BASE}-saudi.txt", "w").write(tk); open(f"{D}/post-instagram-{BASE}-saudi.txt", "w").write(tk)
tg = (f"📘 {SERIE}: {VJ['tema']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ الدليل الكامل: {{youtube}}\n{cta_post}{canal_linea}\n\nمحتوى تعليمي وليس توصية استثمارية.")
if len(tg) > 1000: tg = tg.replace(f"{I['resumen']}\n\n", "")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-saudi.txt", "w").write(tg)

# Miniatura 1280x720 (de derecha a izquierda): etiqueta, tema en grande, subtítulo y, si hay, el gráfico real (línea semanal)
th = VJ["miniatura"]
f = fig(1280, 720)
f.patches.append(plt.Rectangle((0, 0.82), 1.0, 0.18, transform=f.transFigure, color=GOLD, figure=f))
f.text(0.96, 0.91, ar(th["etiqueta"]), color=BG, fontsize=34, weight="bold", va="center", ha="right")
f.text(0.96, 0.67, ar(th["titulo"]), color=FG, fontsize=64 if len(th["titulo"]) <= 22 else 52, weight="bold", va="center", ha="right")
f.text(0.96, 0.53, ar(th["sub"]), color=GOLD, fontsize=36, weight="bold", va="center", ha="right")
if th.get("grafico") and VJ.get("simbolo"):
    import numpy as np
    fv = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
    VEL = json.load(open(os.environ.get("VELAS", f"{D}/velas.json")))["series"][VJ["simbolo"]]["velas"]
    S = {}
    for v in VEL:
        if not VJ.get("ultima_vela") or fv(v["t"]).isoformat() <= VJ["ultima_vela"]: S[fv(v["t"]).isocalendar()[:2]] = v["c"]
    ys = np.array(list(S.values())); ax = f.add_axes([0.04, 0.04, 0.92, 0.40]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
    ax.fill_between(range(len(ys)), ys, ys.min() * 0.8, color=TEAL, alpha=0.18, lw=0); ax.plot(ys, color=TEAL, lw=3.5)
    ax.set_xlim(0, len(ys)); ax.set_ylim(ys.min() * 0.8, ys.max() * 1.05)
p = f"{D}/thumbnail-{BASE}-saudi.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((170, 170), Image.LANCZOS); im.alpha_composite(lg, (20, 150)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "fb", len(fb), "tg", len(tg), "x", largo_x(x.replace("{youtube}", URL)), "titulo", len(I["titulo"]))
