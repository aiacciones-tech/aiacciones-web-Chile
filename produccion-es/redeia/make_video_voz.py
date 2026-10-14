# Redeia 1S 2026 · video España 1080p con locución (Piper es_ES davefx) y logo AIAcciones España
# Uso: VOICE=.../es_ES-davefx-medium.onnx AUD=scratch python3 make_video_voz.py
import subprocess, os, wave, json, numpy as np
from PIL import Image
from base import *
plt.rcParams['text.parse_math']=False
from narracion import N
DIR="/mnt/project-files/espana/redeia"
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD=os.environ.get("AUD","aud")
SILENT=os.path.join(AUD,"video-silent.mp4")
OUT=f"{DIR}/youtube-redeia-1S26-con-voz.mp4"
SECS=["El titular","Ingresos","Beneficio / BPA","Márgenes y caja","Guidance","Valoración","Qué cambió"]
NS=len(SECS)
EMP=["Redeia"]
PUR="#C38BF2"; COL=[ACC2,ACC,PUR]   # un color fijo por empresa
num=lambda v:f"{v:,.1f}".replace(",","X").replace(".",",").replace("X",".")
pc=lambda v:f"{v:+.1f}%".replace(".",",")

# logo en esquina inferior derecha de cada cuadro
def load_logo(w):
    im=Image.open(LOGO).convert("RGBA"); h=int(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    a=np.asarray(im).astype(np.float32)/255.0; return a[:,:,:3]*255.0,a[:,:,3:4]
LG_RGB,LG_A=load_logo(290)
def with_logo(arr,rgb=LG_RGB,al=LG_A,x=None,y=None):
    h,w=al.shape[:2]; x=W-w-40 if x is None else x; y=H-h-30 if y is None else y
    reg=arr[y:y+h,x:x+w].astype(np.float32); arr[y:y+h,x:x+w]=(reg*(1-al)+rgb*al).astype(np.uint8); return arr

def sec(f,n):
    f.text(0.94,0.92,f"{n}/{NS} · {SECS[n-1].upper()}",color=MUTED,fontsize=18,ha="right",weight="bold")
    for i in range(NS):
        f.patches.append(plt.Rectangle((0.06+i*(0.88/NS),0.975),0.88/NS-0.008,0.008,transform=f.transFigure,color=ACC if i<n else DIM,figure=f))

def base_fig(n,kicker,title,sub):
    f=fig(); header(f,kicker,title); sec(f,n)
    f.text(0.06,0.06,sub,color=MUTED,fontsize=19 if len(sub)<115 else 16,style="italic"); return f

def legend(f,y=0.73,x0=0.06,labels=None,step=0.20):
    for i,(e,c) in enumerate(zip(labels or EMP,COL)):
        f.patches.append(plt.Rectangle((x0+i*step,y),0.014,0.025,transform=f.transFigure,color=c,figure=f))
        f.text(x0+0.02+i*step,y+0.002,e,color=FG,fontsize=21 if not labels else 25,weight="normal" if not labels else "bold")

def side(ax,f,texts,t):
    a=ease((t-0.3)/0.5)
    for yy,d in zip(np.arange(len(texts))[::-1],texts):
        ax.text(1.12,yy,d,transform=ax.get_yaxis_transform(),color=MUTED,fontsize=24,alpha=a,va="center")

def bullets(f,items,t,y0=0.64,step=0.13,col=FG,mark="•",fs=31):
    for i,p in enumerate(items):
        b=ease((t-i*0.15)/0.4)
        if b>0: f.text(0.06,y0-i*step,f"{mark}  "+p,color=col,fontsize=fs,alpha=b)

def table(f,t,cols,rows,xs,y0=0.68,hi=None,step=0.085,fs=26,colors=None):
    a=ease(t/0.6)
    for j,c in enumerate(cols): f.text(xs[j],y0,c,color=MUTED,fontsize=22,alpha=a)
    for i,r in enumerate(rows):
        y=y0-0.10-i*step
        for j,c in enumerate(r):
            col=(colors[i] if (colors and j==0) else (ACC if i==hi else FG))
            f.text(xs[j],y,c,color=col,fontsize=fs,weight="bold" if (j==0 or i==hi) else "normal",alpha=a)

def gbars(ax,groups,series,t,fmt,ymax=None,lab_fs=20):
    """series: lista por empresa de valores por grupo"""
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    n=len(series); x=np.arange(len(groups)); w=0.8/n; e=ease(t)
    allv=[v for s in series for v in s]; top=ymax or max(allv)*1.22; lo=min(0,min(allv)*1.3)
    for i,s in enumerate(series):
        ax.bar(x+(i-(n-1)/2)*w,[v*e for v in s],w*0.92,color=COL[i])
        if t>=0.6:
            for xx,v in zip(x,s): ax.text(xx+(i-(n-1)/2)*w,(v*e if v>=0 else 0)+top*0.015,fmt(v),ha="center",color=FG,fontsize=lab_fs,weight="bold")
    ax.set_xticks(x,groups); ax.tick_params(colors=MUTED,labelsize=22,length=0); ax.set_yticks([]); ax.set_ylim(lo,top)
    if lo<0: ax.axhline(0,color=DIM,lw=1.5)


FMT=lambda v:f"{v:,.0f}".replace(",",".")
F1=lambda v:f"{v:,.1f}".replace(",","X").replace(".",",").replace("X",".")
def s_title(t):
    f=fig(); a=ease(t/0.6)
    f.text(0.06,0.60,"RESULTADOS 1S 2026 · RED",color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.06,0.47,"Redeia",color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.37,"Beneficio +4%, en línea con el consenso; deuda -465 M€",color=ACC2,fontsize=40,weight="bold",alpha=a)
    f.text(0.06,0.28,"Red Eléctrica, Redinter y Reintel. ¿Cuánto vale hoy la acción?",color=MUTED,fontsize=29,alpha=a)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=90)

