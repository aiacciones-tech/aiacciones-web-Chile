"""Sección "Impacto de las mejoras" del informe semanal de Saudi Arabia AI Stocks (la usa scripts/estadisticas-saudi.py).

Mide, semana a semana y contra una línea base de antes del 24-nov-2026, las cuatro mejoras de crecimiento:
  1. Pruebas A/B de miniatura y título: lee cola-sa/*/ab-estado.json de la rama youtube-cola (carpeta AB_DIR, la trae
     el workflow) y además detecta cambios de título comparando con la semana anterior. Con permiso de Analytics,
     CTR de miniaturas por vídeo (YouTube Reporting API, informe channel_reach_basic_a1).
  2. Playlists por empresa y sector: lista del canal (Data API) y, con Analytics, vistas y minutos desde cada playlist.
  3. Vídeos evergreen de búsqueda: los del registro saudi/crecimiento/mejoras-saudi.json (tipo "evergreen"), sus vistas
     y, con Analytics, cuántas vienen de la búsqueda de YouTube y con qué términos.
  4. Directos y estrenos: se detectan solos (liveStreamingDetails) y se miden sus vistas y suscriptores ganados.
Todo lo que pide YouTube Analytics necesita el token con yt-analytics.readonly (YT_SAUDI_STATS_REFRESH_TOKEN);
sin él la sección sale igual con lo que da la Data API y avisa de lo que falta.
"""
import csv, io, json, os, glob, urllib.parse
from datetime import date, datetime, timedelta

INICIO = date(2026, 11, 24)               # día en que empiezan las mejoras
BASE_INI, BASE_FIN = date(2026, 11, 3), date(2026, 11, 23)   # línea base: 3 semanas antes (el canal empezó el 3-nov)
BASE_SEMANAS = ((BASE_FIN - BASE_INI).days + 1) / 7
# Línea base sin Analytics: el informe del 20-nov-2026 (última semana completa antes de las mejoras)
BASE_PUBLICA = {"fecha": "2026-11-20", "suscriptores": 6, "vistas_semana": 774}
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, "saudi", "crecimiento", "mejoras-saudi.json")
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
REPORTING = "https://youtubereporting.googleapis.com/v1"
TIPO_CTR = "channel_reach_basic_a1"
BUSQUEDA = {"YT_SEARCH"}
PLAYLIST = {"PLAYLIST", "YT_PLAYLIST_PAGE"}


# ---------- lectura ----------

def registro():
    try:
        return json.load(open(REGISTRO, encoding="utf-8")).get("mejoras", [])
    except (OSError, ValueError):
        return []


def pruebas_ab():
    """Estados de las pruebas A/B (cola-sa/<slug>/ab-estado.json de la rama youtube-cola)."""
    d = os.environ.get("AB_DIR", "").strip()
    res = []
    for f in sorted(glob.glob(os.path.join(d, "*", "ab-estado.json"))) if d else []:
        try:
            e = json.load(open(f, encoding="utf-8"))
            e.setdefault("slug", os.path.basename(os.path.dirname(f)))
            res.append(e)
        except (OSError, ValueError):
            pass
    return res


def playlists(pedir_json, cab):
    res, pagina = [], ""
    while True:
        r = pedir_json("https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults=50"
                       + (f"&pageToken={pagina}" if pagina else ""), headers=cab)
        res += [{"id": p["id"], "titulo": p["snippet"]["title"], "videos": p["contentDetails"]["itemCount"],
                 "creada": p["snippet"]["publishedAt"][:10]} for p in r.get("items", [])]
        pagina = r.get("nextPageToken")
        if not pagina:
            return res


