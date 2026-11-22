# Short semanal «تقويم النتائج الأسبوعي» de @QatarAIStocks (1080x1920, 45-59 s, árabe, voz Piper).
# Uso: AUD=<scratch> python3 make_calendario.py <carpeta de la semana>/calendario.json [preview]
# Escenas: gancho (la empresa más importante + N más), empresa (una por compañía, en orden cronológico), fin (seguir el canal,
# canal de Wall Street en árabe si hay empresas de EE. UU., aviso). Reutiliza fuente, colores, logo, voz y render de ../diario/comun.py.
# Zonas seguras de Shorts: texto entre y=0.25 y 0.86, alineado a la derecha en x=0.86 (los botones van a la derecha, abajo).
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *  # noqa: F401,F403  (ar, fig, to_arr, with_logo, load_logo, voz, render, colores)
W, H, FPS = 1080, 1920, 30
AUD = os.environ.get("AUD", "aud"); MAXDUR = 59.0; MINDUR = 45.0; MINEMP = float(os.environ.get("MINEMP", "6.0"))  # 6-8 s por empresa (Daniel)
LG = load_logo(150); LGB = load_logo(260)
XR = 0.86
NABD = "youtube.com/@NabdWallStreet"


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def L(f, x, y, s, c=FG, fs=30, w="normal", ha="right", **k):  # texto latino (tickers, cifras) sin reshaper
    return f.text(x, y, s, color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def barra(f, a=1.0):
    T(f, XR, 0.835, S["cabecera"], GOLD, 30, "bold", alpha=a)
    tot = sum(1 for x in S["escenas"] if x["tipo"] == "empresa")
    return tot


def s_gancho(e, t):
    f = fig(W, H); a = ease(t / 0.4)
    T(f, XR, 0.80, e["kicker"], GOLD, 38, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.69), 1.0, 0.09, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, XR, 0.735, e["semana"], BG, 54, "bold", va="center", alpha=a)
    b = ease((t - 0.1) / 0.4)
    T(f, XR, 0.62, e["linea1"], FG, 62, "bold", alpha=b)
    T(f, XR, 0.545, e["estrella"], GOLD, 96, "bold", alpha=b)
    T(f, XR, 0.475, e["linea2"], FG, 56, "bold", alpha=ease((t - 0.25) / 0.4))
    if e.get("nota"): T(f, XR, 0.37, e["nota"], MUTED, 32, alpha=ease((t - 0.4) / 0.5), va="top", linespacing=1.5)
    if e.get("logos"):  # tickers en fila
        c = ease((t - 0.35) / 0.5)
        L(f, XR, 0.405, "   ".join(e["logos"]), BLUE, 34, "bold", alpha=c)
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_empresa(e, t):
    f = fig(W, H); tot = barra(f)
    for i in range(tot):
        f.patches.append(plt.Rectangle((XR - (i + 1) * 0.075 + 0.015, 0.82), 0.06, 0.006, transform=f.transFigure, color=GOLD if i < e["n"] else DIM, figure=f))
    a = ease(t / 0.35)
    # día y hora
    f.patches.append(plt.Rectangle((0.14, 0.715), XR - 0.14 + 0.02, 0.07, transform=f.transFigure, color=DIM, alpha=a, figure=f))
    T(f, XR, 0.75, e["dia"], GOLD, 44, "bold", va="center", alpha=a)
    T(f, XR, 0.665, e["mercado"], MUTED, 34, "bold", alpha=a)
    b = ease((t - 0.1) / 0.4)
    T(f, XR, 0.585, e["nombre"], FG, 84, "bold", alpha=b)
    L(f, XR, 0.53, e["ticker"], BLUE, 46, "bold", alpha=b)
    y = 0.445
    for j, (lab, big) in enumerate(e["datos"]):
        c = ease((t - 0.25 - j * 0.15) / 0.4)
        T(f, XR, y, lab, MUTED, 34, alpha=c)
        L(f, XR, y - 0.07, big, TEAL, 84, "bold", alpha=c)
        y -= 0.135
    if not e["datos"]:
        T(f, XR, y, "لا توجد تقديرات منشورة", MUTED, 36, alpha=ease((t - 0.25) / 0.4))
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.4)
    T(f, XR, 0.72, e["titular"], GOLD, 54, "bold", alpha=a, linespacing=1.3, va="top")
    b = ease((t - 0.2) / 0.5)
    f.text(XR, 0.585, "youtube.com/@QatarAIStocks", color=col(BLUE), fontsize=42, weight="bold", ha="right", alpha=b)
    if e.get("nabd"):
        c = ease((t - 0.35) / 0.5)
        T(f, XR, 0.515, e["nabd"], FG, 38, "bold", alpha=c)
        f.text(XR, 0.47, NABD, color=col(TEAL), fontsize=40, weight="bold", ha="right", alpha=c)
    T(f, XR, 0.405, "محتوى معلوماتي، وليس توصية استثمارية.", FG, 34, "bold", alpha=a)
    T(f, XR, 0.37, S["fuente"], MUTED, 24, linespacing=1.5, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=(W - 260) // 2, y=150)


RX = {"gancho": s_gancho, "empresa": s_empresa, "fin": s_fin}
def frame(e, t): return RX[e["tipo"]](e, t)


if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); E = S["escenas"]; S["out"] = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), S["out"]); os.makedirs(AUD, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"cal_prev_{i}.png"))
        sys.exit()
    clips = [voz(e["voz"], os.path.join(AUD, f"cal_{i}.wav")) for i, e in enumerate(E)]; sr = clips[0][1]
    LEAD, TAIL = 0.08, 0.25
    durs = [max(LEAD + len(a) / sr + TAIL, MINEMP if e["tipo"] == "empresa" else 0) for (a, _), e in zip(clips, E)]; durs[-1] += 1.2
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if sum(durs) > MAXDUR: sys.exit(f"Short demasiado largo: {sum(durs):.1f} s (máx {MAXDUR}). Acorta la voz o quita una empresa.")
    if sum(durs) < MINDUR: durs[-1] += MINDUR - sum(durs)  # mínimo 45 s (pedido de Daniel): alarga el cierre
    times, t0 = render([lambda t, e=e: frame(e, t) for e in E], durs, ([a for a, _ in clips], [LEAD] * len(E)), sr, W, H, FPS, S["out"],
                       os.path.join(AUD, "cal-silent.mp4"), os.path.join(AUD, "cal-full.wav"), loud=-14, ANIM=20, XF=6)
    print("listo", S["out"], round(t0, 1), "s")
