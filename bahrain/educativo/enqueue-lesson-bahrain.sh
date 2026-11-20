#!/bin/bash
# bash enqueue-lesson-bahrain.sh <lesson folder>: queues a lesson of «التحليل الفني ببساطة» (Bahrain AI Stocks) and its Short in
# cola-bahrain/lesson-<base>[-short]/ of branch youtube-cola, like the daily video (bahrain/daily-bahrain/enqueue-daily-bahrain.sh).
# Then youtube-bahrain.yml uploads to YouTube (@BahrainAIStocks), buffer.yml posts to X, Threads and Facebook (long video) and the Short
# as a video to LinkedIn, TikTok and Instagram, and telegram-bahrain.yml posts to Telegram. Facebook stays off while Daniel's account is blocked.
# REDES: "todas" (default, every network of the channel) or "ninguna" (YouTube only).
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video-bahrain.json'))['base'])"); S=${SCRATCH:-/tmp/bahrain-lesson-scratch}; mkdir -p $S
REDES=${REDES:-todas}
for f in lesson-$BASE-bahrain.mp4 short-$BASE-bahrain.mp4 meta-youtube-$BASE-bahrain.json meta-short-$BASE-bahrain.json thumbnail-$BASE-bahrain.png \
         post-x-$BASE-bahrain.txt post-threads-$BASE-bahrain.txt post-facebook-$BASE-bahrain.txt post-linkedin-$BASE-bahrain.txt \
         post-tiktok-$BASE-bahrain.txt post-instagram-$BASE-bahrain.txt post-telegram-$BASE-bahrain.txt; do
  test -s "$B/$f" || { echo "missing $B/$f"; exit 1; }
done
grep -q "BahrainAIStocks" $B/meta-youtube-$BASE-bahrain.json && grep -q "BahrainAIStocks" $B/meta-short-$BASE-bahrain.json || { echo "channel link missing in the metadata"; exit 1; }
for p in x threads facebook linkedin tiktok instagram telegram; do grep -q "BahrainAIStocks" $B/post-$p-$BASE-bahrain.txt || { echo "channel link missing in post-$p"; exit 1; }; done
tail -n1 $B/post-linkedin-$BASE-bahrain.txt | grep -qx "https://www.youtube.com/@BahrainAIStocks" || { echo "LinkedIn post must end with the channel link"; exit 1; }
grep -q "فيديو من إعداد قناة" $B/post-linkedin-$BASE-bahrain.txt || { echo "LinkedIn post needs the transparency line"; exit 1; }
if [ ! -d $S/cola ]; then  # sparse clone: only cola-bahrain (a full youtube-cola clone is ~5 GB)
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-bahrain)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-bahrain/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('YouTube uploads (Bahrain) in 24 h:',n); assert n<=8, 'YouTube limit (~10/24 h, shared with the daily and results videos): wait before queueing'
PY
C=cola-bahrain/lesson-$BASE; CS=cola-bahrain/lesson-$BASE-short
[ -e $C ] && { echo "already queued: $C"; exit 1; }
mkdir -p $C $CS
cp $B/lesson-$BASE-bahrain.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-bahrain.json $C/meta.json; cp $B/thumbnail-$BASE-bahrain.png $C/miniatura.png
cp $B/short-$BASE-bahrain.mp4 $CS/video.mp4; cp $B/meta-short-$BASE-bahrain.json $CS/meta.json
git add cola-bahrain; git commit -qm "Cola Baréin: serie educativa, $BASE (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
if [ "$REDES" != ninguna ]; then
# Posts go in a second push, once the videos are on the branch (Buffer takes the Short's video from GitHub).
cp $B/post-x-$BASE-bahrain.txt $C/post-x.txt; cp $B/post-threads-$BASE-bahrain.txt $C/post-threads.txt; cp $B/post-facebook-$BASE-bahrain.txt $C/post-facebook.txt
cp $B/post-telegram-$BASE-bahrain.txt $C/post-telegram.txt
cp $B/post-linkedin-$BASE-bahrain.txt $CS/post-linkedin.txt
echo '{"omitido": "Facebook va en la carpeta del video largo (post-facebook.txt)"}' > $CS/buffer-facebook.json
cp $B/post-tiktok-$BASE-bahrain.txt $CS/post-tiktok.txt; cp $B/post-instagram-$BASE-bahrain.txt $CS/post-instagram.txt
git add cola-bahrain; git diff --cached --quiet || git commit -qm "Cola Baréin: posts de la serie educativa, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
fi
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "lesson $BASE: YouTube $V, Short $SH" | tee -a $B/ids-bahrain.txt
