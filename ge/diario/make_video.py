# Vídeo diario largo (8-10 min) en alemán de Wall Street para Wall Street auf Deutsch (portado de nabd/diario/make_video.py):
# 8 secciones (Einstieg, die großen Indizes, Sektoren, fünf Aktien, Makro, Charttechnik mit Szenarien, Termine und Fazit mit Telegram),
# ticker inferior con cotizaciones y titulares, y subtítulos alemanes frase a frase. 1080p, de izquierda a derecha, logo arriba a la derecha.
# Voz: Azure de-DE-ConradNeural si VOZ_DIR tiene sus wav (voz-GE.yml); si no, Piper de_DE-thorsten.
# Uso: AUD=<scratch> [VOZ_DIR=<wav de Azure>] python3 make_video.py <carpeta del día> [preview]
#   La carpeta del día tiene mercado.json y video.json (ver ejemplo-2026-11-09/). Escribe video-bolsa-<fecha>-GE.mp4, times.json,
#   guion-<fecha>-GE.md (guion en tabla: tiempo, narración, visual, datos) y datos-<fecha>-GE.csv (datos usados, con fuente y hora).
import os, sys, json, re, csv, textwrap, numpy as np, datetime as dt
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
from comun import _de
from tecnico import calc, accion, INDICE, INDICE_CORTO, MESES, DIAS, TZ, BERLIN, EUROPA, fecha_de
DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
W, H, FPS = 1920, 1080, 30
AUD = os.environ.get("AUD", "aud")
MIN_S, MAX_S = 450, 630   # duración: entre 7:30 y 10:30 (objetivo 8-10 minutos)
M = json.load(open(f"{DIR}/mercado.json")); VJ = json.load(open(f"{DIR}/video.json"))
R, A = calc(M, VJ.get("nombres")); NYZ = ZoneInfo("America/New_York"); FECHA = dt.date.fromisoformat(R["fecha"]); FECHA_TXT = fecha_de(FECHA)
OUT = f"{DIR}/video-bolsa-{R['fecha']}-GE.mp4"
SECS = ["Einstieg", "Die großen Indizes", "Sektoren", "Aktien des Tages", "Makro", "Charttechnik", "Was morgen ansteht", "Fazit"]; NS = len(SECS)
LG = load_logo(130); LGS = load_logo(95); LGB = load_logo(230)
NB = 126  # unos 6 meses de sesiones
TV_TXT = "TradingView"
NAVY = "#13294B"


corto = lambda d: f"{d.day}. {MESES[d.month - 1][:3]}." if len(MESES[d.month - 1]) > 4 else f"{d.day}. {MESES[d.month - 1]}"
fiso = lambda s: re.sub(r"(\d{4})-(\d{2})-(\d{2})", lambda m: corto(dt.date(int(m[1]), int(m[2]), int(m[3]))) + (f" {m[1]}" if int(m[1]) != FECHA.year else ""), s)
cc_ = lambda v: TEAL if (v or 0) >= 0 else NEG
pts = lambda v, d=2: _de(f"{v:+,.{d}f}")   # +173,08 (puntos con signo, formato alemán)


def millones(v):
    if v is None: return "—"
    return f"{num(v / 1e9, 2)} Mrd." if v >= 1e9 else f"{num(v / 1e6, 1)} Mio."


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="left", **k):
    return f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)


def base_fig(n, kicker, title, sub):
    f = fig(W, H)
    T(f, 0.06, 0.905, kicker, GOLD, 24, "bold")
    T(f, 0.06, 0.82, title, FG, 42 if len(title) <= 55 else 34, "bold")
    T(f, 0.895, 0.925, f"{n}/{NS} · {SECS[n - 1]}", MUTED, 19, "bold", ha="right")
    T(f, 0.895, 0.89, MARCA + " · " + PROGRAMA + " · " + FECHA_TXT, DIM, 16, "bold", ha="right")
    w = 0.88 / NS
    for i in range(NS):  # barra de progreso de izquierda a derecha
        f.patches.append(plt.Rectangle((0.06 + i * w, 0.975), w - 0.008, 0.008, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))
    T(f, 0.06, 0.172, "\n".join(textwrap.wrap(sub, 175)), MUTED, 14, linespacing=1.35)
    return f


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=c, alpha=a, figure=f))


def hbars(f, box, labels, vals, colors, fmt=pct, e=1.0, fs=19, extra=None):
    """Barras horizontales (etiquetas a la izquierda del eje, texto extra a la derecha). extra: texto pequeño junto a cada valor."""
    ax = f.add_axes(box); clean(ax); y = np.arange(len(vals))[::-1]
    lim = max(abs(min(vals + [0])), abs(max(vals + [0]))) * 1.9 or 1
    ax.barh(y, [v * e for v in vals], color=colors, height=0.62)
    ax.set_yticks([]); ax.set_xticks([]); ax.axvline(0, color=DIM, lw=1.5)
    ax.set_xlim(-lim if min(vals) < 0 else -lim * 0.3, lim if max(vals) > 0 else lim * 0.3); ax.set_ylim(-0.7, len(vals) - 0.3)
    for i, (yy, v) in enumerate(zip(y, vals)):
        ax.text(-0.01, yy, ar(labels[i]), transform=ax.get_yaxis_transform(), ha="right", va="center", color=FG, fontsize=fs, weight="bold")
        if e > 0.6:
            ax.text(v * e + (lim * 0.03 if v >= 0 else -lim * 0.03), yy, fmt(v), va="center",
                    ha="left" if v >= 0 else "right", color=FG, fontsize=fs - 2, weight="bold")
            if extra and extra[i]:
                ax.text(1.02, yy, ar(extra[i]), transform=ax.get_yaxis_transform(), ha="left", va="center", color=MUTED, fontsize=fs - 4)
    return ax


