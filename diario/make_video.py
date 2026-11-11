# Video diario de la Bolsa de Santiago (MSCI IPSA): 1080p, locución Piper es_MX claude (voz fluida), logo AIAcciones Chile.
# Uso: AUD=<scratch> python3 make_video.py <carpeta del día> [preview]
#   La carpeta del día tiene mercado.json (de datos/mercado-<fecha>.json) y video.json (textos y locución; ver ejemplo-2026-11-09/).
#   Escribe <carpeta>/youtube-bolsa-chile-<fecha>.mp4 y AUD/times.json (capítulos).
import subprocess, os, sys, wave, json, textwrap, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import imageio_ffmpeg
from PIL import Image
plt.rcParams['text.parse_math']=False
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from tecnico import calc, MESES
import campana
DIR=os.path.abspath(sys.argv[1]); PREVIEW=len(sys.argv)>2 and sys.argv[2]=="preview"
W,H,FPS=1920,1080,30
BG="#0B1E3A"; FG="#FFFFFF"; MUTED="#9FB3CC"; ACC="#2FB7A3"; ACC2="#4C8DF0"; NEG="#F2A541"; DIM="#3A5378"; PUR="#C38BF2"
COLS={"acc":ACC,"acc2":ACC2,"neg":NEG,"fg":FG,"muted":MUTED,"pur":PUR}
LOGO=os.environ.get("LOGO","/mnt/project-files/marca/logo-aiacciones-chile.png")
VOICE=os.environ.get("VOICE","vits-piper-es_MX-claude-high/es_MX-claude-high.onnx")
AUD=os.environ.get("AUD","aud"); SILENT=os.path.join(AUD,"video-silent.mp4")
M=json.load(open(f"{DIR}/mercado.json")); VJ=json.load(open(f"{DIR}/video.json"))
R,A=calc(M); TV=M["tv"]; TK=M.get("ipsa_tickers",{})
OUT=f"{DIR}/youtube-bolsa-chile-{R['fecha']}.mp4"
FECHA_TXT=VJ["fecha_txt"].upper()
SECS=["Noticias","Por qué se movió","Acciones","Sectores","Perspectiva","Técnico","Agenda"]; NS=len(SECS)
es=lambda v,d=1:f"{v:,.{d}f}".replace(",","X").replace(".",",").replace("X",".")
pc=lambda v:f"{v:+.2f}%".replace(".",",")
col=lambda c:COLS.get(c,c)

def ease(t): t=min(max(t,0),1); return 1-(1-t)**3
def fig():
    f=plt.figure(figsize=(W/100,H/100),dpi=100); f.patch.set_facecolor(BG); return f
def to_arr(f):
    f.canvas.draw(); a=np.asarray(f.canvas.buffer_rgba())[:,:,:3].copy(); plt.close(f); return a
