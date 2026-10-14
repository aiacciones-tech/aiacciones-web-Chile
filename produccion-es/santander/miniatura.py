from base import *
from PIL import Image
plt.rcParams['text.parse_math']=False
f=plt.figure(figsize=(12.8,7.2),dpi=100); f.patch.set_facecolor(BG)
f.text(0.05,0.70,"SANTANDER · 1S 2026",color=ACC,fontsize=34,weight="bold")
f.text(0.05,0.36,"+15%",color=ACC,fontsize=120,weight="bold")
f.text(0.05,0.26,"beneficio ordinario récord",color=FG,fontsize=32,weight="bold")
f.text(0.60,0.44,"7.328 M€\nBPA +20%",color=ACC2,fontsize=46,weight="bold",linespacing=1.1)
f.text(0.60,0.30,"Eficiencia 42,8%",color=FG,fontsize=30,weight="bold")
f.text(0.05,0.08,"PER 13,6x  |  RoTE 15,6%  |  CET1 14%",color=MUTED,fontsize=28,weight="bold")
f.savefig("miniatura-youtube.png",dpi=100,facecolor=BG); plt.close(f)
im=Image.open("miniatura-youtube.png").convert("RGBA"); lg=Image.open("/mnt/project-files/espana/marca/logo-aiacciones-espana.png")
w=420; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS); im.alpha_composite(lg,(1280-w-30,25)); im.convert("RGB").save("miniatura-youtube.png")