# ---------- 1. Einstieg ----------
def s_title(t):
    f = fig(W, H); a = ease(t / 0.6); r = R["spx"]; cc = cc_(r["var_pct"])
    T(f, 0.06, 0.895, MARCA + " · " + PROGRAMA, GOLD, 28, "bold", alpha=a)
    rect(f, 0, 0.71, 1.0, 0.135, GOLD, a)
    T(f, 0.06, 0.775, "Handelstag " + FECHA_TXT, BG, 60, "bold", va="center", alpha=a)
    T(f, 0.06, 0.625, INDICE["spx"], MUTED, 30, "bold", alpha=a)
    f.text(0.06, 0.52, num(r["cierre"]), color=FG, fontsize=86, weight="bold", ha="left", alpha=a)
    f.text(0.06, 0.45, f"{pct(r['var_pct'])}   ({pts(r['var_pts'])} Punkte)", color=cc, fontsize=36, weight="bold", ha="left", alpha=a)
    for i, k in enumerate(("ndx", "dji", "rut")):
        if k not in R: continue
        b = ease((t - 0.15 - i * 0.1) / 0.5); x_ = R[k]; y = 0.375 - i * 0.055
        T(f, 0.06, y, INDICE_CORTO[k], MUTED, 25, "bold", alpha=b)
        f.text(0.21, y, f"{num(x_['cierre'])}   {pct(x_['var_pct'])}", color=cc_(x_["var_pct"]), fontsize=26, weight="bold", ha="left", alpha=b)
    I = [v for v in M.get("spx_intradia", {}).get("velas", []) if dt.datetime.fromtimestamp(v["t"], NYZ).date() == FECHA]
    I = [v for v in I if dt.time(9, 30) <= dt.datetime.fromtimestamp(v["t"], NYZ).time() < dt.time(16, 0)]
    IC = np.array([v["c"] for v in I]); prev = r["anterior"]
    if len(IC) > 2:
        IC = np.append(IC, r["cierre"])
        ax = f.add_axes([0.47, 0.29, 0.48, 0.33]); clean(ax)
        n = max(2, int(len(IC) * ease(t))); x = np.arange(len(IC))
        ax.plot(x[:n], IC[:n], color=cc, lw=3.5); ax.axhline(prev, color=DIM, lw=1.5, ls="--")
        ax.fill_between(x[:n], IC[:n], prev, color=cc, alpha=0.12)
        pad = (max(IC.max(), prev) - min(IC.min(), prev)) * 0.15
        ax.set_xlim(0, len(IC) - 1); ax.set_ylim(min(IC.min(), prev) - pad, max(IC.max(), prev) + pad); ax.set_yticks([])
        hrs = [dt.datetime.fromtimestamp(v["t"], TZ) for v in I]; tk = [j for j, h in enumerate(hrs) if h.minute == 30]
        ax.set_xticks(tk, [hrs[j].strftime("%H:%M") for j in tk]); ax.tick_params(labelsize=15)
        T(f, 0.47, 0.635, "S&P 500 im Tagesverlauf (5-Minuten-Kerzen, deutsche Zeit)", MUTED, 18)
        T(f, 0.95, 0.245, "Gestrichelte Linie: Vortagesschluss " + num(prev), MUTED, 16, ha="right")
    if VJ.get("titular"): T(f, 0.06, 0.18, VJ["titular"], BLUE, 29, "bold", alpha=ease((t - 0.3) / 0.5))
    return with_logo(to_arr(f), LG, x=W - 130 - 60, y=40)


# ---------- 2. Die großen Indizes ----------
def s_indices(t):
    J = VJ.get("indices", {})
    f = base_fig(2, "Die großen Indizes: Schluss und Entwicklung", J.get("titulo", "So schlossen die US-Indizes"),
                 J.get("fuente", f"Kurse: {TV_TXT} (Schluss {fiso(R['fecha'])} in New York). Wochenveränderung, Abstand zum Hoch, zur 200-Tage-Linie und Trend: berechnet. "
                       "Der Trend beschreibt die Lage des Kurses zu den 20-, 50- und 200-Tage-Linien und ist keine Prognose."))
    cols = [(0.27, "Schluss"), (0.38, "Tag"), (0.48, "Woche"), (0.595, "zum Hoch"), (0.71, "zur 200-T.-Linie"), (0.85, "Trend")]
    T(f, 0.06, 0.70, "Index", MUTED, 20, "bold")
    for x, h in cols: T(f, x, 0.70, h, MUTED, 20, "bold", ha="center")
    rect(f, 0.05, 0.685, 0.90, 0.003, GOLD)
    for i, k in enumerate(("spx", "ndx", "dji", "rut")):
        if k not in R: continue
        b = ease((t - i * 0.12) / 0.4)
        if b <= 0: continue
        r = R[k]; y = 0.605 - i * 0.1
        if i % 2 == 0: rect(f, 0.05, y - 0.04, 0.90, 0.088, NAVY, 0.55 * b)
        T(f, 0.06, y, INDICE_CORTO[k], GOLD if k != "rut" else FG, 27, "bold", va="center", alpha=b)
        vals = [(num(r["cierre"]), FG), (pct(r["var_pct"]), cc_(r["var_pct"])),
                ("—" if r.get("semana_pct") is None else pct(r["semana_pct"]), cc_(r.get("semana_pct"))),
                (pct(r["dist_max_hist_pct"]), cc_(r["dist_max_hist_pct"]) if r["dist_max_hist_pct"] < -0.05 else TEAL),
                (pct(r["dist_sma200_pct"], 1), cc_(r["dist_sma200_pct"]))]
        for (x, _), (v, c) in zip(cols, vals): f.text(x, y + 0.008, v, color=c, fontsize=25, weight="bold", ha="center", va="center", alpha=b)
        T(f, cols[3][0], y - 0.03, ("Allzeithoch " if r["max_hist_es_historico"] else "Hoch seit " + r["historia_desde"][:4] + " · ") + fiso(r["max_hist_fecha"]),
          MUTED, 13, ha="center", va="center", alpha=b)
        tc = TEAL if r["tendencia"].startswith("Aufwärts") else (GOLD if r["tendencia"] == "Seitwärts" else NEG)
        T(f, cols[5][0], y, r["tendencia"], tc, 18 if len(r["tendencia"]) > 16 else 21, "bold", ha="center", va="center", alpha=b)
    if J.get("nota"): T(f, 0.06, 0.215, J["nota"], BLUE, 22, "bold", alpha=ease((t - 0.5) / 0.4))
    return to_arr(f)


