set -e
cd /tmp/claude-0/-home-claude/51bbcb85-f720-5650-9a37-2f75843c73b7/scratchpad
rm -rf web && cp -r site web && cp enviar.php.keep web/enviar.php
python3 - <<'PY'
import re
p="web/index.html";t=open(p,encoding="utf-8").read()
t=re.sub(r'^<!doctype html><html><head>.*?</head><body>\s*','',t,count=1,flags=re.S)
t=re.sub(r'\s*</body></html>\s*$','',t)
pre,post=t.split('<header class="site-head">',1)
t='<!doctype html>\n<html lang="es-CL">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'+pre+'\n</head>\n<body>\n<header class="site-head">'+post+'\n</body>\n</html>\n'
open(p,"w",encoding="utf-8").write(t)
PY
python3 seo.py
printf 'google.com, pub-5018554010876151, DIRECT, f08c47fec0942fa0\n' > web/ads.txt
rm -f /mnt/project-files/web/aiacciones-web.zip && (cd web && zip -qr /mnt/project-files/web/aiacciones-web.zip .)
cd web; bad=0; for f in $(find . -name '*.html'); do python3 -c "
import sys;t=open('$f').read();sys.exit(0 if 'pub-5018554010876151' in t.split('</head>')[0] and t.count('<head>')==1 else 1)" || bad=$((bad+1)); done
echo "adsense-bad=$bad gmail=$(grep -rl gmail . | wc -l) files=$(unzip -l /mnt/project-files/web/aiacciones-web.zip | tail -1)"
