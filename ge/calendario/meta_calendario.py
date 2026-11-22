"""Metadatos y posts del Short semanal «Wochenkalender der Quartalszahlen» (Wall Street auf Deutsch), a partir de calendario.json.
uso: python3 meta_calendario.py <carpeta de la semana>
Escribe meta-youtube-calendario-<fecha>-GE.json y post-{tiktok,instagram,threads,telegram}-calendario-<fecha>-GE.txt.
Todos llevan «Keine Anlageberatung. Nur zu Informationszwecken.» y el aviso de IA (Reglamento de IA de la UE, art. 50)."""
import json, os, sys

CANAL = "https://www.youtube.com/channel/UC23KiHTq_lULliZwAM3dEpA"
AVISO = "Keine Anlageberatung. Nur zu Informationszwecken."
KI = "Text, Stimme und Grafiken mit KI erstellt."


def main():
    d = os.path.abspath(sys.argv[1]); S = json.load(open(os.path.join(d, "calendario.json"))); F = S["fecha"]
    emp = [e for e in S["escenas"] if e["tipo"] == "empresa"]
    prox = S["modo"] == "proximos"
    nombres = ", ".join(e["nombre"] for e in emp)
    def linea(e, corto=False):
        s = f"{e['dia']}: {e['nombre']} ({e['ticker']}), {e['momento']}"
        if e.get("estado") == "voraussichtlich": s += " (voraussichtlich)"
        if not corto and (e.get("umsatz") or e.get("eps")):
            k = [x for x in (e.get("umsatz") and f"Umsatz {e['umsatz']}", e.get("eps") and f"Gewinn je Aktie {e['eps']}") if x]
            s += " – Konsens: " + ", ".join(k)
        return s
    if prox:
        titulo = f"Quartalszahlen: Die nächsten Termine – {nombres}"
        intro = f"Wochenkalender der Quartalszahlen ({S['rango']}): Diese Woche legt keine unserer 22 US-Aktien Zahlen vor. Die nächsten Termine:"
    else:
        titulo = f"Quartalszahlen diese Woche: {nombres}"
        intro = f"Wochenkalender der Quartalszahlen ({S['rango']}): Diese Aktien aus unserer Liste legen Zahlen vor:"
    titulo = (titulo if len(titulo) <= 90 else titulo[:87].rsplit(",", 1)[0] + " …") + " #Shorts"
    fuentes = S["fuente"].replace("\n", " ")
    tags = ["Quartalszahlen", "Earnings", "Wall Street", "US-Aktien", "Börse", "Aktien", "Shorts"] + [e["nombre"] for e in emp]
    hashtags = "#Quartalszahlen #WallStreet #Aktien #Börse " + " ".join("#" + e["nombre"].replace(" ", "") for e in emp)
    lineas = "\n".join("• " + linea(e) for e in emp)
    desc = (f"{intro}\n{lineas}\n\nKonsens = Durchschnitt der Analystenschätzungen. Termine können sich ändern. "
            f"US-Börsenschluss: 16 Uhr New York = 22 Uhr deutscher Zeit.\n{fuentes}\n"
            f"{AVISO} Keine Kauf- oder Verkaufsempfehlung. {KI}\nKanal abonnieren: {CANAL}\n#Shorts {hashtags}")
    json.dump({"title": titulo, "description": desc[:5000], "tags": tags, "privacy": "public", "language": "de", "categoryId": "27"},
              open(os.path.join(d, f"meta-youtube-calendario-{F}-GE.json"), "w"), ensure_ascii=False, indent=1)
    social = f"📅 {intro}\n{lineas}\n\nFolge dem Kanal für die Analyse jeder Zahlenvorlage.\n🤖 {KI}\n{AVISO}\n{hashtags}"
    for red in ("tiktok", "instagram"):
        open(os.path.join(d, f"post-{red}-calendario-{F}-GE.txt"), "w").write(social)
    cortas = "\n".join("• " + linea(e, True) for e in emp)
    thr = f"📅 Quartalszahlen-Kalender ({S['rango']})\n" + ("Diese Woche: keine Zahlen unserer 22 US-Aktien. Als Nächstes:\n" if prox else "") + f"{cortas}\n\n{AVISO} Mit KI erstellt."
    if len(thr) > 500: sys.exit(f"Threads: {len(thr)} caracteres (máx. 500)")
    open(os.path.join(d, f"post-threads-calendario-{F}-GE.txt"), "w").write(thr)
    tg = (f"📅 Wall Street auf Deutsch | Wochenkalender der Quartalszahlen\n\n{intro}\n\n{lineas}\n\n▶️ Das Video: {{youtube}}\n"
          f"Unser YouTube-Kanal: {CANAL}\n\n{AVISO} Mit KI erstellt.")
    open(os.path.join(d, f"post-telegram-calendario-{F}-GE.txt"), "w").write(tg)
    print(titulo, f"({len(titulo)})"); print("threads", len(thr), "telegram", len(tg), "tiktok", len(social))


if __name__ == "__main__":
    main()
