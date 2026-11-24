"""Miniatura «cifra grande + logo» de Wall Street auf Deutsch (24-nov-2026, petición de Daniel: «Nvidia +31 %» con logo).
La usan gen_meta.py (Tagesbericht) y ge/serie20/meta_episodio.py. 1280x720, PIL, fuente Tajawal de la marca.

Composición (pensada para verse a 200 px de ancho en el móvil):
  izquierda: etiqueta dorada (programa · fecha), nombre de la empresa, LA CIFRA enorme en verde/rojo/dorado con flecha, y un gancho de 2-5 palabras;
  derecha: el logo de la empresa en un círculo blanco con anillo del color de la cifra (o una insignia con el ticker si no hay logo);
  abajo: dos o tres «chips» de contexto (S&P 500, Nasdaq…). La esquina inferior derecha se deja libre: YouTube pone ahí la duración.
Logos: rama datos-extra-ge (datos-extra-GE.yml, cada domingo), carpeta logos/; se pasa con LOGOS_DIR=<clon>/logos.
Sin logo no falla: dibuja la insignia con el ticker. No se usan caras de personas (derechos de imagen y nada de rostros generados por IA)."""
import json, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FB = os.path.join(HERE, "fonts", "Tajawal-Bold.ttf")
LOGO_CANAL = os.environ.get("LOGO", os.path.join(HERE, "..", "marca", "profile-800-GE.png"))
BG = (11, 26, 46); BG2 = (19, 41, 75); FG = (245, 235, 221); MUTED = (169, 180, 200); GOLD = (212, 175, 55)
COL = {"teal": (34, 197, 94), "neg": (229, 72, 77), "gold": GOLD, "fg": FG, "blue": (125, 183, 240), "muted": MUTED}
W, H = 1280, 720


def color_de(c, cifra=""):
    """'teal' / 'neg' / 'gold' o, si no se da, el signo de la cifra (+ verde, − rojo)."""
    if c: return COL.get(c, GOLD)
    s = str(cifra).strip()
    return COL["teal"] if s.startswith("+") else COL["neg"] if s[:1] in "-−–" else GOLD


def _f(sz): return ImageFont.truetype(FB, sz)


def _ajusta(d, txt, ancho, maxi, mini=28):
    sz = maxi
    while sz > mini and d.textlength(txt, font=_f(sz)) > ancho: sz -= 4
    return _f(sz)


def buscar_logo(ticker, logos_dir=None):
    """PNG del logo para 'NVDA', 'NASDAQ:NVDA' o 'XETR:SAP' en LOGOS_DIR (índice de datos_extra.py), o None."""
    L = logos_dir or os.environ.get("LOGOS_DIR", "")
    if not ticker or not L or not os.path.isdir(L): return None
    t = str(ticker).upper(); corto = t.split(":")[-1]
    idx = {}
    try: idx = json.load(open(os.path.join(L, "indice.json")))["logos"]
    except Exception: pass
    rel = idx.get(t) or next((r for s, r in idx.items() if s.split(":")[-1] == corto and ":" not in t and r.startswith("us/")), None)
    for p in ([rel] if rel else []) + [f"us/{corto}.png", f"de/{corto}.png"]:
        if p and os.path.exists(os.path.join(L, p)): return os.path.join(L, p)
    return None


def _flecha(d, x, y, h, c, arriba):
    w = int(h * 0.9)
    pts = [(x, y + h), (x + w, y + h), (x + w / 2, y)] if arriba else [(x, y), (x + w, y), (x + w / 2, y + h)]
    d.polygon(pts, fill=c); return w