def s_grandes(t):
    J = VJ.get("grandes", {}); e = ease(t / 0.8)
    f = base_fig(2, "Tech-Schwergewichte und Dow-Jones-Werte", J.get("titulo", "Wer hat die Indizes heute bewegt?"),
                 J.get("fuente", f"Veränderung: {TV_TXT}. Beitrag jeder Aktie zum Dow Jones in Punkten = Veränderung in Dollar ÷ Indexdivisor (aus den Tagesdaten berechnet)."))
    G = R.get("ndx_grandes") or []
    T(f, 0.06, 0.725, "Größte Nasdaq-100-Werte (nach Börsenwert)", GOLD, 22, "bold")
    if G: hbars(f, [0.23, 0.25, 0.20, 0.45], [g["nombre"] for g in G], [g["cambio"] for g in G], [cc_(g["cambio"]) for g in G], e=e, fs=18)
    DA = R.get("dow_aportes")
    T(f, 0.53, 0.725, "Dow Jones: größte Beiträge (Punkte)", GOLD, 22, "bold")
    if DA:
        L = DA["valores"][:4] + DA["valores"][-3:]
        hbars(f, [0.72, 0.25, 0.20, 0.45], [x["nombre"] for x in L], [x["puntos"] for x in L], [cc_(x["puntos"]) for x in L],
              fmt=lambda v: pts(v, 0), e=e, fs=18)
    elif J.get("dow_txt"):
        T(f, 0.53, 0.6, "\n".join(textwrap.wrap(J["dow_txt"], 45)), FG, 22, va="top", linespacing=1.4)
    return to_arr(f)


def s_news(t):
    N_ = VJ["noticias"]; f = base_fig(2, "Warum hat sich der Markt bewegt?", N_["titulo"], N_["fuente"]); pal = [GOLD, TEAL, BLUE, NEG, FG]
    for i, (tag, txt) in enumerate(N_["items"][:5]):
        b = ease((t - i * 0.15) / 0.4)
        if b <= 0: continue
        y = 0.68 - i * 0.105; cc = pal[i % 5]
        rect(f, 0.05, y - 0.035, 0.006, 0.08, cc, b)
        T(f, 0.065, y + 0.012, tag, cc, 26, "bold", alpha=b)
        L_ = textwrap.wrap(txt, 115)
        T(f, 0.065, y - 0.03, "\n".join(L_[:2]), FG, 22 if len(L_) == 1 else 18, va="center" if len(L_) == 1 else "top", alpha=b)
    return to_arr(f)


# ---------- 3. Sektoren ----------
def s_sectores(t):
    J = VJ.get("sectores", {}); S = R.get("sectores") or []; e = ease(t / 0.8)
    f = base_fig(3, "Sektoren: SPDR-Sektor-ETFs", J.get("titulo", "So liefen die Sektoren"),
                 J.get("fuente", f"Tages- und Wochenveränderung der ETFs XLK, XLF, XLE, XLV, XLY und XLI: {TV_TXT} (Schluss {fiso(R['fecha'])})."))
    if S:
        cols = [(TEAL if s["cambio"] >= 0 else NEG) if (i < 2 or i >= len(S) - 2) else DIM for i, s in enumerate(S)]
        hbars(f, [0.69, 0.25, 0.17, 0.46], [f"{s['nombre']} {s['simbolo']}" for s in S], [s["cambio"] for s in S], cols, e=e, fs=19,
              extra=[("5 T. " + pct(s["semana"], 1)) if s.get("semana") is not None else "" for s in S])
        T(f, 0.50, 0.725, "Tagesveränderung (und letzte 5 Tage)", MUTED, 18)
    for i, it in enumerate(J.get("items", [])[:4]):
        b = ease((t - 0.3 - i * 0.12) / 0.4)
        if b <= 0: continue
        a_, b_, c_ = (it + ["fg"])[:3]; y = 0.68 - i * 0.15
        T(f, 0.06, y, a_, col(c_), 25, "bold", alpha=b)
        T(f, 0.06, y - 0.03, "\n".join(textwrap.wrap(b_, 50)[:3]), MUTED, 19, va="top", linespacing=1.3, alpha=b)
    return to_arr(f)


# ---------- 4. Fünf Aktien ----------
def s_accion(i, t):
    J = VJ["acciones"][i]; a = accion(M, J["ticker"], VJ.get("nombres")); e = ease(t / 0.8)
    f = base_fig(4, f"Aktien des Tages · {i + 1}/5", f"{a['nombre']} ({a['ticker']})",
                 J.get("fuente", f"Kurs und Volumen: {TV_TXT} (Schluss {fiso(R['fecha'])}). Volumen im Vergleich zum 10-Tage-Schnitt: berechnet. Meldung: genannte Quellen."))
    cc = cc_(a["cambio"])
    if a["nombre_en"].lower() != a["nombre"].lower(): T(f, 0.06, 0.735, a["nombre_en"], MUTED, 22, "bold")
    f.text(0.06, 0.655, num(a["cierre"]) + " $", color=FG, fontsize=60, weight="bold", ha="left")
    f.text(0.06, 0.6, f"{pct(a['cambio'])}   ({pts(a['cambio_abs'])} $)", color=cc, fontsize=32, weight="bold", ha="left")
    fil = [("Handelsvolumen", millones(a["volumen"]) + " Aktien"), ("vs. 10-Tage-Schnitt", f"×{num(a['vol_rel'], 1)}" if a.get("vol_rel") else "—"),
           ("Umsatz", millones(a["valor_usd"]) + " $")]
    for j, (l, v) in enumerate(fil):
        y = 0.545 - j * 0.036; T(f, 0.06, y, l, MUTED, 18); T(f, 0.24, y, v, FG, 19, "bold")
    b = ease((t - 0.25) / 0.4); y = 0.425
    T(f, 0.06, y, "Meldung", GOLD, 20, "bold", alpha=b); L1 = textwrap.wrap(J["noticia"], 55)
    T(f, 0.06, y - 0.03, "\n".join(L1), FG, 19, va="top", linespacing=1.3, alpha=b); y -= 0.065 + 0.033 * len(L1)
    c2 = ease((t - 0.45) / 0.4)
    T(f, 0.06, y, "Einordnung", BLUE, 20, "bold", alpha=c2)
    L2 = textwrap.wrap(J["lectura"], 62)[:max(2, 4 - len(L1))]   # noticia + lectura caben en 4 líneas
    T(f, 0.06, y - 0.03, "\n".join(L2), MUTED, 18, va="top", linespacing=1.3, alpha=c2)
    V = [v for v in (a.get("velas") or []) if fecha_vela_(v["t"]) <= FECHA][-60:]
    if len(V) > 10:
        o, hi, lo, c, vol = (np.array([v[k] if v.get(k) is not None else np.nan for v in V], float) for k in "ohlcv")
        n = len(V); m = max(2, int(n * e)); span = np.nanmax(hi) - np.nanmin(lo)
        ax = f.add_axes([0.50, 0.36, 0.42, 0.38]); clean(ax)
        for j in range(m):
            k = TEAL if c[j] >= o[j] else NEG
            ax.vlines(j, lo[j], hi[j], color=k, lw=1.3); ax.add_patch(plt.Rectangle((j - 0.35, min(o[j], c[j])), 0.7, max(abs(c[j] - o[j]), span * 0.003), color=k))
        ax.set_xlim(-1, n); ax.set_ylim(np.nanmin(lo) - span * 0.05, np.nanmax(hi) + span * 0.05); ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: num(v, 0 if span > 20 else 2)))
        dd = [fecha_vela_(v["t"]) for v in V]; tk = [j for j in range(3, n) if dd[j].month != dd[j - 1].month]
        ax.set_xticks(tk, [MESES[dd[j].month - 1] for j in tk]); ax.tick_params(axis="x", labelsize=15)
        ax2 = f.add_axes([0.50, 0.24, 0.42, 0.10]); clean(ax2); ax2.patch.set_alpha(0); ax2.set_zorder(-1)
        ax2.bar(np.arange(m), np.nan_to_num(vol[:m]), color=[TEAL if c[j] >= o[j] else NEG for j in range(m)], alpha=0.75, width=0.7)
        ax2.set_xlim(-1, n); ax2.set_xticks([]); ax2.set_yticks([])
        T(f, 0.50, 0.75, "Tageskerzen der letzten 3 Monate und Handelsvolumen", MUTED, 17)
    return to_arr(f)


