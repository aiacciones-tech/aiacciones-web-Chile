"""Cupo de subidas a YouTube del canal Wall Street auf Deutsch (regla de Daniel, 24-nov-2026: nunca pasar el límite diario).

YouTube deja unas 10 subidas por canal en 24 h; aquí el tope es LIMITE = 9 (una de margen), contadas en ventana móvil de 24 h:
las ya subidas (cola-ge/*/resultado.json con «subido» de las últimas 24 h) más las encoladas y aún no subidas (cola-ge/* sin resultado.json).
Cada tipo de vídeo tiene una prioridad; las de menos prioridad dejan sitio libre para las de más:
  alta  (Tagesbericht y su Short 1, serie de resultados de las 20 grandes): puede llegar a 9
  media (Short del DAX, Charttechnik de los sábados, calendario de los domingos): hasta 7 (deja 2 para el Tagesbericht)
  baja  (Shorts extra del Tagesbericht, cola-espera-GE.yml): hasta 5 (deja sitio para la serie, el DAX y el Tagesbericht)
Uso (desde la raíz de un clon de youtube-cola):  python3 <repo>/ge/cupo.py <prioridad> <n>
Sale con 0 si caben <n> subidas más con esa prioridad; si no, con 1 (y lo explica). `python3 cupo.py <prioridad>` imprime cuántas caben."""
import json, glob, os, sys, datetime as dt

LIMITE = 9
TOPE = {"alta": LIMITE, "media": LIMITE - 2, "baja": LIMITE - 4}


def usadas(base="cola-ge", ahora=None):
    ahora = ahora or dt.datetime.now(dt.timezone.utc)
    n = 0
    for d in glob.glob(os.path.join(base, "*")):
        if not os.path.isdir(d):
            continue
        r = os.path.join(d, "resultado.json")
        if not os.path.exists(r):
            n += os.path.exists(os.path.join(d, "meta.json"))   # encolado, todavía sin subir: cuenta ya
            continue
        try:
            s = dt.datetime.fromisoformat(json.load(open(r))["subido"].replace("Z", "+00:00"))
        except Exception:
            continue
        n += ahora - s < dt.timedelta(hours=24)
    return n


def libres(prioridad, base="cola-ge"):
    return max(0, TOPE[prioridad] - usadas(base))


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "alta"
    if p not in TOPE:
        sys.exit(f"prioridad {p!r}: usa alta, media o baja")
    u, l = usadas(), libres(p)
    if len(sys.argv) > 2:
        k = int(sys.argv[2])
        ok = k <= l
        print(f"subidas a YouTube (GE) en 24 h: {u} de {LIMITE}; prioridad {p}: caben {l}, pide {k} -> {'sí' if ok else 'no'}")
        sys.exit(0 if ok else 1)
    print(l)