def s1a(t):
    f=base_fig(1,"El titular","En línea con lo esperado","M€. Informe del 29-jul-2026. 1S25 calculado a partir de las variaciones publicadas. Consenso: Renta 4 e Investing.com, \"en línea\".")
    table(f,t,["","1S 2026","1S 2025","Var. a/a"],
          [["Ingresos","869,2","811,6","+7,1%"],["EBITDA","672,6","635,7","+5,8%"],["EBIT","422,6","415,9","+1,6%"],["Beneficio neto","280,4","269,6","+4,0%"]],
          [0.06,0.42,0.60,0.78],y0=0.66,step=0.09,fs=30,hi=3)
    return to_arr(f)

def s1b(t):
    f=base_fig(1,"El titular","EBITDA con un efecto contable de 24 M€","Vida útil regulatoria de activos repotenciados: de 40 a 8 años. Subyacente calculado. Sin efecto en el beneficio neto (Investing.com).")
    kpis(f,[("+5,8%","EBITDA\nreportado",ACC),("~+2%","EBITDA sin el\nefecto (calculado)",ACC2),("+4,0%","Beneficio\nneto",ACC)],t,y=0.50)
    return to_arr(f)

def s2a(t):
    f=base_fig(2,"Ingresos","869,2 M€: +7,1%","M€. Transporte y operación en España: 779,6 M€ (+9,1%), por nuevos parámetros de retribución y activos en servicio.")
    ax=f.add_axes([0.10,0.18,0.80,0.50]); bars(ax,["1S 2025 (calculado)","1S 2026"],[811.6,869.2],t,[DIM,ACC],F1,ymax=1050)
    return to_arr(f)

def s2b(t):
    f=base_fig(2,"Ingresos","España tira; fibra e internacional bajan","EBITDA por negocio, M€, 1S26 (Estrategias de Inversión, 29-jul-2026).")
    ax=f.add_axes([0.30,0.18,0.48,0.50]); hbars(ax,["Infraestructura\neléctrica España","Internacional","Fibra óptica\n(Reintel)"],[554.5,57.7,51.1],t,[ACC,ACC2,NEG],F1)
    side(ax,f,["+10%","ligeramente menor","-11,6% (57,8)"],t)
    return to_arr(f)

def s3a(t):
    f=base_fig(3,"Beneficio por acción","BPA ~0,52 € en el semestre","BPA calculado con 540,9 M de acciones (stockanalysis). Consenso de beneficio: \"en línea\" (Renta 4).")
    ax=f.add_axes([0.20,0.18,0.60,0.50]); bars(ax,["1S 2025","1S 2026"],[0.498,0.518],t,[DIM,ACC],lambda v:f"{v:.3f} €".replace(".",","),ymax=0.65)
    return to_arr(f)

