# Producción de vídeos de AIAcciones España (IBEX 35)

Copia de trabajo de todo lo usado para los vídeos 1S 2026 (13-oct-2026). Las rutas de los scripts apuntan a
`/mnt/project-files/espana/<empresa>/`: si trabajas en otra carpeta, cambia `DIR`, `LOGO`, `B` y `out` en cada script/JSON.
No contiene vídeos (.mp4), audio ni la voz (.onnx).

## Dependencias
- Python 3 con `pip install piper-tts matplotlib imageio-ffmpeg pillow numpy` (imageio-ffmpeg trae ffmpeg).
- Tipografía: la que trae matplotlib por defecto (DejaVu Sans); no hace falta instalar fuentes.
- Voz Piper **es_ES-davefx-medium**: descargar `vits-piper-es_ES-davefx-medium.tar.bz2` de
  https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models (huggingface está bloqueado en el contenedor) y descomprimir;
  el modelo es `vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx`.
- Ajustes de voz fluida (ya en make_video_voz.py): `--length-scale 0.97 --noise-scale 0.55 --noise-w-scale 0.6 --sentence-silence 0.1`.

## Pasos por empresa (ver pipeline/brief-video-1S26.md, que es el encargo completo)
1. Cifras oficiales del informe (nota de prensa + prensa) y valoración en stockanalysis.com; todo con fuente en `guion-<periodo>.md`, cálculos propios marcados "calculado".
2. Copia la carpeta de una empresa parecida (bancos: `bankinter/`; eléctricas: `redeia/` o `iberdrola/`) y cambia `narracion.py` (números en palabras) y `make_video_voz.py` (15 escenas, 7 secciones: titular, ingresos, BPA, márgenes/caja o eficiencia/riesgo/capital en bancos, guía, valoración frente a su historia, qué cambió; cierre con aviso).
3. `AUD=<scratch> python3 make_video_voz.py preview` → revisar PNG; luego `AUD=<scratch> VOICE=<ruta .onnx> python3 make_video_voz.py` (escribe `AUD/times.json` para los capítulos).
4. `python3 miniatura.py` (1280x720).
5. Short: `AUD=<scratch> VOICE=... python3 shorts/make_short_es.py <empresa>/short-<periodo>.json` (menos de 59 s; `big_fs` para números largos, `nombre` en la escena fin si el nombre se corta).
6. `meta-youtube.json` (título ≤100 caracteres, sin "<" ni ">", descripción < 5000 bytes, capítulos, fuentes y el AVISO IMPORTANTE completo de `marca/aviso-legal.txt`; privacy "public"), `meta-short.json` (con `{video:<slug>}`), `post-linkedin-<periodo>.txt` y `post-x-<periodo>.txt` (con `{youtube}`; X ≤280 contando URL = 23).
7. Publicar: `pipeline/encolar.sh <empresa>` copia todo a `cola-es/<slug>/` y `cola-es/<slug>-short/` de la rama `youtube-cola`; el workflow "Subir videos a YouTube (España)" sube, escribe `resultado.json`, y "Mandar posts de X a Buffer" publica en X y LinkedIn. El script espera y rellena `ficha-web.py`.
8. Web: añadir el dict de `ficha-web.py` a `espana/fichas.py`, `python3 espana/build.py`, PR a main (el merge publica aiacciones.es por FTPS).

## Reglas (Daniel)
- Nada de comprar/vender, precio objetivo ni "cara/barata"; la valoración solo compara múltiplos con la historia de la propia empresa (guía CNMV finfluencers, MAR).
- Aviso completo en toda descripción, post y ficha; firma "AIAcciones España"; "AIAcciones España no tiene posiciones en las empresas analizadas".
- Nunca "los primeros"/"los más rápidos". Vídeos públicos por defecto. Cada vídeo lleva su Short.
- Español de España; voz es_ES.

## Resumen de memoria del proyecto (sin secretos)
- **Canal YouTube** @AIAccionesEspaña. Workflow `.github/workflows/youtube-espana.yml` (carpeta `cola-es/` de `youtube-cola`), secreto `YT_ES_REFRESH_TOKEN` (cliente OAuth = el de Chile). Límite ~10 subidas/24 h (`uploadLimitExceeded` el 13-oct 17:08 UTC). Si el job falla a mitad, el paso que guarda `resultado.json` puede no correr: escribirlo a mano para no duplicar. Canal verificado el 14-oct (miniaturas ya funcionan, según el hilo de España).
- **Buffer**: segunda cuenta para España, secreto `BUFFER_API_KEY_ES`; X @AIAccionesES y página de LinkedIn "AIAcciones España" (esta última en la cuenta de Chile como respaldo). `scripts/buffer.py programar cola-es` (el workflow lo corre desde la rama youtube-cola).
- **Web** https://aiacciones.es: carpeta `espana/` de este repo (`build.py`, `fichas.py`, `datos/calendario-3T26.json`), publica con `deploy-espana.yml` por FTPS (secretos FTP_ES_*). Google Analytics G-YBK7SY7FN2 solo tras consentimiento (PR #31). Correo del titular nunca en texto plano.
- **Merge automático**: Daniel autorizó (14-oct) que Claude fusione las PR de las webs y avise después.
- **Calendario 3T26**: `espana/datos/calendario-3T26.json`; confirmadas Iberdrola 21-oct, Bankinter 22-oct, Santander 28-oct, BBVA 29-oct, Repsol 29-oct, CaixaBank 30-oct, Unicaja 30-oct. Las cotizadas publican ~07:00-08:00 Madrid.
- **Publicado (1S26)**: Iberdrola RGgaT31jOxk/ynP_eL0oBIM, Redeia wbzhyA-076o/oFncLSa2iN4, Bankinter k7qJSVY5__k/oboYRN0_OH4, Unicaja QmTUeCVBUk4/zoldZTxXavE, BBVA pUB4hXT_RaQ/9eV_Y5hfj-o, Santander -ED5j67j-0g/ZesAasxjui0, Sabadell wkQGwk63kTE (Short pendiente). CaixaBank listo, subida programada 14-oct 17:15 UTC.
