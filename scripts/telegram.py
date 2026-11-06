#!/usr/bin/env python3
"""Publica en el canal de Telegram los videos de una cola (p. ej. cola-sa/ de la rama youtube-cola).

Uso:
  python3 scripts/telegram.py verificar            prueba el bot y el canal (no publica nada)
  python3 scripts/telegram.py publicar cola-sa     publica lo pendiente

Credenciales (Settings > Secrets and variables > Actions):
  TELEGRAM_BOT_TOKEN  token que da @BotFather (el workflow lo pasa desde TELEGRAM_BOT_TOKEN_SAUDI)
  TELEGRAM_CHANNEL    @usuario del canal o su id numérico (desde TELEGRAM_CHANNEL_SAUDI)
El bot tiene que ser administrador del canal con permiso para publicar mensajes.

Qué se publica: cada carpeta de la cola con post-telegram.txt, o si no post-facebook.txt (el texto largo),
cuyo video ya está subido y público en YouTube (resultado.json). {youtube} se cambia por el enlace del video.
Va como foto (miniatura.png) con el texto de pie; si el texto pasa de 1024 caracteres, foto y luego mensaje.
Las carpetas *-short solo se publican si traen su propio post-telegram.txt (si no, repetirían el video largo).
Lo publicado queda en <carpeta>/telegram.json, así no se repite.

Opcional (lo usa Qatar):
  TELEGRAM_SOLO_POST_TELEGRAM=1   publica solo carpetas con post-telegram.txt (no usa post-facebook.txt)
  TELEGRAM_CANAL_YOUTUBE=<url>    si el texto no trae ese enlace, se añade al final
Opcional (lo usa EAU):
  TELEGRAM_TEXTOS=a.txt,b.txt     textos a buscar, en orden (por defecto post-telegram.txt,post-facebook.txt)
  TELEGRAM_DESDE=2026-11-03       ignora los videos subidos antes de esa fecha (para no publicar el atrasado)
Opcional (lo usa Chile):
  TELEGRAM_TEXTO_YOUTUBE=...      frase antes del enlace al canal de YouTube (por defecto en árabe)
  TELEGRAM_WEB=https://aiacciones.cl   si el texto no trae ese sitio, se añade "🌐 <web>" al final
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

API = "https://api.telegram.org/bot{token}/{metodo}"
LIMITE_PIE = 1024
TEXTOS = ("post-telegram.txt", "post-facebook.txt")
REGISTRO = "telegram.json"


def llamar(metodo, campos=None, archivo=None):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        sys.exit("Falta el secreto del bot de Telegram (TELEGRAM_BOT_TOKEN_<PAÍS>).")
    url = API.format(token=token, metodo=metodo)
    campos = {k: v for k, v in (campos or {}).items() if v is not None}
    if archivo:
        limite = uuid.uuid4().hex
        partes = []
        for k, v in campos.items():
            partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        nombre_campo, ruta = archivo
        partes.append((f'--{limite}\r\nContent-Disposition: form-data; name="{nombre_campo}"; '
                       f'filename="{os.path.basename(ruta)}"\r\nContent-Type: application/octet-stream\r\n\r\n').encode())
        partes.append(open(ruta, "rb").read())
        partes.append(f"\r\n--{limite}--\r\n".encode())
        datos, tipo = b"".join(partes), f"multipart/form-data; boundary={limite}"
    else:
        datos, tipo = json.dumps(campos).encode(), "application/json"
    req = urllib.request.Request(url, data=datos, headers={"Content-Type": tipo})
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)["result"]
        except urllib.error.HTTPError as e:
            cuerpo = json.loads(e.read().decode() or "{}")
            espera = cuerpo.get("parameters", {}).get("retry_after")
            if e.code == 429 and espera and intento < 2:
                time.sleep(int(espera) + 1)
                continue
            sys.exit(f"Telegram {metodo}: error {e.code}: {cuerpo.get('description', cuerpo)}")


def canal():
    c = os.environ.get("TELEGRAM_CHANNEL", "").strip()
    if not c:
        sys.exit("Falta el secreto del canal de Telegram (TELEGRAM_CHANNEL_<PAÍS>), p. ej. @aiaccioneschile.")
    if c.startswith("https://t.me/") or c.startswith("t.me/"):
        c = "@" + c.rstrip("/").rsplit("/", 1)[1]
    elif not c.startswith("@") and not c.lstrip("-").isdigit():
        c = "@" + c
    return c


def verificar():
    bot = llamar("getMe")
    print(f"Bot: @{bot['username']} ({bot['first_name']})")
    chat = llamar("getChat", {"chat_id": canal()})
    print(f"Canal: {chat.get('title')} (@{chat.get('username', '-')}, id {chat['id']})")
    yo = llamar("getChatMember", {"chat_id": chat["id"], "user_id": bot["id"]})
    if yo.get("status") not in ("administrator", "creator") or not yo.get("can_post_messages", yo["status"] == "creator"):
        sys.exit("El bot no es administrador del canal o no tiene permiso para publicar mensajes.")
    print("El bot es administrador y puede publicar. Todo listo.")


def pendiente(carpeta):
    """Devuelve (texto, foto) si hay que publicar la carpeta, o None."""
    if os.path.exists(os.path.join(carpeta, REGISTRO)):
        return None
    solo = os.environ.get("TELEGRAM_SOLO_POST_TELEGRAM", "").strip() not in ("", "0")
    todos = tuple(x.strip() for x in os.environ.get("TELEGRAM_TEXTOS", "").split(",") if x.strip()) or TEXTOS
    textos = todos[:1] if solo or carpeta.rstrip("/").endswith("-short") else todos
    archivo = next((t for t in textos if os.path.isfile(os.path.join(carpeta, t))), None)
    if not archivo:
        return None
    res_path = os.path.join(carpeta, "resultado.json")
    if not os.path.exists(res_path):
        print(f"{carpeta}: esperando que el video se suba a YouTube")
        return None
    res = json.load(open(res_path, encoding="utf-8"))
    desde = os.environ.get("TELEGRAM_DESDE", "").strip()
    if desde and res.get("subido", "") < desde:
        return None
    if res.get("privacy") != "public":
        print(f"{carpeta}: el video no es público todavía")
        return None
    texto = open(os.path.join(carpeta, archivo), encoding="utf-8").read().strip()
    texto = texto.replace("{youtube}", f"https://youtu.be/{res['videoId']}")
    yt = os.environ.get("TELEGRAM_CANAL_YOUTUBE", "").strip()
    if yt and yt.split("//")[-1].lower() not in texto.lower():
        frase = os.environ.get("TELEGRAM_TEXTO_YOUTUBE", "").strip() or "اشترك في القناة:"
        texto += f"\n\n🔔 {frase} {yt}"
    web = os.environ.get("TELEGRAM_WEB", "").strip()
    if web and web.split("//")[-1].rstrip("/").lower() not in texto.lower():
        texto += f"\n🌐 {web}"
    foto = os.path.join(carpeta, "miniatura.png")
    return texto, (foto if os.path.isfile(foto) else None), res.get("subido", "")


def publicar(base):
    destino = canal()
    lista = []
    for d in os.listdir(base):
        p = pendiente(os.path.join(base, d))
        if p:
            lista.append((p[2], d, p[0], p[1]))
    if not lista:
        print("No hay posts pendientes para Telegram.")
        return
    for _, d, texto, foto in sorted(lista):
        ids = []
        if foto and len(texto) <= LIMITE_PIE:
            ids.append(llamar("sendPhoto", {"chat_id": destino, "caption": texto}, ("photo", foto))["message_id"])
        else:
            if foto:
                ids.append(llamar("sendPhoto", {"chat_id": destino}, ("photo", foto))["message_id"])
            ids.append(llamar("sendMessage", {"chat_id": destino, "text": texto})["message_id"])
        with open(os.path.join(base, d, REGISTRO), "w", encoding="utf-8") as f:
            json.dump({"canal": destino, "mensajes": ids, "texto": texto,
                       "fecha": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())},
                      f, ensure_ascii=False, indent=1)
        print(f"{d}: publicado en {destino} (mensajes {ids})")
        time.sleep(3)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "verificar":
        verificar()
    elif len(sys.argv) >= 3 and sys.argv[1] == "publicar":
        publicar(sys.argv[2])
    else:
        sys.exit(__doc__)
