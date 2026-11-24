# Vídeo "evergreen" de búsqueda de Saudi Arabia AI Stocks: serie «دليل المستثمر في السوق السعودية» (Daniel, 24-nov-2026).
# Un tema de los que la gente busca en YouTube (cómo invertir, dividendos, Nomu, OPVs, TASI...) explicado con datos verificados y,
# cuando ayuda, con el gráfico real de TradingView. 1920x1080, 5-8 minutos, voz Azure ar-SA-HamedNeural, subtítulos en árabe.
# Reutiliza las piezas de la serie educativa (saudi/educativo/comun_leccion.py: voz frase a frase, subtítulos, render).
# Escenas en video.json → "escenas"; tipos: portada, puntos, tabla, historico, grafico, fin.
# Uso: AUD=<scratch> VELAS=<velas.json> [VOZ_DIR=<wav de Azure>] python3 make_guia.py <carpeta de la guía> [preview]
#   Escribe guide-<base>-saudi.mp4, times.json y script-<base>-saudi.md.
import os, sys, json, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "educativo")); sys.path.insert(0, HERE)
from comun_leccion import *
import campana
from tecnico import MESES

SERIE = "دليل المستثمر في السوق السعودية"
DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json"))
VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json"))) if VJ.get("simbolo") else None
W, H = 1920, 1080
MIN_S, MAX_S = 280, 500   # 5 a 8 minutos
BASE = VJ["base"]; OUT = f"{DIR}/guide-{BASE}-saudi.mp4"
CTA = campana.activa()
ESC = [dict(e) for e in VJ["escenas"]]
if CTA: ESC[-1]["voz"] = ESC[-1]["voz"] + " " + campana.VOZ
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
fecha_ar = lambda d: f"{d.day} {MESES[d.month - 1]} {d.year}"
if VEL:
    SER = VEL["series"][VJ["simbolo"]]
    VELAS = [v for v in SER["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]]; ULT = fecha_v(VELAS[-1]["t"])
    FUENTE_DATOS = SER.get("fuente", "TradingView")
else:
    VELAS, ULT, FUENTE_DATOS = [], None, ""
DEC = VJ.get("decimales", 2)
LG = load_logo(120); LGB = load_logo(230)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]
XR = 0.94


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def base(i, kicker, title):
    f = fig(W, H)
    T(f, XR, 0.905, kicker, GOLD, 26, "bold")
    T(f, XR, 0.825, title, FG, 42 if len(title) <= 55 else 34, "bold")
    T(f, 0.105, 0.925, SERIE, MUTED, 20, "bold", ha="left")
    T(f, 0.105, 0.885, VJ["tema_corto"], MUTED, 17, ha="left")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n):  # barra de progreso de derecha a izquierda
        rect(f, XR - (k + 1) * w + 0.008, 0.975, w - 0.008, 0.008, GOLD if k < CAP_IDX[i] else DIM)
    return f


def fuente(f, s): T(f, XR, 0.13, s, MUTED, 14, ancho=200, linespacing=1.35)


# ---------- escenas ----------
def s_portada(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, XR, 0.88, f"{MARCA} · {SERIE}", GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.62, 1.0, 0.2, GOLD, a)
    T(f, XR, 0.765, e.get("etiqueta", "دليل شامل"), BG, 34, "bold", va="center", alpha=a)
    T(f, XR, 0.672, VJ["tema"], BG, 64 if len(VJ["tema"]) <= 30 else 50, "bold", va="center", alpha=a)
    if e.get("sub"): T(f, XR, 0.52, e["sub"], FG, 38, "bold", alpha=ease((t - 0.15) / 0.5))
    for k, s in enumerate(e.get("indice", [])[:5]):
        T(f, XR, 0.445 - k * 0.05, "• " + s, MUTED, 26, alpha=ease((t - 0.25 - k * 0.08) / 0.5))
    T(f, XR, 0.16, "محتوى تعليمي وليس توصية استثمارية", BLUE, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=80, y=40)


