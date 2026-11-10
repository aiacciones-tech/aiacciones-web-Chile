"""Piezas comunes del video diario en árabe de Nabd Wall Street (نبض وول ستريت): fuente Tajawal (la de la marca), texto RTL con letras unidas
(arabic-reshaper + python-bidi, porque matplotlib no une ni reordena el árabe), colores de la marca, logo y locución Piper."""
import os, re, subprocess, wave, textwrap, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import arabic_reshaper, logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # Tajawal no tiene peso 400: usa el 500 (Medium)
from bidi.algorithm import get_display
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
for w in ("Medium", "Bold"):
    font_manager.fontManager.addfont(os.path.join(HERE, "fonts", f"Tajawal-{w}.ttf"))
plt.rcParams.update({"font.family": ["Tajawal", "DejaVu Sans"], "text.parse_math": False, "axes.unicode_minus": False})
LOGO = os.environ.get("LOGO", "/mnt/project-files/nabd-brand-kit/png/profile-800-Nabd.png")
VOICE = os.environ.get("VOICE", "/mnt/project-files/nabd-pipeline/voice/ar_JO-kareem-medium.onnx")
CANAL = "https://www.youtube.com/channel/UCRU3n034y5dJBEGnhAKjhfQ"  # cambiar por el @handle cuando esté confirmado
CANAL_ID = "UCRU3n034y5dJBEGnhAKjhfQ"
TELEGRAM = "https://t.me/NabdWallStreet"   # canal de Telegram (@NabdWallStreet); el vídeo largo invita a unirse
PROGRAMA = "التقرير اليومي"   # nombre del programa dentro de la marca (manual de producción de Daniel, 10-nov-2026)
MARCA = "نبض وول ستريت"; MARCA_EN = "Nabd Wall Street"
# Marca Nabd Wall Street: noche #0B1A2E, azul marino #13294B, dorado #D4AF37 (claro #F1D78A), marfil #F5EBDD, sube #22C55E, baja #E5484D
BG = "#0B1A2E"; FG = "#F5EBDD"; MUTED = "#A9B4C8"; GOLD = "#D4AF37"; TEAL = "#22C55E"; NEG = "#E5484D"; DIM = "#2A4468"; BLUE = "#7DB7F0"
COLS = {"gold": GOLD, "teal": TEAL, "neg": NEG, "fg": FG, "muted": MUTED, "blue": BLUE, "acc": TEAL, "acc2": BLUE}
col = lambda c: COLS.get(c, c)


# matplotlib 3.11+ ya ordena el texto de derecha a izquierda (libraqm); en versiones anteriores lo hace python-bidi.
# arabic-reshaper une las letras siempre (formas de presentación), lo que funciona en las dos.
BIDI_NATIVO = tuple(int(x) for x in matplotlib.__version__.split(".")[:2]) >= (3, 11)


NUM_ISO = re.compile(r"([+\-−×]?\d(?:[\d,.:/]|-(?=\d))*%?)")


def ar(s, ancho=None):
    """Texto árabe listo para matplotlib: letras unidas (reshaper) y orden visual de derecha a izquierda (bidi), línea a línea.
    Las cifras van aisladas (LRI ... PDI) para que «+13.26%» no salga como «%13.26+» dentro de una frase árabe."""
    out = []
    for l in str(s).split("\n"):
        if BIDI_NATIVO and re.search("[\u0600-\u06FF]", l): l = NUM_ISO.sub("\u2066\\1\u2069", l)
        partes = textwrap.wrap(l, ancho) if ancho and len(l) > ancho else [l]
        out += [p if BIDI_NATIVO else get_display(p) for p in (arabic_reshaper.reshape(x) for x in partes)]
    return "\n".join(out)


num = lambda v, d=2: f"{v:,.{d}f}"
pct = lambda v, d=2: f"{v:+.{d}f}%"
ease = lambda t: 1 - (1 - min(max(t, 0), 1)) ** 3


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
    ax.tick_params(colors=MUTED, labelsize=16, length=0)


TTS = ["--length-scale", os.environ.get("LENGTH_SCALE", "0.8"), "--noise-scale", "0.6", "--noise-w-scale", "0.7", "--sentence-silence", "0.12"]


