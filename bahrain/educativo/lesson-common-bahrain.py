"""Shared pieces of the weekly Arabic lesson series «التحليل الفني ببساطة» of @BahrainAIStocks (bahrain/educativo/), adapted from
saudi/educativo/comun_leccion.py: Piper voice sentence by sentence (the channel's voice, ar_JO-kareem), subtitles and render() with overlay.
Brand, colours, ar(), logo and Piper settings come from bahrain/daily-bahrain/common-bahrain.py. Load with load("lesson-common-bahrain")."""
import os, re, sys, subprocess, wave, hashlib, importlib.util, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); DAILY = os.path.join(HERE, "..", "daily-bahrain")


def load(name, folder=None):
    """Imports a module whose file name has hyphens (repo rule: English names ending in -bahrain)."""
    p = os.path.join(folder or HERE, name + ".py"); s = importlib.util.spec_from_file_location(name.replace("-", "_"), p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


_C = load("common-bahrain", DAILY)
globals().update({k: v for k, v in vars(_C).items() if not k.startswith("__")})
MESES = load("technical-bahrain", DAILY).MESES

MARCA = "Bahrain AI Stocks"
SERIE = "التحليل الفني ببساطة"
DIA = "سبت"  # one lesson every Saturday (Bahrain Bourse closed, no daily video)
# In the voice, Latin names are written in Arabic letters so Piper reads them; the subtitles show them in their original form.
LATINO = {"بحرين إيه آي ستوكس": "Bahrain AI Stocks"}
sub_pantalla = lambda s: [s := s.replace(a, b) for a, b in LATINO.items()][-1]
PANEL = "#2A1218"; BANDA = (0x5A, 0x0A, 0x16); CAJA = np.array([24, 8, 12], np.float32)
MAX_PALABRAS = 16  # a longer sentence is cut at the comma nearest the middle, so the subtitle fits in two lines


def frases(texto):
    out = []
    for f in re.split(r"(?<=[.!?؟])\s+", " ".join(str(texto).split())):
        if not f.strip(): continue
        pend = [f.strip()]
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith(("،", ",", "؛", ";", ":")) and 3 <= i < len(w) - 3]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def clave(frase):
    return hashlib.sha1(("piper|" + " ".join(TTS) + "|" + " ".join(str(frase).split())).encode()).hexdigest()[:16]


def voz_frases(texto, wav_dir, gap=0.28):
    """Piper voice sentence by sentence (cached by sentence in wav_dir), for the subtitles. Returns (samples, sr, [(start, end, sentence)])."""
    F = frases(texto); trozos, sr = [], None
    for x in F:
        p = os.path.join(wav_dir, f"piper_{clave(x)}.wav")
        if not os.path.exists(p):
            subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-f", p] + TTS, input=(x + "\n").encode(), check=True, capture_output=True)
        w = wave.open(p); sr = w.getframerate(); trozos.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32))
    out, marcas, t = [], [], 0.0
    for x, a in zip(F, trozos):
        nz = np.where(np.abs(a) > 300)[0]
        if len(nz): a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)].copy()
        fi, fo = min(int(0.015 * sr), len(a)), min(int(0.06 * sr), len(a))
        a[:fi] *= np.linspace(0, 1, fi); a[len(a) - fo:] *= np.linspace(1, 0, fo)
        marcas.append((round(t, 3), round(t + len(a) / sr, 3), x)); out += [a, np.zeros(int(gap * sr), np.float32)]; t += len(a) / sr + gap
    return np.concatenate(out[:-1]), sr, marcas


def tira_texto(s, color, fs, H, w="bold"):
    """RGBA image of one line of text (Arabic, joined letters, RTL) cut to its width, for the subtitles."""
    W_ = max(400, int(len(str(s)) * fs * 1.2) + 160)
    f = plt.figure(figsize=(W_ / 100, H / 100), dpi=100); f.patch.set_alpha(0)
    f.text(0.5, 0.5, ar(s), color=color, fontsize=fs, weight=w, ha="center", va="center")
    f.canvas.draw(); a = np.asarray(f.canvas.buffer_rgba()).copy(); plt.close(f)
    cols = np.where(a[:, :, 3].max(axis=0) > 0)[0]
    return a[:, max(cols[0] - 4, 0):cols[-1] + 5] if len(cols) else a[:, :10]


def pegar(arr, rgba, x, y):
    h, w = rgba.shape[:2]; W_ = arr.shape[1]; x0, x1 = max(x, 0), min(x + w, W_)
    if x1 <= x0: return arr
    src = rgba[:, x0 - x:x1 - x].astype(np.float32); al = src[:, :, 3:4] / 255.0
    reg = arr[y:y + h, x0:x1].astype(np.float32); arr[y:y + h, x0:x1] = (reg * (1 - al) + src[:, :, :3] * al).astype(np.uint8)
    return arr


def partir(s, n):
    L, cur = [], ""
    for wd in s.split():
        if cur and len(cur) + 1 + len(wd) > n: L.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    return L + ([cur] if cur else [])


def render(frames, durs, clips, sr, W, H, FPS, out, silent, wav, loud=-16, ANIM=30, XF=8, overlay=None):
    """Writes the mp4: frames are functions t->array (animated during the first ANIM frames), crossfade XF, voice clips with lead-in,
    overlay(frame, scene, second_in_scene, second_total) for the subtitles. Returns the start time of each scene and the total."""
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
