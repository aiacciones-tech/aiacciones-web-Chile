# Serie semanal «التحليل الأساسي ببساطة» (análisis fundamental, fácil) de Qatar AI Stocks: instrucciones (Daniel, 19-nov-2026)

Vídeos educativos en árabe, **un concepto de análisis fundamental por vídeo**, explicado sobre las **cifras reales** de una empresa de la Bolsa de Qatar (QSE).
Unos 6 minutos, con subtítulos (quemados y `.srt`), miniatura y Short. Misma voz y marca que el canal (Piper `ar_JO-kareem-medium`, colores y logo
de `qatar/diario/comun.py`). **Un capítulo cada sábado hacia las 18:00 de Doha** (no choca con el diario, domingo-jueves 14:15, ni con la rutina
de resultados, en pausa hasta enero). Daniel pidió (19-nov-2026) que, tras el capítulo 1, los siguientes se publiquen solos.
Copia de `eau/fundamental/` (mismo formato y escenas). Instrucciones en español; lo que ve y oye el público, en árabe.

Plan de 10 temas en `plan.json` (empresa sugerida; se puede cambiar si otra enseña mejor el concepto o tiene resultados más recientes):
1 ingresos y beneficio neto (QNB) · 2 márgenes (Baladna; IQ descartada: participadas) · 3 PER (Ooredoo) · 4 deuda (Barwa) · 5 flujo de caja libre (Nakilat) ·
6 dividendos (QEWC) · 7 ROE (QIB) · 8 balance (Woqod) · 9 valoración P/VC y EV/EBITDA (MPHC) · 10 todo junto (QNB frente a QIB).

## Reglas de contenido
- Educación, nunca recomendación: nada de comprar/vender, precio objetivo, «barata/cara» ni «oportunidad». La empresa es «مجرد مثال للشرح».
  `make_capitulo.py` para si la locución lleva palabras de recomendación.
- **Toda cifra sale de un informe oficial** (estados financieros auditados, resultados trimestrales, nota de prensa de la empresa) **o de TradingView**
  (`datos.json`), y la de pantalla coincide con la de la voz. Lo de la prensa, atribuido («حسب ذا بنينسولا»). Cálculos propios «محسوب»; porcentajes
  con las cifras completas (en `cuenta`, `v` lleva las cifras exactas en miles de millones de riyales y se muestran con 1 decimal).
- Bancos (QNB, QIB…): no hay «ventas ni coste de ventas»; los «ingresos» son los ingresos operativos (margen de intereses + comisiones + otros).
- TradingView normaliza las cuentas: en pantalla manda el informe oficial; TradingView sirve para series de varios años, ratios y comprobar.
  En el escáner los campos sin `_h` vienen en USD (`fundamental_currency_code`), los históricos `_fy_h` / `_fq_h` en QAR.
- Bidi: en texto árabe, porcentajes con «بالمئة»; las líneas de `fuente` empiezan por una palabra árabe; sin comillas «» en pantalla.
  Una línea que empieza por siglas latinas (QNB, EPS) se gira a LTR: empieza con una palabra árabe.
- Hasta el 22-nov-2026 el cierre pide comentar y suscribirse (automático por la fecha `publicar`, `CTA_*` de `qatar/diario/comun.py`).
- Todo archivo entregado termina en `-qatar` y todo post lleva el enlace al canal (reglas de Daniel). Facebook cerró: Threads en su lugar.

## Piezas
- `capitulos/<base>/video.json`: igual que en `eau/fundamental/CLAUDE.md` (escenas portada, puntos, cuenta, cascada, barras, kpis, formula, fin),
  más `info.pregunta` opcional para el post de Threads.
- `.github/workflows/datos-fundamental-qatar.yml`: al subir `video.json` a una rama `claude/**` pide a TradingView las cifras (`datos_fundamental.py`, ~3 min,
  se congelan) y descarga los `documentos` (PDF o web → texto, `docs_fundamental.py`) a `<base>/` de la rama `datos-fundamental-qatar`.
  El contenedor no llega a qnb.com, qse.com.qa ni a TradingView; GitHub Actions llega a TradingView, pero qnb.com (y sus espejos mob./jobs.)
  le responde 403. Si los PDF oficiales no bajan: cifras clave del comunicado de la empresa (el agente web-fetch sí lee mob.qnb.com y la prensa)
  y desglose de la cuenta de resultados de stockanalysis.com/quote/qse/<TICKER>/financials/income-statement/ (agente web-fetch), atribuido
  («ستوك أناليسس») y cuadrado con el beneficio y el BPA oficiales. TradingView no da las líneas de banco (margen de intereses, provisiones).
- `make_capitulo.py <carpeta> [preview]` (con `AUD`): 5:00-7:30, control de calidad; escribe `<base>-qatar.mp4`, `subtitulos-<base>-qatar.srt`, times.json y guion.
- `../diario/make_short.py <carpeta>/short.json`: el Short (<59 s; escenas titulo, kpis, cifra, fin). `out`: `short-<base>-qatar.mp4`.
- `meta_capitulo.py <carpeta>`: meta de YouTube (vídeo y Short), posts de X, Threads, LinkedIn (Short nativo), TikTok, Instagram y Telegram, miniatura.
- `encolar.sh <carpeta>`: `cola-qa/<base>/` y `<base>-short/` en `youtube-cola` (límite de ~10 subidas/24 h compartido con el diario).

## Pasos de cada sábado
1. Siguiente capítulo de `plan.json` que no esté en `/mnt/project-files/qatar-ai-stocks/fundamental/`. Busca (WebSearch, también en árabe) el último
   informe oficial de la empresa (estados auditados anuales y las últimas trimestrales; qse.com.qa, web de relación con inversores).
2. Crea `capitulos/<base>/video.json` con simbolo, documentos y `"escenas": []`; súbelo a una rama `claude/...` y espera el workflow;
   `git fetch origin datos-fundamental-qatar` (clon de una rama: lee con `git show FETCH_HEAD:<base>/datos.json`) y lee `docs/*.txt`.
3. Guion: **~540 palabras ≈ 6:15** (Piper a LENGTH_SCALE 0.8, ~1,6 palabras/s más pausas). Repite el concepto del capítulo anterior en una frase y
   anuncia el siguiente. Números en palabras en la voz; en pantalla, dígitos occidentales.
4. `AUD=<scratch> python3 make_capitulo.py <carpeta> preview` y mira TODOS los PNG (RTL, nada cortado ni solapado con el subtítulo); render; Short; `meta_capitulo.py`.
5. Copia mp4, Short, miniatura, srt, guion, meta y posts a `/mnt/project-files/qatar-ai-stocks/fundamental/<base>/`; `SCRATCH=<scratch> bash encolar.sh <carpeta>`;
   commit de los json del capítulo (sin mp4/png) en la rama de trabajo y PR. Mensaje corto en el hilo: enlaces, duración y cualquier fallo.
