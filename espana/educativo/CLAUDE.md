# Serie educativa semanal «Análisis técnico, explicado fácil» de AIAcciones España: instrucciones (Daniel, 20-nov-2026)

Vídeos educativos de análisis técnico en español de España, **un concepto por vídeo**, explicado siempre sobre el **gráfico real de Inditex**
(BME:ITX, la mayor empresa del IBEX 35 por capitalización; Daniel pidió una sola acción, «la más importante»), con datos de TradingView,
la voz del canal (es-ES-AlvaroNeural, la del vídeo diario) y su marca. ~6 minutos, subtítulos, miniatura y un Short.
**Un capítulo cada domingo**, desde el 6-dic-2026 (Daniel lo eligió para empezar al acabar la temporada de resultados del 3T26), hacia las 11:00 de Madrid.
El domingo no hay vídeo diario (lun-vie 18:05) ni rutina de resultados de mañana (lun-vie 10:55); la de las 00:00 no choca.
Plan de 10 temas en `plan-espana.json` (marca cada capítulo publicado). Modelo: la serie alemana `ge/educativo/` (PR #184) y la saudí `saudi/educativo/`.

## Reglas de contenido
- Educación, no previsión: se describe lo que hizo el precio; la situación actual va como **condiciones** («Si el precio cerrara por debajo de…,
  la lectura cambiaría»), nunca como previsión, precio objetivo ni recomendación. Inditex es «solo un ejemplo». Sin «cara/barata».
  `make_leccion.py` rechaza palabras como comprar, vender, recomendar (salvo «no es una recomendación»), precio objetivo, subirá, bajará.
- Toda cifra dicha sale de `velas.json` (TradingView; Yahoo solo si TradingView falla, y entonces la fuente en pantalla lo dice) y coincide con la
  pantalla. Medias, indicadores y zonas: «calculado». No se explican las causas de un movimiento salvo con fuente publicada y atribuida.
- En la locución las cifras van con dígitos («58,44 euros», «2025»): `voz_leccion.hablar()` las pasa a palabras para la voz y los subtítulos
  las muestran con dígitos. El femenino va en letras en el guion («doscientas sesiones», «una sesión»).
- `ultima_vela`: la última sesión **cerrada** (el viernes anterior al domingo de publicación). `publicacion`: la fecha del domingo.
- LinkedIn (regla permanente, 8-nov-2026): Short como vídeo nativo, 3-4 datos + conclusión, «Vídeo elaborado por AIAcciones España
  (@AIAccionesEspaña)» y el enlace al canal al final. La llamada a comentar solo se añade si `publicacion` ≤ 22-nov-2026 (ya no aplica).

## Piezas (espana/educativo/)
- `lecciones/<base>/video.json`: base (`at-NN-inditex`), capitulo_n, simbolo `BME:ITX`, ticker, nombre, tema, ultima_vela, publicacion, escenas, short, info, miniatura.
  Escenas (`tipo`): `portada`, `esquema` (modo media / cruces / sr / cambio_rol / cambio_rol_baja / falsa_ruptura), `puntos` (≤5 [título, texto]),
  `grafico` (desde, hasta, `lineas` [{ind: sma50|sma200|ema12…, texto, color}], `bollinger`, `panel` volumen|rsi|macd|estocastico|"",
  `volumen_media`, zonas [{de, a, texto, color}], marcas [{fecha, tipo techo|suelo|cruce, texto}], `tramo` [desde, hasta, texto], nota, ultimo),
  `fin` (claves ≤4, siguiente). `capitulo` = capítulo de YouTube. Indicadores en `comun_leccion.indicadores()` (RSI 14, MACD 12-26-9,
  Bollinger 20-2, estocástico 14-3-3, medias). Para un dibujo nuevo, añade una opción a `s_grafico` y su equivalente en `make_short_leccion.py`.
  `short`: 4 escenas (titulo, grafico con `grafico: <id de escena larga>`, grafico, fin), < 59 s (~110 palabras).
  `info`: titulo, titulo_short, resumen, fuentes, hashtags, hashtags_short, tags, x, tiktok, linkedin {datos (3-4), conclusion}, ficha (opcional).
- `.github/workflows/educativo-espana.yml`: al subir `video.json` a una rama `claude/**`, pide las velas (760 sesiones; solo la primera vez, se
  congelan; `refrescar=1` en workflow_dispatch para volver a pedirlas) y genera la voz frase a frase (edge-tts) en `<base>/` de la rama `voz-espana-educativo`.
- `niveles.py <velas.json> [ventana] [tolerancia %] [sesiones]`: pivotes y zonas candidatas, para escribir el guion.
- `make_leccion.py <carpeta> [preview]` y `make_short_leccion.py <carpeta> [preview]` (con `AUD`, `VELAS`, `VOZ_DIR`): vídeo 5-7,5 min y Short.
- `meta_leccion.py <carpeta>` (con `VELAS`): metadatos de YouTube y del Short, posts (X, LinkedIn, TikTok, Instagram, Telegram) y miniatura.
- `encolar.sh <carpeta>`: `cola-es/curso-<base>/` y `-short/` en `youtube-cola`; desde ahí YouTube, Buffer (X, LinkedIn, TikTok, Instagram) y Telegram publican solos.

## Pasos de cada domingo (tarea programada)
1. Mira `plan-espana.json`: el primer capítulo `pendiente` (o con guion de muestra). Copia la estructura de `lecciones/at-01-inditex/video.json`.
2. Escribe `lecciones/<base>/video.json` con `ultima_vela` = viernes anterior, sube a `claude/espana-educativo-<fecha>` (pide las velas, ~1 min),
   `git clone -q --depth 1 -b voz-espana-educativo <repo> <scratch>/voz`, mira los datos (indicadores y `niveles.py`) y escribe el guion:
   **~900 palabras ≈ 6 min** (calibrado en el capítulo 1); el Short ~110. Preview de los dos: mira TODOS los PNG.
3. Sube `video.json` otra vez (genera la voz, 1-3 min); `git pull` del clon; render con `VOZ_DIR=<scratch>/voz/<base>` y
   `VELAS=<scratch>/voz/<base>/velas.json` (la línea `voz neuronal` lo confirma; si sale `piper`, dilo en el resumen); `meta_leccion.py`.
4. `SCRATCH=<scratch con clon de youtube-cola> bash encolar.sh <carpeta>`; copia mp4, Short, miniatura, metadatos, guion y posts a
   `/mnt/project-files/espana/educativo/<base>/`.
5. Actualiza `plan-espana.json` (estado `publicada`, fecha, IDs) y abre un PR de la rama a main y fusiónalo si los checks pasan.
6. Si el capítulo publicado es el 10 (el último del plan), avisa a Daniel en el hilo de la serie con un mensaje: «Publicado el último capítulo de la serie» con los enlaces (lo pidió el 20-nov-2026), y no programes más capítulos sin que él lo pida.
