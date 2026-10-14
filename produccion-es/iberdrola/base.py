import subprocess, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import imageio_ffmpeg

W,H,FPS=1920,1080,30
BG="#0B1E3A"; FG="#FFFFFF"; MUTED="#9FB3CC"; ACC="#2FB7A3"; ACC2="#4C8DF0"; NEG="#F2A541"; DIM="#3A5378"
OUT=""

def fig():
    f=plt.figure(figsize=(W/100,H/100),dpi=100); f.patch.set_facecolor(BG); return f

def header(f,kicker,title):
    f.text(0.06,0.90,kicker.upper(),color=ACC,fontsize=22,weight="bold")
    f.text(0.06,0.81,title,color=FG,fontsize=46,weight="bold")

def footer(f,sub):
    f.text(0.06,0.06,sub,color=MUTED,fontsize=22,style="italic",wrap=True)
    f.text(0.94,0.92,"IBERDROLA · 1S 2026",color=DIM,fontsize=16,ha="right",weight="bold")

def to_arr(f):
    f.canvas.draw(); a=np.asarray(f.canvas.buffer_rgba())[:,:,:3].copy(); plt.close(f); return a

def ease(t): t=min(max(t,0),1); return 1-(1-t)**3

def bars(ax,labels,vals,t,colors,fmt,ymax=None):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=MUTED,labelsize=22,length=0); ax.set_yticks([])
    x=np.arange(len(vals)); v=[vv*ease(t) for vv in vals]
    ax.bar(x,v,color=colors,width=0.55); ax.set_xticks(x,labels)
    ax.set_ylim(0,ymax or max(vals)*1.25)
    if t>=0.6:
        for i,vv in enumerate(vals): ax.text(i,vv*ease(t)+max(vals)*0.03,fmt(vv),ha="center",color=FG,fontsize=28,weight="bold")

def hbars(ax,labels,vals,t,colors,fmt):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=FG,labelsize=24,length=0); ax.set_xticks([])
    y=np.arange(len(vals))[::-1]; ax.barh(y,[vv*ease(t) for vv in vals],color=colors,height=0.55)
    ax.set_yticks(y,labels); ax.set_xlim(0,max(vals)*1.35)
    if t>=0.6:
        for yy,vv in zip(y,vals): ax.text(vv*ease(t)+max(vals)*0.02,yy,fmt(vv),va="center",color=FG,fontsize=26,weight="bold")

def kpis(f,items,t,y=0.45):
    n=len(items); w=0.88/n
    for i,(big,lab,col) in enumerate(items):
        a=ease((t-i*0.12)/0.5)
        if a<=0: continue
        x=0.06+i*w
        f.text(x,y+0.04*(1-a),big,color=col,fontsize=64,weight="bold",alpha=a)
        f.text(x,y-0.08+0.04*(1-a),lab,color=MUTED,fontsize=22,alpha=a,wrap=True)

m=lambda v: f"${v:,.1f} mil MM".replace(",","X").replace(".",",").replace("X",".")
