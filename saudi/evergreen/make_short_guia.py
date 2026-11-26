# Short vertical (1080x1920, < 60 s) de un vídeo evergreen «دليل المستثمر في السوق السعودية» (Saudi Arabia AI Stocks), para YouTube Shorts,
# TikTok, Instagram (Reel) y LinkedIn (vídeo nativo, regla de Daniel del 8-nov-2026). Escenas en video.json → "short":
#   titulo (pregunta), tarjeta (titulo + lineas ≤5), historico (grafico: <id de la escena "historico" larga>), fin. Subtítulos en árabe.
# Zonas seguras de Shorts: texto entre y=0.25 y 0.90, alineado a la derecha en x=0.86.
# Uso: AUD=<scratch> [VELAS=<velas.json>] [VOZ_DIR=<wav de Azure>] python3 make_short_guia.py <carpeta de la guía> [preview]
import os, sys, json, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "educativo")); sys.path.insert(0, HERE)
from comun_leccion import *
import campana

SERIE = "دليل المستثمر في السوق السعودية"
DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json"))
VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json"))) if VJ.get("simbolo") else None
W, H, FPS, MAXDUR = 1080, 1920, 30, 59.0
BASE = VJ["base"]; OUT = f"{DIR}/short-{BASE}-saudi.mp4"; CTA = campana.activa()
ESC = [dict(e) for e in VJ["short"]]
if CTA: ESC[-1]["voz"] = campana.VOZ_CORTA + " " + ESC[-1]["voz"]
LARGAS = {e["id"]: e for e in VJ["escenas"]}
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
VELAS = [v for v in VEL["series"][VJ["simbolo"]]["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]] if VEL else []
XR = 0.86
LG = load_logo(150)


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def top(f):
    T(f, XR, 0.86, SERIE, GOLD, 30, "bold")


def s_titulo(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.80, SERIE, GOLD, 34, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.60), 1.0, 0.17, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, XR, 0.685, VJ["tema"], BG, 58 if len(VJ["tema"]) <= 24 else 50, "bold", va="center", alpha=a, ancho=22, linespacing=1.15)
    if e.get("pregunta"): T(f, XR, 0.52, e["pregunta"], BLUE, 52, "bold", alpha=ease((t - 0.2) / 0.5))
    T(f, XR, 0.42, "محتوى تعليمي وليس توصية استثمارية", MUTED, 30, "bold", alpha=ease((t - 0.4) / 0.5))
    return with_logo(to_arr(f), LG, x=80, y=170)


def s_tarjeta(e, t):
    f = fig(W, H); top(f); a = ease(t / 0.4)
    T(f, XR, 0.80, e["titulo"], FG, 48, "bold", alpha=a, ancho=28, va="top")
    for k, l in enumerate(e["lineas"][:5]):
        b = ease((t - 0.1 - k * 0.12) / 0.4); y = 0.66 - k * 0.075
        f.patches.append(plt.Rectangle((0.10, y - 0.028), 0.80, 0.062, transform=f.transFigure, color=PANEL, alpha=b, figure=f))
        f.patches.append(plt.Rectangle((XR + 0.035, y - 0.028), 0.005, 0.062, transform=f.transFigure, color=GOLD, alpha=b, figure=f))
        T(f, XR + 0.02, y, l, FG, 34, "bold", va="center", alpha=b, ancho=34)
    return with_logo(to_arr(f), LG, x=80, y=150)


def s_historico(e, t):
    g = LARGAS[e["grafico"]]; f = fig(W, H); top(f); a = ease(t / 0.4)
    T(f, XR, 0.83, e["titulo"], FG, 40, "bold", alpha=a, ancho=30, linespacing=1.05, va="top")
    T(f, XR, 0.705, g.get("leyenda", VJ["nombre"]), MUTED, 20, ancho=70, va="top")
    d0 = g.get("desde", "0000"); d1 = g.get("hasta", "9999")
    V = [v for v in VELAS if d0 <= fecha_v(v["t"]).isoformat() <= d1]
    S = {}
    for v in V: S[fecha_v(v["t"]).isocalendar()[:2]] = (fecha_v(v["t"]), v["c"])
    S = list(S.values()); ys = np.array([c for _, c in S]); n = len(S); xs = np.arange(n); rev = max(2, int(n * ease(t * 1.3)))
    ax = f.add_axes([0.10, 0.36, 0.80, 0.30]); clean(ax)
    ax.fill_between(xs[:rev], ys[:rev], ys.min() * 0.85, color=TEAL, alpha=0.12, lw=0); ax.plot(xs[:rev], ys[:rev], color=TEAL, lw=3)
    ax.set_ylim(ys.min() * 0.8, ys.max() * 1.25); ax.set_xlim(-n * 0.02, n * 1.03)
    pos = {d.isocalendar()[:2]: j for j, (d, _) in enumerate(S)}; byd = {fecha_v(v["t"]).isoformat(): v for v in V}
    for k, m in enumerate(g.get("marcas", [])[:2]):
        v = byd.get(m["fecha"]); b = ease((t - 0.5 - k * 0.12) / 0.3)
        if not v: continue
        j = pos[fecha_v(v["t"]).isocalendar()[:2]]
        if j > rev: continue
        ax.plot([j], [ys[j]], "o", color=GOLD, ms=14, alpha=b)
        ax.text(j + n * 0.03, ys[j] * (1.08 if m.get("campo") != "l" else 0.9), ar(m["texto"].split("\n")[-1]), color=GOLD, fontsize=28, weight="bold",
                ha="left", va="center", alpha=b, bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec="none", alpha=0.85 * b))
    ax.set_yticks(ax.get_yticks()[1:-1]); ax.set_yticklabels([num(y, 0) for y in ax.get_yticks()]); ax.tick_params(labelsize=20)
    ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk = [(j, str(d.year)) for j, (d, _) in enumerate(S) if j == 0 or d.year != S[j - 1][0].year]
    tk = [p for p in tk if int(p[1]) % 6 == 0]; ax.set_xticks([p[0] for p in tk], [p[1] for p in tk])
    return with_logo(to_arr(f), LG, x=80, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.80, "الدليل الكامل على يوتيوب", GOLD, 46, "bold", alpha=a)
    T(f, XR, 0.73, "Saudi Arabia AI Stocks", FG, 54, "bold", alpha=a)
    T(f, XR, 0.66, SERIE, MUTED, 34, "bold", alpha=a)
    if CTA:
        T(f, XR, 0.57, campana.CORTA1, BLUE, 34, "bold", alpha=ease((t - 0.2) / 0.5))
        T(f, XR, 0.52, campana.CORTA2, BLUE, 34, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, XR, 0.46, "محتوى تعليمي وليس توصية استثمارية. الأداء السابق لا يضمن النتائج المستقبلية. صُنع بأدوات الذكاء الاصطناعي.", MUTED, 24,
      alpha=a, ancho=40, linespacing=1.5, va="top")
    return with_logo(to_arr(f), LG, x=80, y=170)


