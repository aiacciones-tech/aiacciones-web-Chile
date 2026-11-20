# Notas para sesiones de Claude

- **Nabd Wall Street, vídeo diario:** desde el 10-nov-2026 el vídeo dura 8-10 minutos con voz Azure. Antes de empezar la tarea
  diaria, lee `nabd/diario/CLAUDE.md`: sus instrucciones sustituyen a las del texto de la tarea programada donde difieran
  (ya no valen "~230 palabras / máx. 180 s" ni `ejemplo-2026-11-06/` como plantilla; la plantilla es `nabd/diario/ejemplo-2026-11-09/`).
- **Wall Street auf Deutsch (canal alemán, código `ge`), vídeo diario:** las instrucciones vigentes están en `ge/diario/CLAUDE.md` y prevalecen
  sobre el texto de su tarea programada. Ese canal solo toca `ge/`, sus workflows `*-GE.yml` y `cola-ge/`; lee los datos de `datos-diario-nabd`
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
