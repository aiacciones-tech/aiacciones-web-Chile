"""Voz Azure ar-SA-HamedNeural (rate +8 %, la del canal) del «تقويم النتائج الأسبوعي» de Saudi Arabia AI Stocks, frase a frase.
Corre en GitHub Actions (calendario-saudi.yml), porque el contenedor de Claude no llega a Azure. Parte las frases y nombra los wav
igual que la serie educativa (saudi/educativo/voz_leccion.py), así comun_leccion.voz_frases() los encuentra con VOZ_DIR.
uso: AZURE_SPEECH_KEY=... python3 voz_calendario.py <carpeta de la semana> <carpeta de salida>
Solo pide a Azure las frases nuevas (cuota gratuita compartida: ~700 caracteres por semana)."""
import json, os, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "educativo"), os.path.join(HERE, "..", "diario")]
from voz_leccion import frases, clave, VOZ, RATE
import campana


def textos(carpeta):
    SJ = json.load(open(os.path.join(carpeta, "short.json")))
    T = [e["voz"] for e in SJ["escenas"] if e.get("voz")] + ([campana.VOZ_CORTA] if campana.activa(dt.date.fromisoformat(SJ["publicar"])) else [])
    F, vistos = [], set()
    for t in T:
        for x in frases(t):
            if clave(x) not in vistos: vistos.add(clave(x)); F.append(x)
    return F


if __name__ == "__main__":
    from voz_azure import sintetiza
    d, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    key, region = os.environ["AZURE_SPEECH_KEY"], os.environ.get("AZURE_SPEECH_REGION", "northeurope")
    F = textos(d); n = c = 0
    for x in F:
        p = os.path.join(out, clave(x) + ".wav")
        if os.path.exists(p): continue
        open(p, "wb").write(sintetiza(x, key, region)); n += 1; c += len(x)
    json.dump({"voz": VOZ, "rate": RATE, "frases": len(F), "nuevas": n, "caracteres_pedidos": c}, open(os.path.join(out, "manifest.json"), "w"))
    print("frases", len(F), "nuevas", n, "caracteres pedidos a Azure", c)
