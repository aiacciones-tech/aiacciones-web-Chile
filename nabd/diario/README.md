# Video diario en árabe de Wall Street para Nabd Wall Street (نبض وول ستريت)

Cada día de sesión en Nueva York (lunes a viernes; cierre a las 16:00 ET, que son las 00:00 en Riad y la 01:00 en Dubái en invierno,
y una hora antes en verano; sin video en festivos de EE. UU.): un video de máximo 3 minutos y su Short para el canal
Nabd Wall Street (https://www.youtube.com/channel/UCRU3n034y5dJBEGnhAKjhfQ), todo en árabe. Adaptado del video diario de Arabia Saudita (`saudi/diario/`).
Muestra: sesión del viernes 6-nov-2026 (`ejemplo-2026-11-06/`).

## Guion (7 escenas, `make_video.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre del S&P 500 con variación en % y en puntos, Nasdaq Composite, Dow Jones y Russell 2000,
   y curva intradía del S&P 500 (5 min, en hora de La Meca/Riad).
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente (datos macro, resultados, Fed, política, petróleo).
3. **Análisis fundamental** (`s_fact`): barras de los índices de EE. UU. (en dorado) y de Golfo, Europa y Asia del mismo día + 2-4 factores
   (bonos, Fed, petróleo, VIX, dólar).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan del S&P 500 (automático; más de 50 millones de dólares negociados), con su motivo.
   Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa. Línea extra con las 7 grandes (`tecnico.grandes`).
5. **Técnico S&P 500** (`s_tech`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias, RSI 14, estocástico (14,3,3), volumen frente a su media de 10 sesiones.
6. **Agenda** (`s_agenda`): datos macro, resultados y festivos de los próximos días, con hora de La Meca (Nueva York + 8 h en invierno, + 7 h en verano).
7. **Cierre** (`s_fin`): resumen y aviso legal completo en árabe (también en la descripción).
La campaña de comentarios y suscripción (`campana.py`) está apagada en Nabd.

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-Nabd.yml`, 21:40 UTC de lunes a viernes) y deja `datos/mercado-<fecha>.json`
en la rama `datos-diario-nabd`: velas diarias de `SP:SPX`, `NASDAQ:IXIC`, `DJ:DJI` y `TVC:RUT`, intradía del S&P 500, las acciones grandes de EE. UU.
(las del S&P 500 se distinguen por su campo `indexes`) y el contexto (VIX, Brent, oro, bono a 10 años, dólar, bitcóin, Golfo, Europa, Asia).
El contenedor de Claude no llega a TradingView ni a Yahoo. En festivos no se guarda nada porque la última vela no es de hoy.
`python3 tecnico.py <mercado.json>` imprime cierres, variaciones (día, semana, año), medias, RSI, estocástico, niveles, los 5 que más suben/bajan, las 7 grandes y el contexto.

## Pasos de cada día
1. Datos de la rama `datos-diario-nabd`.
2. Noticias y motivos: Yahoo Finance (live blog del día), CNBC, Reuters, The Closing Print, StockTitan. Solo cuenta lo publicado ese día.
3. Copia `ejemplo-2026-11-06/` a la carpeta del día (sin los mp4/png) y cambia `video.json` (pantalla y locución, números en palabras),
   `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena). Nombres en árabe que falten: `"nombres"` en `video.json`.
4. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 180 s; unas 230 palabras de locución).
5. `AUD=<scratch> python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>`. Todo lo que se entrega termina en `-Nabd` (regla de Daniel, 8-nov-2026).
6. `SCRATCH=<scratch> bash encolar.sh <dir>`: comprueba los archivos y el enlace del canal, el límite de YouTube (~10 subidas/24 h) y encola en
   `cola-nabd/bolsa-<fecha>` y `cola-nabd/bolsa-<fecha>-short` de `youtube-cola`; `youtube-Nabd.yml` los sube.
   Nabd aún no tiene Buffer ni Telegram: los posts se generan pero no se encolan.

## Árabe y marca
- Fuente: Tajawal (`fonts/`, OFL, la de la marca). Texto: `comun.ar()` une las letras con arabic-reshaper; matplotlib 3.11+ ordena de derecha a izquierda.
- Voz: Piper `ar_JO-kareem-medium` (`/mnt/project-files/nabd-pipeline/voice/`, descargada de las releases tts-models de sherpa-onnx). `LENGTH_SCALE=0.8`.
- Cifras en pantalla con dígitos occidentales; en la voz, en palabras.
- Marca: noche #0B1A2E, dorado #D4AF37, marfil #F5EBDD, sube #22C55E, baja #E5484D; logo `/mnt/project-files/nabd-brand-kit/png/profile-800-Nabd.png`.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi websocket-client`.

## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Transparencia: guion, voz y gráficos hechos con IA (lo dice el cierre y la descripción).
