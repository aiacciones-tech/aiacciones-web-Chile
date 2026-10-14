# Portada (1128x191) y logo cuadrado (400x400) para la página de LinkedIn de AIAcciones España
from PIL import Image, ImageDraw, ImageFont
NAVY, ACC, RED, YEL = (11, 30, 58), (47, 183, 163), (198, 11, 30), (255, 196, 0)
W, H = 1128, 191
im = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(im)
d.rectangle([0, H - 9, W, H - 6], fill=RED); d.rectangle([0, H - 6, W, H - 3], fill=YEL); d.rectangle([0, H - 3, W, H], fill=RED)
logo = Image.open("../logo-aiacciones-espana.png").convert("RGBA")
lh = 110; logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
# LinkedIn tapa la esquina inferior izquierda con el logo de la página: el contenido va a la derecha
x = W - logo.width - 40
im.paste(logo, (x, 22), logo)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
txt = "Resultados de las empresas del IBEX 35 en vídeo · YouTube @AIAccionesEspaña"
tw = d.textlength(txt, font=f)
d.text((W - tw - 40, 146), txt, font=f, fill=(220, 230, 240))
im.save("portada-linkedin.png")
ic = Image.open("../logo-aiacciones-espana-icono.png").convert("RGBA")
sq = Image.new("RGBA", (400, 400), NAVY + (255,))
ic = ic.resize((340, 340), Image.LANCZOS); sq.alpha_composite(ic, (30, 30))
sq.convert("RGB").save("logo-linkedin-400.png")
