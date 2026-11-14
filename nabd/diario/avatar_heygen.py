"""Presentador IA (HeyGen, Avatar IV) en la apertura del vídeo diario de Nabd Wall Street, 2 días por semana (prueba de un mes de Daniel, 14-nov-2026).
Corre en GitHub Actions (voz-Nabd.yml), después de la voz Azure, porque el contenedor de Claude no llega a HeyGen. La clave nunca sale de los secretos.
uso: HEYGEN_API_KEY=... python3 avatar_heygen.py <video.json> <carpeta de la voz Azure del día> <fecha AAAA-MM-DD>
Monta el audio de la escena s_title igual que make_video.py (voz_frases con los wav de Azure), anima avatar/presentador.png con ese audio y deja
avatar.mp4 + avatar.json en la carpeta de la voz; make_video.py lo pega en la escena de apertura si el texto coincide. Nunca falla el flujo:
si algo va mal (día sin avatar, sin saldo, error de la API) escribe el motivo en avatar.json y sale con 0."""
import json, os, sys, time, wave, subprocess, datetime as dt, urllib.request, uuid
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)

API = "https://api.heygen.com"
DIAS = [int(x) for x in os.environ.get("AVATAR_DIAS", "1,3").split(",") if x.strip()]  # 0=lunes: martes y jueves
MIN_SALDO = float(os.environ.get("AVATAR_MIN_SALDO", "2"))   # dólares: no gastar el último saldo
MAX_S = float(os.environ.get("AVATAR_MAX_S", "45"))          # apertura más larga = más cara: se salta
IMG = os.path.join(HERE, "avatar", "presentador.png")


def api(method, path, body=None, files=None):
    key = os.environ["HEYGEN_API_KEY"]
    if files:  # subida multipart con curl (más simple que montarla a mano)
        r = subprocess.run(["curl", "-sS", "-X", "POST", API + path, "-H", f"X-Api-Key: {key}", "-F", f"file=@{files}"], capture_output=True, text=True, check=True)
        return json.loads(r.stdout)
    data = json.dumps(body).encode() if body is not None else None
    h = {"X-Api-Key": key, "Content-Type": "application/json", "Accept": "application/json"}
    if method == "POST": h["Idempotency-Key"] = str(uuid.uuid4())
    req = urllib.request.Request(API + path, data=data, method=method, headers=h)
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}") | {"http": e.code}


def saldo():
    d = (api("GET", "/v3/users/me").get("data") or {})
    w = d.get("wallet") or {}
    return w.get("remaining_balance"), w.get("currency")


def main():
    VJ = json.load(open(sys.argv[1])); out = sys.argv[2]; fecha = dt.date.fromisoformat(sys.argv[3])
    info = {"fecha": str(fecha), "texto": VJ["voz"]["s_title"], "ok": False}
    fin = lambda motivo: (info.update(motivo=motivo), json.dump(info, open(os.path.join(out, "avatar.json"), "w"), ensure_ascii=False, indent=1), print("avatar:", motivo))
    if fecha.weekday() not in DIAS: return fin(f"hoy no toca (días {DIAS}, 0=lunes)")
    if not os.environ.get("HEYGEN_API_KEY"): return fin("falta el secreto HEYGEN_API_KEY")
    os.environ["VOZ_DIR"] = out
    from comun import voz_frases
    a, sr, _, motor = voz_frases(VJ["voz"]["s_title"], out)
    if motor != "azure": return fin("faltan wav de Azure de la apertura")
    dur = len(a) / sr; info["duracion_audio"] = round(dur, 2)
    if dur > MAX_S: return fin(f"apertura de {dur:.0f} s, más de {MAX_S:.0f} s")
    s0, cur = saldo(); info["saldo_antes"] = s0
    if s0 is None or s0 < MIN_SALDO: return fin(f"saldo HeyGen {s0} {cur}, por debajo de {MIN_SALDO}")
    wav = os.path.join(out, "avatar-audio.wav")
    import numpy as np
    w = wave.open(wav, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes()); w.close()
    ia = api("POST", "/v3/assets", files=IMG).get("data", {}).get("asset_id")
    aa = api("POST", "/v3/assets", files=wav).get("data", {}).get("asset_id")
    os.remove(wav)
    if not ia or not aa: return fin("no se pudieron subir la foto o el audio")
    t0 = time.time()
    c = api("POST", "/v3/videos", {"type": "image", "image": {"type": "asset_id", "asset_id": ia}, "audio_asset_id": aa,
                                    "aspect_ratio": "1:1", "resolution": "1080p", "expressiveness": "medium", "title": f"Nabd apertura {fecha}"})
    vid = (c.get("data") or {}).get("video_id")
    if not vid: return fin(f"HeyGen rechazó el vídeo: {json.dumps(c.get('error') or c, ensure_ascii=False)[:300]}")
    while time.time() - t0 < 1500:
        time.sleep(15)
        d = api("GET", f"/v3/videos/{vid}").get("data") or {}
        if d.get("status") == "completed":
            raw = os.path.join(out, "avatar-raw.mp4"); urllib.request.urlretrieve(d["video_url"], raw)
            # más ligero para la rama voz-nabd: 720x720, sin audio (make_video.py usa la voz Azure original)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-an", "-vf", "scale=720:720", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                            "-pix_fmt", "yuv420p", os.path.join(out, "avatar.mp4")], check=True)
            os.remove(raw)
            info.update(ok=True, video_id=vid, segundos_generacion=round(time.time() - t0), duracion_video=d.get("duration"))
            info["saldo_despues"] = saldo()[0]
            return fin("listo")
        if d.get("status") == "failed": return fin(f"HeyGen falló: {d.get('failure_code')} {d.get('failure_message')}")
    return fin("HeyGen no terminó en 25 min")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # el avatar es opcional: nunca debe parar la voz del día
        print("avatar: error", repr(e)[:300])
        try:
            json.dump({"ok": False, "motivo": "error: " + repr(e)[:300].replace(os.environ.get("HEYGEN_API_KEY") or "\0", "***")},
                      open(os.path.join(sys.argv[2], "avatar.json"), "w"), ensure_ascii=False)
        except Exception: pass