def fecha_vela_(t): return dt.datetime.fromtimestamp(t, dt.timezone.utc).date()


# ---------- 5. Makro ----------
def s_macro(t):
    J = VJ.get("macro", {}); X = R.get("macro") or []
    f = base_fig(5, "Zinsen, Dollar, Rohstoffe", J.get("titulo", "Anleihen, Dollar, Volatilität, Öl und Gold"),
                 J.get("fuente", f"{TV_TXT}: Rendite 10-jähriger US-Staatsanleihen (TVC:US10Y, Veränderung in Basispunkten), DXY, VIX, US-Öl WTI (TVC:USOIL), Gold"
                       + (", EUR/USD" if any(x["simbolo"] == "FX:EURUSD" for x in X) else "") + ", DAX (XETR:DAX) und Euro Stoxx 50 (TVC:SX5E). "
                       f"Letzter Schluss bis {fiso(R['fecha'])}; Linie: letzte 15 Handelstage."))
    w = 0.88 / max(len(X), 1)
    for i, x in enumerate(X):
        b = ease((t - i * 0.1) / 0.4)
        if b <= 0: continue
        x0 = 0.06 + i * w; up = x["cambio_pct"] >= 0; cc = TEAL if up else NEG
        rect(f, x0, 0.42, w - 0.012, 0.32, NAVY, 0.6 * b)
        T(f, x0 + 0.01, 0.705, "\n".join(textwrap.wrap(x["nombre"], 22)), GOLD, 19, "bold", va="top" if len(x["nombre"]) > 22 else "baseline", alpha=b)
        val = (f"{num(x['cierre'], 3)} %" if x["unidad"] == "%" else num(x["cierre"], 4 if x["simbolo"] == "FX:EURUSD" else 2))
        f.text(x0 + 0.01, 0.62, val, color=FG, fontsize=34, weight="bold", ha="left", alpha=b)
        ch = _de(f"{x['cambio_pb']:+.1f}") + " Basispunkte" if x.get("cambio_pb") is not None else pct(x["cambio_pct"])
        T(f, x0 + 0.01, 0.58, ch, cc, 20, "bold", alpha=b)
        if not x["mismo_dia"]: T(f, x0 + 0.01, 0.555, "Letzter Schluss " + fiso(x["fecha"]), MUTED, 13, alpha=b)
        ax = f.add_axes([x0 + 0.01, 0.44, w - 0.035, 0.1]); clean(ax); s = np.array(x["serie"])
        ax.plot(np.arange(len(s)), s, color=cc, lw=2.5, alpha=b); ax.fill_between(np.arange(len(s)), s, s.min(), color=cc, alpha=0.12 * b)
        ax.set_xticks([]); ax.set_yticks([])
        txt = (J.get("items") or {}).get(x["simbolo"])
        if txt: T(f, x0 + 0.005, 0.40, "\n".join(textwrap.wrap(txt, 30)[:3]), MUTED, 15, va="top", linespacing=1.3, alpha=b)
    # Europa: DAX, Euro Stoxx 50 (y EUR/USD si está) de los datos de Nabd, más el texto del día
    C = R.get("contexto") or {}
    eu = [f"{n} {num(C[s]['close'], 4 if s == 'FX:EURUSD' else 0)} ({pct(C[s]['change'])})" for s, n in EUROPA if s in C and s != "FX:EURUSD"]
    if eu or J.get("europa"):
        c2 = ease((t - 0.5) / 0.4); rect(f, 0.06, 0.235, 0.88, 0.085, GOLD, 0.15 * c2)
        T(f, 0.075, 0.293, "Und Europa?  " + "  ·  ".join(eu) + "   (Xetra-Schluss 17:30 Uhr)", GOLD, 20, "bold", va="center", alpha=c2)
        if J.get("europa"): T(f, 0.075, 0.255, J["europa"], FG, 18 if len(J["europa"]) < 120 else 15, va="center", alpha=c2)
    return to_arr(f)


