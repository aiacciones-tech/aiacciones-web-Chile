# Crecimiento del canal de YouTube @AIAccionesEspaña

Pedido de Daniel (24-nov-2026): recomendaciones 1 a 7 para hacer crecer el canal. Este archivo dice qué hace cada rutina
sola y qué queda a mano. Vale para el vídeo diario (`espana/diario/`), la serie educativa (`espana/educativo/`), los vídeos
de resultados (`/mnt/project-files/espana/pipeline/`) y el calendario semanal (`espana/semanal/`).

## 1. Títulos y miniaturas con la cifra clave, y prueba A/B
- **Título:** la cifra clave en los primeros 45 caracteres (diario: la variación del IBEX; resultados: el dato del trimestre,
  p. ej. «Iberdrola gana 4.512 M€ (+8%)…»). `diario/gen_meta.py` lo comprueba.
- **Miniatura A** (la de siempre, con la fecha) y **miniatura B** «gancho» (2-4 palabras del día y la cifra enorme):
  `gen_meta.py` hace las dos y `ab.json` con el **título B** (`info.titulo_b`, o uno automático con el gancho).
  El gancho sale de `info.miniatura.gancho` (2-4 palabras, p. ej. «La banca tira»).
- **Serie educativa:** solo título B (`info.titulo_b` en `video.json`), sin miniatura B por ahora.
- **Resultados:** si la sesión deja `ab-<PER>.json` y `miniatura-youtube-b.png` en la carpeta de la empresa, `pipeline/encolar.sh` los encola.
- **Rotación:** `.github/workflows/ab-espana.yml` (08:14 UTC) usa `scripts/ab-saudi.py` (el mismo de Arabia Saudita, sirve para
  cualquier cola): día 0 = A, días 1-4 alternando A y B, el día 5 deja la que tiene más vistas; con el token de Analytics, desde el
  día 8 manda el CTR. Estado en `cola-es/<slug>/ab-estado.json` (rama `youtube-cola`); tabla: *Actions > Pruebas A/B (España) > Run workflow*.
  Con pocas vistas por vídeo, lo que cuenta es el acumulado de muchas pruebas.
- **«Probar y comparar» de YouTube Studio** (reparte impresiones a la vez y es más fiable) no está en la API. A mano: Studio > vídeo >
  Detalles > Miniatura > *Probar y comparar*, sube `miniatura.png` y `miniatura-b.png` (en `cola-es/<slug>/`), y pon `"pausado": true`
  en su `ab-estado.json` (o pídeselo a Claude) para que la rotación no la pise.

## 2. La conclusión en los primeros 15 segundos
- **Diario:** la locución de `s_title` dice qué pasó, por qué (la causa principal) y el dato técnico clave, en **≤45 palabras** y sin
  «veamos por qué». `make_video.py` (también al pedir la voz con `voz.sh`) se para si no se cumple. Ejemplo en `diario/ejemplo-2026-11-09/`.
- **Short:** la primera escena da ya la conclusión (cifra + causa), no solo el titular.
- **Serie educativa:** la portada responde a la pregunta del capítulo en la primera frase («La media de 200 sesiones separa…»), y luego explica.
- **Resultados:** la escena 1 dice el dato y si mejoró o empeoró frente al año anterior, antes de entrar en detalle.

## 3. Varios Shorts por vídeo largo (máx. ~10 subidas en 24 h)
- **Diario:** además de `short.json`, un **segundo Short** `short2.json` con otro ángulo (el gráfico del IBEX, o el valor del día).
  `voz.sh` genera su voz, `make_short.py <dir>/short2.json` lo renderiza, `gen_meta.py` hace `meta-short2.json` (`info.titulo_short2`,
  opcional `info.resumen_short2`) y `encolar.sh` lo deja en `cola-es-programado/`: `canal-espana.yml` lo sube **a las 08:30 de Madrid del
  día siguiente**, solo a YouTube. Con esto el diario son 3 subidas al día (vídeo + 2 Shorts); domingo: lección + Short + calendario.
- Antes de cada subida se cuentan las de las últimas 24 h (`encolar.sh` y `canal-espana.py`): con 9 o más, se espera.

## 4. Vídeos fijos para búsquedas habituales
Propuesta en el hilo «Hacer crecer el canal de YouTube» (Daniel elige). Nunca «comprar/vender»: los títulos responden a lo que la gente
busca («¿Qué es…?», «calendario», «cómo funciona») con datos.

