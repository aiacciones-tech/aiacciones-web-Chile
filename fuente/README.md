# Fuente del sitio

`site/` es la fuente que se edita con los scripts Python de esta carpeta (fichas: `addficha.py`, comparadores, calendario, etc.).
`mkzip.sh` arma `web/` desde `site/` (portada con AdSense en el head, `enviar.php`, `seo.py`). Los scripts tienen rutas
absolutas de la sesión donde se crearon: ajústalas a donde clones el repo.

Después de regenerar `web/` corre siempre `python3 scripts/hornear.py web` para volver a escribir precios de cierre,
índices y hechos esenciales (salen de `web/assets/mercado.json` y `hechos.json`, que actualiza la rutina diaria
`.github/workflows/mercado.yml`). Al hacer push a `main` con cambios en `web/`, `deploy.yml` publica en aiacciones.cl.
