#!/bin/bash
# bash encolar.sh <carpeta del día>: encola el video diario en árabe y su Short en cola-eau/bolsa-<fecha>[-short]/ de la rama youtube-cola.
# Después: youtube-eau.yml sube a YouTube (@AIStocksUAE), buffer.yml publica en X, LinkedIn, Facebook, TikTok e Instagram,
# y telegram-eau.yml en Telegram (post-telegram.txt).
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/eau-scratch}; mkdir -p $S
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-eau/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube EAU en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido con los videos de resultados): espera antes de encolar'
PY
C=cola-eau/bolsa-$F; CS=cola-eau/bolsa-$F-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C $CS
cp $B/video-bolsa-$F-UAE.mp4 $C/video.mp4; cp $B/meta-youtube-$F-UAE.json $C/meta.json; cp $B/miniatura-$F-UAE.png $C/miniatura.png
cp $B/short-bolsa-$F-UAE.mp4 $CS/video.mp4; cp $B/meta-short-$F-UAE.json $CS/meta.json
git add cola-eau; git commit -qm "Cola EAU: video diario de la bolsa $F (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, cuando el video ya está en la rama (Buffer toma el video del Short desde GitHub).
cp $B/post-x-$F-UAE.txt $C/post-x.txt; cp $B/post-linkedin-$F-UAE.txt $C/post-linkedin.txt; cp $B/post-telegram-$F-UAE.txt $C/post-telegram.txt
cp $B/post-tiktok-$F-UAE.txt $CS/post-tiktok.txt; cp $B/post-instagram-$F-UAE.txt $CS/post-instagram.txt
git add cola-eau; git diff --cached --quiet || git commit -qm "Cola EAU: posts del video diario $F"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario EAU $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
