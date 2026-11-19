"""Piezas comunes de la serie semanal de análisis fundamental en árabe de @QatarAIStocks (qatar/fundamental/).
Reutiliza la marca, la fuente y el texto RTL de qatar/diario/comun.py y añade: locución frase a frase (para subtítulos), tiras de texto
y render con capa de subtítulos. Voz: la del canal (Piper ar_JO-kareem-medium). Si algún día el canal pasa a Azure, basta con dejar
en VOZ_DIR un wav por frase con el nombre clave_frase(frase).wav (como hace ge/diario/voz_azure.py): se usa ese en vez de Piper."""
import os, re, sys, wave, hashlib, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *  # noqa: F401,F403  (BG, FG, GOLD, TEAL, NEG, MUTED, DIM, BLUE, ar, fig, to_arr, load_logo, with_logo, clean, ease, LOGO, VOICE, CANAL, CTA_*, cta_activa)
from comun import plt, Image, cta_activa as _cta_hoy
import datetime as _dt


def cta_activa(fecha=None):
    """Campaña de comentarios y suscripción de comun.py (8-22 nov 2026), según la fecha de PUBLICACIÓN del capítulo (no la de hoy)."""
    if os.environ.get("CTA") in ("0", "1") or not fecha: return _cta_hoy()
    return CTA_DESDE <= fecha <= CTA_HASTA


CTA_TXT = CTA_PANTALLA[0] + " · " + CTA_PANTALLA[1]

SERIE = "التحليل الأساسي ببساطة"          # nombre de la serie en pantalla
SERIE_ES = "Análisis fundamental, fácil"
MARCA = "Qatar AI Stocks"
NAVY = "#3A0F20"   # granate oscuro de la marca Qatar (paneles)
MAX_PALABRAS = 13
VOZ_ID = os.environ.get("VOZ_ID", "piper-ar_JO-kareem-medium")
_PIPER = None


def frases(texto):
    """Parte la locución en frases cortas (subtítulos de 1-2 líneas). Corta en . ! ? ؟ y, si hace falta, en la coma (، ,) más centrada."""
    out = []
    for f in re.split(r"(?<=[.!?؟])\s+", " ".join(str(texto).split())):
        pend = [f.strip()] if f.strip() else []
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith(("،", ",", "؛", ":"))]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def clave_frase(frase, voz=VOZ_ID):
    return hashlib.sha1((voz + "|" + frase).encode()).hexdigest()[:16]


def voz_frases(texto, gap=0.30):
    """Locución frase a frase. Devuelve (muestras, sr, [(inicio, fin, frase)], motor)."""
    global _PIPER
    F = frases(texto); vd = os.environ.get("VOZ_DIR")
    paths = [os.path.join(vd, clave_frase(x) + ".wav") for x in F] if vd else []
    trozos, sr, motor = [], None, "piper"
    if paths and all(os.path.exists(p) for p in paths):
        motor = "azure"
        for p in paths:
            w = wave.open(p); sr = w.getframerate(); trozos.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32))
    else:
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
        g = gap * (1.6 if x.endswith((".", "؟", "!", "?")) else 1.0)
        marcas.append((round(t, 3), round(t + len(a) / sr, 3), x)); out += [a, np.zeros(int(g * sr), np.float32)]; t += len(a) / sr + g
    return np.concatenate(out[:-1]), sr, marcas, motor


def tira_texto(s, color, fs, H, w="bold"):
    """Imagen RGBA de una línea de texto (árabe bien unido y RTL) recortada a su ancho."""
    W_ = max(400, int(len(str(s)) * fs * 1.2) + 160)
    f = plt.figure(figsize=(W_ / 100, H / 100), dpi=100); f.patch.set_alpha(0)
    f.text(0.5, 0.5, ar(s), color=color, fontsize=fs, weight=w, ha="center", va="center")
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
    """Como comun.render del diario, con overlay(fotograma, escena, segundo_en_escena) para los subtítulos."""
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
    """Subtítulos también como archivo .srt (por si se quieren subir a YouTube como pista aparte)."""
    ts = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    n, L = 0, []
    for M, t0, ld in zip(marcas_por_escena, inicios, leads):
        for a, b, s in M:
            n += 1; L.append(f"{n}\n{ts(t0 + ld + a)} --> {ts(t0 + ld + b + 0.2)}\n{s}\n")
    open(path, "w").write("\n".join(L))
