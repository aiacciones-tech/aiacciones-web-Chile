# Short vertical (1080x1920, 45-60 s) «Wochenkalender der Quartalszahlen» de Wall Street auf Deutsch (Daniel, 22-nov-2026).
# Cada domingo: qué acciones de las 22 seguidas (ge/serie20: las 20 grandes + ANT + SPCX) presentan resultados de lunes a viernes,
# con día, antes/después de la apertura y el consenso (BPA e ingresos). Si no reporta ninguna (o muy pocas), modo «proximos»: las siguientes fechas.
# Voz: Azure de-DE-ConradNeural si VOZ_DIR tiene los wav de TODAS las frases (calendario-voz-GE.yml); si no, Piper (nunca se mezclan).
# Uso: AUD=<scratch> [VOZ_DIR=<wav>] python3 make_calendario.py <carpeta de la semana>/calendario.json [preview]
# Escenas: gancho, empresa (una por acción, orden cronológico), fin. Zonas seguras de Shorts: el texto va entre y=0.22 y 0.90, x desde 0.08.
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *
from PIL import Image
W, H, FPS = 1080, 1920, 30
AUD = os.environ.get("AUD", "aud"); MAXDUR, MINDUR = 60.0, 40.0
LG = load_logo(150); LGB = load_logo(260)
XL = 0.08


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="left", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def caja(f, x, y, w, h, c, alpha=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=alpha, figure=f))


def top(f, e):
    T(f, XL, 0.845, S["cabecera"], GOLD, 32, "bold")
    T(f, XL, 0.818, S["rango"] if S["modo"] == "semana" else "Die nächsten Termine", MUTED, 28, "bold")
    tot = sum(1 for x in S["escenas"] if x["tipo"] == "empresa")
    for i in range(tot):
        caja(f, XL + i * 0.075, 0.80, 0.06, 0.006, GOLD if i < e["n"] else DIM)


def s_gancho(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XL, 0.81, S["cabecera"], GOLD, 38, "bold", alpha=a)
    caja(f, 0, 0.695, 1.0, 0.09, GOLD, a)
    T(f, XL, 0.74, S["rango"], BG, 52, "bold", va="center", alpha=a)
    T(f, XL, 0.66, e["titulo"], FG, 84, "bold", va="top", linespacing=1.05, alpha=ease((t - 0.1) / 0.5))
    T(f, XL, 0.49, e["sub"], BLUE, 34, "bold", va="top", linespacing=1.4, alpha=ease((t - 0.25) / 0.5))
    for i, nom in enumerate(e.get("lista", [])):
        b = ease((t - 0.35 - i * 0.12) / 0.4); y = 0.49 - (e["sub"].count("\n") + 1) * 0.03 - 0.045 - i * 0.048
        caja(f, XL, y - 0.004, 0.012, 0.022, GOLD, b)
        T(f, XL + 0.03, y, nom, FG, 40, "bold", alpha=b)
    return with_logo(to_arr(f), LG, x=W - 150 - 90, y=150)


