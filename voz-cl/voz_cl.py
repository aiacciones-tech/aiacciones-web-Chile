"""Voz Azure es-CL-LorenzoNeural para los videos de AIAcciones Chile (Daniel la eligió el 18-nov-2026; Piper queda de respaldo).
El contenedor de Claude no llega a Azure: el workflow voz-chile.yml sintetiza y deja un wav por locución en la rama voz-cl.
Cada wav se nombra con clave(texto); el falso módulo piper de voz-cl/shim/ lo busca en VOZ_DIR y, si no está, llama a Piper.

  python3 voz_cl.py pedido <id> <fuente>...     JSON del pedido (stdout). Fuentes: narracion*.py (dict N), video.json (dict "voz"),
                                                short*.json ("escenas"[].voz) o .txt (una locución por línea).
  python3 voz_cl.py sintetizar <pedido.json> <dir>   (solo en Actions; pide a Azure las que falten en <dir>)
  python3 voz_cl.py faltan <VOZ_DIR> <fuente>...    locuciones sin wav de Azure
  python3 voz_cl.py resumen <VOZ_DIR>               cuántas escenas salieron con Azure y cuántas con Piper (uso.log del shim)
"""
import datetime as dt, hashlib, html, importlib.util, json, os, sys, time, urllib.error, urllib.request

VOZ = os.environ.get("AZURE_VOZ_CL", "es-CL-LorenzoNeural")
RATE = os.environ.get("AZURE_RATE_CL", "0%")
SR = 24000
HERE = os.path.dirname(os.path.abspath(__file__))


def norm(texto):
    return " ".join(str(texto).split())


def clave(texto):
    return hashlib.sha1((VOZ + "|" + RATE + "|" + norm(texto)).encode()).hexdigest()[:16]


def _campana():
    """Frases de la campaña de comentarios del diario (diario/campana.py), que make_video/make_short agregan al cierre."""
    try:
        sp = importlib.util.spec_from_file_location("campana_cl", os.path.join(HERE, "..", "diario", "campana.py"))
        m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        return m if dt.date.today().isoformat() <= m.HASTA else None
    except Exception:
        return None


def textos_de(fuentes):
    T, c = [], _campana()
    for f in fuentes:
        if f.endswith(".py"):
            sp = importlib.util.spec_from_file_location("narr", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
            T += [v for v in m.N.values() if isinstance(v, str)]
        elif f.endswith(".json"):
            j = json.load(open(f, encoding="utf-8"))
            for k, v in (j.get("voz") or {}).items():
                if isinstance(v, str):
                    T.append(v)
                    if k == "s_fin" and c: T.append(v + " " + c.VOZ_VIDEO)
            for e in j.get("escenas", []):
                if e.get("voz"):
                    T.append(e["voz"])
                    if e.get("tipo") == "fin" and c: T.append(e["voz"] + " " + c.VOZ_SHORT)
        else:
            T += [l for l in open(f, encoding="utf-8").read().splitlines()]
    vistos, out = set(), []
    for t in T:
        if norm(t) and clave(t) not in vistos:
            vistos.add(clave(t)); out.append(norm(t))
    return out


def sintetiza(texto, key, region):
    ssml = (f"<speak version='1.0' xml:lang='es-CL'><voice name='{VOZ}'><prosody rate='{RATE}'>"
            f"{html.escape(texto)}</prosody></voice></speak>").encode()
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, headers={
        "Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "aiacciones-chile"})
    for i in range(6):
        try:
            return urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 5: time.sleep(2 ** i * 3); continue
            raise


def main():
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "pedido":
        T = textos_de(a[1:])
        json.dump({"id": a[0], "voz": VOZ, "rate": RATE, "creado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "caracteres": sum(len(t) for t in T), "textos": T}, sys.stdout, ensure_ascii=False, indent=1)
    elif cmd == "sintetizar":
        P = json.load(open(a[0], encoding="utf-8")); out = a[1]; os.makedirs(out, exist_ok=True)
        key, region = os.environ["AZURE_SPEECH_KEY"], os.environ["AZURE_SPEECH_REGION"].strip()
        n = c = fallos = 0
        for t in P["textos"]:
            p = os.path.join(out, clave(t) + ".wav")
            if os.path.exists(p): continue
            try:
                open(p, "wb").write(sintetiza(t, key, region)); n += 1; c += len(t)
            except Exception as e:
                fallos += 1; print("FALLA", type(e).__name__, getattr(e, "code", ""), t[:40])
        json.dump({"id": P["id"], "voz": VOZ, "rate": RATE, "creado": P.get("creado"), "textos": len(P["textos"]), "nuevos": n,
                   "caracteres_pedidos": c, "fallos": fallos}, open(os.path.join(out, "manifest.json"), "w"))
        print(P["id"], "textos", len(P["textos"]), "nuevos", n, "caracteres", c, "fallos", fallos)
    elif cmd == "faltan":
        F = [t for t in textos_de(a[1:]) if not os.path.exists(os.path.join(a[0], clave(t) + ".wav"))]
        for t in F: print("falta:", t[:70])
        print(len(F), "locuciones sin voz de Azure")
    elif cmd == "resumen":
        L = open(os.path.join(a[0], "uso.log")).read().split("\n") if os.path.exists(os.path.join(a[0], "uso.log")) else []
        az = sum(l.startswith("azure") for l in L); pi = sum(l.startswith("piper") for l in L)
        print(f"voz: {az} escenas con Azure {VOZ}, {pi} con Piper")
        for l in L:
            if l.startswith("piper"): print("  ", l)


if __name__ == "__main__":
    main()
