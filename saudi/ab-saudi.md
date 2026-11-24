# Pruebas A/B de miniaturas y títulos · Saudi Arabia AI Stocks

Pedido de Daniel (24-nov-2026). Objetivo: subir el CTR (porcentaje de gente que hace clic al ver la miniatura) de los videos largos.

## Por qué no se usa "Test & Compare" de YouTube

La función "Probar y comparar" de YouTube Studio reparte las impresiones entre 2 o 3 miniaturas (y ya también títulos) al mismo tiempo,
que es lo ideal, pero **no está en la API**: solo se puede usar a mano en YouTube Studio. Por eso la prueba automática se hace **por turnos**.

## Cómo funciona la prueba automática

1. **Dos variantes por video largo.** La A es la de siempre. La B la generan los mismos scripts:
   - Vídeo diario (`saudi/diario/gen_meta.py`): A = estilo «fecha» (la fecha en grande, TASI y Nomu); B = estilo «gancho»
     (el titular del día en grande y la variación de TASI enorme), con título B que empieza por el titular y deja la fecha al final.
   - Serie educativa (`saudi/educativo/meta_leccion.py`): A = estilo «serie» (franja de la serie, tema y gráfico); B = estilo «pregunta»
     (una pregunta grande sobre el gráfico a pantalla completa) y título B si la sesión lo escribe (`info.titulo_b`).
   - Los Shorts no entran: la API no deja ponerles miniatura propia.
2. **Rotación por días** (`scripts/ab-saudi.py`, workflow `ab-saudi.yml`, cada día a las 08:10 UTC = medianoche del Pacífico, que es
   como YouTube cuenta los días). Día 0 (el de la subida, incompleto): A. Días 1 a 4: A-B-A-B o B-A-B-A, alternando el orden entre videos
   para que la caída natural de vistas no favorezca siempre a la misma variante.
3. **Medición.** Cada medianoche se guarda el contador de vistas del video, así se sabe cuántas vistas tuvo cada día con cada variante.
   Si existe el secreto `YT_SAUDI_STATS_REFRESH_TOKEN` (con permiso `yt-analytics.readonly`), desde el día 8 se piden además las
   **impresiones y el CTR de la miniatura** por día, que es la métrica buena; si los hay, mandan sobre las vistas.
4. **Ganadora.** El día 5 se deja puesta la variante con más vistas (empate: la A); si luego llega el CTR y gana la otra, se cambia.
5. **Resultados.** Cada prueba queda en `cola-sa/<slug>/ab-estado.json` (rama `youtube-cola`). La tabla completa:
   *Actions > Pruebas A/B de miniaturas y títulos (Arabia Saudita) > Run workflow* (modo `resumen`). El informe semanal de los viernes
   también la incluye.

**Importante:** con las vistas actuales de los videos largos (10-20 por video), una prueba sola no es concluyente.
Lo que vale es el acumulado: después de 15-20 pruebas se ve qué estilo gana de forma consistente, y ese pasa a ser la A.

## Para medir el CTR (recomendado, 10 minutos)

Crear el token de YouTube Analytics siguiendo `stats-report-saudi/youtube-analytics-setup-saudi.md` (archivos del proyecto):
secreto `YT_SAUDI_STATS_REFRESH_TOKEN`. Lo usan el informe semanal y estas pruebas. Sin él, todo funciona igual pero se compara con vistas.

## Si quieres usar "Test & Compare" a mano en un video

1. En YouTube Studio > el video > Detalles > Miniatura > *Probar y comparar*. Sube `miniatura.png` y `miniatura-b.png`
   (están en la carpeta del video en `cola-sa/` de la rama `youtube-cola`, y en `daily-video-SA/<fecha>/` de los archivos del proyecto).
2. **Pausa la prueba automática de ese video**, o las dos se pisan: en `cola-sa/<slug>/ab-estado.json` pon `"pausado": true`
   (o pídeselo a Claude).

## Formato de ab.json (en la carpeta del video en cola-sa/)

```json
{"que": "ambos",
 "B": {"title": "título B", "miniatura": "miniatura-b.png"},
 "estilos": {"A": "fecha", "B": "gancho"}}
```
`que`: `ambos`, `miniatura` o `titulo`. Cualquier video de `cola-sa/` con este archivo entra en prueba (por ejemplo, los videos de
resultados de FY26 si su pipeline lo añade).
