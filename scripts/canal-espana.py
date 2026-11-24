"""Crecimiento del canal @AIAccionesEspaña (Daniel, 24-nov-2026). Lo usa .github/workflows/canal-espana.yml.

  python3 scripts/canal-espana.py programados <raíz del clon de youtube-cola>
      Sube a YouTube los vídeos de cola-es-programado/<slug>/ cuya hora "publicar" (UTC, en meta.json) ya pasó
      (hoy: el segundo Short del vídeo diario, a las 08:30 de Madrid del día siguiente). Antes resuelve los enlaces
      ({lista:...}, {ultimo:...}) con espana/enlaces_cola.py y mueve la carpeta a cola-es/<slug>/ con su resultado.json.
      Solo YouTube: sin posts en redes. Respeta el límite de ~10 subidas en 24 h del canal.

  python3 scripts/canal-espana.py listas <raíz del clon de youtube-cola> [máximo de operaciones]
      Listas de reproducción por serie y por empresa. Crea las que falten y añade cada vídeo subido de cola-es/
      (resultado.json) a sus listas, el más nuevo arriba. El estado queda en cola-es/listas.json:
        {"listas": {"diario": {"id": "PL...", "titulo": "..."}, ...}, "añadidos": {"<slug>": ["diario", ...]}}
      Cada operación gasta 50 unidades de la cuota diaria de la API (10.000), por eso va por tandas (40 por defecto):
      la primera vez tarda unos días en meter los ~140 vídeos antiguos.
      Necesita un token con permiso "youtube" (no basta "youtube.upload"); si no lo tiene, lo dice y no falla.

Credenciales: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (las de youtube-espana.yml). Solo biblioteca estándar.
"""
import importlib.util, json, os, re, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


yt = cargar("youtube_es", os.path.join(AQUI, "youtube.py"))
enl = cargar("enlaces_cola", os.path.join(RAIZ, "espana", "enlaces_cola.py"))
API = "https://www.googleapis.com/youtube/v3"
PERMISOS = {"https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"}
AVISO = ("Contenido informativo y educativo de AIAcciones España: no es una recomendación de inversión ni asesoramiento "
         "personalizado. Invertir en bolsa conlleva riesgo de pérdida. Más en https://aiacciones.es")


def leer(p, defecto=None):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else defecto


