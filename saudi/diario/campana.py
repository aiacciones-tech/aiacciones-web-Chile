"""Campaña temporal de @SaudiArabiaAIStocks: pedir comentarios (para mejorar el canal) y suscripciones en cada video.
Pedido de Daniel (8-nov-2026): durante 2 semanas, hasta el 22-nov-2026 inclusive (hora de Riad). Después se apaga sola:
`activa()` devuelve False y los videos, descripciones y posts vuelven a ser como antes, sin tocar nada.
Para alargarla, cambia HASTA. Para forzarla en una prueba: CTA_CAMPANA=1 (o 0 para apagarla)."""
import os, datetime as dt

HASTA = dt.date(2026, 11, 22)
RIAD = dt.timezone(dt.timedelta(hours=3))

# Locución (se lee en la tarjeta final del video largo; en el Short va la corta, al final de la última escena)
VOZ = "قبل أن تغادر، نريد رأيك: اكتب لنا في التعليقات ما الذي نحسّنه في القناة. واشترك وفعّل الجرس ليصلك كل جديد."
VOZ_CORTA = "اكتب لنا في التعليقات كيف نحسّن القناة، واشترك ليصلك كل جديد."
# Pantalla
TITULO = "رأيك يهمنا"
LINEA1 = "اكتب لنا في التعليقات: ما الذي نحسّنه أو نضيفه في القناة؟"
LINEA2 = "اشترك في القناة وفعّل الجرس ليصلك كل جديد"
CORTA1 = "اكتب لنا في التعليقات: كيف نحسّن القناة؟"
CORTA2 = "واشترك ليصلك كل جديد"
# Textos
DESC = "💬 رأيك يهمنا: اكتب لنا في التعليقات ما الذي تحب أن نحسّنه أو نضيفه في القناة.\n🔔 اشترك في القناة وفعّل الجرس ليصلك كل جديد."
POST = "💬 رأيك يهمنا: اكتب لنا في التعليقات ما الذي نحسّنه في القناة، واشترك ليصلك كل جديد."
POST_X = "💬 شاركنا رأيك لنحسّن القناة، واشترك 🔔"


def activa(hoy=None):
    f = os.environ.get("CTA_CAMPANA")
    if f in ("0", "1"):
        return f == "1"
    return (hoy or dt.datetime.now(RIAD).date()) <= HASTA
