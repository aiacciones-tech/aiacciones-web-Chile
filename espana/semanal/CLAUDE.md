# Calendario semanal de resultados (Short de los domingos, @AIAccionesEspaña)

Formato pedido por Daniel el 22-nov-2026. Estas instrucciones prevalecen sobre el texto de la tarea programada donde difieran.

## Formato
- Short vertical 9:16, **45 a 60 s**, voz `es-ES-AlvaroNeural` (la del canal), marca y colores del vídeo diario.
- Sale **cada domingo entre las 18:00 y las 20:00 (Madrid)** con las empresas que reportan de lunes a viernes de la semana siguiente.
- **Solo empresas españolas** (Daniel, 23-nov-2026: «solo acciones españolas»): primero las del IBEX 35 y, después, las del
  Mercado Continuo más relevantes, hasta 5-7. Nada de empresas extranjeras (ni europeas ni de EE. UU.). Unos 6-8 s por empresa.
- Semanas con pocas: si hay de 1 a 4 españolas, el Short sale con esas (puede durar menos de 45 s; se puede añadir en la escena
  una línea de agenda española verificada, p. ej. un dividendo o una junta, pero nunca empresas extranjeras). Si no reporta
  ninguna española, **no se publica**: avisa a Daniel en el hilo con lo que comprobaste.
- Por empresa: nombre y ticker, bolsa, día y momento (antes de la apertura / tras el cierre / hora de Madrid) y lo que espera el
  mercado: **consenso de analistas** (BPA e ingresos; en España se publica a menudo beneficio neto, ebitda o ingresos: campos
  `bpa`, `beneficio`, `ebitda`, `ingresos`, se muestran como máximo dos). Fuentes: Europa Press/Expansión/Cinco Días (consenso de
  FactSet, Bloomberg o LSEG), Bolsamanía, Investing.es, Estrategias de Inversión.
- Guion: 1) gancho (3 s): «Esta semana reporta [la más importante]… y [N] empresas más que mueven el mercado.» (con una sola: «Esta semana reporta [X].»)
  2) las empresas en orden cronológico; 3) cierre: «Sigue el canal para el análisis de cada reporte.» + aviso
  «Contenido informativo, no es recomendación de inversión.»

## Reglas de datos (Daniel: «no los inventes»)
- Busca y **verifica en la web** cada fecha, momento y cifra; anota la fuente en `verificacion` de `calendario.json`.
- Fecha y hora: mejor la web o nota de la propia empresa (agenda del inversor, CNMV); si no, dos calendarios que coincidan.
- Consenso: Zacks (Yahoo Finance, TradingView, The Globe and Mail), Nasdaq/Stocktitan, Barchart, MarketBeat, prensa.
  La guía de la empresa **no** es consenso. Si las fuentes discrepan poco, usa una y di el rango en `nota`; si discrepan mucho
  (p. ej. GAAP frente a ajustado), descarta la empresa o el dato.
- **Si falta un dato, sácalo del guion** (no se dice ni se pone «n. d.»): la escena muestra solo lo que hay
  (`sin_consenso` = una línea descriptiva verificable de la empresa).
- Comprueba festivos de la Bolsa española y dilo en `nota_semana` (va en la descripción y en Telegram).
- La edición del 23-nov-2026 (`ejemplo-2026-11-23/`) mezcló empresas extranjeras: úsala solo como plantilla de formato.
- Calendario del IBEX: `espana/datos/calendario-*.json`; hechos de la CNMV: `espana/datos/hechos.json`.
- El contenedor no llega a cnmv.es ni a algunas webs: usa el navegador integrado del ordenador de Daniel si está conectado,
  o un agente web-fetch.

## Pasos (desde la raíz del repo)
1. Carpeta de la semana: `/mnt/project-files/espana/semanal/<lunes AAAA-MM-DD>/`. Copia `calendario.json` de
   `ejemplo-2026-11-23/` y cámbialo todo (fechas, `rango`, empresas, `voz` con números en palabras, `titulo`, `linkedin`,
   `fuentes`, `verificacion`, `nota_semana`). Unas 140-150 palabras de locución en total.
2. Vista previa: `AUD=<scratch> python3 espana/semanal/make_short_cal.py <carpeta>/calendario.json preview` (revisa los PNG).
3. Voz: `SCRATCH=<scratch> bash espana/semanal/voz_cal.sh <carpeta> +5%` (workflow `voz-espana.yml` en GitHub; mp3 en `<carpeta>/voz/`).
4. Vídeo: `AUD=<scratch> python3 espana/semanal/make_short_cal.py <carpeta>/calendario.json` (para si pasa de 60 s: acorta la voz).
   Revisa 4-5 fotogramas.
5. Textos: `python3 espana/semanal/gen_meta_cal.py <carpeta>` (meta del Short, X, LinkedIn, TikTok, Instagram, Threads, Telegram y `guion.md`).
6. Publicar **entre las 18:00 y las 20:00 de Madrid**: `SCRATCH=<scratch> bash espana/semanal/encolar_cal.sh <carpeta>`
   (sube al momento, público; comprueba el límite de ~10 subidas/24 h). Deja el ID en `<carpeta>/ids.txt`.

## Redes
- YouTube Short (`youtube-espana.yml`), X con enlace, LinkedIn con el Short como vídeo (regla permanente del 8-nov-2026:
  3-4 datos clave + conclusión, «Vídeo elaborado por AI Acciones España (@AIAccionesEspaña)», enlace al canal),
  TikTok, Instagram Reel, Telegram (`post-telegram.txt` + portada) y Threads (`post-threads.txt`, ≤500 caracteres).
- Threads: el 22-nov-2026 España no tenía canal de Threads en Buffer; el post espera sin error hasta que Daniel lo conecte
  (cuenta BUFFER_API_KEY_ES2, que tiene hueco).
- Campaña «comenta y suscríbete»: solo hasta el 22-nov-2026 (los scripts la quitan solos después).
