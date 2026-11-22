"""Locuciones del Short del calendario semanal de resultados y la clave de su wav de Azure (ar-AE-HamdanNeural).
Lo usan make_short.py (render, con VOZ_DIR) y voz_azure.py (workflow voz-eau.yml): deben coincidir texto a texto."""
import os, json, hashlib

VOZ = os.environ.get("AZURE_VOZ", "ar-AE-HamdanNeural")
RATE = os.environ.get("AZURE_RATE", "+12%")


def clave(texto):
    return hashlib.sha1((VOZ + "|" + RATE + "|" + " ".join(str(texto).split())).encode()).hexdigest()[:16]


def textos(d):
    S = json.load(open(os.path.join(d, "short.json")))
    T, vistos = [], set()
    for e in S["escenas"]:
        t = e.get("voz", "").strip()
        if t and clave(t) not in vistos: vistos.add(clave(t)); T.append(t)
    return T
