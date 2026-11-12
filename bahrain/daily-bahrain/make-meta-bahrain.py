# YouTube metadata (video and Short), posts (X, Threads, Facebook, TikTok, Instagram, Telegram) and thumbnail of the daily Arabic video of @BahrainAIStocks.
# Usage: python3 make-meta-bahrain.py <day folder>   (reads info-bahrain.json and times-bahrain.json, written by make-video-bahrain.py)
# Every delivered file ends in -bahrain (Daniel's rule); enqueue-daily-bahrain.sh copies them to cola-bahrain/ with the queue's names.
import json, sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import importlib.util
def _load(n):
    sp = importlib.util.spec_from_file_location(n.replace("-", "_"), os.path.join(HERE, n + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
_C = _load("common-bahrain"); globals().update({k: getattr(_C, k) for k in dir(_C) if not k.startswith("__")})
D = sys.argv[1]; I = json.load(open(f"{D}/info-bahrain.json")); T = dict(json.load(open(f"{D}/times-bahrain.json")))
slug = "daily-" + I["fecha"]; F = I["fecha"]
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
AVISO = f"""إخلاء مسؤولية مهم
• أعدّته قناة Bahrain AI Stocks في {I['elaborado']} (بتوقيت المنامة) ببيانات جلسة {I['fecha_txt']}، ويُنشر بعد إغلاق كل يوم تداول.
• هذا المحتوى تعليمي وإعلامي فقط ويعتمد على معلومات عامة. لا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية، ولا يراعي وضعك أو أهدافك أو مدى تحملك للمخاطر. استشر جهة مرخصة من مصرف البحرين المركزي قبل أي قرار استثماري.
• الحقائق والآراء: الأرقام من إفصاحات الشركات على بورصة البحرين ومن مصادر السوق المذكورة ({I['fuentes']}). الحسابات الخاصة موضحة بعبارة «محسوب». لا نصدر أسعارًا مستهدفة ولا نحكم على أن سهمًا ما رخيص أو مرتفع الثمن.
• التحليل الفني: المتوسطات المتحركة ومؤشر القوة النسبية والمؤشر العشوائي و MACD ومتوسط المدى الحقيقي ATR والتقلب ومستويات الدعم والمقاومة محسوبة من بيانات الإغلاق العامة. تصف حركة السعر في الماضي، وليست إشارات شراء أو بيع ولا تتنبأ بالمستقبل.
• تضارب المصالح: لا تملك القناة ولا معدّوها مراكز في الأسهم المذكورة، ولا يتلقون أي مقابل من الشركات، ولم يُرسل المحتوى إلى أي شركة قبل نشره.
• المخاطر: الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال كاملًا، والأداء السابق لا يضمن النتائج المستقبلية. قد تحتوي البيانات على أخطاء، فتحقق منها في مصادرها الأصلية.
• الإنتاج: النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي، ومراجعة مع المصادر المذكورة."""
cap = "\n".join(f"{mmss(T[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate([c for c in I["capitulos"] if c[0] in T]))  # s_tech_acc only exists when the scanner has data
CTA = (CTA_DESC + CANAL + "\n\n") if cta_activa(I["fecha"]) else ""
desc = (f"{I['resumen']}\n\n" + CTA + "\n\n".join("• " + c for c in I["claves"]) +
        f"\n\nالفصول\n{cap}\n\nالمصادر: {I['fuentes']}. لا نملك مراكز في الأسهم المذكورة.\n\n{AVISO}\n\n{I['hashtags']}\n\nاشترك في القناة: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
json.dump({"title": I["titulo"], "description": desc, "tags": I["tags"], "privacy": "public", "language": "ar", "categoryId": "27"}, open(f"{D}/meta-youtube-{F}-bahrain.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['resumen']}\n" + CTA.replace("\n\n", "\n") + f"الفيديو الكامل (الأخبار والتحليل الأساسي والفني): {{video:{slug}}}\n"
      f"المصادر: {I['fuentes']}. أعدّته Bahrain AI Stocks في {I['elaborado']} (بتوقيت المنامة). محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. "
      f"التحليل الفني بيانات وليس إشارات شراء أو بيع. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\nاشترك في القناة: {CANAL}\n#Shorts #أسهم_البحرين #بورصة_البحرين #مؤشر_البحرين_العام")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": I["tags"][:6] + ["Shorts"], "privacy": "public", "language": "ar", "categoryId": "27"}, open(f"{D}/meta-short-{F}-bahrain.json", "w"), ensure_ascii=False, indent=1)
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
x = f"{I['x']}\n\n▶️ {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية."
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX"))
open(f"{D}/post-x-{F}-bahrain.txt", "w").write(x); open(f"{D}/post-threads-{F}-bahrain.txt", "w").write(x)
li = (f"أسهم البحرين | ملخص جلسة {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n\n".join("• " + c for c in I["claves"]) +
      f"\n\n▶️ الفيديو الكامل (3 دقائق): {{youtube}}\n{canal_linea}\n\n"
      f"المصادر: {I['fuentes']}.\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. التحليل الفني يصف بيانات وليس إشارات شراء أو بيع. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n\n" + I["hashtags"])
assert len(li.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 2950, len(li)
open(f"{D}/post-facebook-{F}-bahrain.txt", "w").write(li)
# LinkedIn (Daniel, permanent rule from 8-nov-2026): the Short uploaded as a video, with a summary of 3-4 key data of the
# video (figures and what changed) and a conclusion, no filler; it says the video is by the channel and ends with the channel link.
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4 and L["conclusion"], "info-bahrain.json: linkedin needs 3-4 datos and a conclusion"
ln = (f"بورصة البحرين | {I['fecha_txt']}\n\n" + "\n".join("• " + d for d in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      "محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية.\n"
      f"🎬 فيديو من إعداد قناة Bahrain AI Stocks (أسهم البحرين).\n▶️ {CANAL}")
assert ln.rstrip().endswith(CANAL) and "{youtube}" not in ln and len(ln) <= 2950, len(ln)
open(f"{D}/post-linkedin-{F}-bahrain.txt", "w").write(ln)
tk = f"{I['tiktok']}\n{canal_linea}\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\n{I['hashtags_short']}"
open(f"{D}/post-tiktok-{F}-bahrain.txt", "w").write(tk); open(f"{D}/post-instagram-{F}-bahrain.txt", "w").write(tk)
tg = (f"📊 أسهم البحرين | {I['fecha_txt']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in I["claves_cortas"]) +
      f"\n\n▶️ الفيديو الكامل: {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة.")
open(f"{D}/post-telegram-{F}-bahrain.txt", "w").write(tg)

# Thumbnail 1280x720: the session date highlighted, the All Share Index
th = I["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="right", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=BAND, figure=f))
TT(0.955, 0.905, "بورصة البحرين · جلسة", FG, 26, va="center")
TT(0.955, 0.775, th["fecha"], FG, 50, va="center")
for i, (nom, big, c) in enumerate(th["indices"]):
    xx = 0.955 - i * 0.47
    TT(xx, 0.56, nom, MUTED, 26)
    f.text(xx, 0.35, big, color=col(c), fontsize=78, weight="bold", ha="right")
TT(0.955, 0.17, th["sub"], FG, 28)
TT(0.955, 0.05, th["pie"], BLUE, 22)
p = f"{D}/thumbnail-{F}-bahrain.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); im.alpha_composite(logo_img(190), (25, 12)); im.convert("RGB").save(p)
print("ok", slug, "desc", len(desc), "li", len(li), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")))
