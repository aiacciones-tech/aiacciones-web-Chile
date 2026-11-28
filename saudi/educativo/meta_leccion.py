# Metadatos de YouTube (vídeo y Short), posts (X, Threads, Facebook, LinkedIn, TikTok, Instagram, Telegram) y miniatura de una lección de
# «التحليل الفني ببساطة» (Saudi Arabia AI Stocks). Todos los archivos terminan en -saudi (regla de Daniel, 3-nov-2026).
# Uso: python3 meta_leccion.py <carpeta de la lección>   (lee video.json y times.json de make_leccion.py; VELAS=<velas.json> para la miniatura)
import json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_leccion import *
import campana

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
BASE = VJ["base"]; I = VJ["info"]; slug = f"lesson-{BASE}"
CTA = campana.activa()
cta_desc = f"{campana.DESC}\n{CANAL}\n\n" if CTA else ""; cta_post = f"{campana.POST}\n" if CTA else ""; cta_x = f"{campana.POST_X}\n" if CTA else ""
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
AVISO = f"""إخلاء مسؤولية مهم
• هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية. سهم {VJ['nombre']} مجرد مثال للشرح. استشر جهة مرخصة من هيئة السوق المالية قبل أي قرار استثماري.
• التحليل الفني يصف حركة السعر في الماضي ولا يتنبأ بالمستقبل. المناطق المرسومة ليست أسعارًا مستهدفة، والوضع الحالي معروض كشروط لا كتوقعات.
• بيانات الأسعار من {I['fuentes']}. المناطق والعلامات من حساب القناة ورسمها.
• لا تملك القناة ولا معدّوها مراكز في السهم المذكور، ولا يتلقون أي مقابل من الشركات.
• الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال كاملًا، والأداء السابق لا يضمن النتائج المستقبلية.
• النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي."""
serie_txt = f"سلسلة «{SERIE}»: كل سبت حلقة جديدة تشرح مفهومًا واحدًا من التحليل الفني على الرسم البياني الحقيقي لسهم مدرج في السوق السعودية." + \
            (f" الحلقة القادمة: {fin['siguiente']}." if fin.get("siguiente") else "")
