"""Piezas comunes de la serie semanal «Análisis fundamental en simple» de AIAcciones Chile (fundamental-cl/).
Marca del canal (colores del diario IPSA, logo AIAcciones Chile), locución frase a frase (para los subtítulos), tiras de texto
y render con capa de subtítulos. Port en español (izquierda a derecha) de qatar/fundamental/comun_fund.py.

Voz: la del canal, Azure es-CL-LorenzoNeural (voz-cl/). Cada frase es una locución: `python3 comun_fund.py frases <video.json>`
escribe una por línea para `bash voz-cl/pedir.sh`; con VOZ_DIR, voz_frases() toma el wav de cada frase (voz_cl.clave). Si falta alguna,
para (no se mezclan voces): se repite el pedido o se renderiza todo con Piper es_MX-claude-high (sin VOZ_DIR, con VOICE=<onnx>)."""
import os, re, sys, wave, subprocess, textwrap, datetime as dt, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams["text.parse_math"] = False
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "voz-cl")); sys.path.insert(0, os.path.join(REPO, "diario"))
from voz_cl import clave, norm  # noqa: E402
import campana  # noqa: E402  (campaña de comentarios y suscripción del canal, hasta el 22-nov-2026)

# Marca (la del diario IPSA, diario/make_video.py)
BG = "#0B1E3A"; FG = "#FFFFFF"; MUTED = "#9FB3CC"; ACC = "#2FB7A3"; ACC2 = "#4C8DF0"; NEG = "#F2A541"; DIM = "#3A5378"; PUR = "#C38BF2"
NAVY = "#12294D"   # paneles
COLS = {"acc": ACC, "acc2": ACC2, "neg": NEG, "fg": FG, "muted": MUTED, "pur": PUR, "dim": DIM}
col = lambda c: COLS.get(c, c)
LOGO = os.environ.get("LOGO", "/mnt/project-files/marca/logo-aiacciones-chile.png")
VOICE = os.environ.get("VOICE", "vits-piper-es_MX-claude-high/es_MX-claude-high.onnx")
SERIE = "Análisis fundamental en simple"
MARCA = "AIAcciones Chile"
CANAL = "https://www.youtube.com/@aiaccioneschile"
WEB = "https://aiacciones.cl/"
MAX_PALABRAS = 16


def cta_activa(fecha):
    """Campaña de comentarios del canal, según la fecha de PUBLICACIÓN del capítulo (no la de hoy)."""
    return bool(fecha) and fecha <= campana.HASTA


def es(v, d=1):
    """Cifra en formato chileno: 1.234,5"""
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(v, (int, float)) else str(v)


def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3


def fig(W=1920, H=1080):
    f = plt.figure(figsize=(W / 100, H / 100), dpi=100); f.patch.set_facecolor(BG); return f


def to_arr(f):
    f.canvas.draw(); a = np.asarray(f.canvas.buffer_rgba())[:, :, :3].copy(); plt.close(f); return a


def load_logo(w):
    im = Image.open(LOGO).convert("RGBA"); h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0; return a[:, :, :3] * 255.0, a[:, :, 3:4]


def with_logo(arr, lg, x=None, y=None):
    rgb, al = lg; h, w = al.shape[:2]; H_, W_ = arr.shape[:2]
    x = W_ - w - 40 if x is None else x; y = H_ - h - 30 if y is None else y
    reg = arr[y:y + h, x:x + w].astype(np.float32); arr[y:y + h, x:x + w] = (reg * (1 - al) + rgb * al).astype(np.uint8); return arr


def clean(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=18, length=0)


def frases(texto):
    """Parte la locución en frases cortas (subtítulos de 1-2 líneas). Corta en . ! ? y, si hace falta, en la coma o el punto y coma más centrado."""
    out = []
    for f in re.split(r"(?<=[.!?])\s+", " ".join(str(texto).split())):
        pend = [f.strip()] if f.strip() else []
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith((",", ";", ":"))]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def voz_frases(texto, gap=0.22):
    """Locución frase a frase. Devuelve (muestras, sr, [(inicio, fin, frase)], motor)."""
    F = frases(texto); vd = os.environ.get("VOZ_DIR"); trozos, sr = [], None
    if vd:
        falta = [x for x in F if not os.path.exists(os.path.join(vd, clave(x) + ".wav"))]
        if falta: sys.exit(f"Faltan {len(falta)} frases con voz Azure (p. ej. «{falta[0][:60]}»): repite voz-cl/pedir.sh o renderiza todo con Piper (sin VOZ_DIR).")
        motor = "azure"
        for x in F:
            w = wave.open(os.path.join(vd, clave(x) + ".wav")); sr = w.getframerate()
            trozos.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32))
    else:
        motor = "piper"; tmp = os.path.join(os.environ.get("AUD", "aud"), "_frase.wav")
        env = dict(os.environ); env["PYTHONPATH"] = ""   # Piper real, nunca el falso de voz-cl/shim
        for x in F:
            subprocess.run([sys.executable, "-m", "piper", "-m", VOICE, "-f", tmp, "--length-scale", "0.97", "--noise-scale", "0.55", "--noise-w-scale", "0.6"],
                           input=(x + "\n").encode(), check=True, capture_output=True, env=env)
            w = wave.open(tmp); sr = w.getframerate(); trozos.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32))
    out, marcas, t = [], [], 0.0
    for x, a in zip(F, trozos):
        nz = np.where(np.abs(a) > 300)[0]
        if len(nz): a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)].copy()
        fi, fo = min(int(0.015 * sr), len(a)), min(int(0.06 * sr), len(a))
        a[:fi] *= np.linspace(0, 1, fi); a[len(a) - fo:] *= np.linspace(1, 0, fo)
        g = gap * (1.7 if x.endswith((".", "?", "!")) else 1.0)
        marcas.append((round(t, 3), round(t + len(a) / sr, 3), x)); out += [a, np.zeros(int(g * sr), np.float32)]; t += len(a) / sr + g
    return np.concatenate(out[:-1]), sr, marcas, motor


