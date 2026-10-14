# Iberdrola 1S 2026 · video piloto España 1080p con locución (Piper es_ES davefx) y logo AIAcciones España
# Uso: VOICE=.../es_ES-davefx-medium.onnx AUD=scratch python3 make_video_voz.py
import subprocess, os, wave, json, numpy as np
from PIL import Image
from base import *
plt.rcParams['text.parse_math']=False
from narracion import N
DIR="/mnt/project-files/espana/iberdrola"
LOGO="/mnt/project-files/espana/marca/logo-aiacciones-espana.png"
VOICE=os.environ.get("VOICE","vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
AUD=os.environ.get("AUD","aud")
SILENT=os.path.join(AUD,"video-silent.mp4")
OUT=f"{DIR}/youtube-iberdrola-1S26-con-voz.mp4"
SECS=["El titular","Ingresos","Beneficio / BPA","Márgenes y caja","Guidance","Valoración","Qué cambió"]
NS=len(SECS)
EMP=["Iberdrola"]
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
def s_title(t):
    f=fig(); a=ease(t/0.6)
    f.text(0.06,0.60,"RESULTADOS 1S 2026 · IBE",color=ACC,fontsize=34,weight="bold",alpha=a)
    f.text(0.06,0.47,"Iberdrola",color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.37,"Beneficio ajustado +7,8%, 5,5% sobre el consenso",color=ACC2,fontsize=40,weight="bold",alpha=a)
    f.text(0.06,0.28,"¿Qué impulsó el semestre y cuánto vale hoy la acción?",color=MUTED,fontsize=29,alpha=a)
    arr=to_arr(f); return with_logo(arr,LGB_RGB,LGB_A,x=110,y=90)

def s1a(t):
    f=base_fig(1,"El titular","Mejor de lo esperado en beneficio ajustado","M€. Consenso: Bankinter Análisis (22-jul-2026). Ajustado = sin México ni extraordinarios. Informe del 22-jul-2026.")
    table(f,t,["","1S 2026","1S 2025","Var. a/a","Consenso"],
          [["EBITDA ajustado","8.050","7.497","+7,4%","7.910"],["Beneficio neto ajustado","3.565","3.308","+7,8%","3.380"],
           ["Beneficio neto reportado","4.336","3.562","+21,7%","—"],["Plusvalía venta México","953","—","—","—"]],
          [0.06,0.40,0.54,0.68,0.82],y0=0.66,step=0.09,fs=29,hi=1)
    return to_arr(f)

def s1b(t):
    f=base_fig(1,"El titular","Sorpresa positiva frente al consenso","Diferencia calculada vs consenso de Bankinter Análisis. Efecto divisas en EBITDA: -106 M€.")
    kpis(f,[("+5,5%","Beneficio ajustado\nvs consenso",ACC),("+1,8%","EBITDA ajustado\nvs consenso",ACC),("+8,8%","EBITDA sin efecto\ndivisas",ACC2)],t,y=0.50)
    return to_arr(f)

def s2a(t):
    f=base_fig(2,"Ingresos","22.469 M€: +1,7% (+4,2% comparable)","M€. Comparable = 1S25 sin México (21.571 M€). Margen bruto 12.257 M€ (+3,7% comparable).")
    ax=f.add_axes([0.10,0.18,0.80,0.50]); bars(ax,["1S 2025 reportado","1S 2025 comparable","1S 2026"],[22100,21571,22469],t,[DIM,DIM,ACC],FMT,ymax=27000)
    return to_arr(f)

def s2b(t):
    f=base_fig(2,"Ingresos","Las redes tiran del crecimiento","EBITDA ajustado por negocio, M€, 1S26. Variación a/a.")
    ax=f.add_axes([0.30,0.18,0.48,0.50]); hbars(ax,["Redes","Generación\ny clientes"],[4213,3790],t,[ACC,ACC2],FMT)
    side(ax,f,["+13%","+1%"],t)
    return to_arr(f)

def s3a(t):
    f=base_fig(3,"Beneficio por acción","BPA ajustado ~0,55 € en el semestre","BPA calculado con ~6.490 M de acciones (stockanalysis). La empresa no publica BPA en la presentación.")
    ax=f.add_axes([0.06,0.18,0.42,0.50]); bars(ax,["Ajustado","Reportado"],[0.55,0.67],t,[ACC,ACC2],lambda v:f"{v:.2f} €".replace(".",","))
    ax2=f.add_axes([0.54,0.18,0.42,0.50]); bars(ax2,["Consenso","Real"],[3380,3565],t,[DIM,ACC],FMT)
    a=ease(t/0.5)
    f.text(0.08,0.70,"BPA 1S26 (calculado)",color=FG,fontsize=26,weight="bold",alpha=a); f.text(0.56,0.70,"Beneficio ajustado, M€",color=FG,fontsize=26,weight="bold",alpha=a)
    return to_arr(f)

def s4a(t):
    f=base_fig(4,"Márgenes","Margen EBITDA 35,8%: +1,0 pp","% sobre ingresos; 1S25 comparable (sin México). Márgenes calculados. Coste de la deuda 5,13% (4,69%).")
    ax=f.add_axes([0.08,0.18,0.84,0.50]); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    g=["EBITDA","Operativo (EBIT)","Neto ajustado"]; v25=[34.8,21.9,15.3]; v26=[35.8,23.3,15.9]; x=np.arange(3); e=ease(t)
    ax.bar(x-0.2,[v*e for v in v25],0.38,color=DIM,label="1S 2025"); ax.bar(x+0.2,[v*e for v in v26],0.38,color=ACC,label="1S 2026")
    if t>=0.6:
        for xx,a_,b_ in zip(x,v25,v26):
            ax.text(xx-0.2,a_*e+1,f"{a_:.1f}%".replace(".",","),ha="center",color=MUTED,fontsize=22,weight="bold"); ax.text(xx+0.2,b_*e+1,f"{b_:.1f}%".replace(".",","),ha="center",color=FG,fontsize=22,weight="bold")
    ax.set_xticks(x,g); ax.tick_params(colors=MUTED,labelsize=24,length=0); ax.set_yticks([]); ax.set_ylim(0,44)
    ax.legend(frameon=False,labelcolor=FG,fontsize=20,ncol=2,loc="upper center",bbox_to_anchor=(0.5,1.12))
    return to_arr(f)

def s4b(t):
    f=base_fig(4,"Inversión y caja","Inversión 7.010 M€: +25%","M€, 1S26. FCF yield 12 meses: stockanalysis (oct-2026). Renovables: +1.594 MW en el semestre.")
    kpis(f,[("7.010","Inversión total, M€\n(+25%)",ACC2),("4.384","En redes, M€\n(+42%)",ACC),("55.000","Activos regulados\nM€ (+11%)",ACC),("2,2%","FCF yield\n12 meses",NEG)],t,y=0.50)
    return to_arr(f)

def s4c(t):
    f=base_fig(4,"Deuda","Deuda neta 54.000 M€, 3,5x EBITDA","Deuda neta ajustada a jun-2026 (50.182 M€ a dic-2025). Previsión de cierre 2026: ~56.000 M€.")
    kpis(f,[("54.000","Deuda neta, M€\n(+3.800 vs dic)",NEG),("3,5x","Deuda neta /\nEBITDA",FG),("22,4%","FFO / deuda\n(23,1%)",FG),("21.500","Liquidez, M€\n(22 meses)",ACC)],t,y=0.50)
    return to_arr(f)

def s5(t):
    f=base_fig(5,"Guidance","Guía 2026 reafirmada","Fuente: presentación 1S26 y nota de prensa de Iberdrola (22-jul-2026).")
    items=["Beneficio neto ajustado 2026: +8% o más (>6.700 M€)","Compra del 80% de Caruna (Finlandia) por ~2.000 M€, cierre 1T27","+2.100 MW renovables adicionales hasta diciembre","Nuevo plan estratégico: Capital Markets Day en 2027","Dividendo complementario 0,427 €; total ejercicio 0,685 € (+6,2%)"]
    bullets(f,items,t,y0=0.68,step=0.095,fs=28)
    return to_arr(f)

def s6a(t):
    f=base_fig(6,"Valoración","25,9 veces beneficio, EV/EBITDA 13,7x","Acción 21,35 € (9-oct-2026); capitalización ~138.500 M€. Múltiplos: stockanalysis (12 meses y forward).")
    kpis(f,[("25,9x","PER 12 meses",FG),("19,9x","PER forward",FG),("13,7x","EV / EBITDA",FG),("2,2%","FCF yield",FG),("3,2%","Rentab. dividendo",FG)],t,y=0.50)
    return to_arr(f)

def s6b(t):
    f=base_fig(6,"Valoración","Frente a su historia","Múltiplos a cierre de cada año y actual (oct-2026): stockanalysis. Solo datos, sin juicio de valor.")
    table(f,t,["","2023","2024","2025","Actual"],
          [["PER","16,1x","15,2x","20,1x","25,9x"],["EV/EBITDA","10,3x","10,6x","12,6x","13,7x"],["Rentab. dividendo","5,2%","5,1%","3,8%","3,2%"]],
          [0.06,0.36,0.51,0.66,0.81],y0=0.64,step=0.11,fs=30,hi=None)
    a=ease((t-0.3)/0.5)
    f.text(0.06,0.25,"Acción +30% en 12 meses (21,35 €, 9-oct-2026)",color=MUTED,fontsize=26,alpha=a)
    return to_arr(f)

def s7a(t):
    f=base_fig(7,"Qué cambió","3 puntos positivos","")
    bullets(f,["Redes: EBITDA +13% y base de activos regulados +11%",
               "Beneficio ajustado 5,5% sobre el consenso; guía 2026 se mantiene",
               "Plusvalía de 953 M€ por México; dividendo del ejercicio +6,2%"],t,mark="✓")
    return to_arr(f)

def s7b(t):
    f=base_fig(7,"Qué cambió","3 riesgos","")
    bullets(f,["Divisas: dólar y libra débiles restan resultados",
               "Deuda +3.800 M€ en el semestre; coste ya sobre 5%",
               "Regulación en Reino Unido, EE.UU. y Brasil"],t,mark="!")
    return to_arr(f)

def s_fin(t):
    f=fig(); a=ease(t/0.5)
    f.text(0.06,0.55,"Iberdrola · 1S 2026",color=FG,fontsize=60,weight="bold",alpha=a)
    f.text(0.06,0.45,"Redes al alza y beneficio ajustado sobre el consenso.",color=ACC,fontsize=34,alpha=a)
    f.text(0.06,0.37,"Próximo informe (3T26): 21-oct-2026 · YouTube: @AIAccionesEspaña",color=MUTED,fontsize=30,alpha=a)
    f.text(0.06,0.10,"Fuentes: Iberdrola, presentación de resultados 1S26 (CNMV, 22-jul-2026); Bankinter Análisis (consenso); stockanalysis (precio y múltiplos, 9-oct-2026).\nCifras marcadas como calculadas son cálculos propios. Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado. AIAcciones España no tiene posiciones en las empresas analizadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
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
