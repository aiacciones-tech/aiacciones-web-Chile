"""Pruebas A/B de miniatura y título en los videos largos de Saudi Arabia AI Stocks (lo usa .github/workflows/ab-saudi.yml).

YouTube no ofrece "Test & Compare" en la API, así que la prueba se hace por turnos:
  * Una carpeta de cola-sa/ entra en prueba si tiene ab.json (lo escriben saudi/diario/gen_meta.py y saudi/educativo/meta_leccion.py):
      {"que": "ambos" | "miniatura" | "titulo",
       "B": {"title": "...", "miniatura": "miniatura-b.png"},
       "estilos": {"A": "fecha", "B": "gancho"}}
    La variante A es la de siempre (meta.json + miniatura.png), con la que se sube el video.
  * Los días se cuentan en hora del Pacífico (los días de YouTube Analytics). El día 0 es el de la subida.
    Días 1 a 4: A, B, A, B (orden "AB") o B, A, B, A (orden "BA"); el orden se alterna entre videos para que
    la caída natural de vistas con los días no favorezca siempre a la misma variante. El día 0 (incompleto) no cuenta y muestra la A.
  * Cada día, justo después de la medianoche del Pacífico, se guarda el contador de vistas (Data API): vistas del día d = contador(d+1) - contador(d).
  * El día 5 se suman las vistas de cada variante, se deja puesta la que tiene más (empate: la A) y se cierra la prueba.
  * Si hay un token con permiso yt-analytics.readonly (YT_STATS_REFRESH_TOKEN), desde el día 8 (los datos de Analytics
    tardan 2-3 días) se piden impresiones y CTR de la miniatura por día; si las dos variantes tienen impresiones, manda el CTR
    y, si gana la otra, se cambia.
El estado de cada prueba queda en cola-sa/<slug>/ab-estado.json (el workflow lo sube a la rama youtube-cola).
Para pausar una prueba (p. ej. si se usa Test & Compare de YouTube Studio en ese video): "pausado": true en ab-estado.json.

  python3 scripts/ab-saudi.py rotar cola-sa     # cambia variantes, guarda contadores y cierra pruebas
  python3 scripts/ab-saudi.py resumen cola-sa   # tabla en Markdown con todas las pruebas

Credenciales: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (el de subida, permiso youtube) y, opcional, YT_STATS_REFRESH_TOKEN.
Solo usa la biblioteca estándar de Python.
"""
import json, os, sys, urllib.parse, urllib.request
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

API = "https://www.googleapis.com"
PT = ZoneInfo("America/Los_Angeles")
DIAS_PRUEBA = 4          # días 1..4
DIA_ANALYTICS = 8        # desde este día se piden impresiones y CTR
HORA_CONTADOR = 3        # el contador del día se guarda solo si en el Pacífico son menos de las 03:00


class Falla(Exception):
    pass


def pedir(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise Falla(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def token(refresh):
    datos = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                    "refresh_token": refresh, "grant_type": "refresh_token"}).encode()
    r = json.loads(pedir("https://oauth2.googleapis.com/token", datos, {"Content-Type": "application/x-www-form-urlencoded"}))
    return r["access_token"], set(r.get("scope", "").split())


def leer(p, defecto=None):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else defecto


