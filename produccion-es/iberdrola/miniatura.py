from base import *
from PIL import Image
plt.rcParams['text.parse_math']=False
f=plt.figure(figsize=(12.8,7.2),dpi=100); f.patch.set_facecolor(BG)
f.text(0.05,0.70,"IBERDROLA · 1S 2026",color=ACC,fontsize=34,weight="bold")
f.text(0.05,0.36,"+7,8%",color=ACC,fontsize=150,weight="bold")
f.text(0.05,0.26,"beneficio ajustado",color=FG,fontsize=34,weight="bold")
f.text(0.64,0.44,"Redes\n+13%",color=ACC2,fontsize=60,weight="bold",linespacing=1.1)
f.text(0.64,0.30,"5,5% sobre consenso",color=FG,fontsize=30,weight="bold")
f.text(0.05,0.08,"PER 25,9x  |  Deuda neta 3,5x EBITDA",color=MUTED,fontsize=28,weight="bold")
f.savefig("miniatura-youtube.png",dpi=100,facecolor=BG); plt.close(f)
im=Image.open("miniatura-youtube.png").convert("RGBA"); lg=Image.open("/mnt/project-files/espana/marca/logo-aiacciones-espana.png")
w=420; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS); im.alpha_composite(lg,(1280-w-30,25)); im.convert("RGB").save("miniatura-youtube.png")
