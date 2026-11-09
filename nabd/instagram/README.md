# Instagram de Nabd Wall Street (نبض وول ستريت)

Instagram se publica a través de Buffer con una **segunda** cuenta de Buffer (secreto `BUFFER_API_KEY_NABD_IG`),
porque la primera (`BUFFER_API_KEY_NABD`) ya tiene LinkedIn, X y TikTok, el máximo del plan gratis.
`scripts/buffer.py` junta los canales de las dos cuentas (`CLAVES_NABD`) y cada post sale por la que tiene esa red.

- **Reel diario**: el Short vertical del cierre. `nabd/diario/gen_meta.py` escribe `post-instagram-<fecha>-Nabd.txt`
  (el mismo texto que TikTok: resumen en árabe, enlace al canal de YouTube, aviso de IA y de que no es asesoría,
  hashtags sin `#Shorts`); `encolar.sh` lo copia como `cola-nabd/bolsa-<fecha>-short/post-instagram.txt`
  (rama `youtube-cola`), junto al `video.mp4` del Short, y `buffer-Nabd.yml` lo publica como Reel (también en el feed).
- **Post de bienvenida** (primera foto del perfil): `nabd/instagram/cola-nabd/lanzamiento/` (texto + `imagen.png`
  1080x1350). Se publica una sola vez con "Run workflow" de `buffer-Nabd.yml`, modo `lanzamiento`
  (los de LinkedIn y X ya tienen su `buffer*.json` y no se repiten). Publicado el 9-nov-2026 (`buffer-instagram.json`; mientras exista no se repite).
- Mientras Instagram no esté conectado (o falte el secreto), el post espera sin error; los cierres de hace más de
  3 días no se mandan.
- Comprobar la conexión: "Run workflow" de `buffer-Nabd.yml` con `modo=verificar` (debe decir
  "Nabd Wall Street, Instagram: ...").
- Kit de la cuenta (foto, nombre, bio, pasos): `/mnt/project-files/nabd-instagram/` del proyecto.
