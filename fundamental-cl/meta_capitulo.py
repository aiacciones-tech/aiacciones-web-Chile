# Metadatos de YouTube (video y Short), posts (X, LinkedIn con el Short, TikTok, Telegram) y miniatura de un capítulo de la serie
# semanal «Análisis fundamental en simple» de AIAcciones Chile. Uso: python3 meta_capitulo.py <carpeta del capítulo>  (lee video.json y times.json)
# Reglas del canal: enlace a aiacciones.cl y a youtube.com/@aiaccioneschile en todo (Daniel, 20-oct y 8-nov-2026), títulos ≤100 sin clickbait,
# nada de comprar/vender ni precio objetivo (NCG 502), LinkedIn = el Short como video con resumen y mención de AIAcciones Chile.
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_fund import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
BASE = VJ["base"]; I = VJ["info"]; N = VJ["capitulo_n"]
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
CTA = ("\n" + campana.DESCRIPCION.replace("este resumen diario", "esta serie")) if cta_activa(VJ["publicar"]) else ""
dur = round(T_.get("_total", 0) / 60)
AVISO = f"""AVISO IMPORTANTE
• Contenido educativo e informativo de la serie «{SERIE}». No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoría de inversión personalizada: no considera tu situación financiera, objetivos ni tolerancia al riesgo. {VJ['nombre']} es solo un ejemplo para explicar el concepto; elegirla no implica una opinión sobre la acción. AIAcciones Chile no es un asesor de inversión inscrito en la CMF. Antes de invertir, consulta a un asesor o intermediario autorizado.
• Las cifras provienen de los informes oficiales de la empresa (estados financieros y comunicados de resultados) y de TradingView, según se indica. Los cálculos propios están marcados como "calculado". No emitimos precio objetivo ni opinión sobre si una acción está cara o barata.
• Conflictos de interés: AIAcciones Chile y sus autores no tienen posiciones en las acciones citadas y no reciben pago de las empresas.
• Riesgos: invertir en acciones implica riesgo de pérdida, incluso de todo el capital. Las rentabilidades pasadas no garantizan rentabilidades futuras. Los datos pueden contener errores; verifícalos en las fuentes originales.
• Producción: guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas."""
serie_txt = f"Serie «{SERIE}»: un capítulo cada domingo, un concepto de análisis fundamental explicado con las cifras reales de una empresa del IPSA."
desc = (f"{I['resumen']}{CTA}\n\n" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nCapítulos\n{cap}\n\nFuentes: {I['fuentes']}.\n\n{serie_txt}"
        + (f" Próximo capítulo: {fin['siguiente']}." if fin.get("siguiente") else "") + f"\n\nMás análisis de acciones chilenas: {WEB}\nCanal: {CANAL}\n\n{AVISO}\n\n{I['hashtags']}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc.encode()) < 5000, (len(I["titulo"]), len(desc.encode()))
tags = list(dict.fromkeys([SERIE, "análisis fundamental", "acciones chilenas", "IPSA", "Bolsa de Santiago", "AIAcciones Chile", VJ["nombre"], VJ["ticker"], VJ["tema"]] + I.get("tags", [])))
json.dump({"title": I["titulo"], "description": desc, "tags": tags, "privacy": "public", "language": "es", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['resumen']}{CTA}\nCapítulo completo ({dur} minutos): {{video:{BASE}}}\nFuentes: {I['fuentes']}. Contenido educativo: no es una recomendación de inversión. "
      f"Sin posiciones en las acciones citadas. Invertir conlleva riesgo de pérdida. Hecho con inteligencia artificial.\n{WEB}\n{CANAL}\n{I['hashtags_short']}")
assert len(I["titulo_short"]) <= 100 and len(sd.encode()) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": tags[:8] + ["Shorts"], "privacy": "public", "language": "es", "categoryId": "27"},
          open(f"{D}/meta-short-{BASE}.json", "w"), ensure_ascii=False, indent=1)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
