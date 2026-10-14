# BBVA 1S 2026 · video España 1080p con locución (Piper es_ES davefx) y logo AIAcciones España
# Uso: VOICE=.../es_ES-davefx-medium.onnx AUD=scratch python3 make_video_voz.py
import subprocess, os, wave, json, numpy as np
from PIL import Image
from base import *
plt.rcParams['text.parse_math']=False
from narracion import N
DIR="/mnt/project-files/espana/bbva"
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD=os.environ.get("AUD","aud")
SILENT=os.path.join(AUD,"video-silent.mp4")
OUT=f"{DIR}/youtube-bbva-1S26-con-voz.mp4"
SECS=["El titular","Ingresos","Beneficio / BPA","Eficiencia y balance","Guidance","Valoración","Qué cambió"]
NS=len(SECS)
EMP=["BBVA"]
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
    f.text(0.06,0.60,"RESULTADOS 1S 2026 · BBVA",color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.06,0.47,"BBVA",color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.37,"Beneficio récord: 6.051 M€ (+11,1%); 2T sobre el consenso",color=ACC2,fontsize=40,weight="bold",alpha=a)
    f.text(0.06,0.28,"México, España, Turquía y América del Sur. ¿Cuánto vale hoy la acción?",color=MUTED,fontsize=29,alpha=a)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=90)

def s1a(t):
    f=base_fig(1,"El titular","Beneficio +11,1%: récord semestral","M€ y variación a/a en euros corrientes. Informe de resultados enero-junio 2026 (30-jul-2026).")
    table(f,t,["","1S 2026","1S 2025","Var. a/a"],
          [["Margen de intereses","15.164","12.607","+20,3%"],["Comisiones netas","4.572","4.010","+14,0%"],["Margen bruto","21.159","18.034","+17,3%"],["Gastos de explotación","8.000","6.787","+17,9%"],["Deterioro de activos fin.","3.497","2.761","+26,6%"],["Beneficio atribuido","6.051","5.447","+11,1%"]],
          [0.06,0.45,0.62,0.79],y0=0.68,step=0.075,fs=28,hi=5)
    return to_arr(f)

def s1b(t):
    f=base_fig(1,"El titular","2T26: 3.062 M€, por encima del consenso","Consenso de BBVA (19 analistas) y Bloomberg vía Benzinga; % calculados. Jefferies y Renta 4 vía Merca2 (30/31-jul-2026).")
    kpis(f,[("+4,5%","BN 2T vs consenso\nBBVA (2.931 M€)",ACC),("+2,6%","BN 2T vs\nBloomberg (2.984)",ACC),("~+4%","Sorpresa según\nJefferies",ACC2),(">+4%","Subida intradía\n30-jul-2026",ACC2)],t,y=0.50)
    return to_arr(f)

def s2a(t):
    f=base_fig(2,"Ingresos","Margen bruto 21.159 M€: +17,3%","M€, euros corrientes. En un banco, el margen bruto equivale a los ingresos. Sin efecto divisa: MI +18,8%; comisiones +15,8%.")
    ax=f.add_axes([0.30,0.18,0.48,0.50]); hbars(ax,["Margen bruto","Margen de\nintereses","Comisiones\nnetas"],[21159,15164,4572],t,[ACC,ACC2,ACC],FMT)
    side(ax,f,["+17,3%","+20,3%","+14,0%"],t)
    return to_arr(f)

def s2b(t):
    f=base_fig(2,"Ingresos","México, primer motor; España, +2,3%","Beneficio atribuido por área, M€, 1S26; variación sin efecto divisa. Centro Corporativo: -696 M€.")
    ax=f.add_axes([0.30,0.15,0.48,0.56]); hbars(ax,["México","España","América\ndel Sur","Turquía","Resto de\nnegocios"],[2979,2172,556,532,508],t,[ACC,ACC2,ACC,ACC,DIM],FMT)
    side(ax,f,["+8,2%","+2,3%","+33,6%","+29,1%","+60,0%"],t)
    return to_arr(f)

def s3a(t):
    f=base_fig(3,"Beneficio por acción","BPA 1,04 €: +14,1%","BPA publicado por BBVA; 1S25 calculado con la variación publicada. Trimestres: 1T26 2.989 M€ y 2T26 3.062 M€.")
    ax=f.add_axes([0.08,0.18,0.38,0.50]); bars(ax,["1S 2025","1S 2026"],[0.911,1.04],t,[DIM,ACC],lambda v:f"{v:.2f} €".replace(".",","),ymax=1.30)
    ax2=f.add_axes([0.54,0.18,0.38,0.50]); bars(ax2,["BN 1T26","BN 2T26"],[2989,3062],t,[DIM,ACC2],lambda v:f"{v:,.0f} M€".replace(",","."),ymax=3800)
    return to_arr(f)

