# Banco Santander 1S 2026 · video España 1080p con locución (Piper es_ES davefx) y logo AIAcciones España
# Uso: VOICE=.../es_ES-davefx-medium.onnx AUD=scratch python3 make_video_voz.py
import subprocess, os, wave, json, numpy as np
from PIL import Image
from base import *
plt.rcParams['text.parse_math']=False
from narracion import N
DIR="/mnt/project-files/espana/santander"
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD=os.environ.get("AUD","aud")
SILENT=os.path.join(AUD,"video-silent.mp4")
OUT=f"{DIR}/youtube-santander-1S26-con-voz.mp4"
SECS=["El titular","Ingresos","Beneficio / BPA","Eficiencia y balance","Guidance","Valoración","Qué cambió"]
NS=len(SECS)
EMP=["Banco Santander"]
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
F1=lambda v:f"{v:,.1f}".replace(",","X").replace(".",",").replace("X",".")
def s_title(t):
    f=fig(); a=ease(t/0.6)
    f.text(0.06,0.60,"RESULTADOS 1S 2026 · SAN",color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.06,0.47,"Banco Santander",color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.37,"Beneficio ordinario récord: 7.328 M€ (+15%); 2T en línea",color=ACC2,fontsize=40,weight="bold",alpha=a)
    f.text(0.06,0.28,"España, Brasil, EE. UU., México y Reino Unido. ¿Cuánto vale hoy la acción?",color=MUTED,fontsize=29,alpha=a)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=90)

def s1a(t):
    f=base_fig(1,"El titular","Beneficio ordinario +15%: récord semestral","M€. Nota y presentación de resultados del 22-jul-2026.\nEl atribuido incluye +1.895 M€ por la venta de Polonia y -250 M€ de reestructuración de TSB.")
    table(f,t,["","1S 2026","1S 2025","Var. a/a"],
          [["Margen de intereses","22.711","21.237","+7%"],["Comisiones netas","6.851","6.311","+9%"],["Margen bruto","30.847","28.966","+6%"],["Costes","13.211","13.251","0%"],["Margen neto","17.636","15.715","+12%"],["Dotaciones por insolvencias","6.574","6.058","+9%"],["Beneficio ordinario","7.328","6.377","+15%"],["Beneficio atribuido","8.973","6.833","+31%"]],
          [0.06,0.45,0.62,0.79],y0=0.70,step=0.064,fs=27,hi=6)
    return to_arr(f)

def s1b(t):
    f=base_fig(1,"El titular","2T26: 3.768 M€, en línea con el consenso","Consenso: sondeo de Reuters (3.750 M€) y consenso recopilado por el banco con 10 analistas (3.771 M€; Benzinga, 21-jul-2026).\nMargen de intereses y dotaciones del 2T calculados (1S menos 1T) frente a ese mismo consenso.")
    kpis(f,[("3.768","BN ordinario 2T\nM€ (+17% a/a)",ACC),("≈ 0%","Frente al\nconsenso",ACC2),("+2%","Margen intereses\n2T vs consenso",ACC),("+1%","Dotaciones 2T\nvs consenso",NEG)],t,y=0.50)
    return to_arr(f)

def s2a(t):
    f=base_fig(2,"Ingresos","Margen bruto 30.847 M€: +6%","M€. En un banco, el margen bruto equivale a los ingresos. En euros constantes: margen bruto +6%, intereses +6%, comisiones +7%.")
    ax=f.add_axes([0.30,0.18,0.48,0.50]); hbars(ax,["Margen bruto","Margen de\nintereses","Comisiones\nnetas"],[30847,22711,6851],t,[ACC,ACC2,ACC],FMT)
    side(ax,f,["+6%","+7%","+9%"],t)
    return to_arr(f)

def s2b(t):
    f=base_fig(2,"Ingresos","España lidera; Reino Unido crece con TSB","Beneficio 1S26 en M€ y variación a/a (Infobae y El Español, 22-jul-2026). Reino Unido incluye TSB desde el 1-may-2026.")
    f.text(0.06,0.70,"Por países",color=ACC,fontsize=24,weight="bold")
    f.text(0.55,0.70,"Por negocios",color=ACC,fontsize=24,weight="bold")
    ax=f.add_axes([0.16,0.16,0.27,0.51]); hbars(ax,["España","Brasil","EE. UU.","México","Reino Unido"],[2534,1093,989,897,725],t,[ACC,ACC2,ACC2,ACC2,ACC2],
        lambda v:{2534:"2.534 (+12%)",1093:"1.093 (+10%)",989:"989 (+18%)",897:"897 (+13%)",725:"725 (+30%)"}[v])
    ax.set_xlim(0,2534*1.75); ax.tick_params(labelsize=22)
    ax2=f.add_axes([0.67,0.16,0.20,0.51]); hbars(ax2,["Banca comercial","CIB","Wealth","Openbank","Pagos"],[4124,1742,1083,827,78],t,[ACC,ACC2,ACC2,NEG,DIM],
        lambda v:{4124:"4.124 (+13%)",1742:"1.742 (+18%)",827:"827 (-21%)",1083:"1.083 (+20%)",78:"78 (x5)"}[v])
    ax2.set_xlim(0,4124*1.75); ax2.tick_params(labelsize=22)
    return to_arr(f)

