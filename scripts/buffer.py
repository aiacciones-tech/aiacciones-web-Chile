"""Manda a Buffer los posts para X que la rutina nocturna deja en cola/ de la rama youtube-cola
(lo usa .github/workflows/buffer.yml).

Cada post es un archivo cola/<slug>/post-x.txt (el mismo texto de <empresa>/post-x-<trimestre>.txt).
Al mandarlo escribe cola/<slug>/buffer.json con el ID del post en Buffer, y no vuelve a mandar esa carpeta.

  python3 scripts/buffer.py verificar      # solo prueba la clave y muestra los canales
  python3 scripts/buffer.py programar cola # manda lo pendiente

Secreto del repo: BUFFER_API_KEY (Buffer > Settings > API).
Variables del repo (opcionales, Settings > Secrets and variables > Actions > Variables):
  BUFFER_MODO   borrador (por defecto: queda en Borradores de Buffer y Daniel lo aprueba)
                o cola (se publica solo en el próximo horario de la cola de Buffer)
  BUFFER_CANAL  ID del canal de X, si la cuenta tiene más de uno
Solo usa la biblioteca estándar de Python.
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone

API = "https://api.buffer.com"
LIMITE_X = 280


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


def canal_x():
    lista = canales()
    if os.environ.get("BUFFER_CANAL"):
        elegido = [c for c in lista if c["id"] == os.environ["BUFFER_CANAL"]]
    else:
        elegido = [c for c in lista if c["service"].lower() in ("twitter", "x")]
    if len(elegido) != 1:
        sys.exit(f"Encontré {len(elegido)} canales de X en Buffer; conecta uno o define la variable "
                 f"BUFFER_CANAL. Canales: {[(c['service'], c['name'], c['id']) for c in lista]}")
    return elegido[0]


def verificar():
    lista = canales()
    for c in lista:
        pausa = " (cola en pausa)" if c.get("isQueuePaused") else ""
        print(f"- {c['service']}: {c.get('displayName') or c['name']} [{c['id']}] en {c['org']}{pausa}")
    x = canal_x()
    print(f"OK: la clave funciona y los posts irán a X como @{x['name']} "
          f"en modo {os.environ.get('BUFFER_MODO') or 'borrador'}.")


def programar(base):
    modo = (os.environ.get("BUFFER_MODO") or "borrador").strip().lower()
    if modo not in ("borrador", "cola"):
        sys.exit(f"BUFFER_MODO debe ser borrador o cola, no {modo!r}.")
    pendientes = sorted(d for d in os.listdir(base)
                        if os.path.isfile(os.path.join(base, d, "post-x.txt"))
                        and not os.path.exists(os.path.join(base, d, "buffer.json")))
    if not pendientes:
        print("No hay posts pendientes.")
        return
    x = canal_x()
    fallas = []
    for slug in pendientes:
        carpeta = os.path.join(base, slug)
        texto = open(os.path.join(carpeta, "post-x.txt"), encoding="utf-8").read().strip()
        largo = largo_x(texto)
        if largo > LIMITE_X:
            fallas.append(f"{slug}: {largo} caracteres para X (máximo {LIMITE_X})")
            continue
        extra = ", saveToDraft: true" if modo == "borrador" else ""
        r = gql("mutation { createPost(input: {text: %s, channelId: %s, schedulingType: automatic, "
                "mode: addToQueue%s}) { ... on PostActionSuccess { post { id dueAt } } "
                "... on MutationError { message } } }"
                % (json.dumps(texto, ensure_ascii=False), json.dumps(x["id"]), extra))["createPost"]
        if "post" not in r:
            fallas.append(f"{slug}: {r.get('message')}")
            continue
        json.dump({"id": r["post"]["id"], "modo": modo, "programado": r["post"].get("dueAt"),
                   "canal": x["name"], "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                  open(os.path.join(carpeta, "buffer.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"OK {slug}: post {r['post']['id']} en Buffer ({modo}, {largo} caracteres).")
    if fallas:
        sys.exit("No se mandaron:\n" + "\n".join(fallas))


if __name__ == "__main__":
    if sys.argv[1:2] == ["verificar"]:
        verificar()
    elif sys.argv[1:2] == ["programar"] and len(sys.argv) == 3:
        programar(sys.argv[2])
    else:
        sys.exit(__doc__)
