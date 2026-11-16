# Vídeo diario en alemán de Wall Street para Wall Street auf Deutsch — manual de producción

Adaptación al alemán del manual «Wall Street Daily» de Daniel (10-nov-2026) que usa Nabd Wall Street (`nabd/diario/CLAUDE.md` y `README.md`).
`extraer.py` (parte 8) instala esta parte como `ge/diario/CLAUDE.md`, con los marcadores ya rellenos. Las instrucciones van en español (Daniel habla español);
todo lo que ve o escucha el público va en **alemán** (Hochdeutsch, trato de «Sie»).

Cada día de sesión en Nueva York (lunes a viernes; cierre a las 16:00 ET = **22:00 en Berlín** casi todo el año; 21:00 en las
semanas de marzo y de octubre/noviembre en que EE. UU. y Europa cambian de hora en fechas distintas; sin vídeo en festivos de EE. UU.):
un vídeo de **8 a 10 minutos** («Der Tagesbericht») y su Short para el canal Wall Street auf Deutsch (https://www.youtube.com/channel/PENDIENTE).
Público: Alemania, Austria y Suiza (DACH). Se publica automáticamente y en público, sin revisión previa, como Nabd.
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
| 5 | **Zinsen, Dollar, Rohstoffe** | `s_macro` | ~60 s | Bono a 10 años, DXY, VIX, WTI y oro con su línea de 15 sesiones. En vez de «el petróleo y el Golfo» de Nabd: **qué significa para Europa**: DAX (`XETR:DAX`) y Euro Stoxx 50 (`TVC:SX5E`), ya presentes en los datos, y EUR/USD (añadir `FX:EURUSD` a los datos, ver la parte 7, «Datos»). Mencionar que la sesión alemana ya cerró a las 17:30 y que el Xetra de mañana abre a las 9:00. |
| 6 | **Charttechnik** | `s_tech_spx`, `s_tech_ndx`, `s_esc_spx`, `s_esc_ndx` | ~120 s | Velas de 6 meses, GD 20/50/200 (gleitende Durchschnitte), volumen, RSI 14, soportes/resistencias; tres escenarios (positiv, neutral, negativ) con niveles de `tecnico.escenarios`. |
| 7 | **Was morgen ansteht** | `s_agenda` | ~60 s | Filas `[fecha ISO, evento, hora de Nueva York "HH:MM" o "", estado]`; la hora de Berlín (MEZ/MESZ) se calcula sola. |
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
que escribe `datos-diario-Nabd.yml` a las 21:40 UTC. Si a la hora de la tarea no está, lanzar `datos-diario-Nabd.yml`
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
3. Copiar la plantilla del día (la primera vez: crear `ejemplo-<fecha>/` alemán a partir de `ejemplo-2026-11-09-ar/`) a
   `ge/diario/<fecha>/`, poner el `mercado.json` y reescribir `video.json`, `info.json` y `short.json` (< 59 s; fecha en la primera escena).
4. Subir `video.json` a `claude/ge-diario-<fecha>`: `voz-GE.yml` genera la voz (2-4 min); clonar la rama `voz-ge`.
5. `AUD=<scratch> python3 make_video.py <dir> preview` (mirar TODOS los PNG), luego `AUD=<scratch> VOZ_DIR=<voz>/<fecha> python3 make_video.py <dir>`.
6. `AUD=<scratch> python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>`.
7. `SCRATCH=<scratch> bash encolar.sh <dir>`: encola en `cola-ge/bolsa-<fecha>` y `-short` de `youtube-cola`; `youtube-GE.yml`
   los sube (si una miniatura falla, `youtube-GE.yml` modo=miniaturas la reintenta); `telegram-GE.yml` publica el post de Telegram y `buffer-GE.yml` los de LinkedIn, X, TikTok e Instagram.

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
