# Nabd Wall Street · Short semanal «تقويم النتائج الأسبوعي للأسهم الأمريكية» (calendario de resultados)

Pedido por Daniel el 22-nov-2026. Estas instrucciones prevalecen sobre el texto de la tarea programada donde difieran.

**Qué es:** un Short vertical 9:16 de 45 a 60 s, todo en árabe, voz Azure `ar-SA-HamedNeural`, que sale **cada domingo entre las 19:00 y las
21:00 de Riad (16:00-18:00 UTC)**, antes de que Wall Street abra el lunes. Publicación automática y pública, sin revisión de Daniel.

**Contenido:** SOLO las 22 acciones que sigue el canal (las de la serie «عمالقة وول ستريت», `nabd/serie20/datos_tv.py`: NVDA, MSFT, AAPL,
GOOGL, AMZN, META, AVGO, TSLA, BRK, JPM, LLY, WMT, ORCL, V, MA, XOM, NFLX, COST, JNJ, PLTR, SPCX (SpaceX), ANT (Anthropic)). Ninguna otra.
Para cada una que presente resultados de lunes a viernes de la semana siguiente: nombre y ticker, día del reporte, antes de la apertura o
tras el cierre (con la hora de Riad: la calcula `make_calendario.py`) y el consenso de BPA e ingresos. **Datos verificados en la web; nunca
inventes. Si falta un dato (p. ej. el consenso de ingresos), quítalo** (`ingresos_mm: null`, `bpa: null`; sin fecha confirmada: `fecha_et: null`
con `fecha_texto` y `nota_fecha`, `confirmada: false`).

**Modo:** 2 o más de la lista reportan esa semana → `"modo": "semana"` (todas, en orden cronológico, máximo 8; con más de 4 la portada no
lleva lista). 0 o 1 → `"modo": "proximos"` («Próximos reportes»): las 3 siguientes que reportan, en orden cronológico (incluida la de esa semana si hay una).

**Guion** (locución en árabe estándar, números en palabras, 45-60 s en total; `make_calendario.py` rechaza fuera de 44-59,5 s):
1. Gancho (~3-5 s): semana → «هذا الأسبوع تعلن [la más importante] نتائجها… و[N] أسهم أخرى من قائمتنا.»; próximos → «لا نتائج من قائمتنا هذا الأسبوع. والموعد الأهم القادم: [...]، و[N] أسهم أخرى من قائمتنا.»
2. Las empresas en orden cronológico, unos 6-8 s cada una (con 3 o menos pueden ser ~10-12 s para llegar a 45 s).
3. Cierre: «تابع القناة لتحليل كل تقرير. محتوى إعلامي، وليس توصية استثمارية.»
La más importante = la de mayor capitalización. El aviso «محتوى إعلامي، وليس توصية استثمارية.» va en pantalla, en la voz y en todos los textos.

## Pasos de cada domingo (rutina, ~14:41 UTC)

0. Lee este archivo. Instala `pip install matplotlib arabic_reshaper python-bidi imageio-ffmpeg` (y `piper-tts` solo si hace falta Piper).
   Rama `claude/nabd-calendario-<fecha del lunes>` desde main. `<base>` = `calendario-<fecha del lunes>` (p. ej. calendario-2026-11-30).
1. Punto de partida: `git fetch origin datos-serie20-nabd` y lee de cada `<TICKER>/datos.json` `ultimo.earnings_release_next_date`
   (epoch UTC), `earnings_per_share_forecast_next_fq` y `revenue_forecast_next_fq` (TradingView). OJO: tras un reporte reciente TradingView
   puede tardar en mover la fecha; y sus horas (07:00, 16:15) a veces son estimadas.
2. Verifica en la web cada empresa de la semana (o las próximas): comunicado de la empresa (relación con inversores, PRNewswire/Business Wire)
   para la fecha y el momento; calendario semanal (StockTitan «Earnings Calendar for the Week of…», Investrade, Earnings Whispers) y consenso
   (Zacks vía Yahoo Finance, MarketScreener, TipRanks, Nasdaq). Usa la cifra cuando la fuente web y TradingView coincidan aprox.; si solo hay
   una fuente web fiable, también vale. Si no hay ninguna, quita ese dato. `confirmada: true` solo si la empresa anunció la fecha
   (o un calendario la marca como confirmada). `hora_et` solo si la empresa publica la hora exacta de la nota; si no, se muestra «بعد الإغلاق /
   قبل الافتتاح» con la hora de cierre o apertura en Riad. Ojo con los festivos de EE. UU. (Acción de Gracias, Navidad).
3. Escribe `nabd/calendario/semanas/<base>/video.json` copiando el formato de `semanas/calendario-2026-11-23/` (escenas gancho, empresa…,
   cierre; `fuentes` con las fuentes reales; `periodo` = trimestre fiscal en árabe). Preview:
   `AUD=<scratch> python3 nabd/calendario/make_calendario.py <carpeta>/video.json preview` y mira TODOS los PNG (textos cortados o solapados).
4. Voz Azure: sube la carpeta a tu rama y lanza `voz-Nabd.yml` (workflow_dispatch en tu rama) con `modo=generar`,
   `fecha=nabd/calendario/semanas/<base>`, `avatar=no`. En ~1 min deja los wav en `<base>/` de la rama `voz-nabd`: clónala y
   `VOZ_DIR=<clon>/<base>`. Si falla o falta el secreto, sigue con Piper (sin VOZ_DIR) y dilo en el resumen.
5. Render: `AUD=<scratch> VOZ_DIR=... python3 nabd/calendario/make_calendario.py <carpeta>/video.json` (si la duración se sale de rango,
   ajusta la locución, vuelve a subir y a generar la voz). Luego `python3 nabd/calendario/meta_calendario.py <carpeta>/video.json`.
   Mira el MP4 (fotogramas con ffmpeg) y los textos.
6. Copia el Short, la portada, meta, posts y `guion-<base>-Nabd.md` a `/mnt/project-files/nabd-calendario/<base>/` (todo termina en -Nabd).
7. Publica: `SCRATCH=<scratch> bash nabd/calendario/encolar.sh nabd/calendario/semanas/<base>` (en segundo plano: espera sola hasta las
   16:00 UTC = 19:00 Riad, encola, y espera el ID de YouTube). Si en 10 min tras encolar no hay resultado.json, lanza `youtube-Nabd.yml` modo=subir.
8. Commit de `video.json`, meta, posts y guion (no el mp4 ni el png) en tu rama, PR a main y **fusiónalo tú** (regla de Daniel, 20-nov-2026).
9. Resumen corto en español: enlace del Short, duración, voz, empresas incluidas y cualquier dato que se quitara por no estar verificado.

Redes: YouTube Short (youtube-Nabd.yml), Telegram con la portada (telegram-Nabd.yml), y por Buffer X, LinkedIn, TikTok, Instagram (Reel),
Facebook y Threads (buffer-Nabd.yml). Facebook y Threads no estaban conectados en Buffer el 22-nov-2026: sus posts esperan sin error y
salen solos cuando Daniel los conecte en la cuenta de Buffer de Instagram (BUFFER_API_KEY_NABD_IG, que tiene sitio).
