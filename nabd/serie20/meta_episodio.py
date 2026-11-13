# Metadatos de YouTube, posts (Telegram y X) y miniatura de un episodio de «عمالقة وول ستريت».
# Uso: python3 meta_episodio.py <carpeta del episodio>   (lee video.json y times.json de make_episodio.py)
# Sin Short: la serie sube como máximo 3 vídeos al día y así el canal no pasa del límite de YouTube (~10 subidas en 24 h) con el diario.
import json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
SERIE = "عمالقة وول ستريت"; BASE = f"serie20-{VJ['ticker'].lower()}-{VJ['fecha_resultados']}"
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
CAPS = [("e_portada", "المقدمة"), ("e_resultados", "نتائج الربع"), ("e_ingresos", "الإيرادات والهامش"), ("e_balance", "الميزانية والديون"),
        ("e_flujo", "التدفقات النقدية"), ("e_expectativas", "مقارنةً بالتوقعات"), ("e_fin", "الخلاصة")]
cap = "\n".join(f"{mmss(T_[k]) if i else '0:00'} {t}" for i, (k, t) in enumerate(CAPS) if k in T_)
tg_linea = f"📢 انضموا مجانًا إلى قناتنا على تيليغرام: {TELEGRAM}"
AVISO = """إخلاء مسؤولية مهم
• هذا المحتوى تعليمي وإعلامي فقط ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية. استشر جهة مرخصة في بلدك قبل أي قرار استثماري.
• الأرقام من TradingView (بيانات أساسية مأخوذة من تقارير الشركة) ومن بيان نتائج الشركة والمصادر المذكورة. الحسابات الخاصة موضحة بعبارة «محسوب».
• نسب الديون والنقد إلى القيمة السوقية بيانات وليست حكمًا شرعيًا. لا نصدر أسعارًا مستهدفة ولا نحكم على أن سهمًا ما رخيص أو مرتفع الثمن.
• لا تملك القناة ولا معدّوها مراكز في الأسهم المذكورة ولا يتلقون مقابلًا من الشركات. الاستثمار ينطوي على مخاطر، والأداء السابق لا يضمن النتائج المستقبلية.
• الإنتاج: النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي."""
I = VJ["info"]
titulo = I["titulo"]
desc = (f"{I['resumen']}\n\n{tg_linea}\n\n" + "\n".join("• " + c for c in VJ["claves"]) + f"\n\nالفصول\n{cap}\n\n"
        f"المصادر: {I['fuentes']}\n\nسلسلة «{SERIE}»: حلقة عن كل شركة من أكبر 20 شركة أمريكية بعد إعلان نتائجها.\n\n{AVISO}\n\n"
        f"#عمالقة_وول_ستريت #نبض_وول_ستريت {I['hashtags']}\n\nاشترك في القناة: {CANAL}\n{tg_linea}")
assert len(titulo) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000, (len(titulo), len(desc))
tags = ["عمالقة وول ستريت", "نبض وول ستريت", "Nabd Wall Street", VJ["ar"], VJ["en"], VJ["ticker"], "نتائج الشركات", "القوائم المالية",
        "الأسهم الأمريكية", "earnings"] + I.get("tags", [])
json.dump({"title": titulo, "description": desc, "tags": tags, "privacy": "public", "language": "ar", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}-Nabd.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n\n#عمالقة_وول_ستريت · محتوى تعليمي وليس نصيحة استثمارية."
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x)
open(f"{D}/post-x-{BASE}-Nabd.txt", "w").write(x)
tg = (f"📊 {SERIE} | {VJ['ar']} ({VJ['ticker']}) · {VJ['trimestre']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in VJ["claves"]) +
      f"\n\n▶️ الحلقة كاملة: {{youtube}}\nقناتنا على يوتيوب: {CANAL}\n\nمحتوى تعليمي وليس نصيحة استثمارية. لا نملك مراكز في الأسهم المذكورة.")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}-Nabd.txt", "w").write(tg)

# Miniatura 1280x720
th = VJ["miniatura"]; f = fig(1280, 720)
TT = lambda x, y, s, c, fs, w="bold", ha="right", **k: f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)
f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.30, transform=f.transFigure, color=GOLD, figure=f))
TT(0.955, 0.905, f"{SERIE} · {VJ['trimestre']}", BG, 24, va="center")
TT(0.955, 0.775, VJ["ar"], BG, 56, va="center")
f.text(0.30, 0.775, VJ["ticker"], color=BG, fontsize=40, weight="bold", ha="left", va="center")
TT(0.955, 0.55, th["etiqueta"], MUTED, 30)
f.text(0.955, 0.33, th["cifra"], color=col(th.get("color", "gold")), fontsize=96, weight="bold", ha="right")
TT(0.955, 0.15, th["sub"], FG, 30)
p = f"{D}/miniatura-{BASE}-Nabd.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA").resize((190, 190), Image.LANCZOS); im.alpha_composite(lg, (25, 12)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc), "tg", len(tg), "titulo", len(titulo))
