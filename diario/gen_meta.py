# Genera meta-youtube.json, meta-short.json, posts (X, LinkedIn, TikTok/Instagram, Telegram) y miniatura del video diario del IPSA.
# Uso: python3 gen_meta.py <carpeta del día> [times.json]  (por defecto <carpeta>/times.json, que escribe make_video.py)
import json, sys, os, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams['text.parse_math']=False
D=sys.argv[1]; I=json.load(open(f"{D}/info.json")); T=dict(json.load(open(sys.argv[2] if len(sys.argv)>2 else f"{D}/times.json")))
slug=f"bolsa-{I['fecha']}"
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import campana
CAMP=("\n"+campana.DESCRIPCION) if campana.activa(I["fecha"]) else ""
WEB="https://aiacciones.cl/"; CAL="https://aiacciones.cl/calendario/"
mmss=lambda s:f"{int(s)//60}:{int(s)%60:02d}"
AVISO=f"""AVISO IMPORTANTE
• Elaborado por AIAcciones Chile el {I['elaborado']} (hora de Chile), con datos de la sesión del {I['fecha_txt']}. Se publica cada día hábil de la Bolsa de Santiago.
• Contenido informativo y educativo sobre información pública. No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoría de inversión personalizada: no considera tu situación financiera, objetivos ni tolerancia al riesgo. AIAcciones Chile no es un asesor de inversión inscrito en la CMF. Antes de invertir, consulta a un asesor o intermediario autorizado.
• Hechos y opiniones: las cifras provienen de información pública de las empresas (hechos esenciales y estados financieros en la CMF) y de las fuentes de mercado y prensa indicadas ({I['fuentes']}). Los cálculos propios están marcados como "calculado". No emitimos precio objetivo ni opinión sobre si una acción está cara o barata.
• Análisis técnico: medias móviles, RSI, estocástico y niveles de soporte y resistencia calculados con datos públicos de cierre. Describen el comportamiento pasado del precio; no son señales de compra o venta ni predicen la evolución futura.
• Conflictos de interés: AIAcciones Chile y sus autores no tienen posiciones en las acciones citadas, no reciben pago de las empresas y el contenido no se envía a ninguna empresa antes de publicarse. Cualquier cambio se indicará aquí.
• Riesgos: invertir en acciones implica riesgo de pérdida, incluso de todo el capital. Las rentabilidades pasadas no garantizan rentabilidades futuras. Los datos pueden contener errores; verifícalos en las fuentes originales.
• Producción: guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas."""
cap="\n".join(f"{mmss(T[k]) if i else '0:00'} {t}" for i,(k,t) in enumerate(I["capitulos"]))
desc=(f"{I['resumen']}\n📅 Calendario de resultados y dividendos: {CAL}{CAMP}\n\n"+"\n\n".join("• "+c for c in I["claves"])+
      f"\n\nCapítulos\n{cap}\n\nFuentes: {I['fuentes']}. AIAcciones Chile no tiene posiciones en las acciones citadas.\n\nMás análisis de acciones chilenas: {WEB}\n\n{AVISO}\n\n{I['hashtags']}")
assert len(I["titulo"])<=100 and "<" not in desc and ">" not in desc and len(desc.encode())<5000, (len(I["titulo"]),len(desc.encode()))
json.dump({"title":I["titulo"],"description":desc,"tags":I["tags"],"privacy":"public"},open(f"{D}/meta-youtube.json","w"),ensure_ascii=False,indent=1)
sd=(f"{I['resumen']}\nVideo completo (noticias, análisis fundamental y técnico): {{video:{slug}}}\n📅 {CAL}{CAMP}\n"
    f"Fuentes: {I['fuentes']}. Elaborado por AIAcciones Chile el {I['elaborado']} (hora de Chile). Contenido informativo: no es una recomendación de inversión ni asesoría personalizada. Análisis técnico: datos, no señales. Sin posiciones en las acciones citadas. Invertir conlleva riesgo de pérdida.\n#Shorts #IPSA #BolsaDeSantiago")