def s4a(t):
    f=base_fig(4,"Eficiencia y rentabilidad","Eficiencia 37,8%; ROTE 22,2%","Eficiencia = gastos / margen bruto. ROE y ROTE: informe de resultados 1S26. ROTE 22,2%: máximo histórico.")
    kpis(f,[("37,8%","Eficiencia\n(1S25: 37,6%)",FG),("21,1%","ROE\n(1S25: 19,5%)",ACC2),("22,2%","ROTE\n(1S25: 20,4%)",ACC)],t,y=0.50)
    return to_arr(f)

def s4b(t):
    f=base_fig(4,"Riesgo y capital","Menos morosidad; capital en 12,90%","Mora y cobertura a jun-2026. Coste del riesgo acumulado. CET1 fully loaded; requerimiento 8,98%; objetivo 11,5-12%.")
    kpis(f,[("2,6%","Morosidad\n(jun-25: 2,9%)",ACC),("85%","Cobertura\n(jun-25: 81%)",FG),("1,43%","Coste del riesgo\n(1S25: 1,32%)",NEG),("12,90%","CET1\n(req. 8,98%)",ACC2)],t,y=0.50)
    return to_arr(f)

def s4c(t):
    f=base_fig(4,"Volumen de negocio","Préstamos +10,6% en el semestre","Jun-2026 vs dic-2025 (préstamos 509.424 M€; depósitos 532.981 M€). Crédito 12 meses: a tipos constantes.")
    kpis(f,[("509,4","Préstamos, miles\nde M€ (+10,6%)",ACC),("533,0","Depósitos, miles\nde M€ (+6,1%)",ACC),("243,8","Fuera de balance,\nmiles de M€ (+8,7%)",ACC2),("+17,7%","Crédito 12 meses\n(sin divisa)",ACC2)],t,y=0.50)
    return to_arr(f)

def s5(t):
    f=base_fig(5,"Guidance","Guía 2026","Guía según la conferencia de resultados (Investing.com, 30-jul-2026) y Merca2. Objetivo 2025-2028: plan del banco.")
    items=["ROTE 2026 ~21% (antes ~20%; 1S26: 22,2%)","España: margen de intereses +1 dígito bajo-medio; eficiencia <35%","México: crédito ~+10%; margen de intereses +1 dígito alto","Turquía: coste del riesgo ~220 pb","48.000 M€ de beneficio acumulado en 2025-2028"]
    bullets(f,items,t,y0=0.68,step=0.095,fs=28)
    return to_arr(f)

def s6a(t):
    f=base_fig(6,"Valoración","12,2 veces beneficio; 2 veces libros","Acción 23,11 € (9-oct-2026); capitalización 127.090 M€. Múltiplos: stockanalysis. Dividendo a cuenta 2026: 0,37 € (+16%).")
    kpis(f,[("12,2x","PER 12 meses",FG),("10,4x","PER forward",FG),("1,99x","Precio / valor\nen libros",FG),("4,0%","Rentab. dividendo",FG)],t,y=0.50)
    return to_arr(f)

def s6b(t):
    f=base_fig(6,"Valoración","Frente a su historia","Múltiplos a cierre de cada año y actual (oct-2026): stockanalysis. Solo datos, sin juicio de valor.")
    table(f,t,["","2022","2023","2024","2025","Actual"],
          [["PER","5,5x","6,3x","5,6x","11,3x","12,2x"],["Precio / libros","0,66x","0,87x","0,91x","1,85x","1,99x"],["Rentab. dividendo","9,2%","7,6%","8,0%","4,7%","4,0%"]],
          [0.06,0.36,0.48,0.60,0.72,0.84],y0=0.64,step=0.11,fs=30,hi=None)
    return to_arr(f)

def s7a(t):
    f=base_fig(7,"Qué cambió","3 puntos positivos","")
    bullets(f,["2T récord (3.062 M€), un 4,5% sobre el consenso de BBVA",
               "ROTE 22,2% y guía del año elevada a ~21%",
               "Mora 2,6%; recompra de 2.000 M€ y dividendo a cuenta +16%"],t,mark="✓")
    return to_arr(f)

def s7b(t):
    f=base_fig(7,"Qué cambió","3 riesgos","")
    bullets(f,["Deterioros +26,6% y gastos +17,9%, por encima del margen bruto",
               "España: beneficio solo +2,3%",
               "Peso de emergentes y divisas; Turquía, coste del riesgo ~220 pb"],t,mark="!")
    return to_arr(f)

def s_fin(t):
    f=fig(); a=ease(t/0.5)
    f.text(0.06,0.55,"BBVA · 1S 2026",color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.06,0.45,"Beneficio récord, con México como motor y ROTE en máximos.",color=ACC,fontsize=34,alpha=a)
    f.text(0.06,0.37,"Próximo informe (3T26): 29-oct-2026 · YouTube: @AIAccionesEspaña",color=MUTED,fontsize=30,alpha=a)
    f.text(0.06,0.07,"Fuentes: BBVA, informe 1S26 (30-jul-2026); consenso BBVA y Bloomberg (Benzinga); Jefferies y Renta 4 (Merca2); stockanalysis (9-oct-2026).\nCifras marcadas como calculadas son cálculos propios. Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado.\nAIAcciones España no tiene posiciones en las empresas analizadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
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
