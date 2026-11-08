"""Informe semanal de estadísticas de Saudi Arabia AI Stocks (lo usa .github/workflows/estadisticas-saudi.yml).

Junta lo que se puede leer de cada red y escribe un informe en español (Markdown):
  YouTube   con OAuth: suscriptores, vistas y videos del canal, y estadísticas de cada video (Data API).
            Si el token tiene el permiso yt-analytics.readonly, también vistas, minutos vistos y
            suscriptores ganados/perdidos de la semana (YouTube Analytics API).
            Sin permisos de lectura: vistas de los últimos 15 videos por el feed RSS público.
  Buffer    X, Facebook, Instagram, TikTok y Threads: posts enviados en la semana y sus métricas
            (impresiones, me gusta, comentarios, compartidos, vistas...) si el plan de Buffer las da.
  Telegram  suscriptores del canal (el bot tiene que ser administrador).
Guarda una foto de los números (snapshot-saudi.json) para comparar con la semana anterior.

  python3 scripts/estadisticas-saudi.py <carpeta-salida>

Variables de entorno (todas opcionales; lo que falte sale como "sin acceso" en el informe):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   token de YouTube del canal
  BUFFER_API_KEY_SA, BUFFER_API_KEY_SA2               cuentas de Buffer de Arabia Saudita
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL                bot y canal de Telegram
  YT_CANAL_SA   ID del canal (UC...), para el feed público si el token no puede leer el canal
  DIAS          días que cubre el informe (por defecto 7)
Solo usa la biblioteca estándar de Python.
"""
import json, os, re, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree

CANAL_HANDLE = "@SaudiArabiaAIStocks"
CANAL_ID = os.environ.get("YT_CANAL_SA") or "UC96vi2MiZS7PND6f7zQb0ow"
DIAS = int(os.environ.get("DIAS") or 7)
AHORA = datetime.now(timezone.utc)
DESDE = AHORA - timedelta(days=DIAS)
RED = {"twitter": "X", "x": "X", "facebook": "Facebook", "instagram": "Instagram",
       "tiktok": "TikTok", "threads": "Threads", "linkedin": "LinkedIn", "youtube": "YouTube"}
METRICAS = [("impressions", "Impresiones"), ("reach", "Alcance"), ("views", "Vistas"),
            ("likes", "Me gusta"), ("reactions", "Reacciones"), ("comments", "Comentarios"),
            ("shares", "Compartidos"), ("reposts", "Reposts"), ("saves", "Guardados"),
            ("clicks", "Clics"), ("follows", "Seguidores nuevos")]


class Falla(Exception):
    pass


