# YouTube Short vertical (1080x1920, <60 s) de resultados, con locución Piper fluida y logo AIAcciones España.
# Lee una especificación JSON (ver /mnt/project-files/pehuenche/short-2T26.json) y escribe el mp4 en spec["out"].
# Uso: VOICE=.../es_MX-claude-high.onnx AUD=scratch python3 make_short.py spec.json [preview]
import subprocess, os, sys, wave, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import imageio_ffmpeg
from PIL import Image
plt.rcParams['text.parse_math']=False

W,H,FPS=1080,1920,30
BG="#0B1E3A"; FG="#FFFFFF"; MUTED="#9FB3CC"; ACC="#2FB7A3"; ACC2="#4C8DF0"; NEG="#F2A541"; DIM="#3A5378"
C={"acc":ACC,"acc2":ACC2,"neg":NEG,"fg":FG,"muted":MUTED,"dim":DIM}
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_MX-claude-high/es_MX-claude-high.onnx")
AUD=os.environ.get("AUD","aud")
MAXDUR=59.0
# Zonas seguras de Shorts: arriba ~8% (búsqueda), abajo ~22% (título, canal, suscribirse) y franja derecha (botones).
# El contenido va entre y=0.25 y y=0.90 de la figura; el logo arriba al centro.

def ease(t): t=min(max(t,0),1); return 1-(1-t)**3
def col(c): return C.get(c,c)

def fig():
    f=plt.figure(figsize=(W/100,H/100),dpi=100); f.patch.set_facecolor(BG); return f
def to_arr(f):
    f.canvas.draw(); a=np.asarray(f.canvas.buffer_rgba())[:,:,:3].copy(); plt.close(f); return a

