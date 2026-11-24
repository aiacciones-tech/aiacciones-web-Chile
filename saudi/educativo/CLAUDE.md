# Serie educativa semanal «التحليل الفني ببساطة» de Saudi Arabia AI Stocks: instrucciones (Daniel, 18-nov-2026)

Vídeos educativos de análisis técnico en árabe, **un concepto por vídeo**, explicado sobre el **gráfico real** de una acción de Tadawul
(datos de TradingView), con la voz y la marca del canal. ~6 minutos, subtítulos, miniatura y un Short. **Un vídeo cada sábado** (Tadawul cerrado,
sin vídeo diario ni informe de estadísticas). Plan de 10 temas en `plan-saudi.json` (marca cada lección publicada). Modelo: la serie alemana
`ge/educativo/` (PR #184). Valen las reglas del canal: archivos entregados en inglés y terminados en `-saudi`; contenido en árabe;
cada post enlaza https://www.youtube.com/@SaudiArabiaAIStocks; LinkedIn lleva el Short como vídeo nativo con 3-4 datos + conclusión y
«فيديو من إعداد قناة Saudi Arabia AI Stocks»; campaña de comentarios (`saudi/diario/campana.py`) se añade sola mientras esté activa.

## Reglas de contenido
- Educación, no previsión: zonas y patrones del pasado; la situación actual va como **condiciones** («إذا أغلق السعر فوق… فهذا يعني…»),
  nunca como previsión, precio objetivo ni recomendación. La acción es «مجرد مثال». Sin «رخيص/مرتفع الثمن». `make_leccion.py` rechaza algunas palabras.
- Toda cifra dicha sale de `velas.json` (TradingView; Yahoo solo si TradingView falla, y entonces la fuente en pantalla lo dice) y coincide con la pantalla.
  Las zonas son «محسوبة/مرسومة من القناة». No se explican las causas de un movimiento salvo con fuente publicada y atribuida.
- En la locución, las cifras van en palabras (como el diario: «اثنين وسبعين فاصل أربعة») y los nombres latinos en letras árabes
  («ساودي أرابيا إيه آي ستوكس», «تريدينغ فيو»); `comun_leccion.LATINO` los devuelve a su forma latina en los subtítulos.
- `ultima_vela`: la última sesión **cerrada** (el jueves anterior al sábado de publicación).

## Piezas (saudi/educativo/)
- `lecciones/<base>/video.json`: base (`ta-NN-<accion>`), folge, simbolo (`TADAWUL:<código>`), ticker, nombre, tema, ultima_vela, escenas, short, info, miniatura.
  Escenas (`tipo`): `portada`, `esquema` (modo sr / rollentausch / rollentausch_baja / fehlausbruch), `puntos` (≤5 [título, texto]),
  `grafico` (desde, hasta, zonas [{de, a, texto, color}], marcas [{fecha, tipo techo|suelo, texto}], nota, volumen, animar_velas), `fin` (claves ≤4, siguiente).
  `capitulo` = capítulo de YouTube. Para un tema que necesite otro dibujo (medias, RSI, MACD, Bollinger…) añade una opción a `s_grafico`
  (p. ej. `lineas` calculadas de las velas) o un tipo nuevo en `make_leccion.py`, y su equivalente en `make_short_leccion.py`.
  `short`: 4 escenas (titulo, grafico con `grafico: <id de escena larga>`, grafico, fin), < 59 s (~90 palabras).
  `info`: titulo, titulo_short, resumen, fuentes, hashtags, hashtags_short, tags, x, tiktok, linkedin {datos (3-4), conclusion}.
- `.github/workflows/educativo-saudi.yml`: al subir `video.json` a una rama `claude/**`, pide las velas (solo la primera vez; con
  `REFRESCAR` no aplica en el workflow) y genera la voz Azure ar-SA-HamedNeural (+8 %, clave del diario) frase a frase en `<base>/` de la rama
  `voz-saudi-educativo`. Solo pide a Azure las frases nuevas (cuota gratuita compartida con Nabd: ~4.500 caracteres por lección).
- `niveles.py <velas.json> [ventana] [tolerancia %] [sesiones]`: pivotes y zonas candidatas, para escribir el guion.
- `make_leccion.py <carpeta> [preview]` y `make_short_leccion.py <carpeta> [preview]` (con `AUD`, `VELAS`, `VOZ_DIR`): vídeo 5-7,5 min y Short.
- `meta_leccion.py <carpeta>` (con `VELAS`): metadatos de YouTube y del Short, posts de las 7 redes y miniatura.
- `encolar.sh <carpeta>`: `cola-sa/lesson-<base>/` y `-short/` en `youtube-cola`; desde ahí todo se publica solo.

## Pasos de cada sábado (tarea programada)
1. Mira `plan-saudi.json`: la primera lección `pendiente` (o `lista`, que solo falta publicar). Elige la acción con su gráfico de 2 años
   (TradingView funciona desde el contenedor: `datos_leccion.py` con la carpeta de salida en el scratch).
2. Escribe `lecciones/<base>/video.json` (~640-680 palabras ≈ 6 min con Azure; el Short ~90). Preview: `AUD=<scratch> VELAS=<velas.json>
   python3 make_leccion.py <carpeta> preview` y `make_short_leccion.py … preview`; mira TODOS los PNG.
3. Commit y push a `claude/saudi-educativo-<fecha>` → `educativo-saudi.yml` (2-4 min). `git clone -q --depth 1 -b voz-saudi-educativo <repo> <scratch>/voz`.
4. Render con `VOZ_DIR=<scratch>/voz/<base>` y `VELAS=<scratch>/voz/<base>/velas.json` (la línea `voz azure` lo confirma); `meta_leccion.py`.
   Si Azure falla, Piper (`pip install piper-tts`) y dilo en el resumen.
5. `SCRATCH=<scratch> bash encolar.sh <carpeta>`; copia mp4, Short, miniatura, metadatos, guion y posts a `/mnt/project-files/saudi-educativo/<base>/`.
6. Actualiza `plan-saudi.json` (estado `publicada`, IDs) y abre o actualiza el PR de la rama para que quede en main.

## Prueba A/B de miniatura (y título) (desde el 24-nov-2026, pedido de Daniel)
`meta_leccion.py` hace también una miniatura B estilo «pregunta» (`thumbnail-b-<base>-saudi.png`: pregunta grande sobre el gráfico a pantalla completa)
y `ab-<base>-saudi.json`; `encolar.sh` los copia a la cola y `scripts/ab-saudi.py` (workflow `ab-saudi.yml`) alterna A y B por días y deja la ganadora.
En `video.json` escribe `miniatura.gancho` (la pregunta, p. ej. «كيف تجد الدعم والمقاومة؟»; si falta: «كيف تقرأ <titulo>؟») y
`info.titulo_b` (≤100 caracteres, estilo pregunta, p. ej. «كيف تحدد الدعم والمقاومة؟ شرح عملي على سهم الراجحي»). Sin `titulo_b` solo se prueba la miniatura.
Mira la miniatura B antes de encolar.
