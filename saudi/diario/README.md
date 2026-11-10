# Video diario en árabe de la bolsa saudí (TASI y, en una frase, Nomu)

Cada día de sesión de Tadawul (domingo a jueves; cierre a las 15:00 en Riad, 12:00 UTC; sin video en festivos como el Eid o el Día Nacional):
un video de unos 5 minutos (máx. 330 s; antes 3 min, cambio pedido por Daniel el 10-nov-2026) con el análisis técnico como parte principal, y su Short para @SaudiArabiaAIStocks, todo en árabe (voz, textos en pantalla, título, descripción y posts),
con posts en X, Threads, Facebook, LinkedIn, TikTok, Instagram y Telegram. Adaptado del video diario de EAU (`eau/diario/`).
Plantilla actual: sesión del martes 10-nov-2026 (`ejemplo-2026-11-10/`, formato de 5 minutos). La primera muestra de 3 minutos sigue en `ejemplo-2026-11-05/`.

## Guion (11 escenas, `make_video.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre de TASI, variación en % y en puntos, curva intradía (5 min) y Nomu en una línea.
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente en pantalla (comunicados en Tadawul, resultados, dividendos, operaciones, CMA, SAMA, Aramco y petróleo, OPEP+, Wall Street/Asia).
3. **Análisis fundamental** (`s_fact`): barras de bolsas del Golfo y Asia (mismo día) y de Wall Street y Europa (cierre de la víspera) + 2-4 factores (Brent, Fed y SAMA, flujos extranjeros si hay datos publicados, macro).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan del mercado principal (automático; solo acciones ordinarias de TASI con más de 1 millón de riyales negociados), con su motivo. Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa.
5. **Técnico TASI, bloque de 5 escenas (unos 3 minutos, más de la mitad del video)**. Todo calculado en `tecnico.py` y presentado como datos («هذه بيانات وليست إشارات شراء أو بيع»):
   - `s_tech` (1/5): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias, RSI 14, estocástico (14,3,3) y volumen frente a su media de 10 sesiones.
   - `s_tend` (2/5): un año de cierres con medias de 20, 50 y 200; distancia a cada media, pendiente de las de 50 y 200 en 20 sesiones, último cruce 50/200 y del precio con la de 50; rentabilidad a 1 semana, 1 mes, 3 y 6 meses, 1 año y en el año.
   - `s_osc` (3/5): 3 meses de RSI 14, estocástico y MACD (12,26,9); RSI hoy, hace 5 sesiones y su rango de 3 meses, último cruce %K/%D y de MACD, histograma que se amplía o se estrecha.
   - `s_vol` (4/5): velas de 3 meses con bandas de Bollinger (20,2) y volumen con su media de 10; volumen frente a las medias de 10 y 50, ATR 14, rango del día, ancho de Bollinger (y el mínimo de 6 meses) y posición del cierre en la banda.
   - `s_niv` (5/5): mapa de niveles a ±12 % del cierre (soportes y resistencias, medias, Bollinger, pivotes clásicos P, R1 y S1 para la sesión siguiente, máximo de 52 semanas) con la distancia en %.
   Títulos de pantalla en `video.json` → `tecnico.tendencia/momento/volatilidad/niveles.titulo`; locución en `voz.s_tend/s_osc/s_vol/s_niv` (unos 30-40 s cada una).
6. **Agenda** (`s_agenda`): resultados, dividendos, salidas a bolsa y datos de los próximos días.
   **Campaña de comentarios y suscripción** (`s_cta`, del 8 al 22-nov-2026): tarjeta «رأيك يهمنا» con su locución antes del cierre, una línea más en la escena final del Short
   y el texto en la descripción y en todos los posts. Todo sale de `campana.py` y se apaga solo después de `campana.HASTA` (hora de Riad); para alargarla, cambia esa fecha.
   La tarjeta suma unos 10 s y cuenta dentro del máximo de 330 s.