TIPOS = {"titulo": s_titulo, "tarjeta": s_tarjeta, "historico": s_historico, "fin": s_fin}
SUB = {}


def overlay(marcas, leads):
    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 40, 70, "bold") for l in (partir(sub_pantalla(s), 34) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = 70; h = lh * len(ls); y0 = int(H * 0.70) + 10; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr = fr.copy()
                fr[y0 - 10:y0 + h + 8, x0:x0 + wmax + 48] = (fr[y0 - 10:y0 + h + 8, x0:x0 + wmax + 48].astype(np.float32) * 0.25 + np.array([6, 25, 26], np.float32) * 0.75).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * lh)
                break
        return fr
    return ov


if __name__ == "__main__":
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(TIPOS[e["tipo"]](e, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"short_{j:02d}_{e['id']}.png"))
        print("palabras", sum(len(e["voz"].split()) for e in ESC)); sys.exit()
    VV = [voz_frases(e["voz"], AUD, gap=0.2) for e in ESC]; sr = VV[0][1]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [0.1 + len(a) / sr + 0.45 for a, _, _, _ in VV]; durs[-1] += 1.0
    if sum(durs) > MAXDUR: sys.exit(f"Short de {sum(durs):.1f} s: acorta la locución (máx. {MAXDUR} s)")
    leads = [0.1] * len(ESC)
    times, t0 = render([lambda t, e=e: TIPOS[e["tipo"]](e, t) for e in ESC], durs, ([v[0] for v in VV], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "sh-silent.mp4"), os.path.join(AUD, "sh.wav"), overlay=overlay([v[2] for v in VV], leads))
    print("listo short", round(t0, 1), "s | voz:", VV[0][3], OUT)
