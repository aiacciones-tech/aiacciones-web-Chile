# Unicaja 1S 2026 · video España 1080p con locución (Piper es_ES davefx) y logo AIAcciones España
# Uso: VOICE=.../es_ES-davefx-medium.onnx AUD=scratch python3 make_video_voz.py
import subprocess, os, wave, json, numpy as np
from PIL import Image
from base import *
plt.rcParams['text.parse_math']=False
from narracion import N
DIR="/mnt/project-files/espana/unicaja"
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD=os.environ.get("AUD","aud")
SILENT=os.path.join(AUD,"video-silent.mp4")
OUT=f"{DIR}/youtube-unicaja-1S26-con-voz.mp4"
SECS=["El titular","Ingresos","Beneficio / BPA","Eficiencia y balance","Guidance","Valoración","Qué cambió"]
NS=len(SECS)
EMP=["Unicaja"]
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
    f.text(0.06,0.60,"RESULTADOS 1S 2026 · UNI",color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.06,0.47,"Unicaja",color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.37,"Beneficio 361 M€ (+7,1%); 2T un 10% sobre el consenso",color=ACC2,fontsize=40,weight="bold",alpha=a)
    f.text(0.06,0.28,"Menos morosidad y guía al alza. ¿Cuánto vale hoy la acción?",color=MUTED,fontsize=29,alpha=a)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=90)

def s1a(t):
    f=base_fig(1,"El titular","Beneficio +7,1%; ingresos +2,5%","M€. Nota de resultados (31-jul-2026) y Bolsamania. Costes = personal + generales + amortizaciones (calculado). 1S25 calculado.")
    table(f,t,["","1S 2026","1S 2025","Var. a/a"],
          [["Margen de intereses","755","742","+1,7%"],["Comisiones netas","269","262","+2,6%"],["Margen bruto","1.085","1.059","+2,5%"],["Costes","494","~471","~+5%"],["Margen de explotación","590","~587","~+0,5%"],["Beneficio neto","361","338","+7,1%"]],
          [0.06,0.45,0.62,0.79],y0=0.68,step=0.075,fs=28,hi=5)
    return to_arr(f)

def s1b(t):
    f=base_fig(1,"El titular","2T26: 201 M€, un 10% sobre el consenso","Consenso según Investing.com (31-jul-2026; no nombra proveedor). Reacción: cierre 31-jul vs 30-jul, stockanalysis (calculado).")
    kpis(f,[("+10%","BN 2T vs\nconsenso (183 M€)",ACC),("41 M€","Deterioros\n(55 esperados)",ACC),("-2%","Comisiones\nvs consenso",NEG),("+2,5%","Acción el día\nde resultados",ACC2)],t,y=0.50)
    return to_arr(f)

def s2a(t):
    f=base_fig(2,"Ingresos","Margen bruto 1.085 M€: +2,5%","M€. En un banco, el margen bruto equivale a los ingresos. Nota de resultados (31-jul-2026).")
    ax=f.add_axes([0.30,0.18,0.48,0.50]); hbars(ax,["Margen bruto","Margen de\nintereses","Comisiones\nnetas"],[1085,755,269],t,[ACC,ACC2,ACC],FMT)
    side(ax,f,["+2,5%","+1,7%","+2,6%"],t)
    return to_arr(f)

def s2b(t):
    f=base_fig(2,"Ingresos","Fondos y seguros tiran de las comisiones","Nota de resultados 1S26. Patrimonio en fondos +18,2% y suscripciones netas de 1.103 M€ (Bolsamania).")
    kpis(f,[("53%","Comisiones no bancarias\n/ total (+4 pp)",ACC),("+11,8%","Comisiones\nno bancarias",ACC),("+17,2%","Comisiones de\nfondos",ACC2),("18.016","Fondos de inversión,\nM€ (+18,2%)",FG)],t,y=0.50)
    return to_arr(f)

def s3a(t):
    f=base_fig(3,"Beneficio por acción","BPA ~0,14 € en el semestre","BPA calculado con 2.570 M de acciones (stockanalysis). Trimestres: XTB (31-jul-2026).")
    ax=f.add_axes([0.08,0.18,0.38,0.50]); bars(ax,["BN 2T25","BN 2T26"],[179,201],t,[DIM,ACC],lambda v:f"{v:.0f} M€",ymax=260)
    ax2=f.add_axes([0.54,0.18,0.38,0.50]); bars(ax2,["BN 1T26","BN 2T26"],[161,201],t,[DIM,ACC2],lambda v:f"{v:.0f} M€",ymax=260)
    return to_arr(f)

