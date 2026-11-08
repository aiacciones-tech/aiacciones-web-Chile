#!/bin/bash
# bash encolar.sh <carpeta del día>: encola el video diario en árabe y su Short en cola-sa/bolsa-<fecha>[-short]/ de la rama youtube-cola.
# Después: youtube-saudi.yml sube a YouTube (@SaudiArabiaAIStocks), buffer.yml publica en X, Threads y Facebook (video largo)
# y en LinkedIn, TikTok e Instagram (Short como video nativo/Reel), y telegram-saudi.yml en Telegram (post-telegram.txt).
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/saudi-scratch}; mkdir -p $S
for f in video-bolsa-$F-SA.mp4 short-bolsa-$F-SA.mp4 meta-youtube-$F-SA.json meta-short-$F-SA.json miniatura-$F-SA.png post-x-$F-SA.txt post-threads-$F-SA.txt \
         post-facebook-$F-SA.txt post-linkedin-$F-SA.txt post-tiktok-$F-SA.txt post-instagram-$F-SA.txt post-telegram-$F-SA.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q "SaudiArabiaAIStocks" $B/meta-youtube-$F-SA.json && grep -q "SaudiArabiaAIStocks" $B/meta-short-$F-SA.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
for p in x threads facebook linkedin tiktok instagram telegram; do grep -q "SaudiArabiaAIStocks" $B/post-$p-$F-SA.txt || { echo "falta el enlace del canal en post-$p"; exit 1; }; done
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-sa/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (Arabia Saudita) en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido con los videos de resultados): espera antes de encolar'
PY
C=cola-sa/bolsa-$F; CS=cola-sa/bolsa-$F-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C $CS
cp $B/video-bolsa-$F-SA.mp4 $C/video.mp4; cp $B/meta-youtube-$F-SA.json $C/meta.json; cp $B/miniatura-$F-SA.png $C/miniatura.png
cp $B/short-bolsa-$F-SA.mp4 $CS/video.mp4; cp $B/meta-short-$F-SA.json $CS/meta.json
git add cola-sa; git commit -qm "Cola Arabia Saudita: video diario de la bolsa $F (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, cuando el video ya está en la rama (Buffer toma el video del Short desde GitHub).
cp $B/post-x-$F-SA.txt $C/post-x.txt; cp $B/post-threads-$F-SA.txt $C/post-threads.txt; cp $B/post-facebook-$F-SA.txt $C/post-facebook.txt
cp $B/post-telegram-$F-SA.txt $C/post-telegram.txt
# LinkedIn (Daniel, 8-nov-2026): el Short como video nativo -> post-linkedin.txt en la carpeta -short (buffer.py lo sube con el video.mp4).
# En cola-sa, Facebook usaría post-linkedin.txt como texto alterno; en la carpeta -short se marca como hecho para que no se duplique.
cp $B/post-linkedin-$F-SA.txt $CS/post-linkedin.txt
echo '{"omitido": "Facebook va en la carpeta del video largo (post-facebook.txt)"}' > $CS/buffer-facebook.json
cp $B/post-tiktok-$F-SA.txt $CS/post-tiktok.txt; cp $B/post-instagram-$F-SA.txt $CS/post-instagram.txt
git add cola-sa; git diff --cached --quiet || git commit -qm "Cola Arabia Saudita: posts del video diario $F"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario Arabia Saudita $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
