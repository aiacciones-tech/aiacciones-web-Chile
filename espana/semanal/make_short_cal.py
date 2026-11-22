# Short vertical (1080x1920, 45-60 s) «Calendario semanal de resultados» de @AIAccionesEspaña (Daniel, 22-nov-2026).
# Escenas: gancho (3 s) -> una por empresa (6-8 s, en orden cronológico) -> cierre.
# Uso: AUD=<scratch> python3 make_short_cal.py <carpeta>/calendario.json [preview]
# La voz neuronal (es-ES-AlvaroNeural) viene de <carpeta>/voz/short_<i>.mp3 (voz_cal.sh); si falta, Piper.
import subprocess, os, sys, wave, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import imageio_ffmpeg
from PIL import Image
plt.rcParams['text.parse_math'] = False

W, H, FPS = 1080, 1920, 30
BG = "#0B1E3A"; FG = "#FFFFFF"; MUTED = "#9FB3CC"; ACC = "#2FB7A3"; ACC2 = "#4C8DF0"; NEG = "#F2A541"; DIM = "#3A5378"; CARD = "#12294B"
LOGO = os.environ.get("LOGO", "/mnt/project-files/espana/marca/logo-aiacciones-espana.png")
VOICE = os.environ.get("VOICE", "/mnt/project-files/espana/voz/vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD = os.environ.get("AUD", "aud")
MINDUR, MAXDUR = 45.0, 60.0
CTA_HASTA = "2026-11-22"  # campaña «comenta y suscríbete» (Daniel, 8-nov-2026)


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
def box(f, x, y, w, h, c, a=1.0):
    f.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.018", transform=f.transFigure,
                                    facecolor=c, edgecolor="none", alpha=a, figure=f))


def s_gancho(e, t):
    f = fig(); a = ease(t / 0.4)
    f.text(0.07, 0.735, "CALENDARIO DE RESULTADOS", color=ACC, fontsize=38, weight="bold", alpha=a)
    f.text(0.07, 0.665, S["rango"], color=FG, fontsize=88, weight="bold", alpha=a)
    f.text(0.07, 0.630, S["semana_txt"], color=ACC2, fontsize=34, weight="bold", alpha=a)
    b = ease((t - 0.15) / 0.4)
    f.text(0.07, 0.565, e["titular"], color=FG, fontsize=50, weight="bold", alpha=b, linespacing=1.25, va="top")
    for i, emp in enumerate(S["empresas"]):
        c = ease((t - 0.25 - i * 0.06) / 0.35); y = 0.415 - i * 0.036
        f.text(0.07, y, emp["dia_corto"].upper(), color=ACC, fontsize=34, weight="bold", alpha=c)
        f.text(0.30, y, emp["nombre"], color=FG, fontsize=36, weight="bold", alpha=c)
    return with_logo(to_arr(f), LGB, y=150)


def s_empresa(e, t):
    f = fig(); n = e["n"]; tot = len(S["empresas"])
    f.text(0.07, 0.79, f"RESULTADOS · {S['rango']}", color=ACC, fontsize=30, weight="bold")
    for i in range(tot):
        f.patches.append(plt.Rectangle((0.07 + i * (0.86 / tot), 0.772), 0.86 / tot - 0.012, 0.006, transform=f.transFigure,
                                       color=ACC if i < n else DIM, figure=f))
    a = ease(t / 0.35)
    box(f, 0.07, 0.675, 0.86, 0.075, ACC, a)
    f.text(0.10, 0.712, e["dia_largo"].upper(), color=BG, fontsize=46, weight="bold", va="center", alpha=a)
    f.text(0.07, 0.640, e["hora"], color=ACC, fontsize=36, weight="bold", va="center", alpha=a)
    b = ease((t - 0.1) / 0.4)
    nombre = e["nombre"]; fs = 84 if len(nombre) <= 14 else (68 if len(nombre) <= 18 else 56)
    f.text(0.07, 0.565, nombre, color=FG, fontsize=fs, weight="bold", alpha=b)
    f.text(0.07, 0.530, f"{e['ticker']} · {e['bolsa']}", color=ACC2, fontsize=36, weight="bold", alpha=b)
    if e.get("periodo"): f.text(0.07, 0.497, e["periodo"], color=MUTED, fontsize=30, alpha=b)
    kp = [k for k in (("BPA esperado", e.get("bpa")), ("Ingresos esperados", e.get("ingresos"))) if k[1]]
    for i, (lab, val) in enumerate(kp):
        c = ease((t - 0.25 - i * 0.12) / 0.4); y = 0.37 - i * 0.107
        box(f, 0.07, y, 0.86, 0.095, CARD, c)
        f.text(0.10, y + 0.072, lab.upper(), color=MUTED, fontsize=28, weight="bold", va="center", alpha=c)
        f.text(0.10, y + 0.032, val, color=NEG if i == 0 else FG, fontsize=74, weight="bold", va="center", alpha=c)
    if not kp and e.get("sin_consenso"):
        c = ease((t - 0.25) / 0.4)
        box(f, 0.07, 0.34, 0.86, 0.12, CARD, c)
        f.text(0.10, 0.40, e["sin_consenso"], color=FG, fontsize=38, weight="bold", va="center", alpha=c, linespacing=1.3)
    if e.get("nota"):
        f.text(0.07, 0.205, e["nota"], color=MUTED, fontsize=27, alpha=ease((t - 0.4) / 0.4), linespacing=1.35)
    return with_logo(to_arr(f))


