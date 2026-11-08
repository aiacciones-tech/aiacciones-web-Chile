# Video diario en árabe de la bolsa de EAU (FTSE ADX General y DFM General)

Cada día hábil (lunes a viernes), después del cierre de ADX y DFM (15:00 en EAU, 11:00 UTC): un video de máximo 3 minutos y su Short
para @AIStocksUAE, todo en árabe (voz, textos en pantalla, título, descripción y posts), con posts en X, LinkedIn, Facebook, TikTok,
Instagram y Telegram. Adaptado del video diario de España (`espana/diario/`). Muestra: sesión del viernes 6-nov-2026 (`ejemplo-2026-11-06/`).

## Guion (8 escenas, `make_video.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre de los dos índices, variación en % y en puntos, curva intradía (5 min) de cada uno.
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente en pantalla (comunicados en ADX/DFM, resultados, dividendos, operaciones, SCA, banco central, petróleo, Wall Street/Asia).
3. **Análisis fundamental** (`s_fact`): barras de bolsas del Golfo, Asia, Europa y EE. UU. + 3-4 factores (Brent, Fed y banco central de EAU, flujos extranjeros si hay datos publicados, macro).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan de ADX y DFM juntos (automático; solo valores con más de 1 millón de AED negociados), con su motivo. Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa.
5. **Técnico ADX** (`s_tech_adx`) y 6. **Técnico DFM** (`s_tech_dfm`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias, RSI 14, estocástico (14,3,3) y volumen frente a su media de 10 sesiones. «هذه بيانات وليست إشارات شراء أو بيع».
7. **Agenda** (`s_agenda`): resultados, dividendos, salidas a bolsa y datos de los próximos días.
8. **Cierre** (`s_fin`): resumen y aviso legal completo en árabe (también en la descripción).

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-eau.yml`, 11:40 UTC de lunes a viernes) y deja `datos/mercado-<fecha>.json` en la rama
`datos-diario-eau`: velas diarias e intradía de `ADX:FADGI` y `DFM:DFMGI` (websocket de TradingView), cambio, volumen y valor negociado de todas
las acciones de ADX y DFM (escáner `uae` de TradingView) y contexto (Brent, Wall Street, Asia, Tadawul, Qatar, bonos, oro, dólar).
`python3 tecnico.py <mercado.json>` imprime cierres, variaciones, medias, RSI, estocástico, niveles, volumen y los 5 que más suben/bajan.
El volumen de DFM no viene en la vela del índice: se calcula sumando las acciones del mercado frente a su media de 10 sesiones.

## Pasos de cada día
1. Datos de la rama `datos-diario-eau`. Solo hay video los días en que abren ADX y DFM (lunes a viernes; fin de semana de EAU: sábado y domingo).
   En festivos (Eid, Día Nacional, Año Nuevo...) no se guarda `mercado-<hoy>.json` porque la última vela no es de hoy: ese día no se hace video.
2. Noticias y motivos: Reuters (Business Recorder, Zawya), Gulf News, The National, Khaleej Times, WAM, AGBI, Argaam, Finimize, comunicados en ADX/DFM.
3. Copia `ejemplo-2026-11-06/` a la carpeta del día y cambia `video.json` (textos de pantalla y locución, números en palabras), `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena).
4. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 180 s; la voz árabe es lenta: unas 230 palabras en total).
5. `AUD=<scratch> python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>`. Todo lo que se entrega termina en `-UAE` (regla de Daniel, 5-nov-2026).
6. `SCRATCH=<scratch> bash encolar.sh <dir>`: comprueba el límite de YouTube (~10 subidas/24 h, compartido con los videos de resultados) y encola en `cola-eau/bolsa-<fecha>` de `youtube-cola`.

## Árabe
- Fuente: Noto Naskh Arabic (`fonts/`, OFL; árabe + latín unidos con fontTools desde `@fontsource/noto-naskh-arabic`).
- Texto: `comun.ar()` une las letras con arabic-reshaper y ordena de derecha a izquierda con python-bidi. matplotlib 3.11+ ya hace el orden RTL
  con libraqm, así que entonces solo se aplica reshaper (si se aplicaran los dos, el texto saldría al revés).
- Voz: Piper `ar_JO-kareem-medium` (`/mnt/project-files/aistocksuae/pipeline/voz/`, del espejo de sherpa-onnx porque huggingface está bloqueado); piper-tts 1.8+ pone el tashkeel. `LENGTH_SCALE=0.8`.
- Cifras en pantalla con dígitos occidentales (como la prensa financiera de EAU); en la voz, en palabras.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi`.

## Campaña de comentarios y suscripción (hasta el 22-nov-2026)
Daniel (8-nov-2026): durante dos semanas cada video y Short pide un comentario para mejorar el canal e invita a suscribirse.
Va solo (constantes `CTA_*` de `comun.py`): se añade a la voz del cierre del video y del Short, a la pantalla final y al principio de la descripción
de YouTube. Se apaga sola para las sesiones posteriores al 22-nov-2026 (`CTA_HASTA`). Con ella la voz suma unos 5 s: deja el resto en unas 220 palabras.

<<<<<<< HEAD
## LinkedIn (regla permanente de Daniel, 8-nov-2026)
En LinkedIn va el Short subido como video (no como enlace): `encolar.sh` pone `post-linkedin.txt` en `cola-eau/bolsa-<fecha>-short/`.
El texto (`info.json` → `linkedin`: `datos` con 3 o 4 cifras clave y qué cambió, y `conclusion`) es un resumen con valor, sin relleno,
dice «فيديو من إعداد قناة AI Stocks UAE» y termina con el enlace al canal https://www.youtube.com/@AIStocksUAE.
Facebook sigue con el texto largo y el enlace al video (`post-facebook.txt` en la carpeta del video largo).

=======
>>>>>>> origin/claude/project-thread-7yb9ev
## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Todos los posts y descripciones llevan el enlace al canal https://www.youtube.com/@AIStocksUAE (regla de Daniel, 29-oct-2026).