def load_logo(w):
    im=Image.open(LOGO).convert("RGBA"); h=int(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    a=np.asarray(im).astype(np.float32)/255.0; return a[:,:,:3]*255.0,a[:,:,3:4]
LG=load_logo(400); LGB=load_logo(640)
def with_logo(arr,lg=LG,y=170,alpha=1.0):
    rgb,al=lg; al=al*alpha; h,w=al.shape[:2]; x=(W-w)//2
    reg=arr[y:y+h,x:x+w].astype(np.float32); arr[y:y+h,x:x+w]=(reg*(1-al)+rgb*al).astype(np.uint8); return arr

def top(f,S,e):
    f.text(0.07,0.79,f"{S['empresa'].upper()} · {S['trimestre'].upper()}",color=ACC,fontsize=30,weight="bold")
    if "n" in e:
        tot=sum(1 for x in S["escenas"] if "n" in x)
        for i in range(tot):
            f.patches.append(plt.Rectangle((0.07+i*0.075,0.772),0.06,0.006,transform=f.transFigure,color=ACC if i<e["n"] else DIM,figure=f))

def bars(ax,b,t,fmt,hl):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    labels=[x[0] for x in b]; vals=[x[1] for x in b]; e=ease(t)
    # se destaca la barra de la empresa (comparación con pares) o la del trimestre actual (la última)
    colors=[col(hl)]+[DIM]*(len(vals)-1) if labels[0]==S["empresa"] else [DIM]*(len(vals)-1)+[col(hl)]
    y=np.arange(len(vals))[::-1]; ax.barh(y,[v*e for v in vals],color=colors,height=0.6)
    ax.set_yticks(y,labels); ax.tick_params(colors=FG,labelsize=30,length=0); ax.set_xticks([]); ax.set_xlim(0,max(vals)*1.45)
    if t>=0.5:
        for yy,v in zip(y,vals): ax.text(v*e+max(vals)*0.03,yy,fmt.format(v).replace(".",","),va="center",color=FG,fontsize=32,weight="bold")

def s_titulo(e,t):
    f=fig(); a=ease(t/0.5)
    f.text(0.07,0.72,e["kicker"].upper(),color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.07,0.655,e["titulo"],color=FG,fontsize=82,weight="bold",alpha=a)
    f.text(0.07,0.615,e["sub"],color=ACC2,fontsize=34,weight="bold",alpha=a)
    b=ease((t-0.2)/0.5)
    f.text(0.07,0.44,e["big"],color=col(e["color"]),fontsize=e.get("big_fs",230),weight="bold",alpha=b)
    f.text(0.07,0.38,e["big_label"],color=FG,fontsize=44,weight="bold",alpha=b)
    if e.get("pregunta"): f.text(0.07,0.30,e["pregunta"],color=MUTED,fontsize=36,alpha=ease((t-0.4)/0.5),wrap=True)
    return with_logo(to_arr(f),LGB,y=150)

def s_cifra(e,t):
    f=fig(); top(f,S,e); a=ease(t/0.4)
    f.text(0.07,0.70,f"{e['n']}. {e['label']}",color=MUTED,fontsize=44,weight="bold",alpha=a)
    f.text(0.07,0.605,e["big"],color=FG,fontsize=120 if len(e["big"])<9 else 92,weight="bold",alpha=a)
    f.text(0.07,0.555,e["delta"],color=col(e["color"]),fontsize=50,weight="bold",alpha=ease((t-0.15)/0.4))
    if e.get("barras"):
        ax=f.add_axes([0.27,0.31,0.55,0.20]); bars(ax,e["barras"],t,e.get("fmt","{:.1f}"),e["color"])
    if e.get("nota"): f.text(0.07,0.245,e["nota"],color=MUTED,fontsize=32,alpha=ease((t-0.4)/0.5),wrap=True)
    return with_logo(to_arr(f))

def s_kpis(e,t):
    f=fig(); top(f,S,e)
    f.text(0.07,0.70,e["label"],color=MUTED,fontsize=44,weight="bold",alpha=ease(t/0.4))
    for i,(big,lab,c) in enumerate(e["items"]):
        b=ease((t-i*0.15)/0.4); y=0.58-i*0.12
        f.text(0.07,y,big,color=col(c),fontsize=96,weight="bold",alpha=b)
        f.text(0.50,y+0.012,lab,color=FG,fontsize=36,alpha=b)
    if e.get("nota"): f.text(0.07,0.245,e["nota"],color=MUTED,fontsize=30,alpha=ease((t-0.4)/0.5),wrap=True)
    return with_logo(to_arr(f))

def s_fin(e,t):
    f=fig(); a=ease(t/0.5)
    f.text(0.07,0.66,e.get("nombre",f"{S['empresa']} · {S['trimestre']}"),color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.07,0.565,e["titular"],color=ACC,fontsize=46,weight="bold",alpha=a,linespacing=1.3)
    f.text(0.07,0.45,"▶ "+e["cta"],color=FG,fontsize=44,weight="bold",alpha=ease((t-0.2)/0.5))
    f.text(0.07,0.40,"YouTube @AIAccionesEspaña",color=ACC2,fontsize=40,weight="bold",alpha=ease((t-0.2)/0.5))
    f.text(0.07,0.235,S["fuente"]+"\nContenido informativo, no es una\nrecomendación de inversión. Sin posiciones\nen la empresa. Invertir conlleva riesgo.",color=MUTED,fontsize=22,linespacing=1.45,alpha=a)
    return with_logo(to_arr(f),LGB,y=150)

R={"titulo":s_titulo,"cifra":s_cifra,"kpis":s_kpis,"fin":s_fin}
def frame(e,t): return R[e["tipo"]](e,t)

if __name__=="__main__":
    S=json.load(open(sys.argv[1])); E=S["escenas"]; os.makedirs(AUD,exist_ok=True)
    if len(sys.argv)>2 and sys.argv[2]=="preview":
        for i,e in enumerate(E): Image.fromarray(frame(e,1.0)).save(os.path.join(AUD,f"short_prev_{i}.png"))
        sys.exit()
    TTS=["--length-scale",str(S.get("length_scale",0.95)),"--noise-scale","0.55","--noise-w-scale","0.6","--sentence-silence","0.1"]
    LEAD,TAIL=0.10,0.35
    clips=[]
    for i,e in enumerate(E):
        p=os.path.join(AUD,f"short_{i}.wav")
        subprocess.run(["python3","-m","piper","-m",VOICE,"-f",p]+TTS,input=(e["voz"]+"\n").encode(),check=True,stderr=subprocess.DEVNULL)
        w=wave.open(p); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)
        nz=np.where(np.abs(a)>300)[0]; a=a[max(nz[0]-int(0.03*sr),0):nz[-1]+int(0.08*sr)]
        fi,fo=int(0.015*sr),int(0.06*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); clips.append(a)
    durs=[LEAD+len(a)/sr+TAIL for a in clips]; durs[-1]+=1.0
    if sum(durs)>MAXDUR: sys.exit(f"Short demasiado largo: {sum(durs):.1f} s (máx {MAXDUR}). Acorta la voz o sube length_scale a la baja.")
    ANIM=24; XF=6; ff=imageio_ffmpeg.get_ffmpeg_exe(); silent=os.path.join(AUD,"short-silent.mp4")
    proc=subprocess.Popen([ff,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
       "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-preset","medium",silent],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    audio=[]; bgc=np.array([int(BG[i:i+2],16) for i in (1,3,5)],np.float32)
    for j,(e,dur,a) in enumerate(zip(E,durs,clips)):
        total=int(round(dur*FPS)); last=None
        nxt=frame(E[j+1],0).astype(np.float32) if j+1<len(E) else np.zeros((H,W,3),np.float32)+bgc
        for k in range(total):
            if k<ANIM: last=frame(e,k/(ANIM-1))
            fr=last.astype(np.float32)
            if k>=total-XF: al=(total-k)/(XF+1); fr=fr*al+nxt*(1-al)
            proc.stdin.write(fr.astype(np.uint8).tobytes())
        n=int(round(total/FPS*sr)); seg=np.zeros(n,np.float32); st=int(LEAD*sr); seg[st:st+len(a)]=a[:n-st]; audio.append(seg)
    proc.stdin.close(); proc.wait()
    full=np.clip(np.concatenate(audio),-32768,32767).astype(np.int16)
    wf=os.path.join(AUD,"short-full.wav"); w=wave.open(wf,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(full.tobytes()); w.close()
    AF="highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250,loudnorm=I=-14:TP=-1.5:LRA=9"
    subprocess.run([ff,"-y","-i",silent,"-i",wf,"-af",AF,"-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-shortest","-movflags","+faststart",S["out"]],check=True,stderr=subprocess.DEVNULL)
    print("listo",S["out"],round(sum(durs),1),"s")
