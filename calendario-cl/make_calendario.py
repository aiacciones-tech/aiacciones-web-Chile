# Short vertical (1080x1920, 45-60 s) «Calendario semanal de resultados» de @aiaccioneschile, voz Azure Lorenzo (voz-cl/).
# Lee calendario-cl/semanas/<lunes>/short.json y escribe el mp4 en spec["out"] (relativo a la carpeta del JSON).
# Uso: PYTHONPATH=<repo>/voz-cl/shim VOZ_DIR=<voz> AUD=<scratch> python3 make_calendario.py <dir>/short.json [preview]
import subprocess, os, sys, wave, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import imageio_ffmpeg
from PIL import Image
plt.rcParams['text.parse_math'] = False
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H, FPS = 1080, 1920, 30
BG = "#0B1E3A"; FG = "#FFFFFF"; MUTED = "#9FB3CC"; ACC = "#2FB7A3"; ACC2 = "#4C8DF0"; NEG = "#F2A541"; DIM = "#3A5378"; CARD = "#12294B"
LOGO = os.environ.get("LOGO", os.path.join(R, "web/assets/logo-aiacciones-chile.png"))
VOICE = os.environ.get("VOICE", "vits-piper-es_MX-claude-high/es_MX-claude-high.onnx")
AUD = os.environ.get("AUD", "aud")
MINDUR, MAXDUR = 45.0, 60.0
# Zonas seguras de Shorts: arriba ~8%, abajo ~22% y franja derecha (botones). Contenido entre y=0.25 y y=0.88.

def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def fig():
    f = plt.figure(figsize=(W / 100, H / 100), dpi=100); f.patch.set_facecolor(BG); return f
def to_arr(f):
    f.canvas.draw(); a = np.asarray(f.canvas.buffer_rgba())[:, :, :3].copy(); plt.close(f); return a
def load_logo(w):
    im = Image.open(LOGO).convert("RGBA"); h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0; return a[:, :, :3] * 255.0, a[:, :, 3:4]
LG = load_logo(400); LGB = load_logo(600)
def with_logo(arr, lg=LG, y=170):
    rgb, al = lg; h, w = al.shape[:2]; x = (W - w) // 2
    reg = arr[y:y + h, x:x + w].astype(np.float32); arr[y:y + h, x:x + w] = (reg * (1 - al) + rgb * al).astype(np.uint8); return arr
def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=c, alpha=a, figure=f))

def cabecera(f, e):
    f.text(0.07, 0.80, f"CALENDARIO DE RESULTADOS · {S['rango']}", color=ACC, fontsize=28, weight="bold")
    emp = [x for x in S["escenas"] if x["tipo"] == "empresa"]
    if e in emp:
        i0 = emp.index(e); n = len(emp); wd = 0.80 / n
        for i in range(n): rect(f, 0.07 + i * wd, 0.785, wd - 0.012, 0.006, ACC if i <= i0 else DIM)

def s_gancho(e, t):
    f = fig(); a = ease(t / 0.45); b = ease((t - 0.25) / 0.45)
    f.text(0.07, 0.72, "CALENDARIO DE RESULTADOS", color=ACC, fontsize=40, weight="bold", alpha=a)
    f.text(0.07, 0.675, f"Semana del {S['semana']}", color=ACC2, fontsize=34, weight="bold", alpha=a)
    f.text(0.07, 0.56, "Esta semana reporta", color=FG, fontsize=54, alpha=a)
    f.text(0.07, 0.465, e["top"], color=FG, fontsize=150, weight="bold", alpha=b)
    f.text(0.07, 0.395, f"… y {e['n_mas']} empresas más", color=NEG, fontsize=56, weight="bold", alpha=ease((t - 0.45) / 0.4))
    f.text(0.07, 0.345, "que mueven el mercado", color=MUTED, fontsize=44, alpha=ease((t - 0.45) / 0.4))
    return with_logo(to_arr(f), LGB, y=150)

def s_empresa(e, t):
    f = fig(); cabecera(f, e); a = ease(t / 0.35); b = ease((t - 0.15) / 0.4); c = ease((t - 0.3) / 0.4)
    f.text(0.07, 0.715, e["dia"].upper(), color=FG, fontsize=64, weight="bold", alpha=a)
    hc = ACC2 if "apertura" in e["hora"] else (NEG if "cierre" in e["hora"] else MUTED)
    f.text(0.07, 0.678, e["hora"], color=hc, fontsize=38, weight="bold", alpha=a)
    fs = 96 if len(e["nombre"]) <= 14 else 80
    f.text(0.07, 0.585, e["nombre"], color=FG, fontsize=fs, weight="bold", alpha=b)
    f.text(0.07, 0.545, f"{e['ticker']}  ·  {e['pais']}", color=ACC, fontsize=38, weight="bold", alpha=b)
    if e.get("bpa") or e.get("ingresos"):
        f.text(0.07, 0.49, "Lo que espera el mercado (consenso)", color=MUTED, fontsize=30, alpha=c)
        for i, (lab, k) in enumerate((("BPA", "bpa"), ("Ingresos", "ingresos"))):
            if not e.get(k): continue
            x = 0.07 + i * 0.40
            rect(f, x, 0.36, 0.37 if i == 0 else 0.44, 0.11, CARD, a=c)
            f.text(x + 0.03, 0.435, lab, color=MUTED, fontsize=30, alpha=c)
            f.text(x + 0.03, 0.38, e[k], color=FG, fontsize=58 if len(e[k]) <= 10 else 48, weight="bold", alpha=c)
        f.text(0.07, 0.33, "Trimestre que se reporta. Fuente: " + e["src"], color=MUTED, fontsize=24, alpha=c)
    else:
        # Sin consenso verificado no se muestra ninguna cifra (regla del formato); solo la nota y la fuente de la fecha.
        if e.get("nota"): f.text(0.07, 0.505, e["nota"], color=FG, fontsize=40, alpha=c, linespacing=1.3, va="top")
        f.text(0.07, 0.33, "Fecha: " + e["src"], color=MUTED, fontsize=24, alpha=c)
    return with_logo(to_arr(f))

