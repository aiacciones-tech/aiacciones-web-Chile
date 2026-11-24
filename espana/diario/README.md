# Vídeo diario de la bolsa española (IBEX 35)

Cada día hábil, después del cierre (17:35 en Madrid): un vídeo de hasta 5 minutos (desde el 10-nov-2026, con más peso del análisis técnico) y su Short para @AIAccionesEspaña,
con posts en X, LinkedIn, TikTok, Instagram y Telegram. Formato aprobado por Daniel el 7-nov-2026.

## Guion (11 escenas, `make_video.py`)
1. **Apertura** (`s_title`): fecha de la sesión EN GRANDE, cierre, variación en % y puntos, curva intradía. La voz da ya la conclusión (≤45 palabras).
2. **Noticias del día** (`s_news`): 3-4 noticias con fuente (CNMV, resultados, operaciones, BCE/macro).
3. **Por qué se movió** (`s_fact`): bolsas del mundo + 4 factores (Wall Street, macro, bancos centrales, bono/prima, euro, petróleo).
4. **Valores** (`s_movers`): 5 que más suben y 5 que más bajan (automático) con motivo de la prensa. Sin motivo publicado: "sin noticia concreta en prensa"; nunca se inventa.
5. **Técnico 1** (`s_tech1`): velas de 6 meses, medias de 50 y 200 sesiones, soportes y resistencias.
6. **Técnico 2** (`s_tech3`): bandas de Bollinger (20, 2) y MACD (12, 26, 9), con el último cruce.
7. **Técnico 3** (`s_tech2`): RSI 14, estocástico (14,3,3), volumen frente a su media. "Son datos, no señales de compra o venta".
8. **Técnico 4** (`s_tech4`): tendencia por plazos (1 semana, 1 mes, 3 meses, en el año, 12 meses) y gráfico de 2 años con la media de 200.
9. **Técnico 5** (`s_tech5`): técnico de los grandes valores (frente a su media de 50, RSI 14, estocástico); `tecnico.valores` en video.json elige hasta 8 (por defecto SAN, BBVA, IBE, ITX, CABK, TEF, AMS, REP).
10. **Agenda** (`s_agenda`): resultados, dividendos y macro de los próximos días.
11. **Cierre** (`s_fin`): resumen y aviso.

Locución: unas 700-750 palabras en total (máx. 300 s; la de ejemplo da 4:15). El técnico (escenas 5 a 9) se lleva cerca de la mitad.

## Pasos de cada día
1. Datos: el workflow `datos-diario-espana.yml` (16:45 UTC, lun-vie) deja `datos/mercado-<fecha>.json` en la rama `datos-diario-es`.
   `python3 tecnico.py <mercado.json>` imprime cierre, medias, RSI, estocástico, niveles y los 5 que más suben/bajan.
   Si la fecha no es la de hoy, no hubo sesión (festivo): no se hace vídeo.
2. Noticias y motivos: prensa del día (EFE/Infobae, Bolsamanía, Expansión, Cinco Días, El Español, The Objective) y CNMV (`espana/datos/hechos.json`).
   Agenda: `espana/datos/calendario-*.json` y `espana/dividendos.py`.
3. Copia `ejemplo-2026-11-09/` a la carpeta del día y cambia `video.json` (textos de pantalla y locución, números en palabras),
   `info.json` (título, descripción, posts, miniatura) y `short.json` (menos de 59 s; fecha en la primera escena).
4. Voz natural: `SCRATCH=<scratch> bash espana/diario/voz.sh <dir>` (desde la raíz del repo; necesita info.json, video.json y short.json ya escritos).
   Lanza `voz-espana.yml` en GitHub (voz neuronal es-ES-AlvaroNeural; Daniel, 10-nov: «sin que la voz suene robótica») y deja los mp3 en `<dir>/voz/`.
   Si cambias la locución después, vuelve a ejecutarlo. Si falla, los scripts usan Piper y avisan con «AVISO: sin voz neuronal».
   `AUD=<scratch> python3 make_video.py <dir> preview` (revisa los PNG), luego sin `preview` (máx. 300 s; escribe `times.json`).
