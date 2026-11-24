# Lección de la serie educativa semanal «Análisis técnico, explicado fácil» (AIAcciones España): un concepto de análisis técnico por vídeo,
# explicado sobre el gráfico real de Inditex, la mayor empresa del IBEX 35 (Daniel, 20-nov-2026). 1920x1080, ~6 minutos,
# voz neuronal es-ES-AlvaroNeural (la del vídeo diario), subtítulos en español, marca del canal.
# Escenas en video.json → "escenas"; tipos: portada, esquema, puntos, grafico, fin. Velas: velas.json de la rama voz-espana-educativo.
# Uso: AUD=<scratch> VELAS=<velas.json> [VOZ_DIR=<mp3 de la voz>] python3 make_leccion.py <carpeta de la lección> [preview]
#   Escribe leccion-<base>.mp4, times.json y guion-<base>.md.
import os, re, sys, json, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_leccion import *
from voz_leccion import cta, CTA_VOZ

DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json")))
W, H = 1920, 1080
MIN_S, MAX_S = 300, 450   # ~6 minutos (5 a 7,5)
# Vídeos fijos para búsquedas habituales (Daniel, 24-nov-2026; espana/fijos/): "formato": "fijo" en video.json.
# Misma marca, voz y subtítulos; otra cabecera, sin capítulo, 3-9 minutos, y escenas extra cifras/tabla/barras.
FIJO = VJ.get("formato") == "fijo"
if FIJO: MIN_S, MAX_S = 180, 540
ETIQ = VJ.get("etiqueta", "Guías de bolsa española") if FIJO else SERIE
BASE = VJ["base"]; OUT = f"{DIR}/{'fijo' if FIJO else 'leccion'}-{BASE}.mp4"; N = VJ.get("capitulo_n", 0)
CTA = cta(VJ)
ESC = [dict(e) for e in VJ["escenas"]]
if CTA: ESC[-1]["voz"] = ESC[-1]["voz"] + " " + CTA_VOZ   # llamada a comentar (solo hasta el 22-nov-2026)
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
SER = VEL["series"][VJ["simbolo"]]
# solo sesiones cerradas hasta "ultima_vela" (la vela del día en curso puede ser intradía)
VELAS = [v for v in SER["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]]; ULT = fecha_v(VELAS[-1]["t"])
IND = indicadores(VELAS); FECHAS = [fecha_v(v["t"]).isoformat() for v in VELAS]
FUENTE_DATOS = SER.get("fuente", "TradingView")
FUENTE = (f"Datos: {FUENTE_DATOS} (velas diarias de {VJ['simbolo']}, hasta el cierre del {fecha_txt(ULT)}). "
          "Medias, indicadores y zonas: calculado por AIAcciones España.")
DEC = VJ.get("decimales", 2)
LG = load_logo(260); LGB = load_logo(440)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]
XL = 0.06
NOMBRES_IND = {"sma": "Media simple de {} sesiones", "ema": "Media exponencial de {} sesiones"}


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="left", **k):
    return f.text(x, y, s, color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def wrap(s, n):
    return "\n".join(partir(s, n))


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def base(i, kicker, title):
    f = fig(W, H)
    T(f, XL, 0.905, kicker.upper(), ACC, 24, "bold")
    T(f, XL, 0.825, title, FG, 42 if len(title) <= 58 else 34, "bold")
    T(f, 0.94, 0.925, f"{ETIQ.upper()} · {MARCA.upper()}" if FIJO else f"{SERIE.upper()} · CAPÍTULO {N}", MUTED, 17, "bold", ha="right")
    T(f, 0.94, 0.89, VJ["tema"], DIM, 16, "bold", ha="right")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n):  # barra de progreso por capítulos
        rect(f, XL + k * w, 0.975, w - 0.008, 0.008, ACC if k < CAP_IDX[i] else DIM)
    return f


def fuente(f, s): T(f, XL, 0.115, wrap(s, 170), MUTED, 14, style="italic", linespacing=1.35)


