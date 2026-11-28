# Short vertical (1080x1920, < 60 s) de una lección de «التحليل الفني ببساطة» (Saudi Arabia AI Stocks): el concepto en menos de un minuto
# sobre el mismo gráfico real, para YouTube Shorts, TikTok, Instagram (Reel) y LinkedIn (vídeo nativo, regla de Daniel del 8-nov-2026).
# Escenas en video.json → "short": titulo, grafico (usa zonas y fechas de la escena larga "grafico": <id>), fin. Subtítulos en árabe.
# Zonas seguras de Shorts: texto entre y=0.25 y 0.90, alineado a la derecha en x=0.86 (fuera de los botones).
# Uso: AUD=<scratch> VELAS=<velas.json> [VOZ_DIR=<wav de Azure>] python3 make_short_leccion.py <carpeta de la lección> [preview]
import os, sys, json, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_leccion import *
import campana
from tecnico import MESES

DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json")))
W, H, FPS, MAXDUR = 1080, 1920, 30, 59.0
BASE = VJ["base"]; OUT = f"{DIR}/short-{BASE}-saudi.mp4"; CTA = campana.activa()
ESC = [dict(e) for e in VJ["short"]]
if CTA: ESC[-1]["voz"] = campana.VOZ_CORTA + " " + ESC[-1]["voz"]
LARGAS = {e["id"]: e for e in VJ["escenas"]}
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
VELAS = [v for v in VEL["series"][VJ["simbolo"]]["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]]
DEC = VJ.get("decimales", 2); XR = 0.86
LG = load_logo(150); LGB = load_logo(260)


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def top(f, n):
    T(f, XR, 0.86, f"{SERIE} · الحلقة {VJ['folge']}", GOLD, 30, "bold")
    tot = sum(1 for e in ESC if e["tipo"] == "grafico")
    for i in range(tot):
        f.patches.append(plt.Rectangle((XR - (i + 1) * 0.1 + 0.015, 0.845), 0.085, 0.006, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))


def s_titulo(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.80, f"{SERIE} · الحلقة {VJ['folge']}", GOLD, 34, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.64), 1.0, 0.13, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, XR, 0.705, VJ["tema"], BG, 84 if len(VJ["tema"]) <= 16 else 62, "bold", va="center", alpha=a)
    T(f, XR, 0.57, f"مثال: سهم {VJ['nombre']} ({VJ['ticker']})", FG, 44, "bold", alpha=ease((t - 0.15) / 0.5))
    if e.get("pregunta"): T(f, XR, 0.47, e["pregunta"], BLUE, 44, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, XR, 0.38, "محتوى تعليمي وليس توصية استثمارية", MUTED, 30, "bold", alpha=ease((t - 0.4) / 0.5))
    return with_logo(to_arr(f), LG, x=80, y=170)


def s_grafico(e, t):
    g = LARGAS[e["grafico"]]; n_g = 1 + [x["id"] for x in ESC if x["tipo"] == "grafico"].index(e["id"])
    f = fig(W, H); top(f, n_g); a = ease(t / 0.4)
    T(f, XR, 0.815, e["titulo"], FG, 40, "bold", alpha=a, ancho=36, linespacing=1.1, va="top")
    T(f, XR, 0.722, f"{VJ['nombre']} ({VJ['ticker']}) · شموع يومية · {VEL['series'][VJ['simbolo']].get('fuente', 'TradingView')}", MUTED, 22)
    d0 = g.get("desde", "0"); d1 = g.get("hasta", VJ["ultima_vela"])
    V = [v for v in VELAS if d0 <= fecha_v(v["t"]).isoformat() <= d1]; n = len(V)
    ax = f.add_axes([0.10, 0.38, 0.78, 0.32]); clean(ax)
    o = np.array([v["o"] for v in V]); hi = np.array([v["h"] for v in V]); lo = np.array([v["l"] for v in V]); c = np.array([v["c"] for v in V])
    up = c >= o; xs = np.arange(n); rev = max(2, int(n * ease(t * 1.3)))
    ymin, ymax = lo.min(), hi.max()
    for z in g.get("zonas", []): ymin = min(ymin, z["de"]); ymax = max(ymax, z["a"])
    MED = medias_rango(VELAS, V, g.get("medias", []))
    for m in MED: ymin = min(ymin, np.nanmin(m["y"])); ymax = max(ymax, np.nanmax(m["y"]))
    pad = (ymax - ymin) * 0.08; ax.set_ylim(ymin - pad * 1.5, ymax + pad * (2.5 + 1.6 * len(MED))); ax.set_xlim(-1, n + 1)
    cc_ = [TEAL if u else NEG for u in up]
    ax.vlines(xs[:rev], lo[:rev], hi[:rev], color=cc_[:rev], lw=1.6); ax.bar(xs[:rev], np.maximum(np.abs(c - o), (ymax - ymin) * 0.003)[:rev], bottom=np.minimum(o, c)[:rev], width=0.7, color=cc_[:rev])
    for k, z in enumerate(g.get("zonas", [])):
        b = ease((t - 0.3 - k * 0.12) / 0.35); zc = col(z.get("color", "gold"))
        ax.axhspan(z["de"], z["a"], color=zc, alpha=0.25 * b, lw=0)
        ax.text(n * 0.99, z["a"] + pad * 0.25, ar(z["texto"]) + f"\n{num(z['de'], DEC)}–{num(z['a'], DEC)}", color=zc, fontsize=26, weight="bold", ha="right", va="bottom", alpha=b,
                bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.8 * b))
    ma = ease((t - 0.25) / 0.4)
    for k, m in enumerate(MED):
        ax.plot(xs[:rev], m["y"][:rev], color=m["color"], lw=3.4, alpha=0.95 * ma)
        ax.text(n * 0.99, ymax + pad * (2.3 + 1.6 * k), ar(m["texto"]) + f"  ━━", color=m["color"], fontsize=26, weight="bold", ha="right", va="top", alpha=ma)
    idx = {fecha_v(v["t"]).isoformat(): j for j, v in enumerate(V)}
    for k, m in enumerate(g.get("marcas", [])):
        j = idx.get(m["fecha"]); b = ease((t - 0.5 - k * 0.06) / 0.3)
        if j is None: continue
        if m.get("tipo") == "cruce" and MED:
            ax.plot([j], [MED[0]["y"][j]], marker="o", ms=22, mfc="none", mec=FG, mew=3, alpha=b); continue
        arriba = m.get("tipo") == "techo"; off = (ymax - ymin) * (0.05 if arriba else -0.05)
        ax.plot([j], [(hi[j] if arriba else lo[j]) + off], marker="v" if arriba else "^", color=GOLD, ms=18, alpha=b)
    ax.set_yticks(ax.get_yticks()[1:-1]); tk_y = ax.get_yticks(); dy = 0 if all(abs(y - round(y)) < 1e-6 for y in tk_y) else (1 if all(abs(y * 10 - round(y * 10)) < 1e-6 for y in tk_y) else 2)
    ax.set_yticklabels([num(y, dy) for y in tk_y]); ax.tick_params(labelsize=22)
    ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk, prev = [], None
    for j, v in enumerate(V):
        d = fecha_v(v["t"])
        if d.month != prev: tk.append((j, ar(MESES[d.month - 1]))); prev = d.month
    step = max(1, len(tk) // 4); ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]])
    return with_logo(to_arr(f), LG, x=80, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.80, "الحلقة الكاملة على يوتيوب", GOLD, 46, "bold", alpha=a)
    T(f, XR, 0.73, "Saudi Arabia AI Stocks", FG, 54, "bold", alpha=a)
    T(f, XR, 0.66, f"{SERIE} · كل سبت حلقة جديدة", MUTED, 34, "bold", alpha=a)
    if CTA:
        T(f, XR, 0.57, campana.CORTA1, BLUE, 34, "bold", alpha=ease((t - 0.2) / 0.5))
        T(f, XR, 0.52, campana.CORTA2, BLUE, 34, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, XR, 0.46, "محتوى تعليمي وليس توصية استثمارية. التحليل الفني يصف الماضي ولا يتنبأ بالمستقبل. صُنع بأدوات الذكاء الاصطناعي.", MUTED, 24,
      alpha=a, ancho=40, linespacing=1.5, va="top")
    return with_logo(to_arr(f), LG, x=80, y=170)


TIPOS = {"titulo": s_titulo, "grafico": s_grafico, "fin": s_fin}
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
