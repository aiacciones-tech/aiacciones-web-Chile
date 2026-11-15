# ⚠️ INSTRUCCIONES VIGENTES DE LA TAREA DIARIA (10-nov-2026) — LEER ANTES DE NADA

Desde el 10-nov-2026 el vídeo diario dura **8 a 10 minutos** (manual de Daniel). Estas instrucciones **sustituyen** a las del texto
de la tarea programada allí donde difieran: ya **no** valen "~230 palabras", "máx. 180 s", ni la voz Piper como primera opción,
ni `ejemplo-2026-11-06/` como plantilla (esa carpeta solo redirige aquí; la plantilla es `ejemplo-2026-11-09/`).
`make_video.py` rechaza vídeos de menos de 450 s o más de 630 s. Daniel lo aprobó en el hilo del vídeo largo (10-nov-2026).

> Prepara y publica el vídeo diario en árabe de Wall Street del canal Nabd Wall Street (نبض وول ستريت, id UCRU3n034y5dJBEGnhAKjhfQ): el programa «التقرير اليومي», de 8 a 10 minutos, según el manual de producción de Daniel (10-nov-2026). Daniel aprobó (9-nov-2026) publicarlo automáticamente y en público cada día de sesión, sin revisión previa. No quiere ningún paso manual.
>
> Repo: aiacciones-tech/aiacciones-web-Chile. Usa nabd/diario/ de main. Sigue nabd/diario/README.md al pie de la letra ("Guion", "Voz", "Pasos de cada día" y "Reglas"). Solo toca nabd/, sus workflows y cola-nabd/.
>
> 1. Datos: busca hoy (fecha de Nueva York) datos/mercado-<fecha>.json en la rama datos-diario-nabd. GitHub retrasa a veces el cron: si no está, lanza tú el workflow datos-diario-Nabd.yml (workflow_dispatch en main) y espera a que termine. Si la última vela no es de hoy (festivo o fin de semana), termina sin publicar nada.
> 2. Copia ejemplo-2026-11-09/ (sin mercado.json, mp4, png, md, csv, meta ni post) a nabd/diario/<fecha>/ y pon el mercado.json del día. Ejecuta tecnico.py: cifras, medias 20/50/200, escenarios, sectores, macro, aportación al Dow, grandes del Nasdaq 100 y candidatas.
> 3. Investiga las noticias de la sesión de hoy (Yahoo Finance live blog, CNBC, Reuters, The Closing Print, StockTitan; Fed, BLS, BEA, Tesoro, SEC EDGAR y notas de resultados cuando existan): qué pasó, por qué, sectores, y elige 5 acciones de las candidatas por su relevancia (resultados, noticia, volumen inusual), no solo por el %. Solo lo publicado hoy; si no hay motivo, «لا يوجد خبر محدد في الصحافة». Nunca inventes una cifra, noticia ni nivel: los niveles técnicos y los escenarios salen de tecnico.py. Agenda de la próxima sesión con hora de Nueva York (la de La Meca se calcula sola).
> 4. Reescribe video.json (17 escenas: locución en árabe estándar con números en palabras, entre 7:30 y 10:30 min; objetivo 8-10, unas 950-1.050 palabras con Azure), info.json (sin capítulos: salen solos) y short.json (< 59 s). Diferencia hechos, opiniones y escenarios; escenarios siempre como condiciones, nunca previsiones. Sin recomendaciones de compra/venta.
> 5. Voz (Azure ar-SA-HamedNeural, secretos ya configurados): sube nabd/diario/<fecha>/video.json a la rama claude/nabd-diario-<fecha> (creada desde main); voz-Nabd.yml genera la voz (unos 2 min) y la deja en <fecha>/ de la rama voz-nabd: clónala y usa VOZ_DIR=<clon>/<fecha>. Si cambias la locución después, vuelve a subir video.json y espera la voz nueva. Si el workflow dice que falta el secreto AZURE_SPEECH_KEY_NABD o falla, sigue con Piper (make_video.py lo hace solo sin VOZ_DIR) y dilo en el resumen.
> 6. Render: preview primero y mira TODOS los PNG (textos cortados, solapes, cifras que no cuadren con la locución); luego make_video.py (con VOZ_DIR si hay voz de Azure), make_short.py y gen_meta.py. Si el control de calidad de make_video.py falla, corrige la causa; no lo saltes. Piper ar_JO-kareem-medium está en /mnt/project-files/nabd-pipeline/voice/.
> 7. Publica: SCRATCH=<scratch> bash nabd/diario/encolar.sh nabd/diario/<fecha>. Si en 10 min no aparece resultado.json, lanza el workflow youtube-Nabd.yml con modo=subir.
> 8. Copia el vídeo, el Short, la miniatura, el meta, guion-<fecha>-Nabd.md y datos-<fecha>-Nabd.csv a /mnt/project-files/nabd-diario/<fecha>/ (todos los nombres terminan en -Nabd). Haz commit de video.json, info.json y short.json del día (no del mercado.json, que ya está en datos-diario-nabd) en la rama claude/nabd-diario-<fecha> y abre PR.
> 9. Termina con un resumen corto en español: enlaces de YouTube del vídeo y el Short, duración, voz usada (Azure o Piper), si salieron públicos, y cualquier fallo.

