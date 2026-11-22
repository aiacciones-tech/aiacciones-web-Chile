# Textos del Short «تقويم النتائج الأسبوعي» (nabd/calendario/): meta de YouTube, posts de X, Telegram, TikTok, Instagram y LinkedIn (Facebook y Threads fuera hasta nuevo aviso),
# y el guion legible (guion-<base>-Nabd.md). Todo sale de video.json; se escriben en la misma carpeta con nombres que terminan en -Nabd.
# Uso: python3 meta_calendario.py <carpeta>/video.json
import os, sys, json, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from make_calendario import momento, fecha_ar, MESES, TITULO, RIAD  # noqa: E402  (las mismas fechas y horas que el vídeo)
import make_calendario
CANAL = "https://www.youtube.com/channel/UCRU3n034y5dJBEGnhAKjhfQ"
AVISO = "محتوى إعلامي، وليس توصية استثمارية."
TAGS_X = "#وول_ستريت #نتائج_الشركات"


def largo_x(t):  # como scripts/buffer.py: en X el árabe cuenta doble y un enlace 23
    import re
    t2 = re.sub(r"https?://\S+", "x" * 23, t)
    return sum(2 if ord(c) > 0x10FF else 1 for c in t2)


def main():
    P = os.path.abspath(sys.argv[1]); B = os.path.dirname(P); S = json.load(open(P)); base = S["base"]
    make_calendario.S = S
    EM = [e for e in S["escenas"] if e["tipo"] == "empresa"]
    sem = make_calendario.semana_txt()
    nombres = [e["nombre"] for e in EM]
    lista_n = "، ".join(nombres[:-1]) + " و" + nombres[-1] if len(nombres) > 1 else nombres[0]

    def linea(e, corta=False):
        dia, riad = momento(e)
        s = f"• {e['nombre']} ({e['ticker']}): {dia}"
        if riad and not corta: s += (f" (بتوقيت الرياض: {riad})" if e.get("fecha_et") else f" ({riad})")
        exp = []
        if e.get("bpa") is not None: exp.append(f"ربحية السهم المتوقعة {e['bpa']:.2f}$")
        if e.get("ingresos_mm") and not corta: exp.append(f"الإيرادات المتوقعة {e['ingresos_mm'] / 1000:.1f} مليار$")
        return s + (" · " + " · ".join(exp) if exp else "")

    if S["modo"] == "semana":
        cab = f"📅 {TITULO} ({sem}): يعلن نتائجه {EM[0]['nombre']}" + (f" و{len(EM) - 1} من قائمتنا" if len(EM) > 1 else "") + "."
        titulo = f"{TITULO}: {lista_n} · {sem}"
    else:
        cab = f"📅 {TITULO} ({sem}): لا نتائج من قائمتنا هذا الأسبوع. المواعيد القادمة بالترتيب الزمني:"
        titulo = f"{TITULO}: لا نتائج هذا الأسبوع، والقادم {lista_n}"
    if len(titulo) > 88: titulo = f"{TITULO} · {sem}: {EM[0]['nombre']} وأسهم أخرى"
    titulo += " #Shorts"
    assert len(titulo) <= 100, titulo
    cuerpo = "\n".join(linea(e) for e in EM)
    hecho = f"أعدّته نبض وول ستريت يوم {fecha_ar(dt.datetime.now(RIAD).date(), True, True)}. المواعيد والتوقعات قد تتغير."
    fuentes = S["fuentes"].replace("\n", " ")
    desc = (f"{cab}\n\n{cuerpo}\n\nالتوقعات = متوسط تقديرات المحللين. «بعد الإغلاق» = بعد الساعة 16:00 بتوقيت نيويورك."
            f"\n{fuentes}\n{hecho}\n{AVISO}\nتابع القناة لتحليل كل تقرير: {CANAL}\n#Shorts #وول_ستريت #نتائج_الشركات #الأسهم_الأمريكية")
    meta = {"title": titulo, "description": desc[:4900],
            "tags": ["تقويم النتائج", "نتائج الشركات", "وول ستريت", "الأسهم الأمريكية"] + [e["nombre"] for e in EM] + [e["ticker"] for e in EM] + ["Shorts"],
            "privacy": "public", "language": "ar", "categoryId": "27"}
    out = lambda n, t: open(os.path.join(B, f"{n}-{base}-Nabd.{'json' if n.startswith('meta') else 'txt'}"), "w", encoding="utf-8").write(t)
    out("meta-short", json.dumps(meta, ensure_ascii=False, indent=1))
    largo = f"{cab}\n\n{cuerpo}\n\n{AVISO}"
    # X: lo más corto (árabe cuenta doble); buffer.py añade el enlace al canal si cabe
    x = f"📅 {TITULO}\n" + ("لا نتائج من قائمتنا هذا الأسبوع. القادم: " if S["modo"] != "semana" else "هذا الأسبوع: ") + lista_n + f"\n▶️ {{youtube}}\n{AVISO}"
    if largo_x(x + "\n" + TAGS_X) <= 280: x += "\n" + TAGS_X
    assert largo_x(x) <= 280, (largo_x(x), x)
    out("post-x", x)
    out("post-telegram", f"{largo}\n\n▶️ الفيديو: {{youtube}}")
    out("post-tiktok", f"{cab}\n\n" + "\n".join(linea(e, True) for e in EM) + f"\n\n{AVISO}\nتابعنا لتحليل كل تقرير.\n#وول_ستريت #نتائج_الشركات #الأسهم_الأمريكية #تداول")
    out("post-instagram", f"{largo}\n\nتابعنا لتحليل كل تقرير.\n#وول_ستريت #نتائج_الشركات #الأسهم_الأمريكية #استثمار")
    # Facebook y Threads: fuera hasta nuevo aviso (Daniel, 22-nov-2026); no se generan sus posts.
    out("post-linkedin", f"{largo}\n\n▶️ {{youtube}}\n#وول_ستريت #نتائج_الشركات")
    g = [f"# {TITULO} · {sem}\n", f"Modo: {S['modo']} · Base: {base}\n", "| Escena | Locución |", "|---|---|"]
    g += [f"| {e['tipo']}{' ' + e.get('ticker', '') if e['tipo'] == 'empresa' else ''} | {e['voz']} |" for e in S["escenas"]]
    g += ["", "## Datos", "", cuerpo, "", "## Fuentes", "", S["fuentes"]]
    open(os.path.join(B, f"guion-{base}-Nabd.md"), "w", encoding="utf-8").write("\n".join(g) + "\n")
    print(titulo, "| X:", largo_x(x))


if __name__ == "__main__":
    main()
