"""Imagen 1080x1350 para Instagram con los resultados de una empresa (estilo AIAcciones).

  python3 post_resultados.py spec.json salida.png

spec.json (ejemplo en scripts/instagram/ejemplo-banco-de-chile-2T26.json; el texto del post sigue ejemplo-post-instagram.txt):
  empresa, trimestre ("3T 2026"), titular (una línea corta),
  comparaciones: 1 o 2 de {nombre, antes, ahora, etiqueta_antes, etiqueta_ahora, decimales},
  unidad ("CLP miles de millones"), tiles: 3 de [valor, etiqueta],
  linea (una frase con el consenso u otra cifra clave), fuente.
La variación % de cada comparación se calcula sola. Usa Pillow y numpy; Poppins (OFL) está en fonts/
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
BG, BLUE, GREY, WHITE, SUB, RED = (27, 27, 26), (59, 134, 230), (64, 64, 62), (255, 255, 255), (170, 170, 168), (226, 92, 80)
S, W, H = 2, 1080, 1350


def font(w, size):
    return ImageFont.truetype(f"{F}/Poppins-{w}.ttf", size * S)


def num(v, dec):
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fondo():
    im = Image.new("RGB", (W * S, H * S), BG); d = ImageDraw.Draw(im)
    for x in range(0, W * S, 90 * S): d.line([(x, 0), (x, H * S)], fill=(36, 36, 35), width=S)
    for y in range(0, H * S, 90 * S): d.line([(0, y), (W * S, y)], fill=(36, 36, 35), width=S)
    g = Image.new("RGB", im.size, (0, 0, 0)); cx, cy, r = 540 * S, 520 * S, 450 * S
    ImageDraw.Draw(g).ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 28, 52))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.6))
    return Image.fromarray(np.clip(np.asarray(im, int) + np.asarray(g, int), 0, 255).astype("uint8"))


def main(spec, salida):
    sp = json.load(open(spec, encoding="utf-8"))
    im = fondo(); d = ImageDraw.Draw(im)
    T = lambda x, y, t, f, c, a="la": d.text((x * S, y * S), t, font=f, fill=c, anchor=a)
    # logo
    bw, gap, h = 70 * 0.18, 70 * 0.18 * 0.45, 70
    for i, r in enumerate([0.37, 0.59, 0.49, 0.74, 1.0]):
        x = 105 - (5 * bw + 4 * gap) / 2 + i * (bw + gap)
        d.rounded_rectangle([x * S, (127 - h * r) * S, (x + bw) * S, 127 * S], radius=bw * 0.22 * S, fill=BLUE if i == 4 else GREY)
    f = font("Bold", 34); wa = d.textlength("AI", font=f)
    T(160, 72, "AI", f, BLUE); d.text((160 * S + wa, 72 * S), "Acciones", font=f, fill=WHITE)
    T(980, 78, sp["trimestre"], font("SemiBold", 30), SUB, "ra")
    tam = 78
    while d.textlength(sp["empresa"], font=font("Bold", tam)) > 940 * S: tam -= 4
    T(70, 170, sp["empresa"], font("Bold", tam), WHITE)
    tam = 38
    while d.textlength(sp["titular"], font=font("Medium", tam)) > 940 * S: tam -= 2
    T(70, 275, sp["titular"], font("Medium", tam), BLUE)
    y = 370
    comps = sp["comparaciones"][:2]
    for c in comps:
        a, b, dec = c["antes"], c["ahora"], c.get("decimales", 1)
        var = (b - a) / abs(a) * 100 if a else None
        col = BLUE if var is None or var >= 0 else RED
        T(70, y, c["nombre"], font("SemiBold", 34), WHITE)
        if var is not None:
            T(1010, y, ("+" if var >= 0 else "−") + num(abs(var), 1) + "%", font("Bold", 34), col, "ra")
        mx = max(abs(a), abs(b)) or 1
        for k, (lab, v, cc) in enumerate([(c.get("etiqueta_antes", "Año anterior"), a, GREY), (c.get("etiqueta_ahora", sp["trimestre"]), b, col)]):
            yy = y + 62 + k * 62; L = max(700 * abs(v) / mx, 120)
            T(70, yy + 6, lab, font("Regular", 26), SUB)
            d.rounded_rectangle([200 * S, yy * S, (200 + L) * S, (yy + 44) * S], radius=10 * S, fill=cc)
            T(200 + L - 16, yy + 3, num(v, dec), font("SemiBold", 28), WHITE, "ra")
        y += 210
    T(70, y, sp.get("unidad", ""), font("Regular", 24), SUB)
    y += 70
    for i, (v, k) in enumerate(sp["tiles"][:3]):
        x = 70 + i * 320
        d.rounded_rectangle([x * S, y * S, (x + 300) * S, (y + 180) * S], radius=22 * S, fill=(34, 34, 33), outline=(52, 52, 50), width=2 * S)
        tam = 58
        while d.textlength(v, font=font("Bold", tam)) > 270 * S: tam -= 4
        T(x + 150, y + 35, v, font("Bold", tam), WHITE, "ma"); T(x + 150, y + 120, k, font("Regular", 28), SUB, "ma")
    tam = 32
    while d.textlength(sp.get("linea", ""), font=font("Medium", tam)) > 940 * S: tam -= 2
    T(70, 1090, sp.get("linea", ""), font("Medium", tam), WHITE)
    T(70, 1140, f"Fuente: {sp['fuente']}. No es recomendación de inversión.", font("Regular", 22), SUB)
    f = font("Medium", 34); t = "Análisis completo en aiacciones.cl"; tw = d.textlength(t, font=f)
    d.rounded_rectangle([(540 * S - tw / 2 - 34 * S), 1215 * S, (540 * S + tw / 2 + 34 * S), 1285 * S], radius=35 * S, outline=BLUE, width=3 * S, fill=BG)
    T(540, 1225, t, f, WHITE, "ma")
    im.resize((W, H), Image.LANCZOS).save(salida, optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