# ---------- 6. Charttechnik ----------
def s_tech(k, t):
    TJ = VJ["tecnico"][k]; r = R[k]; a_ = A[k]; vr = r["volumen_vs_media10_pct"]
    f = base_fig(6, "Charttechnik · " + INDICE[k], TJ["titulo"],
                 f"Tageskerzen der letzten 6 Monate von {TV_TXT} ({r['sesiones']} Handelstage seit {r['historia_desde'][:4]}). Gleitende Durchschnitte (GD) 20, 50 und 200, RSI 14, "
                 "Unterstützungen und Widerstände (jüngste Hochs und Tiefs) und Volumen im Vergleich zum 10-Tage-Schnitt: berechnet. Das sind Daten, keine Kauf- oder Verkaufssignale.")
    dates, o, hi, lo, c, vol = (a_[x] for x in ("dates", "o", "hi", "lo", "c", "vol"))
    n = len(c); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    hay_vol = np.isfinite(vol[idx]).sum() > NB * 0.8
    ax = f.add_axes([0.40, 0.44 if hay_vol else 0.36, 0.54, 0.31 if hay_vol else 0.39]); clean(ax)
    span = hi[idx].max() - lo[idx].min()
    for j in range(m):
        i = idx[j]; cc = TEAL if c[i] >= o[i] else NEG
        ax.vlines(j, lo[i], hi[i], color=cc, lw=1.2); ax.add_patch(plt.Rectangle((j - 0.35, min(o[i], c[i])), 0.7, max(abs(c[i] - o[i]), span * 0.002), color=cc))
    for S_, col_, lab in ((a_["S20"], FG, "GD 20"), (a_["S50"], BLUE, "GD 50"), (a_["S200"], GOLD, "GD 200")):
        ax.plot(x[:m], S_[idx][:m], color=col_, lw=2.2, label=lab, alpha=0.9)
    al = ease((t - 0.6) / 0.4); LEV = [l for l in r["niveles"] if lo[idx].min() - span * 0.25 <= l["valor"] <= hi[idx].max() + span * 0.25]
    for l in LEV: ax.axhline(l["valor"], color=NEG if l["tipo"] == "res" else TEAL, lw=1.1, ls="--", alpha=al)
    vals = [l["valor"] for l in LEV]
    ax.set_xlim(-1, NB); ax.set_ylim(min(lo[idx].min(), np.nanmin(a_["S200"][idx]), *vals) - span * 0.05, max(hi[idx].max(), np.nanmax(a_["S200"][idx]), *vals) + span * 0.05)
    tk = [j for j in range(4, NB) if dates[idx[j]].month != dates[idx[j - 1]].month]
    ax.set_xticks(tk, [MESES[dates[idx[j]].month - 1] for j in tk]); ax.tick_params(labelsize=15)
    ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: num(v, 0)))
    ax.legend(frameon=False, labelcolor=FG, fontsize=16, loc=TJ.get("leyenda", "upper left"), ncol=3)
    if hay_vol:
        axv = f.add_axes([0.40, 0.345, 0.54, 0.075]); clean(axv); axv.patch.set_alpha(0); axv.set_zorder(-1)
        axv.bar(x[:m], vol[idx][:m], color=[TEAL if c[i] >= o[i] else NEG for i in idx[:m]], alpha=0.7, width=0.7)
        axv.set_xlim(-1, NB); axv.set_xticks([]); axv.set_yticks([]); axv.text(0.0, 1.0, "Volumen", transform=axv.transAxes, color=MUTED, fontsize=13, ha="left", va="top")
    ax2 = f.add_axes([0.40, 0.215, 0.54, 0.11]); clean(ax2)
    ax2.axhspan(70, 100, color=NEG, alpha=0.08); ax2.axhspan(0, 30, color=TEAL, alpha=0.08)
    for lv in (30, 70): ax2.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax2.plot(x[:m], a_["RSI"][idx][:m], color=BLUE, lw=2.2, label="RSI 14")
    ax2.set_xlim(-1, NB); ax2.set_ylim(0, 100); ax2.set_xticks([]); ax2.yaxis.tick_right(); ax2.set_yticks([30, 70])
    ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left")
    filas = [("Schluss", num(r["cierre"]), FG),
             ("GD 20", f"{num(r['sma20'])}  ({pct(r['dist_sma20_pct'], 1)})", FG),
             ("GD 50", f"{num(r['sma50'])}  ({pct(r['dist_sma50_pct'], 1)})", BLUE),
             ("GD 200", f"{num(r['sma200'])}  ({pct(r['dist_sma200_pct'], 1)})", GOLD),
             ("RSI 14", num(r["rsi14"], 1) + " · " + TJ["rsi_txt"], BLUE),
             ("Volumen", ("—" if vr is None else f"{pct(vr, 0)}") + " vs. 10-T.-Schnitt", MUTED),
             ("Trend (berechnet)", r["tendencia"], GOLD)]
    res = [l for l in r["niveles"] if l["tipo"] == "res"]; sop = [l for l in r["niveles"] if l["tipo"] == "sop"]
    if res: filas.append(("Widerstand", f"{num(min(res, key=lambda l: l['valor'])['valor'])}  (Hoch {fiso(min(res, key=lambda l: l['valor'])['fecha'])})", NEG))
    if sop: filas.append(("Unterstützung", f"{num(max(sop, key=lambda l: l['valor'])['valor'])}  (Tief {fiso(max(sop, key=lambda l: l['valor'])['fecha'])})", TEAL))
    for i, (lab, val, cc) in enumerate(filas):
        b = ease((t - 0.3 - i * 0.05) / 0.4)
        if b <= 0: continue
        y = 0.725 - i * 0.058
        T(f, 0.06, y, lab, MUTED, 18, alpha=b)
        T(f, 0.18, y, val, cc, 19 if len(val) <= 26 else 16, "bold", alpha=b)
    return to_arr(f)


