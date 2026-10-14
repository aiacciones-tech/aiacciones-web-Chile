# Encargo: vídeo de resultados 1S 2026 de un banco del IBEX 35 (AIAcciones España)

Copia EXACTAMENTE el modelo de Bankinter, ya publicado: /mnt/project-files/espana/bankinter/
(base.py, narracion.py, make_video_voz.py, miniatura.py, short-1S26.json, meta-youtube.json, meta-short.json,
post-linkedin-1S26.txt, post-x-1S26.txt, guion-1S26.md). Lee todos esos archivos primero; tu banco va en
/mnt/project-files/espana/<id>/ con los mismos nombres de archivo (cambia "bankinter" por <id> en los nombres de mp4).

## Pasos
1. Cifras oficiales del 1S 2026 (informe de julio 2026) con WebSearch (mode "extended") y WebFetch: nota de prensa del banco,
   y prensa (Expansión, Cinco Días, El Español, Bolsamania/Capitalbolsa, Investing, Europa Press, Infobae).
   Necesitas: beneficio neto (y del 2T), margen de intereses, comisiones netas, margen bruto, costes, margen neto/explotación,
   provisiones/coste del riesgo, eficiencia, ROE/ROTE, morosidad, cobertura, CET1, crédito, depósitos/recursos, desglose por país/negocio,
   comparación con el consenso (fuente nombrada; si solo hay "en línea"/"supera", dilo cualitativo), guía 2026, dividendo/recompras,
   y la reacción si está. Valoración: stockanalysis.com/quote/bme/<TICKER>/ y /statistics/ y /financials/ratios/ (precio con fecha,
   capitalización, acciones, PER 12m, forward, P/VC, dividendo; históricos anuales PER, P/VC, rentabilidad por dividendo). Próximo informe
   3T26 (memoria: Santander 28-oct, BBVA 29-oct, CaixaBank 30-oct confirmadas; Sabadell/Unicaja verifícalo o márcalo "estimado").
   Cada cifra lleva su fuente en guion-1S26.md; los cálculos propios se marcan "calculado". Si una cifra no la encuentras, NO la inventes:
   quita esa escena o cámbiala por otra con dato real.
2. narracion.py (números escritos en palabras para la voz), make_video_voz.py (15 escenas, mismas 7 secciones y mismo cierre
   con aviso; en bancos: sección 4 = eficiencia/rentabilidad, riesgo y capital, volumen; valoración con PER, P/VC y dividendo, sin EV/EBITDA ni FCF).
   Si el banco es grande con varios países (Santander, BBVA), la escena s2b muestra el beneficio por país/negocio.
3. Previews: `AUD=<scratch>/aud-<id> python3 make_video_voz.py preview`, mira los PNG (montaje) y corrige solapes o textos cortados.
4. Render: `AUD=<scratch>/aud-<id> VOICE=/tmp/claude-0/-home-claude-aiacciones-web-chile/300b608f-ded3-59e5-a58f-4fe123b3d25c/scratchpad/voces/vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx python3 make_video_voz.py`
   (tarda varios minutos; corre en background y espera con un bucle until sobre AUD/times.json, nunca sleep suelto). Usa times.json para los capítulos.
5. miniatura.py → miniatura-youtube.png 1280x720 (revisa que nada se corte ni se solape).
6. short-1S26.json y Short: `cd <scratch> && AUD=<scratch>/aud-<id>-short VOICE=... python3 /mnt/project-files/espana/shorts/make_short_es.py /mnt/project-files/espana/<id>/short-1S26.json`
   Debe durar menos de 59 s. Si el número grande de la escena titulo es largo, pon "big_fs": 185. Revisa 6 fotogramas.
7. meta-youtube.json: título ≤100 caracteres, sin "<" ni ">" en la descripción; descripción como la de Bankinter con capítulos,
   fuentes y el AVISO IMPORTANTE completo de /mnt/project-files/espana/marca/aviso-legal.txt (rellena {fecha_hora} = "13-oct-2026, <hora Madrid actual redondeada>",
   {empresa}, {fuentes}; cambia la frase de metodología para bancos como en Bankinter). privacy "public".
   meta-short.json con {video:<id>-1S26}. post-linkedin-1S26.txt con {youtube} y aviso corto. post-x-1S26.txt con {youtube},
   máx. 280 caracteres contando la URL como 23 y emojis como 2.
8. ficha-web.py: un archivo con un dict Python `FICHA = {...}` con las mismas claves que las fichas de /home/claude/aiacciones-web-chile/espana/fichas.py
   (mira la de bankinter); en "videos" pon [("VIDEO_ID", "<título>"), ("SHORT_ID", "<id> 1S 2026 en 60 segundos (Short)")] con esos
   marcadores literales; los rellenará quien sube.

## Reglas (obligatorias)
- Español de España. Nada de recomendaciones de compra/venta, precio objetivo ni "barata/cara"; la valoración solo compara con su propia historia.
- No menciones precios objetivo ni recomendaciones de analistas aunque aparezcan en las fuentes.
- No "los primeros"/"los más rápidos".
- AIAcciones España no tiene posiciones en las empresas analizadas (va en cierre, Short, posts y aviso).
- NO subas nada a YouTube, NO toques git, la rama youtube-cola ni Buffer: solo deja los archivos en /mnt/project-files/espana/<id>/.
- Trabaja solo dentro de /mnt/project-files/espana/<id>/ y tu carpeta de scratch; no modifiques archivos de otras carpetas
  (los generadores compartidos se usan, no se editan).
- Piper, matplotlib e imageio-ffmpeg ya están instalados; no instales paquetes.

## Entrega
Responde con: ruta de la carpeta, título del vídeo, duración del vídeo y del Short, las 5-6 cifras clave con su fuente,
cualquier dato que no pudiste confirmar, y si hubo algo raro.
