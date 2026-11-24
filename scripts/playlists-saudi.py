"""Playlists del canal Saudi Arabia AI Stocks (@SaudiArabiaAIStocks): las crea y les añade los videos de cola-sa/.

  python3 scripts/playlists-saudi.py <cola-sa> <config.json> <estado.json> [--presupuesto 2500] [--simular]

- <config.json>: saudi/playlists/playlists-saudi.json (títulos y descripciones en árabe, empresas y sectores).
- <estado.json>: playlists-saudi.json en la raíz de la rama youtube-cola. Guarda el ID de cada playlist y los videos
  ya añadidos; un video que Daniel quite a mano de una playlist no se vuelve a añadir.
- Solo entran videos públicos (resultado.json "privacy": "public").
- Qué video va a qué playlist sale del nombre de la carpeta:
    bolsa-<fecha>                 -> diario
    lesson-ta-NN-<empresa>        -> tecnico (+ empresa y su sector)
    calendar-*, earnings-calendar* -> calendario
    <empresa>-<periodo>           -> resultados (+ empresa y su sector)
  Las carpetas -short son Shorts: entran en la playlist de la empresa y en la del calendario, no en las demás.
- Se añaden en orden de subida y en la posición 0, así lo más nuevo queda arriba.
- Cuota de la API de YouTube: crear playlist o añadir un video = 50 unidades; listar = 1. Con --presupuesto
  se para antes de pasarse; lo que falte entra en la siguiente pasada. Si YouTube contesta quotaExceeded,
  guarda lo hecho y termina sin error.
- --simular: no llama a la API, solo muestra qué haría.

Credenciales: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (las del canal saudí, como en youtube-saudi.yml).
Solo usa la biblioteca estándar de Python.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3"
COSTO = {"listar": 1, "crear": 50, "anadir": 50}


class SinCuota(Exception):
    pass


class LimiteCrear(Exception):
    """YouTube limita cuántas playlists se crean seguidas (429 RATE_LIMIT_EXCEEDED); se sigue añadiendo a las que ya existen."""


class Cliente:
    def __init__(self, presupuesto, simular):
        self.presupuesto, self.simular, self.gastado, self.t = presupuesto, simular, 0, None

    def token(self):
        datos = urllib.parse.urlencode({
            "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
            "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
        req = urllib.request.Request("https://oauth2.googleapis.com/token", datos,
                                     {"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())["access_token"]

    def puede(self, tipo):
        return self.gastado + COSTO[tipo] <= self.presupuesto

    def pedir(self, tipo, ruta, cuerpo=None):
        if not self.puede(tipo):
            raise SinCuota(f"presupuesto de {self.presupuesto} unidades alcanzado")
        self.gastado += COSTO[tipo]
        self.t = self.t or self.token()
        data = json.dumps(cuerpo).encode() if cuerpo is not None else None
        # YouTube da 409 SERVICE_UNAVAILABLE si se añade muy rápido (sobre todo a una playlist recién creada): se reintenta.
        for espera in (3, 10, 30, None):
            req = urllib.request.Request(f"{API}/{ruta}", data, {"Authorization": f"Bearer {self.t}",
                                                                "Content-Type": "application/json; charset=UTF-8"})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    time.sleep(1)
                    return json.loads(r.read() or b"{}")
            except urllib.error.HTTPError as e:
                txt = e.read().decode("utf-8", "replace")
                if e.code == 403 and ("quotaExceeded" in txt or "rateLimitExceeded" in txt):
                    raise SinCuota("YouTube dice que se acabó la cuota diaria de la API")
                if e.code == 429 and tipo == "crear":
                    raise LimiteCrear()
                if e.code == 429:
                    raise SinCuota("YouTube pide bajar el ritmo (429)")
                if e.code in (409, 500, 503) and espera:
                    time.sleep(espera)
                    continue
                raise RuntimeError(f"HTTP {e.code} en {ruta.split('?')[0]}: {txt[:600]}")


def clasificar(slug, empresas):
    """-> (tipo, empresa o None, es_short) o None si la carpeta no va a ninguna playlist."""
    short = slug.endswith("-short")
    base = slug[:-6] if short else slug
    partes = base.split("-")
    if base.startswith("bolsa-"):
        return "diario", None, short
    if base.startswith("lesson-"):
        return "tecnico", partes[-1] if partes[-1] in empresas else None, short
    if base.startswith("calendar-") or base.startswith("earnings-calendar"):
        return "calendario", None, short
    if partes[0] in empresas and len(partes) > 1:
        return "resultados", partes[0], short
    return None


def destinos(slug, cfg):
    empresas = {e["id"]: e for e in cfg["empresas"]}
    c = clasificar(slug, empresas)
    if not c:
        return []
    tipo, emp, short = c
    claves = [f["clave"] for f in cfg["formatos"] if tipo in f["tipos"] and (f["shorts"] or not short)]
    if emp:
        claves.append(f"empresa-{emp}")
        if not short:
            claves.append(f"sector-{empresas[emp]['sector']}")
    return claves


def definiciones(cfg):
    """Todas las playlists posibles: clave -> (título, descripción)."""
    pie = "\n\n{aviso}\n\nاشترك في القناة: {canal}"
    defs = {}
    for f in cfg["formatos"]:
        defs[f["clave"]] = (f["titulo"], f["descripcion"] + pie.format(**cfg) + "\n\n" + f["hashtags"]
                            + " #الأسهم_السعودية #تداول")
    sectores = {s["clave"]: s for s in cfg["sectores"]}
    for s in cfg["sectores"]:
        defs[f"sector-{s['clave']}"] = (s["titulo"], s["descripcion"] + pie.format(**cfg) + "\n\n" + s["hashtags"]
                                        + " #الأسهم_السعودية #تداول")
    for e in cfg["empresas"]:
        datos = dict(e, sector_ar=sectores[e["sector"]]["nombre_ar"], canal=cfg["canal"], aviso=cfg["aviso"],
                     hashtag=re.sub(r"\W+", "_", e["nombre_ar"]).strip("_"))
        defs[f"empresa-{e['id']}"] = (cfg["empresa"]["titulo"].format(**datos),
                                      cfg["empresa"]["descripcion"].format(**datos))
    return defs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    simular = "--simular" in sys.argv
    presupuesto = 2500
    if "--presupuesto" in sys.argv:
        presupuesto = int(sys.argv[sys.argv.index("--presupuesto") + 1])
        args.remove(str(presupuesto))
    base, cfg_p, est_p = args
    cfg = json.load(open(cfg_p, encoding="utf-8"))
    estado = json.load(open(est_p, encoding="utf-8")) if os.path.exists(est_p) else {}
    estado.setdefault("_nota", "Lo escribe scripts/playlists-saudi.py: ID de cada playlist del canal saudí y videos ya añadidos.")
    estado.setdefault("playlists", {})
    defs = definiciones(cfg)

    # Videos públicos, del más antiguo al más nuevo.
    videos = []
    for d in os.listdir(base):
        rp = os.path.join(base, d, "resultado.json")
        if not os.path.exists(rp):
            continue
        res = json.load(open(rp, encoding="utf-8"))
        if res.get("privacy") == "public" and res.get("videoId"):
            videos.append((res.get("subido", ""), d, res["videoId"]))
    videos.sort()

    pendientes = []  # (clave, videoId, carpeta)
    for _, d, vid in videos:
        for clave in destinos(d, cfg):
            pl = estado["playlists"].get(clave, {})
            if vid not in pl.get("videos", []):
                pendientes.append((clave, vid, d))
    print(f"{len(videos)} videos públicos; {len(pendientes)} altas pendientes en playlists.")
    if simular:
        for clave, vid, d in pendientes:
            print(f"  {d} -> {clave} ({defs[clave][0]})")
        return

    cli = Cliente(presupuesto, simular)
    hechas, creadas, errores, sin_crear = 0, 0, 0, False
    existentes = {}
    try:
        # Playlists que ya existen en el canal (por si el estado se perdió): se reconocen por el título.
        if any(clave not in estado["playlists"] for clave, _, _ in pendientes):
            tok = ""
            while True:
                r = cli.pedir("listar", f"playlists?part=snippet&mine=true&maxResults=50&pageToken={tok}")
                for it in r.get("items", []):
                    existentes[it["snippet"]["title"]] = it["id"]
                tok = r.get("nextPageToken")
                if not tok:
                    break
        for clave, vid, d in pendientes:
            pl = estado["playlists"].get(clave)
            if not pl:
                titulo, desc = defs[clave]
                if titulo in existentes:
                    pid = existentes[titulo]
                elif sin_crear:
                    continue
                else:
                    try:
                        r = cli.pedir("crear", "playlists?part=snippet,status", {
                            "snippet": {"title": titulo[:150], "description": desc[:5000], "defaultLanguage": "ar"},
                            "status": {"privacyStatus": "public"}})
                    except LimiteCrear:
                        sin_crear = True
                        print("YouTube no deja crear más playlists por ahora (429); las que faltan se crean en otra pasada.")
                        continue
                    pid = r["id"]
                    creadas += 1
                    time.sleep(5)  # dar tiempo a YouTube antes de añadirle videos
                    print(f"Creada: {titulo} -> https://www.youtube.com/playlist?list={pid}")
                pl = estado["playlists"][clave] = {"id": pid, "titulo": titulo, "videos": []}
                json.dump(estado, open(est_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            try:
                cli.pedir("anadir", "playlistItems?part=snippet", {"snippet": {
                    "playlistId": pl["id"], "position": 0, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
            except RuntimeError as e:
                errores += 1
                print(f"  {d} -> {pl['titulo']}: {e} (se reintenta en la próxima pasada)")
                continue
            pl["videos"].append(vid)
            hechas += 1
            print(f"  {d} -> {pl['titulo']}")
            json.dump(estado, open(est_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except SinCuota as e:
        print(f"Parado: {e}. Lo que falta entra en la próxima pasada.")
    json.dump(estado, open(est_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Listo: {creadas} playlists creadas, {hechas} videos añadidos, ~{cli.gastado} unidades de cuota; "
          f"quedan {len(pendientes) - hechas} altas.")
    if errores:
        sys.exit(f"{errores} altas fallaron (no por cuota).")


if __name__ == "__main__":
    main()