# ---------- escenas ----------
def s_portada_fijo(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, XL, 0.86, f"{MARCA.upper()} · {ETIQ.upper()}", ACC, 26, "bold", alpha=a)
    rect(f, 0, 0.60, 1.0, 0.21, ACC, a)
    T(f, XL, 0.755, e.get("kicker", "").upper(), BG, 32, "bold", va="center", alpha=a)
    T(f, XL, 0.66, VJ["tema"], BG, 72 if len(VJ["tema"]) <= 30 else 54, "bold", va="center", alpha=a)
    if e.get("respuesta"): T(f, XL, 0.50, wrap(e["respuesta"], 80), FG, 32, "bold", alpha=ease((t - 0.15) / 0.5), va="top", linespacing=1.3)
    if e.get("sub"): T(f, XL, 0.37, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    T(f, XL, 0.28, "Contenido informativo y educativo · no es una recomendación de inversión", ACC2, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=W - 440 - 90, y=50)


def s_cifras(i, e, t):
    """Hasta 4 cifras grandes: [valor, etiqueta, color], con nota y fuente."""
    f = base(i, e["kicker"], e["titulo"]); C = e["cifras"][:4]; w = 0.88 / len(C)
    for k, (v, lab, c) in enumerate(C):
        b = ease((t - k * 0.12) / 0.4); x = XL + k * w
        rect(f, x, 0.36, w - 0.02, 0.36, PANEL, b)
        T(f, x + 0.02, 0.58, v, c, (64 if len(v) <= 8 else 48) if len(C) < 4 else (50 if len(v) <= 7 else 40), "bold", alpha=b)
        T(f, x + 0.02, 0.50, wrap(lab, int(w * 120)), FG, 22, alpha=b, va="top", linespacing=1.3)
    if e.get("nota"): T(f, XL, 0.28, wrap(e["nota"], 120), NEG, 22, "bold", alpha=ease((t - 0.4) / 0.4), va="top")
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def s_tabla(i, e, t):
    """Tabla: "columnas" (cabecera) y "filas" (listas de textos). "destacar": índice de fila; "anchos": fracciones."""
    f = base(i, e["kicker"], e["titulo"]); cols = e["columnas"]; F = e["filas"][:9]
    an = e.get("anchos") or [1 / len(cols)] * len(cols); xs = [XL + 0.88 * sum(an[:k]) for k in range(len(cols))]
    hh = min(0.065, 0.56 / (len(F) + 1)); y = 0.74 - hh
    rect(f, XL, y, 0.88, hh - 0.006, ACC)
    for x, c in zip(xs, cols): T(f, x + 0.008, y + hh / 2 - 0.003, c, BG, 21, "bold", va="center")
    for r, fila in enumerate(F):
        b = ease((t - r * 0.06) / 0.35); y -= hh
        rect(f, XL, y, 0.88, hh - 0.006, ACC2 if e.get("destacar") == r else PANEL, 0.35 * b if e.get("destacar") == r else b)
        for k, (x, v) in enumerate(zip(xs, fila)):
            T(f, x + 0.008, y + hh / 2 - 0.003, str(v), FG if k == 0 else MUTED, 21, "bold" if k == 0 else "normal", va="center", alpha=b)
    if e.get("nota"): T(f, XL, y - 0.05, wrap(e["nota"], 150), NEG, 19, "bold", alpha=ease((t - 0.4) / 0.4), va="top")
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def s_barras(i, e, t):
    """Barras horizontales: "barras" [[etiqueta, valor]], "formato" (p. ej. "{:.1f} %"), "destacar" (etiqueta)."""
    f = base(i, e["kicker"], e["titulo"]); B = e["barras"][:10]
    ax = f.add_axes([XL + 0.2, 0.2, 0.62, 0.53]); clean(ax); ax.set_xticks([])
    vals = [v for _, v in B]; ys = np.arange(len(B))[::-1]; a = ease(t / 0.6); m = max(abs(v) for v in vals) or 1
    colores = [col(e.get("color_destacado", "neg")) if lab == e.get("destacar") else col(e.get("color", "acc")) for lab, _ in B]
    ax.barh(ys, [v * a for v in vals], color=colores, height=0.62)
    ax.set_yticks(ys, [lab for lab, _ in B]); ax.tick_params(colors=FG, labelsize=21, length=0)
    ax.set_xlim(min(0, min(vals)) * 1.3, m * 1.3)
    fmt = e.get("formato", "{:.1f}")
    if t >= 0.5:
        for y_, v in zip(ys, vals): ax.text(v * a + m * 0.02, y_, fmt.format(v).replace(",", "X").replace(".", ",").replace("X", "."), va="center", color=FG, fontsize=20, weight="bold")
    if e.get("nota"): T(f, XL, 0.16, wrap(e["nota"], 150), NEG, 19, "bold", alpha=ease((t - 0.4) / 0.4))
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def s_portada(i, e, t):
    if FIJO: return s_portada_fijo(i, e, t)
    f = fig(W, H); a = ease(t / 0.6)
    T(f, XL, 0.86, f"{MARCA.upper()} · NUEVA SERIE CADA DOMINGO", ACC, 26, "bold", alpha=a)
    rect(f, 0, 0.60, 1.0, 0.21, ACC, a)
    T(f, XL, 0.755, f"«{SERIE.upper()}» · CAPÍTULO {N}", BG, 32, "bold", va="center", alpha=a)
    T(f, XL, 0.66, VJ["tema"], BG, 72 if len(VJ["tema"]) <= 26 else 56, "bold", va="center", alpha=a)
    T(f, XL, 0.50, f"Explicado sobre el gráfico real de {VJ['nombre']} ({VJ['ticker']}), la mayor empresa del IBEX 35", FG, 32, "bold",
      alpha=ease((t - 0.15) / 0.5))
    if e.get("sub"): T(f, XL, 0.43, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    T(f, XL, 0.30, "Contenido educativo · no es una recomendación de inversión", ACC2, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=W - 440 - 90, y=50)


def s_puntos(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); P = e["puntos"][:5]; hh = min(0.12, 0.6 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.68 - (k + 1) * hh; ym = y + (hh - 0.014) / 2
        rect(f, XL, y, 0.88, hh - 0.014, PANEL, b); rect(f, XL, y, 0.005, hh - 0.014, e.get("colores", [ACC] * 5)[k], b)
        T(f, XL + 0.018, ym, f"{k + 1}", ACC, 34, "bold", va="center", alpha=b)
        T(f, XL + 0.05, ym, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, XL + 0.32, ym, wrap(txt, 74), MUTED, 21, va="center", alpha=b, linespacing=1.3)
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def _zigzag(modo):
    """Recorrido de precio esquemático (no son datos reales)."""
    P = {"sr": [(0, 40), (8, 78), (15, 32), (24, 80), (31, 30), (40, 79), (47, 33), (55, 70)],
         "cambio_rol": [(0, 30), (8, 58), (14, 36), (22, 60), (28, 40), (36, 82), (42, 62), (48, 61), (56, 92)],
         "cambio_rol_baja": [(0, 70), (8, 42), (14, 64), (22, 40), (28, 60), (36, 18), (42, 38), (48, 39), (56, 8)],
         "falsa_ruptura": [(0, 40), (8, 76), (15, 35), (24, 79), (30, 50), (37, 86), (41, 72), (48, 45), (56, 38)],
         "media": [(0, 30), (10, 48), (16, 40), (26, 68), (32, 58), (40, 80), (46, 70), (56, 74)],
         "cruces": [(0, 75), (12, 60), (22, 34), (30, 28), (38, 44), (48, 72), (56, 84)]}[modo]
    x = np.arange(0, 57, 0.5); y = np.interp(x, [p[0] for p in P], [p[1] for p in P])
    rng = np.random.default_rng(7); return x, y + rng.normal(0, 2.2 if modo in ("media", "cruces") else 1.4, len(x))


def s_esquema(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); modo = e.get("modo", "sr")
    ax = f.add_axes([XL, 0.25, 0.55, 0.52]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
    x, y = _zigzag(modo); n = max(2, int(len(x) * min(1, ease(t * 1.2)))); ax.set_xlim(-1, 58)
    ax.set_ylim(0, 100) if modo == "cambio_rol_baja" else ax.set_ylim(15, 100)
    za = ease((t - 0.3) / 0.4); lab = lambda xx, yy, s, c, ha="left", a=za: ax.text(xx, yy, s, color=c, fontsize=22, weight="bold", ha=ha, alpha=a)
    if modo == "sr":
        ax.axhspan(76, 82, color=NEG, alpha=0.25 * za); ax.axhspan(28, 34, color=ACC, alpha=0.25 * za)
        lab(1, 85, "Resistencia", NEG); lab(1, 20, "Soporte", ACC)
    elif modo == "cambio_rol":
        ax.axhspan(57, 63, color=NEG, alpha=0.28 * za)
        lab(1, 66, "Primero resistencia…", NEG); lab(57, 50, "…después soporte", ACC, "right", ease((t - 0.6) / 0.3))
    elif modo == "cambio_rol_baja":
        ax.axhspan(37, 43, color=NEG, alpha=0.28 * za)
        lab(1, 30, "Primero soporte…", ACC); lab(57, 47, "…después resistencia", NEG, "right", ease((t - 0.6) / 0.3))
    elif modo == "falsa_ruptura":
        ax.axhspan(76, 81, color=NEG, alpha=0.25 * za); lab(1, 84, "Resistencia", NEG)
        ax.annotate("Falsa ruptura", (37, 86), (44, 95), color=ACC2, fontsize=22, weight="bold", alpha=ease((t - 0.6) / 0.3),
                    arrowprops=dict(arrowstyle="->", color=ACC2, lw=2, alpha=ease((t - 0.6) / 0.3)))
    elif modo == "media":  # la media suaviza el precio y va por detrás
        k = 16; m = np.array([y[max(0, j - k + 1):j + 1].mean() for j in range(len(y))])
        ax.plot(x[:n], m[:n], color=ACC2, lw=4.5, alpha=za)
        lab(1, 92, "Precio (con su «ruido» diario)", FG); lab(57, 22, "Media móvil: más suave, va por detrás", ACC2, "right")
    elif modo == "cruces":  # media rápida y media lenta
        m1 = np.array([y[max(0, j - 10 + 1):j + 1].mean() for j in range(len(y))]); m2 = np.array([y[max(0, j - 40 + 1):j + 1].mean() for j in range(len(y))])
        ax.plot(x[:n], m1[:n], color=ACC2, lw=4, alpha=za); ax.plot(x[:n], m2[:n], color=PUR, lw=4, alpha=za)
        cr = [j for j in range(20, len(x)) if (m1[j] - m2[j]) * (m1[j - 1] - m2[j - 1]) < 0]
        for j in cr:
            if j < n: ax.plot([x[j]], [m1[j]], "o", ms=18, mfc="none", mec=NEG, mew=3, alpha=ease((t - 0.6) / 0.3))
        lab(1, 92, "Media rápida", ACC2); lab(1, 84, "Media lenta", PUR)
    ax.plot(x[:n], y[:n], color=FG, lw=2.6 if modo in ("media", "cruces") else 3.2, alpha=0.75 if modo in ("media", "cruces") else 1)
    T(f, XL, 0.215, "Esquema ilustrativo: no son datos reales de cotización", MUTED, 17, "bold")
    for k, s in enumerate(e.get("notas", [])[:4]):
        b = ease((t - 0.2 - k * 0.12) / 0.4); yy = 0.70 - k * 0.135
        rect(f, 0.64, yy - 0.05, 0.30, 0.115, PANEL, b); rect(f, 0.64, yy - 0.05, 0.004, 0.115, ACC, b)
        T(f, 0.655, yy + 0.008, wrap(s, 30), FG, 21, "bold", va="center", alpha=b, linespacing=1.15)
    return to_arr(f)


def _rango(e):
    d0 = e.get("desde", "0000"); d1 = e.get("hasta", ULT.isoformat())
    return [j for j, f in enumerate(FECHAS) if d0 <= f <= d1]


def nombre_ind(k):
    for p, s in NOMBRES_IND.items():
        if k.startswith(p) and k[len(p):].isdigit(): return s.format(k[len(p):])
    return k


def s_grafico(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); J = _rango(e); n = len(J); V = [VELAS[j] for j in J]
    panel = e.get("panel", "volumen")
    ax = f.add_axes([XL, 0.36 if panel else 0.24, 0.79, 0.41 if panel else 0.53]); clean(ax)
    rev = n if not e.get("animar_velas") else max(2, int(n * ease(t * 1.15)))
    o = np.array([v["o"] for v in V]); hi = np.array([v["h"] for v in V]); lo = np.array([v["l"] for v in V]); c = np.array([v["c"] for v in V])
    up = c >= o; xs = np.arange(n); wd = 0.65 if n < 160 else 0.75
    LIN = [(l, IND[l["ind"]][J]) for l in e.get("lineas", [])]
    ymin, ymax = lo.min(), hi.max()
    for _, s in LIN: ymin = min(ymin, np.nanmin(s)); ymax = max(ymax, np.nanmax(s))
    if e.get("bollinger"): ymin = min(ymin, np.nanmin(IND["boll_i"][J])); ymax = max(ymax, np.nanmax(IND["boll_s"][J]))
    for z in e.get("zonas", []): ymin = min(ymin, z["de"]); ymax = max(ymax, z["a"])
    pad = (ymax - ymin) * 0.08
    suelo = any(m.get("tipo", "suelo") == "suelo" for m in e.get("marcas", []))
    ax.set_ylim(ymin - pad * (2.6 if suelo else 1.6), ymax + pad * 1.8); ax.set_xlim(-1, n + (n * 0.22))
    cc = [ACC if u else NEG for u in up]
    if e.get("linea_precio"):
        ax.plot(xs[:rev], c[:rev], color=FG, lw=1.8, alpha=0.85)
    else:
        ax.vlines(xs[:rev], lo[:rev], hi[:rev], color=cc[:rev], lw=1.0 if n > 160 else 1.5, alpha=0.8 if LIN else 1)
        ax.bar(xs[:rev], np.maximum(np.abs(c - o), (ymax - ymin) * 0.002)[:rev], bottom=np.minimum(o, c)[:rev], width=wd, color=cc[:rev], alpha=0.8 if LIN else 1)
    la = ease((t - 0.15) / 0.4)
    if e.get("bollinger"):
        ax.fill_between(xs[:rev], IND["boll_i"][J][:rev], IND["boll_s"][J][:rev], color=ACC2, alpha=0.12 * la, lw=0)
        for k_ in ("boll_s", "boll_m", "boll_i"): ax.plot(xs[:rev], IND[k_][J][:rev], color=ACC2, lw=1.6, alpha=0.9 * la, ls="--" if k_ == "boll_m" else "-")
    etiquetas = []
    for l, s in LIN:
        cl = col(l.get("color", "acc2")); ax.plot(xs[:rev], s[:rev], color=cl, lw=3.2, alpha=la)
        if rev == n and not np.isnan(s[-1]): etiquetas.append([s[-1], f"{l.get('texto', nombre_ind(l['ind']))}: {num(s[-1], DEC)}", cl])
    if e.get("ultimo", True) and rev == n: etiquetas.append([c[-1], f"Cierre: {num(c[-1], DEC)}", FG])
    etiquetas.sort(key=lambda x: x[0]); gap = (ymax - ymin + 3 * pad) * 0.075   # que no se pisen
    for k in range(1, len(etiquetas)):
        if etiquetas[k][0] - etiquetas[k - 1][0] < gap: etiquetas[k][0] = etiquetas[k - 1][0] + gap
    for yv, s, cl in etiquetas:
        ax.text(n + 1.5, yv, s, color=BG if cl == FG else cl, fontsize=16, weight="bold", va="center", alpha=la,
                bbox=dict(boxstyle="round,pad=0.25", fc=FG if cl == FG else BG, ec="none", alpha=0.9 * la))
    for k, z in enumerate(e.get("zonas", [])):
        a = ease((t - 0.25 - k * 0.12) / 0.35); zc = col(z.get("color", "neg"))
        ax.axhspan(z["de"], z["a"], color=zc, alpha=0.22 * a, lw=0)
        ax.text(1, z["a"], f"{z['texto']} ({num(z['de'], DEC)}–{num(z['a'], DEC)})", color=zc, fontsize=16, weight="bold", va="bottom", alpha=a)
    idx = {FECHAS[j]: k for k, j in enumerate(J)}
    for k, m in enumerate(e.get("marcas", [])):
        j = idx.get(m["fecha"])
        if j is None: continue
        a = ease((t - 0.45 - k * 0.07) / 0.3); tipo = m.get("tipo", "suelo")
        if tipo == "cruce":
            yv = LIN[0][1][j] if LIN else c[j]
            ax.plot([j], [yv], "o", ms=24, mfc="none", mec=NEG, mew=3.5, alpha=a)
            ax.text(j, yv + (ymax - ymin) * (0.13 if m.get("arriba", True) else -0.13), m.get("texto", ""), color=NEG, fontsize=17, weight="bold",
                    ha="center", va="center", alpha=a, linespacing=1.1, bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec="none", alpha=0.85 * a))
            continue
        arriba = tipo == "techo"; yv = hi[j] if arriba else lo[j]; off = (ymax - ymin) * (0.07 if arriba else -0.07)
        ax.plot([j], [yv + off * 0.35], marker="v" if arriba else "^", color=NEG, ms=15, alpha=a)
        if m.get("texto"): ax.text(j, yv + off * (2.0 if arriba else 1.6), m["texto"], color=NEG, fontsize=16, weight="bold", ha="center", va="center", alpha=a, linespacing=1.1)
    if e.get("tramo"):  # tramo sombreado entre dos fechas (p. ej. «mercado lateral»)
        d0, d1, txt = e["tramo"]; j0 = min((k for f_, k in idx.items() if f_ >= d0), default=0); j1 = max((k for f_, k in idx.items() if f_ <= d1), default=n - 1)
        ax.axvspan(j0, j1, color=PUR, alpha=0.12 * la, lw=0); ax.text((j0 + j1) / 2, ymax + pad * 1.2, txt, color=PUR, fontsize=17, weight="bold", ha="center", alpha=la)
    ax.yaxis.tick_left(); ax.tick_params(labelsize=15)
    ydec = 0 if (ymax - ymin) > 8 else 1
    ax.set_yticks(ax.get_yticks()[1:-1]); ax.set_yticklabels([num(y, ydec) for y in ax.get_yticks()])
    ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk, prev = [], None
    for k, j in enumerate(J):
        d = dt.date.fromisoformat(FECHAS[j])
        if d.month != prev: tk.append((k, MESES[d.month - 1] + (f"\n{d.year}" if d.month == 1 or not tk else ""))); prev = d.month
    step = 1 if len(tk) <= 13 else 2
    ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]] if not panel else [])
    if panel:
        av = f.add_axes([XL, 0.225, 0.79, 0.12]); clean(av); av.set_xlim(ax.get_xlim())
        if panel == "volumen":
            vv = IND["vol"][J] / 1e6
            av.bar(xs[:rev], vv[:rev], color=cc[:rev], width=wd, alpha=0.55); av.set_yticks([]); av.set_ylim(0, vv.max() * 1.1)
            if e.get("volumen_media"): av.plot(xs[:rev], IND["vol_m20"][J][:rev] / 1e6, color=FG, lw=1.8)
            nombre = "Volumen (acciones)" + (" y su media de 20 sesiones" if e.get("volumen_media") else "")
        elif panel == "rsi":
            r = IND["rsi"][J]; av.plot(xs[:rev], r[:rev], color=PUR, lw=2); av.set_ylim(0, 100)
            for lv in (30, 70): av.axhline(lv, color=MUTED, lw=1, ls="--")
            av.axhspan(70, 100, color=NEG, alpha=0.08); av.axhspan(0, 30, color=ACC, alpha=0.08); av.set_yticks([30, 70]); nombre = "RSI de 14 sesiones"
        elif panel == "macd":
            av.bar(xs[:rev], IND["hist"][J][:rev], color=[ACC if h_ >= 0 else NEG for h_ in IND["hist"][J][:rev]], width=wd, alpha=0.6)
            av.plot(xs[:rev], IND["macd"][J][:rev], color=ACC2, lw=2); av.plot(xs[:rev], IND["senal"][J][:rev], color=NEG, lw=2); av.axhline(0, color=DIM, lw=1)
            av.set_yticks([]); nombre = "MACD (12, 26, 9): línea MACD, señal e histograma"
        elif panel == "estocastico":
            av.plot(xs[:rev], IND["stoch_k"][J][:rev], color=ACC2, lw=2); av.plot(xs[:rev], IND["stoch_d"][J][:rev], color=NEG, lw=1.6)
            for lv in (20, 80): av.axhline(lv, color=MUTED, lw=1, ls="--")
            av.set_ylim(0, 100); av.set_yticks([20, 80]); nombre = "Estocástico (14, 3, 3): %K y %D"
        av.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]]); av.tick_params(labelsize=15)
        T(f, XL, 0.347, nombre, MUTED, 15)
    T(f, XL, 0.785, f"{VJ['nombre']} ({VJ['ticker']}) · velas diarias · euros por acción", MUTED, 19, "bold")
    if e.get("nota"):
        b = ease((t - 0.5) / 0.4); T(f, 0.94, 0.785, e["nota"], NEG, 21, "bold", ha="right", alpha=b)
    fuente(f, FUENTE)
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XL, 0.86, VJ["tema"] if FIJO else f"Capítulo {N}: {VJ['tema']}", FG, 44, "bold", alpha=a)
    T(f, XL, 0.795, "LO ESENCIAL", ACC, 30, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, XL, 0.725 - k * 0.062, "• " + c, FG, 26, alpha=ease((t - 0.1 - k * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    if e.get("siguiente"): T(f, XL, 0.45, "Próximo capítulo: " + e["siguiente"], ACC2, 28, "bold", alpha=b)
    if CTA: T(f, XL, 0.395, "💬 Déjanos tu comentario · 🔔 suscríbete al canal".replace("💬 ", "").replace("🔔 ", ""), NEG, 25, "bold", alpha=b)
    else: T(f, XL, 0.395, "Suscríbete al canal · el IBEX 35 cada día de bolsa" if FIJO else "Suscríbete al canal · un capítulo nuevo cada domingo", NEG, 25, "bold", alpha=b)
    aviso = ("AVISO: contenido informativo y educativo. No es una recomendación de inversión, ni una invitación a comprar o vender valores, "
             "ni asesoramiento personalizado. Las cifras proceden de las fuentes citadas en pantalla; los cálculos propios están marcados como "
             "calculado. Las rentabilidades pasadas no garantizan las futuras. AIAcciones España no tiene posiciones en los valores citados. "
             "Invertir conlleva riesgo de pérdida, incluso de todo el capital. "
             "Guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial.") if FIJO else ("AVISO: contenido educativo e informativo. No es una recomendación de inversión, ni una invitación a comprar o vender valores, "
             f"ni asesoramiento personalizado. {VJ['nombre']} es solo un ejemplo. El análisis técnico describe el comportamiento pasado del precio y no "
             f"predice el futuro; las zonas dibujadas no son precios objetivo. Datos: {FUENTE_DATOS}; medias, indicadores y zonas: calculado. "
             "AIAcciones España no tiene posiciones en el valor citado. Invertir conlleva riesgo de pérdida, incluso de todo el capital. "
             "Guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial.")
    T(f, XL, 0.32, wrap(aviso, 150), MUTED, 16, linespacing=1.6, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=W - 440 - 90, y=50)


TIPOS = {"portada": s_portada, "puntos": s_puntos, "esquema": s_esquema, "grafico": s_grafico, "fin": s_fin,
         "cifras": s_cifras, "tabla": s_tabla, "barras": s_barras}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"{MARCA} · {ETIQ if FIJO else '«' + SERIE + '»'} · contenido {'informativo' if FIJO else 'educativo'}, no es una recomendación de inversión", MUTED, 17, 44, "normal")
    band = np.array(BANDA, np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 30, 56, "bold") for l in (partir(s, 70) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        fr = fr.copy(); bh = 44
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0x2F, 0xB7, 0xA3)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = 56; h = lh * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.25 + np.array([5, 14, 30], np.float32) * 0.75).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * lh)
                break
        return fr
    return ov


