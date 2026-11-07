# Video diario de la Bolsa de Santiago (MSCI IPSA)

Cada día hábil, después del cierre (16:00 en Santiago): un video de máximo 3 minutos y su Short para @aiaccioneschile,
con posts en X, LinkedIn, TikTok y Telegram. Adaptado del video diario de España (`espana/diario/`).
Formato aprobado por Daniel el 7-nov-2026 (muestra: sesión del 6-nov-2026). Datos a las 20:15 UTC; la rutina diaria hace el video y lo encola.

## Guion (8 escenas, `make_video.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre, variación en % y puntos, curva intradía (5 min).
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente (hechos esenciales CMF, resultados, operaciones, macro local, Wall Street/Asia).
3. **Por qué se movió** (`s_fact`): bolsas del mundo + 4 factores (Wall Street, macro, tasas y bonos, dólar, cobre).
4. **Acciones** (`s_movers`): 5 que más suben y 5 que más bajan de las 31 del IPSA (automático) con motivo de la prensa. Sin motivo publicado: "sin noticia concreta en prensa"; nunca se inventa.
5. **Técnico 1** (`s_tech1`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias.
6. **Técnico 2** (`s_tech2`): RSI 14, estocástico (14,3,3), monto transado frente a su media. "Son datos, no señales de compra o venta".
7. **Agenda** (`s_agenda`): resultados, dividendos y macro de los próximos días (calendario de aiacciones.cl).
8. **Cierre** (`s_fin`): resumen y aviso (el aviso completo va en la descripción).

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-chile.yml`) y deja `datos/mercado-<fecha>.json` en la rama `datos-diario-cl`:
velas diarias e intradía del MSCI IPSA (TradingView `BCS:MXIPSAGC`, el que cita la prensa; Yahoo dejó de publicar ^IPSA),
cambio y volumen de las 31 acciones del IPSA (lista `IPSA`, revisar en cada rebalanceo trimestral) y contexto (Wall Street, Asia, cobre, dólar, bonos).
`python3 tecnico.py <mercado.json>` imprime cierre, medias, RSI, estocástico, niveles, monto y los 5 que más suben/bajan.

## Pasos de cada día
1. Datos de la rama `datos-diario-cl`. Si la fecha no es la de hoy, no hubo sesión (feriado): no se hace video.
2. Noticias y motivos: Diario Financiero, Diario Estrategia, La Tercera/Pulso, Emol, CNN Chile, hechos esenciales CMF (`web/assets/hechos.json`), INE/Banco Central.
   Agenda: `fuente/calendario.py` y `fuente/divs.json`.
3. Copia `ejemplo-2026-11-06/` a la carpeta del día y cambia `video.json`, `info.json` y `short.json` (menos de 59 s; fecha en la primera escena).
4. `VOICE=<es_MX-claude-high.onnx> AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 180 s).
5. `python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>` (meta de YouTube con capítulos y aviso, posts y miniatura con la fecha).
6. `bash encolar.sh <dir>`: revisa el límite de YouTube (compartido con los videos de resultados) y encola en `cola/bolsa-<fecha>` de `youtube-cola`.

Voz: Piper `es_MX-claude-high` (github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_MX-claude-high.tar.bz2), ajustes de voz fluida.
Logo: `/mnt/project-files/marca/logo-aiacciones-chile.png`. Dependencias: `pip install piper-tts matplotlib imageio-ffmpeg pillow numpy`.

## Reglas
Nada de comprar/vender, precio objetivo ni "cara/barata" (NCG 502). El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados "calculado".
Enlace a aiacciones.cl en video, Short y posts; TikTok con youtube.com/@aiaccioneschile.
