# LinkedIn de Nabd Wall Street (نبض وول ستريت)

La página de empresa de LinkedIn se publica a través de Buffer, con su propia cuenta (secreto `BUFFER_API_KEY_NABD`).

- **Post diario**: `nabd/diario/gen_meta.py` escribe `post-linkedin-<fecha>-Nabd.txt`; `encolar.sh` lo copia como
  `cola-nabd/bolsa-<fecha>-short/post-linkedin.txt` (rama `youtube-cola`), y `buffer-Nabd.yml` lo manda a LinkedIn
  con el Short adjunto como video nativo.
- **Post de lanzamiento**: `nabd/linkedin/cola-nabd/lanzamiento/` (texto + `imagen.png`). Se publica una sola vez con
  "Run workflow" de `buffer-Nabd.yml`, modo `lanzamiento`. Publicado el 9-nov-2026 (`buffer-linkedin.json`; mientras exista no se repite).
- `modo=verificar` solo prueba la clave y muestra los canales de la cuenta.
