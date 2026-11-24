# Vídeos evergreen de búsqueda «دليل المستثمر في السوق السعودية» de Saudi Arabia AI Stocks: instrucciones (Daniel, 24-nov-2026)

Vídeos en árabe que responden a lo que la gente busca en YouTube sobre la bolsa saudí (cómo invertir, dividendos, Nomu, OPVs, TASI...),
para atraer tráfico de búsqueda durante meses. **Dos por semana: martes y viernes** (elección de Daniel). Plan de 12 temas en `plan-saudi.json`
(temas y palabras clave sacados de las sugerencias de búsqueda de YouTube con gl=SA). Valen las reglas del canal: archivos entregados en
inglés y terminados en `-saudi`; contenido en árabe; cada post enlaza https://www.youtube.com/@SaudiArabiaAIStocks; LinkedIn lleva el Short
como vídeo nativo con 3-4 datos + conclusión y «فيديو من إعداد قناة Saudi Arabia AI Stocks»; Facebook con el enlace al canal; Instagram como Reel.

## Reglas de contenido
- Educación, no recomendación: nada de «اشترِ», precios objetivo ni «أفضل سهم» como consejo. En listas (p. ej. dividendos) son datos con
  fuente y fecha, no una selección. `make_guia.py` rechaza algunas palabras.
- Cada dato (horarios, límites, normas, cifras de empresas) con fuente oficial (CMA, Saudi Exchange, la empresa) o dos fuentes que coincidan;
  si no se confirma, fuera. Las normas cambian: el aviso final dice que los datos son a la fecha del vídeo.
- Excluidos: zakat y «الأسهم النقية» (cuestiones religiosas) y tutoriales de apps de bancos o brókers concretos (se dice «شركة وساطة مرخصة»).
- Locución: cifras en palabras, nombres latinos en letras árabes («ساودي أرابيا إيه آي ستوكس», «تريدينغ فيو»).
- Título de YouTube = la pregunta que la gente escribe (campo `palabra_clave`) + promesa clara; sin año si el contenido no caduca.

## Piezas (saudi/evergreen/, reutiliza voz y render de saudi/educativo/)
- `guias/<base>/video.json`: base (`eg-NN-<tema>`), numero, tema, tema_corto, palabra_clave, simbolo opcional (p. ej. `TADAWUL:TASI` con
  velas_n 6000 = desde 2002), ultima_vela, escenas, short, info, miniatura. Ejemplo completo: `guias/eg-01-how-to-invest/`.
  Escenas: `portada` (etiqueta, sub, indice ≤5), `puntos` (≤5 [título, texto], fuente), `tabla` (columnas, anchos, filas ≤7, resaltar, fuente),
  `historico` (línea semanal de muchos años con marcas {fecha, campo h|l|c, texto, dx, dy}), `grafico` (velas diarias), `fin` (claves ≤4, siguiente).
  Short: `titulo` (pregunta), `tarjeta` (titulo, lineas ≤5), `historico` (grafico: id de la escena larga), `fin`; < 59 s (~75-90 palabras).
- `.github/workflows/evergreen-saudi.yml`: al subir `video.json` a una rama `claude/**`, velas (si hay simbolo) y voz Azure frase a frase
  en `<base>/` de la rama `voz-saudi-evergreen`.
- `make_guia.py <carpeta> [preview]`, `make_short_guia.py <carpeta> [preview]` (con `AUD`, `VELAS`, `VOZ_DIR`), `meta_guia.py <carpeta>`.
- `encolar.sh <carpeta>`: `cola-sa/guide-<base>/` y `-short/` en `youtube-cola`; desde ahí todo se publica solo.

## Pasos de cada guía (martes y viernes)
1. Primera guía `pendiente` de `plan-saudi.json`. Verifica los datos en la web (fuentes oficiales) y escribe `guias/<base>/video.json`
   (~800-850 palabras ≈ 6:30-7:00 con Azure; el Short ~75).
2. Preview: `AUD=<scratch> VELAS=<velas.json> python3 saudi/evergreen/make_guia.py <carpeta> preview` (y el Short); mira TODOS los PNG.
3. Commit y push a `claude/saudi-evergreen-<fecha>` → `evergreen-saudi.yml` (2-4 min). `git clone -q --depth 1 -b voz-saudi-evergreen <repo> <scratch>/voz`.
4. Render con `VOZ_DIR=<scratch>/voz/<base>` y `VELAS=<scratch>/voz/<base>/velas.json`; `meta_guia.py`.
5. `SCRATCH=<scratch> bash saudi/evergreen/encolar.sh <carpeta>`; copia mp4, Short, miniatura, metadatos, guion y posts a
   `/mnt/project-files/saudi-evergreen/<base>/`.
6. Marca la guía `publicada` (IDs) en `plan-saudi.json`, añade la entrada a `saudi/crecimiento/mejoras-saudi.json`
   (`{"tipo": "evergreen", "video": "<id>", "desde": "<fecha>", "nota": "<palabra_clave>"}`, lo lee el informe semanal) y abre o actualiza el PR.
