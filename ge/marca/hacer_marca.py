"""Kit de marca de Wall Street auf Deutsch: logo/foto de perfil, banner de YouTube, cabeceras de X y LinkedIn, imagen de bienvenida de Telegram.
Colores del canal (comun.py): noche #0B1A2E, azul marino #13294B, dorado #D4AF37, marfil #F5EBDD, sube #22C55E.
Acento: franja negro-rojo-oro (bandera alemana) bajo el monograma.
uso: python3 hacer_marca.py <carpeta de salida>   (deja profile-800-GE.png también en esta carpeta, que usan los vídeos)"""
import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else HERE; os.makedirs(OUT, exist_ok=True)
FB = os.path.join(HERE, "..", "diario", "fonts", "Tajawal-Bold.ttf"); FM = os.path.join(HERE, "..", "diario", "fonts", "Tajawal-Medium.ttf")
NOCHE, NAVY, ORO, MARFIL, VERDE, MUTED = "#0B1A2E", "#13294B", "#D4AF37", "#F5EBDD", "#22C55E", "#A9B4C8"
DE = ["#111111", "#DD0000", "#FFCE00"]
fnt = lambda p, s: ImageFont.truetype(p, s)


def centrado(d, xy, txt, f, fill):
    l, t, r, b = d.textbbox((0, 0), txt, font=f); d.text((xy[0] - (r - l) / 2 - l, xy[1] - (b - t) / 2 - t), txt, font=f, fill=fill)


def emblema(S, fondo=True):
    """Monograma WS sobre círculo marino con aro dorado, línea de pulso al alza y franja alemana. S = lado en px."""
    k = 4; N = S * k; im = Image.new("RGBA", (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if fondo: d.ellipse((0, 0, N - 1, N - 1), fill=NAVY)
    w = int(N * 0.035); d.ellipse((w, w, N - 1 - w, N - 1 - w), outline=ORO, width=w)
    centrado(d, (N / 2, N * 0.43), "WS", fnt(FB, int(N * 0.40)), MARFIL)
    # línea de pulso que sube (como una gráfica de velas resumida)
    P = [(0.22, 0.66), (0.34, 0.66), (0.40, 0.60), (0.46, 0.70), (0.53, 0.56), (0.60, 0.63), (0.68, 0.58), (0.78, 0.58)]
    d.line([(x * N, y * N) for x, y in P], fill=VERDE, width=int(N * 0.022), joint="curve")
    r = N * 0.022; x, y = P[-1][0] * N, P[-1][1] * N; d.ellipse((x - r, y - r, x + r, y + r), fill=VERDE)
    # franja negro-rojo-oro
    x0, x1, y0, h = N * 0.33, N * 0.67, N * 0.76, N * 0.022
    for i, c in enumerate(DE): d.rectangle((x0, y0 + i * h, x1, y0 + (i + 1) * h), fill=c)
    return im.resize((S, S), Image.LANCZOS)


def lienzo(W, H):
    im = Image.new("RGB", (W, H), NOCHE); d = ImageDraw.Draw(im)
    for i in range(0, H, 2):  # degradado suave hacia el marino
        a = i / H; c = tuple(int(int(NOCHE[j:j + 2], 16) * (1 - a * 0.6) + int(NAVY[j:j + 2], 16) * a * 0.6) for j in (1, 3, 5)); d.line((0, i, W, i), fill=c, width=2)
    return im, d


def cabecera(W, H, safe_w, safe_h, lema=True):
    """Banner con el emblema y el nombre dentro de la zona segura centrada (safe_w x safe_h)."""
    im, d = lienzo(W, H); cx, cy = W / 2, H / 2
    e = int(safe_h * 0.78); em = emblema(e)
    nombre_f = fnt(FB, int(safe_h * 0.30)); lema_f = fnt(FM, int(safe_h * 0.115))
    l, t, r, b = d.textbbox((0, 0), "Wall Street auf Deutsch", font=nombre_f); tw = r - l
    total = e + int(safe_h * 0.10) + tw; x = int(cx - total / 2)
    im.paste(em, (x, int(cy - e / 2)), em)
    tx = x + e + int(safe_h * 0.10)
    d.text((tx - l, cy - safe_h * 0.30 - t), "Wall Street auf Deutsch", font=nombre_f, fill=MARFIL)
    if lema:
        d.text((tx, cy + safe_h * 0.06), "Der Tagesbericht zur US-Börse · Mo–Fr nach Handelsschluss", font=lema_f, fill=ORO)
        d.text((tx, cy + safe_h * 0.22), "S&P 500 · Nasdaq · Dow Jones · Charttechnik", font=lema_f, fill=MUTED)
    return im


for s in (800, 400, 240):
    emblema(s).save(os.path.join(OUT, f"profile-{s}-GE.png"))
cabecera(2560, 1440, 1546, 423).save(os.path.join(OUT, "banner-youtube-2560x1440-GE.png"))
cabecera(1500, 500, 1200, 360).save(os.path.join(OUT, "cabecera-x-1500x500-GE.png"))
cabecera(1128, 191, 1000, 170, lema=False).save(os.path.join(OUT, "cabecera-linkedin-1128x191-GE.png"))
# Telegram: imagen de bienvenida 1280x720
im, d = lienzo(1280, 720); em = emblema(300); im.paste(em, (490, 70), em)
centrado(d, (640, 430), "Wall Street auf Deutsch", fnt(FB, 64), MARFIL)
centrado(d, (640, 510), "Der Tagesbericht zur US-Börse, jeden Handelstag", fnt(FM, 32), ORO)
centrado(d, (640, 570), "Kurse · Nachrichten · Charttechnik · keine Anlageberatung", fnt(FM, 26), MUTED)
im.save(os.path.join(OUT, "bienvenida-telegram-GE.png"))
if os.path.abspath(OUT) != HERE: shutil.copy(os.path.join(OUT, "profile-800-GE.png"), os.path.join(HERE, "profile-800-GE.png"))
print("kit en", OUT)
