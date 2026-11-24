"""Metadatos de YouTube y posts de TikTok e Instagram del Short diario «DAX am Abend» (Wall Street auf Deutsch), a partir de short.json.
uso: python3 ge/dax/meta_dax.py <carpeta del día>
Lee de short.json, además de las escenas: "titulo_yt" (≤ 90 caracteres, sin #Shorts), "resumen" (2-3 frases con las cifras del día),
"claves" (3-4 viñetas cortas) y "fuente". Escribe meta-youtube-dax-<fecha>-GE.json y post-{tiktok,instagram}-dax-<fecha>-GE.txt.
Llevan el aviso legal y el de IA (Reglamento de IA de la UE, art. 50) y una invitación al Tagesbericht de Wall Street de la noche."""
import json, os, sys

CANAL = "https://www.youtube.com/channel/UC23KiHTq_lULliZwAM3dEpA"
AVISO = ("Keine Anlageberatung. Nur Information und Bildung. Keine Kauf- oder Verkaufsempfehlung. Keine Positionen in den genannten Aktien. "
         "Aktien sind mit Risiken bis zum Totalverlust verbunden. Charttechnik beschreibt Daten und ist kein Kauf- oder Verkaufssignal.")
KI = "Text, Stimme und Grafiken mit KI erstellt."
HASH = "#DAX #Börse #Aktien #Xetra #DAX40"


def main():
    d = os.path.abspath(sys.argv[1]); S = json.load(open(os.path.join(d, "short.json"))); F = S["fecha"]
    t = S["titulo_yt"].strip()
    assert len(t) <= 90, f"titulo_yt demasiado largo ({len(t)})"
    titulo = t + " #Shorts"
    fuente = S["fuente"].replace("\n", " ")
    claves = "\n".join("• " + c for c in S["claves"])
    desc = (f"{S['resumen']}\n\n{claves}\n\n{fuente}\nHeute Abend nach US-Börsenschluss: Der Tagesbericht zur Wall Street auf unserem Kanal.\n\n"
            f"{AVISO}\n{KI}\n\nKanal abonnieren: {CANAL}\n#Shorts {HASH}")
    assert len(desc) < 5000 and "<" not in desc and ">" not in desc
    tags = ["DAX", "DAX 40", "Börse", "Aktien", "Xetra", "Deutsche Aktien", "Börse Frankfurt", "Shorts"] + S.get("tags", [])
    json.dump({"title": titulo, "description": desc, "tags": tags[:15], "privacy": "public", "language": "de", "categoryId": "27"},
              open(os.path.join(d, f"meta-youtube-dax-{F}-GE.json"), "w"), ensure_ascii=False, indent=1)
    social = (f"🇩🇪 {S['resumen']}\n{claves}\n\nUnser YouTube-Kanal: {CANAL}\n🤖 {KI}\n"
              f"Keine Anlageberatung, nur Information und Bildung. Risiko bis zum Totalverlust.\n#WallStreetAufDeutsch {HASH}")
    assert len(social) <= 2200, len(social)
    for red in ("tiktok", "instagram"):
        open(os.path.join(d, f"post-{red}-dax-{F}-GE.txt"), "w").write(social)
    print(titulo, f"({len(titulo)})", "desc", len(desc), "social", len(social))


if __name__ == "__main__":
    main()
