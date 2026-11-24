# Vídeo diario en alemán de Wall Street para Wall Street auf Deutsch — manual de producción

Adaptación al alemán del manual «Wall Street Daily» de Daniel (10-nov-2026) que usa Nabd Wall Street (`nabd/diario/CLAUDE.md` y `README.md`).
`extraer.py` (parte 8) instala esta parte como `ge/diario/CLAUDE.md`, con los marcadores ya rellenos. Las instrucciones van en español (Daniel habla español);
todo lo que ve o escucha el público va en **alemán** (Hochdeutsch, trato de «Sie»).

Cada día de sesión en Nueva York (lunes a viernes; cierre a las 16:00 ET = **22:00 en Berlín** casi todo el año; 21:00 en las
semanas de marzo y de octubre/noviembre en que EE. UU. y Europa cambian de hora en fechas distintas; sin vídeo en festivos de EE. UU.):
un vídeo de **8 a 10 minutos** («Der Tagesbericht») y **tres Shorts** para el canal Wall Street auf Deutsch (https://www.youtube.com/channel/UC23KiHTq_lULliZwAM3dEpA).
Público: Alemania, Austria y Suiza (DACH).

**Horario (desde el 25-nov-2026, Daniel aprobó el 24-nov):** el Tagesbericht ya **no sale de noche** sino **a la mañana siguiente, antes de la apertura
europea**, como «lo que pasó anoche en Wall Street». La tarea programada arranca **martes a sábado a las 05:17 de Berlín** y publica hacia las 06:30-07:00.
La sesión del lunes sale el martes por la mañana; la del viernes, el sábado por la mañana. Los Shorts extra salen solos a las 12:15 y 15:05 de Berlín
(ver «Shorts extra»); el Short del DAX («DAX am Abend», `ge/dax/`) va a las 18:30-20:00, sin choques.
- **Fecha de la sesión** = la de la última vela de `datos/mercado-<fecha>.json` más reciente (normalmente la de ayer en Berlín). Si `cola-ge/bolsa-<fecha>/`
  ya tiene `resultado.json` (p. ej. el viernes tras Thanksgiving, cuando la última vela es del miércoles), no se publica nada.
- **Tiempo verbal:** la sesión es «gestern» / «in der Nacht» para el espectador: «Die Wall Street hat gestern …», «Am Montagabend schloss der S&P 500 …».
  Nunca «heute» para la sesión. «Heute» es la sesión que viene: agenda «Was heute ansteht», «Xetra öffnet heute um 9:00 Uhr», «New York öffnet heute
  um 15:30 Uhr unserer Zeit». Los sábados: «am Montag».
- Se pueden citar resultados y noticias publicados **después del cierre** (after hours, p. ej. resultados tras la campana) con su fuente y hora;
  no hay datos de futuros ni de premarket en `mercado.json`: no inventes cifras de futuros.
- Títulos: no «Wall Street heute (…)», sino p. ej. «Wall Street über Nacht: S&P 500 +4,7 %, Nvidia +31 % | Der Tagesbericht (23. November 2026)». Se publica automáticamente y en público, sin revisión previa, como Nabd.
El nombre del programa no puede ser «Wall Street Daily» (marca existente).
Antes de publicar el primer vídeo, el canal debe estar verificado por teléfono (si no, las miniaturas fallan).

## Guion (8 secciones, 17 escenas, `make_video.py`)
Las claves de escena son las mismas que en Nabd; solo cambia el idioma y la sección 5 (Europa en vez del Golfo).

| # | Sección en pantalla | Escenas | Duración | Contenido |
|---|---|---|---|---|
| 1 | **Einstieg** | `s_title` | ~30 s | Qué pasó, mejor y peor índice, la noticia del día; cierre del S&P 500 y curva intradía. |
| 2 | **Die großen Indizes** | `s_indices`, `s_grandes`, `s_news` | ~90 s | Tabla de S&P 500, Nasdaq 100, Dow Jones y Russell 2000 (Schluss, Tag, Woche, Abstand zum Allzeithoch, Abstand zur 200-Tage-Linie, Trend); las 8 mayores del Nasdaq 100 y la aportación en puntos al Dow (calculada); por qué se movió el mercado (noticias con fuente). |
| 3 | **Sektoren** | `s_sectores` | ~60 s | XLK, XLF, XLE, XLV, XLY, XLI: los dos mejores y los dos peores y sus posibles razones. |
| 4 | **Fünf Aktien des Tages** | `s_accion_1`…`5` | ~120 s | Elegidas de `candidatas` (tecnico.py) por relevancia (resultados, noticia, volumen inusual), no solo por el %. Nombre, ticker, precio, %, volumen y volumen frente a su media, noticia y lectura, velas de 3 meses. Sin noticia publicada: «Keine konkrete Meldung in der Presse». Nunca se inventa. Prioriza, a igualdad, valores conocidos en Alemania (Apple, Nvidia, Tesla, Microsoft…) o con negocio en Europa. |
| 5 | **Zinsen, Dollar, Rohstoffe** | `s_macro` | ~60 s | Bono a 10 años, DXY, VIX, WTI y oro con su línea de 15 sesiones. En vez de «el petróleo y el Golfo» de Nabd: **qué significa para Europa**: DAX (`XETR:DAX`) y Euro Stoxx 50 (`TVC:SX5E`), ya presentes en los datos, y EUR/USD (añadir `FX:EURUSD` a los datos, ver la parte 7, «Datos»). Mencionar que el Xetra abre **hoy** a las 9:00 (el vídeo sale antes). |
| 6 | **Charttechnik** | `s_tech_spx`, `s_tech_ndx`, `s_esc_spx`, `s_esc_ndx` | ~120 s | Velas de 6 meses, GD 20/50/200 (gleitende Durchschnitte), volumen, RSI 14, soportes/resistencias; tres escenarios (positiv, neutral, negativ) con niveles de `tecnico.escenarios`. |
| 7 | **Was heute ansteht** | `s_agenda` | ~60 s | Filas `[fecha ISO, evento, hora de Nueva York "HH:MM" o "", estado]`; la hora de Berlín (MEZ/MESZ) se calcula sola. |
| 8 | **Fazit und Telegram** | `s_fin` | ~30 s | Resumen, invitación a t.me/WallStreetAufDeutsch, aviso legal y aviso de IA. |

En todas: ticker inferior (índices, macro, sectores y titulares de `video.json` → `ticker`) y subtítulos alemanes frase a frase.
`make_video.py` hace el **control de calidad** antes de renderizar (fecha de las velas, sesiones suficientes para la media de 200,
sectores y macro presentes, las 5 acciones en los datos y con noticia/lectura/voz, agenda posterior a la sesión) y escribe
`guion-<fecha>-GE.md` y `datos-<fecha>-GE.csv`. Duración aceptada: 450-630 s. Las tarjetas de escenarios de tres líneas pasan solas a 58 caracteres y letra 18 (arreglo de Nabd del 11-nov).

**Longitud de la locución:** calibrado el 16-nov-2026 con el ejemplo del 9-nov y Azure de-DE-ConradNeural: 1.086 palabras dieron
8:30 (510 s), unas **128 palabras por minuto** con pausas. Objetivo: **1.100-1.250 palabras** para 8:40-9:50.

## Idioma y estilo (alemán)
- Registro de noticiero económico (estilo Börse/Handelsblatt, frases cortas), tratamiento «Sie». Nada de anglicismos innecesarios,
  pero los nombres de índices y empresas se quedan como se usan en Alemania («der S&P 500», «der Dow Jones», «die Nvidia-Aktie»).
- **Pantalla:** formato alemán: coma decimal y punto de miles (7.550,25 Punkte; +2,35 %). `comun.num()` y `comun.pct()` ya lo hacen.
- **Locución:** Azure de-DE lee bien las cifras en formato alemán; escribe «2,35 Prozent» (la palabra «Prozent», no «%»),
  «7.550 Punkte», «10-jährige US-Staatsanleihe». Fechas: «Montag, 9. November».
- Horas siempre en hora de Nueva York y hora alemana («um 8:30 Uhr New Yorker Zeit, 14:30 Uhr bei uns»).
- Términos: Schlusskurs, Tagesplus/-minus, Allzeithoch, 200-Tage-Linie, Unterstützung, Widerstand, Handelsvolumen, Leitzins,
  Rendite, Ölpreis (WTI), Goldpreis, Volatilitätsindex VIX, Quartalszahlen.

## Datos
Se **reutilizan los datos de Nabd** (mismos índices de EE. UU.): `datos/mercado-<fecha>.json` de la rama `datos-diario-nabd`,
que escribe `datos-diario-Nabd.yml` a las 21:40 UTC (por la mañana ya está). Si a la hora de la tarea no está, lanzar `datos-diario-Nabd.yml`
(workflow_dispatch en main) y esperar; no se duplica el workflow. Si la última vela no es de hoy (festivo), no se publica nada.
`python3 tecnico.py <mercado.json>` imprime cierres, medias, RSI, niveles, escenarios, sectores, macro, aportación al Dow,
las 8 grandes del Nasdaq 100 y las candidatas.

## Voz
- **Azure `de-DE-ConradNeural`** (recomendada: masculina, tono de noticiero; alternativa femenina `de-DE-KatjaNeural`; más expresivas:
  `de-DE-FlorianMultilingualNeural` / `de-DE-SeraphinaMultilingualNeural`). Recurso de Azure Speech **propio del canal**
  (plan gratuito **F0**, secretos `AZURE_SPEECH_KEY_GE` y `AZURE_SPEECH_REGION_GE`; la región está guardada como «Germany West Central»
  y `voz_azure.py` la normaliza a `germanywestcentral`). Se dispara al subir `ge/diario/<fecha>/video.json` a una rama `claude/ge-diario-*`
  y deja un wav por frase en `<fecha>/` de la rama `voz-ge`. `VOZ_DIR=<esa carpeta> python3 make_video.py ...` los usa.
- **Cuota F0:** 500.000 caracteres/mes solo para este canal (~8.000/día, unos 180.000 al mes en 22 sesiones): hay margen para
  regeneraciones. Si Azure devuelve error de cuota, el vídeo sale con Piper y se avisa.
- **Short:** `voz-GE.yml` también genera con Azure las frases de `short.json` (misma carpeta); `make_short.py` usa `VOZ_DIR` si están
  todas y, si falta alguna, el Short entero sale con Piper.
- **Piper `de_DE-thorsten-high`** (respaldo): descargar una vez de huggingface.co/rhasspy/piper-voices a
  `/mnt/project-files/ge-pipeline/voice/`. Nunca se mezclan las dos voces en un vídeo.

## Pasos de cada día
1. Datos de `datos-diario-nabd` (si faltan, lanzar `datos-diario-Nabd.yml` y esperar).
2. `python3 tecnico.py` y noticias del día: Yahoo Finance (live blog), CNBC, Reuters, The Closing Print, StockTitan; en alemán
   como contraste: Handelsblatt, Börse Online, finanzen.net, boerse.de, Reuters Deutschland. Fuentes oficiales (Fed, BLS, BEA,
   Tesoro, SEC EDGAR, notas de resultados) cuando las haya. Solo lo publicado ese día.
3. Copiar la plantilla del día (`ejemplo-2026-11-09/`, sin mercado.json ni salidas; en `video.json` → `macro.europa` va la frase de Europa) a
   `ge/diario/<fecha>/`, poner el `mercado.json` y reescribir `video.json`, `info.json` y `short.json` (< 59 s; fecha en la primera escena).
4. Subir `video.json` a `claude/ge-diario-<fecha>`: `voz-GE.yml` genera la voz (2-4 min); clonar la rama `voz-ge`.
5. `AUD=<scratch> python3 make_video.py <dir> preview` (mirar TODOS los PNG), luego `AUD=<scratch> VOZ_DIR=<voz>/<fecha> python3 make_video.py <dir>`.
6. `AUD=<scratch> VOZ_DIR=<voz>/<fecha> python3 make_short.py <dir>/<x>.json` para `short.json`, `short-2.json` y `short-3.json` (preview primero),
   y `python3 gen_meta.py <dir>`.
7. `SCRATCH=<scratch> bash encolar.sh <dir>`: encola en `cola-ge/bolsa-<fecha>` y `-short` de `youtube-cola`; `youtube-GE.yml`
   los sube (si una miniatura falla, `youtube-GE.yml` modo=miniaturas la reintenta); `telegram-GE.yml` publica el post de Telegram y `buffer-GE.yml` los de LinkedIn, X, TikTok e Instagram.
   Los Shorts 2 y 3 quedan en `cola-ge-espera/` y salen solos a su hora (ver «Shorts extra»).

## Shorts extra (desde el 24-nov-2026, Daniel aprobó 2-3 Shorts diarios del mismo guion)
Del mismo guion y los mismos datos salen tres Shorts (< 59 s cada uno, con `make_short.py`, mismas escenas `titulo`/`cifra`/`kpis`/`fin`).
Plantilla con ejemplo real: `ejemplo-shorts-extra/` (`short-2.json`, `short-3.json` y el bloque `shorts_extra` de `info.json`).

| Short | Archivo | Sale | Contenido |
|---|---|---|---|
| 1 «Wall Street über Nacht» | `short.json` → `short-bolsa-<fecha>-GE.mp4` | con el vídeo (~07:00) | El de siempre: índices y tres puntos. YouTube, TikTok, Instagram y LinkedIn. |
| 2 «Aktie des Tages» | `short-2.json` → `short-2-bolsa-<fecha>-GE.mp4` | 12:15 Berlín | La acción más llamativa de las 5 del vídeo (no repetir la del Short 1 si hay otra con noticia): qué pasó, cifras, fuente. |
| 3 «Die Marken für heute» | `short-3.json` → `short-3-bolsa-<fecha>-GE.mp4` | 15:05 Berlín (antes de la apertura de NY, 15:30) | Resistencia, 200-Tage-Linie (o GD 50) y soporte del S&P 500 o del Nasdaq 100 de `tecnico.py`, «berechnet»; escenarios solo como condiciones («Schließt der S&P 500 über …, dann liegt er …»), nunca previsiones. Sábados: «für Montag». |

- `info.json` → `shorts_extra`: `[{"n": 2, "titulo": "… #Shorts" (≤ 100), "resumen", "tiktok", "hashtags", "tags"}, {"n": 3, …}]`.
  `gen_meta.py` escribe `meta-short<n>-<fecha>-GE.json` y `post-tiktok/instagram-short<n>-<fecha>-GE.txt` (enlazan al vídeo largo).
- La voz: `voz-GE.yml` genera con Azure las frases de `short*.json` (sube los tres JSON a la rama `claude/ge-diario-<fecha>` junto con `video.json`).
- `encolar.sh` deja los Shorts 2 y 3 en `cola-ge-espera/bolsa-<fecha>-short<n>/` (rama `youtube-cola`) con `publicar.txt` (hora UTC).
  `cola-espera-GE.yml` (cada 20 min de 09 a 16 UTC) los pasa a `cola-ge/` a su hora, lanza `youtube-GE.yml` y luego `buffer-GE.yml`
  (TikTok e Instagram; sin LinkedIn ni X para no saturar). Con más de 8 h de retraso no se publican (`caducado.txt`).
- Límite de YouTube (~10 subidas/24 h): el diario usa 4 (vídeo + 3 Shorts), el DAX 1 y la serie de las 20 grandes hasta 3.
  Si un día no cabe, `cola-espera-GE.yml` espera; si hace falta recortar, se omite el Short 3 (no hagas `short-3.json`).

## Reglas (Alemania / UE)
- Nada de comprar/vender, precio objetivo ni «günstig/teuer». Análisis técnico como datos. Cada cifra con fuente; cálculos propios «(berechnet)».
- Hechos, opiniones y escenarios separados; escenarios como condiciones («Schließt der S&P 500 über …, dann …»), nunca previsiones.
- Aviso en cierre, descripción y posts: «Keine Anlageberatung. Nur Information und Bildung. Keine Kauf- oder Verkaufsempfehlung.
  Aktien sind mit Risiken bis zum Totalverlust verbunden.» Sin posiciones en los valores citados.
  No dar «Anlageempfehlungen» en el sentido de la MAR (art. 20) ni del WpHG: eso obligaría a deberes de transparencia extra.
- Transparencia IA (Reglamento de IA de la UE, art. 50): «Text, Stimme und Grafiken mit KI erstellt» en el cierre, la descripción
  y los posts; marcar «contenido alterado o sintético» al subir.
- **Impressum** (§ 5 DDG): enlace al Impressum de Daniel en la descripción del canal y en cada descripción de vídeo, cuando exista.
- Todo archivo de salida termina en `-GE` antes de la extensión.
- Todos los secretos de GitHub del canal terminan en `_GE` (regla de Daniel).

## Serie de resultados de las 20 grandes
Además del diario, un vídeo corto (2-4 min) por cada informe de resultados de las 20 mayores empresas de EE. UU.: `ge/serie20/CLAUDE.md`.
