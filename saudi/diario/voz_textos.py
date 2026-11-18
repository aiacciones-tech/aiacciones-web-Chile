"""Locuciones del día que leen make_video.py y make_short.py, y la clave de su wav de Azure. Sin dependencias pesadas:
lo usan comun.voz() (render) y voz_azure.py (workflow voz-saudi.yml), y deben coincidir texto a texto."""
import os, json, hashlib
import campana

VOZ = os.environ.get("AZURE_VOZ", "ar-SA-HamedNeural")
RATE = os.environ.get("AZURE_RATE", "+8%")


def clave(texto):
    return hashlib.sha1((VOZ + "|" + RATE + "|" + " ".join(str(texto).split())).encode()).hexdigest()[:16]


def textos_dia(d):
    """Todas las locuciones posibles de la carpeta del día: escenas del video, tarjeta de la campaña y escenas del Short
    (la última, con y sin la frase corta de la campaña, para que valga se active o no)."""
    T = []
    p = os.path.join(d, "video.json")
    if os.path.exists(p):
        T += [v for v in json.load(open(p)).get("voz", {}).values() if isinstance(v, str) and v.strip()]
        T.append(campana.VOZ)
    p = os.path.join(d, "short.json")
    if os.path.exists(p):
        for e in json.load(open(p)).get("escenas", []):
            if not e.get("voz"): continue
            T.append(e["voz"])
            if e.get("tipo") == "fin": T.append(campana.VOZ_CORTA + " " + e["voz"])
    vistos = set()
    return [t for t in T if not (clave(t) in vistos or vistos.add(clave(t)))]
