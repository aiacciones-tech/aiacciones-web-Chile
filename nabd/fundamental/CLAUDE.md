# Serie semanal «التحليل الأساسي ببساطة» (análisis fundamental, fácil) de Nabd Wall Street: instrucciones (Daniel, 20-nov-2026)

Vídeos educativos en árabe, **un concepto de análisis fundamental por vídeo**, explicado sobre las **cifras reales de una gran empresa de EE. UU.**
(Daniel pidió expresamente acciones de EE. UU.; el capítulo 1 es Apple). Unos 6 minutos (5:00-7:30), con subtítulos (quemados y `.srt`),
miniatura y Short. Misma voz y marca que el canal: Azure `ar-SA-HamedNeural` (voz-Nabd.yml, Piper de respaldo), colores y logo de `nabd/diario/comun.py`.
**Un capítulo cada sábado**, publicado hacia las 15:00-16:00 UTC (18:00-19:00 Riad): no choca con el diario (L-V 21:47 UTC), y la serie 20
(12:23 y 22:53 UTC) casi nunca tiene resultados en sábado. Daniel pidió que todo sea automático: los capítulos se publican solos, sin revisión previa.
Instrucciones en español; lo que ve y oye el público, en árabe. Todo lo que se entrega termina en `-Nabd`.

Plan de 10 temas en `plan.json` (empresa sugerida, se puede cambiar si otra enseña mejor el concepto o tiene resultados más recientes; siempre de EE. UU.):
1 ingresos y beneficio neto (Apple) · 2 márgenes (NVIDIA) · 3 PER (Microsoft) · 4 deuda (Oracle) · 5 flujo de caja libre (Amazon) ·
6 dividendos (Johnson & Johnson) · 7 ROE (JPMorgan) · 8 balance (Berkshire Hathaway) · 9 valoración P/V, P/VC y EV/EBITDA (Alphabet) · 10 todo junto (Meta).
**La serie termina en el capítulo 10** (Daniel, 20-nov-2026): el capítulo 10 se presenta como cierre de la serie (en la locución y la tarjeta final:
«الحلقة الأخيرة», sin «الحلقة القادمة»; en su lugar un repaso de los 10 conceptos) y no se inventan capítulos nuevos sin que Daniel lo pida.

## Reglas de contenido
- Educación, nunca recomendación: nada de comprar/vender, precio objetivo, «barata/cara» ni «oportunidad». La empresa es «مجرد مثال للشرح».
  `make_capitulo.py` para si la locución lleva palabras de recomendación. Las ratios no son juicio de halal/haram.
- **Toda cifra sale de un informe oficial** (nota de prensa de resultados de la empresa con sus estados financieros, 10-K/10-Q) **o de TradingView**
  (`datos.json`), y la de pantalla coincide con la de la voz. Lo de la prensa, atribuido («حسب بيان أبل»). Cálculos propios «محسوب»; porcentajes
  con las cifras completas (en `cuenta`, `v` lleva las cifras exactas en miles de millones y se muestran con 1 decimal).
- La SEC (EDGAR) bloquea las descargas automáticas: usa la web de inversores o la sala de prensa de la empresa (PDF de estados financieros).
  Pon sus URL en `documentos` y el workflow de datos deja el texto en la rama `datos-fundamental-nabd`.
- Año fiscal: di siempre de qué periodo hablas (Apple cierra en septiembre, NVIDIA en enero, Microsoft en junio…).
- Bidi: en texto árabe, porcentajes con «بالمئة»; las líneas de `fuente` empiezan por una palabra árabe; sin comillas «» en pantalla salvo nombres.

## Piezas
- `capitulos/<base>/video.json`: base, capitulo_n, simbolo (p. ej. NASDAQ:AAPL), simbolos_extra, documentos [{id, url}], ticker, nombre, tema,
  publicar (fecha), fuente_general, escenas, info (titulo ≤100, titulo_short, resumen, fuentes, x, hashtags, hashtags_short, tags,
  linkedin {datos 3-4, conclusion}), miniatura (etiqueta, titulo, sub, cifras, pie). Ejemplo: `capitulos/fundamental-01-aapl/`.
  Escenas (`tipo`): `portada`, `puntos` (≤5 [título, texto]), `cuenta` (columnas, filas [{t, v, tipo ingreso|resta|sub|final|nota, d}], variación calculada),
  `cascada` (pasos [{t, v, tipo total|resta|suma}], de derecha a izquierda), `barras` (categorias, series), `kpis` (≤4 {big, label, sub, color}),
  `formula` (formula, ejemplo [[texto, resultado]], nota ≤110 caracteres), `fin` (claves ≤4, siguiente). `capitulo` = capítulo de YouTube y tramo de la barra.
