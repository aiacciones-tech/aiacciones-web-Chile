# ⚠️ INSTRUCCIONES VIGENTES DE LA TAREA DIARIA (10-nov-2026) — LEER ANTES DE NADA

Desde el 10-nov-2026 el vídeo diario dura **8 a 10 minutos** (manual de Daniel). Estas instrucciones **sustituyen** a las del texto
de la tarea programada allí donde difieran: ya **no** valen "~230 palabras", "máx. 180 s", ni la voz Piper como primera opción,
ni `ejemplo-2026-11-06/` como plantilla (esa carpeta solo redirige aquí; la plantilla es `ejemplo-2026-11-09/`).
`make_video.py` rechaza vídeos de menos de 450 s o más de 630 s. Daniel lo aprobó en el hilo del vídeo largo (10-nov-2026).

**Martes y jueves (desde el 17-nov-2026, prueba de un mes):** voz-Nabd.yml añade un presentador IA de HeyGen a la apertura (ver README,
"Presentador IA"). Espera a que el workflow de la voz termine (unos 3 min más esos días) antes de descargar `voz-nabd`; `make_video.py` lo usa
solo e imprime `avatar: sí/no`. No cambies la locución de `s_title` después de generar la voz (el avatar se descartaría). Di en el resumen
si el vídeo salió con presentador y, si no, el motivo de `voz-nabd/<fecha>/avatar.json`.
**Aviso por correo (pedido por Daniel, 14-nov-2026):** cuando el vídeo publicado lleve presentador (`avatar: sí`), envía un correo a Daniel
con el conector de Gmail (`send_message`, a la dirección de su cuenta, la misma del Gmail conectado; está en la memoria del proyecto), asunto
`Nabd: vídeo con avatar <fecha>` y en el cuerpo, en español: enlace de YouTube del vídeo, duración, segundos de la apertura con avatar,
coste y saldo de HeyGen (`saldo_antes`/`saldo_despues` de `avatar.json`). Si no hay conector de Gmail, dilo en el resumen.

> Prepara y publica el vídeo diario en árabe de Wall Street del canal Nabd Wall Street (نبض وول ستريت, id UCRU3n034y5dJBEGnhAKjhfQ): el programa «التقرير اليومي», de 8 a 10 minutos, según el manual de producción de Daniel (10-nov-2026). Daniel aprobó (9-nov-2026) publicarlo automáticamente y en público cada día de sesión, sin revisión previa. No quiere ningún paso manual.
>
> Repo: aiacciones-tech/aiacciones-web-Chile. Usa nabd/diario/ de main. Sigue nabd/diario/README.md al pie de la letra ("Guion", "Voz", "Pasos de cada día" y "Reglas"). Solo toca nabd/, sus workflows y cola-nabd/.
>
> 1. Datos: busca hoy (fecha de Nueva York) datos/mercado-<fecha>.json en la rama datos-diario-nabd. GitHub retrasa a veces el cron: si no está, lanza tú el workflow datos-diario-Nabd.yml (workflow_dispatch en main) y espera a que termine. Si la última vela no es de hoy (festivo o fin de semana), termina sin publicar nada.
> 2. Copia ejemplo-2026-11-09/ (sin mercado.json, mp4, png, md, csv, meta ni post) a nabd/diario/<fecha>/ y pon el mercado.json del día. Ejecuta tecnico.py: cifras, medias 20/50/200, escenarios, sectores, macro, aportación al Dow, grandes del Nasdaq 100 y candidatas.
> 3. Investiga las noticias de la sesión de hoy (Yahoo Finance live blog, CNBC, Reuters, The Closing Print, StockTitan; Fed, BLS, BEA, Tesoro, SEC EDGAR y notas de resultados cuando existan): qué pasó, por qué, sectores, y elige 5 acciones de las candidatas por su relevancia (resultados, noticia, volumen inusual), no solo por el %. Solo lo publicado hoy; si no hay motivo, «لا يوجد خبر محدد في الصحافة». Nunca inventes una cifra, noticia ni nivel: los niveles técnicos y los escenarios salen de tecnico.py. Agenda de la próxima sesión con hora de Nueva York (la de La Meca se calcula sola).
> 4. Reescribe video.json (17 escenas: locución en árabe estándar con números en palabras, entre 7:30 y 10:30 min; objetivo 8-10, unas 950-1.050 palabras con Azure), info.json (sin capítulos: salen solos) y short.json (< 59 s). Diferencia hechos, opiniones y escenarios; escenarios siempre como condiciones, nunca previsiones. Sin recomendaciones de compra/venta.
> 5. Voz (Azure ar-SA-HamedNeural, secretos ya configurados): sube nabd/diario/<fecha>/video.json a la rama claude/nabd-diario-<fecha> (creada desde main); voz-Nabd.yml genera la voz (unos 2 min) y la deja en <fecha>/ de la rama voz-nabd: clónala y usa VOZ_DIR=<clon>/<fecha>. Si cambias la locución después, vuelve a subir video.json y espera la voz nueva. Si el workflow dice que falta el secreto AZURE_SPEECH_KEY_NABD o falla, sigue con Piper (make_video.py lo hace solo sin VOZ_DIR) y dilo en el resumen.
> 6. Render: preview primero y mira TODOS los PNG (textos cortados, solapes, cifras que no cuadren con la locución); luego make_video.py (con VOZ_DIR si hay voz de Azure), make_short.py y gen_meta.py. Si el control de calidad de make_video.py falla, corrige la causa; no lo saltes. Piper ar_JO-kareem-medium está en /mnt/project-files/nabd-pipeline/voice/.
> 7. Publica: SCRATCH=<scratch> bash nabd/diario/encolar.sh nabd/diario/<fecha>. Si en 10 min no aparece resultado.json, lanza el workflow youtube-Nabd.yml con modo=subir.
> 8. Copia el vídeo, el Short, la miniatura, el meta, guion-<fecha>-Nabd.md y datos-<fecha>-Nabd.csv a /mnt/project-files/nabd-diario/<fecha>/ (todos los nombres terminan en -Nabd). Haz commit de video.json, info.json y short.json del día (no del mercado.json, que ya está en datos-diario-nabd) en la rama claude/nabd-diario-<fecha> y abre PR.
> 9. Termina con un resumen corto en español: enlaces de YouTube del vídeo y el Short, duración, voz usada (Azure o Piper), si salieron públicos, y cualquier fallo.

