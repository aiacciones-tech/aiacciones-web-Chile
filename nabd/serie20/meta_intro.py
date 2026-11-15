# Metadatos de YouTube (vídeo y Short), posts (Telegram, X, LinkedIn, TikTok, Instagram) y miniatura del vídeo de presentación
# de la serie «عمالقة وول ستريت». Uso: python3 meta_intro.py <carpeta>   (lee video.json y times.json de make_intro.py)
# Todo termina en -Nabd (regla de Daniel). encolar_intro.sh lo copia a cola-nabd/ con los nombres que esperan los workflows.
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); E = VJ["empresas"]; SERIE = VJ["serie"]
T_ = dict(json.load(open(f"{D}/times.json"))); SLUG = "serie20-intro"
TOTAL = sum(e["cap"] for e in E) / 1000
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
CAPS = [("s_portada", "المقدمة"), ("s_porque", "لماذا هذه الشركات"), ("s_lista_1", "القائمة"), ("s_que", "ماذا سنحلل في كل حلقة"),
        ("s_como", "مصادر الأرقام"), ("s_formato", "كيف ستسير السلسلة"), ("s_fin", "الختام")]
cap = "\n".join(f"{mmss(T_[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate(CAPS))
lista = "\n".join(f"{i + 1}. {e['ar']} ({e['ticker']}) · {e['cap']:,.0f} مليار دولار" for i, e in enumerate(E))
tg_linea = f"📢 انضموا مجانًا إلى قناتنا على تيليغرام: {TELEGRAM}"
AVISO = """إخلاء مسؤولية مهم
• هذا المحتوى تعليمي وإعلامي فقط ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية. استشر جهة مرخصة في بلدك قبل أي قرار استثماري.
• القيمة السوقية من TradingView عند إغلاق 12 نوفمبر 2026 في نيويورك، والمجموع محسوب. أرقام الحلقات من إفصاحات الشركات لدى هيئة الأوراق المالية والبورصات الأمريكية (SEC) وبيانات نتائجها.
• لا نصدر أسعارًا مستهدفة ولا نحكم على أن سهمًا ما رخيص أو مرتفع الثمن. لا تملك القناة ولا معدّوها مراكز في الأسهم المذكورة ولا يتلقون مقابلًا من الشركات.
• الاستثمار في الأسهم ينطوي على مخاطر، والأداء السابق لا يضمن النتائج المستقبلية.
• الإنتاج: النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي."""
resumen = (f"سلسلة جديدة على نبض وول ستريت: «{SERIE}». نحلل القوائم المالية ونتائج 20 من أكبر الشركات الأمريكية، "
           f"قيمتها السوقية مجتمعةً نحو {TOTAL:.1f} تريليون دولار (محسوب، إغلاق 12 نوفمبر 2026). "
           "حلقة لكل شركة بعد إعلان نتائجها الفصلية، لا تزيد على 4 دقائق، بدءًا من موسم النتائج الحالي.")
titulo = f"سلسلة جديدة: {SERIE} | القوائم المالية ونتائج 20 من أكبر الشركات الأمريكية"
desc = (f"{resumen}\n\n{tg_linea}\n\nماذا سنحلل في كل حلقة\n• قائمة الدخل: الإيرادات وهوامش الربح وربحية السهم\n• الميزانية العمومية: النقد والديون وحقوق المساهمين\n"
        "• التدفقات النقدية: التدفق النقدي الحر والإنفاق الرأسمالي والتوزيعات وإعادة شراء الأسهم\n• النتائج مقارنةً بتوقعات المحللين وتوجيهات الإدارة\n"
        f"• نسبة الديون والنقد إلى القيمة السوقية\n\nالشركات العشرون (حسب القيمة السوقية)\n{lista}\n\nالفصول\n{cap}\n\n"
        f"💬 أي شركة تنتظر نتائجها أكثر؟ اكتب لنا في التعليقات.\n\n{AVISO}\n\n"
        "#عمالقة_وول_ستريت #نبض_وول_ستريت #الأسهم_الأمريكية #وول_ستريت #القوائم_المالية #نتائج_الشركات #ناسداك\n\n"
        f"اشترك في القناة: {CANAL}\n{tg_linea}")
tags = ["عمالقة وول ستريت", "نبض وول ستريت", "Nabd Wall Street", "الأسهم الأمريكية", "القوائم المالية", "نتائج الشركات", "وول ستريت",
        "إنفيديا", "آبل", "مايكروسوفت", "أمازون", "تسلا", "Nvidia", "Apple", "Microsoft", "earnings"]
assert len(titulo) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(titulo), len(desc))
json.dump({"title": titulo, "description": desc, "tags": tags, "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-youtube-serie-20-acciones-Nabd.json", "w"), ensure_ascii=False, indent=1)
tshort = f"سلسلة جديدة: {SERIE} 🇺🇸 القوائم المالية لـ20 من أكبر الشركات الأمريكية"
sd = (f"{resumen}\nفيديو التعريف الكامل: {{video:{SLUG}}}\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة. "
      f"الاستثمار ينطوي على مخاطر. النص والصوت والرسوم من إعداد الذكاء الاصطناعي.\nاشترك في القناة: {CANAL}\n#Shorts #عمالقة_وول_ستريت #وول_ستريت #الأسهم_الأمريكية")
