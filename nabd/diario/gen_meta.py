# Metadatos de YouTube (video y Short), posts (X, Threads, Facebook, LinkedIn, TikTok, Instagram, Telegram) y miniatura del video diario en árabe de Nabd Wall Street (نبض وول ستريت).
# Uso: python3 gen_meta.py <carpeta del día>   (lee info.json y times.json, que escribe make_video.py)
# Todos los archivos que se entregan terminan en -Nabd (regla de Daniel, 8-nov-2026); encolar.sh copia a cola-nabd/ el video, el Short, sus metadatos y la miniatura.
# post-telegram lo publica telegram-Nabd.yml; post-linkedin, post-x, post-tiktok y post-instagram buffer-Nabd.yml (vía encolar.sh); el resto quedan listos por si se conectan más redes.
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
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
AVISO = f"""إخلاء مسؤولية مهم
• أعدّته قناة نبض وول ستريت (Nabd Wall Street) في {I['elaborado']} (بتوقيت الرياض) ببيانات جلسة {I['fecha_txt']}، ويُنشر بعد إغلاق كل جلسة في وول ستريت.
• هذا المحتوى تعليمي وإعلامي فقط ويعتمد على معلومات عامة. لا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية، ولا يراعي وضعك أو أهدافك أو مدى تحملك للمخاطر. استشر جهة مرخصة من هيئة السوق المالية في بلدك قبل أي قرار استثماري.
• الحقائق والآراء: الأرقام من إفصاحات الشركات لدى هيئة الأوراق المالية والبورصات الأمريكية (SEC) ومن مصادر السوق المذكورة ({I['fuentes']}). الحسابات الخاصة موضحة بعبارة «محسوب». لا نصدر أسعارًا مستهدفة ولا نحكم على أن سهمًا ما رخيص أو مرتفع الثمن.
• التحليل الفني: المتوسطات المتحركة ومؤشر القوة النسبية والمؤشر العشوائي ومستويات الدعم والمقاومة محسوبة من بيانات الإغلاق العامة. تصف حركة السعر في الماضي، وليست إشارات شراء أو بيع ولا تتنبأ بالمستقبل.
• تضارب المصالح: لا تملك القناة ولا معدّوها مراكز في الأسهم المذكورة، ولا يتلقون أي مقابل من الشركات، ولم يُرسل المحتوى إلى أي شركة قبل نشره.
• المخاطر: الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال كاملًا، والأداء السابق لا يضمن النتائج المستقبلية. قد تحتوي البيانات على أخطاء، فتحقق منها في مصادرها الأصلية.
• الإنتاج: النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي، ومراجعة مع المصادر المذكورة."""
# Capítulos: los del info.json si todos existen en times.json; si no, los de las 8 secciones del vídeo largo (manual de Daniel, 10-nov-2026)
CAPS = [("s_title", "المقدمة"), ("s_indices", "المؤشرات الرئيسية"), ("s_news", "لماذا تحركت السوق"), ("s_sectores", "القطاعات"),
        ("s_accion_1", "أسهم اليوم"), ("s_macro", "الاقتصاد الكلي والنفط"), ("s_tech_spx", "التحليل الفني: إس آند بي 500"),
        ("s_tech_ndx", "التحليل الفني: ناسداك 100"), ("s_agenda", "ماذا ننتظر في الجلسة المقبلة"), ("s_fin", "الخلاصة وقناة تيليغرام")]
