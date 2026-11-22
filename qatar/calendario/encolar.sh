#!/bin/bash
# bash encolar.sh <carpeta de la semana>: encola el Short «تقويم النتائج الأسبوعي» en cola-qa/calendario-<semana>-short/ de la rama youtube-cola.
# Después: youtube-qatar.yml lo sube a YouTube (@QatarAIStocks), buffer.yml publica en X y Threads (Buffer 1) y en TikTok e Instagram
# (Buffer 2), y telegram-qatar.yml en Telegram (la carpeta -short trae su propio post-telegram.txt). {youtube} = enlace del Short.
# Redes pedidas por Daniel (22-nov-2026): YouTube Shorts, X, TikTok, Telegram, Instagram y Threads (sin LinkedIn ni Facebook).
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/calendario.json'))['semana'])"); S=${SCRATCH:-/tmp/qa-scratch}; mkdir -p $S
for f in short-calendario-$F-qatar.mp4 meta-short-$F-qatar.json post-x-$F-qatar.txt post-threads-$F-qatar.txt post-telegram-$F-qatar.txt \
         post-tiktok-$F-qatar.txt post-instagram-$F-qatar.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "youtube.com/@QatarAIStocks" $B/meta-short-$F-qatar.json || { echo "falta el enlace del canal"; exit 1; }
if [ ! -d $S/colaf ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/colaf
  (cd $S/colaf && git sparse-checkout set cola-qa)
fi
cd $S/colaf; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-qa/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube Qatar en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido): espera antes de encolar'
PY
CS=cola-qa/calendario-$F-short
[ -e $CS ] && { echo "ya encolado: $CS"; exit 1; }
mkdir -p $CS
cp $B/short-calendario-$F-qatar.mp4 $CS/video.mp4; cp $B/meta-short-$F-qatar.json $CS/meta.json
TZ=Asia/Qatar date +%F' '%H:%M > $CS/encolado.txt
git add cola-qa; git commit -qm "Cola Qatar: calendario semanal de resultados $F (Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, con el video ya en la rama (Buffer toma el video del Short desde GitHub).
for r in x threads telegram tiktok instagram; do cp $B/post-$r-$F-qatar.txt $CS/post-$r.txt; done
git add cola-qa; git diff --cached --quiet || git commit -qm "Cola Qatar: posts del calendario semanal $F"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $CS/resultado.json ] && break; sleep 15; done
SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "calendario Qatar $F: Short $SH" | tee -a $B/ids-$F-qatar.txt
