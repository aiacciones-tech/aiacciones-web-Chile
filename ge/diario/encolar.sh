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
CUPO=$(cd "$(dirname "$0")/.." && pwd)/cupo.py   # cupo de subidas a YouTube (regla de Daniel, 24-nov-2026: nunca pasar el límite)
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/ge-scratch}; mkdir -p $S
for f in video-bolsa-$F-GE.mp4 short-bolsa-$F-GE.mp4 meta-youtube-$F-GE.json meta-short-$F-GE.json miniatura-$F-GE.png; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
ID=UC23KiHTq_lULliZwAM3dEpA
grep -q "$ID" $B/meta-youtube-$F-GE.json && grep -q "$ID" $B/meta-short-$F-GE.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
# prioridad alta: espera (hasta 3 h) a que quepan 2 subida(s) sin pasar el límite diario (ge/cupo.py)
for i in $(seq 18); do git pull -q origin youtube-cola 2>/dev/null; python3 $CUPO alta 2 && break; [ $i = 18 ] && { echo "sin cupo de YouTube tras 3 h: no se encola"; exit 1; }; sleep 600; done
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
# Shorts extra del mismo guion (short-2 / short-3, desde el 24-nov-2026): no van a cola-ge/ (se subirían ya), sino a cola-ge-espera/
# con publicar.txt (hora UTC); cola-espera-GE.yml los pasa a cola-ge/ a su hora y lanza youtube-GE.yml (y después buffer-GE.yml: TikTok e Instagram).
# Horas de Berlín del día en que se encola: Short 2 a las 12:15, Short 3 a las 15:05 (antes de la apertura de Nueva York a las 15:30). El DAX va a las 18:30-20:00.
EXTRA=0
for k in 2 3; do
  [ -s $B/short-$k-bolsa-$F-GE.mp4 ] && [ -s $B/meta-short$k-$F-GE.json ] || continue
  grep -q "$ID" $B/meta-short$k-$F-GE.json || { echo "falta el enlace del canal en meta-short$k"; continue; }
  E=cola-ge-espera/bolsa-$F-short$k; [ -d $E ] || [ -d cola-ge/bolsa-$F-short$k ] && { echo "ya encolado: bolsa-$F-short$k"; continue; }
  mkdir -p $E; cp $B/short-$k-bolsa-$F-GE.mp4 $E/video.mp4; cp $B/meta-short$k-$F-GE.json $E/meta.json
  [ -s $B/post-tiktok-short$k-$F-GE.txt ] && cp $B/post-tiktok-short$k-$F-GE.txt $E/post-tiktok.txt
  [ -s $B/post-instagram-short$k-$F-GE.txt ] && cp $B/post-instagram-short$k-$F-GE.txt $E/post-instagram.txt
  H=$([ $k = 2 ] && echo "12:15" || echo "15:05")
  python3 -c "import datetime as d,zoneinfo as z;b=z.ZoneInfo('Europe/Berlin');h,m=map(int,'$H'.split(':'));print(d.datetime.combine(d.datetime.now(b).date(),d.time(h,m),b).astimezone(d.timezone.utc).isoformat(timespec='minutes'))" > $E/publicar.txt
  echo "Short $k en espera hasta $(cat $E/publicar.txt) (UTC)"; EXTRA=1
done
if [ $EXTRA = 1 ]; then
  git add cola-ge-espera; git commit -qm "Cola GE: Shorts extra del $F (en espera)"
  for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
fi
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario GE $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
