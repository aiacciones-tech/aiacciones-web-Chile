# Genera meta-youtube.json, meta-short.json, posts (X, LinkedIn, TikTok/Instagram, Telegram) y miniatura del vídeo diario.
# Uso: python3 gen_meta.py <carpeta del día> [times.json]  (por defecto <carpeta>/times.json, que escribe make_video.py)
import json, sys, os, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams['text.parse_math']=False
D=sys.argv[1]; I=json.load(open(f"{D}/info.json")); T=dict(json.load(open(sys.argv[2] if len(sys.argv)>2 else f"{D}/times.json")))
slug=f"bolsa-{I['fecha']}"
CANAL="https://www.youtube.com/@AIAccionesEspa%C3%B1a"
# Llamada a comentar y suscribirse (Daniel, 8-nov-2026), hasta el 22-nov-2026 incluido
CTA=I["fecha"]<="2026-11-22"
CTA_TXT="💬 ¿Qué te ha parecido el resumen de hoy y qué te gustaría ver? Déjanos tu comentario: nos ayuda a mejorar el canal.\n🔔 Suscríbete a @AIAccionesEspaña para no perderte el resumen de cada día de bolsa.\n\n" if CTA else ""
mmss=lambda s:f"{int(s)//60}:{int(s)%60:02d}"
AVISO=f"""AVISO IMPORTANTE
• Elaborado por AIAcciones España el {I['elaborado']} (hora de Madrid), con datos de la sesión del {I['fecha_txt']}. Se publica cada día de bolsa.
• Contenido informativo y educativo sobre información pública. No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoramiento personalizado: no tiene en cuenta tu situación, objetivos ni perfil de riesgo. Antes de invertir, consulta a una entidad autorizada por la CNMV.
• Hechos y opiniones: las cifras proceden de la información pública de las empresas en la CNMV y de las fuentes de mercado indicadas ({I['fuentes']}). Los cálculos propios están marcados como "calculado". No emitimos precio objetivo ni opinión sobre si una acción está cara o barata.
• Análisis técnico: medias móviles, RSI, estocástico y niveles de soporte y resistencia calculados con datos públicos de cierre. Describen el comportamiento pasado del precio; no son señales de compra o venta ni predicen la evolución futura.
• Conflictos de interés: AIAcciones España y sus autores no tienen posiciones en los valores citados, no reciben pago de las empresas y el contenido no se ha enviado a ninguna empresa antes de publicarse. Cualquier cambio se indicará aquí.
• Riesgos: invertir en bolsa implica riesgo de pérdida, incluso de todo el capital. Las rentabilidades pasadas no garantizan rentabilidades futuras. Los datos pueden contener errores; verifícalos en las fuentes originales.
• Producción: guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas."""
cap="\n".join(f"{mmss(T[k]) if i else '0:00'} {t}" for i,(k,t) in enumerate(I["capitulos"]))
# Cifra clave en el título (Daniel, 24-nov-2026): la variación del IBEX tiene que estar en los primeros 45 caracteres.
assert I["miniatura"]["big"] in I["titulo"][:45], f"el título debe llevar la cifra clave ({I['miniatura']['big']}) al principio"
# Enlaces al siguiente vídeo (las pantallas finales y tarjetas no se pueden poner por API): encolar.sh resuelve
# {ultimo:bolsa-} (la sesión anterior ya subida) y {lista:...} (listas de cola-es/listas.json); si no existen, borra la línea.
SIGUE=("▶️ Sesión anterior: {ultimo:bolsa-}\n📺 Todos los resúmenes diarios: {lista:diario}\n"
       "🎓 Curso «Análisis técnico, explicado fácil»: {lista:curso}\n\n")
desc=(f"{I['resumen']}\n📊 Hechos relevantes del IBEX 35: https://aiacciones.es/hechos/\n\n"+SIGUE+CTA_TXT+"\n\n".join("• "+c for c in I["claves"])+
      f"\n\nCapítulos\n{cap}\n\nFuentes: {I['fuentes']}. AIAcciones España no tiene posiciones en los valores citados.\n\n{AVISO}\n\n{I['hashtags']}")