caps = I.get("capitulos") if I.get("capitulos") and all(k in T for k, _ in I["capitulos"]) else [c for c in CAPS if c[0] in T]
cap = "\n".join(f"{mmss(T[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate(caps))
MIN = max(1, round(T.get("_total", 180) / 60))
tg_linea = f"📢 انضموا مجانًا إلى قناتنا على تيليغرام: {TELEGRAM}"
desc = (f"{I['resumen']}\n\n{tg_linea}\n\n{cta_desc}" + "\n\n".join("• " + c for c in I["claves"]) +
        f"\n\nالفصول\n{cap}\n\nالمصادر: {I['fuentes']}. لا نملك مراكز في الأسهم المذكورة.\n\n{AVISO}\n\n{I['hashtags']}\n\nاشترك في القناة: {CANAL}\n{tg_linea}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
json.dump({"title": I["titulo"], "description": desc, "tags": I["tags"], "privacy": "public", "language": "ar", "categoryId": "27"}, open(f"{D}/meta-youtube-{F}-Nabd.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['resumen']}\nالفيديو الكامل (الأخبار والتحليل الأساسي والفني): {{video:{slug}}}\n"
      f"المصادر: {I['fuentes']}. أعدّته نبض وول ستريت في {I['elaborado']} (بتوقيت الرياض). محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. "
      f"التحليل الفني بيانات وليس إشارات شراء أو بيع. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n{cta_post}اشترك في القناة: {CANAL}\n#Shorts #وول_ستريت #الأسهم_الأمريكية #ناسداك")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": I["tags"][:6] + ["Shorts"], "privacy": "public", "language": "ar", "categoryId": "27"}, open(f"{D}/meta-short-{F}-Nabd.json", "w"), ensure_ascii=False, indent=1)
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
x = f"{I['x']}\n\n▶️ {{youtube}}\n{cta_x}{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية."
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
if cta_x and largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) > 280: x = x.replace(cta_x, "")  # sin sitio en X: va sin la línea de la campaña
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX"))
open(f"{D}/post-x-{F}-Nabd.txt", "w").write(x); open(f"{D}/post-threads-{F}-Nabd.txt", "w").write(x)
li = (f"نبض وول ستريت | ملخص جلسة {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n\n".join("• " + c for c in I["claves"]) +
      f"\n\n▶️ الفيديو الكامل ({MIN} دقائق): {{youtube}}\n{cta_post}{canal_linea}\n\n"
      f"المصادر: {I['fuentes']}.\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. التحليل الفني يصف بيانات وليس إشارات شراء أو بيع. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n\n" + I["hashtags"])
assert len(li.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 2950, len(li)
open(f"{D}/post-facebook-{F}-Nabd.txt", "w").write(li)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short subido como video nativo (no enlace), con un resumen con valor
# (3-4 datos clave con cifras y qué cambió + una conclusión, sin relleno), la autoría transparente y al final el enlace al canal.
L = I["linkedin"]
assert 3 <= len(L["datos"]) <= 4, "LinkedIn: 3 o 4 datos clave"
lk = (f"نبض وول ستريت | جلسة {I['fecha_txt']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      "محتوى تعليمي وليس نصيحة استثمارية. التحليل الفني بيانات وليس إشارات شراء أو بيع.\n"
      f"فيديو من إعداد قناة نبض وول ستريت (Nabd Wall Street).\n{CANAL}")
assert len(lk) <= 2950 and "{youtube}" not in lk and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-{F}-Nabd.txt", "w").write(lk)
# TikTok e Instagram (Reels): sin #Shorts (es de YouTube) y con el aviso de IA en el texto, porque el canal es 100% IA (Daniel, 9-nov-2026)
tags_tk = " ".join(t for t in I["hashtags_short"].split() if t.lower() != "#shorts")
tags_tk = ("#نبض_وول_ستريت " + tags_tk).strip() if "#نبض_وول_ستريت" not in tags_tk else tags_tk
tk = (f"{I['tiktok']}\n{cta_post}{canal_linea}\n🤖 فيديو من إعداد الذكاء الاصطناعي (نص وصوت ورسوم).\n"
      f"محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n{tags_tk}")
assert len(tk) <= 2200, len(tk)
open(f"{D}/post-tiktok-{F}-Nabd.txt", "w").write(tk); open(f"{D}/post-instagram-{F}-Nabd.txt", "w").write(tk)
tg = (f"📊 نبض وول ستريت | {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in I["claves_cortas"]) +
      f"\n\n▶️ الفيديو الكامل: {{youtube}}\n{cta_post}{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة.")
open(f"{D}/post-telegram-{F}-Nabd.txt", "w").write(tg)

# Miniatura 1280x720: la fecha de la sesión en destacado, TASI y Nomu
th = I["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="right", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=GOLD, figure=f))
TT(0.955, 0.905, "وول ستريت · جلسة", BG, 26, va="center")
TT(0.955, 0.775, th["fecha"], BG, 50, va="center")
for i, (nom, big, c) in enumerate(th["indices"]):
    xx = 0.955 - i * 0.47
    TT(xx, 0.56, nom, MUTED, 26)
    f.text(xx, 0.35, big, color=col(c), fontsize=78, weight="bold", ha="right")
TT(0.955, 0.17, th["sub"], FG, 28)
TT(0.955, 0.05, th["pie"], BLUE, 22)
p = f"{D}/miniatura-{F}-Nabd.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((190, 190), Image.LANCZOS); im.alpha_composite(lg, (25, 12)); im.convert("RGB").save(p)
print("ok", slug, "desc", len(desc), "li", len(li), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")))
