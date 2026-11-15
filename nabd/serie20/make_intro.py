# Vídeo de presentación (1920x1080) y Short (1080x1920) de la serie «عمالقة وول ستريت» de Nabd Wall Street: análisis de los estados financieros
# y resultados de 20 de las mayores empresas de EE. UU. (pedido de Daniel, 13-nov-2026). Reutiliza nabd/diario/comun.py (marca, árabe, render, voz).
# Voz: Azure ar-SA-HamedNeural si VOZ_DIR tiene sus wav (voz-Nabd.yml con fecha=nabd/serie20/intro); si no, Piper.
# Uso: AUD=<scratch> [VOZ_DIR=<wav>] python3 make_intro.py <carpeta con video.json> [preview]
# Escribe intro-serie-20-acciones-Nabd.mp4, short-serie-20-acciones-Nabd.mp4 y times.json (capítulos para meta_intro.py).
import os, sys, json, textwrap, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); E = VJ["empresas"]; SERIE = VJ["serie"]; V = VJ["voz"]
TOTAL = sum(e["cap"] for e in E) / 1000   # billones (trillion) de dólares, محسوب
FUENTE = f"القيمة السوقية: {VJ['datos']['fuente']}، إغلاق 12 نوفمبر 2026 في نيويورك (بالمليار دولار). المجموع محسوب."
NAVY = "#13294B"


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=c, alpha=a, figure=f))


# ---------------- Vídeo largo 1920x1080 ----------------
W, H = 1920, 1080
LG = load_logo(130); LGB = load_logo(230)
SECS = ["المقدمة", "لماذا هذه الشركات", "القائمة", "القائمة", "ماذا سنحلل", "مصادر الأرقام", "مواعيد الحلقات", "الختام"]


def base(n, kicker, title):
    f = fig(W, H)
    T(f, 0.94, 0.905, kicker, GOLD, 24, "bold")
    T(f, 0.94, 0.82, title, FG, 42, "bold")
    T(f, 0.105, 0.925, f"سلسلة {SERIE}", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.89, MARCA + " · " + MARCA_EN, DIM, 16, "bold", ha="left")
    w = 0.88 / 8
    for i in range(8):
        rect(f, 0.94 - (i + 1) * w + 0.008, 0.975, w - 0.008, 0.008, GOLD if i < n else DIM)
    return f


def s_portada(t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, 0.94, 0.88, MARCA + " · سلسلة جديدة", GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.67, 1.0, 0.16, GOLD, a)
    T(f, 0.94, 0.75, SERIE, BG, 84, "bold", va="center", alpha=a)
    T(f, 0.94, 0.57, "القوائم المالية ونتائج 20 من أكبر الشركات الأمريكية", FG, 40, "bold", alpha=ease((t - 0.15) / 0.5))
    T(f, 0.94, 0.505, "حلقة لكل شركة بعد إعلان نتائجها · 4 دقائق كحد أقصى · بالأرقام الرسمية", MUTED, 26, alpha=ease((t - 0.25) / 0.5))
    for i, e in enumerate(E):  # mosaico de los 20 tickers
        b = ease((t - 0.2 - i * 0.025) / 0.4); r, c = divmod(i, 10)
        x = 0.94 - (c + 1) * 0.0885; y = 0.30 - r * 0.115
        rect(f, x + 0.004, y, 0.08, 0.085, NAVY, b)
        f.text(x + 0.044, y + 0.0425, e["ticker"], color=GOLD, fontsize=24, weight="bold", ha="center", va="center", alpha=b)
    return with_logo(to_arr(f), LGB, x=110, y=40)


