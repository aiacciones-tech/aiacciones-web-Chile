# «Wochenkalender der Quartalszahlen» de Wall Street auf Deutsch: instrucciones de la rutina (Daniel, 22-nov-2026)

Short vertical 9:16 de **45 a 60 s**, todo en alemán, voz Azure `de-DE-ConradNeural` (el mismo recurso del canal). Sale **cada domingo entre las 18:00
y las 20:00 de Berlín**. Instrucciones en español; lo que ve y oye el público, en alemán. Valen las reglas de `ge/diario/CLAUDE.md`
(Keine Anlageberatung, transparencia IA, secretos `_GE`, solo se toca `ge/`, `*-GE.yml` y `cola-ge/`).

## Contenido
- **Solo las 22 acciones del canal** (las de `ge/serie20/CLAUDE.md`): NVDA, MSFT, AAPL, GOOGL, AMZN, META, AVGO, TSLA, BRK, JPM, LLY, WMT, ORCL, V, MA,
  XOM, NFLX, COST, JNJ, PLTR, ANT (Anthropic) y SPCX (SpaceX). Ninguna otra.
- Las que presentan resultados de **lunes a viernes de la semana siguiente**. Por cada una (orden cronológico): nombre y ticker, día, antes de la apertura
  (`vor US-Börsenbeginn`) o después del cierre (`nach US-Börsenschluss`, 22 Uhr deutscher Zeit; 21 Uhr en las semanas de desfase de horario),
  y el consenso: ingresos (`Umsatz`) y BPA (`Gewinn je Aktie`). Unos 6-10 s por empresa (máx. 6 empresas en 60 s; si son más, las 6 más grandes por
  capitalización y el resto en «… und N weitere» del gancho y en los textos).
- **Datos verificados en la web, nunca inventados.** Fecha: preferir la nota de la empresa (sala de prensa / IR, SEC 8-K); si solo hay estimación
  (Earnings Whispers «expected», TradingView), decir «voraussichtlich» en voz y pantalla (`estado`). Consenso: Earnings Whispers (lo leen bien
  los agentes web-fetch); contrastar con la guía de la empresa si la hay. MarketBeat y days.to están desactualizados o bloqueados.
  **Si falta un dato, se quita del guion** (y de la pantalla: `umsatz`/`eps` vacíos no se dibujan). Fuentes de cada empresa en `verificacion`.
- Punto de partida: `calendario.json` de la rama `datos-serie20-nabd` (`proxima_ny` de las 22; ANT y SPCX también en `datos-serie20-ge`).
  Una hora `T12:00` es un hueco de TradingView, no una hora real.
- **Pocas o ninguna** (0-1) de las 22 esa semana: modo `"proximos"`: «Próximos reportes» con las siguientes 3-4 en orden cronológico.

## Guion (`calendario.json`, escenas)
1. `gancho` (~3-5 s): semana normal «Diese Woche berichtet [la más grande]… und [N] weitere unserer Aktien.»; modo proximos: «Thanksgiving-Woche /
   Diese Woche: keine Zahlen von unseren 22 Aktien. Als Nächstes berichtet …».
2. `empresa` (una por acción, `n` 1..N): nombre, ticker, dia («Mi., 9. Dezember»), momento, hora, umsatz, eps, estado, nota opcional, voz.
   Voz corta (~18 palabras): «Mittwoch, 9. Dezember, nach Börsenschluss: Broadcom. Konsens: 34,9 Milliarden Dollar Umsatz und 3,45 Dollar je Aktie.»
3. `fin`: voz exacta «Folge dem Kanal für die Analyse jeder Zahlenvorlage. Keine Anlageberatung. Nur zu Informationszwecken.»
Calibrado 22-nov: 103 palabras = 55,9 s con Azure (≈ 9-10 s por empresa con 4 empresas). `make_calendario.py` corta si pasa de 60 s.

## Pasos (cada domingo; la tarea programada arranca ~16:40 Berlín)
1. Clona `datos-serie20-nabd` y `datos-serie20-ge`; lista las de `proxima_ny` en lunes-viernes siguientes. Verifica cada una en la web (fecha, hora, consenso).
2. Copia `semanas/2026-11-22/` como plantilla a `ge/calendario/semanas/<domingo>/` (solo `calendario.json`), reescribe `fecha`, `semana`, `rango`,
   `modo`, `out`, `fuente`, `verificacion` y las escenas.
3. `AUD=<scratch> python3 ge/calendario/make_calendario.py <dir>/calendario.json preview` y mira todos los PNG.
4. Sube `calendario.json` a la rama `claude/ge-calendario-<domingo>`: `calendario-voz-GE.yml` genera la voz (1-2 min) en la rama `voz-ge-calendario`.
   Clónala y `AUD=<scratch> VOZ_DIR=<clon>/<domingo> python3 ge/calendario/make_calendario.py <dir>/calendario.json`.
5. `python3 ge/calendario/meta_calendario.py <dir>` (meta de YouTube y posts de TikTok, Instagram, Threads y Telegram).
6. Copia todo (mp4, miniatura, meta, posts, guion) a `/mnt/project-files/ge-calendario/<domingo>/`. No subas el mp4 al repo.
7. **A partir de las 18:00 de Berlín** (antes no): `SCRATCH=<scratch> bash ge/calendario/encolar.sh <dir>` → `cola-ge/calendario-<domingo>/`;
   `youtube-GE.yml` lo sube, `telegram-GE.yml` y `buffer-GE.yml` publican (Threads espera sin error si no está conectado en Buffer).
8. Resumen corto en español para Daniel con el enlace.
