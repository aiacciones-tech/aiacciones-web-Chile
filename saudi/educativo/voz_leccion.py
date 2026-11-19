"""Locución de una lección de «التحليل الفني ببساطة» (serie educativa de @SaudiArabiaAIStocks) partida en frases, para los subtítulos
y la voz frase a frase, y la clave del wav de Azure de cada frase. Lo usan make_leccion.py, make_short_leccion.py (render) y
voz_azure_leccion.py (workflow educativo-saudi.yml): los tres deben partir igual. Sin dependencias pesadas."""
import os, re, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diario"))
import campana

VOZ = os.environ.get("AZURE_VOZ", "ar-SA-HamedNeural")   # la misma voz que el vídeo diario (Daniel, 18-nov-2026)
RATE = os.environ.get("AZURE_RATE", "+8%")
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


def textos(carpeta):
    """Todas las frases de la lección (escenas del vídeo y del Short, en video.json, y las de la campaña de campana.py), sin repetir."""
    VJ = json.load(open(os.path.join(carpeta, "video.json")))
    T = [e["voz"] for e in VJ.get("escenas", []) if e.get("voz")] + [e["voz"] for e in VJ.get("short", []) if e.get("voz")]
    if campana.activa(): T += [campana.VOZ, campana.VOZ_CORTA]
    F, vistos = [], set()
    for t in T:
        for x in frases(t):
            if clave(x) not in vistos: vistos.add(clave(x)); F.append(x)
    return F