5. `AUD=<scratch> python3 make_short.py <dir>/short.json` (y `short2.json`) y `python3 gen_meta.py <dir>` (meta de YouTube con capítulos y aviso completo, posts y miniatura con la fecha destacada).
6. `bash encolar.sh <dir>`: comprueba el límite de YouTube (~10 subidas/24 h, compartido con los vídeos de resultados) y encola en `cola-es/bolsa-<fecha>` de `youtube-cola`.

Dependencias: voz neuronal en GitHub Actions (`voz_neural.py`, edge-tts); de reserva, `pip install piper-tts matplotlib imageio-ffmpeg pillow numpy`; voz Piper `es_ES-davefx-medium` (variable `VOICE`), logo (`LOGO`).

## Crecimiento del canal (Daniel, 24-nov-2026; detalles en `espana/crecimiento-youtube.md`)
- **Primeros 15 segundos:** la locución de `s_title` es la conclusión del día: qué pasó (cifra), por qué (la causa principal) y el dato
  técnico clave, en **≤45 palabras** y sin «veamos por qué». `make_video.py` se para si no. La primera escena del Short, igual.
- **Título:** la cifra clave (la variación del IBEX, `miniatura.big`) en los primeros 45 caracteres; `gen_meta.py` lo comprueba.
- **Prueba A/B:** `info.miniatura.gancho` (2-4 palabras, p. ej. «La banca tira») e `info.titulo_b` (opcional: el gancho delante, la cifra
  en los primeros 45 caracteres, la fecha al final). `gen_meta.py` hace `miniatura-youtube-b.png` y `ab.json`; `ab-espana.yml` las alterna.
- **Segundo Short** (`short2.json`, mismo formato que `short.json`, `out` = `short2-bolsa-espana-<fecha>.mp4`): otro ángulo, normalmente
  el gráfico del IBEX (medias, osciladores, niveles) o el valor protagonista. Necesita `info.titulo_short2` (con #Shorts) y, opcional,
  `info.resumen_short2`. `voz.sh` hace su voz; render con `AUD=<scratch> python3 make_short.py <dir>/short2.json`. `encolar.sh` lo deja
  programado para las 08:30 de Madrid del día siguiente (solo YouTube). Si un día no hay tiempo, se puede omitir.
- **Pantalla final:** la escena final dura al menos 20 s (no cuenta en los 5 min). Descripciones con enlaces a la sesión anterior y a las
  listas: los resuelve `encolar.sh` (`espana/enlaces_cola.py`); deja ~180 bytes de margen en la descripción (`gen_meta.py` lo comprueba).

## Llamada a comentar y suscribirse (hasta el 22-nov-2026)
Daniel (8-nov-2026): hasta el 22-nov-2026 incluido, cada vídeo pide dejar un comentario y suscribirse. `make_video.py` lo añade a la locución y a la pantalla final, y `gen_meta.py` a la descripción, el Short y los posts; se apaga solo después de esa fecha (`CTA_HASTA`). En `short.json`, termina la voz de la escena `fin` con «Déjanos tu comentario y suscríbete». Deja unos 10 s de margen en la locución para no pasar de 5 minutos.

## LinkedIn (regla permanente, Daniel 8-nov-2026)
En LinkedIn se publica el Short subido como vídeo, no como enlace (`encolar.sh` pone `post-linkedin.txt` en la carpeta `-short`). Texto: 3 o 4 datos clave (cifras y qué cambió) y una conclusión, sin relleno (`info.json` → `linkedin.datos` y `linkedin.conclusion`), «Vídeo elaborado por AIAcciones España (@AIAccionesEspaña)» y al final el enlace al canal. Telegram usa `post-telegram.txt` (texto largo con el enlace al vídeo completo).

## Reglas
Nada de comprar/vender, precio objetivo ni "cara/barata". El análisis técnico se presenta como datos. Cada cifra con fuente; cálculos propios marcados "calculado".
Aviso completo en la descripción. Español de España.

## Para otros mercados
Cambia el índice y los valores en `datos_mercado.py` (`EMISORES`, tickers de Yahoo y TradingView), los nombres en `tecnico.py`, el logo, la voz y la cola de YouTube.
