"""Sube a YouTube los videos en cola/ de la rama youtube-cola (los usa .github/workflows/youtube.yml).

Cada video es una carpeta cola/<slug>/ con video.mp4, miniatura.png (opcional) y meta.json:
  {"title": "...", "description": "...", "tags": [...], "privacy": "private"}
Al subir escribe cola/<slug>/resultado.json con el ID y el enlace, y no vuelve a subir esa carpeta.

  python3 scripts/youtube.py verificar   # solo prueba las credenciales y muestra el canal
  python3 scripts/youtube.py subir cola  # sube lo pendiente

Credenciales (secretos del repo): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
Solo usa la biblioteca estándar de Python.
"""
import json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://www.googleapis.com"


def pedir(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")
        sys.exit(f"Error HTTP {e.code} en {url.split('?')[0]}: {cuerpo[:800]}")


def token():
    datos = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    _, _, cuerpo = pedir("https://oauth2.googleapis.com/token", datos,
                         {"Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(cuerpo)["access_token"]


def verificar():
    t = token()
    _, _, cuerpo = pedir(f"{API}/youtube/v3/channels?part=snippet,statistics&mine=true",
                         headers={"Authorization": f"Bearer {t}"})
    items = json.loads(cuerpo).get("items", [])
    if not items:
        sys.exit("Las credenciales funcionan, pero esa cuenta no tiene canal de YouTube.")
    c = items[0]
    print(f"OK: canal \"{c['snippet']['title']}\" ({c['id']}), "
          f"{c['statistics'].get('videoCount', '?')} videos.")


def subir_uno(t, carpeta):
    meta = json.load(open(os.path.join(carpeta, "meta.json"), encoding="utf-8"))
    video = os.path.join(carpeta, "video.mp4")
    cuerpo = json.dumps({
        "snippet": {
            "title": meta["title"][:100],
            "description": meta.get("description", "")[:5000],
            "tags": meta.get("tags", []),
            "categoryId": str(meta.get("categoryId", "27")),
            "defaultLanguage": "es", "defaultAudioLanguage": "es",
        },
        "status": {"privacyStatus": meta.get("privacy", "private"),
                   "selfDeclaredMadeForKids": False},
    }).encode()
    _, cab, _ = pedir(f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                      cuerpo, {"Authorization": f"Bearer {t}",
                               "Content-Type": "application/json; charset=UTF-8",
                               "X-Upload-Content-Type": "video/mp4",
                               "X-Upload-Content-Length": str(os.path.getsize(video))})
    destino = cab.get("Location") or cab.get("location")
    with open(video, "rb") as f:
        _, _, r = pedir(destino, f.read(), {"Content-Type": "video/mp4"}, "PUT")
    vid = json.loads(r)["id"]
    res = {"videoId": vid, "url": f"https://www.youtube.com/watch?v={vid}",
           "privacy": meta.get("privacy", "private"),
           "subido": datetime.now(timezone.utc).isoformat(timespec="seconds"), "miniatura": "no"}
    mini = os.path.join(carpeta, "miniatura.png")
    if os.path.exists(mini):
        req = urllib.request.Request(f"{API}/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                     open(mini, "rb").read(),
                                     {"Authorization": f"Bearer {t}", "Content-Type": "image/png"})
        try:
            urllib.request.urlopen(req, timeout=120)
            res["miniatura"] = "si"
        except urllib.error.HTTPError as e:
            # Miniaturas propias requieren canal verificado; el video queda subido igual.
            res["miniatura"] = f"error {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
    json.dump(res, open(os.path.join(carpeta, "resultado.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{os.path.basename(carpeta)}: {res['url']} ({res['privacy']}, miniatura {res['miniatura']})")


def subir(base):
    pendientes = sorted(os.path.join(base, d) for d in os.listdir(base)
                        if os.path.exists(os.path.join(base, d, "meta.json"))
                        and not os.path.exists(os.path.join(base, d, "resultado.json")))
    if not pendientes:
        print("No hay videos pendientes.")
        return
    t = token()
    for c in pendientes:
        subir_uno(t, c)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "verificar"
    verificar() if modo == "verificar" else subir(sys.argv[2] if len(sys.argv) > 2 else "cola")
