# Kit YouTube @AIAccionesEspaña: foto de perfil 800x800, banner 2560x1440 (zona segura 1546x423), marca de agua 150x150
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
M="/mnt/project-files/espana/marca/"
NAVY=(11,30,58,255); ACC="#2FB7A3"; ACC2="#4C8DF0"; MUTED="#9FB3CC"; RED="#C60B1E"; YEL="#FFC400"

# 1) Foto de perfil: icono centrado sobre fondo azul (YouTube la recorta en círculo)
ic=Image.open(M+"logo-aiacciones-espana-icono.png").convert("RGBA")
pf=Image.new("RGBA",(800,800),NAVY); s=600; pf.alpha_composite(ic.resize((s,s),Image.LANCZOS),((800-s)//2,(800-s)//2))
pf.convert("RGB").save("foto-perfil-800.png")

# 2) Marca de agua: icono 150x150 con fondo transparente
ic.resize((150,150),Image.LANCZOS).save("marca-agua-150.png")

# 3) Banner 2560x1440: todo lo importante dentro del rectángulo central 1546x423
W,H=2560,1440
f=plt.figure(figsize=(W/100,H/100),dpi=100); f.patch.set_facecolor("#0B1E3A")
ax=f.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")
import numpy as np
rng=np.random.default_rng(7)   # fondo: barras tenues a lo ancho (solo decoración, puede recortarse)
for i,x in enumerate(range(0,W,64)):
    h=180+120*np.sin(i/3.0)+rng.integers(0,90)
    ax.add_patch(plt.Rectangle((x+8,0),44,h,color="#13294A"))
x0,y0=(W-1546)/2,(H-423)/2
f.text(0.5,(y0+300)/H,"Resultados de las empresas del IBEX 35",color="white",fontsize=50,weight="bold",ha="center",va="center")
f.text(0.5,(y0+190)/H,"Un vídeo por empresa, la mañana en que publica",color=ACC,fontsize=38,weight="bold",ha="center",va="center")
f.text(0.5,(y0+95)/H,"Ingresos · Beneficio · Márgenes · Deuda · Guía · Valoración",color=MUTED,fontsize=28,ha="center",va="center")
for yy,hh,c in [(y0+36,6,RED),(y0+24,12,YEL),(y0+18,6,RED)]:
    ax.add_patch(plt.Rectangle((W/2-300,yy),600,hh,color=c))
f.savefig("banner-2560x1440.png",dpi=100,facecolor="#0B1E3A"); plt.close(f)
b=Image.open("banner-2560x1440.png").convert("RGBA")
lg=Image.open(M+"logo-aiacciones-espana.png").convert("RGBA"); w=560; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS)
b.alpha_composite(lg,(int(W/2-w/2),int(y0)-lg.height-40))   # logo encima de la zona segura: visible en TV/escritorio
b.convert("RGB").save("banner-2560x1440.png")
# vista de control con la zona segura marcada (no se sube)
c=b.copy(); from PIL import ImageDraw; d=ImageDraw.Draw(c); d.rectangle([x0,y0,x0+1546,y0+423],outline=(255,80,80,255),width=4)
c.convert("RGB").resize((1280,720)).save("banner-control-zona-segura.png")