def s_porque(t):
    f = base(2, "لماذا هذه الشركات؟", "وزن هائل في وول ستريت"); a = ease(t / 0.5)
    T(f, 0.94, 0.66, "القيمة السوقية للشركات العشرين مجتمعةً (محسوب)", MUTED, 26, "bold", alpha=a)
    f.text(0.94, 0.50, f"{TOTAL:.1f}", color=GOLD, fontsize=120, weight="bold", ha="right", alpha=a)
    T(f, 0.94, 0.43, "تريليون دولار", FG, 40, "bold", alpha=a)
    T(f, 0.94, 0.33, f"أكبرها آبل: {E[0]['cap'] / 1000:.2f} تريليون\nأصغرها في القائمة نتفليكس: {E[-1]['cap']:.0f} مليار", FG, 26, linespacing=1.6, alpha=ease((t - 0.3) / 0.5), va="top")
    ax = f.add_axes([0.07, 0.20, 0.42, 0.60]); clean(ax); ee = ease(t)
    y = np.arange(len(E))[::-1]; v = [e["cap"] for e in E]
    ax.barh(y, [x * ee for x in v], color=[GOLD if i < 5 else BLUE for i in range(len(E))], height=0.62)
    ax.set_yticks(y, [e["ticker"] for e in E]); ax.tick_params(colors=FG, labelsize=15); ax.set_xticks([]); ax.set_xlim(0, max(v) * 1.25)
    if t > 0.6:
        for yy, x in zip(y, v): ax.text(x * ee + max(v) * 0.015, yy, f"{x:,.0f}", va="center", color=MUTED, fontsize=13, weight="bold")
    T(f, 0.49, 0.815, "القيمة السوقية (مليار دولار)", MUTED, 18, alpha=a)
    T(f, 0.94, 0.17, FUENTE, MUTED, 15)
    return with_logo(to_arr(f), LG, x=60, y=40)


def s_lista(k, t):
    P = E[k * 10:(k + 1) * 10]
    f = base(3 + k, f"القائمة ({k * 10 + 1}-{k * 10 + 10})", "الشركات العشرون مرتبة حسب القيمة السوقية")
    for i, e in enumerate(P):
        b = ease((t - i * 0.06) / 0.4); c, r = divmod(i, 5)
        x0 = 0.505 - c * 0.45; y = 0.66 - r * 0.115
        rect(f, x0, y, 0.435, 0.095, NAVY, b); rect(f, x0 + 0.43, y, 0.005, 0.095, GOLD, b)
        f.text(x0 + 0.41, y + 0.047, f"{k * 10 + i + 1}", color=GOLD, fontsize=34, weight="bold", ha="center", va="center", alpha=b)
        T(f, x0 + 0.385, y + 0.055, e["ar"], FG, 28, "bold", va="center", alpha=b)
        T(f, x0 + 0.385, y + 0.018, e["sector"], MUTED, 18, va="center", alpha=b)
        f.text(x0 + 0.015, y + 0.058, e["ticker"], color=GOLD, fontsize=24, weight="bold", ha="left", va="center", alpha=b)
        T(f, x0 + 0.015, y + 0.02, f"{e['cap']:,.0f} مليار $", FG, 18, ha="left", va="center", alpha=b)
    T(f, 0.94, 0.17, FUENTE, MUTED, 15)
    return with_logo(to_arr(f), LG, x=60, y=40)


def tarjetas(f, items, t, y0=0.68, h=0.095, step=0.112, fs=28):
    for i, (tit, txt) in enumerate(items):
        b = ease((t - i * 0.1) / 0.4); y = y0 - i * step
        rect(f, 0.06, y, 0.88, h, NAVY, b); rect(f, 0.935, y, 0.005, h, GOLD, b)
        f.text(0.905, y + h / 2, str(i + 1), color=GOLD, fontsize=36, weight="bold", ha="center", va="center", alpha=b)
        T(f, 0.875, y + h / 2, tit, FG, fs, "bold", va="center", alpha=b)
        T(f, 0.62, y + h / 2, txt, MUTED, 21, va="center", alpha=b)


def s_que(t):
    f = base(5, "ماذا سنحلل في كل حلقة؟", "خمسة محاور ثابتة لكل شركة")
    tarjetas(f, [("قائمة الدخل", "الإيرادات ونموها، هوامش الربح، ربحية السهم"),
                 ("الميزانية العمومية", "النقد، الديون، حقوق المساهمين"),
                 ("التدفقات النقدية", "التدفق النقدي الحر، الإنفاق الرأسمالي، التوزيعات وإعادة شراء الأسهم"),
                 ("آخر نتائج فصلية", "مقارنة بتوقعات المحللين، وتوجيهات الإدارة للفترة المقبلة"),
                 ("الديون والنقد", "نسبتهما إلى القيمة السوقية، من المؤشرات التي يتابعها مستثمرو الخليج")], t)
    return with_logo(to_arr(f), LG, x=60, y=40)


