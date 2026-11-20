"""Locución de una lección de «التحليل الفني ببساطة» (serie educativa de @QatarAIStocks) partida en frases, para los subtítulos y la voz
frase a frase (Piper ar_JO-kareem-medium, la voz del canal), y la clave del wav de cada frase (caché en AUD). Lo usan make_leccion.py y
make_short_leccion.py: los dos deben partir igual. Sin dependencias pesadas."""
import os, re, hashlib

VOZ = "piper-ar_JO-kareem-medium"
RATE = os.environ.get("LENGTH_SCALE", "0.8")
MAX_PALABRAS = 16  # una frase más larga se parte en la coma (، , ؛ :) más cercana a la mitad, para que el subtítulo quepa en dos líneas


def frases(texto):
    out = []
    for f in re.split(r"(?<=[.!?؟])\s+", " ".join(str(texto).split())):
        f = f.strip()
        if not f: continue
        pend = [f]
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith(("،", ",", "؛", ";", ":")) and 3 <= i < len(w) - 3]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def clave(frase):
    return hashlib.sha1((VOZ + "|" + RATE + "|" + " ".join(str(frase).split())).encode()).hexdigest()[:16]
