"""Piezas comunes de la serie educativa «Análisis técnico, explicado fácil» de AIAcciones España (espana/educativo/):
marca del canal (los mismos colores y logo que el vídeo diario), indicadores calculados de las velas, voz frase a frase
(mp3 de es-ES-AlvaroNeural en VOZ_DIR; Piper de respaldo), subtítulos (tira_texto, pegar, partir) y render() con overlay."""
import os, sys, subprocess, wave, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams["text.parse_math"] = False
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from voz_leccion import frases, clave

MARCA = "AIAcciones España"
SERIE = "Análisis técnico, explicado fácil"
CANAL = "https://www.youtube.com/@AIAccionesEspa%C3%B1a"
CANAL_TXT = "https://www.youtube.com/@AIAccionesEspaña"
LOGO = os.environ.get("LOGO", "/mnt/project-files/espana/marca/logo-aiacciones-espana.png")
VOICE = os.environ.get("VOICE", "/mnt/project-files/espana/voz/vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
TTS = ["--length-scale", "0.97", "--noise-scale", "0.55", "--noise-w-scale", "0.6", "--sentence-silence", "0.1"]
# colores del vídeo diario (espana/diario/make_video.py)
BG = "#0B1E3A"; FG = "#FFFFFF"; MUTED = "#9FB3CC"; ACC = "#2FB7A3"; ACC2 = "#4C8DF0"; NEG = "#F2A541"; DIM = "#3A5378"; PUR = "#C38BF2"
PANEL = "#12294B"; BANDA = (0x08, 0x16, 0x2C)
COLS = {"acc": ACC, "acc2": ACC2, "neg": NEG, "fg": FG, "muted": MUTED, "pur": PUR, "dim": DIM,
        "teal": ACC, "blue": ACC2, "orange": NEG, "gold": NEG}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_L = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
col = lambda c: COLS.get(c, c)
num = lambda v, d=2: f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
fecha_txt = lambda d: f"{d.day} de {MESES_L[d.month - 1]} de {d.year}"


def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3


def fig(W, H):
    f = plt.figure(figsize=(W / 100, H / 100), dpi=100); f.patch.set_facecolor(BG); return f


def to_arr(f):
    f.canvas.draw(); a = np.asarray(f.canvas.buffer_rgba())[:, :, :3].copy(); plt.close(f); return a


def load_logo(w):
    im = Image.open(LOGO).convert("RGBA"); h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0; return a[:, :, :3] * 255.0, a[:, :, 3:4]


def with_logo(arr, lg, x, y):
    rgb, al = lg; h, w = al.shape[:2]
    reg = arr[y:y + h, x:x + w].astype(np.float32); arr[y:y + h, x:x + w] = (reg * (1 - al) + rgb * al).astype(np.uint8); return arr


def clean(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=15, length=0)


# ---------- indicadores (calculados sobre toda la serie y luego recortados al rango de cada gráfico) ----------
def sma(a, n):
    a = np.asarray(a, float); return np.array([a[i - n + 1:i + 1].mean() if i >= n - 1 else np.nan for i in range(len(a))])


def ema(a, n):
    a = np.asarray(a, float); k = 2 / (n + 1); out = np.empty(len(a)); out[0] = a[0]
    for i in range(1, len(a)): out[i] = a[i] * k + out[i - 1] * (1 - k)
    return out


def rsi(c, n=14):
    c = np.asarray(c, float); d = np.diff(c); g = np.where(d > 0, d, 0); l = np.where(d < 0, -d, 0); out = [np.nan] * (n + 1)
    ag, al = g[:n].mean(), l[:n].mean()
    for i in range(n, len(d)):
        ag = (ag * (n - 1) + g[i]) / n; al = (al * (n - 1) + l[i]) / n; out.append(100 - 100 / (1 + ag / al) if al else 100.0)
    return np.array(out[:len(c)])


def indicadores(V):
    """Series calculadas de las velas: smaN/emaN (cualquier N), rsi, macd/senal/hist (12,26,9), boll_m/boll_s/boll_i (20,2),
    stoch_k/stoch_d (14,3,3), vol, vol_m20."""
    c = np.array([v["c"] for v in V], float); h = np.array([v["h"] for v in V], float); l = np.array([v["l"] for v in V], float)
    vol = np.array([v["v"] or 0 for v in V], float)

    class S(dict):
        def __missing__(self, k):
            if k.startswith("sma"): self[k] = sma(c, int(k[3:]))
            elif k.startswith("ema"): self[k] = ema(c, int(k[3:]))
            else: raise KeyError(k)
            return self[k]
    I = S(c=c, vol=vol, vol_m20=sma(vol, 20), rsi=rsi(c))
    I["macd"] = ema(c, 12) - ema(c, 26); I["senal"] = ema(I["macd"], 9); I["hist"] = I["macd"] - I["senal"]
    m = sma(c, 20); s = np.array([c[i - 19:i + 1].std() if i >= 19 else np.nan for i in range(len(c))])
    I["boll_m"], I["boll_s"], I["boll_i"] = m, m + 2 * s, m - 2 * s
    fk = np.array([np.nan] * 13 + [(c[i] - l[i - 13:i + 1].min()) / max(h[i - 13:i + 1].max() - l[i - 13:i + 1].min(), 1e-9) * 100 for i in range(13, len(c))])
    I["stoch_k"] = sma(fk, 3); I["stoch_d"] = sma(I["stoch_k"], 3)
    return I


# ---------- voz ----------
def voz_frases(texto, wav_dir, gap=0.28):
    """Locución frase a frase, para los subtítulos. Si VOZ_DIR tiene el mp3 neuronal de cada frase (educativo-espana.yml), usa esos;
    si falta alguno, toda la locución de la escena sale con Piper (no se mezclan voces). Devuelve (muestras, sr, [(inicio, fin, frase)], motor)."""
    import imageio_ffmpeg
    F = frases(texto); vd = os.environ.get("VOZ_DIR")
    mp3 = [os.path.join(vd, clave(x) + ".mp3") for x in F] if vd else []
    motor = "neuronal" if mp3 and all(os.path.exists(p) and os.path.getsize(p) > 0 for p in mp3) else "piper"
    paths = []
    if motor == "neuronal":
        for x, m in zip(F, mp3):
            p = os.path.join(wav_dir, f"n_{clave(x)}.wav")
            if not os.path.exists(p):
                subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", m, "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", p], check=True)
            paths.append(p)
    else:
        if vd: print("aviso: faltan mp3 de la voz neuronal para", texto[:50], "-> Piper")
        for x in F:
            p = os.path.join(wav_dir, f"piper_{clave(x)}.wav")
            if not os.path.exists(p):
                subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-f", p] + TTS, input=(x + "\n").encode(), check=True, capture_output=True)
            paths.append(p)
    trozos, sr = [], None
    for p in paths:
        w = wave.open(p); sr = w.getframerate(); trozos.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32))
    out, marcas, t = [], [], 0.0
    for x, a in zip(F, trozos):
        nz = np.where(np.abs(a) > 300)[0]
        if len(nz): a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)].copy()
        fi, fo = min(int(0.015 * sr), len(a)), min(int(0.06 * sr), len(a))
        a[:fi] *= np.linspace(0, 1, fi); a[len(a) - fo:] *= np.linspace(1, 0, fo)
        marcas.append((round(t, 3), round(t + len(a) / sr, 3), x)); out += [a, np.zeros(int(gap * sr), np.float32)]; t += len(a) / sr + gap
    return np.concatenate(out[:-1]), sr, marcas, motor


# ---------- subtítulos ----------
def tira_texto(s, color, fs, H, w="bold"):
    """Imagen RGBA de una línea de texto recortada a su ancho, para los subtítulos."""
    W_ = max(400, int(len(str(s)) * fs * 0.75) + 160)
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


def partir(s, n):
    """Parte un subtítulo en líneas de como mucho n caracteres, por palabras."""
    L, cur = [], ""
    for wd in s.split():
        if cur and len(cur) + 1 + len(wd) > n: L.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    return L + ([cur] if cur else [])


def render(frames, durs, clips, sr, W, H, FPS, out, silent, wav, loud=-16, ANIM=30, XF=8, overlay=None):
    """Vídeo fotograma a fotograma (animación los primeros ANIM, fundido de XF al siguiente), overlay(fotograma, escena, s_escena, s_total)
    para los subtítulos, y el audio con el mismo filtro que el vídeo diario."""
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
            if overlay: fr = overlay(fr, j, k / FPS, t0 + k / FPS)
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
