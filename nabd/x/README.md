# X de Nabd Wall Street (نبض وول ستريت)

La cuenta de X se publica a través de Buffer, con la misma cuenta que la página de LinkedIn (secreto `BUFFER_API_KEY_NABD`).

- **Post diario**: `nabd/diario/gen_meta.py` escribe `post-x-<fecha>-Nabd.txt`; `encolar.sh` lo copia como
  `cola-nabd/bolsa-<fecha>/post-x.txt` (rama `youtube-cola`), y `buffer-Nabd.yml` lo manda a X con el enlace al video.
  Los cierres de hace más de 3 días no se mandan.
- **Post de lanzamiento** (para fijar a mano en el perfil): `nabd/x/cola-nabd/lanzamiento/` (texto + `imagen.png`).
  Se publica una sola vez con "Run workflow" de `buffer-Nabd.yml`, modo `lanzamiento` (`buffer.json` evita repetirlo).
