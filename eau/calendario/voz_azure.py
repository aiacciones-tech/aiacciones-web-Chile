"""Voz neuronal de Azure (ar-AE-HamdanNeural, emiratí) del Short semanal «تقويم النتائج الأسبوعي» de @AIStocksUAE.
Corre en GitHub Actions (voz-eau.yml), porque el contenedor de Claude no llega a Azure. La clave nunca sale de los secretos.
uso: AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=... python3 voz_azure.py <carpeta de la semana> <carpeta de salida>
Escribe <clave>.wav (24 kHz, 16 bits, mono) por locución y manifest.json; un wav que ya existe no se vuelve a pedir."""
import json, os, sys, time, html, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voz_textos import textos, clave, VOZ, RATE


def sintetiza(texto, key, region):
    ssml = (f"<speak version='1.0' xml:lang='ar-AE'><voice name='{VOZ}'><prosody rate='{RATE}'>"
            f"{html.escape(texto)}</prosody></voice></speak>").encode()
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, headers={
        "Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "eau-calendario"})
    for i in range(6):
        try:
            return urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 5: time.sleep(2 ** i * 3); continue
            raise


def main():
    d, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    key, region = os.environ["AZURE_SPEECH_KEY"], os.environ.get("AZURE_SPEECH_REGION", "northeurope")
    T = textos(d); n = c = 0
    for t in T:
        p = os.path.join(out, clave(t) + ".wav")
        if os.path.exists(p): continue
        open(p, "wb").write(sintetiza(t, key, region)); n += 1; c += len(t)
    json.dump({"voz": VOZ, "rate": RATE, "textos": len(T), "nuevos": n, "caracteres_pedidos": c}, open(os.path.join(out, "manifest.json"), "w"))
    print("textos", len(T), "nuevos", n, "caracteres pedidos a Azure", c)


if __name__ == "__main__":
    main()
