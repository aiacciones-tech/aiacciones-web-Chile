# Playlists del canal Saudi Arabia AI Stocks (@SaudiArabiaAIStocks)

Pedido de Daniel el 24-nov-2026: playlists por empresa y por sector, más una por formato, para captar búsquedas y alargar las sesiones.

- **Config:** `saudi/playlists/playlists-saudi.json` (títulos y descripciones SEO en árabe, las 25 empresas con su sector).
- **Script:** `scripts/playlists-saudi.py`. Crea la playlist la primera vez que le toca un video y añade los videos públicos de `cola-sa/`.
- **Estado:** `playlists-saudi.json` en la raíz de la rama `youtube-cola` (ID de cada playlist y videos ya añadidos).
  Un video quitado a mano en YouTube Studio no se vuelve a añadir. Cambiar un título en la config NO renombra la playlist ya creada.
- **Automático:** `youtube-saudi.yml` lo corre después de cada subida (push a `cola-sa/**/meta.json`), con `continue-on-error`,
  así nunca frena la subida. A mano: Actions > "Subir videos a YouTube (Arabia Saudita)" > modo=playlists.
- **Qué va a dónde** (por el nombre de la carpeta en cola-sa/):
  - `bolsa-<fecha>` → ملخص السوق السعودية اليومي (solo el video largo)
  - `<empresa>-<periodo>` (3T26, FY26…) → نتائج الشركات + playlist de la empresa + playlist del sector
  - `lesson-ta-NN-<empresa>` → التحليل الفني ببساطة + empresa + sector
  - `calendar-*` / `earnings-calendar*` → تقويم النتائج (también los Shorts)
  - Los `-short` solo entran en la playlist de la empresa y en la del calendario.
- **Sectores (7):** bancos, energía y utilities, materiales (petroquímica, minería, cemento), telecom y tecnología, salud, seguros,
  consumo y real estate.
- **Nuevo formato o empresa:** añade la empresa a `empresas` (id = prefijo de su carpeta en cola-sa) o un formato a `formatos`
  y su regla en `clasificar()` del script.
- **Cuota de la API:** crear playlist o añadir video = 50 unidades. Cada pasada gasta como mucho `--presupuesto` (1500 por defecto)
  y si YouTube responde quotaExceeded se para sin error; lo que falta entra en la próxima pasada.
