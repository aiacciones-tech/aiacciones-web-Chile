"""Directos en momentos clave de Saudi Arabia AI Stocks (Daniel, 24-nov-2026): Fed, OPEP+, presupuesto saudí, resultados anuales grandes.

YouTube no deja crear Estrenos por la API, así que cada "directo" es una emisión en directo real: el vídeo ya preparado
(saudi/directos/, 8-12 min, con cuenta atrás al inicio) se emite por RTMP desde GitHub Actions a la hora fijada.
La emisión se crea antes (página "Próximamente", chat en vivo, recordatorios) y al terminar queda guardada en el canal.

Cada directo es una carpeta cola-sa/directo-<base>/ de la rama youtube-cola con:
  video.mp4, miniatura.png (opcional), posts (post-x.txt, post-facebook.txt, post-threads.txt, post-telegram.txt con {youtube})
  directo.json: {"title", "description", "tags", "inicio": "2026-12-09T20:00:00Z" (UTC), "privacy": "public"}
No lleva meta.json, así que youtube.py no la sube como vídeo normal.

  python3 scripts/directo-saudi.py verificar          # permisos del token y si el canal puede emitir en directo
  python3 scripts/directo-saudi.py programar cola-sa  # crea las emisiones pendientes (escribe resultado.json y estado.json)
  python3 scripts/directo-saudi.py siguiente cola-sa  # imprime la carpeta del próximo directo que empieza en < VENTANA_MIN
  python3 scripts/directo-saudi.py emitir <carpeta>   # espera a la hora y emite (ffmpeg); termina la emisión al acabar

estado.json: {"broadcast", "stream", "estado": programado|emitiendo|emitido|error, ...}. resultado.json usa el mismo formato que youtube.py
(videoId = id de la emisión), para que buffer.py y telegram.py anuncien el directo con su enlace en cuanto está programado.
La clave de emisión nunca se guarda en el repo: se pide a la API al emitir y se oculta en el log.
Credenciales: las de youtube.py (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN). Hace falta el permiso youtube o youtube.force-ssl."""
import json, os, subprocess, sys, time, urllib.parse
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import youtube as yt
from youtube import API, pedir

VENTANA_MIN = int(os.environ.get("VENTANA_MIN", "330"))  # un job de Actions dura como mucho 6 h: solo se espera a directos cercanos
PERMISOS = ("https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl")
ahora = lambda: datetime.now(timezone.utc)
iso = lambda d: d.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def token_y_permisos():
    datos = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                    "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    _, _, c = pedir("https://oauth2.googleapis.com/token", datos, {"Content-Type": "application/x-www-form-urlencoded"})
    r = json.loads(c)
    return r["access_token"], set(r.get("scope", "").split())


def api(t, metodo, ruta, cuerpo=None, **q):
    url = f"{API}/youtube/v3/{ruta}?" + urllib.parse.urlencode(q)
    h = {"Authorization": f"Bearer {t}"}
    data = None
    if cuerpo is not None:
        data = json.dumps(cuerpo).encode(); h["Content-Type"] = "application/json; charset=UTF-8"
    _, _, r = pedir(url, data, h, metodo)
    return json.loads(r) if r else {}


