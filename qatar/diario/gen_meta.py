# Metadatos de YouTube (video y Short), posts (X, LinkedIn/Facebook, TikTok, Instagram, Telegram) y miniatura del video diario en árabe.
# Uso: python3 gen_meta.py <carpeta del día>   (lee info.json y times.json, que escribe make_video.py)
# Todos los archivos que se entregan terminan en -qatar (regla de Daniel, 2-nov-2026); encolar.sh los copia a cola-qa/ con los nombres de la cola.
import json, sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
D = sys.argv[1]; I = json.load(open(f"{D}/info.json")); T = dict(json.load(open(f"{D}/times.json")))
slug = f"bolsa-{I['fecha']}"; F = I["fecha"]
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
AVISO = f"""إخلاء مسؤولية مهم
• أعدّته قناة Qatar AI Stocks (أسهم قطر بالذكاء الاصطناعي) في {I['elaborado']} (بتوقيت الدوحة) ببيانات جلسة {I['fecha_txt']}، ويُنشر بعد إغلاق كل يوم تداول.
• هذا المحتوى تعليمي وإعلامي فقط ويعتمد على معلومات عامة. لا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية، ولا يراعي وضعك أو أهدافك أو مدى تحملك للمخاطر. استشر جهة مرخصة من هيئة قطر للأسواق المالية قبل أي قرار استثماري.
• الحقائق والآراء: الأرقام من إفصاحات الشركات في بورصة قطر ومن مصادر السوق المذكورة ({I['fuentes']}). الحسابات الخاصة موضحة بعبارة «محسوب». لا نصدر أسعارًا مستهدفة ولا نحكم على أن سهمًا ما رخيص أو مرتفع الثمن.
• التحليل الفني: المتوسطات المتحركة ومؤشر القوة النسبية والمؤشر العشوائي ومستويات الدعم والمقاومة محسوبة من بيانات الإغلاق العامة. تصف حركة السعر في الماضي، وليست إشارات شراء أو بيع ولا تتنبأ بالمستقبل.
• تضارب المصالح: لا تملك القناة ولا معدّوها مراكز في الأسهم المذكورة، ولا يتلقون أي مقابل من الشركات، ولم يُرسل المحتوى إلى أي شركة قبل نشره.
• المخاطر: الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال كاملًا، والأداء السابق لا يضمن النتائج المستقبلية. قد تحتوي البيانات على أخطاء، فتحقق منها في مصادرها الأصلية.
• الإنتاج: النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي، ومراجعة مع المصادر المذكورة."""
cap = "\n".join(f"{mmss(T[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate(I["capitulos"]))
CTA_TXT = CTA_DESC + "\n\n" if cta_activa() else ""  # campaña de comentarios y suscripción, 8 al 22-nov-2026 (ver comun.py)
desc = (f"{CTA_TXT}{I['resumen']}\n\n" + "\n\n".join("• " + c for c in I["claves"]) +
        f"\n\nالفصول\n{cap}\n\nالمصادر: {I['fuentes']}. لا نملك مراكز في الأسهم المذكورة.\n\n{AVISO}\n\n{I['hashtags']}\n\nاشترك في القناة: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
json.dump({"title": I["titulo"], "description": desc, "tags": I["tags"], "language": "ar", "privacy": "public"}, open(f"{D}/meta-youtube-{F}-qatar.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{CTA_TXT}{I['resumen']}\nالفيديو الكامل (الأخبار والتحليل الأساسي والفني): {{video:{slug}}}\n"
      f"المصادر: {I['fuentes']}. أعدّته Qatar AI Stocks في {I['elaborado']} (بتوقيت الدوحة). محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. "
      f"التحليل الفني بيانات وليس إشارات شراء أو بيع. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\nاشترك في القناة: {CANAL}\n#Shorts #أسهم_قطر #بورصة_قطر #قطر")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": I["tags"][:6] + ["Shorts"], "language": "ar", "privacy": "public"}, open(f"{D}/meta-short-{F}-qatar.json", "w"), ensure_ascii=False, indent=1)
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
x = f"{I['x']}\n\n▶️ {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية."
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX"))
open(f"{D}/post-x-{F}-qatar.txt", "w").write(x)
li = (f"أسهم قطر | ملخص جلسة بورصة قطر {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n\n".join("• " + c for c in I["claves"]) +
      f"\n\n▶️ الفيديو الكامل (3 دقائق): {{youtube}}\n{canal_linea}\n\n"
      f"المصادر: {I['fuentes']}.\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. التحليل الفني يصف بيانات وليس إشارات شراء أو بيع. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n\n" + I["hashtags"])
assert len(li.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 2950, len(li)
open(f"{D}/post-linkedin-{F}-qatar.txt", "w").write(li)
open(f"{D}/post-facebook-{F}-qatar.txt", "w").write(li)  # página de Facebook (Buffer 1): mismo texto que LinkedIn
tk = f"{I['tiktok']}\n{canal_linea}\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n{I['hashtags_short']}"
open(f"{D}/post-tiktok-{F}-qatar.txt", "w").write(tk); open(f"{D}/post-instagram-{F}-qatar.txt", "w").write(tk)
tg = (f"📊 أسهم قطر | بورصة قطر {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in I["claves_cortas"]) +
      f"\n\n▶️ الفيديو الكامل: {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة.")
open(f"{D}/post-telegram-{F}-qatar.txt", "w").write(tg)

# Miniatura 1280x720: la fecha de la sesión en destacado y el cierre de los dos índices
th = I["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="right", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=GOLD, figure=f))
TT(0.955, 0.905, "بورصة قطر · جلسة", BG, 26, va="center")
TT(0.955, 0.775, th["fecha"], BG, 50, va="center")
for i, (nom, big, c) in enumerate(th["indices"]):
    xx = 0.955 - i * 0.47
    TT(xx, 0.56, nom, MUTED, 28)
    f.text(xx, 0.33, big, color=col(c), fontsize=96 if len(th["indices"]) == 1 else 78, weight="bold", ha="right")
if th.get("cierre"): f.text(0.30, 0.36, th["cierre"], color=FG, fontsize=60, weight="bold", ha="center")
TT(0.955, 0.17, th["sub"], FG, 28)
TT(0.955, 0.05, th["pie"], BLUE, 22)
p = f"{D}/miniatura-{F}-qatar.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((190, 190), Image.LANCZOS); im.alpha_composite(lg, (25, 12)); im.convert("RGB").save(p)
print("ok", slug, "desc", len(desc), "li", len(li), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")))
