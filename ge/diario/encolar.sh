#!/bin/bash
# bash encolar.sh <carpeta del día>: encola el video diario en alemán de Wall Street y su Short en cola-ge/bolsa-<fecha>[-short]/ de la rama youtube-cola.
# Después youtube-GE.yml los sube al canal Wall Street auf Deutsch.
# El post de Telegram (post-telegram-<fecha>-GE.txt) va como post-telegram.txt del video largo: telegram-GE.yml lo publica
# con la miniatura cuando el video ya está en YouTube. El post de LinkedIn (post-linkedin-<fecha>-GE.txt) va como
# post-linkedin.txt del Short: buffer-GE.yml lo manda a la página de LinkedIn con el Short adjunto. El post de X (post-x-<fecha>-GE.txt)
# va como post-x.txt del video largo: buffer-GE.yml lo manda a X con el enlace al video (si X no está conectado en Buffer, espera).
# El post de TikTok (post-tiktok-<fecha>-GE.txt) va como post-tiktok.txt del Short: buffer-GE.yml sube el Short a TikTok con ese texto.
# El de Instagram (post-instagram-<fecha>-GE.txt) va como post-instagram.txt del Short: buffer-GE.yml lo publica como Reel.
# El resto se queda en la carpeta del día.
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/ge-scratch}; mkdir -p $S
for f in video-bolsa-$F-GE.mp4 short-bolsa-$F-GE.mp4 meta-youtube-$F-GE.json meta-short-$F-GE.json miniatura-$F-GE.png; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
ID=UC23KiHTq_lULliZwAM3dEpA
grep -q "$ID" $B/meta-youtube-$F-GE.json && grep -q "$ID" $B/meta-short-$F-GE.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-ge/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (GE) en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h por canal): espera antes de encolar'
PY
C=cola-ge/bolsa-$F; CS=cola-ge/bolsa-$F-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C $CS
cp $B/video-bolsa-$F-GE.mp4 $C/video.mp4; cp $B/meta-youtube-$F-GE.json $C/meta.json; cp $B/miniatura-$F-GE.png $C/miniatura.png
[ -s $B/post-telegram-$F-GE.txt ] && cp $B/post-telegram-$F-GE.txt $C/post-telegram.txt
[ -s $B/post-x-$F-GE.txt ] && cp $B/post-x-$F-GE.txt $C/post-x.txt
cp $B/short-bolsa-$F-GE.mp4 $CS/video.mp4; cp $B/meta-short-$F-GE.json $CS/meta.json
[ -s $B/post-linkedin-$F-GE.txt ] && cp $B/post-linkedin-$F-GE.txt $CS/post-linkedin.txt
[ -s $B/post-tiktok-$F-GE.txt ] && cp $B/post-tiktok-$F-GE.txt $CS/post-tiktok.txt
[ -s $B/post-instagram-$F-GE.txt ] && cp $B/post-instagram-$F-GE.txt $CS/post-instagram.txt
git add cola-ge; git commit -qm "Cola GE: video diario de Wall Street $F (video y Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario GE $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