assert len(I["titulo"])<=100 and "<" not in desc and ">" not in desc and len(desc.encode())+180<5000, (len(I["titulo"]),len(desc.encode()))  # +180: los enlaces que resuelve encolar.sh
json.dump({"title":I["titulo"],"description":desc,"tags":I["tags"],"privacy":"public"},open(f"{D}/meta-youtube.json","w"),ensure_ascii=False,indent=1)
sd=(f"{I['resumen']}\n"+("💬 Déjanos tu comentario y 🔔 suscríbete al canal.\n" if CTA else "")+f"Vídeo completo (noticias, análisis fundamental y técnico): {{video:{slug}}}\n📊 https://aiacciones.es/hechos/\n"
    f"Fuentes: {I['fuentes']}. Elaborado por AIAcciones España el {I['elaborado']} (hora de Madrid). Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado. Análisis técnico: datos, no señales. AIAcciones España no tiene posiciones en los valores citados. Invertir conlleva riesgo de pérdida.\n#Shorts #IBEX35 #Bolsa")
assert len(I["titulo_short"])<=100
sd=sd.replace("📊 https://aiacciones.es/hechos/\n","📊 https://aiacciones.es/hechos/\n📺 Más Shorts de la bolsa española: {lista:shorts}\n",1)
json.dump({"title":I["titulo_short"],"description":sd,"tags":I["tags"][:6]+["Shorts"],"privacy":"public"},open(f"{D}/meta-short.json","w"),ensure_ascii=False,indent=1)
x=f"{I['x']}\n\n▶️ {{youtube}}\n\nInformativo, no es recomendación. Sin posiciones."
assert len(x.replace("{youtube}","x"*23))<=280, len(x)
open(f"{D}/post-x.txt","w").write(x)
# Telegram: texto largo con todas las claves y el enlace al vídeo completo
tg=(f"IBEX 35 | La bolsa española hoy ({I['fecha_txt']})\n\n{I['resumen']}\n\n"+"\n\n".join("• "+c for c in I["claves"])+
    ("\n\n💬 Déjanos tu comentario en el vídeo y 🔔 suscríbete al canal." if CTA else "")+"\n\n▶️ Vídeo completo (3 min): {youtube}\n📊 Hechos relevantes del IBEX 35: https://aiacciones.es/hechos/\n\n"
    "Contenido informativo, no es una recomendación de inversión. El análisis técnico describe datos, no son señales de compra o venta. AIAcciones España no tiene posiciones en los valores citados.\n\n"+I["hashtags"])
open(f"{D}/post-telegram.txt","w").write(tg)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short subido como vídeo (encolar.sh lo pone en la carpeta -short),
# texto = 3 o 4 datos clave + una conclusión, sin relleno; transparencia sobre el canal; termina con el enlace al canal.
L=I["linkedin"]; assert 3<=len(L["datos"])<=4
li=(f"IBEX 35 | {I['fecha_txt'][0].upper()+I['fecha_txt'][1:]}\n\n"+"\n".join("• "+d for d in L["datos"])+f"\n\n{L['conclusion']}\n\n"
    +("💬 ¿Qué te ha parecido? Déjanos tu comentario para mejorar el canal y suscríbete.\n\n" if CTA else "")
    +"Contenido informativo, no es una recomendación de inversión. AIAcciones España no tiene posiciones en los valores citados.\n\n"
    +"Vídeo elaborado por AIAcciones España (@AIAccionesEspaña).\n"+CANAL)
assert "{youtube}" not in li and len(li)<=2950, len(li)
open(f"{D}/post-linkedin.txt","w").write(li)
open(f"{D}/post-tiktok.txt","w").write(I["tiktok"]+("\n💬 Cuéntanos en los comentarios qué te gustaría ver y síguenos." if CTA else ""))
# Miniaturas 1280x720. A = estilo «fecha» (franja con la fecha y la variación en grande); B = estilo «gancho»
# (el titular del día y la variación enorme). Prueba A/B automática (Daniel, 24-nov-2026): ab-espana.yml las alterna por días.
BG="#0B1E3A"; FG="#FFFFFF"; MUTED="#9FB3CC"; ACC="#2FB7A3"; ACC2="#4C8DF0"; NEG="#F2A541"
th=I["miniatura"]; COLB=NEG if th["big"].startswith("-") else ACC
def con_logo(p):
    im=Image.open(p).convert("RGBA"); lg=Image.open(os.environ.get("LOGO","/mnt/project-files/espana/marca/logo-aiacciones-espana.png"))
    w=400; lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS); im.alpha_composite(lg,(1280-w-30,30)); im.convert("RGB").save(p)
