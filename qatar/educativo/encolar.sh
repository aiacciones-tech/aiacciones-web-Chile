#!/bin/bash
# bash encolar.sh <carpeta de la lección>: encola una lección de «التحليل الفني ببساطة» (Qatar AI Stocks) y su Short en
# cola-qa/<base>[-short]/ de la rama youtube-cola, igual que la serie fundamental (qatar/fundamental/encolar.sh).
# Después: youtube-qatar.yml sube a YouTube (@QatarAIStocks), buffer.yml publica en X y Threads (carpeta del vídeo; Facebook cerró la
# cuenta el 12-nov-2026) y en LinkedIn (Short como vídeo nativo), TikTok e Instagram (Short como Reel), y telegram-qatar.yml en Telegram.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/qa-edu-scratch}; mkdir -p $S
for f in $BASE-qatar.mp4 short-$BASE-qatar.mp4 meta-youtube-$BASE-qatar.json meta-short-$BASE-qatar.json miniatura-$BASE-qatar.png \
         post-x-$BASE-qatar.txt post-threads-$BASE-qatar.txt post-linkedin-$BASE-qatar.txt \
         post-tiktok-$BASE-qatar.txt post-instagram-$BASE-qatar.txt post-telegram-$BASE-qatar.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "youtube.com/@QatarAIStocks" $B/meta-youtube-$BASE-qatar.json && grep -q "youtube.com/@QatarAIStocks" $B/meta-short-$BASE-qatar.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
for p in x threads linkedin tiktok instagram telegram; do grep -q "youtube.com/@QatarAIStocks" $B/post-$p-$BASE-qatar.txt || { echo "falta el enlace del canal en post-$p"; exit 1; }; done
if [ ! -d $S/colae ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/colae
  (cd $S/colae && git sparse-checkout set cola-qa)
fi
cd $S/colae; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY2
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-qa/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube Qatar en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido con el diario y la serie fundamental): espera antes de encolar'
PY2
C=cola-qa/$BASE; CS=cola-qa/$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C $CS
cp $B/$BASE-qatar.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-qatar.json $C/meta.json; cp $B/miniatura-$BASE-qatar.png $C/miniatura.png
cp $B/short-$BASE-qatar.mp4 $CS/video.mp4; cp $B/meta-short-$BASE-qatar.json $CS/meta.json
TZ=Asia/Qatar date +%F' '%H:%M > $C/encolado.txt
git add cola-qa; git commit -qm "Cola Qatar: serie educativa de análisis técnico, $BASE (vídeo y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, con el vídeo ya en la rama (Buffer toma el vídeo del Short desde GitHub).
cp $B/post-x-$BASE-qatar.txt $C/post-x.txt; cp $B/post-threads-$BASE-qatar.txt $C/post-threads.txt; cp $B/post-telegram-$BASE-qatar.txt $C/post-telegram.txt
cp $B/post-linkedin-$BASE-qatar.txt $CS/post-linkedin.txt
cp $B/post-tiktok-$BASE-qatar.txt $CS/post-tiktok.txt; cp $B/post-instagram-$BASE-qatar.txt $CS/post-instagram.txt
git add cola-qa; git diff --cached --quiet || git commit -qm "Cola Qatar: posts de la serie educativa, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "educativa Qatar $BASE: YouTube $V, Short $SH" | tee -a $B/ids.txt
