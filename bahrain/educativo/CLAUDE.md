# Serie educativa semanal «التحليل الفني ببساطة» de Bahrain AI Stocks: instrucciones (Daniel, 20-nov-2026)

Vídeos educativos de análisis técnico en árabe para @BahrainAIStocks, **un concepto por vídeo**, explicado sobre el **gráfico real** de una acción
**bahreiní** cotizada en Bahrain Bourse (Kuwait Finance House no cuenta: es kuwaití), con la voz y la marca del canal. ~6 minutos (5-7,5),
subtítulos, miniatura y un Short. **Un vídeo cada sábado** (fin de semana en Baréin: sin vídeo diario, que sale dom-jue 14:07 Manama, y sin
vídeos de resultados). Empieza el sábado **28-nov-2026**, tras la temporada de resultados 3T26 (plazo 14-nov); las 10 lecciones acaban el
30-ene-2027, antes de la temporada de resultados anuales FY26. Plan en `plan-lessons-bahrain.json`. Modelo: la serie saudí `saudi/educativo/`
(que a su vez copia la alemana `ge/educativo/`, PR #184). Al publicar la lección 10, avisa a Daniel en el hilo (lo pidió el 20-nov-2026).

Reglas del canal: nombres de archivos y carpetas en inglés terminados en `-bahrain`; todo lo que ve u oye el espectador, en árabe; cada post enlaza
https://www.youtube.com/@BahrainAIStocks; LinkedIn lleva el Short como vídeo nativo con 3-4 datos + conclusión, «🎥 فيديو من إعداد قناة أسهم
البحرين بالذكاء الاصطناعي (Bahrain AI Stocks)» y el enlace del canal en la última línea (lo hace `make-lesson-meta-bahrain.py`). YouTube usa la
miniatura automática (el canal no está verificado; no pedirlo). Facebook sigue bloqueado: el post se genera igual y Buffer lo omite.

## Reglas de contenido
- Educación, no previsión: zonas y patrones del pasado; la situación actual va como **condiciones** («إذا أغلق السعر فوق… فهذا يعني…»),
  nunca previsión, precio objetivo ni recomendación. La acción es «مجرد مثال». Sin «رخيص/مرتفع الثمن». `make-lesson-bahrain.py` rechaza algunas palabras.
- Toda cifra dicha sale de `velas-bahrain.json` y coincide con la pantalla. Las zonas son «محسوبة/مرسومة من القناة». No se explican causas sin fuente publicada.
- Precios en dinares con 3 decimales en pantalla (0.750); en la voz, en **fils** y en palabras («سبعمئة وخمسين فلسًا»). Fechas y cifras en palabras.
- `ultima_vela`: la última sesión **cerrada** (el jueves anterior al sábado de publicación).

## Datos
TradingView no da gráficos de Baréin (paquete de pago, «bahrain_dly»). `lesson-data-bahrain.py` baja el archivo público de velas diarias de
Mubasher que dibuja su web clásica (`static.mubasher.info/.../File.Historical_Stock_Charts_Dir/<id>.csv`; el id sale de
`english-old.mubasher.info/markets/BB/stocks/<TICKER>`). Mubasher está bloqueado desde el contenedor: lo corre `.github/workflows/educativo-bahrain.yml`
al subir `lessons/<carpeta>/video-bahrain.json` a una rama `claude/**`, y deja `<carpeta>/velas-bahrain.json` en la rama `datos-bahrain-educativo`
(solo la primera vez; para rehacerlas, workflow_dispatch con `refrescar=1`). Ojo: algunos archivos están parados (el de **NBB acaba el 5-ene-2026**);
el script avisa si la última vela tiene más de 10 días: entonces usa otra acción.

## Piezas (bahrain/educativo/)
- `lessons/<base>-bahrain/video-bahrain.json`: base (`ta-NN-<accion>`), folge, simbolo (`BAHRAIN:<ticker>`), ticker, nombre, nombre_corto, tema,
  ultima_vela, decimales (3), escenas, short, info, miniatura. Mismos tipos de escena que la serie saudí (ver `saudi/educativo/CLAUDE.md`):
  `portada`, `esquema` (sr / rollentausch / rollentausch_baja / fehlausbruch), `puntos`, `grafico` (desde, hasta, zonas, marcas, nota, volumen,
  animar_velas), `fin`. Para medias, RSI, MACD, Bollinger… añade una opción a `s_grafico` (líneas calculadas de las velas) y su equivalente en el Short.
  `short`: 4 escenas (titulo, grafico, grafico, fin), < 59 s. `info`: titulo, titulo_short, resumen, fuentes, hashtags, hashtags_short, tags, x, tiktok, linkedin {datos, conclusion}.
- `levels-bahrain.py <velas-bahrain.json> [ventana] [tolerancia %] [sesiones]`: pivotes y zonas candidatas, para escribir el guion.
- `make-lesson-bahrain.py <carpeta> [preview]` y `make-lesson-short-bahrain.py <carpeta> [preview]` (con `AUD`, `VELAS`): voz Piper
  ar_JO-kareem del canal (`/mnt/project-files/bahrain-pipeline/voice/`), ~560 palabras ≈ 6 min; el Short ~70 palabras ≈ 47 s.
- `make-lesson-meta-bahrain.py <carpeta>` (con `VELAS`): metadatos de YouTube y del Short, posts de las 7 redes y miniatura.
- `enqueue-lesson-bahrain.sh <carpeta>`: `cola-bahrain/lesson-<base>/` y `-short/` en `youtube-cola` (clon disperso, solo `cola-bahrain`); desde ahí todo se publica solo.
  Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi`.

## Pasos de cada sábado (tarea programada, 17:07 Manama)
1. `plan-lessons-bahrain.json`: la primera lección `pendiente` (o `lista`). Elige la acción bahreiní que mejor enseñe el concepto.
2. Escribe `lessons/<base>-bahrain/video-bahrain.json` (para la lección 1 ya existe: solo refresca las velas y rehaz la escena `ahora`, el
   `ultima_vela`, la info y el LinkedIn con el último cierre). Commit y push → `educativo-bahrain.yml` (~30 s); velas en `datos-bahrain-educativo`.
3. Preview (`... preview`), mira TODOS los PNG; luego el render final, el Short y `make-lesson-meta-bahrain.py`.
4. `SCRATCH=<scratch> bash enqueue-lesson-bahrain.sh <carpeta>`; después `rm -rf <scratch>`. Copia mp4, Short, miniatura, metadatos, guion y posts
   a `/mnt/project-files/bahrain-pipeline/lessons-bahrain/<base>/` (no subas los mp4 al repo).
5. Actualiza `plan-lessons-bahrain.json` (estado `publicada`, fecha, IDs) y abre o actualiza el PR. Si era la lección 10, avisa a Daniel.
