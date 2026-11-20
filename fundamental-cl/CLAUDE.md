# Serie semanal «Análisis fundamental en simple» de AIAcciones Chile: instrucciones (Daniel, 20-nov-2026)

Videos educativos en español, **un concepto de análisis fundamental por video**, explicado sobre las **cifras reales** de una empresa del IPSA.
Unos 6 minutos, con subtítulos (quemados y `.srt`), miniatura y Short. Misma voz y marca que el canal @aiaccioneschile: voz Azure
`es-CL-LorenzoNeural` (`voz-cl/`, Piper solo de respaldo y nunca mezclado), colores del diario IPSA y logo AIAcciones Chile.
**Un capítulo cada domingo, ~10:00 de Santiago** (no choca con el diario IPSA, lunes a viernes 18:41, ni con la rutina de resultados de las 23:00).
Empieza el **domingo 6-dic-2026**, primer domingo tras la temporada de resultados 3T26. Daniel pidió que los capítulos se publiquen solos
(tarea programada semanal) y que se le avise en el hilo «Crear serie educativa semanal» cuando quede publicado el **último** capítulo (el 10).
Port en español de `qatar/fundamental/` (mismas escenas, de izquierda a derecha). Referencia técnica: la serie alemana `ge/educativo/` (PR #184).

Plan de 10 temas en `plan.json` (empresa sugerida; se puede cambiar si otra enseña mejor el concepto o tiene resultados más recientes, y entonces
se corrige el «Próximo capítulo» del capítulo anterior solo si aún no se publicó):
1 ingresos y utilidad (SQM-B) · 2 márgenes (CCU) · 3 precio/utilidad (Banco de Chile) · 4 deuda (Enel Chile) · 5 flujo de caja (CMPC) ·
6 dividendos (Santander Chile) · 7 ROE y ROA (Bci) · 8 balance (Falabella) · 9 valoración P/VL y EV/EBITDA (Copec) · 10 todo junto (Falabella vs. Cencosud).

## Reglas de contenido
- Educación, nunca recomendación (NCG 502): nada de comprar/vender, precio objetivo, «barata/cara» ni «oportunidad». La empresa es «solo un ejemplo».
  `make_capitulo.py` para si la locución lleva esas palabras (si una es inocua, va en `"permitir"` de la escena).
- **Toda cifra sale de un informe oficial** (estados financieros, comunicado de resultados de la empresa, CMF) **o de TradingView** (`datos.json`),
  y la de pantalla coincide con la de la voz. Lo de la prensa, atribuido. Cálculos propios «calculado». Cada escena lleva `fuente`.
- TradingView normaliza las cuentas: en pantalla manda el informe oficial; TradingView sirve para series de varios años (dilo: «según TradingView»).
  En el escáner, `BCS:<TICKER>` da cifras en CLP salvo `fundamental_currency_code` (SQM reporta en USD: usa `NYSE:SQM` para la serie en dólares).
- Bancos: no hay «costo de ventas»; los ingresos son el margen de intereses + comisiones + otros.
- Voz: números en palabras (dos mil ciento doce millones); en pantalla, formato chileno (2.112,0). Repite en una frase el capítulo anterior
  y anuncia el siguiente con su fecha.
- Todo lleva enlace a aiacciones.cl y al canal (reglas de Daniel); LinkedIn = el Short como video, con resumen y mención de AIAcciones Chile.
  La campaña de comentarios (`diario/campana.py`, hasta el 22-nov-2026) se decide por la fecha `publicar` del capítulo: ya no aplica a la serie.

## Piezas
- `capitulos/<base>/video.json`: base, capitulo_n, simbolo (TradingView), simbolos_extra, documentos, ticker, nombre, tema, publicar (AAAA-MM-DD),
  fuente_general, escenas, info (titulo, titulo_short ≤100, resumen, fuentes, x, linkedin {datos 3-4, conclusion}, hashtags, hashtags_short, tags), miniatura.
  Escenas (`tipo`): portada (sub) · puntos (≤5 [título, texto]) · cuenta (columnas, filas [{t, v, tipo ingreso|resta|suma|sub|final, sin_var}], nota) ·
  cascada (pasos [{t, v, tipo total|resta|suma}], nota) · barras (categorias, series [{nombre, valores, color}], nota; negativos en naranja) ·
  kpis (items ≤4 {big, label, sub, color}) · formula (formula, ejemplo [[texto, resultado]] ≤3, nota) · fin (claves ≤4, siguiente).
  `capitulo` en una escena = capítulo de YouTube y tramo de la barra de progreso. Ejemplo completo: `capitulos/fundamental-01-sqm/`.
- `capitulos/<base>/short.json`: el Short con `../diario/make_short.py` (escenas titulo, cifra, kpis, fin; <59 s). `out` = `short-<base>-<publicar>.mp4`
  (la fecha en el nombre apaga la campaña de comentarios del diario).
- `.github/workflows/datos-fundamental-cl.yml`: al subir `video.json` a una rama `claude/**` pide a TradingView las cifras (`datos_fundamental.py`, ~5 min,
  se congelan) y baja los `documentos` (PDF o web → texto) a `<base>/` de la rama `datos-fundamental-cl`. ir.sqm.com responde 403 también a Actions:
  si los PDF no bajan, lee el informe con el agente web-fetch (WebFetch sí abre ir.sqm.com y la prensa) y anota la URL en `fuentes`.
- `comun_fund.py`: marca, `frases()` (subtítulos), `voz_frases()` (un wav Azure por frase desde `VOZ_DIR`; si falta uno, para), render y srt.
  `python3 comun_fund.py frases <video.json> > frases.txt` = fuente para `voz-cl/pedir.sh`.
- `make_capitulo.py <carpeta> [preview]` (con `AUD`, `VOZ_DIR`): 5:00-7:30, control de calidad; escribe `<base>.mp4`, `subtitulos-<base>.srt`, times.json y guion.
- `meta_capitulo.py <carpeta>`: meta de YouTube (video y Short), posts de X, LinkedIn, TikTok y Telegram, miniatura.
- `encolar.sh <carpeta>`: `cola/<base>/` y `cola/<base>-short/` en `youtube-cola` (youtube.yml, buffer.yml, telegram-chile.yml). Límite ~10 subidas/24 h compartido.

## Pasos de cada domingo (tarea programada)
0. Capítulo del día = el de `plan.json` con `fecha` de hoy (hora de Chile). Si su carpeta de `/mnt/project-files/serie-fundamental/<base>/` ya tiene
   `listo.txt` (preparado antes, como el capítulo 1), salta al paso 5.
1. Busca el último informe oficial de la empresa (estados financieros y comunicado del último trimestre; web de inversionistas, CMF) y léelo.
2. Crea `capitulos/<base>/video.json` con simbolo, documentos y `"escenas": []`; súbelo a la rama de trabajo `claude/...` y espera el workflow;
   `git fetch origin datos-fundamental-cl` y lee `git show FETCH_HEAD:<base>/datos.json` y `docs/*.txt`.
3. Guion: **~1.100 palabras ≈ 6 min** con Lorenzo (calibrado en el capítulo 1: 973 palabras dieron 5:15). `AUD=<scratch> python3 make_capitulo.py <carpeta> preview` y mira
   TODOS los PNG (nada cortado ni solapado con el subtítulo, la fuente o el logo), igual con el Short (`make_short.py ... preview`).
4. Voz: `python3 comun_fund.py frases <carpeta>/video.json > <scratch>/frases.txt`; `bash voz-cl/pedir.sh fund-<nn>-<empresa> <scratch>/voz <scratch>/frases.txt <carpeta>/short.json`;
   render con `VOZ_DIR=<scratch>/voz` (video) y `PYTHONPATH=<repo>/voz-cl/shim VOZ_DIR=<scratch>/voz` (Short); `meta_capitulo.py`.
5. Copia mp4, Short, miniatura, srt, guion, meta y posts a `/mnt/project-files/serie-fundamental/<base>/`; `SCRATCH=<scratch> bash encolar.sh <carpeta>`;
   commit de los json del capítulo (sin mp4/png) en la rama de trabajo, PR y merge (Daniel: «todo automático»). Mensaje corto en el hilo: enlaces y duración.
6. Si es el capítulo 10 (`"ultimo": true`), avisa a Daniel en el hilo «Crear serie educativa semanal» de que la serie quedó completa, y apaga la tarea.
