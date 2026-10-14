# Banco Sabadell 1S 2026 · video España 1080p con locución (Piper es_ES davefx) y logo AIAcciones España
# Uso: VOICE=.../es_ES-davefx-medium.onnx AUD=scratch python3 make_video_voz.py
import subprocess, os, wave, json, numpy as np
from PIL import Image
from base import *
plt.rcParams['text.parse_math']=False
from narracion import N
DIR="/mnt/project-files/espana/sabadell"
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD=os.environ.get("AUD","aud")
SILENT=os.path.join(AUD,"video-silent.mp4")
OUT=f"{DIR}/youtube-sabadell-1S26-con-voz.mp4"
SECS=["El titular","Ingresos","Beneficio / BPA","Eficiencia y balance","Guidance","Valoración","Qué cambió"]
NS=len(SECS)
EMP=["Banco Sabadell"]
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
    f.text(0.06,0.60,"RESULTADOS 1S 2026 · SAB",color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.06,0.47,"Banco Sabadell",color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.37,"Beneficio 971 M€ (-0,5%) con TSB; recurrente 691 M€ (-14,1%)",color=ACC2,fontsize=38,weight="bold",alpha=a)
    f.text(0.06,0.28,"Tras la OPA fallida de BBVA y la venta de TSB. ¿Cuánto vale hoy la acción?",color=MUTED,fontsize=29,alpha=a)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=90)

def s1a(t):
    f=base_fig(1,"El titular","Beneficio 971 M€; recurrente -14,1%","M€. Cuenta publicada el 24-jul-2026 (Europa Press); 1S25 calculado. BN con 4 meses de TSB y 322 M€ de plusvalía.")
    table(f,t,["","1S 2026","1S 2025","Var. a/a"],
          [["Margen de intereses","1.774","~1.810","-2,0%"],["Comisiones netas","643","~649","-0,9%"],["Margen bruto","2.463","~2.534","-2,8%"],["Costes","1.227","~1.086","+13%"],["Margen antes de dotaciones","1.236","~1.449","-14,7%"],["Dotaciones","285","~241","+18,3%"],["Beneficio neto","971","~976","-0,5%"]],
          [0.06,0.47,0.63,0.79],y0=0.70,step=0.068,fs=27,hi=6)
    return to_arr(f)

def s1b(t):
    f=base_fig(1,"El titular","2T26: beneficio algo por debajo del consenso","Renta 4 (24-jul-2026). BN 2T26 = 971 - 347 del 1T26 (calculado). Cotización: Merca2 (cierre del 24-jul-2026, 3,36 €).")
    kpis(f,[("624 M€","BN 2T26\n(calculado)",ACC2),("-2%","BN 2T vs\nconsenso",NEG),("+2%","Margen bruto 2T\nvs consenso",ACC),("+3,4%","Acción el día\nde resultados",ACC)],t,y=0.50)
    return to_arr(f)

def s2a(t):
    f=base_fig(2,"Ingresos","Margen bruto 2.463 M€: -2,8%","M€, 1S26. En un banco, el margen bruto equivale a los ingresos. Margen de intereses y comisiones sin TSB: 2.417 M€.")
    ax=f.add_axes([0.30,0.18,0.48,0.50]); hbars(ax,["Margen bruto","Margen de\nintereses","Comisiones\nnetas"],[2463,1774,643],t,[ACC,ACC2,ACC],FMT)
    side(ax,f,["-2,8%","-2,0%","-0,9%"],t)
    return to_arr(f)

def s2b(t):
    f=base_fig(2,"Ingresos","El 2T mejora: intereses +3,4%, comisiones +4%","M€. 2T26 de la nota del banco; 1T26 calculado (semestre menos 2T). Cita: Rafael Alonso, Bankinter (Capitalbolsa).")
    ax=f.add_axes([0.08,0.18,0.38,0.50]); bars(ax,["MI 1T26","MI 2T26"],[872,902],t,[DIM,ACC],FMT,ymax=1100)
    ax2=f.add_axes([0.54,0.18,0.38,0.50]); bars(ax2,["Comis. 1T26","Comis. 2T26"],[315,328],t,[DIM,ACC2],FMT,ymax=400)
    return to_arr(f)

def s3a(t):
    f=base_fig(3,"Beneficio por acción","BPA ~0,20 €; recurrente ~0,14 €","BPA calculado con 4.890 M de acciones (stockanalysis). Beneficio recurrente: 2T26 359 M€ (Capitalbolsa); 1T26 332 M€ calculado.")
    ax=f.add_axes([0.08,0.18,0.38,0.50]); bars(ax,["BPA 1S26","BPA recurrente"],[0.199,0.141],t,[ACC,DIM],lambda v:f"{v:.2f} €".replace(".",","),ymax=0.26)
    ax2=f.add_axes([0.54,0.18,0.38,0.50]); bars(ax2,["Recurr. 1T26","Recurr. 2T26"],[332,359],t,[DIM,ACC2],lambda v:f"{v:.0f} M€",ymax=450)
    return to_arr(f)

