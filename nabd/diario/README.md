# Video diario en árabe de Wall Street para Nabd Wall Street (نبض وول ستريت)

Cada día de sesión en Nueva York (lunes a viernes; cierre a las 16:00 ET, que son las 00:00 en Riad y la 01:00 en Dubái en invierno,
y una hora antes en verano; sin video en festivos de EE. UU.): un video de **8 a 10 minutos** (التقرير اليومي) y su Short para el canal
Nabd Wall Street (https://www.youtube.com/channel/UCRU3n034y5dJBEGnhAKjhfQ), todo en árabe, según el manual de producción de Daniel (10-nov-2026).
Muestra: sesión del lunes 9-nov-2026 (`ejemplo-2026-11-09/`).

## Guion (8 secciones, 17 escenas, `make_video.py`)
1. **Introducción** (`s_title`, ~30 s): qué pasó, mejor y peor índice, la noticia del día; cierre del S&P 500 y curva intradía.
2. **Los grandes índices** (~90 s): `s_indices` tabla animada de S&P 500, Nasdaq 100, Dow Jones y Russell 2000 (cierre, día, semana,
   distancia al máximo histórico, distancia a la media de 200, tendencia); `s_grandes` las 8 mayores del Nasdaq 100 y la aportación en puntos
   de cada valor al Dow Jones (calculada); `s_news` por qué se movió el mercado (noticias con fuente).
3. **Sectores** (`s_sectores`, ~60 s): XLK, XLF, XLE, XLV, XLY, XLI; los dos mejores y los dos peores y sus posibles razones.
4. **Cinco acciones protagonistas** (`s_accion_1`…`5`, ~120 s): elegidas de `candidatas` (tecnico.py: movimiento × volumen relativo) por su
   relevancia (resultados, noticia, volumen inusual), no solo por el %. Cada una: nombre, ticker, precio, %, volumen, volumen frente a su media,
   noticia y lectura, con velas de 3 meses. Sin noticia publicada: «لا يوجد خبر محدد في الصحافة»; nunca se inventa.
5. **Macro** (`s_macro`, ~60 s): bono a 10 años, DXY, VIX, WTI y oro con su línea de 15 sesiones, y el petróleo y el Golfo.
6. **Técnico** (~120 s): `s_tech_spx` / `s_tech_ndx` (velas de 6 meses, medias de 20, 50 y 200 sesiones, volumen, RSI 14, soportes y
   resistencias) y `s_esc_spx` / `s_esc_ndx` con tres escenarios (alcista, neutral, bajista) cuyos niveles calcula `tecnico.escenarios`
   (los textos de pantalla salen solos de los datos; la locución repite esas cifras).
7. **Qué esperamos mañana** (`s_agenda`, ~60 s): filas `[fecha ISO, evento, hora de Nueva York "HH:MM" o "", estado]`; la hora de La Meca se calcula.
8. **Despedida y Telegram** (`s_fin`, ~30 s): resumen, invitación a t.me/NabdWallStreet y aviso legal.
En todas: ticker inferior (índices, macro, sectores y titulares de `video.json` → `ticker`) y subtítulos árabes frase a frase (el texto de la locución).

`make_video.py` hace antes un **control de calidad** (manual, sección 8): fecha de las velas, sesiones suficientes para la media de 200,
sectores y macro presentes, las 5 acciones en los datos y con noticia/lectura/voz, agenda posterior a la sesión; si algo falla, no renderiza.
Además escribe `guion-<fecha>-Nabd.md` (tabla tiempo | narración | visual | datos) y `datos-<fecha>-Nabd.csv` (datos usados con fuente y hora).
Duración aceptada: 450-630 s. Con Piper salen unas 80 palabras por minuto (unas 750 palabras para 9 min); con Azure, unas 115 (unas 1.000).

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-Nabd.yml`, 21:40 UTC de lunes a viernes) y deja `datos/mercado-<fecha>.json`
en la rama `datos-diario-nabd`: velas diarias (hasta 5.000 sesiones, para el máximo histórico) de `SP:SPX`, `NASDAQ:NDX`, `NASDAQ:IXIC`, `DJ:DJI`
y `TVC:RUT`, intradía del S&P 500, las acciones grandes de EE. UU. (las del S&P 500, Nasdaq 100 y Dow se distinguen por su campo `indexes`),
velas de 70 sesiones de las acciones candidatas, los ETF sectoriales y el contexto (VIX, WTI, Brent, oro, bono a 10 años, dólar, Golfo, Europa, Asia).
GitHub puede retrasar horas el cron: si a las 21:47 UTC no está el archivo del día, la sesión diaria lanza `datos-diario-Nabd.yml` a mano.
El contenedor de Claude no llega a TradingView, Yahoo ni Azure. En festivos no se guarda nada porque la última vela no es de hoy.
`python3 tecnico.py <mercado.json>` imprime cierres, variaciones, medias 20/50/200, RSI, niveles, escenarios, tendencia, sectores, macro,
aportación al Dow, las 8 grandes del Nasdaq 100 y las acciones candidatas.

## Voz
- **Azure** `ar-SA-HamedNeural` (más natural): `voz-Nabd.yml` la genera en GitHub Actions al subir `nabd/diario/<fecha>/video.json` a una rama
  `claude/nabd-diario-*` (o con "Run workflow", modo=generar y la fecha) y deja un wav por frase en `<fecha>/` de la rama `voz-nabd`.
  `VOZ_DIR=<esa carpeta> python3 make_video.py ...` los usa. Necesita los secretos `AZURE_SPEECH_KEY_NABD` y `AZURE_SPEECH_REGION_NABD`
  (plan gratuito F0: 500.000 caracteres al mes). modo=verificar prueba la clave.
- **Piper** `ar_JO-kareem-medium` (respaldo, si no hay wav de Azure para todas las frases): `/mnt/project-files/nabd-pipeline/voice/`. `LENGTH_SCALE=0.8`.
Las frases se parten igual en los dos sitios (`voz_frases.py`); nunca se mezclan las dos voces en un vídeo.

## Pasos de cada día
1. Datos de la rama `datos-diario-nabd` (si faltan, lanza `datos-diario-Nabd.yml` y espera).
2. `python3 tecnico.py` y noticias: Yahoo Finance (live blog del día), CNBC, Reuters, The Closing Print, StockTitan; fuentes oficiales (Fed, BLS,
   BEA, Tesoro, SEC EDGAR, notas de resultados) cuando las haya. Solo cuenta lo publicado ese día. Agenda de la próxima sesión con hora de Nueva York.
3. Copia `ejemplo-2026-11-09/` (sin mercado.json, mp4, png, md ni csv) a `nabd/diario/<fecha>/`, pon el `mercado.json` del día y reescribe
   `video.json` (pantalla y locución en árabe estándar, números en palabras), `info.json` (título, descripción, posts, miniatura; los capítulos
   salen solos) y `short.json` (menos de 59 s; fecha en la primera escena). Nombres en árabe que falten: `"nombres"` en `video.json`.
4. Sube `video.json` a la rama `claude/nabd-diario-<fecha>`: `voz-Nabd.yml` genera la voz de Azure (unos 2-4 min); descarga la rama `voz-nabd`.
5. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego `AUD=<scratch> VOZ_DIR=<voz-nabd>/<fecha> python3 make_video.py <dir>`.
6. `AUD=<scratch> python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>`. Todo lo que se entrega termina en `-Nabd` (regla de Daniel, 8-nov-2026).
7. `SCRATCH=<scratch> bash encolar.sh <dir>`: comprueba los archivos y el enlace del canal, el límite de YouTube (~10 subidas/24 h) y encola en
   `cola-nabd/bolsa-<fecha>` y `cola-nabd/bolsa-<fecha>-short` de `youtube-cola`; `youtube-Nabd.yml` los sube.
   El post de Telegram va como `post-telegram.txt` del video largo y lo publica `telegram-Nabd.yml`; LinkedIn, X, TikTok e Instagram los publica `buffer-Nabd.yml`.

## Árabe y marca
- Fuente: Tajawal (`fonts/`, OFL, la de la marca). Texto: `comun.ar()` une las letras con arabic-reshaper; matplotlib 3.11+ ordena de derecha a izquierda,
  y las cifras van aisladas (LRI/PDI) para que «+13.26%» no se invierta dentro de una frase árabe.
- Nombre: marca Nabd Wall Street (نبض وول ستريت); el programa se llama «التقرير اليومي» (no «Wall Street Daily», que es una marca existente).
- Cifras en pantalla con dígitos occidentales; en la voz, en palabras.
- Marca: noche #0B1A2E, dorado #D4AF37, marfil #F5EBDD, sube #22C55E, baja #E5484D; logo `/mnt/project-files/nabd-brand-kit/png/profile-800-Nabd.png`.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi websocket-client`.

## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Hechos, opiniones y escenarios separados; los escenarios son condiciones («si cierra por encima de…»), nunca previsiones ni promesas.
Transparencia: guion, voz y gráficos hechos con IA (lo dice el cierre y la descripción).
