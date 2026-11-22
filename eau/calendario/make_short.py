# Short vertical (1080x1920, 45-60 s) «تقويم النتائج الأسبوعي» de @AIStocksUAE: las empresas que reportan de lunes a viernes,
# primero ADX/DFM y después las grandes de EE. UU., en orden cronológico. Voz Azure ar-AE-HamdanNeural (VOZ_DIR, voz-eau.yml)
# o, si falta, la Piper del canal (ar_JO-kareem).
# Uso: [VOZ_DIR=<wav de Azure>] AUD=<scratch> python3 make_short.py <carpeta de la semana>/short.json [preview]
# Escenas: gancho, local (ADX/DFM), empresa (una por compañía), fin. Texto entre y=0.25 y 0.88, alineado a la derecha en x=0.86
# (zonas seguras de Shorts: arriba la búsqueda, abajo título y canal, a la derecha los botones).
import os, sys, json, wave, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "diario")); sys.path.insert(0, HERE)
from comun import *
import comun
from voz_textos import clave
W, H, FPS = 1080, 1920, 30
AUD = os.environ.get("AUD", "aud"); MINDUR, MAXDUR = 45.0, 60.0
LG = load_logo(150); LGB = load_logo(240)
XR = 0.86
AVISO = "محتوى إعلامي، وليس توصية استثمارية."


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def L(f, x, y, s, c=FG, fs=30, w="bold", ha="right", **k):  # latín/cifras, sin reshaper
    return f.text(x, y, s, color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def caja(f, x0, y0, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x0, y0), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def top(f, e):
    T(f, XR, 0.855, S["cabecera"], GOLD, 30, "bold")
    tot = sum(1 for x in S["escenas"] if "n" in x)
    for i in range(tot):
        caja(f, XR - (i + 1) * 0.075 + 0.015, 0.84, 0.06, 0.006, GOLD if i < e["n"] else DIM)


def s_gancho(e, t):
    f = fig(W, H); a = ease(t / 0.4)
    T(f, XR, 0.80, e["kicker"], GOLD, 40, "bold", alpha=a)
    caja(f, 0, 0.67, 1.0, 0.105, GOLD, a)
    T(f, XR, 0.722, e["semana"], BG, 70, "bold", va="center", alpha=a)
    b = ease((t - 0.15) / 0.4)
    T(f, XR, 0.59, e["estrella"], FG, 92, "bold", alpha=b)
    L(f, XR, 0.545, e["ticker"], BLUE, 44, alpha=b)
    T(f, XR, 0.46, e["mas"], TEAL, 54, "bold", alpha=ease((t - 0.3) / 0.4), va="top", linespacing=1.3)
    if e.get("nota"): T(f, XR, 0.31, e["nota"], MUTED, 34, alpha=ease((t - 0.45) / 0.4), va="top", linespacing=1.4)
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_local(e, t):
    f = fig(W, H); top(f, e); a = ease(t / 0.4)
    T(f, XR, 0.76, f"{e['n']}. {e['label']}", MUTED, 42, "bold", alpha=a)
    T(f, XR, 0.70, e["titular"], FG, 58, "bold", alpha=a, va="top", linespacing=1.1)
    for i, (big, lab, c) in enumerate(e.get("items", [])):
        b = ease((t - 0.2 - i * 0.15) / 0.4); y = 0.47 - i * 0.12
        T(f, XR, y, big, c, 54, "bold", alpha=b)
        T(f, XR, y - 0.04, lab, FG, 32, alpha=b)
    if e.get("nota"): T(f, XR, 0.36, e["nota"], MUTED, 30, alpha=ease((t - 0.4) / 0.5), va="top", linespacing=1.4)
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_empresa(e, t):
    f = fig(W, H); top(f, e); a = ease(t / 0.35)
    # día y momento del reporte
    caja(f, 0.08, 0.745, 0.84, 0.065, e.get("color_dia", "blue"), 0.22 * a)
    T(f, XR - 0.02, 0.777, e["dia"], FG, 40, "bold", va="center", alpha=a)
    T(f, XR, 0.715, e["hora"], MUTED, 30, alpha=a, va="top")
    b = ease((t - 0.12) / 0.4)
    T(f, XR, 0.58, e["nombre"], FG, 84 if len(e["nombre"]) < 14 else 66, "bold", alpha=b)
    L(f, XR, 0.535, e["ticker"], BLUE, 42, alpha=b)
    if e.get("sector"): T(f, 0.12, 0.54, e["sector"], GOLD, 32, "bold", ha="left", alpha=b)
    for i, (lab, big, sub) in enumerate(e["kpis"]):
        c = ease((t - 0.25 - i * 0.15) / 0.4); y = 0.43 - i * 0.115
        caja(f, 0.08, y - 0.045, 0.84, 0.1, DIM, 0.55 * c)
        T(f, XR - 0.02, y + 0.022, lab, MUTED, 30, alpha=c, va="center")
        L(f, 0.12, y, big, TEAL if i == 0 else GOLD, 64, ha="left", va="center", alpha=c)
        if sub: T(f, XR - 0.02, y - 0.02, sub, FG, 24, alpha=c, va="center")
    if e.get("nota"): T(f, XR, 0.235, e["nota"], MUTED, 26, alpha=ease((t - 0.45) / 0.4), va="top", linespacing=1.35)
    return with_logo(to_arr(f), LG, x=90, y=150)


def s_fin(e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.74, e["titular"], GOLD, 48, "bold", alpha=a, va="top", linespacing=1.1)
    T(f, XR, 0.59, "◀ " + e["cta"], FG, 42, "bold", alpha=ease((t - 0.15) / 0.5))
    L(f, XR, 0.545, "youtube.com/@AIStocksUAE", BLUE, 40, alpha=ease((t - 0.15) / 0.5))
    if e.get("nabd"):
        b = ease((t - 0.3) / 0.5)
        caja(f, 0.08, 0.385, 0.84, 0.115, DIM, 0.55 * b)
        T(f, XR - 0.02, 0.468, e["nabd"], FG, 34, "bold", alpha=b, va="center")
        L(f, XR - 0.02, 0.418, "youtube.com/@NabdWallStreet", GOLD, 36, alpha=b, va="center")
    T(f, XR, 0.355, S["fuente"] + "\n" + AVISO + "\nلا نملك مراكز في الأسهم المذكورة.", MUTED, 24, linespacing=1.5, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=(W - 240) // 2, y=150)


RX = {"gancho": s_gancho, "local": s_local, "empresa": s_empresa, "fin": s_fin}
def frame(e, t): return RX[e["tipo"]](e, t)


def voz(texto, wav):
    """Azure (wav de voz-eau.yml en VOZ_DIR) si está; si no, Piper del canal remuestreado a 24 kHz cuando hay VOZ_DIR."""
    vd = os.environ.get("VOZ_DIR"); az = os.path.join(vd, clave(texto) + ".wav") if vd else None
    if az and os.path.exists(az):
        w = wave.open(az); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
        nz = np.where(np.abs(a) > 300)[0]; a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)]
        fo = int(0.04 * sr); a[-fo:] *= np.linspace(1, 0, fo); VOCES.append("azure"); return a, sr
    a, sr = comun.voz(texto, wav); VOCES.append("piper")
    if vd:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe(); o = wav + ".24k.wav"
        subprocess.run([ff, "-y", "-i", wav, "-ar", "24000", o], check=True, capture_output=True)
        # el wav de Piper sin recortar, ya a 24 kHz: recorte y fundido como en comun.voz()
        w = wave.open(o); b = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32); s2 = w.getframerate()
        nz = np.where(np.abs(b) > 300)[0]; b = b[max(nz[0] - int(0.03 * s2), 0):nz[-1] + int(0.08 * s2)]
        fo = int(0.06 * s2); b[-fo:] *= np.linspace(1, 0, fo); return b, s2
    return a, sr


