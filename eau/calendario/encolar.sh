#!/bin/bash
# bash encolar.sh <carpeta de la semana>: encola el Short «تقويم النتائج الأسبوعي» en cola-eau/calendario-<fecha>/ de la rama youtube-cola.
# youtube-eau.yml lo sube a YouTube (@AIStocksUAE); buffer.yml publica en X, LinkedIn (el Short como video nativo), Facebook
# (mismo texto que LinkedIn), TikTok, Instagram y Threads (solo si Threads está conectado en Buffer EAU); telegram-eau.yml en Telegram.
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/info.json'))['fecha'])"); S=${SCRATCH:-/tmp/eau-scratch}; mkdir -p $S
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-eau/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube EAU en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido): espera antes de encolar'
PY
C=cola-eau/calendario-$F
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C
cp $B/short-calendario-$F-UAE.mp4 $C/video.mp4; cp $B/meta-short-$F-UAE.json $C/meta.json
git add cola-eau; git commit -qm "Cola EAU: calendario semanal de resultados $F (Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, cuando el video ya está en la rama (Buffer toma el video desde GitHub).
for r in x linkedin tiktok instagram telegram threads; do cp $B/post-$r-$F-UAE.txt $C/post-$r.txt; done
git add cola-eau; git diff --cached --quiet || git commit -qm "Cola EAU: posts del calendario semanal $F"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 60); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); echo "calendario EAU $F: Short $V" | tee -a $B/ids.txt
