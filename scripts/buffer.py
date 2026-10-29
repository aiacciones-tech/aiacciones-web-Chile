"""Manda a Buffer los posts para X, LinkedIn, TikTok e Instagram que la rutina nocturna deja en cola/ de la rama youtube-cola
(lo usa .github/workflows/buffer.yml).

Cada post es un archivo cola/<slug>/post-x.txt (X) o cola/<slug>/post-linkedin.txt (LinkedIn).
TikTok: cola/<slug>-short/post-tiktok.txt, junto al video.mp4 del Short; el video se manda a Buffer por su
enlace público en GitHub (raw.githubusercontent.com, fijado al commit), así que el repo debe seguir público.
Si el texto trae {youtube}, se reemplaza por el enlace del video de cola/<slug>/resultado.json; mientras
el video no esté subido, el post espera. Si el video quedó privado, el post va a Borradores en vez de publicarse.
Al mandarlo escribe cola/<slug>/buffer.json (X) o buffer-linkedin.json con el ID del post en Buffer, y no
vuelve a mandarlo (buffer-tiktok.json para TikTok). Si LinkedIn o TikTok todavía no están conectados en
Buffer, sus posts esperan sin dar error.

  python3 scripts/buffer.py verificar      # solo prueba la clave y muestra los canales
  python3 scripts/buffer.py programar cola # manda lo pendiente

Secreto del repo: BUFFER_API_KEY (Buffer > Settings > API).
Variables del repo (opcionales, Settings > Secrets and variables > Actions > Variables):
  BUFFER_MODO   ahora (por defecto: se publica en X al tiro), cola (en el próximo horario
                de la cola de Buffer) o borrador (queda en Borradores y Daniel lo aprueba)
  BUFFER_HORA   no (por defecto: los posts de Chile salen al tiro, también de noche) o una hora de Chile
                HH:MM: un post mandado entre las 21:00 y esa hora se programa para esa hora.
                "no" lo desactiva (todo sale al tiro).
  BUFFER_CANAL           ID del canal de X, si la cuenta tiene más de uno
  BUFFER_CANAL_LINKEDIN  ID del canal de LinkedIn, si hay más de uno (perfil y página)
  BUFFER_CANAL_TIKTOK    ID del canal de TikTok, si hay más de uno
  BUFFER_CANAL_LINKEDIN_ES  ID de la página de LinkedIn de AIAcciones España (para cola-es/)
Secreto opcional BUFFER_API_KEY_ES: clave de una segunda cuenta de Buffer solo para España (el plan gratis
admite 3 canales por cuenta). Si existe, cola-es/ usa esa cuenta; si no, la de Chile. Un canal de esa cuenta
cuyo nombre diga "chile" (p. ej. el TikTok aiaccioneschile) es de Chile y lo usa cola/.
Secreto opcional BUFFER_API_KEY_ES2: tercera cuenta de Buffer, también solo de España (Instagram aiacciones.espana).
Instagram: <cola>/<slug>/post-instagram.txt junto a video.mp4 (se publica como Reel) o a imagen.png (post en
el feed, 1080x1350). Vale para cola/ (Chile) y cola-es/ (España).
X, LinkedIn y Facebook: si en la carpeta hay imagen.png, el post la lleva adjunta (p. ej. un calendario).
España: `programar cola-es` manda los posts de cola-es/ solo a canales cuyo nombre diga "espana"/"españa"
(hoy, la página de LinkedIn); si no hay canal de España para esa red, el post espera. Con dos páginas
de LinkedIn conectadas, Chile usa la que se llama "chile".
EAU (Emiratos, canal @AIStocksUAE, posts en árabe): `programar cola-eau` manda los posts de cola-eau/ con su
propia cuenta de Buffer (secreto BUFFER_ACCESS_TOKEN_EAU, que el workflow pasa como BUFFER_API_KEY_EAU) y, si
existe, una segunda (BUFFER_ACCESS_TOKEN_EAU2, para pasar del límite de 3 canales del plan gratis); todos
los canales de esas cuentas son de EAU. Todo post de EAU lleva el enlace al canal de YouTube (se agrega si falta) y nunca usa los de Chile ni España. Si hay más de un canal de una red,
variable BUFFER_CANAL_EAU, BUFFER_CANAL_LINKEDIN_EAU, BUFFER_CANAL_TIKTOK_EAU o BUFFER_CANAL_INSTAGRAM_EAU.
Solo usa la biblioteca estándar de Python.
"""
import json, os, re, subprocess, sys, unicodedata, urllib.request
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

