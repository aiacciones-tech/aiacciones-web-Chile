# Metadatos de YouTube (vídeo y Short), posts (X, LinkedIn, TikTok, Instagram, Telegram), miniaturas A y B y ab.json de un vídeo fijo
# de @AIAccionesEspaña (espana/fijos/, Daniel 24-nov-2026: vídeos para lo que la gente busca, p. ej. «dividendos IBEX 2027»).
# Uso: python3 espana/fijos/meta_fijo.py <carpeta>   (lee video.json y times.json de make_leccion.py)
import json, os, re, sys, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "educativo"))
from comun_leccion import *

D = os.path.abspath(sys.argv[1]); VJ = json.load(open(f"{D}/video.json")); T_ = dict(json.load(open(f"{D}/times.json")))
BASE = VJ["base"]; I = VJ["info"]; slug = f"fijo-{BASE}"
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
fin = next(e for e in VJ["escenas"] if e["tipo"] == "fin")
cap = "\n".join(f"{mmss(T_[e['id']]) if i else '0:00'} {e['capitulo']}" for i, e in enumerate(VJ["escenas"]) if e.get("capitulo") and e["id"] in T_)
AVISO = f"""AVISO IMPORTANTE
• Elaborado por AIAcciones España el {I['elaborado']} con datos públicos hasta esa fecha ({I['fuentes']}). Las cifras pueden cambiar: verifícalas en las fuentes originales.
• Contenido informativo y educativo sobre información pública. No es una recomendación de inversión, ni una invitación a comprar o vender valores, ni asesoramiento personalizado: no tiene en cuenta tu situación, objetivos ni perfil de riesgo. Antes de invertir, consulta a una entidad autorizada por la CNMV.
• Los cálculos propios están marcados como "calculado". No emitimos precio objetivo ni opinión sobre si una acción está cara o barata. Las rentabilidades pasadas no garantizan rentabilidades futuras.
• Conflictos de interés: AIAcciones España y sus autores no tienen posiciones en los valores citados y no reciben pago de las empresas.
• Riesgos: invertir en bolsa implica riesgo de pérdida, incluso de todo el capital.
• Producción: guion, gráficos y locución (voz sintética) generados con herramientas de inteligencia artificial y revisados con las fuentes citadas."""
sigue = "📺 Más guías de la bolsa española: {lista:guias}\n📈 El IBEX 35 cada día de bolsa: {lista:diario}\n\n"
desc = (f"{I['resumen']}\n\n{sigue}" + "\n".join("• " + c for c in fin["claves"]) + f"\n\nCapítulos\n{cap}\n\n" +
        "".join(f"📄 {t}: {u}\n" for t, u in I.get("enlaces", [])) + f"\nFuentes: {I['fuentes']}\n\n{AVISO}\n\n{I['hashtags']}\n\nSuscríbete: {CANAL}")
assert len(I["titulo"]) <= 100 and "<" not in desc and ">" not in desc and len(desc.encode()) + 180 < 5000, (len(I["titulo"]), len(desc.encode()))
tags = list(dict.fromkeys(I.get("tags", []) + ["AIAcciones España", "bolsa española", "IBEX 35"]))
json.dump({"title": I["titulo"], "description": desc, "tags": tags, "privacy": "public", "language": "es", "categoryId": "27"},
          open(f"{D}/meta-youtube-{BASE}.json", "w"), ensure_ascii=False, indent=1)
sd = (f"{I['tiktok']}\nVídeo completo: {{video:{slug}}}\n📺 Más guías: {{lista:guias}}\n"
      f"Contenido informativo, no es una recomendación de inversión. AIAcciones España no tiene posiciones en los valores citados. "
      f"Hecho con IA.\nSuscríbete: {CANAL}\n{I['hashtags_short']}")
assert len(I["titulo_short"]) <= 100 and len(sd.encode()) < 4800
json.dump({"title": I["titulo_short"], "description": sd, "tags": tags[:8] + ["Shorts"], "privacy": "public", "language": "es", "categoryId": "27"},
          open(f"{D}/meta-short-{BASE}.json", "w"), ensure_ascii=False, indent=1)
