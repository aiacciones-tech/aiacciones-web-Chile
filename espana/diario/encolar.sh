#!/bin/bash
# bash encolar.sh <carpeta del día>: encola el vídeo diario del IBEX 35 y su Short en cola-es/bolsa-<fecha>[-short]/ de la rama youtube-cola.
# Después: youtube-espana.yml sube a YouTube, buffer.yml publica en X, LinkedIn, TikTok e Instagram y telegram-espana.yml en Telegram.
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/es-scratch}; mkdir -p $S
[ -d $S/cola ] || git clone -q -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-es/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'])
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube España en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h): espera antes de encolar'
PY
C=cola-es/bolsa-$F; CS=cola-es/bolsa-$F-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C $CS
cp $B/youtube-bolsa-espana-$F.mp4 $C/video.mp4; cp $B/meta-youtube.json $C/meta.json; cp $B/miniatura-youtube.png $C/miniatura.png
cp $B/post-linkedin.txt $C/post-linkedin.txt; cp $B/post-x.txt $C/post-x.txt
[ -f $B/post-telegram.txt ] && cp $B/post-telegram.txt $C/post-telegram.txt
cp $B/short-bolsa-espana-$F.mp4 $CS/video.mp4; cp $B/meta-short.json $CS/meta.json
cp $B/post-tiktok.txt $CS/post-tiktok.txt; cp $B/post-tiktok.txt $CS/post-instagram.txt
git add $C $CS; git commit -qm "Cola España: vídeo diario del IBEX 35 $F (vídeo, Short y posts)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && [ -f $C/buffer.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