def guardar(p, x):
    json.dump(x, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def subidas_24h(cola):
    ahora = datetime.now(timezone.utc); n = 0
    for d in os.listdir(cola):
        r = leer(os.path.join(cola, d, "resultado.json"))
        if not r:
            continue
        try:
            s = datetime.fromisoformat(r["subido"].replace("Z", "+00:00"))
        except Exception:
            continue
        if s.tzinfo is None:
            s = s.replace(tzinfo=timezone.utc)
        n += ahora - s < timedelta(hours=24)
    return n


# ---------- Vídeos programados ----------

def programados(raiz):
    prog, cola = os.path.join(raiz, "cola-es-programado"), os.path.join(raiz, "cola-es")
    if not os.path.isdir(prog):
        print("No hay vídeos programados."); return
    ahora = datetime.now(timezone.utc); t = None
    for slug in sorted(os.listdir(prog)):
        c = os.path.join(prog, slug); meta_p = os.path.join(c, "meta.json")
        meta = leer(meta_p)
        if not meta or not os.path.exists(os.path.join(c, "video.mp4")):
            continue
        cuando = datetime.fromisoformat(meta.get("publicar", "2000-01-01T00:00:00+00:00").replace("Z", "+00:00"))
        if cuando > ahora:
            print(f"{slug}: espera hasta {cuando.isoformat()}"); continue
        if os.path.exists(os.path.join(cola, slug, "resultado.json")):
            print(f"{slug}: ya subido"); continue
        n = subidas_24h(cola)
        if n > 8:
            print(f"{slug}: {n} subidas en 24 h, se deja para la próxima ejecución (límite ~10)"); break
        meta["description"] = enl.resolver(meta.get("description", ""), cola, slug)
        meta.pop("publicar", None)
        dest = os.path.join(cola, slug); os.makedirs(dest, exist_ok=True)
        guardar(os.path.join(dest, "meta.json"), meta)
        os.replace(os.path.join(c, "video.mp4"), os.path.join(dest, "video.mp4"))
        t = t or yt.token()
        yt.subir_uno(t, dest)
        os.remove(os.path.join(dest, "video.mp4"))  # el mp4 no se guarda en git (ya está en YouTube)
        open(os.path.join(c, "subido.txt"), "w").write(leer(os.path.join(dest, "resultado.json"))["url"] + "\n")


# ---------- Listas de reproducción ----------

PER = r"(?:[1-4]T|[12]S|FY)\d\d"


def nombres_empresas():
    try:
        f = cargar("fichas", os.path.join(RAIZ, "espana", "fichas.py"))
        return {x["id"]: x["nombre"] for x in f.FICHAS}
    except Exception as e:
        print("No se pudieron leer los nombres de espana/fichas.py:", e); return {}


def periodo_txt(p):
    return {"T": f"{p[0]}T", "S": f"{p[0]}S"}.get(p[1], p[:2]) + " 20" + p[-2:]


def claves(slug):
    """Listas a las que va cada vídeo de cola-es/ según su carpeta."""
    corto = re.search(r"-short\d*$", slug) is not None
    base = re.sub(r"-short\d*$", "", slug)
    out = ["shorts"] if corto else []
    if re.fullmatch(r"bolsa-\d{4}-\d\d-\d\d", base):
        out += [] if corto else ["diario"]
    elif base.startswith("curso-"):
        out += [] if corto else ["curso"]
    elif base.startswith("calendario-"):
        out += ["calendario"]
    else:
        m = re.fullmatch(rf"(.+)-({PER})", base)
        if m:
            out += [f"empresa-{m.group(1)}"] + ([] if corto else [f"resultados-{m.group(2)}"])
    return out


def titulo_lista(k, nombres):
    fijas = {
        "diario": ("IBEX 35 hoy: resumen diario de la bolsa española",
                   "Cada día de bolsa, el cierre del IBEX 35: noticias, por qué se movió, valores y análisis técnico."),
        "shorts": ("La bolsa española en 1 minuto (Shorts)",
                   "Los Shorts de AIAcciones España: el IBEX 35 del día, resultados de empresas y calendario semanal."),
        "curso": ("Análisis técnico, explicado fácil (curso)",
                  "Curso semanal de análisis técnico con el gráfico real de Inditex: un concepto por capítulo."),
        "calendario": ("Calendario semanal de resultados (IBEX 35)",
                       "Cada domingo, qué empresas españolas presentan resultados la semana siguiente y qué espera el mercado."),
    }
    if k in fijas:
        return fijas[k]
    if k.startswith("resultados-"):
        p = periodo_txt(k.split("-", 1)[1])
        return (f"Resultados {p} del IBEX 35", f"Los resultados {p} de las empresas del IBEX 35, explicados en vídeo con cifras oficiales.")
    eid = k.split("-", 1)[1]; n = nombres.get(eid, eid.replace("-", " ").title())
    return (f"{n}: resultados y análisis en vídeo", f"Todos los vídeos de AIAcciones España sobre {n}: resultados, cifras clave y Shorts. "
            f"Ficha: https://aiacciones.es/empresas/{eid}/")


def api(t, ruta, cuerpo):
    _, _, r = yt.pedir(f"{API}/{ruta}", json.dumps(cuerpo).encode(),
                       {"Authorization": f"Bearer {t}", "Content-Type": "application/json; charset=UTF-8"}, "POST")
    return json.loads(r)


def token_con_permisos():
    datos = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                    "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    _, _, r = yt.pedir("https://oauth2.googleapis.com/token", datos, {"Content-Type": "application/x-www-form-urlencoded"})
    r = json.loads(r)
    return r["access_token"], set(r.get("scope", "").split())


def listas(raiz, maximo=40):
    cola = os.path.join(raiz, "cola-es"); est_p = os.path.join(cola, "listas.json")
    est = leer(est_p, {"listas": {}, "añadidos": {}}); est.setdefault("listas", {}); est.setdefault("añadidos", {})
    pend = []
    for slug in sorted(os.listdir(cola)):
        r = leer(os.path.join(cola, slug, "resultado.json"))
        if not r or not r.get("videoId"):
            continue
        hechas = set(est["añadidos"].get(slug, []))
        for k in claves(slug):
            if k not in hechas:
                pend.append((r.get("subido", ""), slug, r["videoId"], k))
    pend = [x[1:] for x in sorted(pend)]  # por fecha de subida: con "position": 0 el más nuevo queda arriba
    if not pend:
        print("Listas al día."); return
    t, permisos = token_con_permisos()
    if not permisos & PERMISOS:
        print("AVISO: el token de YouTube España (YT_ES_REFRESH_TOKEN) solo tiene permiso de subida "
              f"({' '.join(sorted(permisos))}). Para crear listas hace falta el permiso «youtube»: ver espana/crecimiento-youtube.md.")
        return
    nombres = nombres_empresas(); ops = 0
    for slug, vid, k in pend:
        if ops >= maximo:
            print(f"Tope de {maximo} operaciones por día (cuota de la API): quedan {len(pend)} pendientes para mañana."); break
        try:
            if k not in est["listas"]:
                titulo, desc = titulo_lista(k, nombres)
                r = api(t, "playlists?part=snippet,status", {"snippet": {"title": titulo[:150], "description": f"{desc}\n\n{AVISO}",
                        "defaultLanguage": "es"}, "status": {"privacyStatus": "public"}})
                est["listas"][k] = {"id": r["id"], "titulo": titulo}; ops += 1
                print(f"Lista creada: {titulo} ({r['id']})")
            api(t, "playlistItems?part=snippet", {"snippet": {"playlistId": est["listas"][k]["id"], "position": 0,
                    "resourceId": {"kind": "youtube#video", "videoId": vid}}})
            ops += 1
            est["añadidos"].setdefault(slug, []).append(k)
            print(f"{slug} -> {k}")
        except SystemExit as e:  # yt.pedir sale con el error HTTP
            print(f"{slug} -> {k}: {e}")
            if "quota" in str(e).lower() or "429" in str(e):
                break
            if "videoNotFound" in str(e) or "404" in str(e):
                est["añadidos"].setdefault(slug, []).append(k)  # vídeo borrado: no reintentar
        finally:
            guardar(est_p, est)
    guardar(est_p, est)


if __name__ == "__main__":
    modo, raiz = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "."
    if modo == "programados":
        programados(raiz)
    elif modo == "listas":
        listas(raiz, int(sys.argv[3]) if len(sys.argv) > 3 else 40)
    else:
        sys.exit(__doc__)