def s4a(t):
    f=base_fig(4,"Márgenes","Margen EBITDA 77,4%: -0,9 pp","% sobre ingresos. Márgenes calculados. Gastos operativos +8,9%; personal +11,5%.")
    ax=f.add_axes([0.08,0.18,0.84,0.50]); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    g=["EBITDA","Operativo (EBIT)","Neto"]; v25=[78.3,51.2,33.2]; v26=[77.4,48.6,32.3]; x=np.arange(3); e=ease(t)
    ax.bar(x-0.2,[v*e for v in v25],0.38,color=DIM,label="1S 2025"); ax.bar(x+0.2,[v*e for v in v26],0.38,color=ACC,label="1S 2026")
    if t>=0.6:
        for xx,a_,b_ in zip(x,v25,v26):
            ax.text(xx-0.2,a_*e+1.5,f"{a_:.1f}%".replace(".",","),ha="center",color=MUTED,fontsize=22,weight="bold"); ax.text(xx+0.2,b_*e+1.5,f"{b_:.1f}%".replace(".",","),ha="center",color=FG,fontsize=22,weight="bold")
    ax.set_xticks(x,g); ax.tick_params(colors=MUTED,labelsize=24,length=0); ax.set_yticks([]); ax.set_ylim(0,95)
    ax.legend(frameon=False,labelcolor=FG,fontsize=20,ncol=2,loc="upper center",bbox_to_anchor=(0.5,1.12))
    return to_arr(f)

def s4b(t):
    f=base_fig(4,"Inversión y caja","Inversión 657 M€: +9%","M€, 1S26. 551 M€ a la red de transporte. FCF yield 12 meses: stockanalysis (oct-2026).")
    kpis(f,[("657","Inversión total, M€\n(+9%)",ACC2),("631","Red Eléctrica, M€\n(+11,8%)",ACC),("64","Salto de Chira, M€",ACC),("-6,8%","FCF yield\n12 meses",NEG)],t,y=0.50)
    return to_arr(f)

def s4c(t):
    f=base_fig(4,"Deuda","Deuda neta 5.009 M€: -465 M€","Jun-2026 vs dic-2025. Híbrido 500 M€ (abril) y subvenciones 158 + 154 M€. Deuda/EBITDA calculado con EBITDA 12 m ~1.295 M€.")
    kpis(f,[("5.009","Deuda neta, M€\n(-465 vs dic)",ACC),("~3,9x","Deuda neta /\nEBITDA (calculado)",FG),("2,35%","Coste medio\n(2,20%)",NEG),("81%","A tipo fijo;\n100% largo plazo",FG)],t,y=0.50)
    return to_arr(f)

def s5(t):
    f=base_fig(5,"Guidance","Guía 2026 en camino","Guías: Bankinter Análisis (29-abr-2026) y plan 2026-2029 (Merca2, 27-feb-2026). Apagón: nota de 29-jul-2026.")
    items=["Beneficio neto 2026 ~510 M€: el 1S ya suma el 55% (calculado)","EBITDA 2026 superior a 1.250 M€ (sin el efecto contable)","Plan 2026-2029: 6.500 M€ de inversión (6.000 en redes en España)","Dividendo: +2% anual hasta 0,87 € en 2029 (0,80 € con cargo a 2025)","Apagón: sin provisiones; alegaciones al expediente de la CNMC"]
    bullets(f,items,t,y0=0.68,step=0.095,fs=28)
    return to_arr(f)

def s6a(t):
    f=base_fig(6,"Valoración","16,6 veces beneficio, EV/EBITDA 11,3x","Acción 14,80 € (2-oct-2026); capitalización ~8.000 M€ (calculado). Múltiplos: stockanalysis (12 meses y forward).")
    kpis(f,[("16,6x","PER 12 meses",FG),("15,6x","PER forward",FG),("11,3x","EV / EBITDA",FG),("-6,8%","FCF yield",FG),("5,4%","Rentab. dividendo",FG)],t,y=0.50)
    return to_arr(f)

def s6b(t):
    f=base_fig(6,"Valoración","Frente a su historia","Múltiplos a cierre de cada año y actual (oct-2026): stockanalysis. Solo datos, sin juicio de valor.")
    table(f,t,["","2023","2024","2025","Actual"],
          [["PER","11,7x","25,4x","16,8x","16,6x"],["EV/EBITDA","10,4x","13,9x","13,3x","11,3x"],["Rentab. dividendo","7,6%","5,3%","5,5%","5,4%"]],
          [0.06,0.36,0.51,0.66,0.81],y0=0.64,step=0.11,fs=30,hi=None)
    return to_arr(f)

def s7a(t):
    f=base_fig(7,"Qué cambió","3 puntos positivos","")
    bullets(f,["Transporte en España: EBITDA +10%; nueva tasa 6,58% (2026-2031)",
               "Deuda neta -465 M€ en el semestre",
               "Beneficio: ya el 55% de la guía anual"],t,mark="✓")
    return to_arr(f)

def s7b(t):
    f=base_fig(7,"Qué cambió","3 riesgos","")
    bullets(f,["Expediente de la CNMC por el apagón, todavía abierto",
               "Fibra óptica (-11,6%) e internacional pierden peso",
               "Inversión récord: FCF negativo y más deuda en el plan"],t,mark="!")
    return to_arr(f)

