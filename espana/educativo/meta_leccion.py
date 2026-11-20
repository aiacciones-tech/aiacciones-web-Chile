# Metadatos de YouTube (vídeo y Short), posts (X, LinkedIn, TikTok, Instagram, Telegram) y miniatura de una lección de
# «Análisis técnico, explicado fácil» (AIAcciones España). Mismo formato y aviso que el vídeo diario (espana/diario/gen_meta.py).
# Uso: VELAS=<velas.json> python3 meta_leccion.py <carpeta de la lección>   (lee video.json y times.json de make_leccion.py)
import json, os, re, sys, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_leccion import *
from voz_leccion import cta

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
BASE = VJ["base"]; I = VJ["info"]; N = VJ["capitulo_n"]; slug = f"curso-{BASE}"
CTA = cta(VJ)
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
ult = dt.date.fromisoformat(VJ["ultima_vela"])
AVISO = f"""AVISO IMPORTANTE
• Contenido educativo e informativo sobre información pública. No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoramiento personalizado: no tiene en cuenta tu situación, objetivos ni perfil de riesgo. Antes de invertir, consulta a una entidad autorizada por la CNMV. {VJ['nombre']} es solo un ejemplo para explicar el concepto.
• Análisis técnico: describe el comportamiento pasado del precio; no predice la evolución futura. La situación actual se presenta como condiciones, no como previsión. Las zonas y líneas dibujadas no son precios objetivo.
• Datos: {I['fuentes']}. Medias, indicadores y zonas: calculado por AIAcciones España. Los datos pueden contener errores; verifícalos en las fuentes originales.
• Conflictos de interés: AIAcciones España y sus autores no tienen posiciones en el valor citado y no reciben pago de las empresas.
• Riesgos: invertir en bolsa implica riesgo de pérdida, incluso de todo el capital. Las rentabilidades pasadas no garantizan rentabilidades futuras.
• Producción: guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas."""
cta_desc = ("💬 ¿Qué concepto quieres que expliquemos? Déjanos tu comentario: nos ayuda a mejorar el canal.\n"
            "🔔 Suscríbete a @AIAccionesEspaña para no perderte ningún capítulo.\n\n") if CTA else ""
serie = (f"«{SERIE}»: cada domingo, un concepto de análisis técnico explicado sobre el gráfico real de {VJ['nombre']}, la mayor empresa del IBEX 35."
         + (f" Próximo capítulo: {fin['siguiente']}." if fin.get("siguiente") else ""))
