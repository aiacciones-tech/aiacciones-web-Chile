"""Campaña de comentarios y suscripción, APAGADA (HASTA en el pasado), igual que en Nabd. Para encenderla, pon una fecha futura en HASTA;
después se apaga sola. Para forzarla en una prueba: CTA_CAMPANA=1 (o 0 para apagarla)."""
import os, datetime as dt
from zoneinfo import ZoneInfo

HASTA = dt.date(2026, 11, 1)
BERLIN = ZoneInfo("Europe/Berlin")

VOZ = "Bevor Sie gehen: Schreiben Sie uns in die Kommentare, was wir verbessern können. Und abonnieren Sie den Kanal mit der Glocke, damit Sie nichts verpassen."
VOZ_CORTA = "Schreiben Sie uns in die Kommentare, was wir verbessern können, und abonnieren Sie den Kanal."
TITULO = "Ihre Meinung zählt"
LINEA1 = "Schreiben Sie uns in die Kommentare: Was sollen wir verbessern oder ergänzen?"
LINEA2 = "Kanal abonnieren und Glocke aktivieren"
CORTA1 = "Was sollen wir verbessern? Ab in die Kommentare!"
CORTA2 = "Und den Kanal abonnieren"
DESC = "💬 Ihre Meinung zählt: Schreiben Sie uns in die Kommentare, was wir verbessern oder ergänzen sollen.\n🔔 Kanal abonnieren und Glocke aktivieren."
POST = "💬 Ihre Meinung zählt: Schreiben Sie uns, was wir verbessern sollen, und abonnieren Sie den Kanal."
POST_X = "💬 Feedback willkommen – und abonnieren 🔔"


def activa(hoy=None):
    f = os.environ.get("CTA_CAMPANA")
    if f in ("0", "1"):
        return f == "1"
    return (hoy or dt.datetime.now(BERLIN).date()) <= HASTA