def an(pedir_json, cab, ini, fin, metricas, **extra):
    q = {"ids": "channel==MINE", "startDate": ini.isoformat(), "endDate": fin.isoformat(), "metrics": metricas}
    q.update({k: v for k, v in extra.items() if v})
    r = pedir_json(ANALYTICS + "?" + urllib.parse.urlencode(q), headers=cab)
    cols = [c["name"] for c in r.get("columnHeaders", [])]
    return [dict(zip(cols, f)) for f in r.get("rows") or []]


def periodo(pedir_json, cab, ini, fin, videos=None):
    """Totales de un período (todo el canal, o solo esos vídeos) con el tráfico por fuente."""
    filtro = ("video==" + ",".join(videos)) if videos else None
    met = "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost"
    fila = (an(pedir_json, cab, ini, fin, met, filters=filtro) or [{}])[0]
    res = {k: fila.get(k, 0) for k in met.split(",")}
    res["trafico"] = {f["insightTrafficSourceType"]: f["views"] for f in
                      an(pedir_json, cab, ini, fin, "views", dimensions="insightTrafficSourceType", filters=filtro)}
    res["busqueda"] = sum(v for k, v in res["trafico"].items() if k in BUSQUEDA)
    res["desde_playlist"] = sum(v for k, v in res["trafico"].items() if k in PLAYLIST)
    return res


def por_video(pedir_json, cab, ini, fin, ids):
    if not ids:
        return {}
    filas = an(pedir_json, cab, ini, fin, "views,estimatedMinutesWatched,averageViewPercentage,subscribersGained",
               dimensions="video", filters="video==" + ",".join(ids[:200]), sort="-views", maxResults=200)
    return {f["video"]: f for f in filas}


def terminos_busqueda(pedir_json, cab, ini, fin, videos=None):
    filtro = "insightTrafficSourceType==YT_SEARCH" + (";video==" + ",".join(videos) if videos else "")
    return [(f["insightTrafficSourceDetail"], f["views"]) for f in
            an(pedir_json, cab, ini, fin, "views", dimensions="insightTrafficSourceDetail", filters=filtro,
               sort="-views", maxResults=10)]


def vistas_playlists(pedir_json, cab, ini, fin):
    for met in ("views,estimatedMinutesWatched,playlistStarts", "views,estimatedMinutesWatched"):
        try:
            return {f["playlist"]: f for f in an(pedir_json, cab, ini, fin, met, dimensions="playlist",
                                                 filters="isCurated==1", sort="-views", maxResults=200)}
        except Exception:
            continue
    return {}


def ctr_diario(pedir, pedir_json, cab, desde):
    """{(video, fecha): [impresiones, clics]} desde la Reporting API. Crea el trabajo la primera vez
    (YouTube empieza a generar los informes diarios a partir de entonces, con 1-2 días de retraso)."""
    jobs = pedir_json(f"{REPORTING}/jobs", headers=cab).get("jobs", [])
    job = next((j for j in jobs if j.get("reportTypeId") == TIPO_CTR), None)
    if not job:
        pedir_json(f"{REPORTING}/jobs", json.dumps({"reportTypeId": TIPO_CTR, "name": "ctr-saudi"}).encode(),
                   {**cab, "Content-Type": "application/json"})
        return None
    datos, pagina = {}, ""
    while True:
        r = pedir_json(f"{REPORTING}/jobs/{job['id']}/reports?" + urllib.parse.urlencode(
            {"startTimeAtOrAfter": desde.isoformat() + "T00:00:00Z", **({"pageToken": pagina} if pagina else {})}),
            headers=cab)
        for rep in r.get("reports", []):
            texto = pedir(rep["downloadUrl"], headers=cab).decode("utf-8", "replace")
            for f in csv.DictReader(io.StringIO(texto)):
                imp = float(f.get("video_thumbnail_impressions") or 0)
                ctr = float(f.get("video_thumbnail_impressions_ctr") or 0)
                ctr = ctr / 100 if ctr > 1 else ctr
                d = f.get("date", "")
                d = f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 else d
                k = (f.get("video_id"), d)
                a = datos.setdefault(k, [0.0, 0.0])
                a[0] += imp
                a[1] += imp * ctr
        pagina = r.get("nextPageToken")
        if not pagina:
            return datos


