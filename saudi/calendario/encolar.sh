#!/bin/bash
# bash encolar.sh <carpeta de la semana>: encola el Short «تقويم النتائج الأسبوعي» (Saudi Arabia AI Stocks) en cola-sa/calendar-<base>-short/
# de la rama youtube-cola. Es un Short sin vídeo largo, así que todos los posts van en su carpeta:
# youtube-saudi.yml lo sube a YouTube (con portada), buffer.yml publica en X, Threads y Facebook (enlace al Short), LinkedIn (vídeo nativo),
# TikTok e Instagram (Reel), y telegram-saudi.yml en Telegram (portada + texto). Encolar el sábado entre las 20:00 y las 21:00 de Riad.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/short.json'))['base'])"); S=${SCRATCH:-/tmp/saudi-cal-scratch}; mkdir -p $S
for f in short-$BASE-saudi.mp4 meta-short-$BASE-saudi.json thumbnail-$BASE-saudi.png post-x-$BASE-saudi.txt post-threads-$BASE-saudi.txt \
         post-facebook-$BASE-saudi.txt post-linkedin-$BASE-saudi.txt post-tiktok-$BASE-saudi.txt post-instagram-$BASE-saudi.txt post-telegram-$BASE-saudi.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "SaudiArabiaAIStocks" $B/meta-short-$BASE-saudi.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
for p in threads facebook linkedin tiktok instagram telegram; do grep -q "SaudiArabiaAIStocks" $B/post-$p-$BASE-saudi.txt || { echo "falta el enlace del canal en post-$p"; exit 1; }; done
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
print('subidas a YouTube (Arabia Saudita) en 24 h:',n); assert n<=9, 'límite de YouTube (~10/24 h, compartido con el diario, la serie y los resultados): espera antes de encolar'
PY
CS=cola-sa/calendar-$BASE-short
[ -e $CS ] && { echo "ya encolado: $CS"; exit 1; }
mkdir -p $CS
cp $B/short-$BASE-saudi.mp4 $CS/video.mp4; cp $B/meta-short-$BASE-saudi.json $CS/meta.json; cp $B/thumbnail-$BASE-saudi.png $CS/miniatura.png
git add cola-sa; git commit -qm "Cola Arabia Saudita: calendario semanal de resultados, $BASE (Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Posts en un segundo push, con el vídeo ya en la rama (Buffer toma el vídeo desde GitHub)
for p in x threads facebook linkedin tiktok instagram telegram; do cp $B/post-$p-$BASE-saudi.txt $CS/post-$p.txt; done
git add cola-sa; git diff --cached --quiet || git commit -qm "Cola Arabia Saudita: posts del calendario semanal, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $CS/resultado.json ] && break; sleep 15; done
SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "calendario $BASE: Short $SH" | tee -a $B/ids.txt