def s_como(t):
    f = base(6, "من أين تأتي الأرقام؟", "مصادر رسمية وقواعد واضحة")
    tarjetas(f, [("هيئة الأوراق المالية (SEC)", "التقارير السنوية والفصلية: نماذج 10-K و 10-Q"),
                 ("بيانات النتائج", "ما تنشره الشركات عند إعلان نتائجها، ومكالماتها مع المحللين"),
                 ("«محسوب»", "كل حساب نقوم به نحن نوضحه بهذه الكلمة، مع مصدر كل رقم"),
                 ("حقائق وآراء", "نفصل دائمًا بين ما تقوله الأرقام وما نستنتجه منها"),
                 ("بلا توصيات", "لا شراء ولا بيع ولا أسعار مستهدفة: القرار لك")], t)
    return with_logo(to_arr(f), LG, x=60, y=40)


def s_formato(t):
    f = base(7, "كيف ستسير السلسلة؟", "حلقة لكل شركة بعد إعلان نتائجها")
    tarjetas(f, [("بعد كل إعلان نتائج", "حلقة عن الشركة لا تزيد على 4 دقائق: النتائج الجديدة والقوائم المالية"),
                 ("من موسم النتائج الحالي", "نتابع مواعيد إعلان النتائج للشركات العشرين"),
                 ("إذا تزامنت النتائج", "نوزع الحلقات على الأيام التالية"),
                 ("التقرير اليومي مستمر", "بعد إغلاق كل جلسة في وول ستريت كالمعتاد")], t, y0=0.64, h=0.105, step=0.13)
    T(f, 0.94, 0.12, "الحلقة الأولى قريبًا على القناة", GOLD, 34, "bold", alpha=ease((t - 0.4) / 0.5))
    return with_logo(to_arr(f), LG, x=60, y=40)


def s_fin(t):
    f = fig(W, H); a = ease(t / 0.5); b = ease((t - 0.25) / 0.5)
    T(f, 0.94, 0.85, MARCA + " · سلسلة " + SERIE, FG, 46, "bold", alpha=a)
    T(f, 0.94, 0.765, "اكتب لنا في التعليقات: أي شركة تنتظر نتائجها أكثر؟", GOLD, 32, "bold", alpha=a)
    T(f, 0.94, 0.705, "واشترك في القناة وفعّل الجرس حتى لا تفوتك أي حلقة", FG, 28, alpha=a)
    rect(f, 0.30, 0.47, 0.64, 0.19, BLUE, 0.14 * b); rect(f, 0.935, 0.47, 0.005, 0.19, BLUE, b)
    T(f, 0.92, 0.615, "انضموا مجانًا إلى قناتنا على تيليغرام", FG, 34, "bold", alpha=b)
    T(f, 0.92, 0.565, "تحليلات السوق الأمريكية · الرابط في وصف الفيديو", MUTED, 22, alpha=b)
    f.text(0.92, 0.495, TELEGRAM.replace("https://", ""), color=BLUE, fontsize=34, ha="right", weight="bold", alpha=b)
    f.text(0.94, 0.41, CANAL.replace("https://www.", ""), color=MUTED, fontsize=22, ha="right", weight="bold", alpha=a)
    aviso = ("إخلاء مسؤولية: محتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية أو دعوة لشراء أو بيع أي ورقة مالية أو استشارة مالية شخصية. "
             "استشر جهة مرخصة في بلدك قبل أي قرار استثماري. القيمة السوقية من TradingView (إغلاق 12 نوفمبر 2026)، والمجموع محسوب. "
             "لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر، والأداء السابق لا يضمن النتائج. "
             "النص والرسوم والصوت (صوت اصطناعي) من إعداد الذكاء الاصطناعي.")
    T(f, 0.94, 0.20, "\n".join(textwrap.wrap(aviso, 135)), MUTED, 15, linespacing=1.5, alpha=a)
    return with_logo(to_arr(f), LGB, x=110, y=70)


ESC = [("s_portada", s_portada), ("s_porque", s_porque), ("s_lista_1", lambda t: s_lista(0, t)), ("s_lista_2", lambda t: s_lista(1, t)),
       ("s_que", s_que), ("s_como", s_como), ("s_formato", s_formato), ("s_fin", s_fin)]
CAPS = {"s_portada": "المقدمة", "s_porque": "لماذا هذه الشركات", "s_lista_1": "القائمة", "s_que": "ماذا سنحلل في كل حلقة",
        "s_como": "مصادر الأرقام", "s_formato": "كيف ستسير السلسلة", "s_fin": "الختام"}

