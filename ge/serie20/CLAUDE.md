# Serie «Die Wall-Street-Giganten» de Wall Street auf Deutsch: instrucciones de la rutina (Daniel, 18-nov-2026)

Adaptación al alemán de la serie de Nabd (`nabd/serie20/CLAUDE.md`). Un episodio en alemán por empresa **después de cada informe de resultados**,
desde el informe de Nvidia del 17-nov-2026 (`INICIO_GE` en `plan.py`), de las 20 mayores empresas de EE. UU.:
NVDA, MSFT, AAPL, GOOGL, AMZN, META, AVGO, TSLA, BRK, JPM, LLY, WMT, ORCL, V, MA, XOM, NFLX, COST, JNJ, PLTR, **y además Anthropic (ANT) y SpaceX (SPCX)** (Daniel, 21-nov-2026; solo en el canal alemán).
Reglas: **máximo 4 minutos** por vídeo; **máximo 3 vídeos de la serie al día** (el resto pasa a los días siguientes, `plan.py` lo reparte);
sin Short; sin pasos manuales; todo lo que se entrega termina en `-GE`. Instrucciones en español; lo que ve y oye el público, en alemán («Sie»).
Valen todas las reglas de `ge/diario/CLAUDE.md` (Keine Anlageberatung, transparencia IA, secretos `_GE`, solo se toca `ge/`, `*-GE.yml` y `cola-ge/`).

## Piezas
- Datos: rama `datos-serie20-nabd` (la escribe `serie20-datos-Nabd.yml` a las 11:00 y 23:30 UTC, a menudo con horas de retraso; **solo lectura**:
  no se lanza ese workflow desde aquí).
  `calendario.json` y `<TICKER>/datos.json` (TradingView). `datos_listos=false` significa que TradingView aún no tiene el trimestre: se espera.
- Datos de ANT y SPCX: rama `datos-serie20-ge` (la escribe `serie20-datos-GE.yml` a las 11:10 y 23:40 UTC con `ge/serie20/datos_extra.py`,
  que reutiliza `nabd/serie20/datos_tv.py` sin tocarlo; mismo formato). Este workflow sí es del canal y se puede lanzar a mano.
- `plan.py <datos> <cola-ge> [<datos-ge>]`: episodios de hoy (0-3, día de Berlín) y pendientes, de las dos ramas de datos; cada episodio dice en `datos` de qué carpeta copiar `datos.json`.
- `make_episodio.py <carpeta> [preview]`: 7 escenas (Einstieg, Das Quartal in Zahlen, Umsatz und Marge, Bilanz, Cashflow, Erwartungen, Fazit),
  1920x1080, 120-240 s, control de calidad. Las cifras de pantalla salen solas de `datos.json`.
- `meta_episodio.py <carpeta>`: meta de YouTube (`language: de`), posts de Telegram, X, LinkedIn (página del canal, con enlace al episodio) y TikTok (el episodio entero), los tres últimos vía Buffer, miniatura.
- `encolar.sh <carpeta>`: `cola-ge/serie20-<ticker>-<fecha>/` en `youtube-cola`; `youtube-GE.yml` sube y `telegram-GE.yml` publica.
- Voz: `.github/workflows/serie20-voz-GE.yml` (Azure de-DE-ConradNeural, mismo recurso que el diario), rama `voz-ge-serie20` (aparte de `voz-ge`).
- Ejemplo de `video.json`: `episodios/serie20-nvda-2026-11-17/`. Claves: ticker, nombre, sector, sector_tipo («banco» para JPM, BRK no),
  trimestre (el del año fiscal de la empresa según su nota, p. ej. «3. Quartal GJ 2027» para Nvidia; los gráficos usan la etiqueta de TradingView, que es el trimestre natural en que acaba), fecha_resultados, titular,
  expectativas {items [[título, texto]] 0-2, fuente}, claves (3), voz (7 escenas), info {titulo ≤ 100, resumen, fuentes, hashtags, x ≤ 200, tags},
  miniatura {etiqueta, cifra («57,0 Mrd. $»), sub, color}.

## Pasos
1. Clona `datos-serie20-nabd` (`git clone -q --depth 1 -b datos-serie20-nabd ...`) y `cola-ge` de `youtube-cola` (sparse, como `encolar.sh`).
   Clona también `datos-serie20-ge` (igual, `-b datos-serie20-ge`).
   `python3 ge/serie20/plan.py <datos> <scratch>/cola/cola-ge <datos-ge>`. Si "hoy" está vacío, termina.
2. Por cada episodio: `ge/serie20/episodios/<carpeta>/`, copia `<datos del episodio>/<TICKER>/datos.json` (no se sube al repo). Busca en la prensa del día (nota de la empresa,
   Reuters, CNBC, AP, Yahoo Finance; en alemán Handelsblatt, Börse Online, finanzen.net) qué explicó los números y la guía de la empresa.
   Escribe `video.json`: `voz` en alemán, **380-440 palabras** (calibrado: 419 palabras dieron 3:25 con Azure; «Prozent», «Milliarden Dollar»), las cifras dichas son las de pantalla;
   lo de la prensa se atribuye («laut Mitteilung des Unternehmens»). Nada de comprar/vender, Kursziele ni «günstig/teuer».
3. Sube los `video.json` a `claude/ge-serie20-<fecha de hoy>`: `serie20-voz-GE.yml` genera la voz (2-4 min). Clona `voz-ge-serie20`: `VOZ_DIR=<clon>/<carpeta>`.
4. `AUD=<scratch> python3 ge/serie20/make_episodio.py <carpeta> preview` (mira todos los PNG), luego sin preview con `VOZ_DIR`,
   y `python3 ge/serie20/meta_episodio.py <carpeta>`.
5. `SCRATCH=<scratch> bash ge/serie20/encolar.sh <carpeta>` (uno detrás de otro); espera el enlace.
6. Copia mp4, miniatura, meta y guion a `/mnt/project-files/ge-serie20/<carpeta>/`. Resumen corto en español.