API = "https://api.buffer.com"
MODOS = {"ahora": "shareNow", "cola": "addToQueue", "borrador": "addToQueue"}


CLAVE = "BUFFER_API_KEY"  # España usa BUFFER_API_KEY_ES (su propia cuenta de Buffer) si existe


def gql(consulta):
    req = urllib.request.Request(API, json.dumps({"query": consulta}).encode(), {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ[CLAVE]}",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            datos = json.loads(r.read())
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")
        if e.code == 401:
            sys.exit(f"Buffer rechazó la clave (401). Revisa el secreto {CLAVE}.")
        sys.exit(f"Error HTTP {e.code} de Buffer: {cuerpo[:800]}")
    if datos.get("errors"):
        sys.exit(f"Error de Buffer: {json.dumps(datos['errors'], ensure_ascii=False)[:800]}")
    return datos["data"]


def largo_x(texto):
    """Largo ponderado de X: cada URL cuenta 23, emojis y la mayoría de símbolos cuentan 2."""
    texto = re.sub(r"https?://\S+", "x" * 23, texto)
    n = 0
    for c in texto:
        o = ord(c)
        if o in (0xFE0F, 0x200D):
            continue
        n += 1 if (o <= 0x10FF or 0x2000 <= o <= 0x200D or 0x2010 <= o <= 0x201F
                   or 0x2032 <= o <= 0x2037) else 2
    return n


def canales():
    orgs = gql("query { account { organizations { id name } } }")["account"]["organizations"]
    todos = []
    for org in orgs:
        q = 'query { channels(input: {organizationId: %s}) { id name displayName service isQueuePaused } }'
        for c in gql(q % json.dumps(org["id"]))["channels"]:
            todos.append(dict(c, org=org["name"], clave=CLAVE))
    return todos


REDES = {
    "x": {"nombre": "X", "archivo": "post-x.txt", "registro": "buffer.json", "servicios": ("twitter", "x"),
          "variable": "BUFFER_CANAL", "limite": 280, "largo": largo_x, "obligatoria": True, "imagen": True},
    "linkedin": {"nombre": "LinkedIn", "archivo": "post-linkedin.txt", "registro": "buffer-linkedin.json",
                 "servicios": ("linkedin",), "variable": "BUFFER_CANAL_LINKEDIN", "limite": 3000,
                 "largo": len, "obligatoria": False, "imagen": True},
    "tiktok": {"nombre": "TikTok", "archivo": "post-tiktok.txt", "registro": "buffer-tiktok.json",
               "servicios": ("tiktok",), "variable": "BUFFER_CANAL_TIKTOK", "limite": 2200,
               "largo": len, "obligatoria": False, "video": True},
    "instagram": {"nombre": "Instagram", "archivo": "post-instagram.txt", "registro": "buffer-instagram.json",
                  "servicios": ("instagram",), "variable": "BUFFER_CANAL_INSTAGRAM", "limite": 2200,
                  "largo": len, "obligatoria": False, "video": True, "imagen": True,
                  "metadata": "{instagram: {type: reel, shouldShareToFeed: true}}"},
    # Página de Facebook (hoy solo EAU): post-facebook.txt o, en cola-eau/, el mismo texto de post-linkedin.txt
    "facebook": {"nombre": "Facebook", "archivo": "post-facebook.txt", "registro": "buffer-facebook.json",
                 "servicios": ("facebook",), "variable": "BUFFER_CANAL_FACEBOOK", "limite": 63206,
                 "largo": len, "obligatoria": False, "alterno_eau": "post-linkedin.txt", "imagen": True},
}


def archivo_post(carpeta, r, pais):
    """El archivo de texto del post de esa red en la carpeta, o None si no hay."""
    for nombre in (r["archivo"], r.get("alterno_eau") if pais == "eau" else None):
        if nombre and os.path.isfile(os.path.join(carpeta, nombre)):
            return nombre
    return None
CLAVES_ES = ("BUFFER_API_KEY_ES", "BUFFER_API_KEY_ES2")  # cuentas de Buffer solo de España
CLAVES_EAU = ("BUFFER_API_KEY_EAU", "BUFFER_API_KEY_EAU2")  # cuentas de Buffer solo de EAU (@AIStocksUAE)
CANAL_EAU = "https://www.youtube.com/@AIStocksUAE"
SUFIJOS = {"chile": "", "espana": "_ES", "eau": "_EAU"}


def sin_tildes(t):
    return unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()


def es_de(c, pais):
    nombre = sin_tildes(f"{c['name']} {c.get('displayName') or ''}")
    # un canal que dice "chile" es de Chile aunque esté en la cuenta de España (p. ej. el TikTok aiaccioneschile)
    if "chile" in nombre:
        return pais == "chile"
    # el resto de la cuenta de Buffer de España es de España, aunque su nombre no lo diga (p. ej. @AIAccionesES)
    if c.get("clave") in CLAVES_ES:
        return pais == "espana"
    return pais in nombre


def canales_chile():
    """Canales de la cuenta de Chile, más los de las cuentas de España cuyo nombre dice "chile"."""
    global CLAVE
    usar_clave("chile")
    lista = canales()
    for clave in CLAVES_ES:
        if os.environ.get(clave):
            CLAVE = clave
            lista += [c for c in canales() if es_de(c, "chile")]
    usar_clave("chile")
    return lista


def elegir_canal(red, lista, pais="chile"):
    """El canal de Buffer de esa red para ese país, o None si no está conectado y la red es opcional."""
    r = REDES[red]
    variable = r["variable"] + SUFIJOS[pais]
    if os.environ.get(variable):
        elegido = [c for c in lista if c["id"] == os.environ[variable]]
    else:
        elegido = [c for c in lista if c["service"].lower() in r["servicios"]]
        if pais == "espana":
            elegido = [c for c in elegido if es_de(c, "espana")]
        elif pais == "eau":
            elegido = [c for c in elegido if c.get("clave") in CLAVES_EAU]
        elif len(elegido) > 1:
            # Chile: si también está conectado el canal de España, ese no cuenta
            elegido = [c for c in elegido if not es_de(c, "espana")] or elegido
            if len(elegido) > 1:
                elegido = [c for c in elegido if es_de(c, "chile")] or elegido
    if not elegido and (pais != "chile" or not r["obligatoria"]):
        return None
    if len(elegido) != 1:
        sys.exit(f"Encontré {len(elegido)} canales de {r['nombre']} en Buffer; conecta uno o define la variable "
                 f"{variable}. Canales: {[(c['service'], c['name'], c['id']) for c in lista]}")
    return elegido[0]


def canales_espana():
    """Canales de España de sus propias cuentas de Buffer (BUFFER_API_KEY_ES y BUFFER_API_KEY_ES2)."""
    global CLAVE
    propios = []
    for clave in CLAVES_ES:
        if os.environ.get(clave):
            CLAVE = clave
            propios += [c for c in canales() if es_de(c, "espana")]
    return propios


def canales_eau():
    """Canales de las cuentas de Buffer de EAU (BUFFER_API_KEY_EAU y BUFFER_API_KEY_EAU2), o [] si no hay clave."""
    global CLAVE
    lista = []
    for clave in CLAVES_EAU:
        if os.environ.get(clave):
            CLAVE = clave
            lista += canales()
    return lista


def usar_clave(pais):
    global CLAVE
    CLAVE = "BUFFER_API_KEY_ES" if pais == "espana" and os.environ.get("BUFFER_API_KEY_ES") else "BUFFER_API_KEY"


def verificar():
    lista = canales_chile()
    for c in lista:
        pausa = " (cola en pausa)" if c.get("isQueuePaused") else ""
        print(f"- {c['service']}: {c.get('displayName') or c['name']} [{c['id']}] en {c['org']}{pausa}")
    modo = os.environ.get("BUFFER_MODO") or "ahora"
    x = elegir_canal("x", lista)
    print(f"OK: la clave funciona y los posts irán a X como @{x['name']} en modo {modo}.")
    hora = os.environ.get("BUFFER_HORA") or "no"
    print("Posts de noche: salen al tiro." if hora.strip().lower() == "no"
          else f"Posts mandados entre las 21:00 y las {hora} (hora de Chile) salen a las {hora}.")
    li = elegir_canal("linkedin", lista)
    print(f"OK: LinkedIn como {li.get('displayName') or li['name']}." if li
          else "LinkedIn todavía no está conectado en Buffer.")
    tt = elegir_canal("tiktok", lista)
    print(f"OK: TikTok como {tt.get('displayName') or tt['name']}." if tt
          else "TikTok todavía no está conectado en Buffer.")
    fb = elegir_canal("facebook", lista)
    if fb:
        print(f"OK: Facebook como {fb.get('displayName') or fb['name']}.")
    ig = elegir_canal("instagram", lista)
    print(f"OK: Instagram como {ig.get('displayName') or ig['name']}." if ig
          else "Instagram de Chile todavía no está conectado en Buffer.")
    usar_clave("espana")
    if CLAVE != "BUFFER_API_KEY":
        print("España usa su propia cuenta de Buffer (BUFFER_API_KEY_ES):")
        propios = canales_espana()
        for c in propios:
            print(f"- {c['service']}: {c.get('displayName') or c['name']} [{c['id']}] en {c['org']}")
        servicios = {c["service"].lower() for c in propios}
        lista = propios + [c for c in lista if c["service"].lower() not in servicios]
    for red in REDES:
        es = elegir_canal(red, lista, "espana")
        print(f"España, {REDES[red]['nombre']}: " + (es.get("displayName") or es["name"] if es else "sin canal"))
    if os.environ.get(CLAVES_EAU[0]):
        print("EAU usa sus propias cuentas de Buffer (BUFFER_ACCESS_TOKEN_EAU y _EAU2):")
        lista = canales_eau()
        for c in lista:
            print(f"- {c['service']}: {c.get('displayName') or c['name']} [{c['id']}] en {c['org']} ({c['clave']})")
        for red in REDES:
            ea = elegir_canal(red, lista, "eau")
            print(f"EAU, {REDES[red]['nombre']}: " + (ea.get("displayName") or ea["name"] if ea else "sin canal"))
    else:
        print("EAU: falta el secreto BUFFER_ACCESS_TOKEN_EAU.")


CHILE = ZoneInfo("America/Santiago")
NOCHE = 21  # desde las 21:00 de Chile casi nadie ve los posts: esperan a la mañana


def hora_manana(ahora=None):
    """dueAt (ISO UTC) de la próxima BUFFER_HORA de Chile si ahora es de noche, o None si el post sale al tiro."""
    hora = (os.environ.get("BUFFER_HORA") or "no").strip().lower()
    if hora == "no":
        return None
    try:
        h, m = (int(x) for x in hora.split(":"))
        manana = time(h, m)
    except ValueError:
        sys.exit(f"BUFFER_HORA debe ser HH:MM (p. ej. 08:00) o no, no {hora!r}.")
    ahora = (ahora or datetime.now(timezone.utc)).astimezone(CHILE)
    if manana <= ahora.time() < time(NOCHE):
        return None
    dia = ahora.date() + timedelta(days=ahora.time() >= time(NOCHE))
    return datetime.combine(dia, manana, CHILE).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def texto_final(carpeta, archivo="post-x.txt"):
    """Devuelve (texto, privado) o (None, motivo) si el video todavía no está subido."""
    texto = open(os.path.join(carpeta, archivo), encoding="utf-8").read().strip()
    res_path = os.path.join(carpeta, "resultado.json")
    res = json.load(open(res_path, encoding="utf-8")) if os.path.exists(res_path) else None
    if "{youtube}" in texto:
        if not res:
            return None, "esperando que el video se suba a YouTube"
        texto = texto.replace("{youtube}", f"https://youtu.be/{res['videoId']}")
    # solo enlaces a un video (no el del canal, p. ej. youtube.com/@AIStocksUAE)
    con_video = re.search(r"youtu\.be/|youtube\.com/(watch|shorts/)", texto)
    privado = bool(con_video and (not res or res.get("privacy") != "public"))
    return texto, privado


def enlace_video(carpeta, nombre="video.mp4"):
    """Enlace público y directo al archivo de la carpeta, fijado al commit que lo trae (no expira)."""
    ruta = os.path.join(carpeta, nombre)
    if not os.path.isfile(ruta):
        return None
    commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", ruta],
                            capture_output=True, text=True).stdout.strip()
    if not commit:
        return None
    repo = os.environ.get("GITHUB_REPOSITORY", "aiacciones-tech/aiacciones-web-Chile")
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{os.path.relpath(ruta).replace(os.sep, '/')}"


