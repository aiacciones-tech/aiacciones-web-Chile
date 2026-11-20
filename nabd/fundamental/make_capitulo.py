# Capítulo de la serie semanal «التحليل الأساسي ببساطة» (análisis fundamental, fácil) de Nabd Wall Street: un concepto por vídeo,
# explicado sobre las cifras reales de una empresa de EE. UU. (Daniel, 20-nov-2026). 1920x1080, unos 6 minutos, voz del canal (Azure), subtítulos.
# Escenas en video.json → "escenas"; tipos: portada, puntos, cuenta (cuenta de resultados por líneas), cascada (de ingresos a beneficio),
# barras (serie por años), kpis, formula, fin. Toda cifra de pantalla viene escrita en video.json desde datos.json (TradingView) o los informes oficiales.
# Uso: AUD=<scratch> [VOZ_DIR=<wav por frase>] python3 make_capitulo.py <carpeta del capítulo> [preview]
#   Escribe <base>-Nabd.mp4, subtitulos-<base>-Nabd.srt, times.json y guion-<base>-Nabd.md.
import os, re, sys, json, textwrap, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_fund import *

DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")) if DIR else {}
W, H = 1920, 1080
MIN_S, MAX_S = 300, 450   # unos 6 minutos (5:00-7:30)
BASE = VJ.get("base", ""); OUT = f"{DIR}/{BASE}-Nabd.mp4"
ESC = VJ.get("escenas", [])
XR = 0.94   # margen derecho (texto árabe alineado a la derecha)
LG = load_logo(130); LGB = load_logo(230)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]
ORD = ["", "الأولى", "الثانية", "الثالثة", "الرابعة", "الخامسة", "السادسة", "السابعة", "الثامنة", "التاسعة", "العاشرة", "الحادية عشرة", "الثانية عشرة"]


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def wrap(s, n): return "\n".join(textwrap.wrap(str(s), n))


def base(i, e):
    f = fig(W, H)
    T(f, XR, 0.905, e.get("kicker", ""), GOLD, 24, "bold")
    tt = e.get("titulo", ""); T(f, XR, 0.83, tt, FG, 40 if len(tt) <= 55 else 32, "bold")
    T(f, 0.105, 0.925, f"{SERIE} · الحلقة {VJ['capitulo_n']}", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.89, f"{VJ['tema']} · {VJ['nombre']}", DIM, 16, "bold", ha="left")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n): rect(f, XR - (k + 1) * w + 0.008, 0.975, w - 0.008, 0.008, GOLD if k < CAP_IDX[i] else DIM)   # de derecha a izquierda
    return f


def fuente(f, e):
    s = e.get("fuente") or VJ.get("fuente_general", "")
    if s: T(f, XR, 0.215, wrap(s, 175), MUTED, 14, linespacing=1.3)


def U(v, d=1):
    """Cifra en pantalla con dígitos occidentales (como la prensa financiera del Golfo)."""
    return f"{v:,.{d}f}" if isinstance(v, (int, float)) else str(v)


