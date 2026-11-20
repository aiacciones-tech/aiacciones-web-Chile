"""Locución de una lección de «Análisis técnico, explicado fácil» (serie educativa de @AIAccionesEspaña) partida en frases, para los
subtítulos y la voz frase a frase, y la clave del mp3 de cada frase. Lo usan make_leccion.py, make_short_leccion.py (render) y
voz_edge_leccion.py (workflow educativo-espana.yml): los tres deben partir igual. Sin dependencias pesadas."""
import os, re, json, hashlib, datetime as dt

VOZ = os.environ.get("VOZ_ES", "es-ES-AlvaroNeural")   # la misma voz neuronal que el vídeo diario (voz-espana.yml, Daniel 10-nov-2026)
RATE = os.environ.get("VOZ_RATE", "+0%")
MAX_PALABRAS = 18  # una frase más larga se parte en la coma más cercana a la mitad, para que el subtítulo quepa en dos líneas

# Llamada a comentar y suscribirse (Daniel, 8-nov-2026): solo en lo que se publique hasta el 22-nov-2026 incluido.
CTA_HASTA = "2026-11-22"
CTA_VOZ = "Déjanos en los comentarios qué te ha parecido y qué concepto quieres que expliquemos, y suscríbete al canal."
CTA_VOZ_CORTA = "Déjanos tu comentario y suscríbete."


def cta(VJ):
    return VJ.get("publicacion", dt.date.today().isoformat()) <= CTA_HASTA


_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince",
      "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco",
      "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
_D = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa"}
_C = {100: "ciento", 200: "doscientos", 300: "trescientos", 400: "cuatrocientos", 500: "quinientos", 600: "seiscientos", 700: "setecientos",
      800: "ochocientos", 900: "novecientos"}


def palabras(n):
    """Entero en palabras (español de España), para la voz: 2025 → «dos mil veinticinco»."""
    if n < 30: return _U[n]
    if n < 100: return _D[n // 10 * 10] + ("" if n % 10 == 0 else " y " + _U[n % 10])
    if n < 1000: return "cien" if n == 100 else _C[n // 100 * 100] + ("" if n % 100 == 0 else " " + palabras(n % 100))
    if n < 1_000_000:
        m, r = divmod(n, 1000); pre = "mil" if m == 1 else re.sub(r"(veinti)?uno$", lambda g: "veintiún" if g.group(1) else "un", palabras(m))+ " mil"
        return pre + ("" if r == 0 else " " + palabras(r))
    m = n // 1_000_000; r = n % 1_000_000
    return ("un millón" if m == 1 else re.sub(r"(veinti)?uno$", lambda g: "veintiún" if g.group(1) else "un", palabras(m)) + " millones") + ("" if r == 0 else " " + palabras(r))


def hablar(x):
    """Texto que se manda a la voz: las cifras escritas con dígitos (como en los subtítulos) pasan a palabras.
    «55,66» → «cincuenta y cinco coma sesenta y seis»; «19.186» → «diecinueve mil ciento ochenta y seis»; «%» → «por ciento».
    Para el femenino («doscientas sesiones», «una sesión») escribe el número con letras en el guion."""
    def dec(m):
        ent = palabras(int(m.group(1).replace(".", "")))
        if not m.group(2): return ent
        d = m.group(2)
        return ent + " coma " + ("cero " * (len(d) - len(d.lstrip("0")))) + (palabras(int(d)) if d.strip("0") else "")
    x = re.sub(r"(\d+(?:\.\d{3})*|\d+)(?:,(\d+))?", dec, x)
    return x.replace("%", " por ciento").replace(" ,", ",").replace("  ", " ").strip()


def frases(texto):
    out = []
    for f in re.split(r"(?<=[.!?])\s+", " ".join(str(texto).split())):
        f = f.strip()
        if not f: continue
        pend = [f]
        while pend:
            x = pend.pop(0); w = x.split()
            if len(w) <= MAX_PALABRAS: out.append(x); continue
            comas = [i for i, p in enumerate(w[:-1]) if p.endswith((",", ";", ":")) and 3 <= i < len(w) - 3]
            i = min(comas, key=lambda i: abs(i - len(w) / 2)) if comas else len(w) // 2
            pend[:0] = [" ".join(w[:i + 1]), " ".join(w[i + 1:])]
    return out


def clave(frase):
    return hashlib.sha1((VOZ + "|" + RATE + "|" + " ".join(str(frase).split())).encode()).hexdigest()[:16]


def textos(carpeta):
    """Todas las frases de la lección (escenas del vídeo y del Short en video.json, y la llamada a comentar si toca), sin repetir."""
    VJ = json.load(open(os.path.join(carpeta, "video.json")))
    T = [e["voz"] for e in VJ.get("escenas", []) if e.get("voz")] + [e["voz"] for e in VJ.get("short", []) if e.get("voz")]
    if cta(VJ): T += [CTA_VOZ, CTA_VOZ_CORTA]
    F, vistos = [], set()
    for t in T:
        for x in frases(t):
            if clave(x) not in vistos: vistos.add(clave(x)); F.append(x)
    return F