def s4a(t):
    f=base_fig(4,"Eficiencia y rentabilidad","ROTE recurrente 13,6%","Eficiencia = costes / margen bruto (calculado; recurrente sin los 88 M€ de prejubilaciones). ROTE y costes: nota de resultados.")
    kpis(f,[("~46%","Eficiencia recurrente\n(1S25: ~43%)",ACC),("~50%","Eficiencia con\nprejubilaciones",FG),("13,6%","ROTE recurrente\n(objetivo 14,5%)",ACC2),("+4,9%","Costes\nrecurrentes",NEG)],t,y=0.50)
    return to_arr(f)

def s4b(t):
    f=base_fig(4,"Riesgo y capital","Menos morosidad, más capital","Morosidad, cobertura y CET1 fully loaded a jun-2026: nota de resultados. Variación del CET1: Renta 4.")
    kpis(f,[("2,47%","Morosidad\n(1T26: 2,55%)",ACC),("68,7%","Cobertura",FG),("40 pb","Coste del riesgo\n(guía ~40 pb)",FG),("13,11%","CET1\n(+20 pb t/t)",ACC2)],t,y=0.50)
    return to_arr(f)

def s4c(t):
    f=base_fig(4,"Volumen de negocio","Crédito +5,5%; recursos +6,4%","M€, jun-2026 vs jun-2025. Hipotecas y consumo: España. Nota de resultados del 24-jul-2026.")
    kpis(f,[("125.184","Crédito vivo, M€\n(+5,5%)",ACC),("188.110","Recursos de\nclientes (+6,4%)",ACC),("+3,4%","Hipotecas\n(40.200 M€)",ACC2),("+12,7%","Consumo\n(5.600 M€)",ACC2)],t,y=0.50)
    return to_arr(f)

def s5(t):
    f=base_fig(5,"Guidance","Guía 2026 mantenida","Guía: nota de Banco Sabadell y Renta 4 (24-jul-2026). Dividendo extraordinario pagado el 29-may-2026 (Ara).")
    items=["Margen de intereses: más de +1% (1S26: -2%)","Comisiones: crecimiento de un dígito medio (1S26: -1%)","Costes recurrentes: menos de +3% (1S26: +4,9%)","Coste del riesgo ~40 pb · ROTE recurrente 14,5% (2027: 16%)","Recompra de 331 M€ · dividendo extra de 0,50 € (mayo)"]
    bullets(f,items,t,y0=0.68,step=0.095,fs=28)
    return to_arr(f)

def s6a(t):
    f=base_fig(6,"Valoración","11,5 veces beneficio esperado; 1,4 veces libros","Acción 3,583 € (13-oct-2026); capitalización 17.510 M€. stockanalysis. Dividendo ordinario 0,26 €: no incluye el extra de 0,50 €.")
    kpis(f,[("19,3x","PER 12 meses",FG),("11,5x","PER forward",FG),("1,42x","Precio / valor\nen libros",FG),("7,4%","Rentab. dividendo",FG)],t,y=0.50)
    return to_arr(f)

def s6b(t):
    f=base_fig(6,"Valoración","Frente a su historia","Múltiplos a cierre de cada año y actual (13-oct-2026): stockanalysis. Sin TSB el perímetro cambia. Solo datos, sin juicio de valor.")
    table(f,t,["","2022","2023","2024","2025","Actual"],
          [["PER","6,3x","5,0x","5,9x","10,3x","19,3x"],["Precio / libros","0,38x","0,44x","0,68x","1,19x","1,42x"],["Rentab. dividendo","4,6%","5,4%","10,8%","n.d.","7,4%"]],
          [0.06,0.36,0.48,0.60,0.72,0.84],y0=0.64,step=0.11,fs=30,hi=None)
    return to_arr(f)

def s7a(t):
    f=base_fig(7,"Qué cambió","3 puntos positivos","")
    bullets(f,["Intereses (+3,4%) y comisiones (+4%) mejoran en el 2T",
               "Crédito +5,5% y morosidad a la baja (2,47%)",
               "CET1 13,11%, recompra de 331 M€ y dividendo extra"],t,mark="✓")
    return to_arr(f)

def s7b(t):
    f=base_fig(7,"Qué cambió","3 riesgos","")
    bullets(f,["Beneficio recurrente -14,1%; 2T algo bajo el consenso",
               "Costes recurrentes +4,9%, por encima de la guía (<3%)",
               "Comisiones -1% frente a la guía de un dígito medio"],t,mark="!")
    return to_arr(f)

def s_fin(t):
    f=fig(); a=ease(t/0.5)
    f.text(0.06,0.55,"Banco Sabadell · 1S 2026",color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.06,0.45,"Beneficio sostenido por TSB; el negocio recurrente mejora en el 2T.",color=ACC,fontsize=34,alpha=a)
    f.text(0.06,0.37,"Próximo informe (3T26): 29-oct-2026 (estimada) · YouTube: @AIAccionesEspaña",color=MUTED,fontsize=30,alpha=a)
    f.text(0.06,0.07,"Fuentes: Banco Sabadell, nota de resultados 1S26 (24-jul-2026); Europa Press; Renta 4; Capitalbolsa; Merca2; stockanalysis (precio y múltiplos, 13-oct-2026).\nCifras marcadas como calculadas son cálculos propios. Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado.\nAIAcciones España no tiene posiciones en las empresas analizadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
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
