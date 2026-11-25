# Vídeo de un directo en momentos clave de Saudi Arabia AI Stocks (Daniel, 24-nov-2026): Fed, OPEP+, presupuesto saudí, resultados anuales.
# 1920x1080, 8-12 min de contenido + 60 s de cuenta atrás al principio (sin voz: es lo que ve la audiencia mientras entra al directo).
# Voz Azure ar-SA-HamedNeural frase a frase con subtítulos (como la serie educativa). Escenas en eventos/<base>/video.json:
#   portada · cifras (≤4 cifras grandes) · puntos (≤5 [título, texto]) · linea (series de datos con fuente) · fin (claves ≤4 + aviso legal)
# Uso: AUD=<scratch> [VOZ_DIR=<wav de Azure>] python3 make_directo.py <carpeta del evento> [preview]
#   Escribe live-<base>-saudi.mp4, times.json y script-<base>-saudi.md en la carpeta del evento.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "educativo"), os.path.join(HERE, "..", "diario")]
from comun_leccion import *

DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json"))
W, H = 1920, 1080
MIN_S, MAX_S = 420, 780   # contenido de 7 a 13 min (objetivo 8-12), sin contar la cuenta atrás
CUENTA_S = 60
BASE = VJ["base"]; OUT = f"{DIR}/live-{BASE}-saudi.mp4"
ESC = [dict(e) for e in VJ["escenas"]]
LG = load_logo(120); LGB = load_logo(230)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]
XR = 0.94
ETQ = "بث مباشر"


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def base(i, kicker, title):
    f = fig(W, H)
    T(f, XR, 0.905, kicker, GOLD, 26, "bold")
    T(f, XR, 0.825, title, FG, 42 if len(title) <= 55 else 34, "bold")
    rect(f, 0.10, 0.905, 0.105, 0.045, NEG); T(f, 0.1525, 0.927, "● " + ETQ, FG, 20, "bold", ha="center", va="center")
    T(f, 0.10, 0.875, VJ["evento"], MUTED, 17, ha="left")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n):
        rect(f, XR - (k + 1) * w + 0.008, 0.975, w - 0.008, 0.008, GOLD if k < CAP_IDX[i] else DIM)
    return f


def fuente(f, s):
    if s: T(f, XR, 0.13, "المصدر: " + s, MUTED, 14, ancho=200, linespacing=1.35)


def s_cuenta(seg):
    def fr(t):
        f = fig(W, H)
        rect(f, 0, 0.60, 1.0, 0.2, GOLD)
        T(f, XR, 0.745, f"{MARCA} · {ETQ}", BG, 32, "bold", va="center")
        T(f, XR, 0.655, VJ["titulo"], BG, 54 if len(VJ["titulo"]) <= 34 else 42, "bold", va="center")
        T(f, 0.5, 0.45, "يبدأ البث بعد", FG, 40, "bold", ha="center")
        r = max(0, int(round(seg - t))); T(f, 0.5, 0.29, f"{r // 60}:{r % 60:02d}", GOLD, 110, "bold", ha="center")
        T(f, 0.5, 0.17, "اكتب في الدردشة من أين تتابعنا · محتوى إعلامي وليس توصية استثمارية", MUTED, 24, ha="center")
        return with_logo(to_arr(f), LGB, x=80, y=40)
    return fr


def s_portada(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    rect(f, 0.19, 0.84, 0.15, 0.06, NEG, a); T(f, 0.265, 0.87, "● " + ETQ, FG, 28, "bold", ha="center", va="center", alpha=a)
    T(f, XR, 0.87, MARCA, GOLD, 30, "bold", alpha=a, va="center")
    rect(f, 0, 0.60, 1.0, 0.2, GOLD, a)
    T(f, XR, 0.745, VJ["evento"], BG, 34, "bold", va="center", alpha=a)
    T(f, XR, 0.652, VJ["titulo"], BG, 64 if len(VJ["titulo"]) <= 30 else 50, "bold", va="center", alpha=a)
    T(f, XR, 0.50, VJ["fecha_ar"], FG, 40, "bold", alpha=ease((t - 0.15) / 0.5))
    if e.get("sub"): T(f, XR, 0.42, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5), ancho=90)
    T(f, XR, 0.28, "محتوى إعلامي وليس توصية استثمارية", BLUE, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=80, y=40)