def guardar(p, x):
    json.dump(x, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def ahora_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fecha_pt(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(PT).date()


def variante_del_dia(orden, k):
    """Variante que debe verse el día k: el día 0 (subida, no cuenta) siempre la A; días 1-4 según el orden."""
    return "A" if k <= 0 else orden[(k - 1) % 2]


# ---------- YouTube ----------

def vistas(t, ids):
    out = {}
    for i in range(0, len(ids), 50):
        r = json.loads(pedir(f"{API}/youtube/v3/videos?part=statistics&id={','.join(ids[i:i + 50])}",
                             headers={"Authorization": f"Bearer {t}"}))
        out.update({it["id"]: int(it["statistics"].get("viewCount", 0)) for it in r.get("items", [])})
    return out


def poner_miniatura(t, vid, png):
    pedir(f"{API}/upload/youtube/v3/thumbnails/set?videoId={vid}", open(png, "rb").read(),
          {"Authorization": f"Bearer {t}", "Content-Type": "image/png"})


def poner_titulo(t, vid, titulo):
    r = json.loads(pedir(f"{API}/youtube/v3/videos?part=snippet&id={vid}", headers={"Authorization": f"Bearer {t}"}))
    if not r.get("items"):
        raise Falla("video no encontrado")
    s = r["items"][0]["snippet"]
    if s.get("title") == titulo:
        return
    sn = {k: s[k] for k in ("description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in s}
    sn["title"] = titulo[:100]
    pedir(f"{API}/youtube/v3/videos?part=snippet", json.dumps({"id": vid, "snippet": sn}).encode(),
          {"Authorization": f"Bearer {t}", "Content-Type": "application/json; charset=UTF-8"}, "PUT")


def aplicar(t, carpeta, ab, est, v):
    """Pone la variante v (miniatura y/o título). Devuelve True si quedó puesta."""
    meta = leer(os.path.join(carpeta, "meta.json"), {})
    png = os.path.join(carpeta, "miniatura.png" if v == "A" else ab["B"].get("miniatura", "miniatura-b.png"))
    titulo = meta.get("title") if v == "A" else ab["B"].get("title")
    que = ab.get("que", "ambos")
    if que in ("ambos", "miniatura") and os.path.exists(png):
        poner_miniatura(t, est["videoId"], png)
    if que in ("ambos", "titulo") and titulo:
        poner_titulo(t, est["videoId"], titulo)
    est["mostrada"] = v
    est.setdefault("cambios", []).append({"variante": v, "utc": ahora_utc()})
    return True


def analytics(ts, vid, desde, hasta):
    """Vistas, impresiones y CTR de la miniatura por día (fechas del Pacífico). Si la API no da impresiones, solo vistas."""
    for metricas in ("views,videoThumbnailImpressions,videoThumbnailImpressionsClickRate", "views"):
        q = urllib.parse.urlencode({"ids": "channel==MINE", "startDate": desde.isoformat(), "endDate": hasta.isoformat(),
                                    "metrics": metricas, "dimensions": "day", "filters": f"video=={vid}"})
        try:
            r = json.loads(pedir(f"https://youtubeanalytics.googleapis.com/v2/reports?{q}", headers={"Authorization": f"Bearer {ts}"}))
        except Falla as e:
            if metricas != "views" and "HTTP 400" in str(e):
                continue
            raise
        cols = [c["name"] for c in r.get("columnHeaders", [])]
        return {fila[0]: dict(zip(cols[1:], fila[1:])) for fila in r.get("rows", [])}
    return {}


# ---------- Rotación ----------

def calcular(est):
    """Vistas por día de prueba (contadores de medianoche a medianoche) y totales por variante."""
    ini = date.fromisoformat(est["inicio"]); c = est.get("contadores", {}); dias = []
    for k in range(1, DIAS_PRUEBA + 1):
        d0, d1 = (ini + timedelta(days=k)).isoformat(), (ini + timedelta(days=k + 1)).isoformat()
        n = c[d1]["vistas"] - c[d0]["vistas"] if d0 in c and d1 in c else None
        dias.append({"fecha": d0, "variante": variante_del_dia(est["orden"], k), "vistas": n})
    res = {v: {"vistas": sum(d["vistas"] for d in dias if d["variante"] == v and d["vistas"] is not None),
               "dias": sum(1 for d in dias if d["variante"] == v and d["vistas"] is not None)} for v in "AB"}
    return dias, res


def rotar(base):
    hoy = datetime.now(PT).date(); medianoche = datetime.now(PT).hour < HORA_CONTADOR
    carpetas = []
    for d in sorted(os.listdir(base)):
        c = os.path.join(base, d)
        if os.path.exists(os.path.join(c, "ab.json")) and os.path.exists(os.path.join(c, "resultado.json")):
            carpetas.append(c)
    if not carpetas:
        print("No hay videos con prueba A/B.")
        return
    n_previas = sum(1 for c in carpetas if os.path.exists(os.path.join(c, "ab-estado.json")))
    t, _ = token(os.environ["YT_REFRESH_TOKEN"])
    ts = None
    if os.environ.get("YT_STATS_REFRESH_TOKEN"):
        try:
            ts, permisos = token(os.environ["YT_STATS_REFRESH_TOKEN"])
            if "https://www.googleapis.com/auth/yt-analytics.readonly" not in permisos:
                print("El token de estadísticas no tiene yt-analytics.readonly: se mide solo con vistas.")
                ts = None
        except Falla as e:
            print(f"Token de estadísticas: {e}")
    estados = {}
    for c in carpetas:
        res = leer(os.path.join(c, "resultado.json")); ab = leer(os.path.join(c, "ab.json"))
        est = leer(os.path.join(c, "ab-estado.json"))
        if est is None:
            est = {"slug": os.path.basename(c), "videoId": res["videoId"], "que": ab.get("que", "ambos"),
                   "variantes": {"A": {"estilo": ab.get("estilos", {}).get("A", "A"), "titulo": leer(os.path.join(c, "meta.json"), {}).get("title")},
                                 "B": {"estilo": ab.get("estilos", {}).get("B", "B"), "titulo": ab["B"].get("title")}},
                   "orden": "AB" if n_previas % 2 == 0 else "BA", "inicio": fecha_pt(res["subido"]).isoformat(),
                   "mostrada": "A", "contadores": {}, "cambios": [{"variante": "A", "utc": res["subido"]}]}
            n_previas += 1
        estados[c] = (est, ab)
    activos = [e["videoId"] for e, _ in estados.values() if not e.get("pausado") and not e.get("analytics_hecho")]
    conteo = vistas(t, activos) if activos and medianoche else {}
    limite = False
    for c, (est, ab) in estados.items():
        if est.get("pausado"):
            continue
        k = (hoy - date.fromisoformat(est["inicio"])).days
        if k < 0:
            continue
        if est["videoId"] in conteo and hoy.isoformat() not in est["contadores"] and k <= DIAS_PRUEBA + 1:
            est["contadores"][hoy.isoformat()] = {"vistas": conteo[est["videoId"]], "utc": ahora_utc()}
        try:
            if not est.get("cerrado"):
                fin = (date.fromisoformat(est["inicio"]) + timedelta(days=DIAS_PRUEBA + 1)).isoformat()
                if k <= DIAS_PRUEBA or (k == DIAS_PRUEBA + 1 and fin not in est["contadores"]):
                    # el día 5 se cierra con el contador de su medianoche; hasta tenerlo sigue la variante del día 4
                    objetivo = variante_del_dia(est["orden"], min(k, DIAS_PRUEBA))
                else:
                    est["dias"], est["resultado"] = calcular(est)
                    a, b = est["resultado"]["A"], est["resultado"]["B"]
                    est["ganador"] = "B" if b["dias"] and a["dias"] and b["vistas"] > a["vistas"] else "A"
                    est["metrica"] = "vistas" if a["dias"] and b["dias"] else "sin datos (se deja la A)"
                    est["cerrado"] = ahora_utc(); objetivo = est["ganador"]
                    print(f"{est['slug']}: prueba cerrada, A {a['vistas']} vistas / B {b['vistas']} vistas -> {objetivo}")
                if not est.get("cerrado"):
                    est["dias"] = calcular(est)[0][:max(k, 0)]  # días de prueba ya empezados (el informe semanal los cuenta)
                if objetivo != est["mostrada"] and not limite:
                    aplicar(t, c, ab, est, objetivo)
                    print(f"{est['slug']}: día {k}, variante {objetivo}")
            elif ts and k >= DIA_ANALYTICS and not est.get("analytics_hecho"):
                ini = date.fromisoformat(est["inicio"])
                filas = analytics(ts, est["videoId"], ini + timedelta(days=1), ini + timedelta(days=DIAS_PRUEBA))
                tot = {v: {"vistas": 0, "impresiones": 0, "clics": 0.0} for v in "AB"}
                for k2 in range(1, DIAS_PRUEBA + 1):
                    f = filas.get((ini + timedelta(days=k2)).isoformat(), {}); v = variante_del_dia(est["orden"], k2)
                    tot[v]["vistas"] += f.get("views", 0) or 0
                    imp = f.get("videoThumbnailImpressions") or 0
                    tot[v]["impresiones"] += imp; tot[v]["clics"] += imp * (f.get("videoThumbnailImpressionsClickRate") or 0)
                for v in "AB":
                    tot[v]["ctr"] = round(tot[v]["clics"] / tot[v]["impresiones"], 5) if tot[v]["impresiones"] else None
                est["analytics"] = tot; est["analytics_hecho"] = ahora_utc()
                if tot["A"]["impresiones"] and tot["B"]["impresiones"]:
                    g = "B" if tot["B"]["ctr"] > tot["A"]["ctr"] else "A"
                    est["metrica"] = "ctr"
                    if g != est["ganador"]:
                        est["ganador"] = g
                        if not limite:
                            aplicar(t, c, ab, est, g)
                    print(f"{est['slug']}: CTR A {tot['A']['ctr']} / B {tot['B']['ctr']} -> {g}")
                elif est["mostrada"] != est["ganador"] and not limite:
                    aplicar(t, c, ab, est, est["ganador"])
            elif est.get("mostrada") != est.get("ganador") and not limite:  # reintento tras un 429
                aplicar(t, c, ab, est, est["ganador"])
        except Falla as e:
            print(f"{est['slug']}: {e}")
            if "HTTP 429" in str(e):
                limite = True; print("Límite de YouTube alcanzado; se reintenta en la próxima ejecución.")
        guardar(os.path.join(c, "ab-estado.json"), est)


# ---------- Resumen ----------

def resumen(base):
    filas = []; ganadas = {}; tot = {}
    for d in sorted(os.listdir(base)):
        est = leer(os.path.join(base, d, "ab-estado.json"))
        if not est:
            continue
        r = est.get("resultado") or calcular(est)[1]
        an = est.get("analytics") or {}
        ctr = lambda v: f"{an[v]['ctr'] * 100:.1f}%" if an.get(v, {}).get("ctr") is not None else "—"
        estado = "pausada" if est.get("pausado") else (f"gana {est['ganador']} ({est.get('metrica')})" if est.get("cerrado") else f"en curso ({est['mostrada']})")
        filas.append(f"| {est['slug']} | {est['que']} | {est['variantes']['A']['estilo']} / {est['variantes']['B']['estilo']} | {est['orden']} | "
                     f"{r['A']['vistas']} / {r['B']['vistas']} | {ctr('A')} / {ctr('B')} | {estado} |")
        if est.get("cerrado") and not est.get("pausado"):
            par = f"{est['variantes']['A']['estilo']} vs {est['variantes']['B']['estilo']}"
            g = ganadas.setdefault(par, {"A": 0, "B": 0, "n": 0}); g["n"] += 1; g[est["ganador"]] += 1
            t2 = tot.setdefault(par, {"A": 0, "B": 0}); t2["A"] += r["A"]["vistas"]; t2["B"] += r["B"]["vistas"]
    print("## Pruebas A/B de miniatura y título\n")
    if not filas:
        print("Todavía no hay pruebas."); return
    print("| Video | Qué se prueba | Estilos A / B | Orden | Vistas A / B | CTR A / B | Estado |\n|---|---|---|---|---|---|---|")
    print("\n".join(filas))
    for par, g in ganadas.items():
        print(f"\n**{par}**: {g['n']} pruebas cerradas, gana A {g['A']} y B {g['B']} · vistas totales A {tot[par]['A']} / B {tot[par]['B']}.")
    print("\nCon pocas vistas por video, una prueba sola no dice mucho: lo útil es el acumulado de muchas pruebas.")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "resumen"
    base = sys.argv[2] if len(sys.argv) > 2 else "cola-sa"
    rotar(base) if modo == "rotar" else resumen(base)
