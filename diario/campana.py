"""Campaña de comentarios y suscripción (Daniel, 8-nov-2026): durante 2 semanas, hasta el 22-nov-2026 inclusive,
el video diario y su Short piden un comentario para mejorar el canal e invitan a suscribirse. Después se apaga sola."""
import datetime as dt, re
HASTA = "2026-11-22"
VOZ_VIDEO = "Antes de irte: déjanos un comentario con lo que te gustaría ver o mejorar en este resumen, así mejoramos el canal. Y si te sirve, suscríbete."
PANTALLA_VIDEO = "Déjanos un comentario: ¿qué mejorarías? · Suscríbete a @aiaccioneschile"
VOZ_SHORT = "Coméntanos qué mejorarías y suscríbete."
PANTALLA_SHORT = "Comenta qué mejorarías\ny suscríbete al canal"
DESCRIPCION = "💬 ¿Qué te gustaría ver o mejorar en este resumen diario? Déjanos un comentario: nos ayuda a mejorar el canal. Si te sirve, suscríbete: https://www.youtube.com/@aiaccioneschile?sub_confirmation=1"


def activa(fecha=None):
    """fecha: 'AAAA-MM-DD' (sesión) o texto que la contenga; sin fecha, hoy."""
    m = re.search(r"\d{4}-\d{2}-\d{2}", fecha or "")
    return (m.group(0) if m else dt.date.today().isoformat()) <= HASTA