VOCES = []
if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); E = S["escenas"]
    S["out"] = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), S["out"]); os.makedirs(AUD, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"cal_prev_{i}.png"))
        sys.exit()
    clips = [voz(e["voz"], os.path.join(AUD, f"cal_{i}.wav")) for i, e in enumerate(E)]; sr = clips[0][1]
    assert all(s == sr for _, s in clips), "frecuencias distintas: no mezclar Azure y Piper sin VOZ_DIR"
    LEAD, TAIL = 0.08, 0.22
    durs = [LEAD + len(a) / sr + TAIL for a, _ in clips]; durs[-1] += 0.7
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs], "voz:", ",".join(sorted(set(VOCES))))
    if sum(durs) > MAXDUR: sys.exit(f"Short demasiado largo: {sum(durs):.1f} s (máx {MAXDUR}). Acorta la voz.")
    if sum(durs) < MINDUR: print(f"aviso: Short corto ({sum(durs):.1f} s; el formato pide 45-60 s)")
    times, t0 = render([lambda t, e=e: frame(e, t) for e in E], durs, ([a for a, _ in clips], [LEAD] * len(E)), sr, W, H, FPS, S["out"],
                       os.path.join(AUD, "cal-silent.mp4"), os.path.join(AUD, "cal-full.wav"), loud=-14, ANIM=20, XF=6)
    print("listo", S["out"], round(t0, 1), "s | voz:", ",".join(sorted(set(VOCES))))