def s_puntos(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); P = e["puntos"][:5]; hh = min(0.12, 0.6 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.68 - (k + 1) * hh; ym = y + (hh - 0.014) / 2
        rect(f, 0.06, y, 0.88, hh - 0.014, PANEL, b); rect(f, XR - 0.005, y, 0.005, hh - 0.014, e.get("colores", [GOLD] * 5)[k], b)
        T(f, 0.925, ym, f"{k + 1}", GOLD, 34, "bold", va="center", alpha=b)
        T(f, 0.895, ym, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.64, ym, txt, MUTED, 21, va="center", alpha=b, ancho=70, linespacing=1.3)
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def s_tabla(i, e, t):
    """Tabla de derecha a izquierda: "columnas" (cabecera) y "filas" (listas de textos); "resaltar": índices de fila en dorado."""
    f = base(i, e["kicker"], e["titulo"]); C = e["columnas"]; R = e["filas"][:7]
    anchos = e.get("anchos", [1 / len(C)] * len(C)); x0, x1 = 0.06, XR; ww = x1 - x0
    xs, acc = [], x1
    for a in anchos: xs.append((acc, acc - a * ww)); acc -= a * ww
    hh = min(0.085, 0.56 / (len(R) + 1)); y = 0.70
    rect(f, x0, y - hh + 0.01, ww, hh - 0.012, GOLD)
    for (xa, xb), c in zip(xs, C): T(f, xa - 0.012, y - hh / 2 + 0.004, c, BG, 24, "bold", va="center")
    for k, fila in enumerate(R):
        b = ease((t - 0.1 - k * 0.08) / 0.4); yy = y - (k + 1) * hh
        rect(f, x0, yy - hh + 0.01, ww, hh - 0.012, PANEL, b)
        dest = k in e.get("resaltar", [])
        for j, ((xa, xb), c) in enumerate(zip(xs, fila)):
            T(f, xa - 0.012, yy - hh / 2 + 0.004, c, GOLD if (dest or j == 0) else FG, 23, "bold" if j == 0 or dest else "normal", va="center", alpha=b,
              ancho=int((xa - xb) * 110), linespacing=1.2)
    if e.get("nota"): T(f, XR, y - (len(R) + 1) * hh - 0.04, e["nota"], BLUE, 21, "bold", ancho=150)
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def _semanal(V):
    """Cierres semanales (último cierre de cada semana ISO) para gráficos de muchos años."""
    out = {}
    for v in V:
        d = fecha_v(v["t"]); out[d.isocalendar()[:2]] = (d, v["c"])
    return list(out.values())


def s_historico(i, e, t):
    """Línea de cierres semanales de muchos años con marcas {fecha, texto, campo h|l|c} sobre el máximo/mínimo/cierre de ese día."""
    f = base(i, e["kicker"], e["titulo"])
    d0 = e.get("desde", "0000"); d1 = e.get("hasta", "9999")
    V = [v for v in VELAS if d0 <= fecha_v(v["t"]).isoformat() <= d1]; S = _semanal(V); n = len(S)
    ax = f.add_axes([0.06, 0.20, 0.80, 0.56]); clean(ax)
    ys = np.array([c for _, c in S]); xs = np.arange(n); rev = max(2, int(n * ease(t * 1.1)))
    ax.fill_between(xs[:rev], ys[:rev], ys.min() * 0.85, color=TEAL, alpha=0.12, lw=0); ax.plot(xs[:rev], ys[:rev], color=TEAL, lw=2.4)
    ymax = max(ys.max(), max((v["h"] for v in V), default=0)); ax.set_ylim(ys.min() * 0.75, ymax * 1.12); ax.set_xlim(-n * 0.02, n * 1.04)
    pos = {}
    for j, (d, _) in enumerate(S): pos[d.isocalendar()[:2]] = j
    byd = {fecha_v(v["t"]).isoformat(): v for v in V}
    for k, m in enumerate(e.get("marcas", [])):
        v = byd.get(m["fecha"]); a = ease((t - 0.5 - k * 0.12) / 0.3)
        if not v: continue
        j = pos[fecha_v(v["t"]).isocalendar()[:2]]; yv = ys[j]; arriba = m.get("campo") != "l"  # punto sobre la línea semanal; la cifra exacta va en el texto
        if j > rev: continue
        ax.plot([j], [yv], "o", color=GOLD, ms=11, alpha=a)
        dy = (ymax - ys.min()) * m.get("dy", 0.09 if arriba else -0.13)
        ax.annotate(ar(m["texto"]), (j, yv), (j + m.get("dx", 0) * n, yv + dy), color=GOLD, fontsize=20, weight="bold", ha="center", va="center", alpha=a,
                    arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.2, alpha=a), bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=GOLD, lw=1, alpha=0.9 * a))
    ax.yaxis.tick_left(); ax.tick_params(labelsize=15); ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    ax.set_yticks(ax.get_yticks()[1:-1]); ax.set_yticklabels([num(y, 0) for y in ax.get_yticks()])
    tk, prev = [], None
    for j, (d, _) in enumerate(S):
        if d.year != prev:
            if d.month == 1: tk.append((j, str(d.year)))
            prev = d.year
    step = max(1, len(tk) // 12); ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]])
    T(f, XR, 0.785, e.get("leyenda", f"{VJ['nombre']} · إغلاق أسبوعي"), MUTED, 19, "bold")
    if e.get("nota"): T(f, 0.06, 0.785, e["nota"], GOLD, 21, "bold", ha="left", alpha=ease((t - 0.5) / 0.4))
    fuente(f, e.get("fuente", f"البيانات: {FUENTE_DATOS} ({VJ['simbolo']}، حتى {fecha_ar(ULT)})."))
    return to_arr(f)


def _rango(e):
    d0 = dt.date.fromisoformat(e["desde"]) if e.get("desde") else None; d1 = dt.date.fromisoformat(e["hasta"]) if e.get("hasta") else ULT
    return [v for v in VELAS if (d0 is None or fecha_v(v["t"]) >= d0) and fecha_v(v["t"]) <= d1]


def s_grafico(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); V = _rango(e); n = len(V)
    ax = f.add_axes([0.06, 0.24, 0.80, 0.53]); clean(ax)
    rev = n if not e.get("animar_velas") else max(2, int(n * ease(t * 1.15)))
    o = np.array([v["o"] for v in V]); hi = np.array([v["h"] for v in V]); lo = np.array([v["l"] for v in V]); c = np.array([v["c"] for v in V])
    up = c >= o; xs = np.arange(n); wd = 0.65 if n < 160 else 0.75
    ymin, ymax = lo.min(), hi.max(); pad = (ymax - ymin) * 0.08
    ax.set_ylim(ymin - pad * 2.0, ymax + pad * 1.8); ax.set_xlim(-1, n + (n * 0.1))
    ax.vlines(xs[:rev], lo[:rev], hi[:rev], color=[TEAL if u else NEG for u in up[:rev]], lw=1.1 if n > 160 else 1.6)
    ax.bar(xs[:rev], np.maximum(np.abs(c - o), (ymax - ymin) * 0.002)[:rev], bottom=np.minimum(o, c)[:rev], width=wd, color=[TEAL if u else NEG for u in up[:rev]])
    ax.yaxis.tick_left(); ax.tick_params(labelsize=15); ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk, prev = [], None
    for j, v in enumerate(V):
        d = fecha_v(v["t"])
        if d.month != prev: tk.append((j, ar(MESES[d.month - 1]) + (f"\n{d.year}" if d.month == 1 or not tk else ""))); prev = d.month
    step = 1 if len(tk) <= 9 else 2; ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]])
    T(f, XR, 0.785, f"{VJ['nombre']} · شموع يومية", MUTED, 19, "bold")
    if e.get("nota"): T(f, 0.06, 0.785, e["nota"], GOLD, 21, "bold", ha="left", alpha=ease((t - 0.5) / 0.4))
    fuente(f, f"البيانات: {FUENTE_DATOS} ({VJ['simbolo']}، حتى {fecha_ar(ULT)}).")
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.86, VJ["tema"], FG, 44 if len(VJ["tema"]) <= 40 else 36, "bold", alpha=a)
    T(f, XR, 0.795, "الخلاصة", GOLD, 32, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, XR, 0.725 - k * 0.062, "• " + c, FG, 26, alpha=ease((t - 0.1 - k * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    if e.get("siguiente"): T(f, XR, 0.45, "الدليل القادم: " + e["siguiente"], GOLD, 28, "bold", alpha=b)
    if CTA: T(f, XR, 0.395, f"{campana.TITULO}: {campana.LINEA1} · {campana.LINEA2}", BLUE, 23, "bold", alpha=b)
    else: T(f, XR, 0.395, "اشترك في القناة ليصلك كل جديد عن السوق السعودية", BLUE, 25, "bold", alpha=b)
    aviso = ("تنبيه مهم: هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية ولا استشارة مالية شخصية. "
             "الأرقام والقواعد المذكورة صحيحة حسب المصادر في تاريخ إعداد الفيديو، وقد تتغير، فتحقق منها لدى هيئة السوق المالية وتداول السعودية. "
             "الأداء السابق لا يضمن النتائج المستقبلية، والاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال. "
             "النص والصوت (صوت اصطناعي) والرسوم من إعداد أدوات الذكاء الاصطناعي.")
    T(f, XR, 0.32, aviso, MUTED, 16, ancho=150, linespacing=1.6, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=80, y=70)


TIPOS = {"portada": s_portada, "puntos": s_puntos, "tabla": s_tabla, "historico": s_historico, "grafico": s_grafico, "fin": s_fin}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"{MARCA} · {SERIE} · محتوى تعليمي وليس توصية استثمارية", GOLD, 18, 46); band = np.array(BANDA, np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 30, 56, "bold") for l in (partir(sub_pantalla(s), 72) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        fr = fr.copy(); bh = 46
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0xE3, 0xC4, 0x5E)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = 56; h = lh * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array([6, 25, 26], np.float32) * 0.72).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * lh)
                break
        return fr
    return ov