def load_logo(w):
    im=Image.open(LOGO).convert("RGBA"); h=int(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    a=np.asarray(im).astype(np.float32)/255.0; return a[:,:,:3]*255.0,a[:,:,3:4]
LG=load_logo(290); LGB=load_logo(560)
def with_logo(arr,lg=LG,x=None,y=None):
    rgb,al=lg; h,w=al.shape[:2]; x=W-w-40 if x is None else x; y=H-h-30 if y is None else y
    reg=arr[y:y+h,x:x+w].astype(np.float32); arr[y:y+h,x:x+w]=(reg*(1-al)+rgb*al).astype(np.uint8); return arr
def base_fig(n,kicker,title,sub):
    f=fig()
    f.text(0.06,0.90,kicker.upper(),color=ACC,fontsize=22,weight="bold")
    f.text(0.06,0.81,title,color=FG,fontsize=46 if len(title)<=48 else 40,weight="bold")
    f.text(0.94,0.92,f"{n}/{NS} · {SECS[n-1].upper()}",color=MUTED,fontsize=18,ha="right",weight="bold")
    f.text(0.94,0.885,"IPSA · "+FECHA_TXT,color=DIM,fontsize=15,ha="right",weight="bold")
    for i in range(NS):
        f.patches.append(plt.Rectangle((0.06+i*(0.88/NS),0.975),0.88/NS-0.008,0.008,transform=f.transFigure,color=ACC if i<n else DIM,figure=f))
    if len(sub)>=115: sub="\n".join(textwrap.wrap(sub,112))
    f.text(0.06,0.045,sub,color=MUTED,fontsize=18 if len(sub)<115 else 16,style="italic",linespacing=1.4); return f
def clean(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=MUTED,labelsize=18,length=0)

dates,o,hi,lo,c=A["dates"],A["o"],A["hi"],A["lo"],A["c"]; S50,S200,RSI,K,Dl=A["S50"],A["S200"],A["RSI"],A["K"],A["D"]
MACD,SIG,HIST,S20,BBU,BBL=A["MACD"],A["SIG"],A["HIST"],A["S20"],A["BBU"],A["BBL"]
import datetime as dt
NB=126
I=[v for v in M["ipsa_intradia"]["velas"] if dt.datetime.fromtimestamp(v["t"],dt.timezone.utc).date()==dates[-1]]
IC=np.array([v["c"] for v in I]); PREV=c[-2]

def s_title(t):
    f=fig(); a=ease(t/0.6); up=c[-1]>=PREV
    f.patches.append(plt.Rectangle((0,0.585),1.0,0.105,transform=f.transFigure,color=ACC,alpha=a,figure=f))
    f.text(0.06,0.637,"IPSA · SESIÓN DEL "+FECHA_TXT,color=BG,fontsize=50 if len(FECHA_TXT)<=22 else 44,weight="bold",va="center",alpha=a)
    f.text(0.06,0.47,"Cierre: "+es(c[-1],2),color=FG,fontsize=72,weight="bold",alpha=a)
    f.text(0.06,0.40,f"{pc(R['var_pct'])} ({'+' if up else ''}{es(R['var_pts'])} puntos)",color=ACC if up else NEG,fontsize=44,weight="bold",alpha=a)
    if VJ.get("titular"): f.text(0.06,0.33,VJ["titular"],color=ACC2,fontsize=32,weight="bold",alpha=ease((t-0.3)/0.5))
    f.text(0.06,0.26,"Noticias · Por qué se movió · Análisis técnico · Agenda",color=MUTED,fontsize=26,alpha=a)
    if len(IC)>2:
        ax=f.add_axes([0.62,0.17,0.33,0.30]); clean(ax)
        n=max(2,int(len(IC)*ease(t))); x=np.arange(len(IC))
        ax.plot(x[:n],IC[:n],color=ACC if up else NEG,lw=3); ax.axhline(PREV,color=DIM,lw=1.5,ls="--")
        ax.set_xlim(0,len(IC)-1); ax.set_ylim(min(IC.min(),PREV)-40,max(IC.max(),PREV)+40); ax.set_xticks([]); ax.set_yticks([])
        f.text(0.62,0.50,"Evolución durante la sesión (5 min)",color=MUTED,fontsize=18)
        f.text(0.955,0.475,"Cierre anterior "+es(PREV),color=MUTED,fontsize=15,ha="right")
    f.text(0.06,0.06,VJ.get("title_fuente",f"Datos: TradingView, MSCI IPSA (cierre {R['fecha']}). Variación semanal: calculado."),color=MUTED,fontsize=17,style="italic")
    return with_logo(to_arr(f),LGB,x=110,y=90)

def s_news(t):
    N_=VJ["noticias"]; f=base_fig(1,"Noticias del día",N_["titulo"],N_["fuente"]); pal=[ACC2,ACC,PUR,NEG,FG]
    for i,(tag,txt) in enumerate(N_["items"]):
        b=ease((t-i*0.15)/0.4)
        if b<=0: continue
        y=0.66-i*0.135; cc=pal[i%5]
        f.patches.append(plt.Rectangle((0.06,y-0.025),0.006,0.075,transform=f.transFigure,color=cc,alpha=b,figure=f))
        f.text(0.08,y+0.02,tag,color=cc,fontsize=28,weight="bold",alpha=b)
        f.text(0.08,y-0.025,txt,color=FG,fontsize=25 if len(txt)<=95 else 22,alpha=b)
    return to_arr(f)

def s_fact(t):
    F=VJ["factores"]; f=base_fig(2,"Por qué se movió",F["titulo"],F["fuente"])
    L=[(n,(TV[v]["change"] if isinstance(v,str) else v)) for n,v in F["bolsas"] if not isinstance(v,str) or (v in TV and TV[v].get("change") is not None)]
    ax=f.add_axes([0.20,0.13,0.30,0.60]); clean(ax); e=ease(t)
    y=np.arange(len(L))[::-1]; v=[x[1] for x in L]; lim=max(abs(min(v)),abs(max(v)))*1.6
    ax.barh(y,[x*e for x in v],color=[(ACC2 if n=="IPSA" else (ACC if x>0 else NEG)) for n,x in L],height=0.6)
    ax.set_yticks(y,[n for n,_ in L]); ax.tick_params(colors=FG,labelsize=20); ax.set_xticks([]); ax.set_xlim(-lim if min(v)<0 else -lim*0.35,lim*0.6 if max(v)>0 else lim*0.35); ax.axvline(0,color=DIM,lw=1.5)
    if t>=0.6:
        for yy,x in zip(y,v): ax.text(x*e+(lim*0.02 if x>0 else -lim*0.02),yy,pc(x),va="center",ha="left" if x>0 else "right",color=FG,fontsize=19,weight="bold")
    f.text(0.06,0.745,F.get("bolsas_titulo","Bolsas en la sesión"),color=MUTED,fontsize=20)
    for i,(a_,b_,cc) in enumerate(F["items"]):
        b=ease((t-0.2-i*0.12)/0.4)
        if b<=0: continue
        yy=0.67-i*0.135
        f.text(0.57,yy,a_,color=col(cc),fontsize=29 if len(a_)<=34 else 25,weight="bold",alpha=b); f.text(0.57,yy-0.045,b_,color=MUTED,fontsize=22 if len(b_)<=44 else 19,alpha=b)
    return to_arr(f)

def s_movers(t):
    V_=VJ["valores"]; MOT=V_.get("motivos",{})
    f=base_fig(3,"Acciones del IPSA",f"{R['bajan']} bajan y {R['suben']} suben" if R['bajan']>=R['suben'] else f"{R['suben']} suben y {R['bajan']} bajan",V_["fuente"])
    for col_x,lst,cc,title in [(0.06,R["mejores"],ACC,"MÁS SUBEN"),(0.52,R["peores"],NEG,"MÁS BAJAN")]:
        f.text(col_x,0.72,title,color=cc,fontsize=24,weight="bold"); mx=max(abs(x[2]) for x in R["mejores"]+R["peores"])
        for i,(nom,tk,ch) in enumerate(lst):
            b=ease((t-i*0.08)/0.4)
            if b<=0: continue
            y=0.645-i*0.095; bw=0.13*abs(ch)/mx*b
            f.patches.append(plt.Rectangle((col_x+0.19,y-0.004),bw,0.035,transform=f.transFigure,color=cc,figure=f))
            f.text(col_x,y,nom,color=FG,fontsize=25,weight="bold",alpha=b)
            f.text(col_x+0.19+bw+0.008,y,pc(ch),color=FG,fontsize=23,weight="bold",alpha=b)
            if tk in MOT: f.text(col_x,y-0.035,MOT[tk],color=MUTED,fontsize=17,alpha=b)
    if V_.get("extra"): f.text(0.06,0.14,V_["extra"],color=ACC2,fontsize=25,weight="bold",alpha=ease((t-0.5)/0.4))
    return to_arr(f)

def hbars(ax,L,e,hl=None,fs=20):
    y=np.arange(len(L))[::-1]; v=[x[1] for x in L]; lim=max(abs(min(v)),abs(max(v)),0.1)*1.6
    ax.barh(y,[x*e for x in v],color=[(ACC2 if n==hl else (ACC if x>=0 else NEG)) for n,x in L],height=0.6)
    ax.set_yticks(y,[n for n,_ in L]); ax.tick_params(colors=FG,labelsize=fs); ax.set_xticks([]); ax.axvline(0,color=DIM,lw=1.5)
    ax.set_xlim(-lim if min(v)<0 else -lim*0.35,lim if max(v)>0 else lim*0.35)
    if e>=0.99:
        for yy,x in zip(y,v): ax.text(x+(lim*0.03 if x>=0 else -lim*0.03),yy,pc(x),va="center",ha="left" if x>=0 else "right",color=FG,fontsize=fs-1,weight="bold")

def s_sect(t):
    G=VJ["sectores"]; f=base_fig(4,"Sectores del IPSA",G["titulo"],"Variación del día de las 31 acciones del MSCI IPSA (TradingView), agrupadas por sector y ponderadas por capitalización bursátil: calculado. No son los pesos oficiales del índice.")
    ax=f.add_axes([0.25,0.15,0.30,0.58]); clean(ax); hbars(ax,[(n,x) for n,x,_ in R["sectores"]],ease(t/0.7))
    f.text(0.06,0.745,"Variación del día por sector",color=MUTED,fontsize=20)
    for i,(a_,b_,cc) in enumerate(G["items"]):
        b=ease((t-0.2-i*0.12)/0.4)
        if b<=0: continue
        yy=0.68-i*0.20
        f.text(0.62,yy,a_,color=col(cc),fontsize=29 if len(a_)<=30 else 25,weight="bold",alpha=b)
        f.text(0.62,yy-0.025,"\n".join(textwrap.wrap(b_,44)[:2]),color=MUTED,fontsize=20,alpha=b,va="top",linespacing=1.25)
    return to_arr(f)

def s_persp(t):
    P=VJ["perspectiva"]; f=base_fig(5,"En perspectiva",P["titulo"],"Rentabilidad del MSCI IPSA en cada plazo, con cierres diarios de TradingView; máximo y mínimo de 52 semanas: calculado.")
    ax=f.add_axes([0.16,0.15,0.36,0.58]); clean(ax); hbars(ax,[(n,x) for n,x in R["periodos"]],ease(t/0.7),fs=22)
    f.text(0.06,0.745,"Rentabilidad del IPSA",color=MUTED,fontsize=20)
    d=lambda s:dt.date.fromisoformat(s); fd=lambda s:f"{d(s).day}-{MESES[d(s).month-1]}-{d(s).year}"
    rows=[(f"{pc(R['dist_max_52s_pct'])}",f"bajo el máximo de 52 semanas\n({es(R['max_52s'],0)}, {fd(R['max_52s_fecha'])})",NEG),
          (f"{pc(R['dist_min_52s_pct'])}",f"sobre el mínimo de 52 semanas\n({es(R['min_52s'],0)}, {fd(R['min_52s_fecha'])})",ACC)]
    for i,(big,lab,cc) in enumerate(rows):
        b=ease((t-0.25-i*0.12)/0.4)
        if b<=0: continue
        f.text(0.62,0.64-i*0.20,big,color=cc,fontsize=46,weight="bold",alpha=b); f.text(0.62,0.62-i*0.20,lab,color=MUTED,fontsize=21,va="top",alpha=b,linespacing=1.3)
    if P.get("nota"): f.text(0.62,0.22,"\n".join(textwrap.wrap(P["nota"],40)),color=ACC2,fontsize=22,weight="bold",alpha=ease((t-0.5)/0.4),linespacing=1.3)
    return to_arr(f)

def s_tech1(t):
    T=VJ["tecnico"]; f=base_fig(6,"Análisis técnico",T["titulo1"],"Velas diarias, últimos 6 meses. Datos: TradingView (MSCI IPSA). Medias móviles simples y niveles (máximos y mínimos recientes): calculado. Son datos, no señales de compra o venta.")
    ax=f.add_axes([0.06,0.16,0.70,0.58]); clean(ax)
    n=len(c); idx=np.arange(n-NB,n); x=np.arange(NB); m=max(1,int(NB*ease(t/0.8)))
    for j in range(m):
        i=idx[j]; cc=ACC if c[i]>=o[i] else NEG
        ax.vlines(j,lo[i],hi[i],color=cc,lw=1.2); ax.add_patch(plt.Rectangle((j-0.35,min(o[i],c[i])),0.7,max(abs(c[i]-o[i]),3),color=cc))
    ax.plot(x[:m],S50[idx][:m],color=ACC2,lw=2.5,label=f"Media 50 sesiones ({es(S50[-1],0)})")
    ax.plot(x[:m],S200[idx][:m],color=PUR,lw=2.5,label=f"Media 200 sesiones ({es(S200[-1],0)})")
    a=ease((t-0.6)/0.4); LEV=T["niveles"]
    for lv,lab,tipo in LEV:
        cc=NEG if tipo=="res" else (ACC if tipo=="sop" else MUTED)
        ax.axhline(lv,color=cc,lw=1.2,ls="--",alpha=a); ax.text(NB+1,lv,lab,color=cc,fontsize=17,va="center",alpha=a)
    ax.set_xlim(-1,NB); ax.set_ylim(min(lo[idx].min(),np.nanmin(S200[idx]),*[l[0] for l in LEV])-200,max(hi[idx].max(),*[l[0] for l in LEV])+200)
    tk=[j for j in range(NB) if j==0 or dates[idx[j]].month!=dates[idx[j-1]].month]
    ax.set_xticks(tk,[MESES[dates[idx[j]].month-1] for j in tk]); ax.set_yticks([])
    ax.legend(frameon=False,labelcolor=FG,fontsize=18,loc=T.get("leyenda","lower right"))
    f.text(0.06,0.76,f"Cierre: {es(c[-1])}",color=FG,fontsize=22,weight="bold")
    return to_arr(f)

def s_tech2(t):
    T=VJ["tecnico"]; f=base_fig(6,"Análisis técnico",T["titulo2"],"RSI de 14 sesiones (Wilder) y estocástico lento (14, 3, 3) con datos de TradingView: calculado. Monto: 30 acciones del IPSA en pesos (precio x acciones, TradingView) frente a su media de 10 sesiones: calculado.")
    n=len(c); idx=np.arange(n-NB,n); x=np.arange(NB); m=max(2,int(NB*ease(t/0.8)))
    for rect,title,series,bands in [([0.06,0.45,0.66,0.25],f"RSI 14: {es(R['rsi14'],0)}",[(RSI,ACC2,"RSI")],(70,30)),
                                     ([0.06,0.13,0.66,0.25],f"Estocástico (14,3,3): %K {es(R['estoc_k'],0)} · %D {es(R['estoc_d'],0)}",[(K,ACC,"%K"),(Dl,NEG,"%D")],(80,20))]:
        ax=f.add_axes(rect); clean(ax)
        ax.axhspan(bands[0],100,color=NEG,alpha=0.08); ax.axhspan(0,bands[1],color=ACC,alpha=0.08)
        ax.axhline(bands[0],color=DIM,lw=1,ls="--"); ax.axhline(bands[1],color=DIM,lw=1,ls="--")
        for s_,cc,lab in series: ax.plot(x[:m],s_[idx][:m],color=cc,lw=2.5,label=lab)
        ax.set_xlim(0,NB-1); ax.set_ylim(0,100); ax.set_xticks([]); ax.set_yticks([bands[1],50,bands[0]])
        f.text(rect[0],rect[1]+rect[3]+0.012,title,color=FG,fontsize=22,weight="bold")
        if len(series)>1: ax.legend(frameon=False,labelcolor=FG,fontsize=16,loc="lower left",ncol=2)
    a=ease((t-0.4)/0.4); vr=R["volumen_vs_media10_pct"]
    for i,(big,lab,cc) in enumerate([(es(R['rsi14'],0),T["rsi_txt"],ACC2),(f"{es(R['estoc_k'],0)} / {es(R['estoc_d'],0)}",T["estoc_txt"],ACC),
                                      ((("+" if vr>0 else "")+es(vr,0)+"%") if vr is not None else "—","Monto transado frente\na su media de 10 sesiones",MUTED)]):
        f.text(0.77,0.64-i*0.17,big,color=cc,fontsize=44,weight="bold",alpha=a); f.text(0.77,0.60-i*0.17-0.04,lab,color=MUTED,fontsize=18,alpha=a)
    return to_arr(f)

def s_tech3(t):
    T=VJ["tecnico"]; f=base_fig(6,"Análisis técnico",T["titulo3"],"Bandas de Bollinger (media de 20 sesiones ± 2 desviaciones estándar) y MACD (12, 26, 9) con cierres diarios de TradingView: calculado. Son datos, no señales de compra o venta.")
    NB3=90; n=len(c); idx=np.arange(n-NB3,n); x=np.arange(NB3); m=max(2,int(NB3*ease(t/0.8)))
    ax=f.add_axes([0.06,0.44,0.62,0.30]); clean(ax)
    ax.fill_between(x[:m],BBL[idx][:m],BBU[idx][:m],color=ACC2,alpha=0.15,lw=0)
    ax.plot(x[:m],BBU[idx][:m],color=ACC2,lw=1.5); ax.plot(x[:m],BBL[idx][:m],color=ACC2,lw=1.5); ax.plot(x[:m],S20[idx][:m],color=MUTED,lw=1.5,ls="--")
    ax.plot(x[:m],c[idx][:m],color=FG,lw=2.5)
    ax.set_xlim(0,NB3-1); ax.set_xticks([]); ax.set_yticks([])
    f.text(0.06,0.755,"Bandas de Bollinger (20, 2) · últimos 3 meses",color=FG,fontsize=21,weight="bold")
    ax2=f.add_axes([0.06,0.13,0.62,0.24]); clean(ax2)
    ax2.bar(x[:m],HIST[idx][:m],color=[ACC if h>=0 else NEG for h in HIST[idx][:m]],width=0.8,alpha=0.8)
    ax2.plot(x[:m],MACD[idx][:m],color=ACC2,lw=2.2,label="MACD"); ax2.plot(x[:m],SIG[idx][:m],color=PUR,lw=2.2,label="Señal")
    ax2.axhline(0,color=DIM,lw=1); ax2.set_xlim(0,NB3-1); ax2.set_xticks([]); ax2.set_yticks([])
    ax2.legend(frameon=False,labelcolor=FG,fontsize=16,loc="lower left",ncol=2)
    f.text(0.06,0.385,"MACD (12, 26, 9) e histograma",color=FG,fontsize=21,weight="bold")
    a=ease((t-0.4)/0.4); cr=R.get("macd_cruce")
    fd=lambda s_:f"{dt.date.fromisoformat(s_).day}-{MESES[dt.date.fromisoformat(s_).month-1]}"
    rows=[(es(R["bb_sup"],0)+" / "+es(R["bb_inf"],0),"Banda superior / inferior",ACC2),
          (es(R["bb_ancho_pct"],1)+"%","Ancho de las bandas\n(sobre su media de 20)",MUTED),
          (es(R["macd"],0)+" / "+es(R["macd_senal"],0),"MACD / línea de señal",ACC if R["macd_hist"]>=0 else NEG),
          ((f"Cruce {cr[1]}, {fd(cr[0])}") if cr else "Sin cruce reciente","Último cruce del MACD\ncon su señal",FG)]
    for i,(big,lab,cc) in enumerate(rows):
        f.text(0.72,0.69-i*0.15,big,color=cc,fontsize=32 if len(big)<=16 else 27,weight="bold",alpha=a); f.text(0.72,0.665-i*0.15,lab,color=MUTED,fontsize=17,va="top",alpha=a)
    return to_arr(f)

def s_tech4(t):
    T=VJ["tecnico"]; Q=R.get("acciones_tec") or {}; f=base_fig(6,"Análisis técnico",T["titulo4"],"Medias de 50 y 200 sesiones y RSI de 14 sesiones de cada acción del MSCI IPSA, con datos diarios de TradingView. RSI ≥ 70: zona de sobrecompra; ≤ 30: sobreventa. Son datos, no señales de compra o venta.")
    a=ease(t/0.5); N=Q.get("n",0)
    for i,(k,lab,cc) in enumerate([("sobre_sma200","sobre su media de 200 sesiones",ACC2),("sobre_sma50","sobre su media de 50 sesiones",ACC)]):
        v=Q.get(k,0); y=0.62-i*0.24
        f.text(0.06,y,f"{v} de {N}",color=cc,fontsize=64,weight="bold",alpha=a); f.text(0.06,y-0.055,"acciones del IPSA "+lab,color=MUTED,fontsize=22,alpha=a)
        f.patches.append(plt.Rectangle((0.06,y-0.10),0.36,0.022,transform=f.transFigure,color=DIM,figure=f))
        f.patches.append(plt.Rectangle((0.06,y-0.10),0.36*(v/N if N else 0)*ease(t/0.7),0.022,transform=f.transFigure,color=cc,figure=f))
    for col_x,key,title,cc in [(0.50,"rsi_max","RSI MÁS ALTO",NEG),(0.74,"rsi_min","RSI MÁS BAJO",ACC)]:
        f.text(col_x,0.70,title,color=cc,fontsize=23,weight="bold",alpha=a)
        for j,(nom,tk,r_) in enumerate(Q.get(key,[])):
            b=ease((t-0.2-j*0.1)/0.4)
            if b<=0: continue
            zona=" · sobrecompra" if r_>=70 else (" · sobreventa" if r_<=30 else "")
            f.text(col_x,0.62-j*0.12,nom,color=FG,fontsize=26,weight="bold",alpha=b); f.text(col_x,0.585-j*0.12,f"RSI {es(r_,0)}{zona}",color=MUTED,fontsize=20,va="top",alpha=b)
    if T.get("nota4"): f.text(0.50,0.17,"\n".join(textwrap.wrap(T["nota4"],52)),color=ACC2,fontsize=22,weight="bold",alpha=ease((t-0.5)/0.4),linespacing=1.3)
    return to_arr(f)

def s_agenda(t):
    G=VJ["agenda"]; f=base_fig(7,"Agenda",G["titulo"],G["fuente"]); a=ease(t/0.6)
    for i,(d_,e_,s_) in enumerate(G["filas"]):
        b=ease((t-i*0.12)/0.4); y=0.64-i*0.10
        cc=MUTED if s_ in ("estimada","estimado") else FG
        f.text(0.06,y,d_,color=ACC,fontsize=28,weight="bold",alpha=b); f.text(0.23,y,e_,color=cc,fontsize=28 if len(e_)<=40 else 24,alpha=b); f.text(0.82,y,s_,color=MUTED,fontsize=22,style="italic",alpha=b)
    f.text(0.06,0.13,"Calendario de resultados y dividendos: aiacciones.cl/calendario",color=ACC2,fontsize=24,alpha=a)
    return to_arr(f)

def s_fin(t):
    Fn=VJ["fin"]; f=fig(); a=ease(t/0.5)
    f.text(0.06,0.56,f"IPSA · {VJ['fecha_txt']}",color=FG,fontsize=56,weight="bold",alpha=a)
    f.text(0.06,0.47,Fn["titular"],color=ACC,fontsize=32,alpha=a)
    f.text(0.06,0.39,"Cada día de bolsa, este resumen · YouTube: @aiaccioneschile · aiacciones.cl",color=MUTED,fontsize=28,alpha=a)
    if campana.activa(R["fecha"]): f.text(0.06,0.30,campana.PANTALLA_VIDEO,color=ACC2,fontsize=30,weight="bold",alpha=ease((t-0.2)/0.5))
    f.text(0.06,0.07,"Fuentes: "+Fn["fuentes"]+". Indicadores técnicos: calculados.\nContenido informativo: no es una recomendación de inversión ni asesoría personalizada. AIAcciones Chile no tiene posiciones en las acciones citadas.\nInvertir en bolsa conlleva riesgo de pérdida; las rentabilidades pasadas no garantizan las futuras. Aviso completo en la descripción.",color=MUTED,fontsize=17,linespacing=1.5)
    return with_logo(to_arr(f),LGB,x=110,y=110)

SEQ=[s_title,s_news,s_fact,s_movers,s_sect,s_persp,s_tech1,s_tech2,s_tech3,s_tech4,s_agenda,s_fin]; BIG={s_title,s_fin}
def frame(fn,t):
    arr=fn(t); return arr if fn in BIG else with_logo(arr)

if __name__=="__main__":
    os.makedirs(AUD,exist_ok=True)
    if PREVIEW:
        for fn in SEQ: Image.fromarray(frame(fn,1.0)).save(os.path.join(AUD,"prev_"+fn.__name__+".png"))
        sys.exit()
    TTS=["--length-scale","0.97","--noise-scale","0.55","--noise-w-scale","0.6","--sentence-silence","0.1"]
    LEAD,TAIL=0.12,0.45
    for fn in SEQ:
        p=os.path.join(AUD,fn.__name__+".wav")
        subprocess.run(["python3","-m","piper","-m",VOICE,"-f",p]+TTS,input=(VJ["voz"][fn.__name__]+(" "+campana.VOZ_VIDEO if fn is s_fin and campana.activa(R["fecha"]) else "")+"\n").encode(),check=True,capture_output=True)
    clips=[]
    for fn in SEQ:
        w=wave.open(os.path.join(AUD,fn.__name__+".wav")); sr=w.getframerate()
        a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)
        nz=np.where(np.abs(a)>300)[0]; a=a[max(nz[0]-int(0.03*sr),0):nz[-1]+int(0.08*sr)]
        f_in,f_out=int(0.015*sr),int(0.06*sr); a[:f_in]*=np.linspace(0,1,f_in); a[-f_out:]*=np.linspace(1,0,f_out); clips.append(a)
    durs=[LEAD+len(a)/sr+TAIL for a in clips]; durs[0]+=0.4; durs[-1]+=1.5
    if sum(durs)>330: sys.exit(f"Vídeo demasiado largo: {sum(durs):.1f} s (máx. 330, objetivo unos 5 min). Acorta la locución.")
    if sum(durs)<270: print(f"Aviso: el video dura {sum(durs):.1f} s; el objetivo es unos 5 minutos (280-320 s).")
    ANIM=30; XF=8; ff=imageio_ffmpeg.get_ffmpeg_exe()
    proc=subprocess.Popen([ff,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-preset","medium",SILENT],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
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
        audio.append(seg); times.append((fn.__name__,round(t0,2))); t0+=total/FPS; print(fn.__name__,round(t0,1),flush=True)
    proc.stdin.close(); proc.wait()
    full=np.clip(np.concatenate(audio),-32768,32767).astype(np.int16)
    w=wave.open(os.path.join(AUD,"full.wav"),"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(full.tobytes()); w.close()
    AF="highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250,loudnorm=I=-16:TP=-1.5:LRA=9"
    subprocess.run([ff,"-y","-i",SILENT,"-i",os.path.join(AUD,"full.wav"),"-af",AF,"-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-shortest","-movflags","+faststart",OUT],check=True,stderr=subprocess.DEVNULL)
    json.dump(times,open(os.path.join(AUD,"times.json"),"w")); json.dump(times,open(os.path.join(DIR,"times.json"),"w")); print("done",t0,OUT)
