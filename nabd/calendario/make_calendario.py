# Short vertical (1080x1920, 45-60 s) «تقويم النتائج الأسبوعي للأسهم الأمريكية» de Nabd Wall Street: qué acciones de la lista del canal
# (las 22 de nabd/serie20/plan.py) presentan resultados la semana que viene, con día, momento (antes de la apertura / tras el cierre),
# hora de Riad y consenso de BPA e ingresos. Si esa semana no reporta ninguna (o pocas), modo "proximos": las siguientes en orden cronológico.
# Uso: AUD=<scratch> [VOZ_DIR=<voz Azure>] python3 make_calendario.py <carpeta>/video.json [preview]
# Escribe en la carpeta: <base>-Nabd.mp4 (el Short) y miniatura-<base>-Nabd.png (portada, para Telegram).
# Voz: Azure ar-SA-HamedNeural (wav por frase de voz-Nabd.yml con fecha=nabd/calendario/semanas/<base>, VOZ_DIR=<clon voz-nabd>/<base>);
# sin VOZ_DIR, Piper (comun.voz_frases). Zonas seguras de Shorts: el texto va entre y=0.22 y 0.86, alineado a la derecha en x=0.86.
import os, sys, json, datetime as dt
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *  # noqa: F401,F403
W, H, FPS = 1080, 1920, 30
AUD = os.environ.get("AUD", "aud"); MINDUR, MAXDUR = 44.0, 59.5
XR = 0.86
NY, RIAD = ZoneInfo("America/New_York"), ZoneInfo("Asia/Riyadh")
DIAS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
TITULO = "تقويم النتائج الأسبوعي"
LG = load_logo(150); LGB = load_logo(260)


def fecha_ar(d, con_dia=True, con_ano=False):
    s = f"{d.day} {MESES[d.month - 1]}" + (f" {d.year}" if con_ano else "")
    return f"{DIAS[d.weekday()]} {s}" if con_dia else s


def momento(e):
    """(texto del día en Nueva York, texto de la hora de Riad) de una empresa. Sin hora_et: apertura 9:30 o cierre 16:00 (hora de NY)."""
    if not e.get("fecha_et"):
        return e["fecha_texto"], e.get("nota_fecha", "")
    d = dt.date.fromisoformat(e["fecha_et"]); antes = e.get("momento") == "antes"
    h = e.get("hora_et") or ("09:30" if antes else "16:00")
    t = dt.datetime.combine(d, dt.time.fromisoformat(h), NY).astimezone(RIAD)
    cuando = "قبل الافتتاح" if antes else "بعد الإغلاق"
    hr = t.strftime("%H:%M")
    if e.get("hora_et"):
        riad = f"{fecha_ar(t.date())}، الساعة {hr}"
    elif antes:
        riad = f"{fecha_ar(t.date())}، قبل {hr}"
    else:
        riad = f"فجر {fecha_ar(t.date())}، بعد {hr}" if t.hour < 6 else f"{fecha_ar(t.date())}، بعد {hr}"
    return f"{fecha_ar(d)} · {cuando}", riad


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def top(f, n):
    T(f, XR, 0.835, f"{TITULO} · {MARCA}", GOLD, 30, "bold")
    tot = sum(1 for x in S["escenas"] if x["tipo"] == "empresa")
    for i in range(tot):
        f.patches.append(plt.Rectangle((XR - (i + 1) * 0.075 + 0.015, 0.82), 0.06, 0.006, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))


def semana_txt():
    a, b = (dt.date.fromisoformat(x) for x in S["semana"])
    return f"{a.day} - {b.day} {MESES[b.month - 1]} {b.year}" if a.month == b.month else f"{fecha_ar(a, False)} - {fecha_ar(b, False, True)}"