def voz(texto, wav):
    """Locución Piper ar_JO-kareem (piper-tts 1.8+ pone la vocalización/tashkeel). Devuelve (muestras recortadas, sr)."""
    subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-f", wav] + TTS, input=(texto + "\n").encode(), check=True, capture_output=True)
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    nz = np.where(np.abs(a) > 300)[0]; a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)]
    fi, fo = int(0.015 * sr), int(0.06 * sr); a[:fi] *= np.linspace(0, 1, fi); a[-fo:] *= np.linspace(1, 0, fo)
    return a, sr


from voz_frases import frases, clave as clave_frase  # noqa: E402  (sin dependencias pesadas: lo usa también voz-Nabd.yml)
_PIPER = None


def voz_frases(texto, wav_dir, gap=0.28):
    """Locución frase a frase, para los subtítulos. Si VOZ_DIR tiene el wav de cada frase (Azure, hecho por voz-Nabd.yml), usa esos;
    si falta alguno, toda la locución sale con Piper (no se mezclan voces). Devuelve (muestras, sr, [(inicio, fin, frase)], motor)."""
    F = frases(texto); vd = os.environ.get("VOZ_DIR")
    paths = [os.path.join(vd, clave_frase(x) + ".wav") for x in F] if vd else []
    trozos, sr, motor = [], None, "piper"
    if paths and all(os.path.exists(p) for p in paths):
        motor = "azure"
        for p in paths:
            w = wave.open(p); sr = w.getframerate(); trozos.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32))
    else:
        global _PIPER
        from piper import PiperVoice, SynthesisConfig
        _PIPER = _PIPER or PiperVoice.load(VOICE)
        cfg = SynthesisConfig(length_scale=float(os.environ.get("LENGTH_SCALE", "0.8")), noise_scale=0.6, noise_w_scale=0.7)
        for x in F:
            ch = list(_PIPER.synthesize(x, cfg)); sr = ch[0].sample_rate
            trozos.append(np.concatenate([c.audio_int16_array for c in ch]).astype(np.float32))
    out, marcas, t = [], [], 0.0
    for x, a in zip(F, trozos):
        nz = np.where(np.abs(a) > 300)[0]
        if len(nz): a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)].copy()
        fi, fo = min(int(0.015 * sr), len(a)), min(int(0.06 * sr), len(a))
        a[:fi] *= np.linspace(0, 1, fi); a[len(a) - fo:] *= np.linspace(1, 0, fo)
        marcas.append((round(t, 3), round(t + len(a) / sr, 3), x)); out += [a, np.zeros(int(gap * sr), np.float32)]; t += len(a) / sr + gap
    return np.concatenate(out[:-1]), sr, marcas, motor


def tira_texto(s, color, fs, H, w="bold", fondo=None):
    """Imagen RGBA de una línea de texto (árabe o latino) recortada a su ancho, para el ticker y los subtítulos."""
    W_ = max(400, int(len(str(s)) * fs * 1.5) + 120)
    f = plt.figure(figsize=(W_ / 100, H / 100), dpi=100); f.patch.set_alpha(0)
    f.text(0.5, 0.5, ar(s), color=color, fontsize=fs, weight=w, ha="center", va="center")
    f.canvas.draw(); a = np.asarray(f.canvas.buffer_rgba()).copy(); plt.close(f)
    cols = np.where(a[:, :, 3].max(axis=0) > 0)[0]
    return a[:, max(cols[0] - 4, 0):cols[-1] + 5] if len(cols) else a[:, :10]


def pegar(arr, rgba, x, y):
    """Compone una imagen RGBA sobre el fotograma (recorta lo que se sale)."""
    h, w = rgba.shape[:2]; H_, W_ = arr.shape[:2]
    x0, x1 = max(x, 0), min(x + w, W_)
    if x1 <= x0: return arr
    src = rgba[:, x0 - x:x1 - x].astype(np.float32); al = src[:, :, 3:4] / 255.0
    reg = arr[y:y + h, x0:x1].astype(np.float32); arr[y:y + h, x0:x1] = (reg * (1 - al) + src[:, :, :3] * al).astype(np.uint8)
    return arr


def render(frames, durs, clips, sr, W, H, FPS, out, silent, wav, loud=-16, ANIM=30, XF=8, overlay=None):
    """frames: lista de funciones t->array; durs en segundos; clips de audio. Escribe el mp4 con voz y devuelve los tiempos de inicio.
    overlay(fotograma, escena, segundo_en_escena, segundo_total) dibuja encima lo que cambia en cada fotograma (ticker, subtítulos)."""
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
