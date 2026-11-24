"""Enlaces al siguiente vídeo en las descripciones de YouTube de @AIAccionesEspaña (Daniel, 24-nov-2026).

Las pantallas finales y las tarjetas no se pueden poner por la API de YouTube, así que cada descripción lleva enlaces a otros
vídeos y a las listas del canal. Este script resuelve, justo antes de encolar, dos marcadores de meta.json:
  {ultimo:<prefijo>}  el último vídeo ya subido de cola-es/ cuyo nombre empieza por <prefijo> (sin los Shorts) y es anterior
                      al vídeo que se encola, p. ej. {ultimo:bolsa-} = la sesión anterior, {ultimo:curso-at-} = el capítulo anterior.
  {lista:<clave>}     la lista de reproducción <clave> de cola-es/listas.json (la crea scripts/listas-espana.py).
Si un marcador no se puede resolver (aún no hay vídeo anterior o la lista no existe), se borra la línea entera.
{video:<slug>} no se toca: lo resuelve scripts/youtube.py al subir.

  python3 espana/enlaces_cola.py <meta.json> <carpeta cola-es> <slug del vídeo que se encola>
"""
import json, os, re, sys

YT = "https://www.youtube.com/"


def resolver(texto, cola, slug):
    listas = {}
    p = os.path.join(cola, "listas.json")
    if os.path.exists(p):
        listas = json.load(open(p, encoding="utf-8")).get("listas", {})

    def ultimo(pref):
        cands = [d for d in os.listdir(cola) if d.startswith(pref) and not re.search(r"-short\d*$", d) and d != slug
                 and d < slug and os.path.exists(os.path.join(cola, d, "resultado.json"))]
        if not cands:
            return ""
        return json.load(open(os.path.join(cola, max(cands), "resultado.json"), encoding="utf-8")).get("url", "")

    def lista(k):
        i = listas.get(k, {}).get("id")
        return f"{YT}playlist?list={i}" if i else ""

    lineas = []
    for ln in texto.split("\n"):
        vacio = False

        def sub(m):
            nonlocal vacio
            v = ultimo(m.group(2)) if m.group(1) == "ultimo" else lista(m.group(2))
            vacio = vacio or not v
            return v
        ln2 = re.sub(r"\{(ultimo|lista):([\w.-]+)\}", sub, ln)
        if not vacio:
            lineas.append(ln2)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lineas))


if __name__ == "__main__":
    meta_p, cola, slug = sys.argv[1:4]
    m = json.load(open(meta_p, encoding="utf-8"))
    m["description"] = resolver(m.get("description", ""), cola, slug)
    json.dump(m, open(meta_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("enlaces resueltos:", slug)