def frame(i, t):
    e = ESC[i]; a = TIPOS[e["tipo"]](i, e, t)
    return a if e["tipo"] in BIG else with_logo(a, LG, x=W - 260 - 40, y=H - 82 - 128)


PROHIBIDAS = (r"compr\w*", r"vend\w*", "precio objetivo", "barat[ao]s?", "car[ao]s?", "subirá", "bajará", "recomend\\w*", "oportunidad\\w*")
NEGADAS = r"no (es )?(una )?recomendación( de inversión)?|ni una invitación a comprar o vender"


def control():
    err = []
    for k in ("base", "simbolo", "tema", "escenas", "info", "miniatura", "short", "ultima_vela") + (() if FIJO else ("capitulo_n", "ticker", "nombre")):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") == "grafico":
            J = _rango(e)
            if len(J) < 20: err.append(f"escena {k}: menos de 20 velas en el rango")
            fechas = {FECHAS[j] for j in J}
            for m in e.get("marcas", []):
                if m["fecha"] not in fechas: err.append(f"escena {k}: marca {m['fecha']} sin vela")
            for l in e.get("lineas", []):
                try: IND[l["ind"]]
                except KeyError: err.append(f"escena {k}: indicador desconocido {l['ind']}")
    if VJ.get("ultima_vela") and VJ["ultima_vela"] != ULT.isoformat(): err.append(f"velas.json acaba el {ULT}, video.json espera {VJ['ultima_vela']}")
    for e in ESC + VJ.get("short", []):
        v = re.sub(NEGADAS, "", e.get("voz", "").lower())
        for p in PROHIBIDAS:
            if re.search(r"\b" + p + r"\b", v):
                err.append(f"escena {e.get('id')}: revisa «{p}» (las zonas van como condiciones, nunca como recomendación)")
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(frame(j, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"prev_{j:02d}_{e.get('id', e['tipo'])}.png"))
        print("palabras", sum(len(e["voz"].split()) for e in ESC)); sys.exit()
    VV = [voz_frases(e["voz"], AUD) for e in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas: " + str([v[3] for v in VV]))
    durs = [0.15 + len(a) / sr + 0.7 for a, _, _, _ in VV]; durs[-1] += 1.5
    print("voz", motor, "duración prevista", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s")
    leads = [0.15] * len(ESC)
    times, t0 = render([lambda t, j=j: frame(j, t) for j in range(len(ESC))], durs, ([v[0] for v in VV], leads), sr, W, H, 30, OUT,
                       os.path.join(AUD, "lec-silent.mp4"), os.path.join(AUD, "lec.wav"), overlay=overlay([v[2] for v in VV], leads))
    json.dump([(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/guion-{BASE}.md", "w") as g:
        g.write(f"# {VJ['tema']} ({ETIQ})" if FIJO else f"# {SERIE} · Capítulo {N}: {VJ['tema']} ({VJ['nombre']}, {VJ['ticker']})")
        g.write(f"\n\nVoz: {motor} · Duración {t0:.0f} s\n\n| Tiempo | Escena | Texto |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