desc = (f"{I['resumen']}\n\n{cta_desc}" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nCapítulos\n{cap}\n\n{serie}\n\n" +
        (f"📊 Ficha de {VJ['nombre']}: {I['ficha']}\n" if I.get("ficha") else "") + f"📚 Aprende bolsa en la web: https://aiacciones.es/educacion/\n\n{AVISO}\n\n{I['hashtags']}\n\nSuscríbete: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc.encode()) < 5000, (len(I["titulo"]), len(desc.encode()))
tags = list(dict.fromkeys(I.get("tags", []) + [SERIE, "AIAcciones España", "análisis técnico", VJ["nombre"], "IBEX 35"]))
json.dump({"title": I["titulo"], "description": desc, "tags": tags, "privacy": "public", "language": "es", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['tiktok']}\n" + ("💬 Déjanos tu comentario y 🔔 suscríbete al canal.\n" if CTA else "") +
      f"Capítulo completo ({VJ['tema'].lower()}): {{video:{slug}}}\n"
      f"Contenido educativo, no es una recomendación de inversión. El análisis técnico describe el pasado y no predice el futuro. "
      f"AIAcciones España no tiene posiciones en {VJ['nombre']}. Hecho con herramientas de IA.\nSuscríbete: {CANAL}\n{I['hashtags_short']}")
assert len(I["titulo_short"]) <= 100 and len(sd) < 5000
json.dump({"title": I["titulo_short"], "description": sd, "tags": tags[:8] + ["Shorts"], "privacy": "public", "language": "es", "categoryId": "27"},
          open(f"{D}/meta-short-{BASE}.json", "w"), ensure_ascii=False, indent=1)
# X (máx. 280, los enlaces cuentan 23)
largo_x = lambda s: len(re.sub(r"https?://\S+|\{youtube\}", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n\nEducativo, no es recomendación. Sin posiciones."
assert largo_x(x) <= 280, largo_x(x)
open(f"{D}/post-x-{BASE}.txt", "w").write(x)
MIN = max(1, round(T_["_total"] / 60))
tg = (f"📚 {SERIE} | Capítulo {N}: {VJ['tema']} (con el gráfico de {VJ['nombre']})\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      ("\n\n💬 Déjanos tu comentario en el vídeo y 🔔 suscríbete al canal." if CTA else "") +
      f"\n\n▶️ Capítulo completo ({MIN} min): {{youtube}}\n\nContenido educativo, no es una recomendación de inversión. El análisis técnico describe el pasado y no predice el futuro. "
      f"AIAcciones España no tiene posiciones en {VJ['nombre']}.\n\n{I['hashtags']}")
assert len(tg) <= 2000, len(tg)
open(f"{D}/post-telegram-{BASE}.txt", "w").write(tg)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short como vídeo nativo (encolar.sh lo pone en la carpeta -short),
# 3 o 4 datos clave + una conclusión, sin relleno; transparencia sobre quién lo hace; termina con el enlace al canal.
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4
li = (f"{SERIE} | Capítulo {N}: {VJ['tema']}\n\n" + "\n".join("• " + d for d in L["datos"]) + f"\n\n{L['conclusion']}\n\n" +
      ("💬 ¿Qué concepto quieres que expliquemos? Déjanos tu comentario y suscríbete.\n\n" if CTA else "") +
      f"Contenido educativo, no es una recomendación de inversión. AIAcciones España no tiene posiciones en {VJ['nombre']}.\n\n"
      "Vídeo elaborado por AIAcciones España (@AIAccionesEspaña).\n" + CANAL)
assert "{youtube}" not in li and len(li) <= 2950 and li.endswith(CANAL), len(li)
open(f"{D}/post-linkedin-{BASE}.txt", "w").write(li)
tk = (f"{I['tiktok']}\n" + ("💬 Cuéntanos qué concepto quieres que expliquemos y síguenos.\n" if CTA else "") +
      f"Educativo, no es recomendación de inversión. Sin posiciones en {VJ['nombre']}. Hecho con IA.\n{I['hashtags_short']}")
assert len(tk) <= 2200
open(f"{D}/post-tiktok-{BASE}.txt", "w").write(tk); open(f"{D}/post-instagram-{BASE}.txt", "w").write(tk)

# Miniatura 1280x720: serie y capítulo en la banda, tema en grande, gráfico real con las líneas de la escena elegida
th = VJ["miniatura"]; VEL = json.load(open(os.environ.get("VELAS", f"{D}/velas.json")))["series"][VJ["simbolo"]]["velas"]
fv = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
VEL = [v for v in VEL if fv(v["t"]) <= VJ["ultima_vela"]]; IND = indicadores(VEL); F = [fv(v["t"]) for v in VEL]
g = next((e for e in VJ["escenas"] if e["id"] == th.get("grafico")), next(e for e in VJ["escenas"] if e["tipo"] == "grafico"))
J = [j for j, d in enumerate(F) if g.get("desde", "0") <= d <= g.get("hasta", "9")]; V = [VEL[j] for j in J]
f = fig(1280, 720)
f.patches.append(plt.Rectangle((0, 0.84), 1.0, 0.16, transform=f.transFigure, color=ACC, figure=f))
f.text(0.04, 0.92, th["etiqueta"], color=BG, fontsize=26, weight="bold", va="center")
f.text(0.04, 0.715, th["titulo"], color=FG, fontsize=72 if len(th["titulo"]) <= 16 else 56, weight="bold", va="center")
f.text(0.04, 0.585, th["sub"], color=NEG, fontsize=28, weight="bold", va="center")
ax = f.add_axes([0.03, 0.03, 0.94, 0.48]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
o = np.array([v["o"] for v in V]); c = np.array([v["c"] for v in V]); h = np.array([v["h"] for v in V]); l = np.array([v["l"] for v in V]); xs = np.arange(len(V))
cc = [ACC if a >= b else NEG for a, b in zip(c, o)]
ax.vlines(xs, l, h, color=cc, lw=1.2, alpha=0.7); ax.bar(xs, np.maximum(abs(c - o), (h.max() - l.min()) * 0.004), bottom=np.minimum(o, c), color=cc, width=0.7, alpha=0.7)
for ln in g.get("lineas", []): ax.plot(xs, IND[ln["ind"]][J], color=col(ln.get("color", "acc2")), lw=5)
pos = {d: k for k, d in enumerate(F[J[0]:J[-1] + 1])}
for m in g.get("marcas", []):
    if m.get("tipo") == "cruce" and m["fecha"] in pos and g.get("lineas"):
        k = pos[m["fecha"]]; ax.plot([k], [IND[g["lineas"][0]["ind"]][J][k]], "o", ms=34, mfc="none", mec=FG, mew=5)
ax.set_xlim(-1, len(V))
p = f"{D}/miniatura-{BASE}.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f)
im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA"); w = 330
lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS); im.alpha_composite(lg, (1280 - w - 30, 140)); im.convert("RGB").save(p)
print("ok", BASE, "desc", len(desc.encode()), "li", len(li), "tg", len(tg), "x", largo_x(x), "titulo", len(I["titulo"]))
