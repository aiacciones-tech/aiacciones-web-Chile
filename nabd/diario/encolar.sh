#!/bin/bash
# bash encolar.sh <carpeta del día>: encola el video diario en árabe de Wall Street y su Short en cola-nabd/bolsa-<fecha>[-short]/ de la rama youtube-cola.
# Después youtube-Nabd.yml los sube al canal Nabd Wall Street (نبض وول ستريت).
# El post de Telegram (post-telegram-<fecha>-Nabd.txt) va como post-telegram.txt del video largo: telegram-Nabd.yml lo publica
# con la miniatura cuando el video ya está en YouTube. El resto de posts (Buffer) se quedan en la carpeta del día.
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/nabd-scratch}; mkdir -p $S
for f in video-bolsa-$F-Nabd.mp4 short-bolsa-$F-Nabd.mp4 meta-youtube-$F-Nabd.json meta-short-$F-Nabd.json miniatura-$F-Nabd.png; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
ID=UCRU3n034y5dJBEGnhAKjhfQ
grep -q "$ID" $B/meta-youtube-$F-Nabd.json && grep -q "$ID" $B/meta-short-$F-Nabd.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-nabd/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (Nabd) en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h por canal): espera antes de encolar'
PY
C=cola-nabd/bolsa-$F; CS=cola-nabd/bolsa-$F-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C $CS
cp $B/video-bolsa-$F-Nabd.mp4 $C/video.mp4; cp $B/meta-youtube-$F-Nabd.json $C/meta.json; cp $B/miniatura-$F-Nabd.png $C/miniatura.png
[ -s $B/post-telegram-$F-Nabd.txt ] && cp $B/post-telegram-$F-Nabd.txt $C/post-telegram.txt
cp $B/short-bolsa-$F-Nabd.mp4 $CS/video.mp4; cp $B/meta-short-$F-Nabd.json $CS/meta.json
git add cola-nabd; git commit -qm "Cola Nabd: video diario de Wall Street $F (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario Nabd $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
