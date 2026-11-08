#!/bin/bash
# bash enqueue-daily-bahrain.sh <day folder>: queues the daily Arabic video and its Short in cola-bahrain/daily-<date>[-short]/ of branch youtube-cola.
# Then youtube-bahrain.yml uploads to YouTube (@BahrainAIStocks), buffer.yml posts to X, Threads and Facebook (long video)
# and to TikTok, Instagram and LinkedIn (Short as video), and telegram-bahrain.yml posts to Telegram (post-telegram.txt).
# REDES picks the networks besides YouTube: "todas" (default), "linkedin" (only the Short on LinkedIn, Daniel's rule of 8-nov-2026),
# or "ninguna". SOLO_YOUTUBE=1 is the old spelling of REDES=ninguna.
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info-bahrain.json'))['fecha'])"); S=${SCRATCH:-/tmp/bahrain-scratch}; mkdir -p $S
REDES=${REDES:-todas}; [ "${SOLO_YOUTUBE:-0}" = 1 ] && REDES=ninguna
for f in post-linkedin-$F-bahrain.txt video-$F-bahrain.mp4 short-$F-bahrain.mp4 meta-youtube-$F-bahrain.json meta-short-$F-bahrain.json thumbnail-$F-bahrain.png post-x-$F-bahrain.txt \
         post-threads-$F-bahrain.txt post-facebook-$F-bahrain.txt post-tiktok-$F-bahrain.txt post-instagram-$F-bahrain.txt post-telegram-$F-bahrain.txt; do
  test -s "$B/$f" || { echo "missing $B/$f"; exit 1; }
done
grep -q "BahrainAIStocks" $B/meta-youtube-$F-bahrain.json && grep -q "BahrainAIStocks" $B/meta-short-$F-bahrain.json || { echo "channel link missing in the metadata"; exit 1; }
for p in x threads facebook tiktok instagram telegram linkedin; do grep -q "BahrainAIStocks" $B/post-$p-$F-bahrain.txt || { echo "channel link missing in post-$p"; exit 1; }; done
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-bahrain/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('YouTube uploads (Bahrain) in 24 h:',n); assert n<=8, 'YouTube limit (~10/24 h, shared with the results videos): wait before queueing'
PY
C=cola-bahrain/daily-$F; CS=cola-bahrain/daily-$F-short
[ -f $C/resultado.json ] && { echo "already uploaded: $C"; exit 1; }
mkdir -p $C $CS
cp $B/video-$F-bahrain.mp4 $C/video.mp4; cp $B/meta-youtube-$F-bahrain.json $C/meta.json; cp $B/thumbnail-$F-bahrain.png $C/miniatura.png
cp $B/short-$F-bahrain.mp4 $CS/video.mp4; cp $B/meta-short-$F-bahrain.json $CS/meta.json
git add cola-bahrain; git commit -qm "Cola Baréin: video diario de la bolsa $F (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
if [ "$REDES" = ninguna ]; then for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
else
# Posts go in a second push, once the video is on the branch (Buffer takes the Short's video from GitHub).
cp $B/post-linkedin-$F-bahrain.txt $CS/post-linkedin.txt
if [ "$REDES" = todas ]; then
cp $B/post-x-$F-bahrain.txt $C/post-x.txt; cp $B/post-threads-$F-bahrain.txt $C/post-threads.txt; cp $B/post-facebook-$F-bahrain.txt $C/post-facebook.txt
cp $B/post-telegram-$F-bahrain.txt $C/post-telegram.txt
cp $B/post-tiktok-$F-bahrain.txt $CS/post-tiktok.txt; cp $B/post-instagram-$F-bahrain.txt $CS/post-instagram.txt
fi
git add cola-bahrain; git diff --cached --quiet || git commit -qm "Cola Baréin: posts del video diario $F"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
fi
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "Bahrain daily $F: YouTube $V, Short $SH" | tee -a $B/ids-bahrain.txt