# ---------- escenas ----------
def s_portada(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, XR, 0.88, f"سلسلة {SERIE} · {MARCA}", GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.60, 1.0, 0.22, GOLD, a)
    T(f, XR, 0.765, f"الحلقة {ORD[VJ['capitulo_n']] if VJ['capitulo_n'] < len(ORD) else VJ['capitulo_n']}", BG, 34, "bold", va="center", alpha=a)
    T(f, XR, 0.665, VJ["tema"], BG, 70 if len(VJ["tema"]) <= 28 else 54, "bold", va="center", alpha=a)
    T(f, XR, 0.50, f"بالأرقام الحقيقية لشركة {VJ['nombre']}", FG, 42, "bold", alpha=ease((t - 0.15) / 0.5))
    T(f, XR, 0.44, f"({VJ['ticker']})", MUTED, 28, "bold", alpha=ease((t - 0.2) / 0.5))
    if e.get("sub"): T(f, XR, 0.36, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    T(f, XR, 0.25, "محتوى تعليمي، وليس توصية استثمارية", BLUE, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=60, y=40)


def s_puntos(i, e, t):
    f = base(i, e); P = e["puntos"][:5]; hh = min(0.12, 0.5 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.76 - (k + 1) * hh; h = hh - 0.014
        rect(f, 0.06, y, 0.88, h, NAVY, b); rect(f, XR - 0.004, y, 0.004, h, e.get("colores", [GOLD] * 5)[k], b)
        T(f, XR - 0.02, y + h / 2, f"{k + 1}", GOLD, 34, "bold", va="center", alpha=b)
        T(f, XR - 0.055, y + h / 2, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.62, y + h / 2, wrap(txt, 62), MUTED, 21, va="center", alpha=b, linespacing=1.15)
    fuente(f, e)
    return to_arr(f)


TIPO_C = {"ingreso": FG, "resta": NEG, "suma": TEAL, "sub": GOLD, "final": GOLD, "nota": MUTED}


def s_cuenta(i, e, t):
    """Cuenta de resultados línea a línea: filas [{t, v:[col1, col2], tipo, nota}], columnas ["2025", "2024"]. Columna «التغير» calculada."""
    f = base(i, e); R = e["filas"]; C = e["columnas"]; n = len(R); hh = min(0.068, 0.43 / n); var = e.get("variacion", len(C) == 2)
    xs = [0.50, 0.36][:len(C)]; xv = 0.18
    y0 = 0.735
    T(f, XR - 0.01, y0, e.get("unidad", "مليار دولار"), MUTED, 18, "bold", va="center")
    for c, x in zip(C, xs): T(f, x, y0, c, GOLD, 24, "bold", va="center", ha="center")
    if var: T(f, xv, y0, "التغير (محسوب)", MUTED, 18, "bold", va="center", ha="center")
    hi = e.get("destacar")
    for k, r in enumerate(R):
        b = ease((t * 1.4 - k * 0.09) / 0.35); y = y0 - (k + 1) * hh; tp = r.get("tipo", "ingreso"); c = TIPO_C.get(tp, FG)
        if tp in ("sub", "final") or (hi and k in hi): rect(f, 0.06, y - hh * 0.45, 0.88, hh * 0.9, NAVY, b)
        if tp == "final": rect(f, XR - 0.004, y - hh * 0.45, 0.004, hh * 0.9, GOLD, b)
        lab = ("− " if tp == "resta" else "") + r["t"]
        T(f, XR - 0.015, y, lab, c, 25 if tp in ("sub", "final") else 23, "bold" if tp != "nota" else "normal", va="center", alpha=b)
        for v, x in zip(r.get("v", []), xs):
            f.text(x, y, U(v, r.get("d", 1)) if v is not None else "—", color=c, fontsize=25, weight="bold", ha="center", va="center", alpha=b)
        vv = r.get("v", [])
        if var and len(vv) == 2 and all(isinstance(x, (int, float)) for x in vv) and vv[1] and not r.get("sin_var"):
            ch = (vv[0] / vv[1] - 1) * 100
            f.text(xv, y, f"{ch:+.0f}%", color=MUTED if tp == "resta" else (TEAL if ch >= 0 else NEG), fontsize=23, weight="bold", ha="center", va="center", alpha=b)
    if e.get("nota"): T(f, XR, 0.255, e["nota"], GOLD, 21, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_cascada(i, e, t):
    """Puente de ingresos a beneficio: pasos [{t, v, tipo: total|resta|suma}] (en orden, de derecha a izquierda)."""
    f = base(i, e); P = e["pasos"]; n = len(P)
    ax = f.add_axes([0.06, 0.32, 0.88, 0.42]); clean(ax)
    acc, bars = 0.0, []
    for p in P:
        if p["tipo"] == "total": bars.append((0, p["v"])); acc = p["v"]
        elif p["tipo"] == "resta": bars.append((acc - p["v"], p["v"])); acc -= p["v"]
        else: bars.append((acc, p["v"])); acc += p["v"]
    top = max(b0 + h for b0, h in bars)
    xs = np.arange(n)[::-1]   # el primero a la derecha
    for k, ((b0, h), p, x) in enumerate(zip(bars, P, xs)):
        a = ease((t * 1.3 - k * 0.1) / 0.35); c = GOLD if p["tipo"] == "total" else (NEG if p["tipo"] == "resta" else TEAL)
        ax.bar(x, h * a, bottom=b0 + (h * (1 - a) if p["tipo"] == "resta" else 0), color=c, width=0.62, alpha=0.95)
        ax.text(x, b0 + h + top * 0.03, ("−" if p["tipo"] == "resta" else ("+" if p["tipo"] == "suma" else "")) + U(p["v"], p.get("d", 1)),
                color=FG, fontsize=24, weight="bold", ha="center", alpha=a)
        if k < n - 1:
            nb = bars[k + 1]; lvl = b0 + h if p["tipo"] != "resta" else b0
            ax.plot([x - 0.31, x - 0.69], [lvl, lvl], color=MUTED, lw=1, ls=":", alpha=a)
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(0, top * 1.15); ax.set_yticks([])
    ax.set_xticks(xs, [ar(wrap(p["t"], 22 if n <= 6 else 18)) for p in P]); ax.tick_params(colors=FG, labelsize=18)
    T(f, 0.06, 0.775, e.get("unidad", "مليار دولار"), MUTED, 18, "bold", ha="left")
    if e.get("nota"): T(f, XR, 0.775, e["nota"], GOLD, 20, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_barras(i, e, t):
    """Serie por años: categorias [...], series [{nombre, valores, color}], etiquetas con el valor encima."""
    f = base(i, e); C = e["categorias"]; S = e["series"]; n, m = len(C), len(S)
    ax = f.add_axes([0.08, 0.33, 0.84, 0.40]); clean(ax); wdt = 0.8 / m; a = ease(t * 1.2)
    top = max(max(v for v in s["valores"] if v is not None) for s in S)
    for j, s in enumerate(S):
        x = np.arange(n) + (j - (m - 1) / 2) * wdt; vals = [v if v is not None else 0 for v in s["valores"]]
        ax.bar(x, [v * a for v in vals], width=wdt * 0.9, color=col(s.get("color", "gold")))
        if t > 0.5:
            for xx, v in zip(x, s["valores"]):
                if v is not None: ax.text(xx, v * a + top * 0.02, U(v, e.get("d", 1)), color=FG, fontsize=20 if m > 1 else 24, weight="bold", ha="center")
    ax.set_xticks(np.arange(n), C); ax.tick_params(colors=FG, labelsize=22); ax.set_yticks([]); ax.set_ylim(0, top * 1.18)
    for j, s in enumerate(S):   # leyenda arriba a la derecha
        rect(f, XR - 0.015, 0.765 - j * 0.04, 0.012, 0.022, s.get("color", "gold")); T(f, XR - 0.025, 0.768 - j * 0.04, s["nombre"], FG, 20, "bold", va="bottom")
    T(f, 0.08, 0.765, e.get("unidad", "مليار دولار"), MUTED, 18, "bold", ha="left")
    if e.get("nota"): T(f, XR, 0.255, e["nota"], GOLD, 21, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_kpis(i, e, t):
    f = base(i, e); K = e["items"][:4]; n = len(K); w = 0.88 / n
    for k, it in enumerate(K):
        b = ease((t - k * 0.12) / 0.4); x1 = XR - k * w; x0 = x1 - w + 0.015
        rect(f, x0, 0.35, w - 0.015, 0.39, NAVY, b); rect(f, x0, 0.735, w - 0.015, 0.006, it.get("color", "gold"), b)
        cx = (x0 + x1 - 0.015) / 2
        f.text(cx, 0.60, it["big"], color=col(it.get("color", "gold")), fontsize=66 if len(it["big"]) <= 7 else 50, weight="bold", ha="center", va="center", alpha=b)
        T(f, cx, 0.48, wrap(it["label"], 26), FG, 23, "bold", ha="center", va="center", alpha=b, linespacing=1.1)
        if it.get("sub"): T(f, cx, 0.395, wrap(it["sub"], 36), MUTED, 18, ha="center", va="center", alpha=b, linespacing=1.3)
    if e.get("nota"): T(f, XR, 0.275, e["nota"], GOLD, 21, "bold", alpha=ease((t - 0.6) / 0.4))
    fuente(f, e)
    return to_arr(f)


def s_formula(i, e, t):
    """Fórmula en grande y un ejemplo con las cifras de la empresa: formula (texto), ejemplo [[texto, resultado]], nota."""
    f = base(i, e); a = ease(t / 0.4)
    rect(f, 0.06, 0.56, 0.88, 0.17, NAVY, a); rect(f, XR - 0.004, 0.56, 0.004, 0.17, GOLD, a)
    T(f, 0.5, 0.645, e["formula"], GOLD, 44 if len(e["formula"]) <= 40 else 34, "bold", ha="center", va="center", alpha=a)
    for k, (txt, res) in enumerate(e.get("ejemplo", [])[:3]):
        b = ease((t - 0.25 - k * 0.15) / 0.4); y = 0.48 - k * 0.075
        T(f, XR - 0.01, y, txt, FG, 27, "bold", va="center", alpha=b)
        f.text(0.10, y, res, color=TEAL, fontsize=34, weight="bold", ha="left", va="center", alpha=b)
    if e.get("nota"): T(f, XR, 0.265, wrap(e["nota"], 120), MUTED, 20, alpha=ease((t - 0.6) / 0.4), linespacing=1.35)
    fuente(f, e)
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.86, f"الحلقة {VJ['capitulo_n']}: {VJ['tema']}", FG, 42, "bold", alpha=a)
    T(f, XR, 0.80, "الخلاصة", GOLD, 30, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, XR, 0.73 - k * 0.062, "• " + c, FG, 25, alpha=ease((t - 0.1 - k * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    if e.get("siguiente"): T(f, XR, 0.46, "الحلقة القادمة: " + e["siguiente"], GOLD, 26, "bold", alpha=b)
    T(f, XR, 0.41, f"اشترك في قناة {MARCA} · حلقة جديدة كل سبت", BLUE, 24, "bold", alpha=b)
    aviso = (f"إخلاء مسؤولية: محتوى تعليمي وإعلامي فقط، وليس توصية استثمارية ولا دعوة لشراء أو بيع أي سهم. {VJ['nombre']} مجرد مثال للشرح. "
             "الأرقام من القوائم المالية الرسمية للشركة ومن TradingView، والحسابات الخاصة موضحة بعبارة «محسوب». لا نصدر أسعارًا مستهدفة. "
             "لا نملك مراكز في الأسهم المذكورة. الاستثمار في الأسهم ينطوي على مخاطر. النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي.")
    T(f, XR, 0.33, wrap(aviso, 120), MUTED, 16, linespacing=1.6, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=60, y=70)


TIPOS = {"portada": s_portada, "puntos": s_puntos, "cuenta": s_cuenta, "cascada": s_cascada, "barras": s_barras, "kpis": s_kpis,
         "formula": s_formula, "fin": s_fin}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"سلسلة {SERIE} · محتوى تعليمي وليس توصية استثمارية · {MARCA}", GOLD, 18, 46); band = np.array([0x13, 0x29, 0x4B], np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 28, 54, "bold") for l in (textwrap.wrap(s, 75) or [s])]
        return SUB[s]

    def ov(fr, j, ts, _t=0):
        fr = fr.copy(); bh = 46
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0xD4, 0xAF, 0x37)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); h = 54 * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.25 + np.array([11, 26, 46], np.float32) * 0.75).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * 54)
                break
        return fr
    return ov


def frame(i, t):
    e = ESC[i]; a = TIPOS[e["tipo"]](i, e, t)
    return a if e["tipo"] in BIG else with_logo(a, LG, x=40, y=40)


def control():
    err = []
    for k in ("base", "capitulo_n", "simbolo", "ticker", "nombre", "tema", "escenas", "info", "miniatura", "publicar"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") not in BIG and not (e.get("fuente") or VJ.get("fuente_general")): err.append(f"escena {k}: sin fuente")
        for mal in (r"اشتر(?!اك)", "بِع ", "سعر مستهدف", "رخيص", "فرصة شراء", "ننصح"):   # «اشتراك» (suscripción) no cuenta
            if re.search(mal, e.get("voz", "")): err.append(f"escena {k}: palabra de recomendación «{mal}» en la locución")
    if not any(e.get("tipo") == "fin" for e in ESC): err.append("falta la escena fin")
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(frame(j, 1.0), j, 1.0, 0)).save(os.path.join(AUD, f"prev_{j:02d}_{e.get('id', e['tipo'])}.png"))
        pal = sum(len(e["voz"].split()) for e in ESC); print("palabras", pal, "· duración estimada (Azure ~1,85 palabras/s)", round(pal / 1.85 + 1.05 * len(ESC)), "s"); sys.exit()
    VV = [voz_frases(e["voz"], AUD) for e in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [0.25 + len(a) / sr + 0.8 for a, _, _, _ in VV]; durs[-1] += 1.5
    print("voz", motor, "duración prevista", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s")
    leads = [0.25] * len(ESC)
    times, t0 = render([lambda t, j=j: frame(j, t) for j in range(len(ESC))], durs, ([v[0] for v in VV], leads), sr, W, H, 30, OUT,
                       os.path.join(AUD, "cap-silent.mp4"), os.path.join(AUD, "cap.wav"), overlay=overlay([v[2] for v in VV], leads))
    srt([v[2] for v in VV], times, leads, f"{DIR}/subtitulos-{BASE}-Nabd.srt")
    json.dump([(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/guion-{BASE}-Nabd.md", "w") as g:
        g.write(f"# {SERIE} · الحلقة {VJ['capitulo_n']}: {VJ['tema']} ({VJ['nombre']}, {VJ['ticker']})\n\nVoz: {motor} · Duración {t0:.0f} s\n\n| Tiempo | Escena | Texto |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