def ctr(datos, ini, fin, videos=None):
    imp = clic = 0.0
    for (v, d), (i, c) in (datos or {}).items():
        if ini.isoformat() <= d <= fin.isoformat() and (videos is None or v in videos):
            imp += i
            clic += c
    return (clic / imp if imp else None), imp


# ---------- recogida ----------

def recoger(yt, token, permisos, pedir, pedir_json, ahora, dias):
    """Junta todo lo que la sección necesita. Nunca lanza: lo que falla queda en 'notas'."""
    fin = (ahora - timedelta(days=1)).date()
    ini = fin - timedelta(days=dias - 1)
    cab = {"Authorization": f"Bearer {token}"} if token else {}
    res = {"ini": ini, "fin": fin, "notas": [], "registro": registro(), "ab": pruebas_ab(),
           "playlists": None, "an": None}
    vids = {v["id"]: v for v in yt.get("videos", [])}
    por_titulo = {v["titulo"]: v["id"] for v in yt.get("videos", [])}
    ever = []
    for m in res["registro"]:
        if m.get("tipo") == "evergreen":
            vid = m.get("video") or por_titulo.get(m.get("titulo", ""))
            if vid:
                ever.append(vid)
    res["evergreen"] = ever
    res["directos"] = [v["id"] for v in yt.get("videos", []) if v.get("directo")]
    ab_ids = [e.get("videoId") for e in res["ab"] if e.get("videoId")]
    ab_ids += [m["video"] for m in res["registro"] if m.get("tipo") == "ab" and m.get("video")]
    res["ab_ids"] = list(dict.fromkeys(ab_ids))

    if token and yt.get("fuente") == "api":
        try:
            res["playlists"] = playlists(pedir_json, cab)
        except Exception as e:
            res["notas"].append(f"No se pudieron leer las playlists ({e}).")
    if not (token and "https://www.googleapis.com/auth/yt-analytics.readonly" in permisos):
        res["notas"].append("Falta el permiso de YouTube Analytics (secreto YT_SAUDI_STATS_REFRESH_TOKEN): sin él no hay "
                            "CTR de miniaturas, vistas desde búsqueda, vistas desde playlists ni minutos vistos. "
                            "Mientras tanto comparo suscriptores y vistas con el informe del 20-nov.")
        return res
    a = res["an"] = {}
    pasos = [
        ("base", lambda: periodo(pedir_json, cab, BASE_INI, BASE_FIN)),
        ("semana", lambda: periodo(pedir_json, cab, ini, fin)),
        ("terminos", lambda: terminos_busqueda(pedir_json, cab, ini, fin)),
        ("playlists", lambda: vistas_playlists(pedir_json, cab, ini, fin)),
        ("videos", lambda: por_video(pedir_json, cab, ini, fin, list(dict.fromkeys(ever + res["directos"] + res["ab_ids"])))),
        ("ever_sem", lambda: periodo(pedir_json, cab, ini, fin, ever) if ever else None),
        ("ever_terminos", lambda: terminos_busqueda(pedir_json, cab, ini, fin, ever) if ever else []),
        ("ctr", lambda: ctr_diario(pedir, pedir_json, cab, min(BASE_INI, ini - timedelta(days=14)))),
    ]
    for nombre, f in pasos:
        try:
            a[nombre] = f()
        except Exception as e:
            a[nombre] = None
            res["notas"].append(f"YouTube Analytics ({nombre}) falló: {str(e)[:200]}")
    if a.get("ctr") is None and "ctr" in a and not any("(ctr)" in n for n in res["notas"]):
        res["notas"].append("CTR de miniaturas: acabo de activar el informe diario de alcance en YouTube (Reporting API). "
                            "Los datos empiezan a llegar en 1-2 días y saldrán en el próximo informe.")
    return res