desc = (f"{I['resumen']}\n\n{cta_desc}" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nالفصول\n{cap}\n\n{serie_txt}\n\nالمصادر: {I['fuentes']}.\n\n{AVISO}\n\n"
        f"#التحليل_الفني_ببساطة {I['hashtags']}\n\nاشترك في القناة: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
tags = [SERIE, "Saudi Arabia AI Stocks", VJ["nombre"], VJ["ticker"], VJ["tema"], "التحليل الفني", "أسهم السعودية", "تداول"] + I.get("tags", [])
json.dump({"title": I["titulo"], "description": desc, "tags": list(dict.fromkeys(tags)), "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}-saudi.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['tiktok']}\nالحلقة الكاملة ({VJ['tema']}): {{video:{slug}}}\n{cta_post}"
      f"محتوى تعليمي وليس توصية استثمارية. التحليل الفني يصف الماضي ولا يتنبأ بالمستقبل. لا نملك مراكز في السهم المذكور. صُنع بأدوات الذكاء الاصطناعي.\n"
      f"اشترك في القناة: {CANAL}\n{I['hashtags_short']}")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": list(dict.fromkeys(tags))[:8] + ["Shorts"], "privacy": "public", "language": "ar", "categoryId": "27"},
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
fb = (f"📚 {SERIE} | الحلقة {VJ['folge']}: {VJ['tema']} (مثال: {VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ الحلقة الكاملة ({MIN} دقائق): {{youtube}}\n{cta_post}{canal_linea}\n\n"
      f"محتوى تعليمي وإعلامي فقط ولا يُعد توصية استثمارية. التحليل الفني يصف الماضي ولا يتنبأ بالمستقبل. لا نملك مراكز في السهم المذكور. الاستثمار ينطوي على مخاطر.\n\n{I['hashtags']}")
assert len(fb.replace("{youtube}", URL)) <= 2950
open(f"{D}/post-facebook-{BASE}-saudi.txt", "w").write(fb)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short como vídeo nativo, 3-4 datos + conclusión, autoría transparente y el enlace al canal al final
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4
lk = (f"{SERIE} | الحلقة {VJ['folge']}: {VJ['tema']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      "محتوى تعليمي وليس توصية استثمارية. التحليل الفني يصف الماضي ولا يتنبأ بالمستقبل.\n"
      f"فيديو من إعداد قناة Saudi Arabia AI Stocks.\n{CANAL}")
assert len(lk) <= 2950 and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-{BASE}-saudi.txt", "w").write(lk)
tk = (f"{I['tiktok']}\n{cta_post}{canal_linea}\nمحتوى تعليمي وليس توصية استثمارية. سهم {VJ['nombre']} مجرد مثال. لا نملك مراكز في السهم المذكور. صُنع بأدوات الذكاء الاصطناعي.\n"
      f"{I['hashtags_short']}")
assert len(tk) <= 2200
open(f"{D}/post-tiktok-{BASE}-saudi.txt", "w").write(tk); open(f"{D}/post-instagram-{BASE}-saudi.txt", "w").write(tk)
tg = (f"📚 {SERIE} | الحلقة {VJ['folge']}: {VJ['tema']} (مثال: {VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ الحلقة الكاملة: {{youtube}}\n{cta_post}{canal_linea}\n\nمحتوى تعليمي وليس توصية استثمارية. لا نملك مراكز في السهم المذكور.")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-saudi.txt", "w").write(tg)

# Miniatura 1280x720 (de derecha a izquierda): serie y número, tema en grande, acción, y el gráfico real con las zonas
th = VJ["miniatura"]; VEL = json.load(open(os.environ.get("VELAS", f"{D}/velas.json")))["series"][VJ["simbolo"]]["velas"]
import numpy as np
fv = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
g = next((e for e in VJ["escenas"] if e["id"] == th.get("grafico")), next(e for e in VJ["escenas"] if e["tipo"] == "grafico"))
VEL = [v for v in VEL if fv(v["t"]) <= VJ.get("ultima_vela", "9")]
V = [v for v in VEL if g.get("desde", "0") <= fv(v["t"]) <= g.get("hasta", VJ.get("ultima_vela", "9"))]
MED = medias_rango(VEL, V, g.get("medias", []))
Z = g.get("zonas", []); ylo = min([v["l"] for v in V] + [z["de"] for z in Z] + [np.nanmin(m["y"]) for m in MED]) * 0.985
yhi = max([v["h"] for v in V] + [z["a"] for z in Z] + [np.nanmax(m["y"]) for m in MED]) * 1.02
f = fig(1280, 720)
f.patches.append(plt.Rectangle((0, 0.82), 1.0, 0.18, transform=f.transFigure, color=GOLD, figure=f))
f.text(0.96, 0.91, ar(th["etiqueta"]), color=BG, fontsize=32, weight="bold", va="center", ha="right")
f.text(0.96, 0.69, ar(th["titulo"]), color=FG, fontsize=66 if len(th["titulo"]) <= 18 else 50, weight="bold", va="center", ha="right")
f.text(0.96, 0.565, ar(th["sub"]), color=GOLD, fontsize=30, weight="bold", va="center", ha="right")
ax = f.add_axes([0.04, 0.04, 0.92, 0.45]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
o = np.array([v["o"] for v in V]); c = np.array([v["c"] for v in V]); h = np.array([v["h"] for v in V]); l = np.array([v["l"] for v in V]); xs = np.arange(len(V))
cc = [TEAL if a >= b else NEG for a, b in zip(c, o)]
ax.vlines(xs, l, h, color=cc, lw=1.6); ax.bar(xs, np.maximum(abs(c - o), (h.max() - l.min()) * 0.004), bottom=np.minimum(o, c), color=cc, width=0.7)
for z in g.get("zonas", []):
    ax.axhspan(z["de"], z["a"], color=col(z.get("color", "gold")), alpha=0.35, lw=0)
    abajo = (z["de"] + z["a"]) / 2 < np.median(c)  # etiqueta debajo de las zonas inferiores, encima de las superiores
    ax.text(len(V) * 0.995, z["de"] if abajo else z["a"], ar(z["texto"]), color=col(z.get("color", "gold")), fontsize=26, weight="bold", ha="right", va="top" if abajo else "bottom")
for m in MED: ax.plot(xs, m["y"], color=m["color"], lw=3.5)
ax.set_xlim(-1, len(V)); ax.set_ylim(ylo, yhi)
p = f"{D}/thumbnail-{BASE}-saudi.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((170, 170), Image.LANCZOS); im.alpha_composite(lg, (20, 150)); im.convert("RGB").save(p)

# Prueba A/B (Daniel, 24-nov-2026): variante B de miniatura, estilo «pregunta» (una pregunta grande sobre el gráfico a pantalla completa).
# Título B: I["titulo_b"] si la sesión lo escribe (entonces se prueban miniatura y título juntos); si no, solo la miniatura.
# scripts/ab-saudi.py alterna A y B por días y deja la que gana.
pregunta = th.get("gancho") or f"كيف تقرأ {th['titulo']}؟"
f = fig(1280, 720)
ax = f.add_axes([0.0, 0.0, 1.0, 0.62]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
ax.vlines(xs, l, h, color=cc, lw=2.2); ax.bar(xs, np.maximum(abs(c - o), (h.max() - l.min()) * 0.004), bottom=np.minimum(o, c), color=cc, width=0.7)
for z in g.get("zonas", []):
    ax.axhspan(z["de"], z["a"], color=col(z.get("color", "gold")), alpha=0.35, lw=0)
for m in MED: ax.plot(xs, m["y"], color=m["color"], lw=3.5)
ax.set_xlim(-1, len(V)); ax.set_ylim(ylo, yhi)
f.text(0.96, 0.81, ar(pregunta, 22), color=GOLD, fontsize=64 if len(pregunta) <= 22 else 50, weight="bold", va="center", ha="right", linespacing=1.0)
f.text(0.155, 0.90, ar(f"{SERIE} · {VJ['folge']}"), color=MUTED, fontsize=24, weight="bold", va="center", ha="left")
pb = f"{D}/thumbnail-b-{BASE}-saudi.png"; f.savefig(pb, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(pb).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((150, 150), Image.LANCZOS); im.alpha_composite(lg, (25, 0)); im.convert("RGB").save(pb)
ab = {"que": "ambos" if I.get("titulo_b") else "miniatura", "B": {"miniatura": "miniatura-b.png"}, "estilos": {"A": "serie", "B": "pregunta"}}
if I.get("titulo_b"):
    assert len(I["titulo_b"]) <= 100 and "<" not in I["titulo_b"] and ">" not in I["titulo_b"], len(I["titulo_b"])
    ab["B"]["title"] = I["titulo_b"]
json.dump(ab, open(f"{D}/ab-{BASE}-saudi.json", "w"), ensure_ascii=False, indent=1)
print("ok", BASE, "desc", len(desc), "fb", len(fb), "tg", len(tg), "x", largo_x(x.replace("{youtube}", URL)), "titulo", len(I["titulo"]))
