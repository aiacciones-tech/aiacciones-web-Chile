"""Voz neuronal de Azure en alemán (de-DE-ConradNeural) para el vídeo largo de Wall Street auf Deutsch, frase a frase.
Corre en GitHub Actions (voz-GE.yml), porque el contenedor de Claude no llega a Azure. La clave nunca sale de los secretos.
Recurso de Azure Speech propio del canal (secretos AZURE_SPEECH_KEY_GE / AZURE_SPEECH_REGION_GE, plan F0: 500.000 caracteres al mes).
uso: AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=germanywestcentral python3 voz_azure.py <video.json> <carpeta de salida>
Escribe <clave>.wav (24 kHz, 16 bits, mono) por frase y manifest.json; make_video.py los usa con VOZ_DIR=<carpeta>."""
import json, os, sys, time, urllib.request, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voz_frases import frases, textos, clave, VOZ

RATE = os.environ.get("AZURE_RATE", "+0%")


def sintetiza(frase, key, region):
    ssml = (f"<speak version='1.0' xml:lang='de-DE'><voice name='{VOZ}'><prosody rate='{RATE}'>"
            f"{html.escape(frase)}</prosody></voice></speak>").encode()
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, headers={
        "Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "ge-diario"})
    for i in range(5):
        try:
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 4: time.sleep(2 ** i * 2); continue
            raise


def main():
    VJ = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    key = os.environ["AZURE_SPEECH_KEY"].strip()
    # el secreto puede estar como «Germany West Central»: Azure quiere «germanywestcentral»
    region = "".join(os.environ.get("AZURE_SPEECH_REGION", "germanywestcentral").split()).lower()
    F = [f for t in textos(VJ) for f in frases(t)]
    n = 0
    for f in F:
        p = os.path.join(out, clave(f) + ".wav")
        if os.path.exists(p): continue
        open(p, "wb").write(sintetiza(f, key, region)); n += 1
    json.dump({"voz": VOZ, "frases": len(F), "nuevas": n, "caracteres": sum(len(f) for f in F)}, open(os.path.join(out, "manifest.json"), "w"))
    print("frases", len(F), "nuevas", n, "caracteres", sum(len(f) for f in F))


if __name__ == "__main__":
    main()
