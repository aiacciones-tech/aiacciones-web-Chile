# Capítulo de la serie semanal «Análisis fundamental en simple» de AIAcciones Chile (Daniel, 20-nov-2026): un concepto por video,
# explicado sobre las cifras reales de una empresa del IPSA. 1920x1080, unos 6 minutos, voz del canal (Azure Lorenzo), subtítulos.
# Escenas en video.json → "escenas"; tipos: portada, puntos, cuenta (estado de resultados por líneas), cascada (de ingresos a utilidad),
# barras (serie por años), kpis, formula, fin. Toda cifra de pantalla está escrita en video.json desde datos.json (TradingView) o los informes oficiales.
# Uso: AUD=<scratch> [VOZ_DIR=<wav por frase>] python3 make_capitulo.py <carpeta del capítulo> [preview]
#   Escribe <base>.mp4, subtitulos-<base>.srt, times.json y guion-<base>.md en la carpeta.
import os, sys, json, textwrap, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_fund import *

DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")) if DIR else {}
W, H = 1920, 1080
MIN_S, MAX_S = 300, 450   # unos 6 minutos (5:00-7:30)
BASE = VJ.get("base", ""); OUT = f"{DIR}/{BASE}.mp4"
ESC = VJ.get("escenas", [])
XL = 0.06   # margen izquierdo
LG = load_logo(250); LGB = load_logo(520)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="left", **k):
    return f.text(x, y, s, color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def wrap(s, n): return "\n".join(textwrap.wrap(str(s), n, break_long_words=False))


def base(i, e):
    f = fig(W, H)
    T(f, XL, 0.905, e.get("kicker", "").upper(), ACC, 22, "bold")
    tt = e.get("titulo", ""); T(f, XL, 0.83, tt, FG, 42 if len(tt) <= 55 else 34, "bold")
    T(f, 0.94, 0.925, f"{SERIE.upper()} · CAPÍTULO {VJ['capitulo_n']}", MUTED, 17, "bold", ha="right")
    T(f, 0.94, 0.89, f"{VJ['tema']} · {VJ['nombre']}", DIM, 15, "bold", ha="right")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n): rect(f, XL + k * w, 0.975, w - 0.008, 0.008, ACC if k < CAP_IDX[i] else DIM)
    return f


def fuente(f, e):
    s = e.get("fuente") or VJ.get("fuente_general", "")
    if s: T(f, XL, 0.222, wrap(s, 175), MUTED, 13, style="italic", linespacing=1.25, va="top")


def U(v, d=1): return es(v, d)