def s3a(t):
    f=base_fig(3,"Beneficio por acción","BPA ordinario +20%, más que el beneficio","Crecimiento oficial (nota de resultados). BPA ~0,51 € calculado con 14.400 M de acciones (stockanalysis).\nBeneficio ordinario: 1T26 3.560 M€ y 2T26 3.768 M€.")
    ax=f.add_axes([0.08,0.23,0.38,0.46]); bars(ax,["Beneficio\nordinario","BPA\nordinario"],[15,20],t,[DIM,ACC],lambda v:f"+{v:.0f}%",ymax=26)
    ax2=f.add_axes([0.54,0.23,0.38,0.46]); bars(ax2,["BN 1T26","BN 2T26"],[3560,3768],t,[DIM,ACC2],lambda v:FMT(v)+" M€",ymax=4700)
    return to_arr(f)

def s4a(t):
    f=base_fig(4,"Eficiencia y rentabilidad","Eficiencia 42,8%; RoTE 15,6%","Eficiencia = costes / margen bruto. RoTE ordinario. Costes en euros constantes (-2% sin TSB). Nota de resultados del 22-jul-2026.")
    kpis(f,[("42,8%","Eficiencia\n(-2,9 pp a/a)",ACC),("15,6%","RoTE ordinario\n(+0,7 pp)",ACC2),("-1%","Costes\n(euros constantes)",ACC)],t,y=0.50)
    return to_arr(f)

def s4b(t):
    f=base_fig(4,"Riesgo y capital","Morosidad a la baja; CET1 del 14%","Morosidad y cobertura a jun-2026 (Bolsamania). Coste del riesgo 1S26. CET1: la compra de TSB restó 55 pb.")
    kpis(f,[("2,93%","Morosidad\n(-7 pb t/t)",ACC),("64%","Cobertura",FG),("1,15%","Coste del riesgo\n(+2 pb; Argentina)",NEG),("14,0%","CET1\n(+1,0 pp a/a)",ACC2)],t,y=0.50)
    return to_arr(f)

def s4c(t):
    f=base_fig(4,"Volumen de negocio","Crédito +9%; recursos +11%","Jun-2026, crecimiento a/a en euros constantes (sin TSB: crédito +5%, recursos +7%). Presentación de resultados del 22-jul-2026.")
    kpis(f,[("1,07 bill.","Crédito bruto, €\n(+9%)",ACC),("1,30 bill.","Depósitos y\nfondos, € (+11%)",ACC),("182 M","Clientes\n(+12 M)",ACC2),("+19%","Valor tangible\npor acción + div.",ACC2)],t,y=0.50)
    return to_arr(f)

def s5(t):
    f=base_fig(5,"Guidance","Objetivos 2026, reiterados","Guía en euros constantes y sin fusiones de 2025-26 (TSB, Webster). Nota y presentación de resultados del 22-jul-2026. 52% calculado.")
    items=["Ingresos: crecimiento de un dígito medio","Costes: a la baja","Beneficio ordinario > 14.101 M€ (2025); 1S26: 7.328 M€ (52%)","CET1 entre el 12% y el 13% (1S26: 14,0%)","Recompras 2025-26: ~9.000 M€, con una nueva de ~1.800 M€"]
    bullets(f,items,t,y0=0.68,step=0.095,fs=28)
    return to_arr(f)

def s6a(t):
    f=base_fig(6,"Valoración","13,6 veces beneficio; 1,5 veces libros","Acción 12,02 € (9-oct-2026); capitalización 173.090 M€. Múltiplos: stockanalysis.\nPrecio / valor tangible 1,91x; las recompras suman otro 3,5% anual.")
    kpis(f,[("13,6x","PER 12 meses",FG),("10,5x","PER forward",FG),("1,49x","Precio / valor\nen libros",FG),("2,1%","Rentab. dividendo",FG)],t,y=0.50)
    return to_arr(f)

def s6b(t):
    f=base_fig(6,"Valoración","Frente a su historia","Múltiplos a cierre de cada año y actual (9-oct-2026): stockanalysis. Solo datos, sin juicio de valor.")
    table(f,t,["","2022","2023","2024","2025","Actual"],
          [["PER","5,1x","5,7x","5,7x","11,0x","13,6x"],["Precio / libros","0,48x","0,58x","0,63x","1,31x","1,49x"],["Rentab. dividendo","4,7%","5,0%","4,9%","2,4%","2,1%"]],
          [0.06,0.36,0.48,0.60,0.72,0.84],y0=0.64,step=0.11,fs=30,hi=None)
    return to_arr(f)

def s7a(t):
    f=base_fig(7,"Qué cambió","3 puntos positivos","")
    bullets(f,["Beneficio ordinario récord (+15%) y BPA +20%",
               "Costes -1% y eficiencia 42,8% (-2,9 pp)",
               "CET1 14,0% y ~9.000 M€ en recompras 2025-26"],t,mark="✓")
    return to_arr(f)

def s7b(t):
    f=base_fig(7,"Qué cambió","3 riesgos","")
    bullets(f,["Dotaciones +9% (Argentina); coste del riesgo 1,15%",
               "Openbank -21%: coches en Reino Unido y EE. UU.",
               "Integración de TSB y Webster: costes y menos capital"],t,mark="!")
    return to_arr(f)

def s_fin(t):
    f=fig(); a=ease(t/0.5)
    f.text(0.06,0.55,"Banco Santander · 1S 2026",color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.06,0.45,"Beneficio ordinario récord, con más ingresos y menos costes.",color=ACC,fontsize=34,alpha=a)
    f.text(0.06,0.37,"Próximo informe (3T26): 28-oct-2026 · YouTube: @AIAccionesEspaña",color=MUTED,fontsize=30,alpha=a)
    f.text(0.06,0.07,"Fuentes: Banco Santander, resultados 1S26 (22-jul-2026); Reuters, Benzinga, Infobae, El Español; stockanalysis (precio y múltiplos, 9-oct-2026).\nCifras marcadas como calculadas son cálculos propios. Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado.\nAIAcciones España no tiene posiciones en las empresas analizadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
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
