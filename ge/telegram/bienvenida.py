#!/usr/bin/env python3
"""Publica en el canal de Telegram de Wall Street auf Deutsch la imagen y el mensaje de bienvenida y lo fija.
Lo lanza telegram-GE.yml con modo=bienvenida (secretos TELEGRAM_BOT_TOKEN_GE y TELEGRAM_CHANNEL_GE).
El bot necesita permiso para publicar y editar mensajes (fijar en un canal pide "editar")."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from telegram import llamar, canal, LIMITE_PIE

texto = open(os.path.join(HERE, "bienvenida.txt"), encoding="utf-8").read().strip()
foto = os.path.join(HERE, "bienvenida.png")
destino = canal()
if len(texto) <= LIMITE_PIE:
    fijar = llamar("sendPhoto", {"chat_id": destino, "caption": texto}, ("photo", foto))["message_id"]
else:
    llamar("sendPhoto", {"chat_id": destino}, ("photo", foto))
    fijar = llamar("sendMessage", {"chat_id": destino, "text": texto})["message_id"]
llamar("pinChatMessage", {"chat_id": destino, "message_id": fijar, "disable_notification": True})
print(f"Bienvenida publicada y fijada en {destino} (mensaje {fijar})")