assert len(I["titulo_short"])<=100
json.dump({"title":I["titulo_short"],"description":sd,"tags":I["tags"][:6]+["Shorts"],"privacy":"public"},open(f"{D}/meta-short.json","w"),ensure_ascii=False,indent=1)
x=f"{I['x']}\n\n▶️ {{youtube}}\n📅 aiacciones.cl/calendario\nInformativo, no es recomendación."
assert len(x.replace("{youtube}","x"*23))<=270, len(x)
open(f"{D}/post-x.txt","w").write(x)
# LinkedIn (Daniel, 8-nov-2026): se publica el Short como video; texto con un resumen que aporte valor,
# aviso transparente de que el video es de AIAcciones Chile y el enlace al canal. Va en cola/<slug>-short/.
li=(f"📊 IPSA | La Bolsa de Santiago hoy ({I['fecha_txt']})\n\n{I['resumen']}\n\n"+"\n\n".join("• "+c for c in I["claves"])+
    "\n\n🎥 Este video corto es de AIAcciones Chile: resumimos cada sesión de la Bolsa de Santiago con datos públicos, noticias con fuente y análisis técnico, con guion, gráficos y voz generados con inteligencia artificial."
    "\n▶️ El análisis completo de unos 5 minutos y los resúmenes de cada día están en nuestro canal de YouTube: https://www.youtube.com/@aiaccioneschile"
    f"\n📅 Calendario de resultados y dividendos: {CAL}\n\n"
    "Contenido informativo, no es una recomendación de inversión. El análisis técnico describe datos, no son señales de compra o venta. AIAcciones Chile no tiene posiciones en las acciones citadas.\n\n"+I["hashtags"])
assert len(li)<=2950, len(li)
open(f"{D}/post-linkedin.txt","w").write(li)
tg=(f"📊 IPSA · {I['fecha_txt']}\n\n{I['resumen']}\n\n"+"\n".join("• "+c for c in I["claves"][:3])+
    f"\n\n▶️ Video: {{youtube}}\n📅 {CAL}\nYouTube: youtube.com/@aiaccioneschile\nContenido informativo, no es recomendación de inversión.")
open(f"{D}/post-telegram.txt","w").write(tg)
tk=I["tiktok"]
for need in ("aiacciones.cl","youtube.com/@aiaccioneschile"): assert need in tk, need
open(f"{D}/post-tiktok.txt","w").write(tk)
# miniatura 1280x720 con la fecha de la sesión destacada
BG="#0B1E3A"; FG="#FFFFFF"; MUTED="#9FB3CC"; ACC="#2FB7A3"; ACC2="#4C8DF0"; NEG="#F2A541"
th=I["miniatura"]
f=plt.figure(figsize=(12.8,7.2),dpi=100); f.patch.set_facecolor(BG)
f.patches.append(plt.Rectangle((0,0.76),0.66,0.24,transform=f.transFigure,color=ACC,figure=f))
f.text(0.04,0.925,"IPSA · SESIÓN DEL",color=BG,fontsize=26,weight="bold",va="center")
f.text(0.04,0.835,th["fecha"],color=BG,fontsize=44,weight="bold",va="center")
f.text(0.05,0.40,th["big"],color=NEG if th["big"].startswith("-") else ACC,fontsize=120,weight="bold")
f.text(0.05,0.30,th["sub"],color=FG,fontsize=26,weight="bold",va="top")
f.text(0.60,0.47,th["der"],color=ACC2,fontsize=38,weight="bold",linespacing=1.1)
f.text(0.60,0.24,th["der2"],color=FG,fontsize=28,weight="bold")
f.text(0.05,0.05,th["pie"],color=MUTED,fontsize=24,weight="bold")
p=f"{D}/miniatura-youtube.png"; f.savefig(p,dpi=100,facecolor=BG); plt.close(f)
im=Image.open(p).convert("RGBA"); lg=Image.open(os.environ.get("LOGO","/mnt/project-files/marca/logo-aiacciones-chile.png")).convert("RGBA")
w=380; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS); im.alpha_composite(lg,(1280-w-30,40)); im.convert("RGB").save(p)
print("ok",slug,len(desc.encode()),len(li),len(x))
