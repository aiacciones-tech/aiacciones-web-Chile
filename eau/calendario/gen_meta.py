# Metadatos del Short (YouTube) y posts (X, LinkedIn, TikTok, Instagram, Telegram, Threads) del calendario semanal de resultados.
# Uso: python3 gen_meta.py <carpeta de la semana>   (lee info.json). Todo lo entregado termina en -UAE (regla de Daniel, 5-nov-2026).
# Cada post lleva el enlace al canal (regla 29-oct-2026); si hay empresas de EE. UU. ("usa": true), recomienda Nabd Wall Street
# (Daniel, 22-nov-2026). LinkedIn: el Short como video nativo, 3-4 datos + conclusión, «فيديو من إعداد قناة AI Stocks UAE», termina en el canal.
import json, sys, os, re
D = sys.argv[1]; I = json.load(open(f"{D}/info.json")); F = I["fecha"]
CANAL = "https://www.youtube.com/@AIStocksUAE"; NABD = "https://www.youtube.com/@NabdWallStreet"
AVISO = "محتوى إعلامي، وليس توصية استثمارية."
nabd = f"لمتابعة وول ستريت بالعربية: قناة نبض وول ستريت {NABD}" if I.get("usa") else ""
lista = "\n".join("• " + x for x in I["empresas"])
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
w = lambda n, s: open(f"{D}/{n}-{F}-UAE.txt", "w").write(s.strip() + "\n")

desc = (f"تقويم النتائج الأسبوعي ({I['semana_txt']}): الشركات الأهم التي تعلن نتائجها من الاثنين إلى الجمعة، "
        f"أولًا سوق أبوظبي وسوق دبي ثم كبرى الشركات الأمريكية.\n\n• {I['local']}\n{lista}\n• {I['nota_semana']}\n\n"
        f"التقديرات هي متوسط توقعات المحللين (الربحية المعدلة للسهم والإيرادات) كما نشرتها المصادر في {I['elaborado']}، وقد تتغير قبل الإعلان.\n"
        f"المصادر: {I['fuentes']}.\n\n{nabd}\n\n{AVISO} لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر. "
        f"النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي ومراجعة مع المصادر.\n\nاشترك في القناة: {CANAL}\n#Shorts {I['hashtags']}")
assert len(I["titulo_short"]) <= 100 and "<" not in desc and ">" not in desc and len(desc) < 5000
json.dump({"title": I["titulo_short"], "description": desc, "tags": I["tags"] + ["Shorts"], "privacy": "public"},
          open(f"{D}/meta-short-{F}-UAE.json", "w"), ensure_ascii=False, indent=1)

x = f"📅 تقويم النتائج الأسبوعي ({I['semana_txt']})\n" + "\n".join(I["empresas_cortas"]) + f"\n\n▶️ {{youtube}}\n{CANAL}\n" + (f"وول ستريت بالعربية: {NABD}\n" if nabd else "") + AVISO
assert largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 280, largo_x(x)
w("post-x", x)
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4
lk = (f"تقويم النتائج الأسبوعي | {I['semana_txt']}\n\n" + "\n".join("• " + d for d in L["datos"]) + f"\n\nالخلاصة: {L['conclusion']}\n\n"
      + (nabd + "\n\n" if nabd else "") + f"{AVISO} لا نملك مراكز في الأسهم المذكورة.\nفيديو من إعداد قناة AI Stocks UAE.\n{CANAL}")
assert len(lk) <= 2950 and lk.rstrip().endswith(CANAL)
w("post-linkedin", lk)
tk = (f"📅 تقويم النتائج الأسبوعي ({I['semana_txt']}): {I['gancho']}\n" + "\n".join(I["empresas_cortas"]) +
      f"\n\n{nabd}\nقناتنا على يوتيوب: {CANAL}\n{AVISO}\n{I['hashtags']}")
w("post-tiktok", tk); w("post-instagram", tk)
tg = (f"📅 تقويم النتائج الأسبوعي | {I['semana_txt']}\n\n🇦🇪 {I['local']}\n\n🇺🇸 وول ستريت:\n{lista}\n\n{I['nota_semana']}\n\n"
      f"▶️ الفيديو: {{youtube}}\nقناتنا على يوتيوب: {CANAL}\n{nabd}\n\n{AVISO}")
w("post-telegram", tg)
th = (f"📅 تقويم النتائج الأسبوعي ({I['semana_txt']})\n" + "\n".join(I["empresas_cortas"]) +
      f"\n\n▶️ {{youtube}}\n{CANAL}\n" + (f"وول ستريت بالعربية: {NABD}\n" if nabd else "") + AVISO)
assert len(th.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")) <= 500, len(th)
w("post-threads", th)
print("ok desc", len(desc), "x", largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")), "li", len(lk), "threads", len(th))