def tira_texto(s, color, fs, H, w="bold"):
    """Imagen RGBA de una línea de texto recortada a su ancho."""
    W_ = max(400, int(len(str(s)) * fs * 1.0) + 160)
    f = plt.figure(figsize=(W_ / 100, H / 100), dpi=100); f.patch.set_alpha(0)
    f.text(0.5, 0.5, s, color=color, fontsize=fs, weight=w, ha="center", va="center")
    f.canvas.draw(); a = np.asarray(f.canvas.buffer_rgba()).copy(); plt.close(f)
    cols = np.where(a[:, :, 3].max(axis=0) > 0)[0]
    return a[:, max(cols[0] - 4, 0):cols[-1] + 5] if len(cols) else a[:, :10]


def pegar(arr, rgba, x, y):
    h, w = rgba.shape[:2]; H_, W_ = arr.shape[:2]
    x0, x1 = max(x, 0), min(x + w, W_)
    if x1 <= x0: return arr
    src = rgba[:, x0 - x:x1 - x].astype(np.float32); al = src[:, :, 3:4] / 255.0
    reg = arr[y:y + h, x0:x1].astype(np.float32); arr[y:y + h, x0:x1] = (reg * (1 - al) + src[:, :, :3] * al).astype(np.uint8)
    return arr


def render(frames, durs, clips, sr, W, H, FPS, out, silent, wav, loud=-16, ANIM=30, XF=8, overlay=None):
    """Fotogramas animados (ANIM primeros), fundido entre escenas, overlay(fotograma, escena, segundo) para los subtítulos, y audio."""
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                             "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", silent], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    bgc = np.array([int(BG[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    t0, times, audio = 0, [], []
    for j, (fn, dur, a, lead) in enumerate(zip(frames, durs, clips[0], clips[1])):
        total = int(round(dur * FPS)); last = None
        nxt = frames[j + 1](0).astype(np.float32) if j + 1 < len(frames) else np.zeros((H, W, 3), np.float32) + bgc
        for k in range(total):
            if k < ANIM: last = fn(k / (ANIM - 1))
            fr = last.astype(np.float32)
            if k >= total - XF: al = (total - k) / (XF + 1); fr = fr * al + nxt * (1 - al)
            fr = fr.astype(np.uint8)
            if overlay: fr = overlay(fr, j, k / FPS)
            proc.stdin.write(fr.tobytes())
        n = int(round(total / FPS * sr)); seg = np.zeros(n, np.float32); st = int(lead * sr); seg[st:st + len(a)] = a[:n - st]
        audio.append(seg); times.append(round(t0, 2)); t0 += total / FPS
    proc.stdin.close(); proc.wait()
    full = np.clip(np.concatenate(audio), -32768, 32767).astype(np.int16)
    w = wave.open(wav, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(full.tobytes()); w.close()
    AF = f"highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250,loudnorm=I={loud}:TP=-1.5:LRA=9"
    subprocess.run([ff, "-y", "-i", silent, "-i", wav, "-af", AF, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out],
                   check=True, stderr=subprocess.DEVNULL)
    return times, t0


def srt(marcas_por_escena, inicios, leads, path):
    """Subtítulos también como archivo .srt (pista aparte en YouTube; el video ya los lleva quemados)."""
    ts = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    n, L = 0, []
    for M, t0, ld in zip(marcas_por_escena, inicios, leads):
        for a, b, s in M:
            n += 1; L.append(f"{n}\n{ts(t0 + ld + a)} --> {ts(t0 + ld + b + 0.2)}\n{s}\n")
    open(path, "w").write("\n".join(L))


def locuciones(vj):
    """Todas las locuciones del capítulo tal como se dirán (con el cierre de campaña si toca por la fecha de publicación)."""
    E = vj.get("escenas", []); out = []
    for e in E:
        v = e.get("voz", "")
        if e.get("tipo") == "fin" and cta_activa(vj.get("publicar")): v = v.rstrip() + " " + campana.VOZ_VIDEO
        out.append(v)
    return out


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[1] == "frases":
    # python3 comun_fund.py frases <video.json>  → una frase por línea (fuente .txt para voz-cl/pedir.sh)
    import json
    VJ = json.load(open(sys.argv[2]))
    for v in locuciones(VJ):
        for x in frases(v): print(norm(x))
