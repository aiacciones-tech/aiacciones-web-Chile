# Video diario en árabe de la Bolsa de Qatar (índice QE General)

Cada día de sesión de la QSE (domingo a jueves), después del cierre (13:15 en Doha, 10:15 UTC): un video de máximo 3 minutos y su Short
para @QatarAIStocks, todo en árabe (voz, textos en pantalla, título, descripción y posts), con posts en X y Facebook (Buffer 1), LinkedIn,
TikTok e Instagram (Buffer 2) y Telegram. Adaptado del video diario de España (`espana/diario/`) a partir de su versión árabe de EAU (`eau/diario/`).
Muestra: sesión del jueves 5-nov-2026 (`ejemplo-2026-11-05/`). Formato aprobado por Daniel el 7-nov-2026: datos a las 13:45 de Doha y rutina diaria a las 14:15 (domingo a jueves), publicación automática.

## Guion (7 escenas, `make_video.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre del QE, variación en % y en puntos, variación semanal y curva intradía (5 min, hora de Doha).
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente en pantalla (comunicados en la QSE, resultados, dividendos, operaciones, QFMA, Banco Central de Qatar, GNL y petróleo, Wall Street/Asia).
3. **Análisis fundamental** (`s_fact`): barras del QE y de sus mayores valores (o de otras bolsas) + 3-4 factores (Brent y GNL, Fed y QCB, flujos extranjeros si hay datos publicados, macro).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan (automático; solo valores con más de 1 millón de riales negociados), con su motivo. Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa.
5. **Técnico** (`s_tech`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias (los del guion, dibujados y en la tabla), RSI 14, estocástico (14,3,3) y volumen frente a su media de 10 sesiones. «هذه بيانات وليست إشارات شراء أو بيع».
6. **Agenda** (`s_agenda`): resultados, dividendos y datos de los próximos días.
7. **Cierre** (`s_fin`): resumen y aviso legal completo en árabe (también en la descripción).

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-qatar.yml`) y deja `datos/mercado-<fecha>.json` en la rama `datos-diario-qa`:
velas diarias e intradía de `QSE:GNRI` (websocket de TradingView), cambio, volumen y valor negociado de todas las acciones de la QSE
(escáner `qatar`) y contexto (Brent, GNL JKM y TTF, Henry Hub, Golfo, Wall Street, Asia, bonos, oro, dólar).
La vela del índice no trae volumen: se calcula sumando las acciones frente a su media de 10 sesiones.
`python3 tecnico.py <mercado.json>` imprime cierre, variación diaria y semanal (semana de domingo a jueves), medias, RSI, estocástico, niveles, volumen y los 5 que más suben/bajan.
Programación: `cron: "45 10 * * 0-4"` (13:45 en Doha); también a mano (workflow_dispatch).

## Pasos de cada día
1. Datos de la rama `datos-diario-qa`. Solo hay video si la última vela es de hoy (en festivos no se guarda nada).
2. Noticias y motivos: QNA (vía الشرق / الراية / Qatar Tribune), Reuters (Business Recorder, Zawya), Gulf Times, The Peninsula, Argaam, comunicados en qe.com.qa.
   Una cifra de una sola fuente no va; si dos fuentes discrepan, se usa la de los datos de TradingView/QSE y se dice.
3. Copia `ejemplo-2026-11-05/` a la carpeta del día y cambia `video.json` (textos de pantalla y locución, números en palabras), `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena).
4. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 180 s).
5. `AUD=<scratch> python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>`. Todo lo que se entrega termina en `-qatar` (regla de Daniel).
6. `SCRATCH=<scratch> bash encolar.sh <dir>`: comprueba el límite de YouTube (~10 subidas/24 h, compartido con los videos de resultados) y encola en `cola-qa/bolsa-<fecha>` de `youtube-cola`.

## Árabe
- Fuente Noto Naskh Arabic (`fonts/`, OFL). `comun.ar()` une las letras con arabic-reshaper; con matplotlib 3.11+ el orden RTL lo hace libraqm,
  y las cifras con signo o % se aíslan (U+2066…U+2069) para que se vean «+1.84%» y no «%1.84+». Con matplotlib anterior se usa python-bidi.
- Voz: Piper `ar_JO-kareem-medium` (`/mnt/project-files/qatar-ai-stocks/pipeline/voz/`), `LENGTH_SCALE=0.8`. Cifras en pantalla con dígitos occidentales; en la voz, en palabras.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi`.

## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Todos los posts y descripciones llevan el enlace al canal https://www.youtube.com/@QatarAIStocks (regla de Daniel).
