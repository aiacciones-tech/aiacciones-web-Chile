# Directo semanal «El IBEX de la semana, en directo» de @AIAccionesEspaña (Daniel, 24-nov-2026)

Cada **viernes a las 17:45 de Madrid**, 15-20 minutos. Lo emite **Daniel** (OBS o el móvil) desde YouTube; nosotros le preparamos las
diapositivas y el guion. Primer directo: viernes 27-nov-2026 (Daniel pidió activar los directos en el canal el 24-nov; tarda ~24 h).
Si un viernes no hay sesión (festivo nacional en la Bolsa de Madrid), no hay directo: avisa a Daniel el jueves.

## Piezas
- `make_slides.py <mercado.json> <semana.json> <salida>`: 8 diapositivas 1920x1080 (portada, IBEX 35 de la semana día a día, mejor y peor
  semana de los 35 valores, fuera de España, noticias, gráfico de seis meses con medias de 50 y 200, agenda, preguntas), un PDF con todas
  y `guion-<fecha>.md` con los puntos que decir en cada una. Variaciones de la semana: calculadas frente al cierre del viernes anterior
  (Yahoo Finance; TradingView si Yahoo aún no tiene la vela del día). Contexto internacional: variación semanal de TradingView.
- `semana.json` (lo escribe Claude cada viernes, ver `ejemplo-semana.json`): `noticias` (≤5 [título, texto, fuente]), `agenda`
  (≤5 [día, cita, fuente]) y `notas` ({ibex, valores, mercados, tecnico}: frases extra para el guion, con fuente). Nada sin fuente publicada.
  Noticias: hechos relevantes de la CNMV (espana/datos/hechos.json), resultados, dividendos y prensa (EFE, Expansión, Cinco Días…).
  Agenda: calendario semanal (espana/semanal/), espana/dividendos.py, BCE/Fed si toca.

## Pasos de cada viernes (tarea programada, 16:41 Madrid)
1. `git pull` de main. Lanza `datos-diario-espana.yml` (workflow_dispatch en main) y espera a que acabe; baja `datos/mercado-<hoy>.json`
   de la rama `datos-diario-es`. Datos de las ~16:45: es la versión **provisional** (sesión aún abierta).
2. Escribe `/mnt/project-files/espana/directo/<fecha>/semana.json` con noticias, agenda y notas verificadas.
3. `python3 espana/directo/make_slides.py <mercado.json> <semana.json> /mnt/project-files/espana/directo/<fecha>/`; mira los PNG.
4. Publica en el hilo, hacia las 17:00, un mensaje corto con el PDF y el guion adjuntos («provisional, con datos de las 16:45»).
5. Programa con send_later un aviso a las 17:37 Madrid: relanza `datos-diario-espana.yml` (cierre a las 17:35), rehaz las diapositivas
   y publica en el hilo la **versión de cierre** (PDF y guion) antes de las 17:45. Si a las 17:43 no está, dilo: Daniel usa la provisional.
6. Contenido: hechos y datos, nunca recomendaciones, previsiones ni precios objetivo; la situación técnica como condiciones.