def s_esc(k, t):
    r = R[k]; E = r["escenarios"]; a_ = A[k]; TJ = VJ["tecnico"][k]
    f = base_fig(6, "Drei Szenarien · " + INDICE[k], TJ.get("esc_titulo", "Die Marken, auf die Anleger achten"),
                 "Marken berechnet aus öffentlichen Schlusskursen (Hochs und Tiefs der letzten 5 und 30 Handelstage und 52 Wochen, GD 20, 50 und 200). "
                 "Bedingte Szenarien, die beschreiben, was jede Marke bedeuten könnte: keine Prognosen und keine Kauf- oder Verkaufsempfehlungen.")
    et = lambda l: f"{num(l['valor'])} ({fiso(l['et'])})"
    up, dn, ne = E["alcista"], E["bajista"], E["neutral"]
    cards = [("Positives Szenario", TEAL, ("Ein Schluss über " + et(up[0]) + " bestätigt die Erholung" + ((", nächste Marke " + et(up[1])) if len(up) > 1 else "")) if up
              else "Der Index notiert am Hoch des Zeitraums: kein früherer Widerstand darüber, entscheidend ist ein Halten über " + num(r["cierre"])),
             ("Neutrales Szenario", GOLD, (f"Handel zwischen {num(ne[0]['valor'])} und {num(ne[1]['valor'])} bedeutet Konsolidierung (Spanne {num(abs(ne[1]['valor'] / ne[0]['valor'] * 100 - 100), 1)} %)") if ne
              else "Keine klare Spanne zwischen nahen Unterstützungen und Widerständen"),
             ("Negatives Szenario", NEG, ("Ein Schluss unter " + et(dn[0]) + ((" rückt " + et(dn[1]) + " in den Blick") if len(dn) > 1 else " wäre ein Warnsignal")) if dn
              else "Keine frühere Unterstützung knapp unter dem aktuellen Kurs")]
    for i, (tt, cc, tx) in enumerate(cards):
        b = ease((t - i * 0.18) / 0.4)
        if b <= 0: continue
        y = 0.63 - i * 0.155
        rect(f, 0.06, y - 0.06, 0.44, 0.135, cc, 0.13 * b); rect(f, 0.06, y - 0.06, 0.005, 0.135, cc, b)
        T(f, 0.075, y + 0.035, tt, cc, 26, "bold", alpha=b)
        L_ = textwrap.wrap(tx, 50); fs_ = 20
        if len(L_) > 2: L_ = textwrap.wrap(tx, 60); fs_ = 17  # tres líneas: letra menor, desde arriba, sin pisar el título
        T(f, 0.075, y + 0.012, "\n".join(L_), FG, fs_, va="top", linespacing=1.3, alpha=b)
    c = a_["c"][-60:]; n = len(c); ax = f.add_axes([0.55, 0.25, 0.40, 0.48]); clean(ax)
    ax.plot(np.arange(n), c, color=FG, lw=2.5)
    lv = [(l["valor"], TEAL) for l in up if abs(l["dist_pct"]) <= 7] + [(l["valor"], NEG) for l in dn if abs(l["dist_pct"]) <= 7]
    ult = None
    for v, cc in sorted(lv):
        ax.axhline(v, color=cc, lw=1.4, ls="--")
        if ult is None or abs(v / ult - 1) > 0.006: ax.text(n + 0.5, v, num(v, 0), color=cc, fontsize=15, va="center", weight="bold"); ult = v
    lo_ = min([c.min()] + [v for v, _ in lv]); hi_ = max([c.max()] + [v for v, _ in lv]); sp = hi_ - lo_
    ax.set_ylim(lo_ - sp * 0.06, hi_ + sp * 0.06); ax.set_xlim(0, n + 8); ax.set_xticks([]); ax.set_yticks([])
    ax.scatter([n - 1], [c[-1]], color=GOLD, s=80, zorder=5)
    T(f, 0.55, 0.75, "Schlusskurse der letzten 60 Handelstage und Marken", MUTED, 17)
    return to_arr(f)


# ---------- 7. Was morgen ansteht ----------
def s_agenda(t):
    G = VJ["agenda"]; f = base_fig(7, "Was steht in der nächsten Sitzung an?", G["titulo"], G["fuente"])
    for x, h, ha in ((0.06, "Datum", "left"), (0.21, "Termin", "left"), (0.82, "New York", "center"), (0.92, "Deutschland", "center")):
        T(f, x, 0.71, h, MUTED, 19, "bold", ha=ha)
    rect(f, 0.05, 0.695, 0.90, 0.003, GOLD)
    for i, row in enumerate(G["filas"][:7]):
        b = ease((t - i * 0.1) / 0.4); y = 0.645 - i * 0.068
        if b <= 0: continue
        if len(row) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}$", row[0]):
            d = dt.date.fromisoformat(row[0]); dia = DIAS[d.weekday()][:2] + ", " + corto(d); ny = row[2] if len(row) > 2 else ""
            de = ""
            if re.match(r"\d{1,2}:\d{2}$", ny or ""):
                hh, mm = map(int, ny.split(":")); z = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=NYZ).astimezone(BERLIN)
                de = z.strftime("%H:%M") + (" (+1)" if z.date() > d else "")
        else:
            dia, ny, de = row[0], "", ""
        T(f, 0.06, y, dia, GOLD, 23, "bold", alpha=b)
        T(f, 0.21, y, row[1], FG, 22 if len(row[1]) <= 60 else 18, alpha=b)
        f.text(0.82, y, ny or "—", color=FG, fontsize=21, weight="bold", ha="center", alpha=b)
        f.text(0.92, y, de or "—", color=BLUE, fontsize=21, weight="bold", ha="center", alpha=b)
    return to_arr(f)


# ---------- 8. Fazit ----------
def s_fin(t):
    Fn = VJ["fin"]; f = fig(W, H); a = ease(t / 0.5); b = ease((t - 0.25) / 0.5)
    T(f, 0.06, 0.85, MARCA + " · " + FECHA_TXT, FG, 46 if len(MARCA + FECHA_TXT) < 48 else 40, "bold", alpha=a)
    T(f, 0.06, 0.775, "\n".join(textwrap.wrap(Fn["titular"], 60)), GOLD, 30, "bold", alpha=a, linespacing=1.35, va="top")
    rect(f, 0.06, 0.47, 0.64, 0.19, BLUE, 0.14 * b); rect(f, 0.06, 0.47, 0.005, 0.19, BLUE, b)
    T(f, 0.08, 0.615, "Kostenlos unserem Telegram-Kanal folgen", FG, 34, "bold", alpha=b)
    T(f, 0.08, 0.565, "Analysen zur US-Börse und Updates während der Sitzung · Link in der Videobeschreibung", MUTED, 21, alpha=b)
    f.text(0.08, 0.495, TELEGRAM.replace("https://", ""), color=BLUE, fontsize=34, ha="left", weight="bold", alpha=b)
    f.text(0.06, 0.41, CANAL.replace("https://www.", ""), color=MUTED, fontsize=22, ha="left", weight="bold", alpha=a)
    aviso = ("Wichtiger Hinweis: Nur Information und Bildung. Keine Anlageberatung und keine Kauf- oder Verkaufsempfehlung für ein Wertpapier. "
             "Die Zahlen stammen aus öffentlichen, genannten Quellen (" + Fn["fuentes"] + "); eigene Berechnungen sind mit «berechnet» gekennzeichnet. "
             "Charttechnik und Szenarien beschreiben Kursverläufe und sind keine Prognosen. Wir halten keine Positionen in den genannten Aktien. "
             "Aktien sind mit Risiken bis zum Totalverlust verbunden; frühere Wertentwicklungen sind kein verlässlicher Indikator für künftige Ergebnisse. "
             "Text, Stimme (synthetische Stimme) und Grafiken mit KI erstellt.")
    T(f, 0.06, 0.20, "\n".join(textwrap.wrap(aviso, 150)), MUTED, 15, linespacing=1.5, alpha=a)
    return with_logo(to_arr(f), LGB, x=W - 230 - 110, y=70)


