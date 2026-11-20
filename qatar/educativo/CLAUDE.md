# Serie educativa semanal «التحليل الفني ببساطة» de Qatar AI Stocks: instrucciones (Daniel, 20-nov-2026)

Vídeos educativos de análisis técnico en árabe, **un concepto por vídeo**, explicado sobre el **gráfico real** de una acción de la Bolsa de Qatar
(QSE; datos de TradingView), con la voz y la marca del canal (Piper `ar_JO-kareem-medium`, colores y logo de `qatar/diario/comun.py`).
~6 minutos, subtítulos (quemados y `.srt`), miniatura y Short. **Un vídeo por semana.** Daniel (20-nov-2026): la serie **empieza cuando termine
la serie fundamental** (`qatar/fundamental/`, 10 sábados, el último el 23-ene-2027); Daniel eligió (20-nov-2026) el sábado ~18:00 Doha desde el
30-ene-2027 (`DIA` en `comun_leccion.py` y `plan-qatar.json`; cámbialos si Daniel elige otro). Después del primero, los demás se publican solos.
Copia de `saudi/educativo/` (que a su vez viene de la alemana `ge/educativo/`, PR #184) con la marca, la voz y las redes de Qatar.
Plan de 10 temas en `plan-qatar.json` (marca cada lección publicada). Instrucciones en español; lo que ve y oye el público, en árabe.

## Reglas de contenido
- Educación, no previsión: zonas y patrones del pasado; la situación actual va como **condiciones** («إذا أغلق السعر فوق… فهذا يعني…»),
  nunca como previsión, precio objetivo ni recomendación. La acción es «مجرد مثال». Sin «رخيص/مرتفع الثمن». `make_leccion.py` rechaza algunas palabras.
- Toda cifra dicha sale de `velas.json` (TradingView; Yahoo `.QA` solo si TradingView falla, y entonces la fuente en pantalla lo dice) y coincide
  con la pantalla. Las zonas son «محسوبة/مرسومة من القناة». No se explican las causas de un movimiento salvo con fuente publicada y atribuida.
- En la locución, las cifras en palabras («ثمانية عشر فاصل أربعة») y los nombres latinos en letras árabes («قطر إيه آي ستوكس», «تريدينغ فيو»,
  «كيو إن بي»); `comun_leccion.LATINO` los devuelve a su forma latina en los subtítulos (añade ahí cada nombre nuevo).
- Bidi: sin comillas «» en pantalla; una línea que empieza por siglas latinas (QNB, RSI, MACD) se gira a LTR: empieza con una palabra árabe.
- `ultima_vela`: la última sesión **cerrada** (el jueves anterior; la QSE abre de domingo a jueves).
- Campaña de comentarios: `campana.py` usa `cta_activa()` de `qatar/diario/comun.py` (hasta el 22-nov-2026; después no añade nada).
- Todo archivo entregado termina en `-qatar` y todo post lleva el enlace al canal (reglas de Daniel). Facebook cerró: no hay post de Facebook.

## Piezas (qatar/educativo/)
- `lecciones/<base>/video.json`: base (`ta-NN-<accion>`), folge, simbolo (`QSE:<código>`), ticker, nombre, tema, ultima_vela, escenas, short, info, miniatura.
  Escenas (`tipo`): `portada`, `esquema` (modo sr / rollentausch / rollentausch_baja / fehlausbruch), `puntos` (≤5 [título, texto]),
  `grafico` (desde, hasta, zonas [{de, a, texto, color}], marcas [{fecha, tipo techo|suelo, texto}], nota, volumen, animar_velas,
  **lineas** [{sma: 50, color, texto}] = medias móviles simples calculadas de todas las velas, **rsi**: true = panel RSI(14) en lugar del volumen),
  `fin` (claves ≤4, siguiente). `capitulo` = capítulo de YouTube. Para un tema que necesite otro dibujo (MACD, Bollinger, gaps…) añade una
  opción a `s_grafico` o un tipo nuevo en `make_leccion.py`, y su equivalente en `make_short_leccion.py` (el Short aún no dibuja `lineas` ni `rsi`).
  `short`: 4 escenas (titulo, grafico con `grafico: <id de escena larga>`, grafico, fin), < 59 s (~80-90 palabras).
  `info`: titulo, titulo_short, resumen, fuentes, hashtags, hashtags_short, tags, x, pregunta (Threads), tiktok, linkedin {datos (3-4), conclusion}.
- `.github/workflows/educativo-qatar.yml`: al subir `video.json` a una rama `claude/**` pide a TradingView las velas diarias (~520) del `simbolo`
  (y `simbolos_extra`) y las deja en `<base>/velas.json` de la rama `datos-educativo-qatar` (se congelan; para volver a pedirlas: workflow_dispatch
  con `refrescar=1`). **El contenedor de Claude no llega a TradingView** (403 del proxy); GitHub Actions sí.
- `niveles.py <velas.json> [simbolo] [ventana] [tolerancia %] [sesiones]`: pivotes y zonas candidatas, para escribir el guion.
- `make_leccion.py <carpeta> [preview]` y `make_short_leccion.py <carpeta> [preview]` (con `AUD`, `VELAS`): vídeo 5-7,5 min y Short.
  Escriben `<base>-qatar.mp4`, `subtitulos-<base>-qatar.srt`, `guion-<base>-qatar.md`, times.json y `short-<base>-qatar.mp4`.
- `meta_leccion.py <carpeta>` (con `VELAS`): metadatos de YouTube y del Short, posts (X, Threads, LinkedIn, TikTok, Instagram, Telegram) y miniatura.
- `encolar.sh <carpeta>`: `cola-qa/<base>/` y `<base>-short/` en `youtube-cola`; desde ahí todo se publica solo.

## Pasos de cada semana (tarea programada)
1. Mira `plan-qatar.json`: la primera lección `lista` (renderizada de muestra, falta actualizarla y publicarla) o `pendiente`.
   Elige la acción con su gráfico de 2 años. Comprueba que la serie fundamental terminó (no publiques antes del 30-ene-2027 salvo que Daniel lo pida).
2. Escribe o actualiza `lecciones/<base>/video.json` (~600-650 palabras ≈ 6:30 con Piper a 0,8; el Short ~80-90). Para una lección `lista`, pide velas
   nuevas (`gh workflow run educativo-qatar.yml -f carpetas=<base> -f refrescar=1 --ref <rama>`), pon `ultima_vela` al último jueves y reescribe las
   escenas que hablan del presente (`ahora`, `x`, `tiktok`, `linkedin`, resumen) con las cifras nuevas.
3. Commit y push a `claude/qatar-educativo-<fecha>` → `educativo-qatar.yml` (~1 min). `git clone -q --depth 1 -b datos-educativo-qatar <repo> <scratch>/datos`.
4. Preview: `AUD=<scratch> VELAS=<scratch>/datos/<base>/velas.json python3 make_leccion.py <carpeta> preview` y `make_short_leccion.py … preview`;
   mira TODOS los PNG. Render de los dos; `meta_leccion.py`.
5. Copia mp4, Short, miniatura, srt, guion, metadatos y posts a `/mnt/project-files/qatar-ai-stocks/educativo/<base>/`; `SCRATCH=<scratch> bash encolar.sh <carpeta>`.
6. Actualiza `plan-qatar.json` (estado `publicada`, fecha, IDs) y abre o actualiza el PR de la rama para que quede en main. Mensaje corto en el hilo.
