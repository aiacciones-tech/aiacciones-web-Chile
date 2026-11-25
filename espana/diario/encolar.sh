#!/bin/bash
# bash encolar.sh <carpeta del día>: encola el vídeo diario del IBEX 35 y su Short en cola-es/bolsa-<fecha>[-short]/ de la rama youtube-cola.
# Después: youtube-espana.yml sube a YouTube, buffer.yml publica en X, LinkedIn, TikTok e Instagram y telegram-espana.yml en Telegram.
set -e
ENL=$(cd "$(dirname "$0")/.." && pwd)/enlaces_cola.py
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/es-scratch}; mkdir -p $S
[ -d $S/cola ] || git clone -q -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-es/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'])
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube España en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h): espera antes de encolar'
PY
C=cola-es/bolsa-$F; CS=cola-es/bolsa-$F-short
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C $CS
cp $B/youtube-bolsa-espana-$F.mp4 $C/video.mp4; cp $B/meta-youtube.json $C/meta.json; cp $B/miniatura-youtube.png $C/miniatura.png
# Prueba A/B de miniatura y título (ab-espana.yml alterna A y B por días y deja la ganadora)
[ -f $B/ab.json ] && [ -f $B/miniatura-youtube-b.png ] && { cp $B/ab.json $C/ab.json; cp $B/miniatura-youtube-b.png $C/miniatura-b.png; }
cp $B/post-x.txt $C/post-x.txt; cp $B/post-telegram.txt $C/post-telegram.txt
cp $B/short-bolsa-espana-$F.mp4 $CS/video.mp4; cp $B/meta-short.json $CS/meta.json
cp $B/post-tiktok.txt $CS/post-tiktok.txt; cp $B/post-tiktok.txt $CS/post-instagram.txt
# LinkedIn: el Short como vídeo, no como enlace (Daniel, 8-nov-2026)
cp $B/post-linkedin.txt $CS/post-linkedin.txt
# Enlaces a la sesión anterior y a las listas del canal (sustituyen a las pantallas finales, que la API no permite)
python3 $ENL $C/meta.json cola-es bolsa-$F; python3 $ENL $CS/meta.json cola-es bolsa-$F-short
# Segundo Short (opcional): se sube solo a YouTube a las 08:30 de Madrid del día siguiente (canal-espana.yml),
# para repartir las subidas y no publicar dos Shorts a la vez.
C2=cola-es-programado/bolsa-$F-short2
if [ -f $B/short2.json ] && [ -f $B/short2-bolsa-espana-$F.mp4 ] && [ -f $B/meta-short2.json ]; then
  mkdir -p $C2; cp $B/short2-bolsa-espana-$F.mp4 $C2/video.mp4
  python3 - $B/meta-short2.json $C2/meta.json <<'PY'
import json,sys,datetime as dt
from zoneinfo import ZoneInfo
m=json.load(open(sys.argv[1])); Z=ZoneInfo("Europe/Madrid")
m["publicar"]=dt.datetime.combine(dt.datetime.now(Z).date()+dt.timedelta(days=1),dt.time(8,30),Z).astimezone(dt.timezone.utc).isoformat(timespec="seconds")
json.dump(m,open(sys.argv[2],"w"),ensure_ascii=False,indent=1); print("segundo Short programado:",m["publicar"])
PY
  git add $C2
fi
git add $C $CS; git commit -qm "Cola España: vídeo diario del IBEX 35 $F (vídeo, Short y posts)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && [ -f $C/buffer.json ] && [ -f $CS/buffer-linkedin.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "diario $F: YouTube $V, Short $SH" | tee -a $B/ids.txt
