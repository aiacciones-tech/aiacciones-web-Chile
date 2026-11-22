#!/bin/bash
# bash calendario-cl/encolar.sh <carpeta de la semana>: publica el Short del «Calendario semanal de resultados» (Daniel, 22-nov-2026:
# automático, domingos entre las 18:00 y las 20:00 de Chile). Si se llama antes de las 18:00 espera hasta las 18:02; después de las 20:00 no publica.
# Encola en cola/calendario-<lunes>-short/ de la rama youtube-cola: youtube.yml sube el Short (público); buffer.yml publica TikTok,
# Instagram (Reel) y Threads; telegram-chile.yml, Telegram (con el enlace del Short).
set -e
B=$(cd "$1" && pwd); L=$(basename "$B"); S=${SCRATCH:-/tmp/cl-scratch}; mkdir -p $S
for f in calendario-resultados-$L.mp4 meta-short.json post-tiktok.txt post-instagram.txt post-threads.txt post-telegram.txt; do [ -f "$B/$f" ] || { echo "falta $f"; exit 1; }; done
python3 - "$B" <<'PY'
import json,sys,os
b=sys.argv[1]; m=json.load(open(f"{b}/meta-short.json"))
assert len(m["title"])<=100 and m["privacy"]=="public" and "<" not in m["description"] and ">" not in m["description"] and len(m["description"].encode())<5000
assert m["description"].rstrip().endswith("Contenido informativo, no es recomendación de inversión."), "aviso al final de la descripción"
assert len(open(f"{b}/post-threads.txt").read())<=500 and len(open(f"{b}/post-instagram.txt").read())<=2200 and len(open(f"{b}/post-tiktok.txt").read())<=2200
PY
while :; do
  H=$(TZ=America/Santiago date +%H%M)
  [ "$H" -ge 2000 ] && { echo "Ya pasaron las 20:00 en Chile: no se publica fuera de la franja. Avisa a Daniel."; exit 3; }
  [ "$H" -ge 1802 ] && break
  echo "esperando las 18:02 de Chile (ahora $H)"; sleep 60
done
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'])
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube Chile en 24 h:',n); assert n<=9, 'límite de YouTube (~10/24 h): espera antes de encolar'
PY
C=cola/calendario-$L-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C
cp $B/calendario-resultados-$L.mp4 $C/video.mp4; cp $B/meta-short.json $C/meta.json
for f in post-tiktok.txt post-instagram.txt post-threads.txt post-telegram.txt; do cp $B/$f $C/$f; done
git add $C; git commit -qm "Cola Chile: calendario semanal de resultados $L (Short y posts)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
SH=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])")
echo "calendario $L: Short https://youtube.com/shorts/$SH" | tee -a $B/ids.txt
