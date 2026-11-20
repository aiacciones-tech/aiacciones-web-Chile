"""Voz neuronal es-ES-AlvaroNeural (la del vídeo diario) de una lección de «Análisis técnico, explicado fácil», frase a frase.
Corre en GitHub Actions (educativo-espana.yml), porque el contenedor de Claude no llega al servicio de voz de Microsoft (edge-tts).
uso: python3 voz_edge_leccion.py <carpeta de la lección> <carpeta de salida>
Escribe <clave>.mp3 por frase; los que ya existen no se vuelven a pedir (re-subir el guion solo pide las frases cambiadas)."""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voz_leccion import textos, clave, VOZ, RATE
import edge_tts


async def main(d, out):
    os.makedirs(out, exist_ok=True); F = textos(d); n = 0
    for x in F:
        p = os.path.join(out, clave(x) + ".mp3")
        if os.path.exists(p) and os.path.getsize(p) > 0: continue
        for intento in range(5):
            try:
                await edge_tts.Communicate(x, VOZ, rate=RATE).save(p)
                if os.path.getsize(p) > 0: break
            except Exception as e:
                print("reintento", intento, e)
            await asyncio.sleep(3 * (intento + 1))
        else:
            sys.exit(f"sin audio para: {x}")
        n += 1
    json.dump({"voz": VOZ, "rate": RATE, "frases": len(F), "nuevas": n}, open(os.path.join(out, "manifest.json"), "w"))
    print("frases", len(F), "nuevas", n)

asyncio.run(main(sys.argv[1], sys.argv[2]))