def pedir(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise Falla(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    except urllib.error.URLError as e:
        raise Falla(f"sin conexión: {e.reason}")


def pedir_json(url, data=None, headers=None):
    return json.loads(pedir(url, data, headers))


def num(n):
    return "—" if n is None else f"{int(round(n)):,}".replace(",", ".")


def delta(ahora, antes):
    if ahora is None or antes is None:
        return ""
    d = ahora - antes
    return f" ({'+' if d >= 0 else ''}{num(d)})"


# ---------- YouTube ----------

def yt_token():
    cid, sec, ref = (os.environ.get(k, "").strip() for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"))
    if not (cid and sec and ref):
        raise Falla("faltan las credenciales de YouTube")
    datos = urllib.parse.urlencode({"client_id": cid, "client_secret": sec, "refresh_token": ref,
                                    "grant_type": "refresh_token"}).encode()
    r = pedir_json("https://oauth2.googleapis.com/token", datos,
                   {"Content-Type": "application/x-www-form-urlencoded"})
    return r["access_token"], set(r.get("scope", "").split())


def duracion(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return ((d * 24 + h) * 60 + mi) * 60 + s


def youtube_api(t):
    api = "https://www.googleapis.com/youtube/v3"
    cab = {"Authorization": f"Bearer {t}"}
    canal = pedir_json(f"{api}/channels?part=statistics,contentDetails,snippet&mine=true", headers=cab)["items"][0]
    st = canal["statistics"]
    subidas = canal["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, pagina = [], ""
    while True:
        r = pedir_json(f"{api}/playlistItems?part=contentDetails&maxResults=50&playlistId={subidas}"
                       + (f"&pageToken={pagina}" if pagina else ""), headers=cab)
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        pagina = r.get("nextPageToken")
        if not pagina:
            break
    videos = []
    for i in range(0, len(ids), 50):
        r = pedir_json(f"{api}/videos?part=snippet,statistics,contentDetails,status&id={','.join(ids[i:i+50])}",
                       headers=cab)
        for v in r.get("items", []):
            s = v.get("statistics", {})
            videos.append({"id": v["id"], "titulo": v["snippet"]["title"],
                           "fecha": v["snippet"]["publishedAt"],
                           "short": duracion(v["contentDetails"].get("duration")) <= 180,
                           "privacidad": v.get("status", {}).get("privacyStatus"),
                           "vistas": int(s.get("viewCount", 0)), "megusta": int(s.get("likeCount", 0)),
                           "comentarios": int(s.get("commentCount", 0))})
    return {"fuente": "api", "canal_id": canal["id"], "nombre": canal["snippet"]["title"],
            "suscriptores": None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount", 0)),
            "vistas": int(st.get("viewCount", 0)), "num_videos": int(st.get("videoCount", 0)), "videos": videos}


def youtube_analytics(t, canal_id):
    fin = (AHORA - timedelta(days=1)).date()
    ini = fin - timedelta(days=DIAS - 1)
    base = "https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode({
        "ids": "channel==MINE", "startDate": ini.isoformat(), "endDate": fin.isoformat()})
    cab = {"Authorization": f"Bearer {t}"}
    met = "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,shares,comments"
    r = pedir_json(base + "&metrics=" + met, headers=cab)
    fila = (r.get("rows") or [[0] * len(met.split(","))])[0]
    res = dict(zip(met.split(","), fila), desde=ini.isoformat(), hasta=fin.isoformat())
    try:
        r = pedir_json(base + "&dimensions=insightTrafficSourceType&metrics=views&sort=-views", headers=cab)
        res["trafico"] = r.get("rows") or []
    except Falla:
        res["trafico"] = []
    return res


def youtube_publico():
    xml = pedir(f"https://www.youtube.com/feeds/videos.xml?channel_id={CANAL_ID}")
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
          "m": "http://search.yahoo.com/mrss/"}
    raiz = ElementTree.fromstring(xml)
    videos = []
    for e in raiz.findall("a:entry", ns):
        est = e.find("m:group/m:community/m:statistics", ns)
        cal = e.find("m:group/m:community/m:starRating", ns)
        enlace = e.find("a:link", ns).get("href", "")
        videos.append({"id": e.find("yt:videoId", ns).text, "titulo": e.find("a:title", ns).text,
                       "fecha": e.find("a:published", ns).text, "short": "/shorts/" in enlace,
                       "vistas": int(est.get("views", 0)) if est is not None else 0,
                       "megusta": int(cal.get("count", 0)) if cal is not None else None, "comentarios": None})
    subs = None
    try:
        html = pedir(f"https://www.youtube.com/{CANAL_HANDLE}", headers={
            "User-Agent": "Mozilla/5.0", "Accept-Language": "en-US"}).decode("utf-8", "replace")
        m = re.search(r'"content":"([\d.,]+)([KM]?) subscribers?"', html)
        if m:
            subs = float(m.group(1).replace(",", "")) * {"": 1, "K": 1e3, "M": 1e6}[m.group(2)]
    except Falla:
        pass
    return {"fuente": "publico", "canal_id": CANAL_ID, "nombre": "Saudi Arabia AI Stocks",
            "suscriptores": subs, "vistas": None, "num_videos": None, "videos": videos}


def youtube():
    notas, permisos, t = [], set(), None
    try:
        t, permisos = yt_token()
    except Falla as e:
        notas.append(f"No se pudo pedir el token de YouTube ({e}).")
    lectura = permisos & {"https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.readonly",
                          "https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtubepartner"}
    datos = None
    if t and lectura:
        try:
            datos = youtube_api(t)
        except (Falla, KeyError, IndexError) as e:
            notas.append(f"La API de YouTube falló ({e}); uso el feed público.")
    elif t:
        notas.append("El token de YouTube solo puede subir videos (falta youtube.readonly): uso el feed público, "
                     "que muestra solo los últimos 15 videos.")
    if datos is None:
        try:
            datos = youtube_publico()
        except (Falla, ElementTree.ParseError) as e:
            notas.append(f"Tampoco se pudo leer el feed público ({e}).")
            datos = {"fuente": "nada", "videos": [], "suscriptores": None, "vistas": None, "num_videos": None}
    datos["analytics"] = None
    if t and "https://www.googleapis.com/auth/yt-analytics.readonly" in permisos:
        try:
            datos["analytics"] = youtube_analytics(t, datos.get("canal_id"))
        except Falla as e:
            notas.append(f"YouTube Analytics falló ({e}).")
    elif t:
        notas.append("Sin permiso de YouTube Analytics (yt-analytics.readonly): no hay minutos vistos ni "
                     "suscriptores ganados por semana.")
    datos["permisos"] = sorted(p.rsplit("/", 1)[-1] for p in permisos)
    datos["notas"] = notas
    return datos


# ---------- Buffer ----------

def gql(clave, consulta):
    r = pedir_json("https://api.buffer.com", json.dumps({"query": consulta}).encode(),
                   {"Content-Type": "application/json", "Authorization": f"Bearer {clave}"})
    if r.get("errors"):
        raise Falla(json.dumps(r["errors"], ensure_ascii=False)[:300])
    return r["data"]


def buffer():
    redes, notas = {}, []
    claves = [(k, os.environ.get(k, "").strip()) for k in ("BUFFER_API_KEY_SA", "BUFFER_API_KEY_SA2")]
    if not any(c for _, c in claves):
        notas.append("No hay claves de Buffer de Arabia Saudita.")
    rango = json.dumps({"start": DESDE.isoformat(timespec="seconds").replace("+00:00", "Z"),
                        "end": AHORA.isoformat(timespec="seconds").replace("+00:00", "Z")})
    rango = re.sub(r'"(\w+)":', r"\1:", rango)
    for nombre, clave in claves:
        if not clave:
            continue
        try:
            orgs = gql(clave, "query { account { organizations { id } } }")["account"]["organizations"]
            for org in orgs:
                oid = json.dumps(org["id"])
                chs = gql(clave, "query { channels(input: {organizationId: %s}) { id name service isDisconnected } }"
                          % oid)["channels"]
                for ch in chs:
                    red = RED.get(ch["service"], ch["service"])
                    r = redes.setdefault(red, {"cuentas": [], "posts": [], "totales": {}, "sin_metricas": 0,
                                               "desconectado": False})
                    r["cuentas"].append(ch["name"])
                    r["desconectado"] |= ch["isDisconnected"]
                    try:
                        posts_canal(clave, oid, ch["id"], rango, r, True)
                    except Falla as e:
                        try:  # Si el plan no da métricas, al menos contar los posts
                            posts_canal(clave, oid, ch["id"], rango, r, False)
                            notas.append(f"Buffer ({red}): sin métricas ({e}).")
                        except Falla as e2:
                            notas.append(f"Buffer ({red}): {e2}")
        except Falla as e:
            notas.append(f"Buffer ({nombre}): {e}")
    return {"redes": redes, "notas": notas}


def posts_canal(clave, oid, canal, rango, r, con_metricas):
    """Suma a r los posts enviados en la semana por un canal de Buffer (con sus métricas si se piden)."""
    campos = "id text sentAt dueAt externalLink" + (" metrics { type value }" if con_metricas else "")
    despues, posts = None, []
    while True:
        q = ("query { posts(first: 50%s, input: {organizationId: %s, filter: {channelIds: [%s], "
             "status: [sent], dueAt: %s}}) { edges { node { %s } } pageInfo { hasNextPage endCursor } } }") % (
            f", after: {json.dumps(despues)}" if despues else "", oid, json.dumps(canal), rango, campos)
        p = gql(clave, q)["posts"]
        posts += [e["node"] for e in p["edges"]]
        if not p["pageInfo"]["hasNextPage"]:
            break
        despues = p["pageInfo"]["endCursor"]
    for n in posts:
        met = {m["type"]: m["value"] for m in (n.get("metrics") or [])}
        if not met:
            r["sin_metricas"] += 1
        for k, v in met.items():
            if k != "engagementRate":
                r["totales"][k] = r["totales"].get(k, 0) + v
        r["posts"].append({"texto": (n["text"] or "").split("\n")[0][:70],
                           "fecha": n.get("sentAt") or n.get("dueAt"),
                           "enlace": n.get("externalLink"), "metricas": met})


# ---------- Telegram ----------

def telegram():
    tok, canal = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(), os.environ.get("TELEGRAM_CHANNEL", "").strip()
    if not (tok and canal):
        return {"suscriptores": None, "nota": "Faltan el bot o el canal de Telegram."}
    try:
        r = pedir_json(f"https://api.telegram.org/bot{tok}/getChatMemberCount?" + urllib.parse.urlencode({"chat_id": canal}))
        return {"suscriptores": r["result"], "canal": canal, "nota": ""}
    except Falla as e:
        return {"suscriptores": None, "nota": f"Telegram: {e}"}


# ---------- Informe ----------

def informe(yt, bf, tg, antes):
    fecha = AHORA.date().isoformat()
    a_yt = antes.get("youtube", {})
    vistas_antes = a_yt.get("videos", {})
    L = [f"# Informe semanal · Saudi Arabia AI Stocks · {fecha}", "",
         f"Semana del {DESDE.date().isoformat()} al {fecha} (UTC)."
         + (f" Comparado con el informe del {antes['fecha']}." if antes.get("fecha") else
            " Es el primer informe: las diferencias aparecen desde la próxima semana."), ""]

    # Resumen
    an = yt.get("analytics")
    L += ["## Resumen", "", "| Red | Seguidores | Esta semana |", "|---|---|---|"]
    vistas_sem = an["views"] if an else (
        sum(v["vistas"] - vistas_antes.get(v["id"], 0) for v in yt["videos"]) if vistas_antes else None)
    nuevos = [v for v in yt["videos"] if v["fecha"] >= DESDE.isoformat()[:19]]
    L.append(f"| YouTube | {num(yt['suscriptores'])}{delta(yt['suscriptores'], a_yt.get('suscriptores'))} | "
             f"{len(nuevos)} videos nuevos · {num(vistas_sem)} vistas |")
    for red, r in sorted(bf["redes"].items()):
        t = r["totales"]
        extra = " · ".join(f"{num(t[k])} {e.lower()}" for k, e in METRICAS if t.get(k))
        L.append(f"| {red} | — | {len(r['posts'])} posts" + (f" · {extra}" if extra else "") + " |")
    L.append(f"| Telegram | {num(tg['suscriptores'])}{delta(tg['suscriptores'], antes.get('telegram'))} | — |")
    L.append("")

    # YouTube
    L += ["## YouTube", ""]
    if yt.get("vistas") is not None:
        L.append(f"- Canal: {num(yt['suscriptores'])} suscriptores{delta(yt['suscriptores'], a_yt.get('suscriptores'))}, "
                 f"{num(yt['vistas'])} vistas en total{delta(yt['vistas'], a_yt.get('vistas'))}, {num(yt['num_videos'])} videos.")
    elif yt.get("suscriptores") is not None:
        L.append(f"- Canal: {num(yt['suscriptores'])} suscriptores (leído de la página pública).")
    if an:
        L.append(f"- Del {an['desde']} al {an['hasta']} (YouTube Analytics): {num(an['views'])} vistas, "
                 f"{num(an['estimatedMinutesWatched'])} minutos vistos, {num(an['averageViewDuration'])} s de "
                 f"duración media, +{num(an['subscribersGained'])} / −{num(an['subscribersLost'])} suscriptores, "
                 f"{num(an['likes'])} me gusta, {num(an['comments'])} comentarios, {num(an['shares'])} compartidos.")
        if an.get("trafico"):
            L.append("- De dónde vienen las vistas: " + ", ".join(f"{k} {num(v)}" for k, v in an["trafico"][:6]) + ".")
    for tipo, es_short in (("Videos largos", False), ("Shorts", True)):
        vs = sorted((v for v in yt["videos"] if v["short"] == es_short), key=lambda v: -v["vistas"])
        if not vs:
            continue
        L += ["", f"**{tipo}: los 10 con más vistas** ({len(vs)} en total, {num(sum(v['vistas'] for v in vs))} vistas)", "",
              "| Video | Publicado | Vistas | Semana | Me gusta | Coment. |", "|---|---|---|---|---|---|"]
        for v in vs[:10]:
            sem = delta(v["vistas"], vistas_antes.get(v["id"])).strip(" ()") or ("nuevo" if v in nuevos else "—")
            titulo = v["titulo"].replace("|", "/")[:60]
            L.append(f"| [{titulo}](https://youtu.be/{v['id']}) | {v['fecha'][:10]} | {num(v['vistas'])} | {sem} | "
                     f"{num(v['megusta'])} | {num(v['comentarios'])} |")
    if yt["notas"]:
        L += [""] + [f"> {n}" for n in yt["notas"]]
    L.append("")

    # Buffer
    L += ["## X, Facebook, Instagram, TikTok y Threads (vía Buffer)", ""]
    if not bf["redes"]:
        L.append("Sin datos de Buffer.")
    for red, r in sorted(bf["redes"].items()):
        cuentas = ", ".join(sorted(set(r["cuentas"])))
        L.append(f"**{red}** ({cuentas}){' — DESCONECTADO en Buffer' if r['desconectado'] else ''}: "
                 f"{len(r['posts'])} posts enviados en la semana.")
        if r["posts"] and (r["sin_metricas"] == len(r["posts"])
                           or not any(r["totales"].get(k) for k, _ in METRICAS)):
            L.append("Buffer no devuelve métricas de estos posts (puede que el plan gratis no las incluya, "
                     "o que todavía no las haya recogido) o están todas en 0.")
        elif r["posts"]:
            cols = [(k, e) for k, e in METRICAS if r["totales"].get(k)]
            L += ["", "| Post | Fecha | " + " | ".join(e for _, e in cols) + " |",
                  "|---|---|" + "---|" * len(cols)]
            for p in sorted(r["posts"], key=lambda p: -sum(p["metricas"].get(k, 0) for k, _ in cols))[:8]:
                txt = p["texto"].replace("|", "/")
                txt = f"[{txt}]({p['enlace']})" if p.get("enlace") else txt
                L.append(f"| {txt} | {(p['fecha'] or '')[:10]} | "
                         + " | ".join(num(p["metricas"].get(k)) for k, _ in cols) + " |")
        L.append("")
    if bf["notas"]:
        L += [f"> {n}" for n in bf["notas"]] + [""]

    # Telegram
    L += ["## Telegram", ""]
    if tg["suscriptores"] is not None:
        L.append(f"- {tg['canal']}: {num(tg['suscriptores'])} suscriptores{delta(tg['suscriptores'], antes.get('telegram'))}.")
    if tg["nota"]:
        L.append(f"> {tg['nota']}")
    L += ["", "---", f"Fuente de YouTube: {yt.get('fuente')} · permisos del token: "
          f"{', '.join(yt.get('permisos') or []) or 'ninguno'}"]
    return "\n".join(L) + "\n"


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else "informes-saudi"
    os.makedirs(salida, exist_ok=True)
    foto = os.path.join(salida, "snapshot-saudi.json")
    antes = json.load(open(foto, encoding="utf-8")) if os.path.exists(foto) else {}
    yt, bf, tg = youtube(), buffer(), telegram()
    texto = informe(yt, bf, tg, antes)
    nombre = os.path.join(salida, f"informe-{AHORA.date().isoformat()}-saudi.md")
    open(nombre, "w", encoding="utf-8").write(texto)
    json.dump({"fecha": AHORA.date().isoformat(),
               "youtube": {"suscriptores": yt["suscriptores"], "vistas": yt["vistas"],
                           "videos": {v["id"]: v["vistas"] for v in yt["videos"]}},
               "telegram": tg["suscriptores"],
               "buffer": {red: {"posts": len(r["posts"]), **r["totales"]} for red, r in bf["redes"].items()}},
              open(foto, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(texto)
    print(f"Informe: {nombre}", file=sys.stderr)


if __name__ == "__main__":
    main()