# ---------- Secuencia ----------
ESC = [("s_title", 1, s_title), ("s_indices", 2, s_indices), ("s_grandes", 2, s_grandes), ("s_news", 2, s_news), ("s_sectores", 3, s_sectores)]
ESC += [(f"s_accion_{i + 1}", 4, (lambda t, i=i: s_accion(i, t))) for i in range(len(VJ.get("acciones", [])))]
ESC += [("s_macro", 5, s_macro), ("s_tech_spx", 6, lambda t: s_tech("spx", t)), ("s_esc_spx", 6, lambda t: s_esc("spx", t)),
        ("s_tech_ndx", 6, lambda t: s_tech("ndx", t)), ("s_esc_ndx", 6, lambda t: s_esc("ndx", t)), ("s_agenda", 7, s_agenda), ("s_fin", 8, s_fin)]
BIG = {"s_title", "s_fin"}
VISUAL = {"s_title": "Título del programa y fecha, cierre del S&P 500 y curva intradía, Nasdaq 100, Dow Jones y Russell 2000",
          "s_indices": "Tabla comparativa animada: cierre, día, semana, distancia al máximo, a la 200-Tage-Linie y tendencia",
          "s_grandes": "Barras: grandes del Nasdaq 100 y aportación en puntos de los valores del Dow Jones", "s_news": "Noticias principales y motivos del movimiento con fuentes",
          "s_sectores": "Barras del día de los seis ETF sectoriales con la semana", "s_macro": "Tarjetas con línea de 15 sesiones y franja de Europa (DAX, Euro Stoxx 50)",
          "s_tech_spx": "Velas de 6 meses, GD 20/50/200, volumen, RSI 14, soportes y resistencias", "s_esc_spx": "Tarjetas de los tres escenarios y línea de 60 sesiones",
          "s_tech_ndx": "Velas de 6 meses, GD 20/50/200, volumen, RSI 14, soportes y resistencias", "s_esc_ndx": "Tarjetas de los tres escenarios y línea de 60 sesiones",
          "s_agenda": "Tabla de citas con hora de Nueva York y de Alemania", "s_fin": "Logo, invitación a Telegram y aviso legal"}


def texto_voz(nombre):
    if nombre.startswith("s_accion_"): return VJ["acciones"][int(nombre.split("_")[-1]) - 1]["voz"]
    return VJ["voz"][nombre]


def frame(nombre, fn, t):
    arr = fn(t); return arr if nombre in BIG else with_logo(arr, LGS, x=W - 95 - 48, y=48)   # logo arriba a la derecha


# ---------- Control de calidad (manual, sección 8) ----------
def control():
    err, aviso = [], []
    hoy_ny = dt.datetime.now(NYZ).date()
    if FECHA > hoy_ny: err.append(f"la sesión {FECHA} es posterior a hoy en Nueva York")
    if VJ.get("fecha") and VJ["fecha"] != R["fecha"]: err.append(f"video.json es del {VJ['fecha']} y los datos del {R['fecha']}")
    for k in ("spx", "ndx", "dji", "rut"):
        if k not in R: err.append(f"faltan las velas de {k}"); continue
        if R[k]["fecha"] != R["fecha"]: err.append(f"{k}: última vela del {R[k]['fecha']}, la sesión es del {R['fecha']}")
        if R[k]["sesiones"] < 220: err.append(f"{k}: solo {R[k]['sesiones']} sesiones, no alcanza para la media de 200")
    if len(R.get("sectores") or []) < 6: err.append("faltan ETF sectoriales en los datos")
    if len(R.get("macro") or []) < 5: err.append("faltan indicadores macro en los datos")
    for x in R.get("macro") or []:
        if not x["mismo_dia"]: aviso.append(f"{x['simbolo']}: último dato del {x['fecha']} (se muestra la fecha en pantalla)")
    A5 = VJ.get("acciones", [])
    if len(A5) != 5: err.append(f"hacen falta 5 acciones y hay {len(A5)}")
    for a in A5:
        if not accion(M, a["ticker"]): err.append(f"{a['ticker']} no está en los datos del día")
        for c in ("noticia", "lectura", "voz"):
            if not a.get(c): err.append(f"{a.get('ticker')}: falta {c}")
    for nombre, _, _ in ESC:
        try:
            if not texto_voz(nombre).strip(): err.append(f"falta la locución de {nombre}")
        except (KeyError, IndexError): err.append(f"falta la locución de {nombre}")
    for row in VJ.get("agenda", {}).get("filas", []):
        if re.match(r"\d{4}-\d{2}-\d{2}$", row[0]) and dt.date.fromisoformat(row[0]) <= FECHA: err.append(f"agenda: {row[0]} no es posterior a la sesión")
    for x in aviso: print("aviso:", x)
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


# ---------- Ticker y subtítulos ----------
def ticker_tira():
    piezas = []
    for k in ("spx", "ndx", "dji", "rut"):
        if k in R: piezas.append([(INDICE_CORTO[k], FG), (num(R[k]["cierre"]), FG), (pct(R[k]["var_pct"]), cc_(R[k]["var_pct"]))])
    for x in R.get("macro") or []:
        piezas.append([(x["nombre"], FG),
                       (f"{num(x['cierre'], 3)} %" if x["unidad"] == "%" else num(x["cierre"], 4 if x["simbolo"] == "FX:EURUSD" else 2), FG), (pct(x["cambio_pct"]), cc_(x["cambio_pct"]))])
    for s in R.get("sectores") or []: piezas.append([(s["simbolo"], FG), (pct(s["cambio"]), cc_(s["cambio"]))])
    for h in VJ.get("ticker") or [n[0] + ": " + n[1] for n in VJ["noticias"]["items"]]: piezas.append([(h, GOLD)])
    sep = tira_texto("◆", GOLD, 14, 52); hueco = np.zeros((52, 26, 4), np.uint8)
    imgs = []
    for p in piezas:  # orden de lectura de izquierda a derecha: la primera pieza a la izquierda
        partes = [tira_texto(s, c, 19, 52) for s, c in p]
        im = np.concatenate(sum([[x, np.zeros((52, 12, 4), np.uint8)] for x in partes], [])[:-1], axis=1)
        imgs += [im, hueco, sep, hueco]
    return np.concatenate(imgs, axis=1)


SUB_CACHE = {}


def subtitulo(s):
    if s not in SUB_CACHE:
        lin = textwrap.wrap(s, 80) or [s]
        SUB_CACHE[s] = [tira_texto(l, FG, 27, 50, "bold") for l in lin]
    return SUB_CACHE[s]


