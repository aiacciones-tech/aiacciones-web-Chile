#!/bin/bash
# bash encolar.sh <carpeta del capítulo>: encola un capítulo de la serie «التحليل الأساسي ببساطة» (vídeo y Short) en cola-eau/<base>[-short]/
# de la rama youtube-cola. Después: youtube-eau.yml sube a YouTube (@AIStocksUAE), buffer.yml publica en X y Facebook (carpeta del vídeo)
# y en LinkedIn (Short como vídeo nativo), TikTok e Instagram (carpeta del Short), y telegram-eau.yml en Telegram. Igual que eau/diario/encolar.sh.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/eau-scratch}; mkdir -p $S
for f in $BASE-UAE.mp4 short-$BASE-UAE.mp4 meta-youtube-$BASE-UAE.json meta-short-$BASE-UAE.json miniatura-$BASE-UAE.png post-x-$BASE-UAE.txt \
         post-facebook-$BASE-UAE.txt post-telegram-$BASE-UAE.txt post-linkedin-$BASE-UAE.txt post-tiktok-$BASE-UAE.txt post-instagram-$BASE-UAE.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "youtube.com/@AIStocksUAE" $B/meta-youtube-$BASE-UAE.json || { echo "falta el enlace del canal"; exit 1; }
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-eau)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-eau/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube EAU en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido con el diario y los resultados): espera antes de encolar'
PY
C=cola-eau/$BASE; CS=cola-eau/$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C $CS
cp $B/$BASE-UAE.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-UAE.json $C/meta.json; cp $B/miniatura-$BASE-UAE.png $C/miniatura.png
cp $B/short-$BASE-UAE.mp4 $CS/video.mp4; cp $B/meta-short-$BASE-UAE.json $CS/meta.json
TZ=Asia/Dubai date +%F' '%H:%M > $C/encolado.txt
git add cola-eau; git commit -qm "Cola EAU: serie fundamental, $BASE (vídeo y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, con el vídeo ya en la rama (Buffer toma el vídeo del Short desde GitHub).
cp $B/post-x-$BASE-UAE.txt $C/post-x.txt; cp $B/post-facebook-$BASE-UAE.txt $C/post-facebook.txt; cp $B/post-telegram-$BASE-UAE.txt $C/post-telegram.txt
cp $B/post-linkedin-$BASE-UAE.txt $CS/post-linkedin.txt
echo '{"omitido": "Facebook va en la carpeta del vídeo largo (post-facebook.txt)"}' > $CS/buffer-facebook.json
cp $B/post-tiktok-$BASE-UAE.txt $CS/post-tiktok.txt; cp $B/post-instagram-$BASE-UAE.txt $CS/post-instagram.txt
git add cola-eau; git diff --cached --quiet || git commit -qm "Cola EAU: posts de la serie fundamental, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "fundamental EAU $BASE: YouTube $V, Short $SH" | tee -a $B/ids.txt
