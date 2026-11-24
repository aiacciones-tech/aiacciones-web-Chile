# Notas para sesiones de Claude

- **Nabd Wall Street, vídeo diario:** desde el 10-nov-2026 el vídeo dura 8-10 minutos con voz Azure. Antes de empezar la tarea
  diaria, lee `nabd/diario/CLAUDE.md`: sus instrucciones sustituyen a las del texto de la tarea programada donde difieran
  (ya no valen "~230 palabras / máx. 180 s" ni `ejemplo-2026-11-06/` como plantilla; la plantilla es `nabd/diario/ejemplo-2026-11-09/`).
- **Wall Street auf Deutsch (canal alemán, código `ge`), vídeo diario:** las instrucciones vigentes están en `ge/diario/CLAUDE.md` y prevalecen
  sobre el texto de su tarea programada. Desde el 25-nov-2026 sale por la mañana (Berlín) con la sesión de la noche anterior, más 2 Shorts extra a las 12:15 y 15:05. Ese canal solo toca `ge/`, sus workflows `*-GE.yml` y `cola-ge/`; lee los datos de `datos-diario-nabd`
  sin modificarlos. Sus secretos de GitHub terminan en `_GE`.
- **Arabia Saudita (@SaudiArabiaAIStocks, `saudi/diario/`), vídeo diario:** desde el 18-nov-2026 la voz es Azure `ar-SA-HamedNeural` (workflow `voz-saudi.yml`,
  rama `voz-saudi`, `VOZ_DIR`). Antes de empezar, lee `saudi/diario/CLAUDE.md`: prevalece sobre el texto de la tarea programada donde difieran.
- **Voz de AIAcciones Chile (diario IPSA, videos de resultados y Shorts):** desde el 18-nov-2026 es Azure `es-CL-LorenzoNeural` (elección de Daniel);
  Piper solo de respaldo. Antes de renderizar, lee `voz-cl/README.md`: `bash voz-cl/pedir.sh <id> <dir> <fuentes>` y luego el render de siempre con
  `PYTHONPATH=<repo>/voz-cl/shim VOZ_DIR=<dir>`. Prevalece sobre "voz Piper" en el texto de las tareas programadas de Chile.
  Desde el 19-nov-2026 Lorenzo va un 5% más rápido (Daniel, para acortar los videos): el mismo guion del diario dura ~265 s. No alargues el guion
  para llegar a 280 s: en el diario valen 255-320 s (unos 4:15-5:00), aunque la tarea programada diga 280-320.
- **Arabia Saudita, serie educativa semanal «التحليل الفني ببساطة» (sábados):** instrucciones y pasos en `saudi/educativo/CLAUDE.md`
  (prevalecen sobre el texto de su tarea programada). Plan de temas en `saudi/educativo/plan-saudi.json`.