def hacer_overlay(marcas, leads):
    TIRA = ticker_tira(); L = TIRA.shape[1]; band = np.array([0x13, 0x29, 0x4B], np.float32); gold = np.array([0xD4, 0xAF, 0x37], np.uint8)
    def ov(fr, j, ts, tg):
        fr = fr.copy()
        fr[H - 52:] = (fr[H - 52:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - 54:H - 52] = gold
        off = int(tg * 85) % L
        for x in range(-off, W, L): pegar(fr, TIRA, x, H - 52)   # el ticker corre de derecha a izquierda
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = subtitulo(s); h = 50 * len(ls); y0 = H - 66 - h; wmax = max(l.shape[1] for l in ls)
                x0 = (W - wmax) // 2 - 24; fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array([11, 26, 46], np.float32) * 0.72).astype(np.uint8)
                for i, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + i * 50)
                break
        return fr
    return ov


def guion_y_datos(times, durs, marcas, motor):
    """Guion en tabla (tiempo, narración, visual, datos) y tabla de datos usados (manual, secciones 7 y 10)."""
    mmss = lambda s: f"{int(s) // 60:02d}:{int(s) % 60:02d}"
    datos_escena = {"s_title": " · ".join(f"{INDICE_CORTO[k]} {num(R[k]['cierre'])} ({pct(R[k]['var_pct'])})" for k in ("spx", "ndx", "dji", "rut") if k in R),
                    "s_sectores": " · ".join(f"{s['simbolo']} {pct(s['cambio'])}" for s in R.get("sectores") or []),
                    "s_macro": " · ".join(f"{x['simbolo']} {x['cierre']} ({pct(x['cambio_pct'])})" for x in R.get("macro") or [])}
    for k in ("spx", "ndx"):
        r = R[k]; datos_escena[f"s_tech_{k}"] = f"cierre {num(r['cierre'])} · SMA20 {num(r['sma20'])} · SMA50 {num(r['sma50'])} · SMA200 {num(r['sma200'])} · RSI {r['rsi14']}"
        datos_escena[f"s_esc_{k}"] = json.dumps(r["escenarios"], ensure_ascii=False)
    L = [f"# Guion {MARCA} · {PROGRAMA} · {FECHA_TXT}", "", f"Voz: {motor}. Duración: {mmss(sum(durs))}.", "",
         "| Tiempo | Narración en alemán | Visual | Datos |", "|---|---|---|---|"]
    for (nombre, _, _), t0 in zip(ESC, times):
        vis = VISUAL.get(nombre, "Tarjeta de la acción: precio, cambio, volumen, noticia, lectura y velas de 3 meses")
        dat = datos_escena.get(nombre, "")
        if nombre.startswith("s_accion_"):
            a = accion(M, VJ["acciones"][int(nombre.split("_")[-1]) - 1]["ticker"]); dat = f"{a['ticker']} {a['cierre']} ({pct(a['cambio'])}) vol {a['volumen']} ×{a['vol_rel']}"
        L.append(f"| {mmss(t0)} | {texto_voz(nombre)} | {vis} | {dat} |")
    open(f"{DIR}/guion-{R['fecha']}-GE.md", "w").write("\n".join(L) + "\n")
    ref = f"cierre {R['fecha']} 16:00 Nueva York; descargado {M.get('generado', '')}"
    with open(f"{DIR}/datos-{R['fecha']}-GE.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["concepto", "valor", "fuente", "referencia"])
        for k in ("spx", "ndx", "dji", "rut"):
            r = R[k]
            for c in ("cierre", "var_pct", "var_pts", "semana_pct", "max_hist", "max_hist_fecha", "dist_max_hist_pct", "sma20", "sma50", "sma200", "rsi14", "volumen_vs_media10_pct", "tendencia"):
                w.writerow([f"{k}.{c}", r.get(c), "TradingView" if c in ("cierre", "var_pct", "var_pts") else "berechnet (TradingView)", ref])
            for e_, L_ in r["escenarios"].items():
                for l in L_: w.writerow([f"{k}.escenario.{e_}", l["valor"], "berechnet (TradingView)", l["et"]])
        for s in R.get("sectores") or []: w.writerow([f"sector.{s['simbolo']}", s["cambio"], "TradingView", ref])
        for x in R.get("macro") or []: w.writerow([f"macro.{x['simbolo']}", x["cierre"], "TradingView", f"cierre {x['fecha']}; cambio {x['cambio_pct']}%"])
        for a in VJ.get("acciones", []):
            d = accion(M, a["ticker"]); w.writerow([f"accion.{a['ticker']}", f"{d['cierre']} ({d['cambio']}%) vol {d['volumen']}", "TradingView; " + a.get("fuente", ""), ref])
        for n in VJ["noticias"]["items"]: w.writerow(["noticia", " ".join(n), VJ["noticias"]["fuente"], R["fecha"]])
        for row in VJ["agenda"]["filas"]: w.writerow(["agenda", " · ".join(row), VJ["agenda"]["fuente"], "hora de Nueva York"])


if __name__ == "__main__":
    os.makedirs(AUD, exist_ok=True)
    control()
    if PREVIEW:
        ov = hacer_overlay([[(0, 99, frases(texto_voz(n))[0])] for n, _, _ in ESC], [0] * len(ESC))
        for j, (nombre, _, fn) in enumerate(ESC): Image.fromarray(ov(frame(nombre, fn, 1.0), j, 1.0, 3.0 + j)).save(os.path.join(AUD, "prev_" + nombre + ".png"))
        sys.exit()
    V = [voz_frases(texto_voz(n), AUD) for n, _, _ in ESC]; sr = V[0][1]; motor = V[0][3]
    if len({v[1] for v in V}) > 1 or len({v[3] for v in V}) > 1: sys.exit("voces mezcladas")
    LEAD, TAIL = 0.15, 0.6
    durs = [LEAD + len(a) / sr + TAIL for a, _, _, _ in V]; durs[0] += 0.4; durs[-1] += 2.0
    print("voz", motor, "duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s: alarga o acorta la locución")
    leads = [LEAD + (0.4 if j == 0 else 0) for j in range(len(ESC))]
    times, t0 = render([lambda t, n=n, fn=fn: frame(n, fn, t) for n, _, fn in ESC], durs, ([v[0] for v in V], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "video-silent.mp4"), os.path.join(AUD, "full.wav"), overlay=hacer_overlay([v[2] for v in V], leads))
    json.dump([(n, tt) for (n, _, _), tt in zip(ESC, times)] + [("_total", round(t0, 2)), ("_voz", motor)], open(os.path.join(DIR, "times.json"), "w"))
    guion_y_datos(times, durs, [v[2] for v in V], motor)
    print("listo", round(t0, 1), "s", OUT)