---

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
Duración aceptada: 450-630 s. Con Azure salen unas 110 palabras por minuto, pausas incluidas (900 palabras = 8:00; unas 1.000 para 9 min);
con Piper, unas 90 (las mismas 900 palabras = 9:50).

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

## Presentador IA (HeyGen), martes y jueves
Prueba de un mes pedida por Daniel (14-nov-2026): los **martes y jueves** (fecha de la sesión en Nueva York), `voz-Nabd.yml`, después de la voz
de Azure, ejecuta `avatar_heygen.py`: monta el audio de la apertura (`s_title`) igual que `make_video.py`, anima `avatar/presentador.png`
con la API de HeyGen (Avatar IV, unos 2-3 min, ~2,3 $/min) y deja `avatar.mp4` y `avatar.json` en `<fecha>/` de la rama `voz-nabd`.
`make_video.py` lo detecta solo con `VOZ_DIR` y pone al presentador hablando en un recuadro de la apertura (en lugar del gráfico intradía)
si `avatar.json` trae `ok: true` y el mismo texto de `s_title`; si no, el vídeo sale como siempre. Nunca bloquea: sin saldo (menos de 2 $),
apertura de más de 45 s, error de la API o sin el secreto `HEYGEN_API_KEY`, `avatar.json` dice el motivo y se sigue sin presentador.
Si cambias la apertura después de generar la voz, el avatar ya no coincide: vuelve a subir `video.json` (se genera otro, y se paga otra vez).
"Run workflow" de `voz-Nabd.yml` con avatar=si lo fuerza cualquier día; avatar=no lo apaga.

## Pasos de cada día
1. Datos de la rama `datos-diario-nabd` (si faltan, lanza `datos-diario-Nabd.yml` y espera).
2. `python3 tecnico.py` y noticias: Yahoo Finance (live blog del día), CNBC, Reuters, The Closing Print, StockTitan; fuentes oficiales (Fed, BLS,
   BEA, Tesoro, SEC EDGAR, notas de resultados) cuando las haya. Solo cuenta lo publicado ese día. Agenda de la próxima sesión con hora de Nueva York.
3. Copia `ejemplo-2026-11-09/` (sin mercado.json, mp4, png, md ni csv) a `nabd/diario/<fecha>/`, pon el `mercado.json` del día y reescribe
   `video.json` (pantalla y locución en árabe estándar, números en palabras), `info.json` (título, descripción, posts, miniatura; los capítulos
   salen solos) y `short.json` (menos de 59 s; fecha en la primera escena). Nombres en árabe que falten: `"nombres"` en `video.json`.
4. Sube `video.json` a la rama `claude/nabd-diario-<fecha>`: `voz-Nabd.yml` genera la voz de Azure (unos 2-4 min; martes y jueves, unos 3 min
   más por el presentador HeyGen); descarga la rama `voz-nabd` cuando el workflow termine.
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
