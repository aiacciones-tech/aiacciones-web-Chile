#!/bin/bash
# bash encolar.sh <carpeta del capítulo>: encola un capítulo de la serie «التحليل الأساسي ببساطة» de Nabd Wall Street (vídeo y Short)
# en cola-nabd/<base>[-short]/ de la rama youtube-cola. Después, sin pasos a mano: youtube-Nabd.yml sube a YouTube; telegram-Nabd.yml publica
# post-telegram.txt (carpeta del vídeo) y buffer-Nabd.yml manda post-x.txt (vídeo) a X y, con el Short, post-linkedin.txt a LinkedIn,
# post-tiktok.txt a TikTok y post-instagram.txt a Instagram (Reel). Igual que nabd/diario/encolar.sh.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/nabd-scratch}; mkdir -p $S
for f in $BASE-Nabd.mp4 short-$BASE-Nabd.mp4 meta-youtube-$BASE-Nabd.json meta-short-$BASE-Nabd.json miniatura-$BASE-Nabd.png post-x-$BASE-Nabd.txt \
         post-telegram-$BASE-Nabd.txt post-linkedin-$BASE-Nabd.txt post-tiktok-$BASE-Nabd.txt post-instagram-$BASE-Nabd.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
ID=UCRU3n034y5dJBEGnhAKjhfQ
grep -q "$ID" $B/meta-youtube-$BASE-Nabd.json && grep -q "$ID" $B/meta-short-$BASE-Nabd.json || { echo "falta el enlace del canal"; exit 1; }
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-nabd)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-nabd/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (Nabd) en 24 h:',n); assert n<=7, 'límite de YouTube (~10/24 h por canal): espera antes de encolar'
PY
C=cola-nabd/$BASE; CS=cola-nabd/$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C $CS
cp $B/$BASE-Nabd.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-Nabd.json $C/meta.json; cp $B/miniatura-$BASE-Nabd.png $C/miniatura.png
cp $B/short-$BASE-Nabd.mp4 $CS/video.mp4; cp $B/meta-short-$BASE-Nabd.json $CS/meta.json
TZ=Asia/Riyadh date +%F' '%H:%M > $C/encolado.txt
git add $C $CS; git commit -qm "Cola Nabd: serie fundamental, $BASE (vídeo y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, con el vídeo ya en la rama (Buffer toma el vídeo del Short desde GitHub).
cp $B/post-x-$BASE-Nabd.txt $C/post-x.txt; cp $B/post-telegram-$BASE-Nabd.txt $C/post-telegram.txt
cp $B/post-linkedin-$BASE-Nabd.txt $CS/post-linkedin.txt; cp $B/post-tiktok-$BASE-Nabd.txt $CS/post-tiktok.txt; cp $B/post-instagram-$BASE-Nabd.txt $CS/post-instagram.txt
git add $C $CS; git diff --cached --quiet || git commit -qm "Cola Nabd: posts de la serie fundamental, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "fundamental Nabd $BASE: YouTube $V, Short $SH" | tee -a $B/ids.txt
