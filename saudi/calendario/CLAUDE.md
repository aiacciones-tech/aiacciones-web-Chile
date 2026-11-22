# «تقويم النتائج الأسبوعي» de Saudi Arabia AI Stocks: instrucciones (Daniel, 22-nov-2026)

Short vertical 9:16 de 45-59 s, todo en árabe, voz Azure ar-SA-HamedNeural (+8 %). Sale **cada sábado entre las 20:00 y las 21:00 de Riad**,
antes de que Tadawul abra el domingo. Contenido: las 5-7 empresas más relevantes que reportan en la semana siguiente (domingo a viernes):
primero Tadawul/TASI (domingo a jueves) y después las grandes de EE. UU. (lunes a viernes), en orden cronológico. Por empresa: nombre y ticker,
día (y antes/después de la sesión) y consenso de **BPA ajustado e ingresos**, ~6-8 s cada una.
Guion: 1) gancho (~3 s): «هذا الأسبوع تعلن [la más grande] نتائجها، و[N] شركات أخرى»; 2) empresas en orden cronológico; 3) cierre:
«تابع القناة لتحليل كل تقرير» + (si hay empresas de EE. UU.) recomendar la canal **نبض وول ستريت** https://www.youtube.com/@NabdWallStreet
(Daniel, 22-nov-2026) + «محتوى إعلامي، وليس توصية استثمارية».
Reglas del canal: archivos en inglés terminados en `-saudi`; cada post enlaza https://www.youtube.com/@SaudiArabiaAIStocks; LinkedIn lleva el Short
como vídeo nativo con 3-4 datos + «الخلاصة» + «فيديو من إعداد قناة Saudi Arabia AI Stocks» + enlace del canal al final; Instagram como Reel;
Facebook y Telegram también. La campaña de comentarios (`saudi/diario/campana.py`) se añade sola si está activa en la fecha `publicar`.

## Datos: buscar y verificar, nunca inventar
- **Fechas:** solo confirmadas por la empresa (nota de prensa / web de IR / anuncio en Tadawul). Una fecha "estimada" de un agregador no basta.
- **Consenso:** cada cifra en **al menos dos fuentes** que coincidan (±1-2 %): StockAnalysis (`curl https://stockanalysis.com/stocks/<t>/forecast/`,
  bloque `quarterly:{...epsThis:{last,this}...revenueThis:{last,this}}`, carga con curl), Nasdaq (`curl -H "Accept: application/json"
  "https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD"`: fecha, hora, BPA Zacks; ojo, a veces en base GAAP), y búsquedas web
  (MarketBeat, TipRanks, Zacks, Barchart, Benzinga; la guía de la empresa ayuda a confirmar). MarketBeat y Yahoo bloquean curl.
  Si las fuentes no coinciden o solo hay una, **ese dato sale del guion** (p. ej. 29-nov: ingresos de Dollar General fuera; Snowflake fuera por BPA 0.42 vs 0.60).
- **Tadawul:** las empresas saudíes casi nunca anuncian la fecha antes: solo entra una con anuncio en saudiexchange.sa / Argaam de que publica
  esa semana, o la que ya publicó. Consenso de Tadawul: solo si hay dos fuentes (Argaam, Al Rajhi Capital, SNB Capital…); si no, solo nombre y día.
  Si no hay ninguna grande, la escena `tasi` lo dice (fuera de temporada: plazo CMA 30 días tras el trimestre, 3 meses para el anual).
  Las 25 que sigue el canal están en `/mnt/project-files/saudi-pipeline/calendar-FY26-saudi.json`.
- Relevancia en EE. UU.: capitalización (Nasdaq la da) y nombres conocidos; excluye bancos canadienses y empresas no estadounidenses.

## Piezas (saudi/calendario/)
- `semanas/<base>/short.json` (base `earnings-week-<domingo>`): semana, publicar (sábado), datos_al, escenas
  (`gancho` con estrella/otras/lista, `tasi` con lineas, `empresa` con nombre/latino/ticker/dia/hora/eps/ingresos, `fin`), fuentes (tabla de verificación,
  incluidas las cifras que quedaron FUERA y por qué), info (titulo ≤100 con #Shorts, resumen, lineas, x, linkedin {titulo, datos, conclusion}, hashtags).
  La voz (`voz`) con cifras en palabras y nombres latinos en letras árabes; ~90 palabras ≈ 56 s.
- `.github/workflows/calendario-saudi.yml`: al subir `short.json` a una rama `claude/**`, genera la voz Azure frase a frase en `<base>/` de la rama `voz-saudi-calendario`.
- `make_calendario.py <carpeta> [preview]` (con `AUD`, `VOZ_DIR`): el Short (falla si pasa de 59 s).
- `meta_calendario.py <carpeta>`: metadatos del Short, posts de las 7 redes + LinkedIn y portada 1080x1920 (miniatura y foto de Telegram).
- `encolar.sh <carpeta>`: `cola-sa/calendar-<base>-short/` en `youtube-cola`; desde ahí todo se publica solo.

## Pasos de cada sábado (tarea programada)
1. Semana = domingo siguiente a viernes. Busca y verifica (arriba). Escribe `semanas/<base>/short.json` (copia la semana anterior como plantilla).
2. Preview: `AUD=<scratch> python3 make_calendario.py <carpeta> preview`; mira TODOS los PNG.
3. Commit y push a `claude/saudi-calendario-<fecha>` → `calendario-saudi.yml` (~30 s). `git clone -q --depth 1 -b voz-saudi-calendario <repo> <scratch>/voz`.
4. Render con `VOZ_DIR=<scratch>/voz/<base>` (la línea `voz: azure` lo confirma); `meta_calendario.py`. Si Azure falla, Piper y dilo.
5. Copia mp4, portada, metadatos, guion y posts a `/mnt/project-files/saudi-calendario/<base>/`.
6. Entre las 20:00 y las 21:00 de Riad: `SCRATCH=<scratch> bash encolar.sh <carpeta>`. Abre o actualiza el PR de la rama para que quede en main.
