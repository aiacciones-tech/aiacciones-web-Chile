# Video diario en árabe de la bolsa de EAU (FTSE ADX General y DFM General)

Cada día hábil (lunes a viernes), después del cierre de ADX y DFM (15:00 en EAU, 11:00 UTC): un video de máximo 5 minutos (desde el 10-nov-2026; antes 3) y su Short
para @AIStocksUAE, todo en árabe (voz, textos en pantalla, título, descripción y posts), con posts en X, LinkedIn, Facebook, TikTok,
Instagram y Telegram. Adaptado del video diario de España (`espana/diario/`). Plantilla: sesión del martes 10-nov-2026 (`ejemplo-2026-11-10/`, formato de 5 minutos con más técnico). `ejemplo-2026-11-06/` es la muestra antigua de 3 minutos.

## Guion (9 escenas, `make_video.py`)

Daniel (10-nov-2026): hasta 5 minutos y más peso del análisis técnico. Reparto orientativo: apertura, noticias, fundamental y valores ~1:20; técnico ~2:50 (más de la mitad); agenda y cierre ~0:35.
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre de los dos índices, variación en % y en puntos, curva intradía (5 min) de cada uno.
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente en pantalla (comunicados en ADX/DFM, resultados, dividendos, operaciones, SCA, banco central, petróleo, Wall Street/Asia).
3. **Análisis fundamental** (`s_fact`): barras de bolsas del Golfo, Asia, Europa y EE. UU. + 3-4 factores (Brent, Fed y banco central de EAU, flujos extranjeros si hay datos publicados, macro).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan de ADX y DFM juntos (automático; solo valores con más de 1 millón de AED negociados), con su motivo. Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa.
5. **Técnico ADX** (`s_tech_adx`) y 6. **Técnico DFM** (`s_tech_dfm`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias, RSI 14, estocástico (14,3,3) y volumen frente a su media de 10 sesiones. Cada escena técnica lleva unas 85-95 palabras de voz: posición frente a las dos medias (en %), cruce de medias (dorado o de la muerte, con fecha), las dos resistencias y los dos soportes con su distancia, RSI y su zona, estocástico y su zona (y si acaba de salir de una), volumen.
7. **Panel técnico** (`s_tech_panel`): los dos índices lado a lado: tendencia (media 50 frente a 200 y último cruce), rendimiento a 1 mes, 3 meses y en el año, resistencia y soporte más cercanos con su distancia, volumen, y barras del rango de 52 semanas, RSI 14 y estocástico %K. Voz de ~60-70 palabras que compare los dos y termine con «هذه بيانات تصف حركة الأسعار، وليست إشارات شراء أو بيع». Datos: `perf_1m`, `perf_3m`, `perf_ytd`, `cruce`, `pos_52s_pct`, `res_cercana`/`dist_res_pct`, `sop_cercano`/`dist_sop_pct`, `rsi_zona`, `estoc_zona` de `tecnico.py`. Título opcional en `video.json` → `tecnico.panel.titulo`. Si el guion no trae `voz.s_tech_panel`, la escena se omite (guiones antiguos).
8. **Agenda** (`s_agenda`): resultados, dividendos, salidas a bolsa y datos de los próximos días.
9. **Cierre** (`s_fin`): resumen y aviso legal completo en árabe (también en la descripción).

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
3. Copia `ejemplo-2026-11-10/` a la carpeta del día y cambia `video.json` (textos de pantalla y locución, números en palabras), `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena).
4. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 300 s; la voz árabe es lenta: ~1,45 palabras/s, unas 400-430 palabras en total, de ellas ~240 en el técnico). Añade `["s_tech_panel", "لوحة المؤشرات الفنية"]` en `info.json` → `capitulos` después de `s_tech_dfm`.
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

## LinkedIn (regla permanente de Daniel, 8-nov-2026)
En LinkedIn va el Short subido como video (no como enlace): `encolar.sh` pone `post-linkedin.txt` en `cola-eau/bolsa-<fecha>-short/`.
El texto (`info.json` → `linkedin`: `datos` con 3 o 4 cifras clave y qué cambió, y `conclusion`) es un resumen con valor, sin relleno,
dice «فيديو من إعداد قناة AI Stocks UAE» y termina con el enlace al canal https://www.youtube.com/@AIStocksUAE.
Facebook sigue con el texto largo y el enlace al video (`post-facebook.txt` en la carpeta del video largo).

## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Todos los posts y descripciones llevan el enlace al canal https://www.youtube.com/@AIStocksUAE (regla de Daniel, 29-oct-2026).
