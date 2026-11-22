# «تقويم النتائج الأسبوعي» (calendario semanal de resultados) de @AIStocksUAE

Formato pedido por Daniel el 22-nov-2026: un Short vertical 9:16 de 45 a 60 s, todo en árabe, cada **domingo entre las 18:00 y las 20:00
de Dubái** (las bolsas de EAU abren el lunes). Cuenta las 5-7 empresas más relevantes que reportan de lunes a viernes: primero las de
ADX y DFM y después las grandes de EE. UU. que más mueven el mercado, en orden cronológico.

## Guion (`<fecha del domingo>/short.json`, escenas de `make_short.py`)
1. `gancho` (~3-4 s): «هذا الأسبوع تعلن [la empresa más importante] نتائجها، ومعها [N] شركات…».
2. `local`: ADX y DFM. Si no hay resultados de empresas grandes (fuera de temporada), se dice y se añade algún hecho verificado de la semana
   (dividendos, juntas) del calendario de DFM/ADX. Nunca se inventa.
3. `empresa` (una por compañía, 6-8 s): nombre y ticker, día y antes de la apertura / después del cierre (con la hora de EAU), BPA ajustado
   de consenso e ingresos de consenso. En pantalla van las dos cifras; en la voz, el BPA (y los ingresos solo de la principal) para no pasar de 60 s.
   Si falta una estimación verificada, se quita la línea; si la compañía solo da guía, se rotula «توجيه الشركة».
4. `fin`: «تابع القناة لتحليل كل تقرير», canal, aviso «محتوى إعلامي، وليس توصية استثمارية.» y, si hay empresas de EE. UU.,
   recomendación de **Nabd Wall Street** https://www.youtube.com/@NabdWallStreet (Daniel, 22-nov-2026).

Voz: ~90-95 palabras en total. Azure Hamdan a +12% lee ~1,7 palabras/s; 94 palabras ≈ 55-58 s con las pausas.

## Datos (solo verificados en la web)
- Fechas y horas: comunicado de cada empresa (IR) o calendario de Nasdaq `https://api.nasdaq.com/api/calendar/earnings?date=AAAA-MM-DD`
  (se lee con el navegador del ordenador de Daniel; el contenedor no llega). El BPA de Nasdaq/Zacks a veces no es el ajustado:
  usa el consenso ajustado de las previas (Earnings Whispers, Barchart, LSEG vía prensa) y cítalo en pantalla.
- ADX/DFM: calendario de acciones corporativas de DFM (`dfm.ae/the-exchange/news-disclosures/corporate-actions`) y prensa (Gulf News, Al Bayan, Argaam).

## Pasos de cada domingo
1. Copia la carpeta de la semana anterior a `eau/calendario/<fecha del domingo>/` y cambia `short.json` e `info.json`.
2. `AUD=<scratch> python3 make_short.py <dir>/short.json preview` y revisa los PNG.
3. Commit y push de `short.json` a la rama `claude/...`: `voz-eau.yml` genera la voz Azure `ar-AE-HamdanNeural` (~1 min) en `<fecha>/`
   de la rama `voz-eau`. Clave: `AZURE_SPEECH_KEY_EAU` o, si no existe, la de Nabd (plan F0 compartido; esto gasta ~700 caracteres/semana).
4. `git fetch origin voz-eau && git archive FETCH_HEAD <fecha> | tar -x -C <scratch>/voz` y
   `VOZ_DIR=<scratch>/voz/<fecha> AUD=<scratch> python3 make_short.py <dir>/short.json` (sale con error si pasa de 60 s; avisa si baja de 45).
   Si Azure falla, sin `VOZ_DIR` sale con Piper (más lenta: acorta la voz) y se dice en el hilo.
5. `python3 gen_meta.py <dir>`: meta del Short y posts de X, LinkedIn, TikTok, Instagram, Telegram y Threads, todos `-UAE`.
6. Copia los entregables a `/mnt/project-files/aistocksuae/calendario-semanal/<fecha>/` y `SCRATCH=<scratch> bash encolar.sh <dir>`.

Reglas: enlace al canal en todos los posts; LinkedIn con el Short como video nativo, 3-4 datos + conclusión, «فيديو من إعداد قناة AI Stocks UAE»
y al final el enlace al canal; nada de comprar/vender ni precio objetivo.
