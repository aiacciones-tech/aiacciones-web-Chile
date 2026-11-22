"""Azure neural voice (ar-BH-AliNeural) for the weekly results-calendar Short of @BahrainAIStocks, one wav per slide.
Runs in GitHub Actions (voz-calendar-bahrain.yml): the Claude container cannot reach Azure. The key never leaves the secrets.
  AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=northeurope python3 voz_calendar_bahrain.py <week folder> <out folder>
Writes <clave>.wav (24 kHz, 16-bit, mono) for every "voice" line of <week folder>/short-*.json; make-calendar-bahrain.py uses them
with VOZ_DIR=<folder>. A wav already in the out folder is not requested again."""
import glob, hashlib, html, json, os, sys, time, urllib.request

VOZ = os.environ.get("AZURE_VOZ_BH", "ar-BH-AliNeural")
RATE = os.environ.get("AZURE_RATE_BH", "+0%")


def clave(texto):
    return hashlib.sha1((VOZ + "|" + RATE + "|" + " ".join(str(texto).split())).encode()).hexdigest()[:16]


def textos(folder):
    T = []
    for p in sorted(glob.glob(os.path.join(folder, "short-*.json"))):
        for sl in json.load(open(p, encoding="utf-8"))["slides"]:
            if sl.get("voice") and sl["voice"] not in T:
                T.append(sl["voice"])
    return T


def sintetiza(texto, key, region):
    ssml = (f"<speak version='1.0' xml:lang='ar-BH'><voice name='{VOZ}'><prosody rate='{RATE}'>"
            f"{html.escape(texto)}</prosody></voice></speak>").encode()
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, headers={
        "Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "bahrain-calendar"})
    for i in range(6):
        try:
            return urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 5:  # free F0 plan shared with Nabd/Saudi: wait and retry
                time.sleep(2 ** i * 3); continue
            raise


def main():
    d, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    key, region = os.environ["AZURE_SPEECH_KEY"], os.environ.get("AZURE_SPEECH_REGION", "northeurope")
    T = textos(d); n = c = 0
    for t in T:
        p = os.path.join(out, clave(t) + ".wav")
        if os.path.exists(p): continue
        open(p, "wb").write(sintetiza(t, key, region)); n += 1; c += len(t)
    json.dump({"voz": VOZ, "rate": RATE, "textos": len(T), "nuevos": n, "caracteres_pedidos": c},
              open(os.path.join(out, "manifest.json"), "w"))
    print("texts", len(T), "new", n, "characters sent to Azure", c)


if __name__ == "__main__":
    main()
