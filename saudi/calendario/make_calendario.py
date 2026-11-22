# Short vertical (1080x1920, 45-59 s) «تقويم النتائج الأسبوعي» de Saudi Arabia AI Stocks (Daniel, 22-nov-2026): las 5-7 empresas más
# relevantes que reportan en la semana, primero Tadawul (domingo a jueves) y luego las grandes de EE. UU. (lunes a viernes), en orden
# cronológico, con día, hora y consenso (BPA e ingresos). Sale cada sábado entre las 20:00 y las 21:00 de Riad.
# Escenas en semanas/<base>/short.json: gancho, tasi (empresas saudíes o aviso de que no hay), empresa (una por compañía), fin.
# Zonas seguras de Shorts: texto entre y=0.25 y 0.90, alineado a la derecha en x=0.86 (fuera de los botones). Subtítulos en árabe.
# Uso: AUD=<scratch> [VOZ_DIR=<wav de Azure>] python3 make_calendario.py <carpeta de la semana> [preview]
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "educativo"), os.path.join(HERE, "..", "diario")]
from comun_leccion import *
import campana

DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
SJ = json.load(open(f"{DIR}/short.json")); BASE = SJ["base"]; OUT = f"{DIR}/short-{BASE}-saudi.mp4"
W, H, FPS, MAXDUR, MINDUR = 1080, 1920, 30, 59.0, 40.0
TITULO = "تقويم النتائج الأسبوعي"
import datetime as dt
PUB = dt.date.fromisoformat(SJ["publicar"])  # la campaña se mira en la fecha de publicación (sábado), no en la del render
ESC = [dict(e) for e in SJ["escenas"]]; CTA = campana.activa(PUB)
if CTA: ESC[-1]["voz"] = campana.VOZ_CORTA + " " + ESC[-1]["voz"]
EMP = [e for e in ESC if e["tipo"] == "empresa"]
assert 1 <= len(EMP) <= 7, "entre 1 y 7 empresas"
PROHIBIDO = ("بيع السهم", "رخيص", "سعر مستهدف", "توصية بالشراء")
for e in ESC:
    assert not any(p in e["voz"] for p in PROHIBIDO), f"palabra no permitida en {e['id']}"
XR = 0.86; LG = load_logo(150)


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def caja(f, x0, y0, w, h, c=PANEL, ec=DIM, alpha=1.0):
    from matplotlib.patches import FancyBboxPatch
    f.patches.append(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.006,rounding_size=0.018", transform=f.transFigure,
                                    fc=c, ec=ec, lw=2, alpha=alpha, figure=f))


def top(f, n):
    T(f, XR, 0.875, TITULO, GOLD, 30, "bold")
    tot = len(EMP); w = min(0.1, 0.72 / tot)
    for i in range(tot):
        f.patches.append(plt.Rectangle((XR - (i + 1) * w + 0.012, 0.858), w - 0.012, 0.006, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))


def s_gancho(e, t):
    f = fig(W, H); a = ease(t / 0.4)
    f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.12, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, XR, 0.76, TITULO, BG, 70, "bold", va="center", alpha=a)
    T(f, XR, 0.655, SJ["semana"], FG, 42, "bold", alpha=ease((t - 0.1) / 0.4))
    T(f, XR, 0.575, f"هذا الأسبوع: {e['estrella']}", GOLD, 54, "bold", alpha=ease((t - 0.2) / 0.4))
    if e.get("otras"): T(f, XR, 0.525, e["otras"], FG, 42, "bold", alpha=ease((t - 0.25) / 0.4))
    y = 0.47
    for k, nm in enumerate(e.get("lista", [])):
        T(f, XR, y - k * 0.03, "• " + nm, MUTED, 30, "bold", alpha=ease((t - 0.3 - k * 0.05) / 0.3))
    return with_logo(to_arr(f), LG, x=80, y=150)


def s_tasi(e, t):
    f = fig(W, H); top(f, 0); a = ease(t / 0.4)
    T(f, XR, 0.80, "السوق السعودية (تداول)", GOLD, 52, "bold", alpha=a)
    T(f, XR, 0.755, "من الأحد إلى الخميس", MUTED, 32, "bold", alpha=a)
    caja(f, 0.10, 0.36, 0.80, 0.36, alpha=a)
    y = 0.67
    for k, l in enumerate(e["lineas"]):
        fs = 40 if k == 0 else 34
        for r in textwrap.wrap(l, 28):  # una línea por llamada: el salto de línea de matplotlib no es fiable con árabe
            T(f, XR - 0.02, y, r, FG if k == 0 else MUTED, fs, "bold", va="top", alpha=ease((t - 0.15 - k * 0.12) / 0.4)); y -= fs * 1.75 / H
        y -= 0.03
    return with_logo(to_arr(f), LG, x=80, y=150)