def frame(i, t):
    e = ESC[i]; a = TIPOS[e["tipo"]](i, e, t)
    return a if e["tipo"] in BIG else with_logo(a, LG, x=40, y=30)


def control():
    err = []
    for k in ("base", "numero", "tema", "tema_corto", "palabra_clave", "escenas", "info", "miniatura", "short"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") in ("grafico", "historico") and not VELAS: err.append(f"escena {k}: gráfico sin 'simbolo'/velas")
        if e.get("tipo") == "historico":
            fechas = {fecha_v(v["t"]).isoformat() for v in VELAS}
            for m in e.get("marcas", []):
                if m["fecha"] not in fechas: err.append(f"escena {k}: marca {m['fecha']} sin vela")
    if VJ.get("ultima_vela") and ULT and VJ["ultima_vela"] != ULT.isoformat(): err.append(f"velas.json acaba el {ULT}, video.json espera {VJ['ultima_vela']}")
    import re
    for p in ("توصية بالشراء", "اشترِ", "بِع", "سعر مستهدف", "رخيص", "سيرتفع", "سينخفض", "سيصل", "مضمون", "ربح مؤكد"):
        for e in ESC:  # palabra completa (con prefijos ال/و/ف/ب), para que «ترخيص» no salte por «رخيص»
            if re.search(r"(?<![\u0600-\u06FF])(?:ال|و|ف|ب)?" + p + r"(?![\u0600-\u06FF])", e.get("voz", "")) and "ليس" not in e["voz"]:
                err.append(f"escena {e.get('id')}: revisa «{p}»")
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
                       os.path.join(AUD, "guia-silent.mp4"), os.path.join(AUD, "guia.wav"), overlay=overlay([v[2] for v in VV], leads))
    json.dump([(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/script-{BASE}-saudi.md", "w") as g:
        g.write(f"# {SERIE} · {VJ['numero']}: {VJ['tema']}\n\nPalabra clave: {VJ['palabra_clave']} · Voz: {motor} · Duración {t0:.0f} s\n\n| Tiempo | Escena | Texto |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