## 5. Listas de reproducción
`scripts/canal-espana.py listas` (dentro de `canal-espana.yml`, a diario): «IBEX 35 hoy», «La bolsa española en 1 minuto (Shorts)»,
«Análisis técnico, explicado fácil», «Calendario semanal de resultados», «Resultados 3T 2026 / 1S 2026 del IBEX 35» y una por empresa.
Cada vídeo nuevo entra solo, el más nuevo arriba. Estado en `cola-es/listas.json`. Tope de 40 operaciones al día por la cuota de la API.
**Necesita un token con permiso `youtube`** (ver abajo); si el actual solo tiene `youtube.upload`, el workflow lo avisa y no hace nada.

## 6. Pantallas finales y tarjetas
La API no las permite. Lo automático:
- Descripciones con enlaces al vídeo anterior y a las listas: `{ultimo:bolsa-}`, `{ultimo:curso-at-}`, `{lista:diario}`, `{lista:curso}`,
  `{lista:shorts}`, `{lista:empresa-<id>}`, `{lista:resultados-<PER>}`. Los resuelve `espana/enlaces_cola.py` al encolar; si aún no
  existe el destino, la línea se borra.
- La última escena del diario dura al menos 20 s (hueco para la pantalla final; no cuenta en el límite de 5 min).
A mano (Daniel, 1 minuto por vídeo; lo mejor: solo en los vídeos que más vistas traen):
1. YouTube Studio > Contenido > el vídeo > Editor > **Pantalla final** > *Importar desde vídeo* (elige uno que ya la tenga) o
   *Plantilla* «1 vídeo, 1 suscribir». Elemento vídeo: «El más reciente» (se actualiza solo) o «Mejor para el espectador».
2. **Tarjetas:** Editor > Tarjetas > Lista de reproducción «IBEX 35 hoy» hacia el minuto 1 y, en los de resultados, la lista de la empresa.
3. Guardar. Basta con hacerlo en un vídeo nuevo al día; los antiguos con más vistas, una vez.

## 7. Directo semanal
Formato y horario en el hilo; los directos dependen de que YouTube active la función (Daniel la pidió el 24-nov-2026; suele tardar 24 h).

## Token de YouTube con permisos completos (para listas y títulos A/B)
El secreto `YT_ES_REFRESH_TOKEN` puede tener solo permiso de subida. Para listas y para cambiar títulos hace falta `youtube`, y para
medir el CTR `yt-analytics.readonly`. Para crear uno con los dos (10 minutos, con la cuenta del canal @AIAccionesEspaña):
1. https://developers.google.com/oauthplayground > engranaje > *Use your own OAuth credentials* > el Client ID y Client Secret del cliente
   de Google Cloud que usa España (`YT_ES_CLIENT_ID`/`_SECRET`, o los de Chile si no hay).
2. Paso 1: escribe `https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/yt-analytics.readonly` > *Authorize APIs* >
   entra con la cuenta del canal de España. Paso 2: *Exchange authorization code for tokens* y copia el **Refresh token**.
3. GitHub > Settings > Secrets and variables > Actions: reemplaza `YT_ES_REFRESH_TOKEN` con ese valor (sigue sirviendo para subir) y crea
   `YT_ES_STATS_REFRESH_TOKEN` con el mismo valor.
Si sale `redirect_uri_mismatch`, añade `https://developers.google.com/oauthplayground` a los URI de redirección del cliente en Google Cloud.

## Revisión semanal (recomendación 12, aún no activada)
Meta: CTR > 5 % y buena retención en los primeros 30 s. Con el token de Analytics se puede automatizar como en Arabia Saudita.

## Vídeos fijos (4) y directo semanal (7): cómo se hacen (24-nov-2026)
- **Vídeos fijos** (`espana/fijos/<base>/video.json`, `"formato": "fijo"`): las mismas herramientas de la serie educativa
  (`make_leccion.py`, `make_short_leccion.py`, con escenas nuevas `cifras`, `tabla` y `barras`), después `espana/fijos/meta_fijo.py <carpeta>`
  y `SCRATCH=… bash espana/fijos/encolar_fijo.sh <carpeta>` (cola `cola-es/fijo-<base>`; lista «Guías de la bolsa española»).
  Toda cifra con fuente en pantalla; los cálculos propios, «calculado». Ejemplo: `espana/fijos/inditex-resultados-9m-2026/`.
- **Directo de los viernes 17:45** («El IBEX de la semana, en directo»): lo emite Daniel; diapositivas y guion con `espana/directo/`
  (instrucciones en `espana/directo/CLAUDE.md`).
