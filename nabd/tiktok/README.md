# TikTok de Nabd Wall Street (نبض وول ستريت)

La cuenta de TikTok se publica a través de Buffer, con la misma cuenta que LinkedIn y X (secreto `BUFFER_API_KEY_NABD`;
es el tercer canal, el máximo del plan gratis).

- **Video diario**: el Short vertical del cierre. `nabd/diario/gen_meta.py` escribe `post-tiktok-<fecha>-Nabd.txt`
  (resumen en árabe, enlace al canal de YouTube, aviso de IA y de que no es asesoría, hashtags sin `#Shorts`);
  `encolar.sh` lo copia como `cola-nabd/bolsa-<fecha>-short/post-tiktok.txt` (rama `youtube-cola`), junto al `video.mp4`
  del Short, y `buffer-Nabd.yml` lo sube a TikTok (Buffer descarga el video por su enlace de raw.githubusercontent.com).
- Mientras TikTok no esté conectado en Buffer, el post espera sin error; los cierres de hace más de 3 días no se mandan.
- Comprobar la conexión: "Run workflow" de `buffer-Nabd.yml` con `modo=verificar` (debe decir "Nabd Wall Street, TikTok: ...").
