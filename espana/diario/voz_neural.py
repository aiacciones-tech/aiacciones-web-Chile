"""Locución con voz neuronal (Microsoft Edge, es-ES-AlvaroNeural) para el vídeo diario: suena natural, no robótica (Daniel, 10-nov-2026).
Se ejecuta en GitHub Actions (workflow voz-espana.yml), porque el contenedor de Claude no llega al servicio de voz.
uso: python3 voz_neural.py <textos.json> <carpeta salida>   textos.json = {"nombre": "texto", ...} (opcional "_voz", "_rate")."""
import asyncio, json, os, sys
import edge_tts

async def main(src, out):
    T = json.load(open(src)); voz = T.pop("_voz", "es-ES-AlvaroNeural"); rate = T.pop("_rate", "+0%")
    os.makedirs(out, exist_ok=True)
    for k, txt in T.items():
        for intento in range(4):
            try:
                await edge_tts.Communicate(txt, voz, rate=rate).save(os.path.join(out, k + ".mp3")); break
            except Exception as e:
                print("reintento", k, e); await asyncio.sleep(3 * (intento + 1))
        else:
            sys.exit(f"sin audio para {k}")
        print("ok", k)

asyncio.run(main(sys.argv[1], sys.argv[2]))
