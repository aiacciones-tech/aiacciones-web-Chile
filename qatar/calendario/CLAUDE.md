# Qatar AI Stocks · Short semanal «تقويم النتائج الأسبوعي» (calendario semanal de resultados)

Pedido por Daniel el 22-nov-2026. Estas instrucciones prevalecen sobre el texto de la tarea programada donde difieran.

## Formato
- Short vertical 9:16, 45-59 s, todo en árabe. Voz: la del canal (Piper `ar_JO-kareem-medium`, `../diario/comun.py`).
- Se publica cada **sábado entre las 20:00 y las 21:00 de Doha** (antes de que abra la QSE el domingo). Semana cubierta: domingo a viernes siguientes.
- 5 a 7 empresas, en orden cronológico: primero las de la **Bolsa de Qatar** (domingo a jueves), después las grandes de **EE. UU.** (lunes a viernes).
- Por empresa (6-8 s, `MINEMP`): nombre en árabe y ticker, día (y antes/después de la sesión si está confirmado), consenso de BPA e ingresos.
- Gancho (~3-4 s): «هذا الأسبوع تعلن [la más importante]، و[N] شركات أخرى». Cierre: «تابع القناة لتحليل كل تقرير».
- Si hay empresas de EE. UU., el cierre y los textos recomiendan el canal **نبض وول ستريت** (https://www.youtube.com/@NabdWallStreet) (regla de Daniel).
- Aviso en pantalla y en los textos: «محتوى معلوماتي، وليس توصية استثمارية».
- Si ninguna empresa de la QSE reporta, se dice en pantalla (nota del gancho) y se rellena con EE. UU. Nunca se inventa una fecha o una cifra.

## Datos (verificar en la web; no inventar)
- QSE: las búsquedas en árabe encuentran lo que las inglesas no (الراية raya.com «تفصح عن النتائج»، أرقام argaam.com، CNBC عربية، qe.com.qa).
  Temporadas: resultados anuales a finales de enero-febrero; trimestrales en abril, julio y octubre.
- EE. UU.: fecha y hora en el comunicado de la empresa (investor relations / PR Newswire / Business Wire) o en dos calendarios coincidentes.
  Consenso: Earnings Whispers (finviz.com/news reproduce sus previas), Zacks, Barchart, TheStreet/TipRanks, Nasdaq. Prefiere las previas más recientes.
- Regla de cifras: si dos fuentes discrepan un poco, usa la más reciente o redondea («نحو 6.6 دولار»); si discrepan mucho o solo hay una dudosa, quita la cifra.
  Si falta un dato, se quita del guion (la escena muestra solo lo que hay).
- `fuente` de `calendario.json` nombra las fuentes y la fecha de consulta.

## Pasos de cada sábado
1. Investiga la semana siguiente (domingo-viernes). Elige 5-7 empresas: todas las relevantes de la QSE + las mayores de EE. UU. por capitalización/interés.
2. Copia `semanas/2026-11-22/calendario.json` a `semanas/<domingo AAAA-MM-DD>/calendario.json` y cambia `semana`, `cabecera`, `out`
   (`short-calendario-<semana>-qatar.mp4`), `fuente` y las escenas. La voz lee números en palabras; la pantalla, con dígitos.
   `mercado`: «بورصة قطر» o «وول ستريت · ناسداك/نيويورك» (gen_meta usa esa palabra para decidir si recomienda @NabdWallStreet).
3. `AUD=<scratch> python3 make_calendario.py semanas/<semana>/calendario.json preview` y revisa los PNG; luego sin `preview` (máx. 59 s; si se pasa, acorta la voz o quita una empresa).
4. `python3 gen_meta_calendario.py semanas/<semana>` → meta del Short, posts (X, Threads, TikTok, Instagram, Telegram) y guion, todos `-<semana>-qatar`.
5. Copia la carpeta a `/mnt/project-files/qatar-ai-stocks/calendario/<semana>/`.
6. Entre las 20:00 y las 21:00 de Doha: `SCRATCH=<scratch> bash encolar.sh semanas/<semana>` (sube el Short y publica en las redes).
7. Mensaje en el hilo «Crear calendario semanal de resultados» con el enlace del Short y las empresas.

Dependencias: `pip install piper-tts "matplotlib>=3.11" imageio-ffmpeg pillow numpy arabic-reshaper python-bidi`.