7. **Cierre** (`s_fin`): resumen y aviso legal completo en árabe (también en la descripción).

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-saudi.yml`, 12:40 UTC de domingo a jueves) y deja `datos/mercado-<fecha>.json`
en la rama `datos-diario-saudi`: velas diarias e intradía de `TADAWUL:TASI` y `TADAWUL:NOMUC` (websocket de TradingView), cambio, volumen y valor negociado
de todas las acciones de Tadawul (escáner `ksa`; las de TASI se distinguen por su campo `indexes`), velas recientes del contexto (Golfo, Asia, Wall Street,
Europa, Brent, oro, bono de EE. UU. a 10 años, Aramco) y el último dato del escáner. También funciona desde el contenedor de Claude si llega a TradingView.
`python3 tecnico.py <mercado.json>` imprime cierres, variaciones, medias, RSI, estocástico, niveles, volumen, los 5 que más suben/bajan y el contexto del día.
Si el websocket de TradingView no entrega series (pasó el 10-nov-2026), `datos_mercado.py` falla a los 45 s por serie y usa Yahoo Finance;
como Yahoo solo da la vela del día para `^TASI.SR`, después corre `python3 completar_velas.py <dir>/mercado.json <dir sesión anterior>/mercado.json`,
que rehace el histórico diario con las velas de la sesión anterior y añade la de hoy. En `info.json` las `claves` llevan dos sobre el técnico
(tendencia y niveles; momento, volumen y volatilidad); `gen_meta.py` quita de Facebook la clave más larga si no cabe.
El volumen de Nomu no viene en la vela del índice: se calcula sumando sus acciones frente a su media de 10 sesiones.

## Pasos de cada día
1. Datos de la rama `datos-diario-saudi`. En festivos no se guarda `mercado-<hoy>.json` porque la última vela no es de hoy: ese día no se hace video.
2. Noticias y motivos: Mubasher (páginas de cada valor: `mubasher.info/markets/TDWL/stocks/<código>/news`), Argaam, SPA (resumen de cierre con los que más suben y bajan),
   Al Arabiya, Asharq Business, Reuters (Zawya), comunicados en saudiexchange.sa. Ojo con la fecha: solo cuenta como motivo lo publicado ese día o la víspera tras el cierre.
3. Copia `ejemplo-2026-11-10/` a la carpeta del día (sin los mp4/png) y cambia `video.json` (textos de pantalla y locución, números en palabras),
   `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena). Nombres en árabe que falten: `"nombres"` en `video.json`.
4. `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (unos 5 minutos, máx. 330 s; unas 480 palabras de locución en total, la mitad en el bloque técnico).
5. `AUD=<scratch> python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>`. Todo lo que se entrega termina en `-SA` (regla de Daniel, 7-nov-2026).
6. `SCRATCH=<scratch> bash encolar.sh <dir>`: comprueba los archivos y el enlace del canal, el límite de YouTube (~10 subidas/24 h, compartido con los videos de resultados)
   y encola en `cola-sa/bolsa-<fecha>` y `cola-sa/bolsa-<fecha>-short` de `youtube-cola`.

## LinkedIn (regla permanente de Daniel, 8-nov-2026)
En LinkedIn va el Short subido como video (no como enlace): `encolar.sh` pone `post-linkedin.txt` en `cola-sa/bolsa-<fecha>-short/`.
El texto sale de `info.json` → `linkedin`: `datos` con 3 o 4 cifras clave y qué cambió, y `conclusion` (una frase). Es un resumen con valor, sin relleno
(sin la línea de la campaña), dice «فيديو من إعداد قناة Saudi Arabia AI Stocks» y termina con el enlace al canal https://www.youtube.com/@SaudiArabiaAIStocks.
Facebook sigue con el texto largo y el enlace al video (`post-facebook.txt` en la carpeta del video largo).

## Árabe
- Fuente: Noto Naskh Arabic (`fonts/`, OFL). Texto: `comun.ar()` une las letras con arabic-reshaper; matplotlib 3.11+ ordena de derecha a izquierda (libraqm); en versiones anteriores lo hace python-bidi.
- Voz: Piper `ar_JO-kareem-medium` (`/mnt/project-files/saudi-pipeline/voice/`); piper-tts 1.8+ pone el tashkeel. `LENGTH_SCALE=0.8`.
- Cifras en pantalla con dígitos occidentales (como Argaam y la prensa financiera saudí); en la voz, en palabras.
- Marca: verde #0B6E4F y dorado #C9A227 (aclarados sobre fondo oscuro), logo `youtube-kit-saudi/profile-picture-800x800-saudi.png`.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi websocket-client`.

## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Todos los posts y descripciones llevan el enlace al canal https://www.youtube.com/@SaudiArabiaAIStocks. Cada video lleva su Short; el video va también a Facebook y el Short como Reel de Instagram.
