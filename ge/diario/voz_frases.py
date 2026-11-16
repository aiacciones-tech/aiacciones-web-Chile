"""Locución partida en frases (subtítulos y voz frase a frase) y clave de archivo, para el vídeo diario en alemán de Wall Street auf Deutsch.
Lo usan comun.py (vídeo) y voz_azure.py (workflow voz-GE.yml): los dos deben partir igual. Sin dependencias pesadas."""
import os, re, hashlib

VOZ = os.environ.get("AZURE_VOZ", "de-DE-ConradNeural")   # de-DE-ConradNeural (masculina) o de-DE-KatjaNeural (femenina)
MAX_PALABRAS = 14  # el alemán tiene palabras largas: una frase más larga se parte en la coma más cercana a la mitad


def frases(texto):
    out = []
    for f in re.split(r"(?<=[.!?])\s+", " ".join(str(texto).split())):
        f = f.strip()
        if not f: continue
        pend = [f]
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith((",", ";", ":"))]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def clave(frase, voz=VOZ):
    return hashlib.sha1((voz + "|" + frase).encode()).hexdigest()[:16]


def textos(VJ):
    """Todas las locuciones de un video.json (escenas fijas en "voz" y las cinco acciones en "acciones")
    o de un short.json (la "voz" de cada escena): voz-GE.yml genera con Azure las dos, en la misma carpeta."""
    T = [t for t in (VJ.get("voz") or {}).values() if t] if isinstance(VJ.get("voz"), dict) else []
    T += [a["voz"] for a in VJ.get("acciones", []) if a.get("voz")]
    T += [e["voz"] for e in VJ.get("escenas", []) if e.get("voz")]
    return T
