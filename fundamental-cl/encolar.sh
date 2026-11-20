#!/bin/bash
# bash encolar.sh <carpeta del capítulo>: encola un capítulo de «Análisis fundamental en simple» (video y Short) en cola/<base>[-short]/
# de la rama youtube-cola. Después: youtube.yml sube a YouTube (@aiaccioneschile), buffer.yml publica en X (video largo), LinkedIn y TikTok
# (el Short) y telegram-chile.yml en Telegram. Igual que diario/encolar.sh; el límite de ~10 subidas/24 h se comparte con el diario y los resultados.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])")
SH=$(python3 -c "import json;print(json.load(open('$B/short.json'))['out'])"); S=${SCRATCH:-/tmp/cl-scratch}; mkdir -p $S
for f in $BASE.mp4 $SH meta-youtube-$BASE.json meta-short-$BASE.json miniatura-$BASE.png post-x-$BASE.txt post-telegram-$BASE.txt post-linkedin-$BASE.txt post-tiktok-$BASE.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "aiacciones.cl" $B/meta-youtube-$BASE.json || { echo "falta el enlace a la web"; exit 1; }
if [ ! -d $S/colaf ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/colaf
  (cd $S/colaf && git sparse-checkout set cola)
fi
cd $S/colaf; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube Chile en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h): espera antes de encolar'
PY
C=cola/$BASE; CS=cola/$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C $CS
cp $B/$BASE.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE.json $C/meta.json; cp $B/miniatura-$BASE.png $C/miniatura.png
cp $B/$SH $CS/video.mp4; cp $B/meta-short-$BASE.json $CS/meta.json
TZ=America/Santiago date +%F' '%H:%M > $C/encolado.txt
git add cola; git commit -qm "Cola Chile: serie fundamental, $BASE (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, con el video ya en la rama (Buffer toma el video del Short desde GitHub).
cp $B/post-x-$BASE.txt $C/post-x.txt; cp $B/post-telegram-$BASE.txt $C/post-telegram.txt
cp $B/post-linkedin-$BASE.txt $CS/post-linkedin.txt; cp $B/post-tiktok-$BASE.txt $CS/post-tiktok.txt   # LinkedIn: el Short como video
git add cola; git diff --cached --quiet || git commit -qm "Cola Chile: posts de la serie fundamental, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SV=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "fundamental Chile $BASE: YouTube $V, Short $SV" | tee -a $B/ids.txt
