# Textos del Short «Calendario semanal de resultados»: meta de YouTube Shorts, posts (X, LinkedIn, TikTok, Instagram,
# Threads, Telegram) y guion.md. Uso: python3 gen_meta_cal.py <carpeta de la semana>
import json, sys, os
D = sys.argv[1]; S = json.load(open(f"{D}/calendario.json")); E = S["empresas"]
CANAL = "https://www.youtube.com/@AIAccionesEspa%C3%B1a"
AVISO = "Contenido informativo, no es recomendación de inversión."
CTA = S["fecha"] <= "2026-11-22"  # campaña «comenta y suscríbete» (Daniel, 8-nov-2026), hasta el 22-nov-2026
slug = f"calendario-{S['semana']}"


def linea(e, corta=False):
    k = []
    if e.get("bpa"): k.append(f"BPA {e['bpa']}")
    if e.get("beneficio"): k.append(f"beneficio neto {e['beneficio']}")
    if e.get("ebitda"): k.append(f"ebitda {e['ebitda']}")
    if e.get("ingresos"): k.append(f"ingresos {e['ingresos']}")
    cons = f" · consenso: {', '.join(k)}" if k else ""
    if corta: return f"{e['dia_corto']} · {e['nombre']} ({e['ticker']}){': ' + ', '.join(k) if k else ''}"
    return f"{e['dia_largo']} · {e['nombre']} ({e['ticker']}, {e['bolsa']}) · {e['hora'].lower()}{cons}"


lista = "\n".join("• " + linea(e) for e in E)
lista_corta = "\n".join("• " + linea(e, True) for e in E)
principal = S["gancho"].get("principal", E[0]["nombre"])
HT = "#Shorts #Resultados #Bolsa #IBEX35 #BolsaEspañola #Inversión #CalendarioDeResultados"
titulo = S.get("titulo") or f"Calendario de resultados ({S['semana_corta']}): {S['gancho']['titular'].splitlines()[0].replace('Esta semana reporta ', '').rstrip('…')} y {len(E)-1} más #Shorts"
assert len(titulo) <= 100, len(titulo)
desc = (f"Calendario semanal de resultados: {S['semana_txt'].lower()}. Las {len(E)} empresas más relevantes que presentan cuentas, "
        f"en orden cronológico, con lo que espera el mercado (consenso de analistas).\n\n{lista}\n\n"
        + (f"ℹ️ {S['nota_semana']}\n\n" if S.get("nota_semana") else "")
        + ("💬 Déjanos tu comentario y 🔔 suscríbete al canal.\n" if CTA else "")
        + f"Sigue el canal para el análisis de cada reporte: {CANAL}\n\n"
        f"Fuentes: {S['fuentes']}. Horas: España (Madrid) o del mercado de cada empresa. BPA = beneficio por acción (ajustado, según el consenso de cada fuente). "
        f"Las estimaciones pueden cambiar antes de la publicación.\n"
        f"Elaborado por AIAcciones España el {S['elaborado']} (hora de Madrid). {AVISO} No es asesoramiento personalizado. "
        f"AIAcciones España no tiene posiciones en las empresas citadas. Invertir conlleva riesgo de pérdida. Guion, gráficos y voz (sintética) generados con IA y revisados con las fuentes.\n\n{HT}")
assert "<" not in desc and ">" not in desc and len(desc.encode()) < 5000
tags = ["calendario de resultados", "resultados empresariales", "bolsa española", "IBEX 35", "Mercado Continuo", "consenso"] + [e["nombre"] for e in E] + ["Shorts"]
json.dump({"title": titulo, "description": desc, "tags": tags, "privacy": "public"}, open(f"{D}/meta-short.json", "w"), ensure_ascii=False, indent=1)

# X (280): el enlace al Short ({youtube} lo pone buffer.py)
x = f"📅 Resultados de la semana ({S['semana_corta']}): " + ", ".join(f"{e['nombre']} ({e['dia_corto'].lower()})" for e in E) + ".\n\n▶️ {youtube}\n\n" + AVISO
if len(x.replace("{youtube}", "x" * 23)) > 280:
    x = f"📅 Resultados {S['semana_corta']}: " + ", ".join(e["ticker"] for e in E) + ".\n\n▶️ {youtube}\n\n" + AVISO
