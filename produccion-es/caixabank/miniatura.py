from base import *
from PIL import Image
plt.rcParams['text.parse_math']=False
f=plt.figure(figsize=(12.8,7.2),dpi=100); f.patch.set_facecolor(BG)
f.text(0.05,0.70,"CAIXABANK · 1S 2026",color=ACC,fontsize=34,weight="bold")
f.text(0.05,0.36,"3.203 M€",color=ACC,fontsize=110,weight="bold")
f.text(0.05,0.26,"beneficio neto récord (+8,5%)",color=FG,fontsize=32,weight="bold")
f.text(0.66,0.44,"2T: +4,6%\nvs consenso",color=ACC2,fontsize=44,weight="bold",linespacing=1.1)
f.text(0.66,0.30,"Morosidad 1,78%",color=FG,fontsize=30,weight="bold")
f.text(0.05,0.08,"PER 14,7x  |  ROTE 18%",color=MUTED,fontsize=28,weight="bold")
f.savefig("miniatura-youtube.png",dpi=100,facecolor=BG); plt.close(f)
im=Image.open("miniatura-youtube.png").convert("RGBA"); lg=Image.open("/mnt/project-files/espana/marca/logo-aiacciones-espana.png")
w=420; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS); im.alpha_composite(lg,(1280-w-30,25)); im.convert("RGB").save("miniatura-youtube.png")
