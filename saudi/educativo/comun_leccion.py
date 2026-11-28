"""Piezas de la serie educativa «التحليل الفني ببساطة» que no están en saudi/diario/comun.py: voz frase a frase (Azure con VOZ_DIR,
Piper de respaldo), subtítulos (tira_texto, pegar) y render() con overlay. El resto (marca, colores, ar(), logo) viene de saudi/diario/comun.py."""
import os, sys, subprocess, wave, tempfile, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *
from voz_leccion import frases, clave

MARCA = "Saudi Arabia AI Stocks"
SERIE = "التحليل الفني ببساطة"
# En la locución, los nombres latinos van escritos en árabe para que la voz los lea bien; en pantalla (subtítulos) vuelven a su forma original.
LATINO = {"ساودي أرابيا إيه آي ستوكس": "Saudi Arabia AI Stocks", "تريدينغ فيو": "TradingView"}
sub_pantalla = lambda s: [s := s.replace(a, b) for a, b in LATINO.items()][-1]
PANEL = "#0E3128"; BANDA = (0x0B, 0x3B, 0x2E)


def voz_frases(texto, wav_dir, gap=0.28):
    """Locución frase a frase, para los subtítulos. Si VOZ_DIR tiene el wav de Azure de cada frase (educativo-saudi.yml), usa esos;
    si falta alguno, toda la locución de la escena sale con Piper (no se mezclan voces). Devuelve (muestras, sr, [(inicio, fin, frase)], motor)."""
    F = frases(texto); vd = os.environ.get("VOZ_DIR")
    paths = [os.path.join(vd, clave(x) + ".wav") for x in F] if vd else []
    motor = "azure" if paths and all(os.path.exists(p) for p in paths) else "piper"
    if motor == "piper":
        if vd: print("aviso: faltan wav de Azure para", texto[:50], "-> Piper")
        paths = []
        for k, x in enumerate(F):
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


def sma(cierres, n):
    """Media móvil simple de n sesiones sobre los cierres (NaN mientras no hay n cierres). Cálculo propio, «محسوب»."""
    c = np.asarray(cierres, dtype=float); o = np.full(len(c), np.nan)
    if len(c) >= n: o[n - 1:] = np.convolve(c, np.ones(n) / n, "valid")
    return o


COL_MEDIAS = {20: "#C792EA", 50: "#6FB6F5", 100: "#F2A65A", 200: "#E3C45E"}


def medias_rango(velas, V, medias):
    """Para cada media de la escena ({n, texto?, color?}), sus valores en las velas V (subconjunto contiguo de velas)."""
    i0 = next(k for k, v in enumerate(velas) if v["t"] == V[0]["t"]); c = [v["c"] for v in velas]
    out = []
    for m in medias:
        n = m["n"] if isinstance(m, dict) else int(m); m = m if isinstance(m, dict) else {}
        out.append({"n": n, "texto": m.get("texto", f"متوسط {n} جلسة"), "color": col(m.get("color", COL_MEDIAS.get(n, "#9DB5AA"))),
                    "y": sma(c, n)[i0:i0 + len(V)]})
    return out


def tira_texto(s, color, fs, H, w="bold"):
    """Imagen RGBA de una línea de texto (árabe con letras unidas y RTL) recortada a su ancho, para los subtítulos."""
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


def partir(s, n):
    """Parte un subtítulo en líneas de como mucho n caracteres, por palabras."""
    L, cur = [], ""
    for wd in s.split():
        if cur and len(cur) + 1 + len(wd) > n: L.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    return L + ([cur] if cur else [])


def render(frames, durs, clips, sr, W, H, FPS, out, silent, wav, loud=-16, ANIM=30, XF=8, overlay=None):
    """Como comun.render() del diario, con overlay(fotograma, escena, segundo_en_escena, segundo_total) para los subtítulos."""
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
