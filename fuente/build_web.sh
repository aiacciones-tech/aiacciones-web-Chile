#!/bin/bash
# Arma web/ (lo que se publica en aiacciones.cl) desde fuente/site/.
# uso: cd fuente && ./build_web.sh [carpeta_destino]   (por defecto ../web)
# Pasos: copia site/, arregla el <head> de la portada (AdSense dentro del head), seo.py (canonical, OG, JSON-LD,
# sitemap, robots, llms.txt), ads.txt, páginas de redirección para URLs retiradas y hornear.py (precios, índices, hechos).
set -e
cd "$(dirname "$0")"
F=$(pwd); R=$(dirname "$F"); T=$(realpath -m "${1:-$R/web}")
TMP=$(mktemp -d)
cp "$R/web/assets/mercado.json" "$R/web/assets/hechos.json" "$TMP/"
rm -rf "$T" && cp -r "$F/site" "$T" && cp "$F/enviar.php.keep" "$T/enviar.php"
cp "$TMP/mercado.json" "$TMP/hechos.json" "$T/assets/" && rm -rf "$TMP"
python3 - "$T" <<'PY'
import re, sys
p = sys.argv[1] + "/index.html"; t = open(p, encoding="utf-8").read()
if t.startswith("<!doctype html><html><head>"):
    t = re.sub(r'^<!doctype html><html><head>.*?</head><body>\s*', '', t, count=1, flags=re.S)
    t = re.sub(r'\s*</body></html>\s*$', '', t)
    pre, post = t.split('<header class="site-head">', 1)
    t = ('<!doctype html>\n<html lang="es-CL">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
         + pre + '\n</head>\n<body>\n<header class="site-head">' + post + '\n</body>\n</html>\n')
    open(p, "w", encoding="utf-8").write(t)
PY
WEB="$T" python3 "$F/seo.py"
printf 'google.com, pub-5018554010876151, DIRECT, f08c47fec0942fa0\n' > "$T/ads.txt"
# URLs retiradas (tenían cifras ilustrativas): noindex + redirección a la sección, para que el hosting no siga sirviendo la versión vieja
while read -r rel dest; do
  [ -z "$rel" ] || [ "${rel:0:1}" = "#" ] && continue
  mkdir -p "$T/$rel"
  cat > "$T/$rel/index.html" <<HTML
<!doctype html>
<html lang="es-CL"><head><meta charset="utf-8"><meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url=$dest"><link rel="canonical" href="https://aiacciones.cl/${dest#../../}">
<title>Página retirada · AI Acciones Chile</title></head>
<body><p>Esta página ya no está disponible. <a href="$dest">Ir a la sección</a>.</p></body></html>
HTML
done < "$F/retirados.txt"
python3 "$R/scripts/hornear.py" "$T"