assert len(tshort) <= 100 and len(sd) < 5000
json.dump({"title": tshort, "description": sd, "tags": tags[:6] + ["Shorts"], "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-short-serie-20-acciones-Nabd.json", "w"), ensure_ascii=False, indent=1)
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
x = (f"سلسلة جديدة على نبض وول ستريت: «{SERIE}» 📊\nنحلل القوائم المالية ونتائج 20 من أكبر الشركات الأمريكية، من آبل وإنفيديا إلى نتفليكس، "
     f"بعد كل إعلان نتائج.\n\n▶️ {{youtube}}\n\nمحتوى تعليمي وليس نصيحة استثمارية.")
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x)
open(f"{D}/post-x-serie-20-acciones-Nabd.txt", "w").write(x)
lk = (f"نبض وول ستريت | سلسلة جديدة: {SERIE}\n\n"
      f"• 20 من أكبر الشركات الأمريكية، قيمتها السوقية مجتمعةً نحو {TOTAL:.1f} تريليون دولار (محسوب من بيانات TradingView، إغلاق 12 نوفمبر 2026).\n"
      f"• أكبرها آبل ({E[0]['cap'] / 1000:.2f} تريليون) ثم إنفيديا ({E[1]['cap'] / 1000:.2f}) ومايكروسوفت ({E[2]['cap'] / 1000:.2f}).\n"
      "• بعد كل إعلان نتائج فصلية: حلقة لا تزيد على 4 دقائق عن قائمة الدخل والميزانية والتدفقات النقدية والنتائج مقارنةً بالتوقعات.\n\n"
      "الخلاصة: قراءة منهجية لأرقام الشركات التي تحرك وول ستريت، من مصادرها الرسمية (SEC)، ومن دون توصيات.\n\n"
      "محتوى تعليمي وليس نصيحة استثمارية.\n"
      f"فيديو من إعداد قناة نبض وول ستريت (Nabd Wall Street).\n{CANAL}")
assert len(lk) <= 2950 and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-serie-20-acciones-Nabd.txt", "w").write(lk)
tk = (f"سلسلة جديدة: {SERIE} 📊 نحلل القوائم المالية ونتائج 20 من أكبر الشركات الأمريكية بعد كل إعلان نتائج. أي شركة تنتظر نتائجها أكثر؟\n"
      f"{canal_linea}\n🤖 فيديو من إعداد الذكاء الاصطناعي (نص وصوت ورسوم).\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. الاستثمار ينطوي على مخاطر.\n"
      "#نبض_وول_ستريت #عمالقة_وول_ستريت #وول_ستريت #الأسهم_الأمريكية #أسهم #استثمار")
assert len(tk) <= 2200
open(f"{D}/post-tiktok-serie-20-acciones-Nabd.txt", "w").write(tk); open(f"{D}/post-instagram-serie-20-acciones-Nabd.txt", "w").write(tk)
tg = (f"📊 نبض وول ستريت | سلسلة جديدة: {SERIE}\n\n{resumen}\n\n• قائمة الدخل والميزانية والتدفقات النقدية\n• النتائج مقارنةً بتوقعات المحللين\n"
      f"• الشركات: " + "، ".join(e["ar"] for e in E) + f"\n\n▶️ فيديو التعريف: {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة.")
assert len(tg) <= 1024, len(tg)  # pie de foto de Telegram
open(f"{D}/post-telegram-serie-20-acciones-Nabd.txt", "w").write(tg)

# Miniatura 1280x720
f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="right", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=GOLD, figure=f))
TT(0.955, 0.905, "سلسلة جديدة", BG, 28, va="center")
TT(0.955, 0.775, SERIE, BG, 54, va="center")
f.text(0.955, 0.33, "20", color=GOLD, fontsize=170, weight="bold", ha="right")
TT(0.62, 0.53, "شركة أمريكية عملاقة", FG, 34)
TT(0.62, 0.42, "القوائم المالية والنتائج", BLUE, 30)
TT(0.62, 0.31, f"{TOTAL:.1f} تريليون دولار", GOLD, 30)
for i, e in enumerate(E[:10]):
    f.text(0.955 - i * 0.094, 0.10, e["ticker"], color=MUTED, fontsize=20, weight="bold", ha="right")
p = f"{D}/miniatura-serie-20-acciones-Nabd.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((190, 190), Image.LANCZOS); im.alpha_composite(lg, (25, 12)); im.convert("RGB").save(p)
print("ok desc", len(desc), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")), "tg", len(tg), "titulo", len(titulo))