def s4a(t):
    f=base_fig(4,"Eficiencia y rentabilidad","Eficiencia 45,6%; ROTE 10%","Eficiencia y ROTE: XTB. 46% en 12 meses y ROTE ajustado 12%: nota de resultados.")
    kpis(f,[("45,6%","Eficiencia\n(1S25: 44,6%)",NEG),("10,0%","ROTE\n(1S25: 9,7%)",ACC2),("12%","ROTE ajustado por\nexceso de capital",ACC2)],t,y=0.50)
    return to_arr(f)

def s4b(t):
    f=base_fig(4,"Riesgo y capital","Menos morosidad, capital holgado","Nota de resultados, jun-2026. Coste del riesgo del semestre (2T: 18 pb). Exceso sobre requerimientos: 2.201 M€.")
    kpis(f,[("1,8%","Morosidad\n(-38 pb a/a)",ACC),("82,7%","Cobertura\nde dudosos",FG),("19 pb","Coste del\nriesgo",ACC),("15,8%","CET1",ACC2)],t,y=0.50)
    return to_arr(f)

def s4c(t):
    f=base_fig(4,"Volumen de negocio","Crédito sano +3,7%; hipotecas nuevas +40%","M€, jun-2026 vs jun-2025. Nota de resultados y Bolsamania (31-jul-2026).")
    kpis(f,[("49.941","Crédito sano, M€\n(+3,7%)",ACC),("+39,5%","Nueva producción\nhipotecaria",ACC),("76.264","Depósitos, M€\n(+4,1%)",FG),("+12,7%","Recursos fuera\nde balance",ACC2)],t,y=0.50)
    return to_arr(f)

def s5(t):
    f=base_fig(5,"Guidance","Guía 2026: al alza","Guía revisada el 31-jul-2026 (Investing.com). Dividendo a cuenta: nota de resultados.")
    items=["Beneficio: crecer a un dígito medio (antes: superar 2025)","Margen de intereses: un dígito bajo-medio (antes: superar 2025)","Coste del riesgo 20-25 pb (antes: menos de 30 pb)","Comisiones: un dígito bajo · Costes: un dígito medio","95% del beneficio en efectivo; a cuenta 8,44 cts (+28%)"]
    bullets(f,items,t,y0=0.68,step=0.095,fs=28)
    return to_arr(f)

def s6a(t):
    f=base_fig(6,"Valoración","12,9 veces beneficio; 1,2 veces libros","Acción 3,242 € (13-oct-2026); capitalización 8.330 M€. Múltiplos: stockanalysis.")
    kpis(f,[("12,9x","PER 12 meses",FG),("11,8x","PER forward",FG),("1,23x","Precio / valor\nen libros",FG),("5,3%","Rentab. dividendo",FG)],t,y=0.50)
    return to_arr(f)

def s6b(t):
    f=base_fig(6,"Valoración","Frente a su historia","Múltiplos a cierre de cada año y actuales (13-oct-2026): stockanalysis. Solo datos, sin juicio de valor.")
    table(f,t,["","2022","2023","2024","2025","Actual"],
          [["PER","10,1x","9,1x","5,7x","11,4x","12,9x"],["Precio / libros","0,42x","0,36x","0,48x","1,01x","1,23x"],["Rentab. dividendo","5,8%","6,6%","11,5%","6,4%","5,3%"]],
          [0.06,0.36,0.48,0.60,0.72,0.84],y0=0.64,step=0.11,fs=30,hi=None)
    return to_arr(f)

def s7a(t):
    f=base_fig(7,"Qué cambió","3 puntos positivos","")
    bullets(f,["2T un 10% sobre el consenso y guía de beneficio al alza",
               "Morosidad 1,8% (-38 pb); coste del riesgo 19 pb",
               "Hipotecas nuevas +39,5%; dividendo a cuenta +28%"],t,mark="✓")
    return to_arr(f)

def s7b(t):
    f=base_fig(7,"Qué cambió","3 riesgos","")
    bullets(f,["La sorpresa vino de menos deterioros; comisiones -2% vs consenso",
               "Costes ~+5% frente a ingresos +2,5%: eficiencia 45,6%",
               "Coste de los depósitos al alza; sin guía para 2027"],t,mark="!")
    return to_arr(f)

def s_fin(t):
    f=fig(); a=ease(t/0.5)
    f.text(0.06,0.55,"Unicaja · 1S 2026",color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.06,0.45,"Más beneficio por menos deterioros; guía al alza.",color=ACC,fontsize=34,alpha=a)
    f.text(0.06,0.37,"Próximo informe (3T26): 30-oct-2026 · YouTube: @AIAccionesEspaña",color=MUTED,fontsize=30,alpha=a)
    f.text(0.06,0.07,"Fuentes: Unicaja, nota de resultados 1S26 (31-jul-2026); Investing.com, XTB y Bolsamania; stockanalysis (precio y múltiplos, 13-oct-2026).\nCifras marcadas como calculadas son cálculos propios. Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado.\nAIAcciones España no tiene posiciones en las empresas analizadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
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