def s_fin(e, t):
    f = fig(); a = ease(t / 0.45); b = ease((t - 0.2) / 0.45)
    f.text(0.07, 0.64, "Sigue el canal", color=FG, fontsize=84, weight="bold", alpha=a)
    f.text(0.07, 0.585, "para el análisis de cada reporte", color=ACC, fontsize=44, weight="bold", alpha=a)
    f.text(0.07, 0.50, "▶ YouTube @aiaccioneschile", color=ACC2, fontsize=42, weight="bold", alpha=b)
    f.text(0.07, 0.455, "aiacciones.cl/calendario", color=ACC, fontsize=40, weight="bold", alpha=b)
    f.text(0.07, 0.27, S["fuente"] + "\nContenido informativo, no es recomendación\nde inversión. Las fechas pueden cambiar.",
           color=MUTED, fontsize=23, linespacing=1.45, alpha=a)
    return with_logo(to_arr(f), LGB, y=150)

RND = {"gancho": s_gancho, "empresa": s_empresa, "fin": s_fin}
def frame(e, t): return RND[e["tipo"]](e, t)

if __name__ == "__main__":
    S = json.load(open(sys.argv[1], encoding="utf-8")); E = S["escenas"]
    S["out"] = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), S["out"]); os.makedirs(AUD, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"cal_prev_{i}.png"))
        sys.exit()
    TTS = ["--length-scale", "0.95", "--noise-scale", "0.55", "--noise-w-scale", "0.6", "--sentence-silence", "0.1"]
    LEAD, TAIL = 0.10, 0.30
    clips = []
    for i, e in enumerate(E):
        p = os.path.join(AUD, f"cal_{i}.wav")
        subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-f", p] + TTS, input=(e["voz"] + "\n").encode(), check=True, stderr=subprocess.DEVNULL)
        w = wave.open(p); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
        nz = np.where(np.abs(a) > 300)[0]; a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)]
        fi, fo = int(0.015 * sr), int(0.06 * sr); a[:fi] *= np.linspace(0, 1, fi); a[-fo:] *= np.linspace(1, 0, fo); clips.append(a)
    durs = [LEAD + len(a) / sr + TAIL for a in clips]; durs[-1] += 1.2
    tot = sum(durs); print("duraciones", [round(d, 1) for d in durs], "total", round(tot, 1))
    if tot > MAXDUR: sys.exit(f"Short demasiado largo: {tot:.1f} s (máx {MAXDUR}). Acorta las locuciones.")
    if tot < MINDUR: durs[-1] += MINDUR - tot  # el cierre se queda en pantalla hasta llegar a 45 s
    ANIM = 20; XF = 6; ff = imageio_ffmpeg.get_ffmpeg_exe(); silent = os.path.join(AUD, "cal-silent.mp4")
    proc = subprocess.Popen([ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", silent], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    audio = []; bgc = np.array([int(BG[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    for j, (e, dur, a) in enumerate(zip(E, durs, clips)):
        total = int(round(dur * FPS)); last = None
        nxt = frame(E[j + 1], 0).astype(np.float32) if j + 1 < len(E) else np.zeros((H, W, 3), np.float32) + bgc
        for k in range(total):
            if k < ANIM: last = frame(e, k / (ANIM - 1))
            fr = last.astype(np.float32)
            if k >= total - XF: al = (total - k) / (XF + 1); fr = fr * al + nxt * (1 - al)
            proc.stdin.write(fr.astype(np.uint8).tobytes())
        n = int(round(total / FPS * sr)); seg = np.zeros(n, np.float32); st = int(LEAD * sr); seg[st:st + len(a)] = a[:n - st]; audio.append(seg)
    proc.stdin.close(); proc.wait()
    full = np.clip(np.concatenate(audio), -32768, 32767).astype(np.int16)
    wf = os.path.join(AUD, "cal-full.wav"); w = wave.open(wf, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(full.tobytes()); w.close()
    AF = "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250,loudnorm=I=-14:TP=-1.5:LRA=9"
    subprocess.run([ff, "-y", "-i", silent, "-i", wf, "-af", AF, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", S["out"]], check=True, stderr=subprocess.DEVNULL)
    print("listo", S["out"], round(sum(durs), 1), "s")
