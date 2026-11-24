# «DAX am Abend»: Short diario del DAX en Wall Street auf Deutsch (prueba de 4-6 semanas desde el 24-nov-2026)

Daniel (24-nov-2026) preguntó por un canal alemán de acciones alemanas. Se acordó **probar primero dentro del canal actual**: un Short diario
del DAX, sin tocar el Tagesbericht. Daniel recibe un reporte por correo el **22-dic-2026** (asunto «RESULTADO DAX», otra tarea programada). Si los Shorts del DAX rinden igual o mejor que los de Wall Street
(vistas, % de visualización, suscriptores ganados en YouTube Studio), se plantea un canal propio. Instrucciones en español; lo que ve y oye el público, en alemán («Sie»).
Valen todas las reglas de `ge/diario/CLAUDE.md` (Keine Anlageberatung, transparencia IA, nunca inventar, archivos `-GE`, secretos `_GE`;
solo se toca `ge/`, `*-GE.yml` y `cola-ge/`).

## Cuándo
Cada día de sesión de **Xetra** (lunes a viernes salvo festivos de la Bolsa de Fráncfort: 24, 25, 26 y 31 de diciembre, 1 de enero,
Viernes Santo, Lunes de Pascua, 1 de mayo). Cierre 17:30 de Berlín. `datos-dax-GE.yml` corre a las 17:05 UTC (18:05 Berlín en invierno)
y deja `datos/dax-<fecha>.json` en la rama `datos-dax-ge`. El Short se publica **entre las 18:30 y las 20:00 de Berlín**.
Desde el 25-nov-2026 el Tagesbericht de Wall Street sale **por la mañana** (hacia las 07:00 de Berlín, con la sesión de la noche anterior),
y los Shorts extra del diario a las 12:15 y 15:05: el DAX de la tarde no choca con ninguno. Si la última vela no es de hoy (festivo alemán), no se publica nada.

## Contenido (45-58 s, `short.json` con el `make_short.py` del diario)
1. `titulo`: kicker «DAX · Handelstag vom», fecha corta, DAX y otro índice (MDAX o Euro Stoxx 50) con % y cierre, y un gancho de 2-4 palabras.
   Voz: «DAX, Dienstag, 24. November. [gancho]. Drei Punkte.»
2. `cifra` 1 «Das Wichtigste»: el porqué del día en el DAX (dato macro, noticia de empresa, Wall Street, aranceles…) con fuente.
   Solo lo publicado hoy (Handelsblatt, Börse Online, finanzen.net, boerse.de, Reuters Deutschland, dpa-AFX vía finanzen.net/onvista,
   notas de empresa). Sin motivo publicado: «Keine konkrete Meldung in der Presse».
3. `cifra` 2 «Gewinner und Verlierer»: `big` = la mayor subida o bajada relevante, `barras` con 2 ganadoras y 2 perdedoras, y en la nota
   la amplitud («16 von 40 DAX-Werten im Plus»). Para la mayor, motivo si hay noticia; si no, solo la cifra.
4. `kpis` 3 «Charttechnik DAX»: RSI 14, distancia a la 200-Tage-Linie y al Rekordhoch (de `dax.py`, «berechnet»). Nota: «Das sind Daten, keine Kauf- oder Verkaufssignale.»
5. `fin`: `titular` breve (p. ej. «Morgen früh:\nWall Street») y `cta` «Tagesbericht vor Börsenstart» (máx. ~28 caracteres o se corta; notas de 40 caracteres por línea como mucho). Voz: «Den Tagesbericht zur Wall Street
   gibt es morgen früh auf unserem Kanal. Keine Anlageberatung.» (Viernes: «am Samstagmorgen».)
Unas 95-115 palabras de voz en total (Azure ≈ 128 palabras/min más pausas). `make_short.py` corta si pasa de 59 s.
Campos extra de `short.json` para `meta_dax.py`: `fecha` (ISO), `titulo_yt` (≤ 90 caracteres, p. ej. «DAX schließt 0,9 % tiefer: Rheinmetall vorn, SAP schwach»),
`resumen`, `claves` (3-4), `tags` (empresas citadas) y `fuente`.

## Pasos de cada día (la tarea programada arranca a las 17:20 UTC)
1. Datos: `git fetch origin +datos-dax-ge:datos-dax-ge` (con +) o clon de la rama; `datos/dax-<hoy>.json`. Si no está a las 17:40 UTC, empuja un cambio
   inocuo de `ge/dax/datos_dax.py` (p. ej. la fecha de la cabecera) a una rama `claude/ge-dax-<fecha>`: el push dispara `datos-dax-GE.yml`.
   Comprueba que `generado` es posterior a las 16:45 UTC (en verano, 15:45): si no, son datos de media sesión.
2. `python3 ge/dax/dax.py <dax.json>`: cierres, amplitud, ganadoras/perdedoras, volumen inusual, contexto (MDAX, TecDAX, Euro Stoxx 50, EUR/USD, Bund).
   Si `origen_acciones` es «lista», la composición sale de la lista DAX40 de `datos_dax.py`: revísala tras cada revisión trimestral del índice
   (efectiva el tercer viernes de marzo, junio, septiembre y diciembre).
3. Noticias del día (fuentes de arriba). Nunca inventes una cifra ni un motivo.
4. Copia `dias/2026-11-24/short.json` a `ge/dax/dias/<fecha>/short.json` y reescríbelo.
5. `AUD=<scratch> python3 ge/diario/make_short.py ge/dax/dias/<fecha>/short.json preview` y mira todos los PNG.
6. Sube `short.json` a la rama `claude/ge-dax-<fecha>` (desde main): `voz-dax-GE.yml` genera la voz (1-2 min) en `<fecha>/` de la rama `voz-ge-dax`.
   Clónala y `AUD=<scratch> VOZ_DIR=<clon>/<fecha> python3 ge/diario/make_short.py ge/dax/dias/<fecha>/short.json` (sale `dax-<fecha>-GE.mp4`).
   Si falla Azure, sale con Piper y se dice en el resumen.
7. `python3 ge/dax/meta_dax.py ge/dax/dias/<fecha>` y `SCRATCH=<scratch> bash ge/dax/encolar.sh ge/dax/dias/<fecha>` → `cola-ge/dax-<fecha>/`:
   `youtube-GE.yml` lo sube, `buffer-GE.yml` manda TikTok e Instagram. Sin Telegram ni X durante la prueba.
8. Copia mp4, meta, posts y short.json a `/mnt/project-files/ge-dax/<fecha>/`. No subas el mp4 al repo. Commit de `short.json` en la rama del día y PR.
9. Resumen corto en español con el enlace del Short.
