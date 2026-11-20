# Metadatos de YouTube (vídeo y Short), posts (X, Facebook, LinkedIn, TikTok, Instagram, Telegram) y miniatura de un capítulo de la serie
# semanal «التحليل الأساسي ببساطة» de @QatarAIStocks. Uso: python3 meta_capitulo.py <carpeta del capítulo>  (lee video.json y times.json)
# Todo lo que se entrega termina en -qatar (regla de Daniel, 2-nov-2026) y todo post lleva el enlace al canal (regla de Daniel).
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_fund import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
BASE = VJ["base"]; I = VJ["info"]; N = VJ["capitulo_n"]
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
CTA = (CTA_DESC + "\n\n") if cta_activa(VJ["publicar"]) else ""
canal_linea = f"قناتنا على يوتيوب: {CANAL}"
dur = round(T_.get("_total", 0) / 60)
AVISO = f"""إخلاء مسؤولية مهم
• محتوى تعليمي وإعلامي فقط ضمن سلسلة «{SERIE}». لا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية، ولا يراعي وضعك أو أهدافك. {VJ['nombre']} مجرد مثال للشرح، واختيارها لا يعني رأيًا فيها. استشر جهة مرخصة من هيئة قطر للأسواق المالية قبل أي قرار استثماري.
• الأرقام من القوائم المالية الرسمية للشركة ومن TradingView ومن المصادر المذكورة. الحسابات الخاصة موضحة بعبارة «محسوب». لا نصدر أسعارًا مستهدفة ولا نحكم على أن سهمًا ما رخيص أو مرتفع الثمن.
• لا تملك القناة ولا معدّوها مراكز في الأسهم المذكورة، ولا يتلقون أي مقابل من الشركات.
• الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال، والأداء السابق لا يضمن النتائج المستقبلية. قد تحتوي البيانات على أخطاء، فتحقق منها في مصادرها الأصلية.
• النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي، ومراجعة مع المصادر المذكورة."""
serie_txt = f"سلسلة «{SERIE}»: حلقة كل سبت، نشرح فيها مفهومًا واحدًا من التحليل الأساسي على الأرقام الحقيقية لشركة مدرجة في بورصة قطر."
desc = (f"{I['resumen']}\n\n{CTA}" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nالفصول\n{cap}\n\nالمصادر: {I['fuentes']}.\n\n{serie_txt}"
        + (f" الحلقة القادمة: {fin['siguiente']}." if fin.get("siguiente") else "") + f"\n\n{AVISO}\n\n{I['hashtags']}\n\nاشترك في القناة: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(I["titulo"]), len(desc))
tags = list(dict.fromkeys([SERIE, "التحليل الأساسي", "أسهم قطر", "بورصة قطر", "Qatar AI Stocks", VJ["nombre"], VJ["tema"]] + I.get("tags", [])))
json.dump({"title": I["titulo"], "description": desc, "tags": tags, "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}-qatar.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['resumen']}\n{CTA}الحلقة كاملة ({dur} دقائق): {{video:{BASE}}}\nالمصادر: {I['fuentes']}. محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. "
      f"لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر. مُعدّ بأدوات الذكاء الاصطناعي.\nاشترك في القناة: {CANAL}\n{I['hashtags_short']}")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": tags[:8] + ["Shorts"], "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-short-{BASE}-qatar.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n{canal_linea}\nمحتوى تعليمي وليس نصيحة استثمارية."
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX"))
open(f"{D}/post-x-{BASE}-qatar.txt", "w").write(x)
# Threads (Buffer 1; sustituye a Facebook, que cerró la cuenta el 12-nov-2026): máx. 500 caracteres, con una pregunta y el enlace al canal.
th = f"{I['x']}\n\n💬 {I.get('pregunta', 'ما المفهوم المالي الذي تريد أن نشرحه في حلقة قادمة؟')}\n\n▶️ {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية."
assert len(th.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 500, len(th)
open(f"{D}/post-threads-{BASE}-qatar.txt", "w").write(th)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short como vídeo nativo; 3-4 datos clave + conclusión; autoría; enlace al canal al final.
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4, "LinkedIn: 3 o 4 datos clave"
lk = (f"{SERIE} | الحلقة {N}: {VJ['tema']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      "محتوى تعليمي وليس نصيحة استثمارية. الأرقام من القوائم المالية الرسمية للشركة.\n"
      f"فيديو من إعداد قناة Qatar AI Stocks.\n{CANAL}")
assert len(lk) <= 2950 and "{youtube}" not in lk and lk.rstrip().endswith(CANAL)
open(f"{D}/post-linkedin-{BASE}-qatar.txt", "w").write(lk)
tk = (f"{SERIE} · الحلقة {N}: {VJ['tema']}\n{I['x']}\n▶️ الحلقة كاملة على يوتيوب: Qatar AI Stocks\n{canal_linea}\n"
      f"🤖 مُعدّ بأدوات الذكاء الاصطناعي (النص والصوت والرسوم). محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية. {VJ['nombre']} مجرد مثال. الاستثمار ينطوي على مخاطر.\n{I['hashtags_short']}")
assert len(tk) <= 2200 and "{youtube}" not in tk
open(f"{D}/post-tiktok-{BASE}-qatar.txt", "w").write(tk); open(f"{D}/post-instagram-{BASE}-qatar.txt", "w").write(tk)
tg = (f"📚 {SERIE} | الحلقة {N}: {VJ['tema']} ({VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ الحلقة كاملة: {{youtube}}\n{canal_linea}\n\nمحتوى تعليمي وليس نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة.")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-qatar.txt", "w").write(tg)

# Miniatura 1280x720: banda dorada con la serie, pregunta grande y hasta tres cifras clave
th = VJ["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="right", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.82), 1.0, 0.18, transform=f.transFigure, color=GOLD, figure=f))
TT(0.955, 0.91, th["etiqueta"], BG, 30, va="center")
TT(0.955, 0.66, th["titulo"], FG, 64 if len(th["titulo"]) <= 16 else 50, va="center")
TT(0.955, 0.52, th["sub"], MUTED, 28, va="center")
C = th.get("cifras", [])[:3]
for i, (big, lab, c) in enumerate(C):
    xx = 0.955 - i * 0.31
    f.text(xx, 0.24, big, color=col(c), fontsize=70, weight="bold", ha="right")
    TT(xx, 0.16, lab, FG, 24)
TT(0.955, 0.05, th["pie"], BLUE, 22)
p = f"{D}/miniatura-{BASE}-qatar.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((170, 170), Image.LANCZOS); im.alpha_composite(lg, (25, 150)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "th", len(th), "tg", len(tg), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")))