def s_gancho(e, t):
    f = fig(W, H); a = ease(t / 0.5); EM = [x for x in S["escenas"] if x["tipo"] == "empresa"]
    T(f, XR, 0.80, TITULO, GOLD, 50, "bold", alpha=a)
    T(f, XR, 0.765, "للأسهم الأمريكية التي نتابعها", MUTED, 34, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.665), 1.0, 0.075, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, XR, 0.703, ("الأسبوع القادم · " if S["modo"] == "semana" else "أسبوع ") + semana_txt(), BG, 46, "bold", va="center", alpha=a)
    b = ease((t - 0.15) / 0.5)
    if S["modo"] == "semana":
        T(f, XR, 0.60, "يعلن نتائجه هذا الأسبوع", FG, 40, "bold", alpha=b)
        T(f, XR, 0.525, EM[0]["nombre"], GOLD, 96, "bold", alpha=b)
        if len(EM) > 1: T(f, XR, 0.47, f"و{len(EM) - 1} " + ("سهم آخر" if len(EM) == 2 else "أسهم أخرى") + " من قائمتنا", FG, 40, "bold", alpha=b)
        y0, lab = 0.40, "بالترتيب الزمني:"
    else:
        T(f, XR, 0.60, "لا نتائج من قائمتنا هذا الأسبوع", FG, 46, "bold", alpha=b)
        if S.get("nota_semana"): T(f, XR, 0.57, S["nota_semana"], MUTED, 28, alpha=b, va="top", linespacing=1.5, ancho=56)
        y0, lab = 0.49, "المواعيد القادمة بالترتيب الزمني:"
    T(f, XR, y0, lab, BLUE, 36, "bold", alpha=ease((t - 0.3) / 0.5))
    for i, x in enumerate(EM):
        c = ease((t - 0.35 - i * 0.12) / 0.5); y = y0 - 0.065 - i * (0.075 if len(EM) <= 4 else 0.055)
        dia = fecha_ar(dt.date.fromisoformat(x["fecha_et"])) if x.get("fecha_et") else x["fecha_texto"]
        T(f, XR, y, x["nombre"], FG, 42, "bold", alpha=c)
        f.text(0.10, y, x["ticker"], color=GOLD, fontsize=38, weight="bold", ha="left", alpha=c)
        if len(EM) <= 4: T(f, XR, y - 0.031, dia, MUTED, 30, "bold", alpha=c)
    return with_logo(to_arr(f), LG, x=90, y=150)


def kpi(f, x, lab, big, a):
    T(f, x, 0.40, lab, MUTED, 32, "bold", alpha=a)
    f.text(x, 0.325, big, color=FG, fontsize=92 if len(big) < 8 else 76, weight="bold", ha="right", alpha=a)


