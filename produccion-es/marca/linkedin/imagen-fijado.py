# Imagen 1200x627 para el post fijado de presentación (LinkedIn / X)
from PIL import Image, ImageDraw, ImageFont
NAVY, ACC, RED, YEL, MUT = (11,30,58), (47,183,163), (198,11,30), (255,196,0), (159,179,204)
W,H=1200,627
im=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(im)
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
lg=Image.open("../logo-aiacciones-espana.png").convert("RGBA"); w=520; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS)
im.paste(lg,((W-w)//2,50),lg)
y=60+lg.height+30
def c(t,f,col,yy):
    tw=d.textlength(t,font=f); d.text(((W-tw)/2,yy),t,font=f,fill=col)
c("Resultados del IBEX 35 en vídeo",ImageFont.truetype(B,46),(255,255,255),y)
c("Un vídeo por empresa, la mañana en que publica",ImageFont.truetype(B,30),ACC,y+70)
c("Ingresos · Beneficio · Márgenes · Deuda · Guía · Valoración",ImageFont.truetype(R,24),MUT,y+125)
c("YouTube @AIAccionesEspaña",ImageFont.truetype(B,28),(255,255,255),H-95)
c("Contenido informativo. No es recomendación de inversión.",ImageFont.truetype(R,18),MUT,H-52)
d.rectangle([0,H-12,W,H-8],fill=RED); d.rectangle([0,H-8,W,H-4],fill=YEL); d.rectangle([0,H-4,W,H],fill=RED)
im.save("imagen-fijado-1200x627.png")
