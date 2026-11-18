# Serie semanal «التحليل الأساسي ببساطة» (análisis fundamental, fácil) de AI Stocks UAE: instrucciones (Daniel, 18-nov-2026)

Vídeos educativos en árabe, **un concepto de análisis fundamental por vídeo**, explicado sobre las **cifras reales** de una empresa de ADX o DFM.
Unos 6 minutos, con subtítulos (quemados y `.srt`), miniatura y Short. Misma voz y marca que el canal (Piper `ar_JO-kareem-medium`, colores y logo
de `eau/diario/comun.py`). **Un capítulo cada sábado hacia las 18:00 de EAU** (no choca con el diario, lun-vie 16:17, ni con los resultados, días laborables).
Daniel autorizó (18-nov-2026) que, tras el capítulo 1, los siguientes se publiquen solos. Instrucciones en español; lo que ve y oye el público, en árabe.

Plan de 10 temas en `plan.json` (empresa sugerida, se puede cambiar si otra enseña mejor el concepto o tiene resultados más recientes):
1 ingresos y beneficio neto (Emaar) · 2 márgenes (ADNOC Distribution) · 3 PER (e&) · 4 deuda (Aldar) · 5 flujo de caja libre (ADNOC Gas) ·
6 dividendos (DEWA) · 7 ROE (FAB) · 8 balance (Air Arabia) · 9 valoración P/VC y EV/EBITDA (ADNOC Drilling) · 10 todo junto (Emaar frente a Aldar).

## Reglas de contenido
- Educación, nunca recomendación: nada de comprar/vender, precio objetivo, «barata/cara» ni «oportunidad». La empresa es «مجرد مثال للشرح».
  `make_capitulo.py` para si la locución lleva palabras de recomendación.
- **Toda cifra sale de un informe oficial** (cuentas auditadas, resultados trimestrales, nota de prensa de la empresa) **o de TradingView** (`datos.json`),
  y la de pantalla coincide con la de la voz. Lo de la prensa, atribuido («حسب غلف نيوز»). Cálculos propios «محسوب»; porcentajes calculados con las cifras
  completas, no con las redondeadas (en `cuenta`, `v` lleva las cifras exactas en miles de millones y se muestran con 1 decimal).
- TradingView normaliza las cuentas: sus «ingresos» pueden no coincidir con los de la empresa (Emaar 2025: 50,8 frente a 49,6 mil millones de AED).
  En pantalla manda el informe oficial; TradingView sirve para series de varios años, ratios y comprobar. Ojo: en el escáner los campos sin `_h`
  vienen en USD (`fundamental_currency_code`), los históricos `_fy_h` / `_fq_h` en AED.
- Bidi: en texto árabe, porcentajes con «بالمئة» (no «(+40%)»); las líneas de `fuente` empiezan por una palabra árabe; sin comillas «» en pantalla.
- Hasta el 22-nov-2026 el cierre pide comentar y suscribirse (automático por `publicar`, `CTA_*` de `eau/diario/comun.py`).

## Piezas
- `capitulos/<base>/video.json`: base, capitulo_n, simbolo, simbolos_extra, documentos [{id, url}], ticker, nombre, tema, publicar (fecha), fuente_general,
  escenas, info (titulo, titulo_short, resumen, fuentes, x, hashtags, hashtags_short, tags, linkedin {datos 3-4, conclusion}), miniatura (etiqueta, titulo, sub, cifras, pie).
  Escenas (`tipo`): `portada`, `puntos` (≤5 [título, texto]), `cuenta` (columnas, filas [{t, v, tipo ingreso|resta|sub|final|nota, d}], variación calculada),
  `cascada` (pasos [{t, v, tipo total|resta|suma}], de derecha a izquierda), `barras` (categorias, series), `kpis` (≤4 {big, label, sub, color}),
  `formula` (formula, ejemplo [[texto, resultado]]), `fin` (claves ≤4, siguiente). `capitulo` = capítulo de YouTube y tramo de la barra de progreso.
- `.github/workflows/datos-fundamental-eau.yml`: al subir `video.json` a una rama `claude/**` pide a TradingView las cifras (`datos_fundamental.py`, ~3 min,
  se congelan) y descarga los `documentos` (PDF o web → texto, `docs_fundamental.py`) a `<base>/` de la rama `datos-fundamental-eau`.
  El contenedor no llega a dfm.ae, adx.ae, nasdaqdubai ni a TradingView; GitHub Actions sí. Para añadir documentos: edita `documentos` y vuelve a subir.
- `make_capitulo.py <carpeta> [preview]` (con `AUD`): 5:00-7:30, control de calidad; escribe `<base>-UAE.mp4`, `subtitulos-<base>-UAE.srt`, times.json y guion.
- `../diario/make_short.py <carpeta>/short.json`: el Short (<59 s; escenas titulo, kpis, cifra, fin; voz muy corta, Piper es lento).
- `meta_capitulo.py <carpeta>`: meta de YouTube (vídeo y Short), posts de X, Facebook, LinkedIn (Short nativo), TikTok, Instagram y Telegram, miniatura.
- `encolar.sh <carpeta>`: `cola-eau/<base>/` y `<base>-short/` en `youtube-cola` (límite de ~10 subidas/24 h compartido).

## Pasos de cada sábado
1. Siguiente capítulo de `plan.json` que no esté en `/mnt/project-files/aistocksuae/fundamental/`. Busca (WebSearch) el último informe oficial de la empresa
   (cuentas anuales auditadas y, si hay, las últimas trimestrales; feeds.dfm.ae, adx.ae, candidocs.nasdaqdubai.com, web de relación con inversores).
2. Crea `capitulos/<base>/video.json` con simbolo, documentos y `"escenas": []`; súbelo a la rama de trabajo `claude/...` y espera el workflow;
   clona `datos-fundamental-eau` y lee `datos.json` y `docs/*.txt` (busca la cuenta de resultados, el balance o el flujo de caja según el tema).
3. Escribe el guion: **~540 palabras ≈ 6:15** (calibrado: 593 palabras dieron 6:40 con Piper a LENGTH_SCALE 0.8, ~1,6 palabras/s más pausas). Repite el
   concepto del capítulo anterior en una frase y anuncia el siguiente. Números en palabras en la voz; en pantalla, dígitos occidentales.
4. `AUD=<scratch> python3 make_capitulo.py <carpeta> preview` y mira TODOS los PNG (RTL, nada cortado ni solapado con el subtítulo); render; Short (preview y render); `meta_capitulo.py`.
5. Copia mp4, Short, miniatura, srt, guion, meta y posts a `/mnt/project-files/aistocksuae/fundamental/<base>/`; `SCRATCH=<scratch> bash encolar.sh <carpeta>`;
   commit de los json del capítulo (sin mp4/png) en la rama de trabajo. Mensaje corto en el hilo: enlaces, duración y cualquier fallo.
