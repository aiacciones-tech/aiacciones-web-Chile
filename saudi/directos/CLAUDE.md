# Directos en momentos clave de Saudi Arabia AI Stocks: instrucciones (Daniel, 24-nov-2026)

Daniel eligió el **directo automático**: el vídeo se prepara como siempre (datos verificados, voz Azure, gráficos) y GitHub Actions lo emite
como **directo real** de YouTube a la hora fijada (YouTube no permite crear Estrenos por la API). La emisión se anuncia antes (página
"Próximamente", chat en vivo, recordatorios) y queda guardada en el canal. Valen las reglas del canal: contenido en árabe, archivos en inglés
terminados en `-saudi`, cada post enlaza https://www.youtube.com/@SaudiArabiaAIStocks, nada inventado (dato sin fuente = fuera).

## Eventos (eventos-saudi.json)
- **Fed** (decisión 14:00 Washington = 22:00 Riad): directo a las 23:00 Riad.
- **OPEP+** (reunión ministerial; el comunicado sale a media tarde): directo ~2 h después del comunicado.
- **Presupuesto saudí** (diciembre; día por confirmar en mof.gov.sa): directo la misma noche.
- **Resultados anuales** de Aramco, Al Rajhi, SNB, SABIC, stc y Ma'aden (ene-mar; fechas en `calendar-FY26-saudi.json` de
  /mnt/project-files/saudi-pipeline/): directo la misma noche o al día siguiente antes de la apertura (09:30 Riad).
Máximo **un directo por día** y nunca a la vez que otro; no hace falta más de 2-3 al mes.

## Pasos de cada directo
1. Espera a que el dato sea **público** (comunicado de la Fed/OPEP, nota de la compañía en Tadawul) y recógelo de 2 fuentes
   (Fed/opec.org/Tadawul + Reuters, CNBC, Argaam, Arab News…). Sin previsiones, precios objetivo ni recomendaciones.
2. Escribe `eventos/<base>/video.json` (copia `eventos/ejemplo-presupuesto-2027/`): `base` (p. ej. `fed-2026-12-09`), `evento`, `titulo`,
   `fecha_ar`, `inicio` (UTC, ISO con Z), `escenas`, `info` (titulo ≤100 con «🔴 بث مباشر:», resumen, lineas, fuentes con url, hashtags, tags, x),
   `miniatura` (linea1, linea2). Escenas: `portada` primero y `fin` al final; en medio `cifras` (≤4 {valor, etiqueta, color}, `fuente`),
   `puntos` (≤5 [título, texto]), `linea` (series {nombre, fechas, valores}, `fuente`, `unidad`). Cada escena con `voz` y `capitulo`.
   **8-12 min de contenido** (`make_directo.py` exige 420-780 s): con Azure, unas 850-1.200 palabras. Cifras en palabras en la locución.
   Estructura típica: portada · qué se decidió (cifras) · contexto (linea) · reacción del mercado (cifras/linea) · qué significa para el riyal/SAMA,
   bancos, Aramco y TASI (puntos, como hechos y condiciones) · qué vigilar después (puntos) · fin.
3. Push del `video.json` a tu rama `claude/...`: `directo-voz-saudi.yml` deja la voz en `<base>/` de la rama `voz-saudi-directo` (~3 min).
4. `git clone -q --depth 1 -b voz-saudi-directo https://github.com/aiacciones-tech/aiacciones-web-Chile.git <scratch>/voz` y
   `AUD=<scratch>/aud VOZ_DIR=<scratch>/voz/<base> python3 make_directo.py eventos/<base>` (antes, `... preview` para ver las escenas en PNG).
   El vídeo empieza con **60 s de cuenta atrás** (sin voz) mientras entra la audiencia.
5. `python3 meta_directo.py eventos/<base>` (directo.json con capítulos, posts de anuncio X/Threads/Facebook/Telegram, miniatura 1280x720).
6. `bash encolar.sh eventos/<base>` **al menos 30 min antes** del inicio (mejor 1-3 h): `directo-saudi.yml` crea la emisión, pone la miniatura,
   escribe `resultado.json` (anuncia el directo en Buffer y Telegram) y, como empieza en menos de 5,5 h, espera y emite. El script imprime el enlace.
7. Mira el run "Directos (Arabia Saudita)" en Actions. Tras el directo, `cola-sa/directo-<base>/estado.json` dice `emitido`.
   Añade el directo al registro del informe semanal: `saudi/crecimiento/mejoras-saudi.json` →
   `{"tipo": "directo", "video": "<videoId>", "desde": "AAAA-MM-DD", "nota": "<evento>"}`.
8. Resume a Daniel: enlace, hora, duración, fuentes. Copia los archivos a /mnt/project-files/saudi-directos/<base>/.

## Notas técnicas
- `scripts/directo-saudi.py`: `verificar` (permiso del token: el de subida ya tiene `youtube`; y si el canal puede emitir),
  `programar`, `siguiente`, `emitir`. La clave de emisión no se guarda nunca (se pide a la API al emitir y se oculta en el log).
- `directo-saudi.yml` corre al encolar y cada 30 min (cron): un job de Actions dura como mucho 6 h, por eso solo espera a directos que empiezan
  en menos de 5,5 h; los más lejanos los recoge un run posterior. Mientras un job espera, los demás runs quedan en cola (un directo a la vez).
- La emisión usa `enableAutoStart`/`enableAutoStop`: pasa a "en directo" al recibir señal y se cierra al acabar el vídeo.
- Si YouTube responde `livePermissionBlocked` o `liveStreamingNotEnabled`, los directos no están activados en el canal (Studio > Crear >
  Emitir en directo; tarda hasta 24 h): avisa a Daniel con esos pasos.
- Los directos no cuentan en el límite de ~10 subidas/24 h, pero sí gastan cuota de la API (crear emisión ~150 unidades).