def s_empresa(e, t):
    f = fig(W, H); top(f, e); a = ease(t / 0.4)
    caja(f, 0, 0.69, 1.0, 0.085, GOLD, a)
    T(f, XL, 0.7325, e["dia"], BG, 56, "bold", va="center", alpha=a)
    T(f, XL, 0.655, e["momento"], FG, 40, "bold", va="top", alpha=a)
    T(f, XL, 0.617, e["hora"], MUTED, 30, va="top", alpha=a)
    b = ease((t - 0.12) / 0.4)
    f.text(XL, 0.50, e["nombre"], color=FG, fontsize=110 if len(e["nombre"]) < 10 else 88, weight="bold", ha="left", alpha=b)
    T(f, XL, 0.465, e["ticker"], GOLD, 40, "bold", alpha=b)
    est = e.get("estado", "")
    if est:
        c = TEAL if est == "bestätigt" else BLUE
        T(f, 0.84, 0.465, ("✓ " if est == "bestätigt" else "") + "Termin " + est, c, 30, "bold", ha="right", alpha=b)
    items = [(e.get("umsatz"), "Umsatz (Konsens)"), (e.get("eps"), "Gewinn je Aktie (Konsens)")]
    items = [x for x in items if x[0]]
    for i, (big, lab) in enumerate(items):
        c = ease((t - 0.25 - i * 0.15) / 0.4); y = 0.36 - i * 0.105
        f.text(XL, y, big, color=TEAL, fontsize=84, weight="bold", ha="left", alpha=c)
        T(f, XL, y - 0.032, lab, FG, 32, alpha=c)
    if e.get("nota"): T(f, XL, 0.36 - len(items) * 0.105 + 0.02, e["nota"], MUTED, 28, alpha=ease((t - 0.45) / 0.4))
    return with_logo(to_arr(f), LG, x=W - 150 - 90, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XL, 0.765, S["cabecera"], GOLD, 36, "bold", alpha=a)
    emp = [x for x in S["escenas"] if x["tipo"] == "empresa"]
    for i, x in enumerate(emp):
        b = ease((t - 0.1 - i * 0.08) / 0.4); y = 0.715 - i * 0.05
        T(f, XL, y, x["dia"], MUTED, 32, "bold", alpha=b)
        T(f, 0.46, y, f"{x['nombre']} ({x['ticker']})", FG, 32, "bold", alpha=b)
    y0 = 0.715 - len(emp) * 0.05 - 0.03
    T(f, XL, y0, e["titular"], GOLD, 42, "bold", va="top", linespacing=1.15, alpha=ease((t - 0.2) / 0.5))
    T(f, XL, y0 - 0.115, "▶ " + MARCA, BLUE, 34, "bold", alpha=ease((t - 0.25) / 0.5))
    T(f, XL, y0 - 0.14, S["fuente"] + "\nKonsens = Schätzung der Analysten. Termine können sich ändern."
      "\nKeine Anlageberatung. Nur zu Informationszwecken.\nText, Stimme und Grafiken mit KI erstellt.", MUTED, 22, linespacing=1.5, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=(W - 260) // 2, y=120)


RX = {"gancho": s_gancho, "empresa": s_empresa, "fin": s_fin}
def frame(e, t): return RX[e["tipo"]](e, t)


def control(S):
    """Control de calidad antes de renderizar: escenas completas, orden cronológico, aviso legal y frase de cierre."""
    E = S["escenas"]; err = []
    if E[0]["tipo"] != "gancho" or E[-1]["tipo"] != "fin": err.append("la primera escena debe ser gancho y la última fin")
    emp = [e for e in E if e["tipo"] == "empresa"]
    if not 1 <= len(emp) <= 6: err.append(f"{len(emp)} empresas (1-6 caben en 60 s)")
    for e in emp:
        for k in ("nombre", "ticker", "dia", "momento", "voz"):
            if not e.get(k): err.append(f"{e.get('ticker')}: falta {k}")
        if e.get("ticker") not in S.get("verificacion", {}): err.append(f"{e.get('ticker')}: falta su fuente en verificacion")
    if "Folge dem Kanal für die Analyse jeder Zahlenvorlage" not in E[-1]["voz"]: err.append("falta la frase de cierre")
    if "Keine Anlageberatung" not in E[-1]["voz"]: err.append("falta el aviso en la voz del cierre")
    if err: sys.exit("control de calidad:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); E = S["escenas"]; base = os.path.dirname(os.path.abspath(sys.argv[1]))
    S["out"] = os.path.join(base, S["out"]); os.makedirs(AUD, exist_ok=True); control(S)
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"cal_prev_{i}.png"))
        sys.exit()
    vd = os.environ.get("VOZ_DIR")
    if vd and not all(os.path.exists(os.path.join(vd, clave_frase(x) + ".wav")) for e in E for x in frases(e["voz"])):
        print("VOZ_DIR no tiene todas las frases: sale entero con Piper (no se mezclan voces)"); os.environ.pop("VOZ_DIR")
    clips = [voz_frases(e["voz"], AUD)[:2] for e in E]; sr = clips[0][1]
    print("voz:", "azure" if os.environ.get("VOZ_DIR") else "piper")
    LEAD, TAIL = 0.10, 0.35
    durs = [LEAD + len(a) / sr + TAIL for a, _ in clips]; durs[-1] += 1.5
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if sum(durs) > MAXDUR: sys.exit(f"demasiado largo: {sum(durs):.1f} s (máx {MAXDUR}). Acorta la voz.")
    if sum(durs) < MINDUR: print(f"AVISO: {sum(durs):.1f} s, por debajo de {MINDUR} s")
    times, t0 = render([lambda t, e=e: frame(e, t) for e in E], durs, ([a for a, _ in clips], [LEAD] * len(E)), sr, W, H, FPS, S["out"],
                       os.path.join(AUD, "cal-silent.mp4"), os.path.join(AUD, "cal-full.wav"), loud=-14, ANIM=24, XF=6)
    # miniatura (Telegram, Threads y YouTube): la escena de resumen
    Image.fromarray(frame(E[-1], 1.0)).save(os.path.join(base, S["out"].replace(".mp4", ".png").replace("calendario-", "miniatura-calendario-")))
    json.dump({"duracion": round(t0, 1), "voz": "azure" if os.environ.get("VOZ_DIR") else "piper", "inicios": times},
              open(os.path.join(base, "times.json"), "w"))
    print("listo", S["out"], round(t0, 1), "s")
