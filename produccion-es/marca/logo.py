# Logo "AIAcciones España" · variante del logo de Chile (marca/logo.py): ESPAÑA en vez de CHILE,
# franja roja-amarilla-roja en vez de la barra roja y sin la estrella.
# Uso: python3 logo.py  -> logo-aiacciones-espana.png, logo-aiacciones-espana-fondo-claro.png, logo-aiacciones-espana-icono.png
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
ACC="#2FB7A3"; ACC2="#4C8DF0"; RED="#C60B1E"; YEL="#FFC400"; WHITE="#FFFFFF"; NAVY="#0B1E3A"

def icon(ax):
    ax.add_patch(FancyBboxPatch((0.04,0.04),0.92,0.92,boxstyle="round,pad=0,rounding_size=0.2",fc=NAVY,ec=ACC,lw=6))
    for i,(h,c) in enumerate([(0.24,ACC2),(0.38,ACC2),(0.54,ACC)]):
        ax.add_patch(FancyBboxPatch((0.20+i*0.21,0.18),0.14,h,boxstyle="round,pad=0,rounding_size=0.03",fc=c,ec="none"))
    ax.plot([0.20,0.40,0.56,0.80],[0.50,0.62,0.58,0.82],color=WHITE,lw=7,solid_capstyle="round")
    ax.add_patch(Polygon([[0.84,0.88],[0.70,0.85],[0.81,0.74]],closed=True,fc=WHITE))
    for y,h,c in [(0.84,0.03,RED),(0.78,0.06,YEL),(0.75,0.03,RED)]:   # banderita de España
        ax.add_patch(plt.Rectangle((0.17,y),0.18,h,fc=c,ec="none"))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")

def text(f,x0,dark=False):
    fg=NAVY if dark else WHITE
    r=f.canvas.get_renderer()
    t1=f.text(x0,0.44,"AI",color=ACC,fontsize=84,weight="bold",family="DejaVu Sans")
    x1=t1.get_window_extent(r).x1/f.bbox.width
    t2=f.text(x1+0.004,0.44,"Acciones",color=fg,fontsize=84,weight="bold",family="DejaVu Sans")
    xe=t2.get_window_extent(r).x1/f.bbox.width
    t3=f.text(x0+0.004,0.10,"E S P A Ñ A",color=ACC2,fontsize=40,weight="bold",family="DejaVu Sans")
    x3=t3.get_window_extent(r).x1/f.bbox.width
    w=xe-x3-0.02
    for y,h,c in [(0.19,0.012,RED),(0.15,0.04,YEL),(0.138,0.012,RED)]:
        f.patches.append(plt.Rectangle((x3+0.02,y),w,h,transform=f.transFigure,color=c,figure=f))

for name,dark in [("logo-aiacciones-espana.png",False),("logo-aiacciones-espana-fondo-claro.png",True)]:
    f=plt.figure(figsize=(12,3.6),dpi=100); f.patch.set_alpha(0)
    icon(f.add_axes([0.01,0.03,0.282,0.94])); text(f,0.30,dark)
    f.savefig(name,dpi=100,transparent=True); plt.close(f)
f=plt.figure(figsize=(5.12,5.12),dpi=100); f.patch.set_alpha(0); icon(f.add_axes([0,0,1,1])); f.savefig("logo-aiacciones-espana-icono.png",transparent=True)
from PIL import Image
for n in ["logo-aiacciones-espana.png","logo-aiacciones-espana-fondo-claro.png","logo-aiacciones-espana-icono.png"]:
    im=Image.open(n); l,t,r,b=im.getbbox(); im.crop((max(l-12,0),max(t-12,0),min(r+12,im.width),min(b+12,im.height))).save(n)