try:
    from buffer import largo_x
except Exception:
    largo_x = lambda s: len(re.sub(r"https?://\S+", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n🌐 aiacciones.cl\nEducativo, no es recomendación."
lx = largo_x(x.replace("{youtube}", "https://youtu.be/XXXXXXXXXXX")); assert lx <= 280, lx
open(f"{D}/post-x-{BASE}.txt", "w").write(x)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short como video; resumen con valor; aviso de que el video es de AIAcciones Chile; enlace al canal.
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4, "LinkedIn: 3 o 4 datos clave"
lk = (f"📚 {SERIE} | Capítulo {N}: {VJ['tema']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in L["datos"]) + f"\n\nEn resumen: {L['conclusion']}\n\n"
      f"🎥 Este video corto es de AIAcciones Chile: cada domingo explicamos un concepto de análisis fundamental con las cifras reales de una empresa del IPSA, con guion, gráficos y voz generados con inteligencia artificial."
      f"\n▶️ El capítulo completo de unos {dur} minutos está en nuestro canal de YouTube: {CANAL}\n🌐 {WEB}\n\n"
      "Contenido educativo, no es una recomendación de inversión. AIAcciones Chile no tiene posiciones en las acciones citadas.\n\n" + I["hashtags"])
assert len(lk) <= 2950 and "{youtube}" not in lk
open(f"{D}/post-linkedin-{BASE}.txt", "w").write(lk)
tk = (f"{SERIE} · Capítulo {N}: {VJ['tema']}\n{I['x']}\n▶️ Capítulo completo en YouTube: youtube.com/@aiaccioneschile\n🌐 aiacciones.cl\n"
      f"🤖 Hecho con inteligencia artificial (guion, voz y gráficos). Contenido educativo, no es recomendación de inversión. {VJ['nombre']} es solo un ejemplo. Invertir conlleva riesgo.\n{I['hashtags_short']}")
assert len(tk) <= 2200 and "aiacciones.cl" in tk and "youtube.com/@aiaccioneschile" in tk
open(f"{D}/post-tiktok-{BASE}.txt", "w").write(tk)
tg = (f"📚 {SERIE} | Capítulo {N}: {VJ['tema']} ({VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ Video: {{youtube}}\n🌐 {WEB}\nYouTube: youtube.com/@aiaccioneschile\nContenido educativo, no es recomendación de inversión.")
assert len(tg) <= 1000, len(tg)
open(f"{D}/post-telegram-{BASE}.txt", "w").write(tg)

# Miniatura 1280x720: banda con la serie y el capítulo, el concepto grande y hasta tres cifras clave
th = VJ["miniatura"]; f = fig(1280, 720)
f.patches.append(plt.Rectangle((0, 0.80), 0.70, 0.20, transform=f.transFigure, color=ACC, figure=f))
f.text(0.04, 0.90, th["etiqueta"], color=BG, fontsize=30, weight="bold", va="center")
f.text(0.04, 0.64, th["titulo"], color=FG, fontsize=62 if len(th["titulo"]) <= 22 else 48, weight="bold", va="center")
f.text(0.04, 0.515, th["sub"], color=MUTED, fontsize=28, weight="bold", va="center")
for i, (big, lab, c) in enumerate(th.get("cifras", [])[:3]):
    xx = 0.04 + i * 0.31
    f.text(xx, 0.25, big, color=col(c), fontsize=64, weight="bold")
    f.text(xx, 0.18, lab, color=FG, fontsize=22, weight="bold")
f.text(0.04, 0.05, th["pie"], color=ACC2, fontsize=22, weight="bold")
p = f"{D}/miniatura-{BASE}.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA"); w = 330
lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS); im.alpha_composite(lg, (1280 - w - 30, 30)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc.encode()), "linkedin", len(lk), "telegram", len(tg), "x", lx)