def s_fin(e, t):
    f = fig(); a = ease(t / 0.4)
    f.text(0.07, 0.68, "Sigue el canal", color=FG, fontsize=78, weight="bold", alpha=a)
    f.text(0.07, 0.635, "para el análisis de cada reporte", color=ACC, fontsize=44, weight="bold", alpha=a)
    f.text(0.07, 0.55, "▶ YouTube @AIAccionesEspaña", color=ACC2, fontsize=44, weight="bold", alpha=ease((t - 0.15) / 0.4))
    if S["fecha"] <= CTA_HASTA:
        f.text(0.07, 0.50, "Déjanos tu comentario y suscríbete", color=FG, fontsize=40, weight="bold", alpha=ease((t - 0.25) / 0.4))
    f.text(0.07, 0.235, S["fuente_pantalla"] + "\nContenido informativo, no es recomendación\nde inversión. Sin posiciones en las empresas.\nInvertir conlleva riesgo.",
           color=MUTED, fontsize=24, linespacing=1.45, alpha=a)
    return with_logo(to_arr(f), LGB, y=150)


def escenas(S):
    E = [dict(S["gancho"], tipo="gancho")]
    for i, emp in enumerate(S["empresas"]): E.append(dict(emp, tipo="empresa", n=i + 1))
    E.append(dict(S["cierre"], tipo="fin")); return E

R = {"gancho": s_gancho, "empresa": s_empresa, "fin": s_fin}
def frame(e, t): return R[e["tipo"]](e, t)

if __name__ == "__main__":
    src = os.path.abspath(sys.argv[1]); D = os.path.dirname(src)
    S = json.load(open(src)); E = escenas(S); out = os.path.join(D, S["out"]); os.makedirs(AUD, exist_ok=True)
    assert 5 <= len(S["empresas"]) <= 7, "el formato pide de 5 a 7 empresas"
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        for i, e in enumerate(E): Image.fromarray(frame(e, 1.0)).save(os.path.join(AUD, f"cal_prev_{i}.png"))
        print("preview en", AUD); sys.exit()
    LEAD, TAIL = 0.10, 0.30
    clips = []; ff = imageio_ffmpeg.get_ffmpeg_exe()
    for i, e in enumerate(E):
        p = os.path.join(AUD, f"cal_{i}.wav"); mp = os.path.join(D, "voz", f"short_{i}.mp3")
        if os.path.exists(mp): subprocess.run([ff, "-y", "-loglevel", "error", "-i", mp, "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", p], check=True)
        else:
            print("AVISO: sin voz neuronal para la escena", i, "-> Piper", flush=True)
            subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-f", p, "--length-scale", "0.95"], input=(e["voz"] + "\n").encode(),
                           check=True, stderr=subprocess.DEVNULL)
        w = wave.open(p); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
        nz = np.where(np.abs(a) > 300)[0]; a = a[max(nz[0] - int(0.03 * sr), 0):nz[-1] + int(0.08 * sr)]
        fi, fo = int(0.015 * sr), int(0.06 * sr); a[:fi] *= np.linspace(0, 1, fi); a[-fo:] *= np.linspace(1, 0, fo); clips.append(a)
    durs = [LEAD + len(a) / sr + TAIL for a in clips]; durs[-1] += 1.2
    tot = sum(durs); print("duraciones:", [round(d, 1) for d in durs], "total", round(tot, 1), "s")
    if tot > MAXDUR: sys.exit(f"Short demasiado largo: {tot:.1f} s (máx {MAXDUR}). Acorta la voz.")
    if tot < MINDUR: print(f"AVISO: {tot:.1f} s, menos de {MINDUR} s")
    ANIM = 20; XF = 6; silent = os.path.join(AUD, "cal-silent.mp4")
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
    subprocess.run([ff, "-y", "-i", silent, "-i", wf, "-af", AF, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    "-movflags", "+faststart", out], check=True, stderr=subprocess.DEVNULL)
    Image.fromarray(frame(E[0], 1.0)).save(os.path.join(D, "portada.png"))
    json.dump({"total": round(tot, 1), "escenas": [round(d, 1) for d in durs]}, open(os.path.join(D, "times.json"), "w"))
    print("listo", out, round(tot, 1), "s")
