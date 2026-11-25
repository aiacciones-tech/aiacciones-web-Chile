# Short vertical (1080x1920, < 60 s) de una lección de «Análisis técnico, explicado fácil» (AIAcciones España): el concepto en menos de
# un minuto sobre el mismo gráfico real, para YouTube Shorts, TikTok, Instagram (Reel) y LinkedIn (vídeo nativo, regla de Daniel del 8-nov-2026).
# Escenas en video.json → "short": titulo, grafico (usa rango, líneas y marcas de la escena larga "grafico": <id>), fin. Subtítulos.
# Zonas seguras de Shorts: contenido entre y=0.25 y 0.90, sin tocar la franja derecha (botones).
# Uso: AUD=<scratch> VELAS=<velas.json> [VOZ_DIR=<mp3 de la voz>] python3 make_short_leccion.py <carpeta de la lección> [preview]
import os, sys, json, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_leccion import *
from voz_leccion import cta, CTA_VOZ_CORTA

DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json")))
W, H, FPS, MAXDUR = 1080, 1920, 30, 59.0
FIJO = VJ.get("formato") == "fijo"   # vídeos fijos (espana/fijos/): otra cabecera y escenas cifras/puntos
ETIQ = VJ.get("etiqueta", "Guías de bolsa española") if FIJO else SERIE
BASE = VJ["base"]; OUT = f"{DIR}/short-{BASE}.mp4"; CTA = cta(VJ); N = VJ.get("capitulo_n", 0)
ESC = [dict(e) for e in VJ["short"]]
if CTA: ESC[-1]["voz"] = CTA_VOZ_CORTA + " " + ESC[-1]["voz"]
LARGAS = {e["id"]: e for e in VJ["escenas"]}
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
SER = VEL["series"][VJ["simbolo"]]
VELAS = [v for v in SER["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]]
FECHAS = [fecha_v(v["t"]).isoformat() for v in VELAS]; IND = indicadores(VELAS)
DEC = VJ.get("decimales", 2); XL = 0.08
LG = load_logo(420)


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="left", **k):
    return f.text(x, y, s, color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def top(f, n):
    T(f, XL, 0.86, ETIQ.upper() if FIJO else f"{SERIE.upper()} · CAP. {N}", ACC, 28, "bold")
    tot = sum(1 for e in ESC if e["tipo"] in ("grafico", "cifras", "puntos"))
    for i in range(tot):
        f.patches.append(plt.Rectangle((XL + i * 0.12, 0.845), 0.105, 0.006, transform=f.transFigure, color=ACC if i < n else DIM, figure=f))


def s_titulo(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XL, 0.80, ETIQ.upper() if FIJO else f"{SERIE.upper()} · CAP. {N}", ACC, 30, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.64), 1.0, 0.13, transform=f.transFigure, color=ACC, alpha=a, figure=f))
    T(f, XL, 0.705, VJ["tema"], BG, 80 if len(VJ["tema"]) <= 14 else 62, "bold", va="center", alpha=a)
    T(f, XL, 0.575, e.get("sub", "") if FIJO else f"Con el gráfico real de {VJ['nombre']}", FG, 44, "bold", alpha=ease((t - 0.15) / 0.5))
    if e.get("pregunta"): T(f, XL, 0.48, e["pregunta"], ACC2, 50, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, XL, 0.39, "Contenido informativo, no es recomendación" if FIJO else "Contenido educativo, no es recomendación", MUTED, 32, "bold", alpha=ease((t - 0.4) / 0.5))
    return with_logo(to_arr(f), LG, x=(W - 420) // 2, y=170)


def s_grafico(e, t):
    g = LARGAS[e["grafico"]]; n_g = 1 + [x["id"] for x in ESC if x["tipo"] == "grafico"].index(e["id"])
    f = fig(W, H); top(f, n_g); a = ease(t / 0.4)
    T(f, XL, 0.815, "\n".join(partir(e["titulo"], 30)), FG, 44, "bold", alpha=a, linespacing=1.1, va="top")
    T(f, XL, 0.715, f"{VJ['nombre']} ({VJ['ticker']}) · velas diarias · {SER.get('fuente', 'TradingView')}", MUTED, 24)
    J = [j for j, d in enumerate(FECHAS) if g.get("desde", "0") <= d <= g.get("hasta", VJ["ultima_vela"])]; n = len(J); V = [VELAS[j] for j in J]
    ax = f.add_axes([0.08, 0.38, 0.80, 0.31]); clean(ax)
    o = np.array([v["o"] for v in V]); hi = np.array([v["h"] for v in V]); lo = np.array([v["l"] for v in V]); c = np.array([v["c"] for v in V])
    up = c >= o; xs = np.arange(n); rev = max(2, int(n * ease(t * 1.3)))
    LIN = [(l, IND[l["ind"]][J]) for l in g.get("lineas", [])]
    ymin, ymax = lo.min(), hi.max()
    for _, s in LIN: ymin = min(ymin, np.nanmin(s)); ymax = max(ymax, np.nanmax(s))
    pad = (ymax - ymin) * 0.08; ax.set_ylim(ymin - pad * 1.5, ymax + pad * 2.5); ax.set_xlim(-1, n + 1)
    cc_ = [ACC if u else NEG for u in up]
    ax.vlines(xs[:rev], lo[:rev], hi[:rev], color=cc_[:rev], lw=1.2, alpha=0.75)
    ax.bar(xs[:rev], np.maximum(np.abs(c - o), (ymax - ymin) * 0.003)[:rev], bottom=np.minimum(o, c)[:rev], width=0.7, color=cc_[:rev], alpha=0.75)
    for k, (l, s) in enumerate(LIN):
        ax.plot(xs[:rev], s[:rev], color=col(l.get("color", "acc2")), lw=4)
        T(f, XL + k * 0.42, 0.325, f"— {l.get('texto', l['ind'])}: {num(s[-1], DEC)}", col(l.get("color", "acc2")), 28, "bold", alpha=a)
    idx = {FECHAS[j]: k for k, j in enumerate(J)}
    for k, m in enumerate(g.get("marcas", [])):
        j = idx.get(m["fecha"]); b = ease((t - 0.5 - k * 0.06) / 0.3)
        if j is None: continue
        if m.get("tipo") == "cruce":
            ax.plot([j], [LIN[0][1][j] if LIN else c[j]], "o", ms=30, mfc="none", mec=NEG, mew=4, alpha=b)
        else:
            arriba = m.get("tipo") == "techo"; off = (ymax - ymin) * (0.05 if arriba else -0.05)
            ax.plot([j], [(hi[j] if arriba else lo[j]) + off], marker="v" if arriba else "^", color=NEG, ms=20, alpha=b)
    ax.set_yticks(ax.get_yticks()[1:-1]); ax.set_yticklabels([num(y, 0) for y in ax.get_yticks()]); ax.tick_params(labelsize=22)
    ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk, prev = [], None
    for k, j in enumerate(J):
        d = dt.date.fromisoformat(FECHAS[j])
        if d.month != prev: tk.append((k, MESES[d.month - 1] + (f"\n{d.year}" if d.month == 1 or not tk else ""))); prev = d.month
    step = max(1, len(tk) // 5); ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]])
    return with_logo(to_arr(f), load_logo(300), x=(W - 300) // 2, y=55)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XL, 0.78, "El vídeo completo," if FIJO else "El capítulo completo,", ACC, 48, "bold", alpha=a)
    T(f, XL, 0.735, "en nuestro canal de YouTube", ACC, 48, "bold", alpha=a)
    T(f, XL, 0.66, "@AIAccionesEspaña", FG, 58, "bold", alpha=a)
    T(f, XL, 0.60, "El IBEX 35, cada día de bolsa" if FIJO else "Un capítulo nuevo cada domingo", MUTED, 36, "bold", alpha=a)
    if CTA: T(f, XL, 0.54, "Déjanos tu comentario y suscríbete", ACC2, 36, "bold", alpha=ease((t - 0.2) / 0.5))
    av = ("Contenido informativo, no es una recomendación de inversión. Cifras de las fuentes citadas en el vídeo completo. "
          "Hecho con herramientas de inteligencia artificial.") if FIJO else ("Contenido educativo, no es una recomendación de inversión. "
          "El análisis técnico describe el pasado y no predice el futuro. Hecho con herramientas de inteligencia artificial.")
    T(f, XL, 0.48, "\n".join(partir(av, 46)), MUTED, 26, alpha=a, linespacing=1.5, va="top")
    return with_logo(to_arr(f), LG, x=(W - 420) // 2, y=170)


def _n(e):
    return 1 + [x["id"] for x in ESC if x["tipo"] in ("grafico", "cifras", "puntos")].index(e["id"])


def s_cifras(e, t):
    """Hasta 3 cifras grandes [valor, etiqueta, color], una debajo de otra."""
    f = fig(W, H); top(f, _n(e)); a = ease(t / 0.4)
    T(f, XL, 0.815, "\n".join(partir(e["titulo"], 30)), FG, 44, "bold", alpha=a, linespacing=1.1, va="top")
    for k, (v, lab, c) in enumerate(e["cifras"][:3]):
        b = ease((t - k * 0.15) / 0.4); y = 0.645 - k * 0.10
        T(f, XL, y, v, c, 84 if len(v) <= 9 else 64, "bold", alpha=b)
        T(f, XL, y - 0.03, lab, MUTED, 30, "bold", alpha=b)
    return with_logo(to_arr(f), load_logo(300), x=(W - 300) // 2, y=55)


def s_puntos(e, t):
    f = fig(W, H); top(f, _n(e)); a = ease(t / 0.4)
    T(f, XL, 0.815, "\n".join(partir(e["titulo"], 30)), FG, 44, "bold", alpha=a, linespacing=1.1, va="top")
    for k, p in enumerate(e["puntos"][:4]):
        b = ease((t - k * 0.12) / 0.4)
        T(f, XL, 0.66 - k * 0.085, "\n".join(partir("• " + p, 36)), FG, 36, "bold", alpha=b, va="top", linespacing=1.2)
    return with_logo(to_arr(f), load_logo(300), x=(W - 300) // 2, y=55)


TIPOS = {"titulo": s_titulo, "grafico": s_grafico, "fin": s_fin, "cifras": s_cifras, "puntos": s_puntos}
SUB = {}


def overlay(marcas, leads):
    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 40, 70, "bold") for l in (partir(s, 34) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = 70; h = lh * len(ls); y0 = int(H * 0.69) + 10; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr = fr.copy()
                fr[y0 - 10:y0 + h + 8, x0:x0 + wmax + 48] = (fr[y0 - 10:y0 + h + 8, x0:x0 + wmax + 48].astype(np.float32) * 0.25 + np.array([5, 14, 30], np.float32) * 0.75).astype(np.uint8)
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
