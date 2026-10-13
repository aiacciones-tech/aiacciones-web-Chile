# AIAcciones España · web

Sitio estático aparte de la web chilena (no comparte páginas ni hosting).

- `fichas.py`: una ficha por empresa, solo con cifras reales de nuestros vídeos (nunca cifras de ejemplo).
- `datos/calendario-3T26.json`: calendario de resultados del IBEX 35 (exportado de `calendario-resultados-3T26-espana.xlsx`).
- `build.py`: arma `web/`. Correr `python3 espana/build.py` después de cada cambio y commitear `espana/web/`.
  Arriba del archivo van el dominio (`DOMINIO`, activa canonical y sitemap) y los datos del titular para el aviso legal (LSSI).
- Publicación: `.github/workflows/deploy-espana.yml` sube `espana/web/` por FTPS al hacer push a `main`.
  Secretos FTP_ES_SERVER, FTP_ES_USERNAME, FTP_ES_PASSWORD; variables opcionales FTP_ES_DIR y FTP_ES_TLS.
- Sin cookies, analítica ni Google Fonts (RGPD): si se agrega AdSense o Analytics hay que sumar banner de consentimiento.