def miniatura(path, etiqueta, nombre, cifra, color=None, gancho="", logo=None, chips=(), insignia=None):
    """etiqueta: «DER TAGESBERICHT · 23.11.2026»; nombre: «Nvidia»; cifra: «+31 %»; gancho: «Huang ist zurück»;
    logo: ticker para buscar el logo; chips: [(«S&P 500», «+4,7 %», 'teal'|'neg'|None)]; insignia: texto si no hay logo (por defecto el ticker)."""
    c = color_de(color, cifra)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(H):   # degradado vertical suave
        k = y / H; d.line([(0, y), (W, y)], fill=tuple(int(BG[i] * (1 - k) + BG2[i] * k * 0.6 + BG[i] * k * 0.4) for i in range(3)))
    cx, cy, R = 1000, 345, 215
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse([cx - R - 90, cy - R - 90, cx + R + 90, cy + R + 90], fill=c + (95,))
    im.paste(glow.filter(ImageFilter.GaussianBlur(70)), (0, 0), glow.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(im)
    # etiqueta dorada
    fe = _ajusta(d, etiqueta, 680, 34, 22); tw = d.textlength(etiqueta, font=fe)
    d.rounded_rectangle([48, 40, 48 + tw + 36, 40 + fe.size + 22], radius=14, fill=GOLD)
    d.text((66, 40 + 11), etiqueta, font=fe, fill=BG)
    # nombre
    fn = _ajusta(d, nombre, 700, 104, 50)
    d.text((48, 120), nombre, font=fn, fill=FG)
    y_c = 120 + fn.size + 12
    # cifra enorme con flecha
    arriba = str(cifra).strip()[:1] == "+"; abajo = str(cifra).strip()[:1] in "-−–"
    fl = 0
    fc = _ajusta(d, cifra, 700 - (130 if (arriba or abajo) else 0), 210, 80)
    if arriba or abajo:   # flecha a la altura real de los dígitos (Tajawal deja mucho aire arriba)
        b = d.textbbox((0, y_c), "0", font=fc); hb = b[3] - b[1]
        fl = _flecha(d, 52, b[1] + int(hb * 0.12), int(hb * 0.76), c, arriba) + 26
    d.text((48 + fl, y_c), cifra, font=fc, fill=c, stroke_width=4, stroke_fill=(6, 14, 26))
    # gancho (hasta 2 líneas)
    if gancho:
        y_g = y_c + int(fc.size * 1.05) + 6
        fg_ = _ajusta(d, gancho, 700, 54, 40)
        if d.textlength(gancho, font=fg_) > 700:
            pal = gancho.split(); l1 = ""
            while pal and d.textlength((l1 + " " + pal[0]).strip(), font=fg_) <= 700: l1 = (l1 + " " + pal.pop(0)).strip()
            lineas = [l1, " ".join(pal)]
        else: lineas = [gancho]
        for i, l in enumerate(lineas[:2]): d.text((48, y_g + i * (fg_.size + 8)), l, font=fg_, fill=GOLD)
    # logo de la empresa (o insignia con el ticker) en círculo blanco con anillo de color
    d.ellipse([cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14], fill=c)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(255, 255, 255))
    lp = buscar_logo(logo)
    if lp:
        lg = Image.open(lp).convert("RGBA").resize((2 * R - 16, 2 * R - 16), Image.LANCZOS)
        m = Image.new("L", lg.size, 0); ImageDraw.Draw(m).ellipse([0, 0, lg.size[0] - 1, lg.size[1] - 1], fill=255)
        a = lg.split()[3]; m = Image.composite(a, Image.new("L", lg.size, 0), m)
        im.paste(lg, (cx - R + 8, cy - R + 8), m)
    else:
        t = insignia or (str(logo).split(":")[-1] if logo else str(nombre).split()[0])[:7]
        d.ellipse([cx - R + 10, cy - R + 10, cx + R - 10, cy + R - 10], fill=BG2)
        ft = _ajusta(d, t, 2 * R - 90, 150, 60)
        d.text((cx, cy), t, font=ft, fill=FG, anchor="mm")
    # chips de contexto
    x = 48; y0 = 622
    for nom, val, cc in list(chips)[:3]:
        fcn = _f(34); fv = _f(38)
        w = d.textlength(nom, font=fcn) + 14 + d.textlength(val, font=fv) + 40
        if x + w > 1060: break
        d.rounded_rectangle([x, y0, x + w, y0 + 64], radius=16, fill=(6, 14, 26), outline=(42, 68, 104), width=2)
        d.text((x + 20, y0 + 32), nom, font=fcn, fill=MUTED, anchor="lm")
        d.text((x + 20 + d.textlength(nom, font=fcn) + 14, y0 + 32), val, font=fv, fill=color_de(cc, val), anchor="lm")
        x += w + 18
    # logo del canal, arriba a la derecha
    lc = Image.open(LOGO_CANAL).convert("RGBA").resize((118, 118), Image.LANCZOS)
    im.paste(lc, (W - 118 - 24, 18), lc)
    im.save(path)
    return path


def corto(p, d=1):
    """'+31,48 %' o 31.48 -> '+31 %' (redondeo para miniatura; d decimales si |v| < 10)."""
    if isinstance(p, str):
        v = float(re.sub(r"[^\d,.\-+−]", "", p).replace("−", "-").replace(".", "").replace(",", "."))
    else: v = float(p)
    s = f"{v:+.0f}" if abs(v) >= 10 else f"{v:+.{d}f}".replace(".", ",")
    return s.replace("-", "−") + " %"


if __name__ == "__main__":   # prueba: python3 miniatura.py <salida.png>
    import sys
    miniatura(sys.argv[1] if len(sys.argv) > 1 else "/tmp/mini.png", "DER TAGESBERICHT · 23.11.2026", "Nvidia", "+31 %",
              gancho="Huang ist zurück", logo="NVDA", chips=[("S&P 500", "+4,7 %", None), ("Nasdaq", "+6,5 %", None)])
