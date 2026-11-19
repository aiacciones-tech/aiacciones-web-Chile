"""Voz Azure ar-SA-HamedNeural (rate +8 %, la del vídeo diario) de una lección de «التحليل الفني ببساطة», frase a frase.
Corre en GitHub Actions (educativo-saudi.yml), porque el contenedor de Claude no llega a Azure. Reutiliza sintetiza() de saudi/diario/voz_azure.py.
uso: AZURE_SPEECH_KEY=... python3 voz_azure_leccion.py <carpeta de la lección> <carpeta de salida>
Escribe <clave>.wav por frase; los que ya existen no se vuelven a pedir (re-subir el guion solo pide las frases cambiadas)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from voz_leccion import textos, clave, VOZ, RATE
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