def s_empresa(e, t):
    n = 1 + EMP.index(next(x for x in EMP if x["id"] == e["id"]))
    f = fig(W, H); top(f, n); a = ease(t / 0.35)
    T(f, XR, 0.805, e["dia"], GOLD, 50, "bold", alpha=a)
    T(f, XR, 0.765, e["hora"], MUTED, 32, "bold", alpha=a)
    T(f, XR, 0.675, e["nombre"], FG, 78 if len(e["nombre"]) <= 12 else 62, "bold", va="center", alpha=ease((t - 0.1) / 0.35))
    T(f, XR, 0.615, f"{e['latino']}  ·  {e['ticker']}", BLUE, 38, "bold", va="center", alpha=ease((t - 0.15) / 0.35))
    cajas = [(k, v) for k, v in (("ربحية السهم المتوقعة", e.get("eps") and f"{e['eps']} دولار"),
                                 ("الإيرادات المتوقعة", e.get("ingresos") and f"{e['ingresos']} دولار")) if v]
    nb = len(cajas); gap = 0.03; bw = (0.80 - gap * (nb - 1)) / nb
    for i, (k, v) in enumerate(cajas):
        b = ease((t - 0.25 - i * 0.1) / 0.35); x1 = 0.90 - i * (bw + gap)
        caja(f, x1 - bw, 0.40, bw, 0.15, alpha=b)
        T(f, x1 - bw / 2, 0.515, k, MUTED, 30, "bold", ha="center", va="center", alpha=b)
        T(f, x1 - bw / 2, 0.45, v, TEAL, 44 if nb == 2 else 60, "bold", ha="center", va="center", alpha=b)
    T(f, XR, 0.365, "متوسط توقعات المحللين · الربحية المعدّلة · الربع المالي الأخير", MUTED, 22, alpha=a)
    return with_logo(to_arr(f), LG, x=80, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.4)
    T(f, XR, 0.80, "تابع القناة لتحليل كل تقرير", GOLD, 46, "bold", alpha=a)
    T(f, XR, 0.74, "Saudi Arabia AI Stocks", FG, 54, "bold", alpha=a)
    T(f, XR, 0.69, f"{TITULO} · كل سبت مساءً", MUTED, 32, "bold", alpha=a)
    caja(f, 0.10, 0.56, 0.80, 0.095, alpha=ease((t - 0.15) / 0.4))
    T(f, XR - 0.02, 0.627, "لأخبار وول ستريت بالعربية:", FG, 34, "bold", va="center", alpha=ease((t - 0.2) / 0.4))
    T(f, XR - 0.02, 0.585, "قناة نبض وول ستريت  @NabdWallStreet", BLUE, 34, "bold", va="center", alpha=ease((t - 0.25) / 0.4))
    y = 0.53
    if CTA:
        T(f, XR, y, campana.CORTA1, BLUE, 28, "bold", alpha=a); T(f, XR, y - 0.03, campana.CORTA2, BLUE, 28, "bold", alpha=a); y -= 0.07
    T(f, XR, y, "محتوى إعلامي وليس توصية استثمارية. التوقعات من متوسط تقديرات المحللين، وقد تتغير المواعيد. صُنع بأدوات الذكاء الاصطناعي.",
      MUTED, 22, alpha=a, ancho=48, linespacing=1.4, va="top")
    return with_logo(to_arr(f), LG, x=80, y=150)


TIPOS = {"gancho": s_gancho, "tasi": s_tasi, "empresa": s_empresa, "fin": s_fin}
SUB = {}


def overlay(marcas, leads):
    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 40, 70, "bold") for l in (partir(sub_pantalla(s), 34) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = 70; h = lh * len(ls); y0 = int(H * 0.68) + 10; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr = fr.copy()
                fr[y0 - 10:y0 + h + 8, x0:x0 + wmax + 48] = (fr[y0 - 10:y0 + h + 8, x0:x0 + wmax + 48].astype(np.float32) * 0.25 + np.array([6, 25, 26], np.float32) * 0.75).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * lh)
                break
        return fr
    return ov


if __name__ == "__main__":
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(TIPOS[e["tipo"]](e, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"cal_{j:02d}_{e['id']}.png"))
        print("palabras", sum(len(e["voz"].split()) for e in ESC)); sys.exit()
    VV = [voz_frases(e["voz"], AUD, gap=0.15) for e in ESC]; sr = VV[0][1]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [0.1 + len(a) / sr + 0.4 for a, _, _, _ in VV]; durs[-1] += 1.2
    tot = sum(durs); print("duración", round(tot, 1), "s", [round(d, 1) for d in durs])
    if tot > MAXDUR: sys.exit(f"Short de {tot:.1f} s: acorta la locución (máx. {MAXDUR} s)")
    if tot < MINDUR: print(f"aviso: Short de {tot:.1f} s, por debajo de {MINDUR} s")
    leads = [0.1] * len(ESC)
    times, t0 = render([lambda t, e=e: TIPOS[e["tipo"]](e, t) for e in ESC], durs, ([v[0] for v in VV], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "cal-silent.mp4"), os.path.join(AUD, "cal.wav"), overlay=overlay([v[2] for v in VV], leads))
    json.dump({"_total": round(t0, 2), **{e["id"]: t for e, t in zip(ESC, times)}}, open(f"{DIR}/times.json", "w"))
    print("listo calendario", round(t0, 1), "s | voz:", VV[0][3], OUT)