# ---------- escenas ----------
def s_portada(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, XL, 0.88, f"SERIE · {SERIE.upper()}", ACC, 28, "bold", alpha=a)
    rect(f, 0, 0.60, 1.0, 0.22, ACC, a)
    T(f, XL, 0.765, f"CAPÍTULO {VJ['capitulo_n']}", BG, 32, "bold", va="center", alpha=a)
    T(f, XL, 0.665, VJ["tema"], BG, 64 if len(VJ["tema"]) <= 34 else 50, "bold", va="center", alpha=a)
    T(f, XL, 0.50, f"Con las cifras reales de {VJ['nombre']}", FG, 42, "bold", alpha=ease((t - 0.15) / 0.5))
    T(f, XL, 0.44, f"({VJ['ticker']})", MUTED, 28, "bold", alpha=ease((t - 0.2) / 0.5))
    if e.get("sub"): T(f, XL, 0.36, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    T(f, XL, 0.25, "Contenido educativo, no es una recomendación de inversión", ACC2, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=W - 520 - 60, y=40)


def s_puntos(i, e, t):
    f = base(i, e); P = e["puntos"][:5]; hh = min(0.12, 0.5 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.76 - (k + 1) * hh; h = hh - 0.014
        rect(f, XL, y, 0.88, h, NAVY, b); rect(f, XL, y, 0.004, h, e.get("colores", [ACC] * 5)[k], b)
        T(f, XL + 0.018, y + h / 2, f"{k + 1}", ACC, 34, "bold", va="center", alpha=b)
        T(f, XL + 0.05, y + h / 2, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.40, y + h / 2, wrap(txt, 70), MUTED, 21, va="center", alpha=b, linespacing=1.15)
    fuente(f, e)
    return to_arr(f)


TIPO_C = {"ingreso": FG, "resta": NEG, "suma": ACC, "sub": ACC2, "final": ACC, "nota": MUTED}


def s_cuenta(i, e, t):
    """Estado de resultados línea a línea: filas [{t, v:[col1, col2], tipo, d}], columnas ["3T 2026", "3T 2025"]. Columna «Variación» calculada."""
    f = base(i, e); R = e["filas"]; C = e["columnas"]; n = len(R); hh = min(0.062, 0.42 / n); var = e.get("variacion", len(C) == 2)
    xs = [0.56, 0.70][:len(C)]; xv = 0.85
    y0 = 0.745
    T(f, XL + 0.01, y0, e.get("unidad", "US$ millones"), MUTED, 18, "bold", va="center")
    for c, x in zip(C, xs): T(f, x, y0, c, ACC, 24, "bold", va="center", ha="center")
    if var: T(f, xv, y0, "Variación (calculada)", MUTED, 18, "bold", va="center", ha="center")
    hi = e.get("destacar")
    for k, r in enumerate(R):
        b = ease((t * 1.4 - k * 0.09) / 0.35); y = y0 - (k + 1) * hh; tp = r.get("tipo", "ingreso"); c = TIPO_C.get(tp, FG)
        if tp in ("sub", "final") or (hi and k in hi): rect(f, XL, y - hh * 0.45, 0.88, hh * 0.9, NAVY, b)
        if tp == "final": rect(f, XL, y - hh * 0.45, 0.004, hh * 0.9, ACC, b)
        lab = ("− " if tp == "resta" else ("+ " if tp == "suma" else "")) + r["t"]
        T(f, XL + 0.015, y, lab, c, 24 if tp in ("sub", "final") else 22, "bold" if tp != "nota" else "normal", va="center", alpha=b)
        for v, x in zip(r.get("v", []), xs):
            f.text(x, y, U(v, r.get("d", 1)) if v is not None else "—", color=col(c), fontsize=24, weight="bold", ha="center", va="center", alpha=b)
        vv = r.get("v", [])
        if var and len(vv) == 2 and all(isinstance(x, (int, float)) for x in vv) and vv[1] and vv[1] > 0 and vv[0] > 0 and not r.get("sin_var"):
            ch = (vv[0] / vv[1] - 1) * 100
            f.text(xv, y, (f"{ch:+.0f}%" if abs(ch) >= 1 else f"{ch:+.1f}%").replace(".", ","), color=col(MUTED if tp == "resta" else (ACC if ch >= 0 else NEG)),
                   fontsize=22, weight="bold", ha="center", va="center", alpha=b)
    if e.get("nota"): T(f, XL, 0.255, e["nota"], ACC2, 21, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_cascada(i, e, t):
    """Puente de ingresos a utilidad: pasos [{t, v, tipo: total|resta|suma}] de izquierda a derecha."""
    f = base(i, e); P = e["pasos"]; n = len(P)
    ax = f.add_axes([0.06, 0.32, 0.88, 0.42]); clean(ax)
    acc, bars = 0.0, []
    for p in P:
        if p["tipo"] == "total": bars.append((0, p["v"])); acc = p["v"]
        elif p["tipo"] == "resta": bars.append((acc - p["v"], p["v"])); acc -= p["v"]
        else: bars.append((acc, p["v"])); acc += p["v"]
    top = max(b0 + h for b0, h in bars)
    xs = np.arange(n)
    for k, ((b0, h), p, x) in enumerate(zip(bars, P, xs)):
        a = ease((t * 1.3 - k * 0.1) / 0.35); c = ACC if p["tipo"] == "total" else (NEG if p["tipo"] == "resta" else ACC2)
        ax.bar(x, h * a, bottom=b0 + (h * (1 - a) if p["tipo"] == "resta" else 0), color=c, width=0.62, alpha=0.95)
        ax.text(x, b0 + h + top * 0.03, ("−" if p["tipo"] == "resta" else ("+" if p["tipo"] == "suma" else "")) + U(p["v"], p.get("d", 0)),
                color=FG, fontsize=23, weight="bold", ha="center", alpha=a)
        if k < n - 1:
            lvl = b0 + h if p["tipo"] != "resta" else b0
            ax.plot([x + 0.31, x + 0.69], [lvl, lvl], color=MUTED, lw=1, ls=":", alpha=a)
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(0, top * 1.15); ax.set_yticks([])
    ax.set_xticks(xs, [wrap(p["t"], 16 if n <= 6 else 13) for p in P]); ax.tick_params(colors=FG, labelsize=18)
    T(f, XL, 0.775, e.get("unidad", "US$ millones"), MUTED, 18, "bold")
    if e.get("nota"): T(f, 0.94, 0.775, e["nota"], ACC2, 20, "bold", ha="right", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_barras(i, e, t):
    """Serie por años: categorias [...], series [{nombre, valores, color}], etiquetas con el valor (negativos hacia abajo)."""
    f = base(i, e); C = e["categorias"]; S = e["series"]; n, m = len(C), len(S)
    ax = f.add_axes([0.06, 0.35, 0.88, 0.37]); clean(ax); wdt = 0.8 / m; a = ease(t * 1.2)
    vals_all = [v for s in S for v in s["valores"] if v is not None]; top = max(max(vals_all), 0); bot = min(min(vals_all), 0)
    span = top - bot
    for j, s in enumerate(S):
        x = np.arange(n) + (j - (m - 1) / 2) * wdt; vals = [v if v is not None else 0 for v in s["valores"]]
        ax.bar(x, [v * a for v in vals], width=wdt * 0.9, color=[col(s.get("color", "acc")) if v >= 0 else NEG for v in vals])
        if t > 0.5:
            for xx, v in zip(x, s["valores"]):
                if v is not None:
                    ax.text(xx, v * a + span * 0.025 if v >= 0 else span * 0.025, U(v, e.get("d", 0)), color=FG if v >= 0 else NEG, fontsize=19 if m > 1 else 23, weight="bold", ha="center")
    if bot < 0: ax.axhline(0, color=MUTED, lw=1)
    ax.set_xticks(np.arange(n), C); ax.tick_params(colors=FG, labelsize=21); ax.set_yticks([]); ax.set_ylim(bot * 1.25 if bot < 0 else 0, top * 1.15)
    for j, s in enumerate(S):   # leyenda arriba a la izquierda
        rect(f, XL, 0.762 - j * 0.04, 0.012, 0.022, s.get("color", "acc")); T(f, XL + 0.018, 0.765 - j * 0.04, s["nombre"], FG, 20, "bold", va="bottom")
    T(f, 0.94, 0.765, e.get("unidad", "US$ millones"), MUTED, 18, "bold", ha="right")
    if e.get("nota"): T(f, XL, 0.255, e["nota"], ACC2, 21, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_kpis(i, e, t):
    f = base(i, e); K = e["items"][:4]; n = len(K); w = 0.88 / n
    for k, it in enumerate(K):
        b = ease((t - k * 0.12) / 0.4); x0 = XL + k * w
        rect(f, x0, 0.35, w - 0.015, 0.39, NAVY, b); rect(f, x0, 0.735, w - 0.015, 0.006, it.get("color", "acc"), b)
        cx = x0 + (w - 0.015) / 2
        f.text(cx, 0.60, it["big"], color=col(it.get("color", "acc")), fontsize=64 if len(it["big"]) <= 8 else 48, weight="bold", ha="center", va="center", alpha=b)
        T(f, cx, 0.48, wrap(it["label"], 28), FG, 23, "bold", ha="center", va="center", alpha=b, linespacing=1.1)
        if it.get("sub"): T(f, cx, 0.395, wrap(it["sub"], 30), MUTED, 18, ha="center", va="center", alpha=b, linespacing=1.3)
    if e.get("nota"): T(f, XL, 0.275, e["nota"], ACC2, 21, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_formula(i, e, t):
    """Fórmula en grande y un ejemplo con las cifras de la empresa: formula (texto), ejemplo [[texto, resultado]], nota."""
    f = base(i, e); a = ease(t / 0.4)
    rect(f, XL, 0.56, 0.88, 0.17, NAVY, a); rect(f, XL, 0.56, 0.004, 0.17, ACC, a)
    T(f, 0.5, 0.645, e["formula"], ACC, 42 if len(e["formula"]) <= 44 else 32, "bold", ha="center", va="center", alpha=a)
    for k, (txt, res) in enumerate(e.get("ejemplo", [])[:3]):
        b = ease((t - 0.25 - k * 0.15) / 0.4); y = 0.50 - k * 0.07
        T(f, XL + 0.01, y, txt, FG, 26, "bold", va="center", alpha=b)
        f.text(0.92, y, res, color=ACC2, fontsize=34, weight="bold", ha="right", va="center", alpha=b)
    if e.get("nota"): T(f, XL, 0.31, wrap(e["nota"], 130), MUTED, 19, alpha=ease((t - 0.6) / 0.4), linespacing=1.3, va="top")
    fuente(f, e)
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XL, 0.86, f"Capítulo {VJ['capitulo_n']}: {VJ['tema']}", FG, 40, "bold", alpha=a)
    T(f, XL, 0.80, "EN RESUMEN", ACC, 26, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, XL, 0.73 - k * 0.062, wrap("• " + c, 95), FG, 24, alpha=ease((t - 0.1 - k * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    if e.get("siguiente"): T(f, XL, 0.46, "Próximo capítulo: " + e["siguiente"], ACC, 26, "bold", alpha=b)
    if VJ.get("_cta"): T(f, XL, 0.41, campana.PANTALLA_VIDEO, ACC2, 24, "bold", alpha=b)
    else: T(f, XL, 0.41, "Un capítulo cada domingo · youtube.com/@aiaccioneschile · aiacciones.cl", ACC2, 24, "bold", alpha=b)
    aviso = (f"Aviso: contenido educativo e informativo. No es una recomendación de inversión ni una invitación a comprar o vender valores. {VJ['nombre']} es solo un ejemplo "
             "para explicar el concepto. Cifras de los informes oficiales de la empresa y de TradingView; los cálculos propios dicen «calculado». No emitimos precio objetivo. "
             "AIAcciones Chile no tiene posiciones en las acciones citadas. Invertir en acciones conlleva riesgo. Guion, gráficos y voz (sintética) hechos con inteligencia artificial.")
    T(f, XL, 0.33, wrap(aviso, 125), MUTED, 16, linespacing=1.6, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=W - 520 - 60, y=60)


TIPOS = {"portada": s_portada, "puntos": s_puntos, "cuenta": s_cuenta, "cascada": s_cascada, "barras": s_barras, "kpis": s_kpis,
         "formula": s_formula, "fin": s_fin}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"{SERIE} · Contenido educativo, no es recomendación de inversión · aiacciones.cl", ACC, 17, 46); band = np.array([0x07, 0x14, 0x29], np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 28, 54, "bold") for l in (textwrap.wrap(s, 70 if len(s) <= 70 else len(s) // 2 + 10) or [s])]
        return SUB[s]

    def ov(fr, j, ts):
        fr = fr.copy(); bh = 46
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0x2F, 0xB7, 0xA3)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); h = 54 * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.25 + band * 0.75).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * 54)
                break
        return fr
    return ov


def frame(i, t):
    e = ESC[i]; a = TIPOS[e["tipo"]](i, e, t)
    return a if e["tipo"] in BIG else with_logo(a, LG, x=W - 250 - 40, y=1080 - 46 - 150)


RECO = ("compra", "comprar", "vende ", "vender", "precio objetivo", "barata", "barato", "cara ", "caro ", "oportunidad", "recomendamos", "te conviene")


def control():
    err = []
    for k in ("base", "capitulo_n", "simbolo", "ticker", "nombre", "tema", "escenas", "info", "miniatura", "publicar"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") not in BIG and not (e.get("fuente") or VJ.get("fuente_general")): err.append(f"escena {k}: sin fuente")
        v = " " + e.get("voz", "").lower() + " "
        for mal in RECO:
            if mal in v and mal not in e.get("permitir", []): err.append(f"escena {k}: palabra de recomendación «{mal.strip()}» en la locución (si es inocua, ponla en \"permitir\")")
    if not any(e.get("tipo") == "fin" for e in ESC): err.append("falta la escena fin")
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    VJ["_cta"] = cta_activa(VJ["publicar"])
    for e, v in zip(ESC, locuciones(VJ)): e["voz"] = v
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(frame(j, 1.0), j, 1.0)).save(os.path.join(AUD, f"prev_{j:02d}_{e.get('id', e['tipo'])}.png"))
        pal = sum(len(e["voz"].split()) for e in ESC); print("palabras", pal, "· duración estimada", round(pal / 2.75 + 1.05 * len(ESC)), "s"); sys.exit()
    VV = [voz_frases(e["voz"]) for e in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [0.25 + len(a) / sr + 0.8 for a, _, _, _ in VV]; durs[-1] += 1.5
    print("voz", motor, "duración prevista", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s")
    leads = [0.25] * len(ESC)
    times, t0 = render([lambda t, j=j: frame(j, t) for j in range(len(ESC))], durs, ([v[0] for v in VV], leads), sr, W, H, 30, OUT,
                       os.path.join(AUD, "cap-silent.mp4"), os.path.join(AUD, "cap.wav"), overlay=overlay([v[2] for v in VV], leads))
    srt([v[2] for v in VV], times, leads, f"{DIR}/subtitulos-{BASE}.srt")
    json.dump([(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/guion-{BASE}.md", "w") as g:
        g.write(f"# {SERIE} · Capítulo {VJ['capitulo_n']}: {VJ['tema']} ({VJ['nombre']}, {VJ['ticker']})\n\nVoz: {motor} · Duración {t0:.0f} s\n\n| Tiempo | Escena | Texto |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
