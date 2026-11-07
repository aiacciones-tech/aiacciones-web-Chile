# Vídeo diario en árabe de la Bolsa de Baréin (Bahrain All Share Index)

Cada sesión de Bahrain Bourse (domingo a jueves, 09:30-13:00 en Manama, UTC+3; sin vídeo en festivos como el Eid o el Día Nacional):
un vídeo de máximo 3 minutos y su Short para @BahrainAIStocks, todo en árabe (voz, textos en pantalla, título, descripción y posts),
con posts en X, Threads, Facebook, TikTok, Instagram y Telegram. Adaptado del diario saudí (`saudi/diario/`) y del de EAU (`eau/diario/`).
Muestra: sesión del jueves 5-nov-2026 (`sample-2026-11-05-bahrain/`). Regla de Daniel: nombres de archivos y carpetas en inglés con sufijo `-bahrain`.

## Guion (7 escenas, `make-video-bahrain.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE (franja roja), cierre del índice, variación en % y en puntos, curva intradía (minuto a minuto), suben/bajan y valor negociado.
2. **Noticias** (`s_news`): 3-4 noticias con fuente en pantalla (disclosures en Bahrain Bourse, resultados, dividendos, CBB, Mumtalakat, petróleo, Golfo).
3. **Análisis fundamental** (`s_fact`): barras de bolsas del Golfo y Asia (mismo día) y de Wall Street y Europa (víspera) + 2-4 factores (Brent, Fed y CBB por el ancla del dinar, flujos extranjeros si hay datos).
4. **Valores** (`s_movers`): hasta 5 que más suben y 5 que más bajan (solo los que negociaron ese día más de 1.000 dinares), con su motivo. Sin motivo publicado: «لا يوجد خبر محدد في الصحافة»; nunca se inventa. Bahrain Bourse es poco líquida: si solo se mueven 2 o 3, se dice en pantalla y no se rellena.
5. **Técnico** (`s_tech`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias, RSI 14, estocástico (14,3,3) y volumen frente a su media de 10 sesiones. «هذه بيانات وليست إشارات شراء أو بيع».
6. **Agenda** (`s_agenda`): resultados, juntas, dividendos, salidas a bolsa y datos de los próximos días.
7. **Cierre** (`s_fin`): resumen, enlace al canal y aviso legal completo en árabe (también en la descripción).

## Datos
`market-data-bahrain.py` corre en GitHub Actions (`daily-data-bahrain.yml`) y deja `data/market-<fecha>-bahrain.json` en la rama `daily-data-bahrain`
(desde el contenedor de Claude Mubasher, CNBC y TradingView están bloqueados).
- Índice: velas diarias desde 2006 e intradía de 1 minuto del Bahrain All Share Index (BHBX) de los CSV públicos de Mubasher; CNBC (`.BAX`) como respaldo.
  Los gráficos de TradingView para Baréin son de pago («permission denied, group bahrain_dly»), por eso de TradingView solo se usa el escáner.
- Valores: lista de Mubasher (`api/1/stocks/prices/all?country=bh`) unida a la del escáner de TradingView; por cada ticker gana el último día negociado,
  porque las dos fuentes se retrasan con algunos valores. Valores cotizados en dólares (GFH, ABC...) se pasan a dinares al tipo fijo 0,376.
- Contexto: Golfo (Tadawul, ADX, DFM, Qatar, Kuwait), Asia, Wall Street, Europa, Brent, oro y bono de EE. UU. a 10 años (TradingView).
`python3 technical-bahrain.py <market.json>` imprime cierre, medias, RSI, estocástico, niveles, volumen, suben/bajan, los más activos y el contexto.
Ojo: el mínimo diario de Mubasher puede traer un precio que no aparece en el intradía (el 5-nov, 1.806,04): no se usa para decir «mínimo del año» sin comprobarlo.

## Pasos de cada día
1. Datos de la rama `daily-data-bahrain`. En festivos no se guarda nada porque la última vela no es de hoy: ese día no hay vídeo.
2. Noticias y motivos: comunicados en bahrainbourse.com y en Mubasher (`english.mubasher.info/markets/BB/`), BNA, Daily Tribune (newsofbahrain.com), GDN,
   Al Bilad, Al Ayam, Al Watan, TradeArabia, Zawya, Argaam, Asharq Business, Banker. Solo cuenta como motivo lo publicado ese día o la víspera tras el cierre.
3. Copia `sample-2026-11-05-bahrain/` a la carpeta del día (sin mp4/png/txt) con `market-bahrain.json` del día y cambia `video-bahrain.json`
   (textos y locución, números en palabras), `info-bahrain.json` (título, descripción, posts, miniatura) y `short-bahrain.json` (menos de 59 s; fecha en la primera escena).
4. `AUD=<scratch> python3 make-video-bahrain.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 180 s; unas 230 palabras de locución).
5. `AUD=<scratch> python3 make-short-bahrain.py <dir>/short-bahrain.json` y `python3 make-meta-bahrain.py <dir>`.
6. `SCRATCH=<scratch> bash enqueue-daily-bahrain.sh <dir>`: comprueba archivos y enlace del canal, el límite de YouTube (~10 subidas/24 h, compartido con
   los vídeos de resultados) y encola en `cola-bahrain/daily-<fecha>` y `cola-bahrain/daily-<fecha>-short` de `youtube-cola`.

## Árabe
- Fuente: Noto Naskh Arabic (`fonts/`, OFL). `ar()` une las letras con arabic-reshaper; matplotlib 3.11+ ordena de derecha a izquierda (libraqm).
- Voz: Piper `ar_JO-kareem-medium` (`/mnt/project-files/bahrain-pipeline/voice/`); piper-tts 1.8+ pone el tashkeel. `LENGTH_SCALE=0.8`.
- Cifras en pantalla con dígitos occidentales; en la voz, en palabras.
- Marca: rojo de Baréin #C2152F y blanco (franja de la fecha en rojo), rosa claro para acentos, verde/coral para subidas/bajadas; logo `kits/avatar-bahrain.png` recortado en círculo.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi websocket-client`.

## Reglas
Nada de comprar/vender, precio objetivo ni «barata/cara». El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados «محسوب».
Todos los posts y descripciones llevan el enlace https://www.youtube.com/@BahrainAIStocks. No se programa el cron de datos ni se publica nada sin el visto bueno de Daniel.