SUB_CACHE = {}


def overlay(marcas, leads, W_, H_, ancho=72, fs=27, banda=True):
    pie = tira_texto(f"{MARCA} · سلسلة {SERIE} · {MARCA_EN}", GOLD, 18, 46)
    band = np.array([0x13, 0x29, 0x4B], np.float32)

    def sub(s):
        if s not in SUB_CACHE: SUB_CACHE[s] = [tira_texto(l, FG, fs, int(fs * 1.85), "bold") for l in (textwrap.wrap(s, ancho) or [s])]
        return SUB_CACHE[s]

    def ov(fr, j, ts, tg):
        if not banda: return fr  # Short: sin subtítulos (la franja inferior queda bajo el título y el canal de YouTube)
        fr = fr.copy(); bh = 46 if banda else 0
        if banda:
            fr[H_ - bh:] = (fr[H_ - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H_ - bh - 2:H_ - bh] = (0xD4, 0xAF, 0x37)
            pegar(fr, pie, (W_ - pie.shape[1]) // 2, H_ - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = ls[0].shape[0]; h = lh * len(ls); y0 = (H_ - bh - 16 - h) if banda else int(H_ * 0.80)
                wmax = max(l.shape[1] for l in ls); x0 = max((W_ - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array([11, 26, 46], np.float32) * 0.72).astype(np.uint8)
                for i, l in enumerate(ls): pegar(fr, l, (W_ - l.shape[1]) // 2, y0 + i * lh)
                break
        return fr
    return ov


# ---------------- Short 1080x1920 ----------------
SW, SH = 1080, 1920; XR = 0.86
LGs = load_logo(150); LGsB = load_logo(260)


def sh_1(t):
    f = fig(SW, SH); a = ease(t / 0.5)
    T(f, XR, 0.80, MARCA + " · سلسلة جديدة", GOLD, 38, "bold", alpha=a)
    rect(f, 0, 0.655, 1.0, 0.125, GOLD, a)
    T(f, XR, 0.717, SERIE, BG, 68, "bold", va="center", alpha=a)
    T(f, XR, 0.58, "القوائم المالية ونتائج\n20 من أكبر الشركات الأمريكية", FG, 46, "bold", va="top", linespacing=1.4, alpha=ease((t - 0.2) / 0.5))
    return with_logo(to_arr(f), LGs, x=90, y=150)


def sh_2(t):
    f = fig(SW, SH); T(f, XR, 0.80, "الشركات العشرون", GOLD, 44, "bold", alpha=ease(t / 0.4))
    for i, e in enumerate(E):
        b = ease((t - i * 0.03) / 0.4); c, r = divmod(i, 10); x = XR - c * 0.38; y = 0.735 - r * 0.048
        T(f, x, y, f"{i + 1}  {e['ar']}", FG, 30, "bold", alpha=b)
    T(f, XR, 0.235, "مرتبة حسب القيمة السوقية · إغلاق 12 نوفمبر 2026", MUTED, 26, alpha=ease((t - 0.4) / 0.4))
    return with_logo(to_arr(f), LGs, x=90, y=150)


def sh_3(t):
    f = fig(SW, SH); a = ease(t / 0.4)
    T(f, XR, 0.72, "القيمة السوقية مجتمعةً (محسوب)", MUTED, 40, "bold", alpha=a)
    f.text(XR, 0.58, f"{TOTAL:.1f}", color=GOLD, fontsize=190, weight="bold", ha="right", alpha=a)
    T(f, XR, 0.52, "تريليون دولار", FG, 56, "bold", alpha=a)
    T(f, XR, 0.42, f"آبل وحدها {E[0]['cap'] / 1000:.2f} تريليون\nإنفيديا {E[1]['cap'] / 1000:.2f} · مايكروسوفت {E[2]['cap'] / 1000:.2f}", FG, 36, va="top", linespacing=1.5, alpha=ease((t - 0.3) / 0.4))
    T(f, XR, 0.28, "المصدر: TradingView، إغلاق 12 نوفمبر 2026", MUTED, 26, alpha=a)
    return with_logo(to_arr(f), LGs, x=90, y=150)


def sh_4(t):
    f = fig(SW, SH); T(f, XR, 0.78, "بعد كل إعلان نتائج", GOLD, 50, "bold", alpha=ease(t / 0.4))
    for i, s in enumerate(["الإيرادات والأرباح", "الديون والنقد", "التدفق النقدي الحر", "النتائج مقابل التوقعات"]):
        b = ease((t - 0.1 - i * 0.12) / 0.4); y = 0.67 - i * 0.09
        rect(f, 0.12, y - 0.025, 0.76, 0.07, NAVY, b); T(f, XR - 0.03, y + 0.01, s, FG, 44, "bold", va="center", alpha=b)
    T(f, XR, 0.29, "بالأرقام الرسمية (SEC) · بلا توصيات", MUTED, 34, "bold", alpha=ease((t - 0.5) / 0.4))
    return with_logo(to_arr(f), LGs, x=90, y=150)


def sh_5(t):
    f = fig(SW, SH); a = ease(t / 0.5)
    T(f, XR, 0.66, "أي شركة تنتظر نتائجها أكثر؟", GOLD, 46, "bold", alpha=a)
    T(f, XR, 0.615, "اكتب لنا في التعليقات", FG, 40, "bold", alpha=a)
    T(f, XR, 0.53, "◀ اشترك حتى لا تفوتك أي حلقة", FG, 42, "bold", alpha=ease((t - 0.2) / 0.5))
    T(f, XR, 0.485, MARCA_EN + " · " + MARCA, BLUE, 31, "bold", alpha=a)
    T(f, XR, 0.45, "محتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية.\nلا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\nالنص والصوت والرسوم من إعداد الذكاء الاصطناعي.", MUTED, 24, linespacing=1.5, va="top", alpha=a)
    return with_logo(to_arr(f), LGsB, x=(SW - 260) // 2, y=150)


SESC = [("sh_1", sh_1), ("sh_2", sh_2), ("sh_3", sh_3), ("sh_4", sh_4), ("sh_5", sh_5)]


def hacer(escenas, W_, H_, out, nombre, ancho, fs, banda, big, lg, lead=0.15, tail=0.6, maxdur=None, mins=None):
    frame = lambda n, fn, t: fn(t) if n in big else with_logo(fn(t), lg, x=60, y=48) if lg else fn(t)
    if PREVIEW:
        ov = overlay([[(0, 99, frases(V[n])[0])] for n, _ in escenas], [0] * len(escenas), W_, H_, ancho, fs, banda)
        for j, (n, fn) in enumerate(escenas): Image.fromarray(ov(frame(n, fn, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"prev_{n}.png"))
        return None
    VV = [voz_frases(V[n], AUD) for n, _ in escenas]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [lead + len(a) / sr + tail for a, _, _, _ in VV]; durs[-1] += 1.5
    print(nombre, "voz", motor, "duración prevista", round(sum(durs), 1))
    if maxdur and sum(durs) > maxdur: sys.exit(f"{nombre}: {sum(durs):.1f} s > {maxdur}")
    leads = [lead] * len(escenas)
    times, t0 = render([lambda t, n=n, fn=fn: frame(n, fn, t) for n, fn in escenas], durs, ([v[0] for v in VV], leads), sr, W_, H_, 30, out,
                       os.path.join(AUD, nombre + "-silent.mp4"), os.path.join(AUD, nombre + ".wav"), loud=-16 if banda else -14,
                       overlay=overlay([v[2] for v in VV], leads, W_, H_, ancho, fs, banda))
    return [(n, tt) for (n, _), tt in zip(escenas, times)] + [("_total", round(t0, 2)), ("_voz", motor)]


if __name__ == "__main__":
    which = os.environ.get("SOLO", "ambos")
    if which in ("ambos", "video"):
        r = hacer(ESC, W, H, f"{DIR}/intro-serie-20-acciones-Nabd.mp4", "intro", 72, 27, True, {"s_portada", "s_fin"}, None, maxdur=240.0)
        if r: json.dump(r, open(f"{DIR}/times.json", "w"))
    if which in ("ambos", "short"):
        r = hacer(SESC, SW, SH, f"{DIR}/short-serie-20-acciones-Nabd.mp4", "short", 30, 40, False, set(), None, lead=0.1, tail=0.35, maxdur=59.0)
        if r: json.dump(r, open(f"{DIR}/times-short.json", "w"))
    print("listo")
