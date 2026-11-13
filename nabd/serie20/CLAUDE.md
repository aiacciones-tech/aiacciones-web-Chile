# Serie «عمالقة وول ستريت» de Nabd Wall Street: instrucciones de la rutina diaria (Daniel, 13-nov-2026)

Un episodio en árabe por empresa **después de cada informe de resultados**, a partir del trimestre en curso (eventos desde el 1-oct-2026),
de las 20 empresas: NVDA, MSFT, AAPL, GOOGL, AMZN, META, AVGO, TSLA, BRK, JPM, LLY, WMT, ORCL, V, MA, XOM, NFLX, COST, JNJ, PLTR.
Reglas de Daniel: **máximo 4 minutos** por vídeo; **máximo 3 vídeos de la serie al día** (si coinciden más, pasan a los días siguientes;
`plan.py` lo reparte); sin pasos manuales; todo lo que se entrega termina en `-Nabd`. Presentación de la serie: https://www.youtube.com/watch?v=hU3GozeSL_U
El vídeo diario (nabd/diario/, 8-10 min) es otra cosa y no cambia.

## Piezas
- `datos_sec.py` + `.github/workflows/serie20-datos-Nabd.yml` (11:00 y 23:30 UTC, o a mano): rama `datos-serie20-nabd` con `calendario.json`
  (último evento de resultados de cada empresa en la SEC y próximas fechas de TradingView) y `<TICKER>/sec.json` (series trimestrales XBRL,
  balance, capitalización) y `<TICKER>/comunicado-<fecha>.txt` (texto del EX-99.1 del 8-K, con su URL en la primera línea).
- `plan.py <datos> <cola-nabd>`: los episodios de hoy (0-3) y los pendientes.
- `make_episodio.py <carpeta> [preview]`: 7 escenas, 1920x1080, voz Azure con `VOZ_DIR` (Piper si falta), control de calidad, 120-240 s.
- `meta_episodio.py <carpeta>`: meta de YouTube, post de Telegram y de X, miniatura. Sin Short.
- `encolar.sh <carpeta>`: cola-nabd/serie20-<ticker>-<fecha>/ en youtube-cola; youtube-Nabd.yml sube, telegram-Nabd.yml y buffer-Nabd.yml (X) publican.
- Ejemplo de `video.json`: `episodios/ejemplo/video.json`.

## Pasos de cada día
1. Lanza `serie20-datos-Nabd.yml` (workflow_dispatch en main) y espera a que termine (2-5 min); clona la rama `datos-serie20-nabd` (--depth 1).
2. Clona `cola-nabd/` de `youtube-cola` (no hagas `git fetch` de toda la rama, es enorme): `git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola
   https://github.com/aiacciones-tech/aiacciones-web-Chile.git <scratch>/cola && cd <scratch>/cola && git sparse-checkout set cola-nabd`.
   `python3 nabd/serie20/plan.py <datos> <scratch>/cola/cola-nabd`. Si "hoy" está vacío, termina con un resumen de una línea (pendientes y próximos).
3. Por cada episodio de hoy: carpeta `nabd/serie20/episodios/<carpeta>/` (p. ej. `serie20-nvda-2026-11-19`); copia ahí `<datos>/<TICKER>/sec.json`.
   Lee el comunicado (`comunicado-<fecha>.txt`) y `sec.json`. Busca en la prensa del día de resultados o posterior (Reuters, CNBC, Yahoo Finance,
   AP, MarketWatch, la web de relación con inversores) las expectativas de los analistas (consenso LSEG/FactSet de ingresos y BPA) y la guía de la
   empresa. Escribe `video.json` como en el ejemplo:
   - `kpis` (3-4): cifras del comunicado del trimestre (ingresos, beneficio neto o BPA diluido, margen, dato propio del negocio) con su variación
     interanual (محسوب si la calculas tú). `fuente_kpis` dice de dónde sale cada una.
   - `trimestres_nuevos`: si el trimestre recién publicado aún no está en `sec.json` (el 10-Q suele llegar días después del 8-K), añádelo con
     `fin` (fecha de cierre del trimestre), `ingresos`, `beneficio_neto` (en dólares, sin redondear) y `fuente` (URL del comunicado). Nada más.
     `balance_nuevo` igual, solo si el comunicado trae el balance y es más reciente que el de `sec.json`.
   - `expectativas.items` (2-4 filas): frente al consenso (con el nombre del medio y la fecha) y la guía de la empresa. Si no encuentras una fuente
     publicada, dilo («لم نجد تقديرًا منشورًا للمحللين») en vez de inventar.
   - `voz`: 7 locuciones en árabe estándar, números en palabras, **330-400 palabras en total** (Azure ~110 palabras/min: 3:00-3:40).
     La locución repite las cifras de pantalla; los ratios de deuda/caja frente a la capitalización salen en pantalla calculados: no los inventes.
   - `info` (título ≤ 100 caracteres, resumen, fuentes, hashtags, texto de X ≤ 200 caracteres), `claves` (3), `miniatura`.
   Hechos, opiniones y escenarios separados. Nada de comprar/vender, precio objetivo ni «barata/cara». Las ratios no son juicio de halal/haram.
4. Voz: sube los `video.json` a la rama `claude/nabd-serie20-<fecha de hoy>` (desde main) y lanza `voz-Nabd.yml` en esa rama con
   modo=generar y fecha=`nabd/serie20/episodios/<carpeta1>,nabd/serie20/episodios/<carpeta2>,...` (una sola ejecución para todos: la rama
   `voz-nabd` se reescribe en cada ejecución). Espera (2-4 min) y clona `voz-nabd`: `VOZ_DIR=<clon>/<carpeta>`. Si falla, sigue con Piper y dilo.
5. `AUD=<scratch> python3 nabd/serie20/make_episodio.py <carpeta> preview` y mira TODOS los PNG (textos cortados, solapes, cifras que no
   cuadren con la locución); luego sin preview con `VOZ_DIR`; después `python3 nabd/serie20/meta_episodio.py <carpeta>`.
   Si el control de calidad o la duración fallan, corrige la causa (acorta la locución y vuelve a generar la voz); no lo saltes.
6. `SCRATCH=<scratch> bash nabd/serie20/encolar.sh <carpeta>` (uno detrás de otro). Espera el enlace de YouTube.
7. Copia el mp4, la miniatura, el meta y el guion a `/mnt/project-files/nabd-serie-20/<carpeta>/`. Commit de `video.json` (no del mp4 ni de
   sec.json) en la rama del día y abre PR.
8. Resumen corto en español: enlaces de YouTube, duración, voz, qué queda pendiente para los próximos días y cualquier fallo.