assert len(x.replace("{youtube}", "x" * 23)) <= 280, len(x)
open(f"{D}/post-x.txt", "w").write(x)

# TikTok e Instagram Reels
tt = (f"📅 Calendario de resultados: {S['semana_txt'].lower()}.\n{lista_corta}\n\nSigue la cuenta para el análisis de cada reporte."
      + ("\n💬 Cuéntanos en comentarios cuál esperas más." if CTA else "")
      + f"\n{AVISO}\n#Bolsa #Resultados #Inversión #IBEX35 #BolsaEspañola #Finanzas")
assert len(tt) <= 2200
open(f"{D}/post-tiktok.txt", "w").write(tt)
ig = tt.replace("Sigue la cuenta", "Síguenos").replace("#Finanzas", "#Finanzas #Reels") + "\nVídeos completos en YouTube @AIAccionesEspaña."
open(f"{D}/post-instagram.txt", "w").write(ig)

# Threads (500)
th = f"📅 Resultados de la semana ({S['semana_corta']}):\n" + "\n".join(f"• {e['dia_corto']} {e['nombre']}" + (f": BPA {e['bpa']}" if e.get("bpa") else (f": beneficio {e['beneficio']}" if e.get("beneficio") else "")) for e in E) + f"\n\nSigue el canal para el análisis de cada reporte: {CANAL}\n{AVISO}"
assert len(th) <= 500, len(th)
open(f"{D}/post-threads.txt", "w").write(th)

# Telegram (texto largo, con el enlace al Short)
tg = (f"📅 CALENDARIO SEMANAL DE RESULTADOS\n{S['semana_txt']}\n\n{lista}\n\n" + (f"ℹ️ {S['nota_semana']}\n\n" if S.get("nota_semana") else "")
      + "▶️ Short: {youtube}\nSigue el canal para el análisis de cada reporte.\n\n" + f"{AVISO} AIAcciones España no tiene posiciones en las empresas citadas.\n\n#Resultados #Bolsa #IBEX35 #BolsaEspañola")
open(f"{D}/post-telegram.txt", "w").write(tg)

# LinkedIn (regla permanente, Daniel 8-nov-2026): el Short como vídeo; 3-4 datos clave + conclusión; transparencia; enlace al canal
L = S["linkedin"]; assert 3 <= len(L["datos"]) <= 4
li = (f"Calendario de resultados | {S['semana_txt']}\n\n" + "\n".join("• " + d for d in L["datos"]) + f"\n\n{L['conclusion']}\n\n"
      + ("💬 ¿Qué resultado esperas más? Déjanos tu comentario.\n\n" if CTA else "")
      + f"{AVISO} AIAcciones España no tiene posiciones en las empresas citadas.\n\nVídeo elaborado por AI Acciones España (@AIAccionesEspaña).\n{CANAL}")
assert "{youtube}" not in li and len(li) <= 2950
open(f"{D}/post-linkedin.txt", "w").write(li)

# Guion legible
T = json.load(open(f"{D}/times.json")) if os.path.exists(f"{D}/times.json") else None
g = [f"# Calendario semanal de resultados · {S['semana_txt']}\n", f"Duración: {T['total']} s\n" if T else "", "## Guion (locución)\n",
     f"1. **Gancho**: {S['gancho']['voz']}"]
g += [f"{i+2}. **{e['nombre']}** ({e['dia_largo']}, {e['hora'].lower()}): {e['voz']}" for i, e in enumerate(E)]
g += [f"{len(E)+2}. **Cierre**: {S['cierre']['voz']}", "\n## Datos y fuentes\n", lista, "", f"Fuentes: {S['fuentes']}.", ""]
if S.get("verificacion"): g += ["## Verificación\n"] + ["- " + v for v in S["verificacion"]] + [""]
g += ["## YouTube Shorts\n", f"**Título:** {titulo}\n", "**Descripción:**\n", "```", desc, "```", "",
      "## TikTok\n", "```", tt, "```", "## Instagram Reels\n", "```", ig, "```", "## Threads\n", "```", th, "```",
      "## Telegram\n", "```", tg, "```", "## LinkedIn (Short como vídeo)\n", "```", li, "```", "## X\n", "```", x, "```"]
open(f"{D}/guion.md", "w").write("\n".join(g))
print("ok", slug, "título:", titulo, "| desc", len(desc.encode()), "| threads", len(th), "| x", len(x))