f=plt.figure(figsize=(12.8,7.2),dpi=100); f.patch.set_facecolor(BG)
f.patches.append(plt.Rectangle((0,0.80),0.62,0.20,transform=f.transFigure,color=ACC,figure=f))
f.text(0.04,0.93,"IBEX 35 · SESIÓN DEL",color=BG,fontsize=24,weight="bold",va="center")
f.text(0.04,0.85,th["fecha"],color=BG,fontsize=40,weight="bold",va="center")
f.text(0.05,0.40,th["big"],color=COLB,fontsize=120,weight="bold")
f.text(0.05,0.30,th["sub"],color=FG,fontsize=26,weight="bold",va="top")
f.text(0.60,0.47,th["der"],color=ACC2,fontsize=38,weight="bold",linespacing=1.1)
f.text(0.60,0.24,th["der2"],color=FG,fontsize=28,weight="bold")
f.text(0.05,0.05,th["pie"],color=MUTED,fontsize=24,weight="bold")
p=f"{D}/miniatura-youtube.png"; f.savefig(p,dpi=100,facecolor=BG); plt.close(f); con_logo(p)
# B: «gancho». th["gancho"] (opcional, 2-6 palabras, p. ej. "La banca tira") o el titular corto de info.json.
import textwrap
g=th.get("gancho") or I.get("gancho") or th["pie"].split("|")[0].strip()
gl=textwrap.wrap(g.upper(),16)[:2]
f=plt.figure(figsize=(12.8,7.2),dpi=100); f.patch.set_facecolor(BG)
f.text(0.05,0.88,"IBEX 35 HOY",color=MUTED,fontsize=30,weight="bold",va="center")
f.text(0.05,0.60,"\n".join(gl),color=FG,fontsize=66 if max(len(x) for x in gl)<=12 else 54,weight="bold",va="center",linespacing=1.05)
f.text(0.05,0.10,th["big"],color=COLB,fontsize=170,weight="bold")
f.text(0.97,0.06,th.get("fecha_corta",I["fecha_corta"]),color=MUTED,fontsize=30,weight="bold",ha="right")
pb=f"{D}/miniatura-youtube-b.png"; f.savefig(pb,dpi=100,facecolor=BG); plt.close(f); con_logo(pb)
# Título B: el gancho delante y la fecha al final; la cifra clave sigue al principio.
tb=I.get("titulo_b") or f"IBEX 35 {th['big']}: {g} | Bolsa española hoy ({I['fecha_corta']})"
assert len(tb)<=100 and th["big"] in tb[:45], ("titulo_b", len(tb))
json.dump({"que":"ambos","B":{"title":tb,"miniatura":"miniatura-b.png"},"estilos":{"A":"fecha","B":"gancho"}},
          open(f"{D}/ab.json","w"),ensure_ascii=False,indent=1)
# Segundo Short (Daniel, 24-nov-2026: 2-3 Shorts por vídeo largo): short2.json, otro ángulo del día (el técnico del IBEX
# o el valor protagonista). Solo YouTube; encolar.sh lo deja programado para la mañana siguiente (canal-espana.yml lo sube).
if os.path.exists(f"{D}/short2.json"):
    t2=I["titulo_short2"]; assert len(t2)<=100 and "#Shorts" in t2, "titulo_short2 (≤100 caracteres, con #Shorts)"
    sd2=(f"{I.get('resumen_short2',I['resumen'])}\nVídeo completo de la sesión: {{video:{slug}}}\n📺 Más Shorts de la bolsa española: {{lista:shorts}}\n"
         f"Fuentes: {I['fuentes']}. Elaborado por AIAcciones España el {I['elaborado']} (hora de Madrid). Contenido informativo: no es una recomendación de inversión ni asesoramiento personalizado. Análisis técnico: datos, no señales. AIAcciones España no tiene posiciones en los valores citados. Invertir conlleva riesgo de pérdida.\n#Shorts #IBEX35 #Bolsa")
    json.dump({"title":t2,"description":sd2,"tags":I["tags"][:6]+["Shorts"],"privacy":"public"},open(f"{D}/meta-short2.json","w"),ensure_ascii=False,indent=1)
print("ok",slug,len(desc.encode()),len(li),len(x))
