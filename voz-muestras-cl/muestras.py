"""Muestras de voces neurales de Azure (es-CL y otras latinas) para que Daniel elija la voz de AIAcciones Chile.
Corre en GitHub Actions (voz-muestras-cl.yml); la clave nunca sale de los secretos.
uso: AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=... python3 muestras.py <texto.txt> <carpeta de salida>"""
import html, os, sys, time, urllib.request, urllib.error

VOCES = [("1-chile-lorenzo-hombre", "es-CL-LorenzoNeural", "es-CL"),
         ("2-chile-catalina-mujer", "es-CL-CatalinaNeural", "es-CL"),
         ("3-mexico-jorge-hombre", "es-MX-JorgeNeural", "es-MX"),
         ("4-latino-alonso-hombre", "es-US-AlonsoNeural", "es-US")]


def sintetiza(texto, voz, lang, key, region):
    ssml = (f"<speak version='1.0' xml:lang='{lang}'><voice name='{voz}'>{html.escape(texto)}</voice></speak>").encode()
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, headers={
        "Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3", "User-Agent": "aiacciones-chile"})
    for i in range(6):
        try:
            return urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 5: time.sleep(2 ** i * 3); continue
            raise


def main():
    texto = open(sys.argv[1], encoding="utf-8").read().strip(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    key, region = os.environ["AZURE_SPEECH_KEY"], os.environ["AZURE_SPEECH_REGION"].strip()
    for nombre, voz, lang in VOCES:
        try:
            open(os.path.join(out, nombre + ".mp3"), "wb").write(sintetiza(texto, voz, lang, key, region))
            print("ok", nombre, voz)
        except Exception as e:
            print("FALLA", nombre, voz, type(e).__name__, getattr(e, "code", ""))


if __name__ == "__main__":
    main()
