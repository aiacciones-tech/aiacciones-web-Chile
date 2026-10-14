# Kit X (Twitter) AIAcciones España: foto 400x400 y cabecera 1500x500
from PIL import Image, ImageDraw, ImageFont
NAVY, ACC, RED, YEL, MUT = (11,30,58), (47,183,163), (198,11,30), (255,196,0), (159,179,204)
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ic=Image.open("../logo-aiacciones-espana-icono.png").convert("RGBA")
pf=Image.new("RGBA",(400,400),NAVY+(255,)); s=300; pf.alpha_composite(ic.resize((s,s),Image.LANCZOS),(50,50)); pf.convert("RGB").save("foto-perfil-400.png")
W,H=1500,500
im=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(im)
# X tapa la parte inferior izquierda con la foto de perfil: el contenido va arriba y a la derecha
lg=Image.open("../logo-aiacciones-espana.png").convert("RGBA"); w=520; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS)
im.paste(lg,(W-w-70,60),lg)
def r(t,f,col,y):
    tw=d.textlength(t,font=f); d.text((W-70-tw,y),t,font=f,fill=col)
r("Resultados del IBEX 35 en vídeo",ImageFont.truetype(B,44),(255,255,255),60+lg.height+40)
r("Un vídeo por empresa, la mañana en que publica",ImageFont.truetype(B,28),ACC,60+lg.height+105)
r("aiacciones.es · YouTube @AIAccionesEspaña",ImageFont.truetype(R,24),MUT,60+lg.height+155)
d.rectangle([0,H-12,W,H-8],fill=RED); d.rectangle([0,H-8,W,H-4],fill=YEL); d.rectangle([0,H-4,W,H],fill=RED)
im.save("cabecera-1500x500.png")