largo_x = lambda s: len(re.sub(r"https?://\S+|\{youtube\}", "x" * 23, s))
x = f"{I['x']}\n\n▶️ {{youtube}}\n\nInformativo, no es recomendación. Sin posiciones."
assert largo_x(x) <= 280, largo_x(x)
open(f"{D}/post-x-{BASE}.txt", "w").write(x)
MIN = max(1, round(T_["_total"] / 60))
tg = (f"📚 {VJ['tema']}\n\n{I['resumen']}\n\n" + "\n".join("• " + c for c in fin["claves"]) +
      f"\n\n▶️ Vídeo completo ({MIN} min): {{youtube}}\n\nContenido informativo, no es una recomendación de inversión. "
      f"AIAcciones España no tiene posiciones en los valores citados.\n\n{I['hashtags']}")
assert len(tg) <= 2000, len(tg)
open(f"{D}/post-telegram-{BASE}.txt", "w").write(tg)
# LinkedIn (regla permanente de Daniel, 8-nov-2026): el Short como vídeo nativo, 3-4 datos + conclusión, autoría y enlace al canal al final.
L = I["linkedin"]; assert 3 <= len(L["datos"]) <= 4
li = (f"{VJ['tema']}\n\n" + "\n".join("• " + d for d in L["datos"]) + f"\n\n{L['conclusion']}\n\n"
      "Contenido informativo, no es una recomendación de inversión. AIAcciones España no tiene posiciones en los valores citados.\n\n"
      "Vídeo elaborado por AIAcciones España (@AIAccionesEspaña).\n" + CANAL)
assert "{youtube}" not in li and len(li) <= 2950 and li.endswith(CANAL), len(li)
open(f"{D}/post-linkedin-{BASE}.txt", "w").write(li)
tk = f"{I['tiktok']}\nInformativo, no es recomendación de inversión. Sin posiciones. Hecho con IA.\n{I['hashtags_short']}"
assert len(tk) <= 2200
open(f"{D}/post-tiktok-{BASE}.txt", "w").write(tk); open(f"{D}/post-instagram-{BASE}.txt", "w").write(tk)

# Miniaturas 1280x720 (cifra clave en grande; Daniel 24-nov-2026). A: franja con la etiqueta, título y la cifra; B: pregunta o gancho y la cifra enorme.
th = VJ["miniatura"]


def con_logo(p):
    im = Image.open(p).convert("RGBA"); lg = Image.open(LOGO).convert("RGBA"); w = 360
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS); im.alpha_composite(lg, (1280 - w - 30, 30)); im.convert("RGB").save(p)


f = fig(1280, 720)
f.patches.append(plt.Rectangle((0, 0.80), 0.66, 0.20, transform=f.transFigure, color=ACC, figure=f))
f.text(0.04, 0.90, th["etiqueta"].upper(), color=BG, fontsize=30, weight="bold", va="center")
tl = textwrap.wrap(th["titulo"], 18)[:2]
f.text(0.04, 0.60, "\n".join(tl), color=FG, fontsize=60 if max(map(len, tl)) <= 14 else 50, weight="bold", va="center", linespacing=1.05)
f.text(0.04, 0.10, th["cifra"], color=col(th.get("color", "acc")), fontsize=150 if len(th["cifra"]) <= 7 else 110, weight="bold")
if th.get("sub"): f.text(0.04, 0.40, th["sub"], color=MUTED, fontsize=34, weight="bold")
p = f"{D}/miniatura-{BASE}.png"; f.savefig(p, dpi=100, facecolor=BG); plt.close(f); con_logo(p)
if th.get("gancho_b"):
    f = fig(1280, 720)
    gl = textwrap.wrap(th["gancho_b"].upper(), 16)[:3]
    f.text(0.04, 0.62, "\n".join(gl), color=FG, fontsize=64 if max(map(len, gl)) <= 12 else 52, weight="bold", va="center", linespacing=1.05)
    f.text(0.04, 0.07, th["cifra"], color=col(th.get("color", "acc")), fontsize=170 if len(th["cifra"]) <= 7 else 120, weight="bold")
    pb = f"{D}/miniatura-b-{BASE}.png"; f.savefig(pb, dpi=100, facecolor=BG); plt.close(f); con_logo(pb)
    tb = I.get("titulo_b")
    assert tb and len(tb) <= 100 and tb != I["titulo"], "titulo_b (≤100, distinto del A) para la prueba A/B"
    json.dump({"que": "ambos", "B": {"title": tb, "miniatura": "miniatura-b.png"}, "estilos": {"A": "fijo-titulo", "B": "fijo-gancho"}},
              open(f"{D}/ab-{BASE}.json", "w"), ensure_ascii=False, indent=1)
print("ok", BASE, "desc", len(desc.encode()), "li", len(li), "tg", len(tg), "x", largo_x(x), "titulo", len(I["titulo"]))