def s_empresa(e, t):
    f = fig(W, H); n = [x for x in S["escenas"] if x["tipo"] == "empresa"].index(e) + 1; tot = sum(1 for x in S["escenas"] if x["tipo"] == "empresa")
    top(f, n); a = ease(t / 0.4); b = ease((t - 0.15) / 0.4); c = ease((t - 0.3) / 0.4)
    T(f, XR, 0.765, f"{n}/{tot} · {e.get('periodo', '')}", MUTED, 32, "bold", alpha=a)
    T(f, XR, 0.69, e["nombre"], FG, 96, "bold", alpha=a)
    f.text(0.10, 0.695, e["ticker"], color=GOLD, fontsize=70, weight="bold", ha="left", alpha=a)
    dia, riad = momento(e)
    f.patches.append(plt.Rectangle((0, 0.585), 1.0, 0.065, transform=f.transFigure, color=GOLD, alpha=b, figure=f))
    T(f, XR, 0.618, dia, BG, 44, "bold", va="center", alpha=b)
    if riad:
        if e.get("fecha_et"): T(f, XR, 0.555, "بتوقيت الرياض:", MUTED, 28, "bold", alpha=b)
        T(f, XR, 0.515 if e.get("fecha_et") else 0.545, riad, BLUE, 38, "bold", alpha=b)
    T(f, XR, 0.475, "موعد أعلنته الشركة" if e.get("confirmada") else "موعد غير مؤكد", TEAL if e.get("confirmada") else MUTED, 28, "bold", alpha=b)
    T(f, XR, 0.44, "ما يتوقعه السوق (متوسط تقديرات المحللين):", GOLD, 30, "bold", alpha=c)
    k = []
    if e.get("bpa") is not None: k.append(("ربحية السهم", f"${e['bpa']:.2f}"))
    if e.get("ingresos_mm"): k.append(("الإيرادات", f"${e['ingresos_mm'] / 1000:.1f}B"))
    for i, (lab, big) in enumerate(k): kpi(f, XR - i * 0.42, lab, big, c)
    if e.get("ingresos_mm"): T(f, XR - 0.42, 0.285, "مليار دولار", MUTED, 28, alpha=c)
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_cierre(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, 0.5, 0.70, "تابع القناة لتحليل كل تقرير", GOLD, 54, "bold", ha="center", alpha=a)
    T(f, 0.5, 0.645, MARCA_EN + " · " + MARCA, BLUE, 34, "bold", ha="center", alpha=a)
    f.patches.append(plt.Rectangle((0.04, 0.545), 0.92, 0.065, transform=f.transFigure, color=DIM, alpha=a, figure=f))
    T(f, 0.5, 0.578, "محتوى إعلامي، وليس توصية استثمارية.", FG, 34, "bold", ha="center", va="center", alpha=a)
    T(f, XR, 0.50, S["fuentes"] + f"\nأُعدّ في {fecha_ar(dt.datetime.now(RIAD).date(), True, True)}. المواعيد والتوقعات قد تتغير.",
      MUTED, 24, linespacing=1.6, va="top", alpha=ease((t - 0.2) / 0.5), ancho=50)
    return with_logo(to_arr(f), LGB, x=(W - 260) // 2, y=150)


RX = {"gancho": s_gancho, "empresa": s_empresa, "cierre": s_cierre}
def frame(e, t): return RX[e["tipo"]](e, t)


if __name__ == "__main__":
    P = os.path.abspath(sys.argv[1]); B = os.path.dirname(P); S = json.load(open(P)); E = S["escenas"]; os.makedirs(AUD, exist_ok=True)
    EM = [x for x in E if x["tipo"] == "empresa"]
    assert S["modo"] in ("semana", "proximos") and E[0]["tipo"] == "gancho" and E[-1]["tipo"] == "cierre" and EM, "estructura: gancho, empresas, cierre"
    orden = [x.get("fecha_et") or "9999" for x in EM]; assert orden == sorted(orden), "las empresas van en orden cronológico"
    Image.fromarray(frame(E[0], 1.0)).save(os.path.join(B, f"miniatura-{S['base']}-Nabd.png"))
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"cal_prev_{i}.png"))
        sys.exit()
    clips = [voz_frases(e["voz"], AUD) for e in E]; sr = clips[0][1]; motores = {c[3] for c in clips}
    LEAD, TAIL = 0.15, 0.45
    durs = [LEAD + len(c[0]) / sr + TAIL for c in clips]; durs[-1] += 1.0
    print("voz", motores, "duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if not MINDUR <= sum(durs) <= MAXDUR: sys.exit(f"Short de {sum(durs):.1f} s: tiene que durar entre {MINDUR:.0f} y {MAXDUR:.0f} s. Ajusta la voz.")
    out = os.path.join(B, f"{S['base']}-Nabd.mp4")
    times, t0 = render([lambda t, e=e: frame(e, t) for e in E], durs, ([c[0] for c in clips], [LEAD] * len(E)), sr, W, H, FPS, out,
                       os.path.join(AUD, "cal-silent.mp4"), os.path.join(AUD, "cal-full.wav"), loud=-14, ANIM=24, XF=6)
    print("listo", out, round(t0, 1), "s", "voz", "/".join(sorted(motores)))
