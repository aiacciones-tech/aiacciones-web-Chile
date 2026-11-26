#!/bin/bash
# bash encolar.sh <carpeta de la guía>: encola un vídeo evergreen «دليل المستثمر في السوق السعودية» (Saudi Arabia AI Stocks) y su Short en
# cola-sa/guide-<base>[-short]/ de la rama youtube-cola, igual que el vídeo diario (saudi/diario/encolar.sh).
# Después: youtube-saudi.yml sube a YouTube, buffer.yml publica en X, Threads y Facebook (vídeo largo) y en LinkedIn (Short como vídeo nativo),
# TikTok e Instagram (Short como Reel), y telegram-saudi.yml en Telegram.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/saudi-evergreen-scratch}; mkdir -p $S
for f in guide-$BASE-saudi.mp4 short-$BASE-saudi.mp4 meta-youtube-$BASE-saudi.json meta-short-$BASE-saudi.json thumbnail-$BASE-saudi.png \
         post-x-$BASE-saudi.txt post-threads-$BASE-saudi.txt post-facebook-$BASE-saudi.txt post-linkedin-$BASE-saudi.txt \
         post-tiktok-$BASE-saudi.txt post-instagram-$BASE-saudi.txt post-telegram-$BASE-saudi.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "SaudiArabiaAIStocks" $B/meta-youtube-$BASE-saudi.json && grep -q "SaudiArabiaAIStocks" $B/meta-short-$BASE-saudi.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
for p in x threads facebook linkedin tiktok instagram telegram; do grep -q "SaudiArabiaAIStocks" $B/post-$p-$BASE-saudi.txt || { echo "falta el enlace del canal en post-$p"; exit 1; }; done
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-sa)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-sa/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (Arabia Saudita) en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido con el diario y los resultados): espera antes de encolar'
PY
C=cola-sa/guide-$BASE; CS=cola-sa/guide-$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C $CS
cp $B/guide-$BASE-saudi.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-saudi.json $C/meta.json; cp $B/thumbnail-$BASE-saudi.png $C/miniatura.png
[ -s $B/ab-$BASE-saudi.json ] && [ -s $B/thumbnail-b-$BASE-saudi.png ] && { cp $B/ab-$BASE-saudi.json $C/ab.json; cp $B/thumbnail-b-$BASE-saudi.png $C/miniatura-b.png; }
cp $B/short-$BASE-saudi.mp4 $CS/video.mp4; cp $B/meta-short-$BASE-saudi.json $CS/meta.json
git add cola-sa; git commit -qm "Cola Arabia Saudita: evergreen, $BASE (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Posts en un segundo push, con el vídeo ya en la rama (Buffer toma el vídeo del Short desde GitHub). Mismo reparto que el diario:
cp $B/post-x-$BASE-saudi.txt $C/post-x.txt; cp $B/post-threads-$BASE-saudi.txt $C/post-threads.txt; cp $B/post-facebook-$BASE-saudi.txt $C/post-facebook.txt
cp $B/post-telegram-$BASE-saudi.txt $C/post-telegram.txt
cp $B/post-linkedin-$BASE-saudi.txt $CS/post-linkedin.txt
echo '{"omitido": "Facebook va en la carpeta del video largo (post-facebook.txt)"}' > $CS/buffer-facebook.json
cp $B/post-tiktok-$BASE-saudi.txt $CS/post-tiktok.txt; cp $B/post-instagram-$BASE-saudi.txt $CS/post-instagram.txt
git add cola-sa; git diff --cached --quiet || git commit -qm "Cola Arabia Saudita: posts de la evergreen, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "evergreen $BASE: YouTube $V, Short $SH" | tee -a $B/ids.txt
