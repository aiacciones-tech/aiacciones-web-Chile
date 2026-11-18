# Voz Azure de AIAcciones Chile (es-CL-LorenzoNeural)

Daniel eligió el 18-nov-2026 la voz **Lorenzo** (Azure, chileno) para todos los videos de @aiaccioneschile: diario IPSA, videos de
resultados y sus Shorts. Piper `es_MX-claude-high` queda solo de respaldo. Muestras de la elección: `/mnt/project-files/voz-azure/`.

El contenedor de Claude no llega a Azure, así que la voz se hace en GitHub Actions (`voz-chile.yml`, secretos
`AZURE_SPEECH_KEY_CL` y `AZURE_SPEECH_REGION_CL`, plan gratuito F0 de 500.000 caracteres al mes: el diario gasta ~5.000 por día
y un video de resultados ~8.000).

## Cómo se usa (cualquier script que llame a `python3 -m piper`)
1. Con el guion terminado, pide la voz y espera (2-3 min):
   ```
   bash voz-cl/pedir.sh <id> <scratch>/voz-<id> <fuentes...>
   ```
   - Diario: `bash voz-cl/pedir.sh diario-<fecha> <scratch>/voz <dir>/video.json <dir>/short.json`
   - Resultados: `bash voz-cl/pedir.sh <empresa>-<trimestre> <scratch>/voz /mnt/project-files/<empresa>/narracion-<T>.py /mnt/project-files/<empresa>/short-<T>.json`
2. Renderiza igual que antes, pero con el falso piper delante y la carpeta de la voz:
   ```
   export PYTHONPATH=/home/user/aiacciones-web-chile/voz-cl/shim VOZ_DIR=<scratch>/voz
   ```
   (`VOICE=<onnx de Piper>` sigue haciendo falta para el respaldo). `python3 voz-cl/voz_cl.py resumen $VOZ_DIR` dice cuántas
   escenas salieron con Azure y cuántas con Piper.
3. Si cambias una locución después del pedido, vuelve a correr `pedir.sh` con el mismo id (solo pide lo nuevo). Antes de renderizar,
   `python3 voz-cl/voz_cl.py faltan $VOZ_DIR <fuentes...>` debe decir 0.

**No mezclar voces:** si `pedir.sh` sale con error (sin voz en 15 min, falta la clave o Azure agotó la cuota) o `faltan` no da 0,
renderiza todo con Piper (sin `PYTHONPATH`/`VOZ_DIR`) y dilo en el mensaje del hilo.

## Piezas
- `voz_cl.py`: voz (`AZURE_VOZ_CL`, por defecto es-CL-LorenzoNeural, velocidad normal), `clave(texto)` = nombre del wav, lectura de las
  fuentes (incluye las frases de la campaña de comentarios de `diario/campana.py` mientras esté activa), síntesis.
- `shim/piper/`: falso `python3 -m piper`. Con `VOZ_DIR`, copia el wav de Azure de esa locución; si no lo hay, llama al Piper real y lo
  pasa a 24 kHz (todas las escenas con la misma frecuencia). Sin `VOZ_DIR`, es Piper tal cual.
- `pedir.sh`: sube `voz-cl/pedidos/<id>.json` a la rama `voz-cl-pedido-<id>` (desde main), espera a `voz-chile.yml` y copia los wav.
- `voz-chile.yml`: sintetiza, guarda `<id>/` en la rama `voz-cl` (sin historial; borra carpetas de más de 10 días) y borra la rama del pedido.
- `voz-muestras-cl.yml` + `../voz-muestras-cl/`: las muestras de voces de la elección.
