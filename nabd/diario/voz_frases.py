"""Partir la locución en frases (para los subtítulos y la voz frase a frase) y su clave de archivo. Sin dependencias pesadas:
lo usan comun.py (vídeo) y voz_azure.py (workflow voz-Nabd.yml), y los dos deben partir igual."""
import re, hashlib

MAX_PALABRAS = 16  # una frase más larga se parte en la coma más cercana a la mitad, para que el subtítulo quepa en dos líneas


def frases(texto):
    out = []
    for f in re.split(r"(?<=[.!؟?])\s+", " ".join(str(texto).split())):
        f = f.strip()
        if not f: continue
        pend = [f]
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith(("،", ",", "؛"))]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def clave(frase, voz="ar-SA-HamedNeural"):
    return hashlib.sha1((voz + "|" + frase).encode()).hexdigest()[:16]


def textos(VJ):
    """Todas las locuciones de un video.json (escenas fijas en "voz" y las cinco acciones en "acciones")."""
    T = [t for t in (VJ.get("voz") or {}).values() if t]
    T += [a["voz"] for a in VJ.get("acciones", []) if a.get("voz")]
    return T
