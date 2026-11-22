# Calendario semanal de resultados (Short de los domingos, @aiaccioneschile)

Formato pedido por Daniel el 22-nov-2026. Short vertical 9:16 de 45-60 s, voz Azure `es-CL-LorenzoNeural` (`../voz-cl/`).
Sale los domingos entre las 18:00 y las 20:00 de Chile, con las empresas que reportan de lunes a viernes de la semana siguiente.

## Contenido
- 5 a 7 empresas: primero las del IPSA que reporten (las que más mueven el mercado), y se completa con las grandes de Wall Street.
- Por empresa (6-8 s): nombre y ticker, día, antes de la apertura o después del cierre, y consenso de BPA e ingresos.
- Cada fecha y cada consenso se verifican en la web (al menos dos fuentes para EE. UU.: TheStreet, TipRanks, StockTitan, Opening Bell;
  Chile: calendario de `fuente/calendario.py`, MarketScreener, Investing.com, Quartr). Si falta un dato o las fuentes no coinciden, se saca del guion
  (sin consenso: la empresa sale sin cifras; sin hora: "Hora no informada"). Nunca se inventa.
- Guion: 1) gancho "Esta semana reporta [la más importante]… y [N] empresas más que mueven el mercado." 2) empresas en orden cronológico.
  3) "Sigue el canal para el análisis de cada reporte."

## Pasos
1. Copia `semanas/2026-11-23/` a `semanas/<lunes>/` y cambia `short.json` (escenas) y `textos.md` (guion, tabla de fuentes, textos por red).
2. `AUD=<scratch> python3 calendario-cl/make_calendario.py <dir>/short.json preview` y revisa los PNG.
3. `bash voz-cl/pedir.sh calendario-<lunes> <scratch>/voz <dir>/short.json`
4. `PYTHONPATH=<repo>/voz-cl/shim VOZ_DIR=<scratch>/voz AUD=<scratch> python3 calendario-cl/make_calendario.py <dir>/short.json`
   (falla si pasa de 60 s; bajo 45 s alarga el cierre). `python3 voz-cl/voz_cl.py resumen <scratch>/voz` debe decir 0 con Piper.
5. Escribe los archivos de publicación en la carpeta de la semana: `meta-short.json` (título, descripción que termina con el aviso,
   tags, `"privacy": "public"`), `post-tiktok.txt`, `post-instagram.txt`, `post-threads.txt` (máx. 500, con `{youtube}`) y
   `post-telegram.txt` (texto plano, con `{youtube}`). Son los mismos textos de `textos.md`.
6. Copia el mp4 y `textos.md` a `/mnt/project-files/calendario-resultados/<lunes>/`.
7. Publicación automática (Daniel, 22-nov-2026): `SCRATCH=<scratch> bash calendario-cl/encolar.sh calendario-cl/semanas/<lunes>`.
   Espera hasta las 18:02 de Chile si es antes; después de las 20:00 no publica. Sube el Short a YouTube (público) y, tras la subida,
   Buffer lo publica en TikTok, Instagram (Reel) y Threads (si Threads no está conectado en la cuenta de Buffer de Chile, queda pendiente)
   y telegram-chile.yml en Telegram. Deja el enlace en `ids.txt`.
Entregables: guion y video; título, descripción y hashtags de YouTube Shorts; textos para TikTok, Instagram Reels, Threads y Telegram.
La descripción termina con "Contenido informativo, no es recomendación de inversión."
