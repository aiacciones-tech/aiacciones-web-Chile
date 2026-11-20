"""Piezas comunes de la serie semanal de análisis fundamental en árabe de Nabd Wall Street (nabd/fundamental/).
Reutiliza la marca, la fuente, el texto RTL, la locución frase a frase (Azure ar-SA-HamedNeural con VOZ_DIR, Piper de respaldo)
y el render con capa de subtítulos de nabd/diario/comun.py. Las frases y sus claves son las de nabd/diario/voz_frases.py,
las mismas que usa voz-Nabd.yml para pedir la voz a Azure."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *  # noqa: F401,F403  (BG, FG, GOLD, TEAL, NEG, MUTED, DIM, BLUE, ar, fig, to_arr, load_logo, with_logo, clean, ease, LOGO, CANAL, voz_frases, tira_texto, pegar, render)
from comun import plt, Image

SERIE = "التحليل الأساسي ببساطة"          # nombre de la serie en pantalla
SERIE_ES = "Análisis fundamental, fácil"
MARCA = "نبض وول ستريت"
NAVY = "#13294B"


def srt(marcas_por_escena, inicios, leads, path):
    """Subtítulos también como archivo .srt (pista aparte para YouTube si se quiere)."""
    ts = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    n, L = 0, []
    for M, t0, ld in zip(marcas_por_escena, inicios, leads):
        for a, b, s in M:
            n += 1; L.append(f"{n}\n{ts(t0 + ld + a)} --> {ts(t0 + ld + b + 0.2)}\n{s}\n")
    open(path, "w").write("\n".join(L))
