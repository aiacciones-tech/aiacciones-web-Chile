"""Voz neuronal de Azure (ar-SA-HamedNeural) para el video diario y el Short de @SaudiArabiaAIStocks, escena a escena.
Corre en GitHub Actions (voz-saudi.yml), porque el contenedor de Claude no llega a Azure. La clave nunca sale de los secretos.
uso: AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=northeurope python3 voz_azure.py <carpeta del día> <carpeta de salida>
Escribe <clave>.wav (24 kHz, 16 bits, mono) por cada locución que pedirán make_video.py y make_short.py, y manifest.json;
comun.voz() los usa con VOZ_DIR=<carpeta>. Un wav que ya existe en la salida no se vuelve a pedir (ahorra cuota si se re-sube el guion)."""
import json, os, sys, time, urllib.request, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voz_textos import textos_dia, clave, VOZ, RATE


def sintetiza(texto, key, region):
    ssml = (f"<speak version='1.0' xml:lang='ar-SA'><voice name='{VOZ}'><prosody rate='{RATE}'>"
            f"{html.escape(texto)}</prosody></voice></speak>").encode()
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, headers={
        "Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "saudi-diario"})
    for i in range(6):
        try:
            return urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            # 429: la cuota por minuto del plan gratuito (compartido con Nabd) -> esperar y repetir
            if e.code in (429, 500, 502, 503) and i < 5: time.sleep(2 ** i * 3); continue
            raise


def main():
    d, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    key, region = os.environ["AZURE_SPEECH_KEY"], os.environ.get("AZURE_SPEECH_REGION", "northeurope")
    T = textos_dia(d); n = c = 0
    for t in T:
        p = os.path.join(out, clave(t) + ".wav")
        if os.path.exists(p): continue
        open(p, "wb").write(sintetiza(t, key, region)); n += 1; c += len(t)
    json.dump({"voz": VOZ, "rate": RATE, "textos": len(T), "nuevos": n, "caracteres_pedidos": c}, open(os.path.join(out, "manifest.json"), "w"))
    print("textos", len(T), "nuevos", n, "caracteres pedidos a Azure", c)


if __name__ == "__main__":
    main()
