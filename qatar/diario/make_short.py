# YouTube Short vertical (1080x1920, < 60 s) del video diario en árabe de @QatarAIStocks (Bolsa de Qatar), con voz Piper y logo.
# Uso: AUD=<scratch> python3 make_short.py <carpeta del día>/short.json [preview]
# Escenas: titulo (fecha de la sesión EN GRANDE y el índice QE), cifra, kpis, fin. "out" relativo a la carpeta del JSON.
# Zonas seguras de Shorts: arriba ~8 % (búsqueda), abajo ~22 % (título, canal) y franja derecha (botones): el texto va entre y=0.25 y 0.90
# y alineado a la derecha en x=0.86 para no quedar bajo los botones.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
W, H, FPS = 1080, 1920, 30
AUD = os.environ.get("AUD", "aud"); MAXDUR = 59.0
LG = load_logo(150); LGB = load_logo(260)
XR = 0.86


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def top(f, e):
    T(f, XR, 0.835, S["cabecera"], GOLD, 30, "bold")
    tot = sum(1 for x in S["escenas"] if "n" in x)
    for i in range(tot):
        f.patches.append(plt.Rectangle((XR - (i + 1) * 0.075 + 0.015, 0.82), 0.06, 0.006, transform=f.transFigure, color=GOLD if i < e["n"] else DIM, figure=f))


def s_titulo(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.80, e["kicker"], GOLD, 36, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.665), 1.0, 0.115, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, XR, 0.722, e["fecha"], BG, 76, "bold", va="center", alpha=a)
    for i, (nom, big, sub, c) in enumerate(e["indices"]):
        b = ease((t - 0.15 - i * 0.15) / 0.5); y = 0.57 - i * 0.165
        T(f, XR, y, nom, MUTED, 38, "bold", alpha=b)
        f.text(XR, y - 0.075, big, color=col(c), fontsize=110, weight="bold", ha="right", alpha=b)
        f.text(0.10, y - 0.06, sub, color=FG, fontsize=40, weight="bold", ha="left", alpha=b)
    if e.get("pregunta"): T(f, XR, 0.295, e["pregunta"], BLUE, 38, "bold", alpha=ease((t - 0.4) / 0.5), va="top", linespacing=1.4)
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_cifra(e, t):
    f = fig(W, H); top(f, e); a = ease(t / 0.4)
    T(f, XR, 0.73, f"{e['n']}. {e['label']}", MUTED, 44, "bold", alpha=a)
    f.text(XR, 0.62, e["big"], color=col(e["color"]), fontsize=150 if len(e["big"]) < 8 else 110, weight="bold", ha="right", alpha=a)
    T(f, XR, 0.555, e["delta"], FG, 40, "bold", alpha=ease((t - 0.15) / 0.4))
    if e.get("barras"):
        ax = f.add_axes([0.12, 0.36, 0.50, 0.15]); clean(ax); B = e["barras"]; ee = ease(t)
        y = np.arange(len(B))[::-1]; v = [x[1] for x in B]
        ax.barh(y, [abs(x) * ee for x in v], color=[TEAL if x > 0 else NEG for x in v], height=0.6)
        ax.set_yticks(y, [ar(x[0]) for x in B]); ax.yaxis.tick_right(); ax.tick_params(colors=FG, labelsize=30); ax.set_xticks([])
        ax.set_xlim(max(abs(x) for x in v) * 1.6, 0)  # barras de derecha a izquierda
        if t >= 0.5:
            for yy, x in zip(y, v): ax.text(abs(x) * ee + max(abs(q) for q in v) * 0.05, yy, pct(x), va="center", ha="right", color=FG, fontsize=30, weight="bold")
    if e.get("nota"): T(f, XR, 0.33, e["nota"], MUTED, 32, alpha=ease((t - 0.4) / 0.5), linespacing=1.4, va="top")
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_kpis(e, t):
    f = fig(W, H); top(f, e)
    T(f, XR, 0.73, f"{e['n']}. {e['label']}", MUTED, 44, "bold", alpha=ease(t / 0.4))
    for i, (big, lab, c) in enumerate(e["items"]):
        b = ease((t - i * 0.15) / 0.4); y = 0.63 - i * 0.125
        f.text(XR, y, big, color=col(c), fontsize=88, weight="bold", ha="right", alpha=b)
        T(f, XR, y - 0.038, lab, FG, 32, alpha=b)
    if e.get("nota"): T(f, XR, 0.30, e["nota"], MUTED, 30, alpha=ease((t - 0.4) / 0.5), linespacing=1.4, va="top")
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.70, e["nombre"], FG, 56, "bold", alpha=a)
    T(f, XR, 0.655, e["titular"], GOLD, 40, "bold", alpha=a, linespacing=1.05, va="top")
    if cta_activa():  # campaña de comentarios y suscripción (comun.py): sustituye la línea "◀ cta"
        b = ease((t - 0.2) / 0.5)
        T(f, XR, 0.52, CTA_SHORT[0], FG, 36, "bold", alpha=b)
        T(f, XR, 0.477, CTA_SHORT[1], FG, 36, "bold", alpha=b)
        T(f, XR, 0.43, "◀ " + CTA_SHORT[2], GOLD, 40, "bold", alpha=b)
    else:
        T(f, XR, 0.43, "◀ " + e["cta"], FG, 42, "bold", alpha=ease((t - 0.2) / 0.5))
    f.text(XR, 0.385, "youtube.com/@QatarAIStocks", color=BLUE, fontsize=40, weight="bold", ha="right", alpha=ease((t - 0.2) / 0.5))
    T(f, XR, 0.355, S["fuente"] + "\nمحتوى تعليمي وإعلامي فقط ولا يُعد نصيحة استثمارية.\nلا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر.\nالتحليل الفني بيانات وليس إشارات شراء أو بيع.", MUTED, 24, linespacing=1.5, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=(W - 260) // 2, y=150)


RX = {"titulo": s_titulo, "cifra": s_cifra, "kpis": s_kpis, "fin": s_fin}
def frame(e, t): return RX[e["tipo"]](e, t)


if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); E = S["escenas"]; S["out"] = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), S["out"]); os.makedirs(AUD, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"short_prev_{i}.png"))
        sys.exit()
    if cta_activa(): E[-1]["voz"] = CTA_VOZ["short"] + " " + E[-1]["voz"]
    clips = [voz(e["voz"], os.path.join(AUD, f"short_{i}.wav")) for i, e in enumerate(E)]; sr = clips[0][1]
    LEAD, TAIL = 0.10, 0.35
    durs = [LEAD + len(a) / sr + TAIL for a, _ in clips]; durs[-1] += 1.0
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if sum(durs) > MAXDUR: sys.exit(f"Short demasiado largo: {sum(durs):.1f} s (máx {MAXDUR}). Acorta la voz.")
    times, t0 = render([lambda t, e=e: frame(e, t) for e in E], durs, ([a for a, _ in clips], [LEAD] * len(E)), sr, W, H, FPS, S["out"],
                       os.path.join(AUD, "short-silent.mp4"), os.path.join(AUD, "short-full.wav"), loud=-14, ANIM=24, XF=6)
    print("listo", S["out"], round(t0, 1), "s")
