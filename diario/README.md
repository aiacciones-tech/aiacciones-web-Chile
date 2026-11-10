# Video diario de la Bolsa de Santiago (MSCI IPSA)

Cada día hábil, después del cierre (16:00 en Santiago): un video de unos 5 minutos (desde el 10-nov-2026, pedido de Daniel, con más análisis técnico) y su Short para @aiaccioneschile,
con posts en X, LinkedIn, TikTok y Telegram. Adaptado del video diario de España (`espana/diario/`).
Formato aprobado por Daniel el 7-nov-2026 (muestra: sesión del 6-nov-2026). Datos a las 20:15 UTC; la rutina diaria hace el video y lo encola.

## Guion (12 escenas, `make_video.py`; unos 5 minutos: 280-320 s, máx. 330)
Formato de 5 minutos con más técnico (Daniel, 10-nov-2026). El técnico ocupa cerca de 2 minutos (4 escenas).
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre, variación en % y puntos, máximo/mínimo del día, curva intradía (5 min).
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente (hechos esenciales CMF, resultados, operaciones, macro local, Wall Street/Asia).
3. **Por qué se movió** (`s_fact`): bolsas del mundo + 4 factores (Wall Street, macro, tasas y bonos, dólar, cobre).
4. **Acciones** (`s_movers`): 5 que más suben y 5 que más bajan de las 31 del IPSA (automático) con motivo de la prensa. Sin motivo publicado: "sin noticia concreta en prensa"; nunca se inventa.
5. **Sectores** (`s_sect`, video.json `sectores`): variación por sector ponderada por capitalización (automático, `tecnico.SECTORES`) + 3 notas.
6. **En perspectiva** (`s_persp`, `perspectiva`): rentabilidad del IPSA a 1 semana, 1, 3, 6 y 12 meses y en el año; distancia al máximo y mínimo de 52 semanas (automático) + nota.
7. **Técnico 1** (`s_tech1`): tendencia: velas de 6 meses, medias de 50 y 200 sesiones (y su pendiente), soportes y resistencias.
8. **Técnico 2** (`s_tech2`): impulso: RSI 14, estocástico (14,3,3), monto transado frente a su media.
9. **Técnico 3** (`s_tech3`, `tecnico.titulo3`): bandas de Bollinger (20, 2), ancho de bandas, MACD (12, 26, 9), histograma y último cruce (automático).
10. **Técnico 4** (`s_tech4`, `tecnico.titulo4`, `nota4`): amplitud: cuántas de las 31 acciones están sobre su media de 50 y de 200, y las de RSI más alto y más bajo (sobrecompra ≥ 70, sobreventa ≤ 30). Datos SMA50/SMA200/RSI de TradingView.
11. **Agenda** (`s_agenda`): resultados, dividendos y macro de los próximos días (calendario de aiacciones.cl).
12. **Cierre** (`s_fin`): resumen y aviso (el aviso completo va en la descripción).
Todo el técnico se dice como datos ("son datos, no señales de compra o venta"); cada afirmación del guion (cruces, "por primera vez desde...") se comprueba con `tecnico.py`.

## Datos
`datos_mercado.py` corre en GitHub Actions (`datos-diario-chile.yml`) y deja `datos/mercado-<fecha>.json` en la rama `datos-diario-cl`:
velas diarias e intradía del MSCI IPSA (TradingView `BCS:MXIPSAGC`, el que cita la prensa; Yahoo dejó de publicar ^IPSA),
cambio y volumen de las 31 acciones del IPSA (lista `IPSA`, revisar en cada rebalanceo trimestral) y contexto (Wall Street, Asia, cobre, dólar, bonos).
`python3 tecnico.py <mercado.json>` imprime cierre, medias, RSI, estocástico, niveles, monto y los 5 que más suben/bajan.

## Pasos de cada día
1. Datos de la rama `datos-diario-cl`. Si la fecha no es la de hoy, no hubo sesión (feriado): no se hace video. Un `mercado-<fecha>-parcial.json` es de antes del cierre: no sirve; lanza el workflow otra vez.
2. Noticias y motivos: Diario Financiero, Diario Estrategia, La Tercera/Pulso, Emol, CNN Chile, hechos esenciales CMF (`web/assets/hechos.json`), INE/Banco Central.
   Agenda: `fuente/calendario.py` y `fuente/divs.json`.
3. Copia `ejemplo-2026-11-09/` a la carpeta del día y cambia `video.json`, `info.json` y `short.json` (menos de 59 s; fecha en la primera escena).
4. `VOICE=<es_MX-claude-high.onnx> AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (280-320 s; máx. 330).
5. `python3 make_short.py <dir>/short.json` y `python3 gen_meta.py <dir>` (meta de YouTube con capítulos y aviso, posts y miniatura con la fecha).
6. `bash encolar.sh <dir>`: revisa el límite de YouTube (compartido con los videos de resultados) y encola en `cola/bolsa-<fecha>` de `youtube-cola`.

Voz: Piper `es_MX-claude-high` (github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_MX-claude-high.tar.bz2), ajustes de voz fluida.
Logo: `/mnt/project-files/marca/logo-aiacciones-chile.png`. Dependencias: `pip install piper-tts matplotlib imageio-ffmpeg pillow numpy`.

## Campaña de comentarios (hasta el 22-nov-2026)
`campana.py`: pedido de Daniel del 8-nov-2026. Mientras la fecha de la sesión sea ≤ `HASTA`, el cierre del video y del Short pide un comentario para mejorar el canal e invita a suscribirse (voz y pantalla), y la descripción lo repite con el enlace de suscripción. Después se apaga sola; para extenderla, cambia `HASTA`.

## Reglas
Nada de comprar/vender, precio objetivo ni "cara/barata" (NCG 502). El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados "calculado".
Enlace a aiacciones.cl en video, Short y posts; TikTok con youtube.com/@aiaccioneschile.
LinkedIn (Daniel, 8-nov-2026): se publica el Short como video (cola/bolsa-<fecha>-short/post-linkedin.txt), con resumen que aporte valor, aviso de que el video es de AIAcciones Chile y el enlace al canal de YouTube.
