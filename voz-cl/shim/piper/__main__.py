"""Falso «python3 -m piper» para AIAcciones Chile: con PYTHONPATH=<repo>/voz-cl/shim y VOZ_DIR=<carpeta con los wav de Azure>,
cada locución sale de Azure (es-CL-LorenzoNeural) si su wav existe; si no, llama al Piper real y lo pasa a 24 kHz para que
todas las escenas tengan la misma frecuencia. Sin VOZ_DIR es Piper tal cual. Anota cada escena en VOZ_DIR/uso.log."""
import os, shutil, subprocess, sys, wave
SHIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(SHIM))
from voz_cl import clave, norm, SR

args = sys.argv[1:]
out = next((args[i + 1] for i, x in enumerate(args) if x in ("-f", "--output_file", "--output-file")), None)
texto = sys.stdin.read()
vd = os.environ.get("VOZ_DIR")


def log(s):
    if vd:
        try: open(os.path.join(vd, "uso.log"), "a").write(s + "\n")
        except OSError: pass


az = os.path.join(vd, clave(texto) + ".wav") if vd else None
if az and out and os.path.exists(az):
    shutil.copyfile(az, out); log("azure " + clave(texto)); sys.exit(0)

env = dict(os.environ)
env["PYTHONPATH"] = os.pathsep.join(p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p and os.path.abspath(p) != SHIM)
r = subprocess.run([sys.executable, "-m", "piper"] + args, input=texto.encode(), env=env)
if r.returncode: sys.exit(r.returncode)
if vd and out:
    import numpy as np
    w = wave.open(out); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32); w.close()
    if sr != SR:
        a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
        w = wave.open(out, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes()); w.close()
    log("piper " + clave(texto) + " " + norm(texto)[:60])