# ---------- informe ----------

def _n(x, dec=0):
    if x is None:
        return "—"
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _pct(x):
    return "—" if x is None else _n(x * 100, 1) + " %"


def _cambio(ahora, antes):
    if ahora is None or not antes:
        return "—"
    c = (ahora - antes) / antes * 100
    return f"{'+' if c >= 0 else ''}{_n(c)} %"


def seccion(yt, imp, antes, vistas_sem):
    """Devuelve (líneas Markdown, fila de historial para el snapshot)."""
    vids = {v["id"]: v for v in yt.get("videos", [])}
    vistas_antes = antes.get("youtube", {}).get("videos", {})
    titulos_antes = antes.get("youtube", {}).get("titulos", {})
    a = imp.get("an") or {}
    ini, fin = imp["ini"], imp["fin"]
    L = ["## Impacto de las mejoras", "",
         f"Mejoras en marcha desde el {INICIO.strftime('%d-%m-%Y')}: miniaturas y títulos A/B, playlists por empresa y sector, "
         "vídeos evergreen de búsqueda y directos/estrenos. Semana medida: "
         f"{ini.isoformat()} a {fin.isoformat()}.", ""]
    fila = {"fecha": fin.isoformat(), "suscriptores": yt.get("suscriptores"), "vistas": vistas_sem}

    # 1) Canal: línea base frente a esta semana
    base, sem = a.get("base"), a.get("semana")
    L += ["### El canal, antes y ahora", ""]
    if base and sem:
        b = lambda k: base[k] / BASE_SEMANAS
        ctr_b = ctr_s = imp_s = None
        if a.get("ctr"):
            ctr_b, _ = ctr(a["ctr"], BASE_INI, BASE_FIN)
            ctr_s, imp_s = ctr(a["ctr"], ini, fin)
        pb = base["busqueda"] / base["views"] if base["views"] else None
        ps = sem["busqueda"] / sem["views"] if sem["views"] else None
        filas = [("Vistas", b("views"), sem["views"]),
                 ("Minutos vistos", b("estimatedMinutesWatched"), sem["estimatedMinutesWatched"]),
                 ("Suscriptores netos", b("subscribersGained") - b("subscribersLost"),
                  sem["subscribersGained"] - sem["subscribersLost"]),
                 ("Vistas desde búsqueda de YouTube", b("busqueda"), sem["busqueda"]),
                 ("Vistas desde playlists", b("desde_playlist"), sem["desde_playlist"])]
        L += [f"| Métrica | Media semanal antes ({BASE_INI.strftime('%d-%m')} a {BASE_FIN.strftime('%d-%m')}) | Esta semana | Cambio |",
              "|---|---|---|---|"]
        L += [f"| {n} | {_n(x, 1)} | {_n(y)} | {_cambio(y, x)} |" for n, x, y in filas]
        L.append(f"| Duración media de visionado (s) | {_n(base['averageViewDuration'])} | {_n(sem['averageViewDuration'])} | "
                 f"{_cambio(sem['averageViewDuration'], base['averageViewDuration'])} |")
        L.append(f"| % de vistas desde búsqueda | {_pct(pb)} | {_pct(ps)} | — |")
        L.append(f"| CTR de miniaturas | {_pct(ctr_b)} | {_pct(ctr_s)} | {_cambio(ctr_s, ctr_b)} |")
        fila.update(vistas=sem["views"], minutos=sem["estimatedMinutesWatched"], busqueda=sem["busqueda"],
                    playlist=sem["desde_playlist"], subs_netos=sem["subscribersGained"] - sem["subscribersLost"],
                    ctr=ctr_s, impresiones=imp_s)
    else:
        L += ["| Métrica | Antes (informe del 20-nov) | Ahora | Cambio |", "|---|---|---|---|",
              f"| Suscriptores | {BASE_PUBLICA['suscriptores']} | {_n(yt.get('suscriptores'))} | "
              f"{_cambio(yt.get('suscriptores'), BASE_PUBLICA['suscriptores'])} |",
              f"| Vistas de la semana | {_n(BASE_PUBLICA['vistas_semana'])} | {_n(vistas_sem)} | "
              f"{_cambio(vistas_sem, BASE_PUBLICA['vistas_semana'])} |"]
    L.append("")

    # Evolución semana a semana
    hist = [h for h in antes.get("historial_impacto", []) if h.get("fecha") != fila["fecha"]] + [fila]
    if len(hist) > 1:
        L += ["**Evolución semanal**", "", "| Semana hasta | Suscriptores | Vistas | Desde búsqueda | Desde playlists | CTR |",
              "|---|---|---|---|---|---|"]
        L += [f"| {h['fecha']} | {_n(h.get('suscriptores'))} | {_n(h.get('vistas'))} | {_n(h.get('busqueda'))} | "
              f"{_n(h.get('playlist'))} | {_pct(h.get('ctr'))} |" for h in hist[-8:]]
        L.append("")

    pv = a.get("videos") or {}

    def fila_video(vid, extra=""):
        v = vids.get(vid, {})
        t = (v.get("titulo") or vid).replace("|", "/")[:55]
        sem_v = pv.get(vid, {})
        delta = None
        if v and vid in vistas_antes:
            delta = v["vistas"] - vistas_antes[vid]
        elif v and (v.get("fecha") or "")[:10] >= ini.isoformat():
            delta = v["vistas"]   # publicado esta semana: todas sus vistas son de la semana
        return (f"| [{t}](https://youtu.be/{vid}) | {(v.get('fecha') or '')[:10]} | {_n(v.get('vistas'))} | "
                f"{_n(sem_v.get('views', delta))} | {_n(sem_v.get('estimatedMinutesWatched'))} | "
                f"{_n(sem_v.get('subscribersGained'))} |{extra}")

    # 2) A/B
    L += ["### 1. Miniaturas y títulos A/B", ""]
    if imp["ab"]:
        L += ["| Vídeo | Inicio | Qué | Estado | Ganadora | CTR antes | CTR después |", "|---|---|---|---|---|---|---|"]
        for e in imp["ab"]:
            vid = e.get("videoId", "")
            t = (vids.get(vid, {}).get("titulo") or e.get("slug", vid)).replace("|", "/")[:45]
            cb = cd = None
            if a.get("ctr") and e.get("inicio"):
                d0 = date.fromisoformat(str(e["inicio"])[:10])
                cb, _ = ctr(a["ctr"], d0 - timedelta(days=14), d0 - timedelta(days=1), {vid})
                cd, _ = ctr(a["ctr"], d0, fin, {vid})
            g = e.get("ganador") or e.get("ganadora")
            ganadora = g or "—"
            res, ana = e.get("resultado") or {}, e.get("analytics") or {}
            if g:
                partes = []
                for k in ("A", "B"):
                    r, x = res.get(k) or {}, ana.get(k) or {}
                    if x.get("ctr") is not None:
                        c = x["ctr"] / 100 if x["ctr"] > 1 else x["ctr"]
                        partes.append(f"{k}: CTR {_pct(c)}")
                    elif isinstance(r, dict) and r.get("vistas") is not None:
                        partes.append(f"{k}: {_n(r['vistas'])} vistas en {r.get('dias', '?')} días")
                if partes:
                    ganadora += " (" + ", ".join(partes) + ")"
            estado = ("cerrada " + str(e.get("cerrado", ""))[:10]).strip() if g else (
                "en pausa" if e.get("pausado") else f"día {len(e.get('dias', []))}")
            L.append(f"| [{t}](https://youtu.be/{vid}) | {str(e.get('inicio', ''))[:10]} | {e.get('que', '—')} | {estado} | "
                     f"{ganadora} | {_pct(cb)} | {_pct(cd)} |")
        cerradas = [e for e in imp["ab"] if e.get("ganador") or e.get("ganadora")]
        gana = {}
        for e in cerradas:
            g = e.get("ganador") or e.get("ganadora")
            estilo = ((e.get("variantes") or {}).get(g) or {}).get("estilo")
            if estilo:
                gana[estilo] = gana.get(estilo, 0) + 1
        if gana:
            L += ["", "Estilos que más ganan: " + ", ".join(f"{k} ({v})" for k, v in sorted(gana.items(), key=lambda x: -x[1])) + "."]
    else:
        L.append("Todavía no hay pruebas A/B registradas.")
    cambios = [(vid, titulos_antes[vid], v["titulo"]) for vid, v in vids.items()
               if vid in titulos_antes and titulos_antes[vid] != v["titulo"]]
    if cambios:
        L += ["", f"Títulos cambiados esta semana: {len(cambios)} vídeos."]
    L.append("")

    # 3) Playlists
    L += ["### 2. Playlists por empresa y sector", ""]
    pls = imp.get("playlists")
    if pls:
        vp = a.get("playlists") or {}
        L += ["| Playlist | Vídeos | Creada | Vistas semana | Minutos semana | Inicios |", "|---|---|---|---|---|---|"]
        for p in sorted(pls, key=lambda p: -(vp.get(p["id"], {}).get("views") or 0)):
            x = vp.get(p["id"], {})
            L.append(f"| [{p['titulo'].replace('|', '/')}](https://www.youtube.com/playlist?list={p['id']}) | {p['videos']} | "
                     f"{p['creada']} | {_n(x.get('views'))} | {_n(x.get('estimatedMinutesWatched'))} | {_n(x.get('playlistStarts'))} |")
        fila["playlists"] = len(pls)
    elif pls == []:
        L.append("El canal todavía no tiene playlists.")
    else:
        L.append("No se pudieron leer las playlists (hace falta el token de la API).")
    L.append("")

    # 4) Evergreen
    L += ["### 3. Vídeos evergreen de búsqueda", ""]
    if imp["evergreen"]:
        L += ["| Vídeo | Publicado | Vistas totales | Vistas semana | Minutos semana | Suscr. ganados |", "|---|---|---|---|---|---|"]
        L += [fila_video(v) for v in imp["evergreen"]]
        es = a.get("ever_sem")
        if es and es["views"]:
            L += ["", f"De sus {_n(es['views'])} vistas de la semana, {_n(es['busqueda'])} ({_pct(es['busqueda'] / es['views'])}) "
                  "vinieron de la búsqueda de YouTube."]
        if a.get("ever_terminos"):
            L.append("Búsquedas que los encontraron: " + ", ".join(f"«{k}» ({_n(v)})" for k, v in a["ever_terminos"]) + ".")
    else:
        L.append("Todavía no hay vídeos evergreen publicados (se registran en saudi/crecimiento/mejoras-saudi.json).")
    if a.get("terminos"):
        L += ["", "Búsquedas que trajeron vistas al canal esta semana: "
              + ", ".join(f"«{k}» ({_n(v)})" for k, v in a["terminos"]) + "."]
    L.append("")

    # 5) Directos y estrenos
    L += ["### 4. Directos y estrenos", ""]
    if imp["directos"]:
        L += ["| Vídeo | Fecha | Vistas totales | Vistas semana | Minutos semana | Suscr. ganados |", "|---|---|---|---|---|---|"]
        L += [fila_video(v) for v in imp["directos"]]
        fila["directos"] = len(imp["directos"])
    else:
        L.append("Todavía no ha habido directos ni estrenos.")
    L.append("")
    if imp["notas"]:
        L += [f"> {n}" for n in imp["notas"]] + [""]
    return L, fila
