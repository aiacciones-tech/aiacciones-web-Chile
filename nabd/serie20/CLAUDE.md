# Serie «عمالقة وول ستريت» de Nabd Wall Street: instrucciones de la rutina diaria (Daniel, 13-nov-2026)

Un episodio en árabe por empresa **después de cada informe de resultados**, a partir del trimestre en curso (eventos desde el 1-oct-2026),
de las 20 empresas: NVDA, MSFT, AAPL, GOOGL, AMZN, META, AVGO, TSLA, BRK, JPM, LLY, WMT, ORCL, V, MA, XOM, NFLX, COST, JNJ, PLTR.
Reglas de Daniel: **máximo 4 minutos** por vídeo; **máximo 3 vídeos de la serie al día** (si coinciden más, pasan a los días siguientes;
`plan.py` lo reparte); sin pasos manuales; todo lo que se entrega termina en `-Nabd`. Presentación de la serie: https://www.youtube.com/watch?v=hU3GozeSL_U
El vídeo diario (nabd/diario/, 8-10 min) es otra cosa y no cambia.

## Piezas
- `datos_tv.py` + `.github/workflows/serie20-datos-Nabd.yml` (11:00 y 23:30 UTC, o a mano): rama `datos-serie20-nabd` con `calendario.json`
  (fecha del último informe de cada empresa, su trimestre fiscal, `datos_listos` y la próxima fecha) y `<TICKER>/datos.json` (cifras del
  trimestre, 12 trimestres de historial, balance, flujo de caja, estimaciones y sorpresa de los analistas). Fuente: TradingView. La SEC
  (EDGAR) bloquea las descargas automáticas desde GitHub Actions y WebFetch (403 / robots), así que no se usa.
- `plan.py <datos> <cola-nabd>`: los episodios de hoy (0-3) y los pendientes. Solo cuenta informes con `datos_listos`.
- `make_episodio.py <carpeta> [preview]`: 7 escenas, 1920x1080, voz Azure con `VOZ_DIR` (Piper si falta), control de calidad, 120-240 s.
  Todas las cifras de pantalla salen solas de `datos.json`; `video.json` solo pone textos, locución y la guía de la empresa.
- `meta_episodio.py <carpeta>`: meta de YouTube, post de Telegram y de X, miniatura. Sin Short.
- `encolar.sh <carpeta>`: cola-nabd/serie20-<ticker>-<fecha>/ en youtube-cola; youtube-Nabd.yml sube, telegram-Nabd.yml y buffer-Nabd.yml (X) publican.
- Ejemplos de `video.json`: `episodios/serie20-jpm-2026-10-13/` (banco: `"sector_tipo": "banco"`), `serie20-jnj-2026-10-13/`, `serie20-nflx-2026-10-20/`.

## Pasos de cada día
1. Lanza `serie20-datos-Nabd.yml` (workflow_dispatch en main) y espera a que termine (1-2 min); clona la rama `datos-serie20-nabd` (--depth 1).
2. Clona `cola-nabd/` de `youtube-cola` (no hagas `git fetch` de toda la rama, es enorme): `git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola
   https://github.com/aiacciones-tech/aiacciones-web-Chile.git <scratch>/cola && cd <scratch>/cola && git sparse-checkout set cola-nabd`.
   `python3 nabd/serie20/plan.py <datos> <scratch>/cola/cola-nabd`. Si "hoy" está vacío, termina con un resumen de una línea (pendientes y próximos).
3. Por cada episodio de hoy: carpeta `nabd/serie20/episodios/<carpeta>/` (p. ej. `serie20-nvda-2026-11-17`); copia ahí `<datos>/<TICKER>/datos.json`.
   Lee `datos.json` (sobre todo `ultimo` y `trimestres`). Busca en la prensa del día de resultados (WebSearch y el agente web-fetch: nota de
   prensa de la empresa en su web de inversores, Reuters, CNBC, AP, Yahoo Finance) qué explicó los números (segmentos, cargos extraordinarios)
   y la guía de la empresa para el próximo trimestre o el año. Escribe `video.json` como los ejemplos:
   - `voz`: 7 locuciones en árabe estándar, números en palabras, **330-400 palabras en total** (Azure ~110 palabras/min: 3:00-3:40). Las cifras
     que se dicen son las de pantalla (`datos.json`, redondeadas igual); lo que venga de la prensa se atribuye («حسب بيان الشركة»…).
     Si la prensa y TradingView difieren, se dice la de TradingView en pantalla y se aclara.
   - `expectativas.items` (0-2 filas extra, `[título, texto]`): guía de la empresa u otro dato de prensa, con `expectativas.fuente` (medio y fecha).
     Las filas de estimaciones y sorpresa las pone `make_episodio.py` desde `datos.json`. Si no encuentras fuente, no añadas filas.
   - `info` (título ≤ 100 caracteres, resumen, fuentes, hashtags, `x` ≤ 200 caracteres, tags), `claves` (3), `miniatura` (cifra en dígitos
     latinos y $, p. ej. "$15.2B"), `titular`, `sector`, `trimestre` ("الربع الثالث 2026", según el periodo fiscal de `datos.json`).
   Hechos, opiniones y escenarios separados. Nada de comprar/vender, precio objetivo ni «barata/cara». Las ratios no son juicio de halal/haram.
4. Voz: sube los `video.json` a la rama `claude/nabd-serie20-<fecha de hoy>` (desde main) y lanza `voz-Nabd.yml` en esa rama con
   modo=generar y fecha=`nabd/serie20/episodios/<carpeta1>,nabd/serie20/episodios/<carpeta2>,...` (una sola ejecución para todos: la rama
   `voz-nabd` se reescribe en cada ejecución). Espera (2-4 min) y clona `voz-nabd`: `VOZ_DIR=<clon>/<carpeta>`. Si falla, sigue con Piper y dilo.
5. `AUD=<scratch> python3 nabd/serie20/make_episodio.py <carpeta> preview` y mira TODOS los PNG (textos cortados, solapes, cifras que no
   cuadren con la locución); luego sin preview con `VOZ_DIR`; después `python3 nabd/serie20/meta_episodio.py <carpeta>`.
   Si el control de calidad o la duración fallan, corrige la causa (acorta la locución y vuelve a generar la voz); no lo saltes.
6. `SCRATCH=<scratch> bash nabd/serie20/encolar.sh <carpeta>` (uno detrás de otro). Espera el enlace de YouTube.
7. Copia el mp4, la miniatura, el meta y el guion a `/mnt/project-files/nabd-serie-20/<carpeta>/`. Commit de `video.json` (no del mp4 ni de
   datos.json) en la rama del día y abre PR.
8. Resumen corto en español: enlaces de YouTube, duración, voz, qué queda pendiente para los próximos días y cualquier fallo.
