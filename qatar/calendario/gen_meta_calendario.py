# Textos del Short semanal «تقويم النتائج الأسبوعي» de @QatarAIStocks, generados desde calendario.json:
# meta-short (YouTube Shorts), post-x, post-threads, post-tiktok, post-instagram y post-telegram, todos con "-<semana>-qatar".
# Uso: python3 gen_meta_calendario.py <carpeta de la semana>
# Reglas de Daniel: todo enlaza al canal de YouTube; si hay empresas de EE. UU., se recomienda @NabdWallStreet; aviso en árabe.
import os, sys, json
D = os.path.abspath(sys.argv[1]); S = json.load(open(os.path.join(D, "calendario.json"))); F = S["semana"]
CANAL = "https://www.youtube.com/@QatarAIStocks"; NABD = "https://www.youtube.com/@NabdWallStreet"
AVISO = "محتوى معلوماتي، وليس توصية استثمارية."
E = [e for e in S["escenas"] if e["tipo"] == "empresa"]; G = S["escenas"][0]
hay_eeuu = any("وول ستريت" in e["mercado"] for e in E)
hay_qse = any("بورصة قطر" in e["mercado"] for e in E)


def linea(e, corta=False):
    d = "، ".join(f"{l.replace(' المتوقعة', '').replace(' المتوقع', '')} {v}" for l, v in e["datos"][: (1 if corta else 2)])
    return f"• {e['dia']}: {e['nombre']} ({e['ticker']})" + (f" — {d}" if d else "")


lista = "\n".join(linea(e) for e in E); lista_corta = "\n".join(linea(e, True) for e in E)
gancho = f"هذا الأسبوع تعلن {G['estrella']} نتائجها، و{len(E) - 1} شركات أخرى."
nota_qse = "" if hay_qse else "بورصة قطر: اكتمل موسم نتائج الربع الثالث، ولا إفصاحات نتائج مقررة هذا الأسبوع."
nabd = f"ولأسهم وول ستريت بالعربي تابع قناة نبض وول ستريت: {NABD}" if hay_eeuu else ""
tags_t = " ".join(f"#{e['ticker']}" for e in E[:5])
hashtags = f"#تقويم_النتائج #أسهم_قطر #بورصة_قطر {'#وول_ستريت ' if hay_eeuu else ''}{tags_t} #Shorts"

meta = {
    "title": f"تقويم النتائج الأسبوعي: {G['estrella']} و{len(E) - 1} شركات أخرى ({G['semana']}) #Shorts",
    "description": "\n".join(x for x in [
        f"تقويم النتائج الأسبوعي ({G['semana']}): {gancho}", nota_qse, "", lista, "",
        "التقديرات متوسط توقعات المحللين وقد تتغير قبل الإعلان. التوقيت: بورصة قطر بتوقيت الدوحة، ووول ستريت بتوقيت نيويورك.",
        "تابع القناة لتحليل كل تقرير: " + CANAL, nabd, "",
        S["fuente"].replace("\n", " "), AVISO + " محتوى تعليمي وإعلامي فقط. لا نملك مراكز في الأسهم المذكورة. مُعدّ بأدوات الذكاء الاصطناعي.",
        hashtags] if x is not None),
    "tags": ["تقويم النتائج الأسبوعي", "نتائج الشركات", "أسهم قطر", "بورصة قطر", "Qatar AI Stocks", "وول ستريت"] + [e["nombre"] for e in E] + ["Shorts"],
    "privacy": "public", "language": "ar", "categoryId": "25",
}
meta["description"] = meta["description"].replace("\n\n\n", "\n\n")
assert len(meta["title"]) <= 100, len(meta["title"])

x = f"📅 تقويم النتائج الأسبوعي ({G['semana']})\n{gancho}\n" + "\n".join(f"• {e['ticker']}" + f" {e['dia'].split(' · ')[0].split(' ')[0]}" for e in E) + \
    f"\n\n▶️ {{youtube}}\nقناتنا على يوتيوب: {CANAL}\n{AVISO}"
if len(x) > 280:  # X: la versión mínima
    x = f"📅 تقويم النتائج الأسبوعي: {gancho}\n▶️ {{youtube}}\nقناتنا على يوتيوب: {CANAL}\n" + (f"وول ستريت بالعربي: {NABD}\n" if hay_eeuu else "") + AVISO
threads = f"📅 تقويم النتائج الأسبوعي ({G['semana']})\n{gancho}\n\n💬 أي تقرير تنتظره هذا الأسبوع؟\n\n▶️ {{youtube}}\nقناتنا على يوتيوب: {CANAL}\n" + (f"وول ستريت بالعربي: {NABD}\n" if hay_eeuu else "") + f"\n{AVISO}"
assert len(threads) <= 500, len(threads)
social = "\n".join(x for x in [f"📅 تقويم النتائج الأسبوعي ({G['semana']})", gancho, lista_corta,
                               "▶️ تحليل كل تقرير على يوتيوب: Qatar AI Stocks", f"قناتنا على يوتيوب: {CANAL}",
                               ("وول ستريت بالعربي: قناة نبض وول ستريت على يوتيوب" if hay_eeuu else ""), "🤖 " + AVISO + " مُعدّ بأدوات الذكاء الاصطناعي.", hashtags] if x)
telegram = "\n".join(x for x in [f"📅 تقويم النتائج الأسبوعي | {G['semana']}", "", gancho, nota_qse, "", lista, "",
                                 "▶️ الفيديو: {youtube}", f"قناتنا على يوتيوب: {CANAL}", nabd, "", AVISO] if x is not None)

out = {f"meta-short-{F}-qatar.json": json.dumps(meta, ensure_ascii=False, indent=1), f"post-x-{F}-qatar.txt": x, f"post-threads-{F}-qatar.txt": threads,
       f"post-tiktok-{F}-qatar.txt": social, f"post-instagram-{F}-qatar.txt": social, f"post-telegram-{F}-qatar.txt": telegram}
for k, v in out.items():
    assert "youtube.com/@QatarAIStocks" in v, k
    open(os.path.join(D, k), "w").write(v.strip() + "\n")
print("textos:", ", ".join(out), "| X", len(x), "| Threads", len(threads))

# Guion legible (voz y pantalla de cada escena)
g = [f"# تقويم النتائج الأسبوعي · {G['semana']}", ""]
for i, e in enumerate(S["escenas"]):
    g.append(f"## {i + 1}. {e['tipo']}" + (f" · {e['nombre']} ({e['ticker']}) · {e['dia']}" if e["tipo"] == "empresa" else ""))
    if e["tipo"] == "empresa": g += [f"- {l}: {v}" for l, v in e["datos"]]
    elif e.get("nota"): g.append(e["nota"].replace("\n", " "))
    g += [f"> {e['voz']}", ""]
g += ["المصادر: " + S["fuente"].replace("\n", " "), "", AVISO]
open(os.path.join(D, f"guion-{F}-qatar.md"), "w").write("\n".join(g) + "\n")
