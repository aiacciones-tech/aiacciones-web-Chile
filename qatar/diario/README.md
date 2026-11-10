# Video diario en árabe de la Bolsa de Qatar (índice QE General)

Cada día de sesión de la QSE (domingo a jueves), después del cierre (13:15 en Doha, 10:15 UTC): un video de unos 5 minutos (máximo 300 s) con énfasis en el análisis técnico, y su Short
para @QatarAIStocks, todo en árabe (voz, textos en pantalla, título, descripción y posts), con posts en X y Facebook (Buffer 1), LinkedIn,
TikTok e Instagram (Buffer 2) y Telegram. Adaptado del video diario de España (`espana/diario/`) a partir de su versión árabe de EAU (`eau/diario/`).
Muestra: sesión del jueves 5-nov-2026 (`ejemplo-2026-11-05/`). Formato aprobado por Daniel el 7-nov-2026: datos a las 13:45 de Doha y rutina diaria a las 14:15 (domingo a jueves), publicación automática.
Desde el 11-nov-2026 (pedido de Daniel el 10-nov): 5 minutos y 4 escenas técnicas. Ejemplo del formato nuevo: `ejemplo-2026-11-10/`.

## Guion (10 escenas, `make_video.py`; unos 290 s)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre del QE, variación en % y en puntos, variación semanal y curva intradía (5 min, hora de Doha).
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente en pantalla (comunicados en la QSE, resultados, dividendos, operaciones, QFMA, Banco Central de Qatar, GNL y petróleo, Wall Street/Asia).
3. **Análisis fundamental** (`s_fact`): barras del QE y de sus mayores valores (o de otras bolsas) + 3-4 factores (Brent y GNL, Fed y QCB, flujos extranjeros si hay datos publicados, macro).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan (automático; solo valores con más de 1 millón de riales negociados), con su motivo. Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa.
5. **Técnico 1: tendencia y niveles** (`s_tech`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias (los del guion, dibujados y en la tabla), RSI 14, estocástico (14,3,3) y volumen frente a su media de 10 sesiones.
6. **Técnico 2: momento y volatilidad** (`s_momentum`): MACD (12,26,9) con su señal e histograma, último cruce, bandas de Bollinger (20,2), %B y anchura de las bandas frente al último año. Automático (`tecnico.py`).
7. **Técnico 3: Fibonacci y rendimientos** (`s_fibo`): retrocesos de Fibonacci del tramo entre el máximo y el mínimo de 52 semanas, con la distancia del cierre a cada nivel, y rendimiento a 1 semana, 1, 3 y 6 meses, 1 año y en el año. Automático.
8. **Técnico 4: amplitud y grandes valores** (`s_amplitud`): % de valores sobre sus medias de 50 y 200 sesiones, cuántos tienen RSI > 70 o < 30 y cuántos están en máximos de 52 semanas; tabla de los 8 mayores por capitalización (cambio, distancia a medias 50/200, RSI, distancia al máximo de 52 semanas). Datos del escáner de TradingView (columnas `RSI`, `SMA50`, `SMA200`, `price_52_week_high` en `datos_mercado.py`).
   En las 4 escenas técnicas: «هذه بيانات وليست إشارات شراء أو بيع»; nunca «comprar/vender», objetivos ni «barato/caro». Títulos automáticos; `video.json` → `tecnico.{momentum,fibo,amplitud}.titulo` los cambia.
9. **Agenda** (`s_agenda`): resultados, dividendos y datos de los próximos días.
10. **Cierre** (`s_fin`): resumen y aviso legal completo en árabe (también en la descripción).

Locución: `video.json` → `voz` con una entrada por escena (`s_title` … `s_fin`, incluidas `s_momentum`, `s_fibo`, `s_amplitud`). Unas 380-420 palabras en total; las 4 técnicas, unas 60-80 palabras cada una, leyendo los números de la pantalla (en palabras). `make_video.py` corta si pasa de 300 s.

## Campaña de comentarios y suscripción (8 al 22 de noviembre de 2026)
Pedida por Daniel el 8-nov-2026. Mientras dure (fecha de Doha, `comun.cta_activa()`), el cierre del video y del Short pide en pantalla y en la voz
un comentario para mejorar el canal y la suscripción (`CTA_PANTALLA`, `CTA_SHORT`, `CTA_VOZ` en `comun.py`), y `gen_meta.py` pone `CTA_DESC` al comienzo
de las descripciones de YouTube. No hay que tocar `video.json` ni `short.json`. Se apaga sola el 23-nov; `CTA=0` / `CTA=1` la fuerzan.
Suma unos 8 s al video y unos 5 s al Short: si el Short pasa de 59 s, acorta su locución.

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
3. Copia `ejemplo-2026-11-10/` a la carpeta del día y cambia `video.json` (textos de pantalla y locución, números en palabras), `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena).
4. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 300 s).
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