def leer(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def guardar(c, n, d):
    json.dump(d, open(os.path.join(c, n), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def verificar():
    t, perm = token_y_permisos()
    print("permisos del token:", " ".join(sorted(perm)) or "(no los dice)")
    if not perm & set(PERMISOS):
        sys.exit("FALTA PERMISO: el token no tiene youtube ni youtube.force-ssl; hay que volver a autorizar la cuenta para crear directos.")
    ch = api(t, "GET", "channels", part="snippet,status", mine="true")["items"][0]
    print(f"canal: {ch['snippet']['title']} ({ch['id']})")
    # No hay un campo que diga si el canal puede emitir: se prueba creando una emisión privada de prueba y borrándola.
    try:
        b = api(t, "POST", "liveBroadcasts", {"snippet": {"title": "prueba de permisos (se borra sola)",
                "scheduledStartTime": iso(ahora() + timedelta(days=7))},
                "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}, "contentDetails": {}}, part="snippet,status,contentDetails")
    except SystemExit as e:
        msg = str(e)
        if "liveStreamingNotEnabled" in msg or "insufficientLivePermissions" in msg:
            sys.exit("El token sirve, pero el canal todavía NO tiene los directos activados (YouTube Studio > Crear > Emitir en directo; tarda hasta 24 h).\n" + msg)
        raise
    api(t, "DELETE", "liveBroadcasts", id=b["id"])
    print("OK: el canal puede crear directos (emisión de prueba creada y borrada).")


def programar_uno(t, c):
    d = leer(c, "directo.json")
    inicio = datetime.fromisoformat(d["inicio"].replace("Z", "+00:00"))
    if inicio < ahora() + timedelta(minutes=10):
        guardar(c, "estado.json", {"estado": "error", "motivo": f"inicio {d['inicio']} ya pasó o es en menos de 10 min"}); print(c, "inicio pasado"); return
    desc = yt.enlazar(d.get("description", ""), os.path.dirname(c))[:5000]
    b = api(t, "POST", "liveBroadcasts", {
        "snippet": {"title": d["title"][:100], "description": desc, "scheduledStartTime": iso(inicio)},
        "status": {"privacyStatus": d.get("privacy", "public"), "selfDeclaredMadeForKids": False},
        "contentDetails": {"enableAutoStart": True, "enableAutoStop": True, "enableDvr": True, "recordFromStart": True,
                           "latencyPreference": "normal", "monitorStream": {"enableMonitorStream": False}}},
        part="snippet,status,contentDetails")
    s = api(t, "POST", "liveStreams", {"snippet": {"title": f"saudi {os.path.basename(c)}"},
            "cdn": {"ingestionType": "rtmp", "resolution": "1080p", "frameRate": "30fps"},
            "contentDetails": {"isReusable": False}}, part="snippet,cdn,contentDetails")
    api(t, "POST", "liveBroadcasts/bind", None, id=b["id"], streamId=s["id"], part="id,contentDetails")
    vid = b["id"]
    # Etiquetas, categoría e idioma: van en videos.update (liveBroadcasts no los acepta).
    try:
        v = api(t, "GET", "videos", part="snippet", id=vid)["items"][0]["snippet"]
        v.update({"tags": d.get("tags", []), "categoryId": str(d.get("categoryId", "25")), "defaultLanguage": "ar", "defaultAudioLanguage": "ar"})
        api(t, "PUT", "videos", {"id": vid, "snippet": v}, part="snippet")
    except SystemExit as e:
        print("aviso: no se pudieron poner etiquetas/idioma:", str(e)[:200])
    res = {"videoId": vid, "url": f"https://www.youtube.com/watch?v={vid}", "privacy": b["status"]["privacyStatus"],
           "subido": iso(ahora()), "directo": True, "inicio": iso(inicio), "miniatura": "no"}
    mini = os.path.join(c, "miniatura.png")
    if os.path.exists(mini): res["miniatura"] = yt.poner_miniatura(t, vid, mini)
    guardar(c, "resultado.json", res)
    guardar(c, "estado.json", {"estado": "programado", "broadcast": vid, "stream": s["id"], "inicio": iso(inicio), "programado": iso(ahora())})
    print(f"{os.path.basename(c)}: directo programado {res['url']} para {iso(inicio)} (miniatura {res['miniatura']})")


def carpetas(base):
    return sorted(os.path.join(base, x) for x in os.listdir(base) if x.startswith("directo-") and os.path.exists(os.path.join(base, x, "directo.json")))


def programar(base):
    pend = [c for c in carpetas(base) if not leer(c, "estado.json")]
    if not pend: print("No hay directos por programar."); return
    t, _ = token_y_permisos()
    for c in pend: programar_uno(t, c)


def siguiente(base):
    lim = ahora() + timedelta(minutes=VENTANA_MIN); mejor = None
    for c in carpetas(base):
        e = leer(c, "estado.json") or {}
        if e.get("estado") != "programado": continue
        ini = datetime.fromisoformat(e["inicio"].replace("Z", "+00:00"))
        if ini <= lim and ini > ahora() - timedelta(minutes=30) and (not mejor or ini < mejor[0]): mejor = (ini, c)
    print(mejor[1] if mejor else "")


def emitir(c):
    """Llamar después de marcar estado "emitiendo" y subirlo (así otro job no la emite dos veces)."""
    e = leer(c, "estado.json"); ini = datetime.fromisoformat(e["inicio"].replace("Z", "+00:00"))
    video = os.path.join(c, "video.mp4")
    # El vídeo empieza con 60 s de cuenta atrás: se arranca al minuto en punto del inicio anunciado.
    espera = (ini - ahora()).total_seconds() - 45  # YouTube tarda ~15-30 s en pasar a "en directo" tras recibir señal
    if espera > 0: print(f"esperando {espera / 60:.1f} min hasta {e['inicio']}"); sys.stdout.flush(); time.sleep(espera)
    t, _ = token_y_permisos()
    s = api(t, "GET", "liveStreams", part="cdn", id=e["stream"])["items"][0]["cdn"]["ingestionInfo"]
    print(f"::add-mask::{s['streamName']}"); sys.stdout.flush()
    destino = f"{s['ingestionAddress']}/{s['streamName']}"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-re", "-i", video, "-c:v", "libx264", "-preset", "veryfast",
           "-b:v", "4500k", "-maxrate", "4500k", "-bufsize", "9000k", "-pix_fmt", "yuv420p", "-r", "30", "-g", "60", "-keyint_min", "60",
           "-sc_threshold", "0", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-f", "flv", destino]
    e.update({"emision_inicio": iso(ahora())}); guardar(c, "estado.json", e)
    r = subprocess.run(cmd).returncode
    time.sleep(20)
    t, _ = token_y_permisos()
    b = api(t, "GET", "liveBroadcasts", part="status", id=e["broadcast"])["items"][0]["status"]
    if b.get("lifeCycleStatus") in ("live", "liveStarting"):
        try: api(t, "POST", "liveBroadcasts/transition", None, broadcastStatus="complete", id=e["broadcast"], part="status")
        except SystemExit as x: print("aviso al cerrar la emisión:", str(x)[:300])
        b = api(t, "GET", "liveBroadcasts", part="status", id=e["broadcast"])["items"][0]["status"]
    e.update({"estado": "emitido" if r == 0 else "error", "ffmpeg": r, "emision_fin": iso(ahora()), "youtube": b.get("lifeCycleStatus")})
    guardar(c, "estado.json", e)
    print(f"{os.path.basename(c)}: ffmpeg {r}, YouTube {b.get('lifeCycleStatus')}")
    if r != 0: sys.exit(1)


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "verificar"
    {"verificar": lambda: verificar(), "programar": lambda: programar(sys.argv[2]),
     "siguiente": lambda: siguiente(sys.argv[2]), "emitir": lambda: emitir(sys.argv[2])}[m]()