def programar(base):
    global CLAVE
    pais = {"cola-es": "espana", "cola-eau": "eau"}.get(os.path.basename(os.path.normpath(base)), "chile")
    modo = (os.environ.get("BUFFER_MODO") or "ahora").strip().lower()
    if modo not in MODOS:
        sys.exit(f"BUFFER_MODO debe ser ahora, cola o borrador, no {modo!r}.")
    pendientes = sorted((d, red) for d in os.listdir(base) for red, r in REDES.items()
                        if archivo_post(os.path.join(base, d), r, pais)
                        and not os.path.exists(os.path.join(base, d, r["registro"])))
    if not pendientes:
        print("No hay posts pendientes.")
        return
    if pais == "eau" and not os.environ.get(CLAVES_EAU[0]):
        sys.exit("Falta el secreto BUFFER_ACCESS_TOKEN_EAU para mandar cola-eau/.")
    # España: canales de su propia cuenta de Buffer (si hay clave) y, como respaldo, los de la cuenta de Chile
    # EAU: solo los de su cuenta
    lista = canales_eau() if pais == "eau" else canales_chile()
    if pais != "eau":
        usar_clave(pais)
    if pais == "espana" and CLAVE != "BUFFER_API_KEY":
        propios = canales_espana()
        servicios = {c["service"].lower() for c in propios}
        lista = propios + [c for c in lista if c["service"].lower() not in servicios]
    fallas = []
    for slug, red in pendientes:
        r = REDES[red]
        carpeta = os.path.join(base, slug)
        canal = elegir_canal(red, lista, pais)
        if canal is None:
            print(f"{slug}: {r['nombre']} no está conectado en Buffer; queda pendiente.")
            continue
        texto, privado = texto_final(carpeta, archivo_post(carpeta, r, pais))
        if texto is None:
            print(f"{slug} ({r['nombre']}): {privado}; queda pendiente.")
            continue
        if pais == "chile" and r.get("video") and "aiacciones.cl" not in texto:
            # todo post de Chile lleva la web (en TikTok/Instagram no es clicable, pero se ve)
            texto += "\n\nFicha completa en aiacciones.cl"
        if pais == "eau" and CANAL_EAU.lower() not in texto.lower():
            # todo post de EAU lleva el enlace al canal de YouTube (Daniel, 29-oct-2026)
            con_rotulo = texto + f"\n\nقناتنا على يوتيوب: {CANAL_EAU}"
            texto = con_rotulo if r["largo"](con_rotulo) <= r["limite"] else texto + f"\n{CANAL_EAU}"
        largo = r["largo"](texto)
        if largo > r["limite"]:
            fallas.append(f"{slug}: {largo} caracteres para {r['nombre']} (máximo {r['limite']})")
            continue
        # Un enlace a un video privado no se ve: ese post va a Borradores para publicarlo a mano.
        CLAVE = canal["clave"]
        modo_post = "borrador" if privado else modo
        extra = ", saveToDraft: true" if modo_post == "borrador" else ""
        imagen = r.get("imagen") and enlace_video(carpeta, "imagen.png")
        if imagen:
            # imagen.png: en X, LinkedIn y Facebook va adjunta; en Instagram es post en el feed en vez de Reel
            extra += ", assets: [{image: {url: %s}}]" % json.dumps(imagen)
            if red == "instagram":
                extra += ", metadata: {instagram: {type: post, shouldShareToFeed: true}}"
        elif r.get("video"):
            url = enlace_video(carpeta)
            if not url:
                fallas.append(f"{slug} ({r['nombre']}): falta video.mp4 en el commit de la carpeta")
                continue
            extra += ", assets: [{video: {url: %s, metadata: {thumbnailOffset: 1000}}}]" % json.dumps(url)
        if r.get("metadata") and not imagen:
            extra += ", metadata: " + r["metadata"]
        modo_api = MODOS[modo_post]
        manana = pais == "chile" and modo_post == "ahora" and hora_manana()
        if manana:
            # de noche: el post de Chile queda programado para la mañana
            modo_api, extra = "customScheduled", extra + f", dueAt: {json.dumps(manana)}"
        resp = gql("mutation { createPost(input: {text: %s, channelId: %s, schedulingType: automatic, "
                   "mode: %s%s}) { ... on PostActionSuccess { post { id dueAt } } "
                   "... on MutationError { message } } }"
                   % (json.dumps(texto, ensure_ascii=False), json.dumps(canal["id"]), modo_api,
                      extra))["createPost"]
        if "post" not in resp:
            fallas.append(f"{slug} ({r['nombre']}): {resp.get('message')}")
            continue
        json.dump({"id": resp["post"]["id"], "modo": modo_post, "video_privado": privado,
                   "programado": resp["post"].get("dueAt"), "canal": canal["name"], "texto": texto,
                   "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                  open(os.path.join(carpeta, r["registro"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        nota = " (video privado: quedó en Borradores)" if privado and modo != "borrador" else ""
        cuando = f", sale {resp['post'].get('dueAt')}" if manana else ""
        print(f"OK {slug}: post {resp['post']['id']} en {r['nombre']} ({modo_post}{cuando}, {largo} caracteres){nota}.")
    if fallas:
        sys.exit("No se mandaron:\n" + "\n".join(fallas))


if __name__ == "__main__":
    if sys.argv[1:2] == ["verificar"]:
        verificar()
    elif sys.argv[1:2] == ["programar"] and len(sys.argv) == 3:
        programar(sys.argv[2])
    else:
        sys.exit(__doc__)