- `.github/workflows/datos-fundamental-Nabd.yml`: al subir `video.json` a una rama `claude/**` pide a TradingView las cifras (`datos_fundamental.py`,
  ~3 min, se congelan; series anuales `_fy_h`) y descarga los `documentos` (`docs_fundamental.py`) a `<base>/` de la rama `datos-fundamental-nabd`.
- Voz: `voz-Nabd.yml` (workflow_dispatch, modo=generar, fecha=`nabd/fundamental/capitulos/<base>`, avatar=no) → `<base>/` de la rama `voz-nabd`
  (`nabd/diario/voz_frases.py` lee las `escenas`). Esa rama la reescribe cada ejecución (también el diario desde las 21:47 UTC y la serie 20):
  si al clonarla falta tu carpeta, vuelve a lanzarlo. Solo pide a Azure las frases nuevas.
- `make_capitulo.py <carpeta> [preview]` (con `AUD` y `VOZ_DIR`): control de calidad y duración 300-450 s; escribe `<base>-Nabd.mp4`,
  `subtitulos-<base>-Nabd.srt`, times.json y `guion-<base>-Nabd.md`.
- `../diario/make_short.py <carpeta>/short.json`: el Short (<59 s, voz Piper como el Short diario; escenas titulo, kpis, cifra, fin; `aviso_fin`).
- `meta_capitulo.py <carpeta>`: meta de YouTube (vídeo y Short), posts de X, LinkedIn (Short nativo), TikTok, Instagram y Telegram, miniatura.
- `encolar.sh <carpeta>`: `cola-nabd/<base>/` y `<base>-short/` en `youtube-cola`; youtube-Nabd.yml, telegram-Nabd.yml y buffer-Nabd.yml publican solos.

## Pasos de cada sábado (rutina semanal)
0. Si el capítulo que toca ya está hecho (`/mnt/project-files/nabd-fundamental/<base>/` con el mp4 y su `video.json`) y no está en `cola-nabd/`,
   solo encólalo: `SCRATCH=<scratch> bash nabd/fundamental/encolar.sh /mnt/project-files/nabd-fundamental/<base>` y salta al paso 7
   (así salió el capítulo 1, Apple, hecho el 20-nov y publicado el sábado 21-nov).
1. Siguiente capítulo de `plan.json` que no esté en `cola-nabd/` (clon sparse de `youtube-cola`, como en nabd/serie20/CLAUDE.md). Busca (WebSearch y el
   agente web-fetch) la última nota de resultados anuales/trimestrales de la empresa y su PDF de estados financieros en su web de inversores.
2. Crea `capitulos/<base>/video.json` con simbolo, documentos y `"escenas": []`; súbelo a una rama `claude/nabd-fundamental-<fecha>` (desde main) y espera
   el workflow de datos; clona `datos-fundamental-nabd` y lee `datos.json` y `docs/*.txt`.
3. Guion: **~620-650 palabras ≈ 6 min** con Azure (calibrado en el capítulo 1: ver su `times.json`). Repite en una frase el concepto del capítulo anterior
   y anuncia el siguiente. Números en palabras en la voz; en pantalla, dígitos occidentales. Short (`short.json`, voz muy corta).
4. `AUD=<scratch> python3 make_capitulo.py <carpeta> preview` y mira TODOS los PNG (nada cortado ni solapado); sube `video.json`, lanza `voz-Nabd.yml`
   y clona `voz-nabd`; render con `VOZ_DIR=<clon>/<base>` (si la voz falla, Piper y dilo); Short (preview y render); `meta_capitulo.py`.
5. Copia mp4, Short, miniatura, srt, guion, meta y posts a `/mnt/project-files/nabd-fundamental/<base>/`.
6. `SCRATCH=<scratch> bash encolar.sh <carpeta>`; commit de los json del capítulo (sin mp4/png/srt) en la rama, PR y **fusiónalo tú** (regla de Daniel).
7. **Aviso de cada vídeo (Daniel, 20-nov-2026):** termina siempre con un mensaje en el hilo, en español, con el enlace del vídeo de YouTube
   (y del Short) en cuanto `encolar.sh` devuelva el `resultado.json`, más duración, voz y cualquier fallo. Si la subida falla, avísalo igual.
   **Capítulo 10 (el último):** el aviso empieza destacado como cierre, p. ej. «🎓 Fin de la serie «التحليل الأساسي ببساطة»: publicado el capítulo 10 de 10»,
   con el enlace del capítulo 10 y la lista de los 10 capítulos con sus enlaces (de `cola-nabd/fundamental-*/resultado.json`). Después borra esta
   tarea programada (`delete_trigger` trig_01YTsf3RwSKpgJPb4sQMWk7v) y dilo en el aviso. Si una ejecución no encuentra capítulo pendiente,
   no publica nada y responde en una línea que la serie ya terminó.