def s_cifras(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); C = e["cifras"][:4]; n = len(C); w = 0.88 / n
    for k, c in enumerate(C):
        b = ease((t - k * 0.1) / 0.4); x0 = XR - (k + 1) * w + 0.01
        rect(f, x0, 0.30, w - 0.02, 0.40, PANEL, b); rect(f, x0, 0.695, w - 0.02, 0.006, c.get("color", GOLD), b)
        cx = x0 + (w - 0.02) / 2
        # la cifra sin ar(): el reordenado árabe cambia el punto decimal
        f.text(cx, 0.53, c["valor"], color=col(c.get("color", GOLD)), fontsize=58 if len(c["valor"]) <= 8 else 42, weight="bold", family="DejaVu Sans", ha="center", va="center", alpha=b)
        T(f, cx, 0.40, c["etiqueta"], FG, 22, "bold", ha="center", va="center", alpha=b, ancho=max(20, int(100 / n)), linespacing=1.3)
    if e.get("nota"): T(f, XR, 0.22, e["nota"], MUTED, 22, alpha=ease((t - 0.4) / 0.4), ancho=120)
    fuente(f, e.get("fuente"))
    return to_arr(f)


def s_puntos(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); P = e["puntos"][:5]; hh = min(0.12, 0.6 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.75 - (k + 1) * hh; ym = y + (hh - 0.014) / 2
        rect(f, 0.06, y, 0.88, hh - 0.014, PANEL, b); rect(f, XR - 0.005, y, 0.005, hh - 0.014, GOLD, b)
        T(f, 0.925, ym, f"{k + 1}", GOLD, 34, "bold", va="center", alpha=b)
        T(f, 0.895, ym, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.64, ym, txt, MUTED, 21, va="center", alpha=b, ancho=70, linespacing=1.3)
    fuente(f, e.get("fuente"))
    return to_arr(f)


def s_linea(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); ax = f.add_axes([0.08, 0.20, 0.84, 0.54]); clean(ax)
    prog = ease(t / 0.8)
    for k, s in enumerate(e["series"]):
        v = np.array(s["valores"], float); x = np.arange(len(v)); m = max(2, int(round(len(v) * prog)))
        c = col(s.get("color", [GOLD, TEAL, BLUE, NEG][k % 4]))
        ax.plot(x[:m], v[:m], color=c, lw=3.2, label=ar(s["nombre"]))
        if m == len(v):
            ax.annotate(s.get("etiqueta_final", f"{v[-1]:,.{e.get('decimales', 2)}f}"), (x[-1], v[-1]), color=c, fontsize=18, weight="bold",
                        xytext=(8, 0), textcoords="offset points", va="center")
        ax.set_xlim(-0.5, len(v) - 0.5 + max(1, len(v) * 0.08))
    F = e["series"][0]["fechas"]; step = max(1, len(F) // 8)
    ax.set_xticks(range(0, len(F), step), [ar(F[j]) for j in range(0, len(F), step)])
    ax.grid(axis="y", color=DIM, lw=0.8); ax.yaxis.tick_right()
    if len(e["series"]) > 1: ax.legend(loc="upper left", frameon=False, labelcolor=FG, fontsize=18)
    if e.get("unidad"): T(f, XR, 0.775, e["unidad"], MUTED, 19, "bold")
    if e.get("nota"): T(f, 0.06, 0.775, e["nota"], GOLD, 21, "bold", ha="left", alpha=ease((t - 0.5) / 0.4))
    fuente(f, e.get("fuente"))
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.86, VJ["titulo"], FG, 44, "bold", alpha=a)
    T(f, XR, 0.795, "الخلاصة", GOLD, 32, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, XR, 0.725 - k * 0.062, "• " + c, FG, 26, alpha=ease((t - 0.1 - k * 0.1) / 0.4), ancho=110)
    b = ease((t - 0.3) / 0.5)
    T(f, XR, 0.42, "اشترك في القناة وفعّل الجرس ليصلك تنبيه البث المباشر القادم", BLUE, 26, "bold", alpha=b)
    aviso = ("تنبيه مهم: هذا المحتوى إعلامي فقط، ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية. "
             "الأرقام من المصادر المذكورة على الشاشة وفي وصف الفيديو. لا نملك مراكز في الأسهم المذكورة. الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال. "
             "هذا البث مُعدّ مسبقًا: النص والصوت (صوت اصطناعي) والرسوم من إعداد أدوات الذكاء الاصطناعي.")
    T(f, XR, 0.35, aviso, MUTED, 16, ancho=150, linespacing=1.6, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=80, y=70)


TIPOS = {"portada": s_portada, "cifras": s_cifras, "puntos": s_puntos, "linea": s_linea, "fin": s_fin}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads, desde):
    pie = tira_texto(f"{MARCA} · {ETQ} · محتوى إعلامي وليس توصية استثمارية", GOLD, 18, 46); band = np.array(BANDA, np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 30, 56, "bold") for l in (partir(sub_pantalla(s), 72) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        if j < desde: return fr
        fr = fr.copy(); bh = 46; j -= desde
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
    for k in ("base", "evento", "titulo", "fecha_ar", "inicio", "escenas", "info"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k in ("titulo", "resumen", "lineas", "fuentes", "hashtags", "x"):
        if not VJ.get("info", {}).get(k): err.append(f"falta info.{k}")
    if ESC and (ESC[0]["tipo"] != "portada" or ESC[-1]["tipo"] != "fin"): err.append("la primera escena es portada y la última fin")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") in ("cifras", "linea") and not e.get("fuente"): err.append(f"escena {e.get('id')}: cifras sin fuente")
        if e.get("tipo") == "linea":
            for s in e["series"]:
                if len(s["valores"]) != len(s["fechas"]): err.append(f"escena {e.get('id')}: {s['nombre']} fechas y valores de distinto largo")
    for f in VJ.get("info", {}).get("fuentes", []):
        if not f.get("url"): err.append(f"fuente sin enlace: {f.get('dato')}")
    for p in ("توصية بالشراء", "اشترِ", "بِع ", "سعر مستهدف", "رخيص", "سيرتفع", "سينخفض", "سيصل"):
        for e in ESC:
            if p in e.get("voz", "") and "ليس" not in e["voz"]: err.append(f"escena {e.get('id')}: revisa «{p}» (sin previsiones ni recomendaciones)")
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    if PREVIEW:
        Image.fromarray(s_cuenta(CUENTA_S)(17.0)).save(os.path.join(AUD, "prev_00_cuenta.png"))
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC), 0)
        for j, e in enumerate(ESC): Image.fromarray(ov(frame(j, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"prev_{j + 1:02d}_{e.get('id', e['tipo'])}.png"))
        print("palabras", sum(len(e["voz"].split()) for e in ESC)); sys.exit()
    VV = [voz_frases(e["voz"], AUD) for e in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas: " + str([v[3] for v in VV]))
    durs = [0.15 + len(a) / sr + 0.9 for a, _, _, _ in VV]; durs[-1] += 8
    print("voz", motor, "duración prevista del contenido", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s")
    # la cuenta atrás: un fotograma por segundo de vídeo (cada segundo cambia el número), sin voz
    cuenta = s_cuenta(CUENTA_S); CC = {}
    fr_c = [lambda t, s=s: CC[s] if s in CC else CC.setdefault(s, cuenta(s)) for s in range(CUENTA_S)]
    frames = fr_c + [lambda t, j=j: frame(j, t) for j in range(len(ESC))]
    D = [1.0] * CUENTA_S + durs; A = [np.zeros(1, np.float32)] * CUENTA_S + [v[0] for v in VV]
    leads = [0.0] * CUENTA_S + [0.15] * len(ESC)
    times, t0 = render(frames, D, (A, leads), sr, W, H, 30, OUT, os.path.join(AUD, "live-silent.mp4"), os.path.join(AUD, "live.wav"),
                       overlay=overlay([v[2] for v in VV], leads[CUENTA_S:], CUENTA_S))
    times = times[CUENTA_S:]
    json.dump([("_cuenta", CUENTA_S)] + [(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)],
              open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/script-{BASE}-saudi.md", "w") as g:
        g.write(f"# {ETQ}: {VJ['titulo']} ({VJ['fecha_ar']})\n\nVoz: {motor} · Duración {t0:.0f} s (incluye {CUENTA_S} s de cuenta atrás)\n\n| Tiempo | Escena | Texto |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
