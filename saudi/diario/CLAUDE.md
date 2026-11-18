# Video diario de Arabia Saudita (@SaudiArabiaAIStocks): notas para la sesión diaria

**Voz Azure desde el 18-nov-2026 (pedido de Daniel).** Estas notas prevalecen sobre el texto de la tarea programada donde difieran
(si dice "voz Piper", ya no es la primera opción). Sigue `README.md` → "Pasos de cada día", pasos 4 a 6:

1. Con `video.json` y `short.json` del día listos, haz commit y push de los dos a tu rama `claude/...`. `voz-saudi.yml` genera la voz
   `ar-SA-HamedNeural` (unos 2 min) en `<fecha>/` de la rama `voz-saudi`. Mira el run en Actions ("Voz Azure del video diario (Arabia Saudita)").
2. `git clone -q --depth 1 -b voz-saudi https://github.com/aiacciones-tech/aiacciones-web-Chile.git <scratch>/voz`
   y renderiza con `VOZ_DIR=<scratch>/voz/<fecha>` en `make_video.py` y `make_short.py`. La línea `listo ... | voz:` dice si salió todo con Azure.
3. Si cambias una locución, vuelve a hacer push del json y espera el run nuevo (solo pide a Azure las escenas cambiadas).
4. Si el workflow falla o falta la clave, renderiza sin `VOZ_DIR` (Piper, como antes) y dilo en el resumen.
5. La voz de Azure es algo más lenta que Piper: respeta el máximo de 330 s; si `make_video.py` dice que es demasiado largo, acorta la locución.

La clave es el plan gratuito de Azure compartido con Nabd Wall Street (500.000 caracteres/mes; este canal gasta ~3.200 por sesión).
No regeneres la voz sin necesidad.