def s_fin(t):
    f=fig(); a=ease(t/0.5)
    f.text(0.06,0.55,"Redeia · 1S 2026",color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.06,0.45,"En línea con lo esperado: más inversión y menos deuda.",color=ACC,fontsize=34,alpha=a)
    f.text(0.06,0.37,"Próximo informe (3T26): 28-oct-2026 (estimado) · YouTube: @AIAccionesEspaña",color=MUTED,fontsize=30,alpha=a)
    f.text(0.06,0.07,"Fuentes: Redeia, nota de resultados 1S26 (29-jul-2026); Renta 4, Investing.com, Bankinter Análisis; stockanalysis (precio y múltiplos, 2-oct-2026).\nCifras marcadas como calculadas son cálculos propios. Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado.\nAIAcciones España no tiene posiciones en las empresas analizadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=110)

LGB_RGB,LGB_A=load_logo(560)
SEQ=[s_title,s1a,s1b,s2a,s2b,s3a,s4a,s4b,s4c,s5,s6a,s6b,s7a,s7b,s_fin]
BIG={s_title,s_fin}
def frame(fn,t):
    arr=fn(t); return arr if fn in BIG else with_logo(arr)

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="preview":
        for fn in SEQ: Image.fromarray(frame(fn,1.0)).save(os.path.join(AUD,"prev_"+fn.__name__+".png"))
        sys.exit()
    # Locución fluida (ver memoria voz-fluida-piper)
    os.makedirs(AUD,exist_ok=True)
    TTS=["--length-scale","0.97","--noise-scale","0.55","--noise-w-scale","0.6","--sentence-silence","0.1"]
    LEAD,TAIL=0.12,0.45
    for fn in SEQ:
        p=os.path.join(AUD,fn.__name__+".wav")
        if not os.path.exists(p):
            subprocess.run(["python3","-m","piper","-m",VOICE,"-f",p]+TTS,input=(N[fn.__name__]+"\n").encode(),check=True)
    clips=[]
    for fn in SEQ:
        w=wave.open(os.path.join(AUD,fn.__name__+".wav")); sr=w.getframerate()
        a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)
        nz=np.where(np.abs(a)>300)[0]; a=a[max(nz[0]-int(0.03*sr),0):nz[-1]+int(0.08*sr)]
        f_in,f_out=int(0.015*sr),int(0.06*sr); a[:f_in]*=np.linspace(0,1,f_in); a[-f_out:]*=np.linspace(1,0,f_out)
        clips.append(a)
    durs=[LEAD+len(a)/sr+TAIL for a in clips]
    durs[0]+=0.4; durs[-1]+=1.5
    ANIM=30; XF=8; ff=imageio_ffmpeg.get_ffmpeg_exe()
    proc=subprocess.Popen([ff,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
       "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-preset","medium",SILENT],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    t0=0; times=[]; audio=[]
    for j,(fn,dur,a) in enumerate(zip(SEQ,durs,clips)):
        total=int(round(dur*FPS)); last=None
        nxt=frame(SEQ[j+1],0).astype(np.float32) if j+1<len(SEQ) else np.zeros((H,W,3),np.float32)+np.array([int(BG[i:i+2],16) for i in (1,3,5)],np.float32)
        for k in range(total):
            if k<ANIM: last=frame(fn,k/(ANIM-1))
            fr=last.astype(np.float32)
            if k>=total-XF: al=(total-k)/(XF+1); fr=fr*al+nxt*(1-al)
            proc.stdin.write(fr.astype(np.uint8).tobytes())
        n=int(round(total/FPS*sr)); seg=np.zeros(n,np.float32); st=int((LEAD+(0.4 if j==0 else 0))*sr); seg[st:st+len(a)]=a[:n-st]
        audio.append(seg)
        times.append((fn.__name__,round(t0,2))); t0+=total/FPS; print(fn.__name__,round(t0,1),flush=True)
    proc.stdin.close(); proc.wait()
    full=np.clip(np.concatenate(audio),-32768,32767).astype(np.int16)
    w=wave.open(os.path.join(AUD,"full.wav"),"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(full.tobytes()); w.close()
    AF="highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250,loudnorm=I=-16:TP=-1.5:LRA=9"
    subprocess.run([ff,"-y","-i",SILENT,"-i",os.path.join(AUD,"full.wav"),"-af",AF,"-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-shortest","-movflags","+faststart",OUT],check=True,stderr=subprocess.DEVNULL)
    json.dump(times,open(os.path.join(AUD,"times.json"),"w")); print("done",t0)