- **AI Stocks UAE, serie semanal de análisis fundamental (`eau/fundamental/`):** un capítulo cada sábado (~18:00 EAU). Antes de cada capítulo lee
  `eau/fundamental/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Qatar AI Stocks, serie semanal de análisis fundamental (`qatar/fundamental/`):** un capítulo cada sábado (~18:00 Doha). Antes de cada capítulo lee
  `qatar/fundamental/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **AIAcciones Chile, serie semanal «Análisis fundamental en simple» (`fundamental-cl/`):** un capítulo cada domingo (~10:00 Santiago) desde el 6-dic-2026,
  en español con la voz Lorenzo. Antes de cada capítulo lee `fundamental-cl/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Qatar AI Stocks, serie semanal de análisis técnico «التحليل الفني ببساطة» (`qatar/educativo/`):** empieza cuando termine la serie fundamental
  (enero de 2027). Antes de cada lección lee `qatar/educativo/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Nabd Wall Street, serie semanal «التحليل الأساسي ببساطة» (sábados, `nabd/fundamental/`):** análisis fundamental con cifras reales de empresas de EE. UU.
  Antes de cada capítulo lee `nabd/fundamental/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Bahrain AI Stocks, serie educativa semanal «التحليل الفني ببساطة» (sábados, desde el 28-nov-2026):** instrucciones en `bahrain/educativo/CLAUDE.md`
  (prevalecen sobre el texto de su tarea programada). Plan de 10 temas en `bahrain/educativo/plan-lessons-bahrain.json`.
- **Qatar AI Stocks, Short semanal «تقويم النتائج الأسبوعي» (`qatar/calendario/`):** cada sábado entre las 20:00 y las 21:00 de Doha.
  Antes de cada Short lee `qatar/calendario/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Bahrain AI Stocks, Short semanal «تقويم النتائج الأسبوعي» (sábados 20:00-21:00 Manama, `bahrain/calendar/`):** voz Azure `ar-BH-AliNeural`.
  Antes de cada semana lee `bahrain/calendar/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Wall Street auf Deutsch, Short semanal «Wochenkalender der Quartalszahlen» (domingos 18:00-20:00 Berlín, `ge/calendario/`):** calendario de resultados
  de las 22 acciones del canal. Antes de cada Short lee `ge/calendario/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Nabd Wall Street, Short semanal «تقويم النتائج الأسبوعي» (domingos, 19:00-21:00 Riad, `nabd/calendario/`):** calendario de resultados de las 22 acciones
  del canal. Antes de cada Short lee `nabd/calendario/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **AIAcciones España, crecimiento del canal de YouTube (desde el 24-nov-2026):** cifra clave en títulos y miniaturas con prueba A/B
  (`ab-espana.yml`), conclusión en los primeros 15 s, segundo Short del diario programado (`canal-espana.yml`), listas de reproducción y
  enlaces al siguiente vídeo. Lee `espana/crecimiento-youtube.md` antes de cualquier vídeo de España: prevalece sobre las tareas programadas.
- **AIAcciones España, directo «El IBEX de la semana, en directo» (viernes 17:45 Madrid, lo emite Daniel):** diapositivas y guion con
  `espana/directo/make_slides.py`. Antes de cada viernes lee `espana/directo/CLAUDE.md`: prevalece sobre el texto de su tarea programada.
- **AIAcciones España, Short semanal «Calendario semanal de resultados» (domingos 18:00-20:00 Madrid, `espana/semanal/`):** antes de cada
  edición lee `espana/semanal/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Wall Street auf Deutsch, Short diario «DAX am Abend» (prueba desde el 24-nov-2026, `ge/dax/`):** L-V tras el cierre de Xetra (18:30-20:00 Berlín).
  Antes de cada Short lee `ge/dax/CLAUDE.md`: prevalece sobre el texto de su tarea programada donde difieran.
- **Arabia Saudita, playlists de YouTube (por empresa, sector y formato):** se crean y rellenan solas tras cada subida (`scripts/playlists-saudi.py`,
  paso de `youtube-saudi.yml`). Detalles en `saudi/playlists/CLAUDE.md`; las carpetas nuevas de `cola-sa/` deben seguir los nombres que allí se listan.
- **Arabia Saudita, directos en momentos clave (Fed, OPEP+, presupuesto, resultados anuales; `saudi/directos/`):** directo automático emitido desde
  GitHub Actions (`directo-saudi.yml`). Antes de cada directo lee `saudi/directos/CLAUDE.md`: prevalece sobre el texto de su tarea programada.
- **Arabia Saudita, pruebas A/B de miniatura y título (desde el 24-nov-2026):** los videos largos del diario y de la serie educativa llevan una variante B
  (`ab.json` + `miniatura-b.png` en su carpeta de `cola-sa/`). `scripts/ab-saudi.py` (workflow `ab-saudi.yml`, 08:10 UTC) las alterna por días y deja
  la ganadora; el estado está en `cola-sa/<slug>/ab-estado.json` de `youtube-cola`. Detalles en `saudi/ab-saudi.md`.
