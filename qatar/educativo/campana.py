"""Campaña de comentarios y suscripción de @QatarAIStocks para la serie educativa, con los textos de qatar/diario/comun.py (CTA_*):
pedida por Daniel el 8-nov-2026, hasta el 22-nov-2026 inclusive (hora de Doha). Después `activa()` devuelve False y todo vuelve a ser
como antes sin tocar nada. CTA=1 / CTA=0 la fuerzan (pruebas). Misma interfaz que saudi/diario/campana.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diario"))
from comun import cta_activa, CANAL

VOZ = "قبل أن تغادر، نريد رأيك: اكتب لنا في التعليقات ما الذي نحسّنه في القناة. واشترك وفعّل الجرس ليصلك كل جديد."
VOZ_CORTA = "اكتب لنا في التعليقات كيف نحسّن القناة، واشترك ليصلك كل جديد."
TITULO = "رأيك يهمنا"
LINEA1 = "اكتب لنا في التعليقات: ما الذي نحسّنه أو نضيفه في القناة؟"
LINEA2 = "اشترك في القناة وفعّل الجرس ليصلك كل جديد"
CORTA1 = "اكتب لنا في التعليقات: كيف نحسّن القناة؟"
CORTA2 = "واشترك ليصلك كل جديد"
DESC = "💬 رأيك يهمنا: اكتب لنا في التعليقات ما الذي تحب أن نحسّنه أو نضيفه في القناة، أو السهم الذي تريد أن نشرح عليه الحلقة القادمة.\n🔔 اشترك في القناة وفعّل الجرس ليصلك كل جديد."
POST = "💬 رأيك يهمنا: اكتب لنا في التعليقات ما الذي نحسّنه في القناة، واشترك ليصلك كل جديد."
POST_X = "💬 شاركنا رأيك لنحسّن القناة، واشترك 🔔"


def activa(hoy=None):
    return cta_activa()
