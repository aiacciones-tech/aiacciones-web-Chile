"""Manda a Buffer los posts para X y LinkedIn que la rutina nocturna deja en cola/ de la rama youtube-cola
(lo usa .github/workflows/buffer.yml).

Cada post es un archivo cola/<slug>/post-x.txt (X) o cola/<slug>/post-linkedin.txt (LinkedIn).
Si el texto trae {youtube}, se reemplaza por el enlace del video de cola/<slug>/resultado.json; mientras
el video no esté subido, el post espera. Si el video quedó privado, el post va a Borradores en vez de publicarse.
Al mandarlo escribe cola/<slug>/buffer.json (X) o buffer-linkedin.json con el ID del post en Buffer, y no
vuelve a mandarlo. Si LinkedIn todavía no está conectado en Buffer, sus posts esperan sin dar error.

  python3 scripts/buffer.py verificar      # solo prueba la clave y muestra los canales
  python3 scripts/buffer.py programar cola # manda lo pendiente

Secreto del repo: BUFFER_API_KEY (Buffer > Settings > API).
Variables del repo (opcionales, Settings > Secrets and variables > Actions > Variables):
  BUFFER_MODO   ahora (por defecto: se publica en X al tiro), cola (en el próximo horario
                de la cola de Buffer) o borrador (queda en Borradores y Daniel lo aprueba)
  BUFFER_CANAL           ID del canal de X, si la cuenta tiene más de uno
  BUFFER_CANAL_LINKEDIN  ID del canal de LinkedIn, si hay más de uno (perfil y página)
Solo usa la biblioteca estándar de Python.
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone

API = "https://api.buffer.com"
MODOS = {"ahora": "shareNow", "cola": "addToQueue", "borrador": "addToQueue"}


def gql(consulta):
    req = urllib.request.Request(API, json.dumps({"query": consulta}).encode(), {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            datos = json.loads(r.read())
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")
        if e.code == 401:
            sys.exit("Buffer rechazó la clave (401). Revisa el secreto BUFFER_API_KEY.")
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
            todos.append(dict(c, org=org["name"]))
    return todos


REDES = {
    "x": {"nombre": "X", "archivo": "post-x.txt", "registro": "buffer.json", "servicios": ("twitter", "x"),
          "variable": "BUFFER_CANAL", "limite": 280, "largo": largo_x, "obligatoria": True},
    "linkedin": {"nombre": "LinkedIn", "archivo": "post-linkedin.txt", "registro": "buffer-linkedin.json",
                 "servicios": ("linkedin",), "variable": "BUFFER_CANAL_LINKEDIN", "limite": 3000,
                 "largo": len, "obligatoria": False},
}


def elegir_canal(red, lista):
    """El canal de Buffer de esa red, o None si no está conectado y la red es opcional."""
    r = REDES[red]
    if os.environ.get(r["variable"]):
        elegido = [c for c in lista if c["id"] == os.environ[r["variable"]]]
    else:
        elegido = [c for c in lista if c["service"].lower() in r["servicios"]]
    if not elegido and not r["obligatoria"]:
        return None
    if len(elegido) != 1:
        sys.exit(f"Encontré {len(elegido)} canales de {r['nombre']} en Buffer; conecta uno o define la variable "
                 f"{r['variable']}. Canales: {[(c['service'], c['name'], c['id']) for c in lista]}")
    return elegido[0]


def verificar():
    lista = canales()
    for c in lista:
        pausa = " (cola en pausa)" if c.get("isQueuePaused") else ""
        print(f"- {c['service']}: {c.get('displayName') or c['name']} [{c['id']}] en {c['org']}{pausa}")
    modo = os.environ.get("BUFFER_MODO") or "ahora"
    x = elegir_canal("x", lista)
    print(f"OK: la clave funciona y los posts irán a X como @{x['name']} en modo {modo}.")
    li = elegir_canal("linkedin", lista)
    print(f"OK: LinkedIn como {li.get('displayName') or li['name']}." if li
          else "LinkedIn todavía no está conectado en Buffer.")


def texto_final(carpeta, archivo="post-x.txt"):
    """Devuelve (texto, privado) o (None, motivo) si el video todavía no está subido."""
    texto = open(os.path.join(carpeta, archivo), encoding="utf-8").read().strip()
    res_path = os.path.join(carpeta, "resultado.json")
    res = json.load(open(res_path, encoding="utf-8")) if os.path.exists(res_path) else None
    if "{youtube}" in texto:
        if not res:
            return None, "esperando que el video se suba a YouTube"
        texto = texto.replace("{youtube}", f"https://youtu.be/{res['videoId']}")
    con_video = re.search(r"youtu\.?be", texto)
    privado = bool(con_video and (not res or res.get("privacy") != "public"))
    return texto, privado


def programar(base):
    modo = (os.environ.get("BUFFER_MODO") or "ahora").strip().lower()
    if modo not in MODOS:
        sys.exit(f"BUFFER_MODO debe ser ahora, cola o borrador, no {modo!r}.")
    pendientes = sorted((d, red) for d in os.listdir(base) for red, r in REDES.items()
                        if os.path.isfile(os.path.join(base, d, r["archivo"]))
                        and not os.path.exists(os.path.join(base, d, r["registro"])))
    if not pendientes:
        print("No hay posts pendientes.")
        return
    lista = canales()
    fallas = []
    for slug, red in pendientes:
        r = REDES[red]
        carpeta = os.path.join(base, slug)
        canal = elegir_canal(red, lista)
        if canal is None:
            print(f"{slug}: {r['nombre']} no está conectado en Buffer; queda pendiente.")
            continue
        texto, privado = texto_final(carpeta, r["archivo"])
        if texto is None:
            print(f"{slug} ({r['nombre']}): {privado}; queda pendiente.")
            continue
        largo = r["largo"](texto)
        if largo > r["limite"]:
            fallas.append(f"{slug}: {largo} caracteres para {r['nombre']} (máximo {r['limite']})")
            continue
        # Un enlace a un video privado no se ve: ese post va a Borradores para publicarlo a mano.
        modo_post = "borrador" if privado else modo
        extra = ", saveToDraft: true" if modo_post == "borrador" else ""
        resp = gql("mutation { createPost(input: {text: %s, channelId: %s, schedulingType: automatic, "
                   "mode: %s%s}) { ... on PostActionSuccess { post { id dueAt } } "
                   "... on MutationError { message } } }"
                   % (json.dumps(texto, ensure_ascii=False), json.dumps(canal["id"]), MODOS[modo_post],
                      extra))["createPost"]
        if "post" not in resp:
            fallas.append(f"{slug} ({r['nombre']}): {resp.get('message')}")
            continue
        json.dump({"id": resp["post"]["id"], "modo": modo_post, "video_privado": privado,
                   "programado": resp["post"].get("dueAt"), "canal": canal["name"], "texto": texto,
                   "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                  open(os.path.join(carpeta, r["registro"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        nota = " (video privado: quedó en Borradores)" if privado and modo != "borrador" else ""
        print(f"OK {slug}: post {resp['post']['id']} en {r['nombre']} ({modo_post}, {largo} caracteres){nota}.")
    if fallas:
        sys.exit("No se mandaron:\n" + "\n".join(fallas))


if __name__ == "__main__":
    if sys.argv[1:2] == ["verificar"]:
        verificar()
    elif sys.argv[1:2] == ["programar"] and len(sys.argv) == 3:
        programar(sys.argv[2])
    else:
        sys.exit(__doc__)
