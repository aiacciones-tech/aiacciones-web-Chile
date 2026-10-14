#!/bin/bash
# encolar.sh <id> : valida y encola vídeo+Short de /mnt/project-files/espana/<id>, espera subida y Buffer, rellena ficha-web.py
set -e
ID=$1; B=/mnt/project-files/espana/$ID; S=${SCRATCH:-/tmp/es-scratch}; mkdir -p $S
[ -d $S/cola ] || git clone -q -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
python3 -c "
import json;m=json.load(open('$B/meta-youtube.json'));d=m['description']
assert len(m['title'])<=100 and m['privacy']=='public' and '<' not in d and '>' not in d and 'AVISO IMPORTANTE' in d and len(d.encode())<5000
s=json.load(open('$B/meta-short.json'));assert '{video:$ID-1S26}' in s['description'] and s['privacy']=='public'
print('meta ok',len(m['title']),len(d.encode()))"
C=cola-es/$ID-1S26; CS=cola-es/$ID-1S26-short; mkdir -p $C $CS
cp $B/youtube-$ID-1S26-con-voz.mp4 $C/video.mp4; cp $B/meta-youtube.json $C/meta.json; cp $B/miniatura-youtube.png $C/miniatura.png
cp $B/post-linkedin-1S26.txt $C/post-linkedin.txt; cp $B/post-x-1S26.txt $C/post-x.txt
cp $B/short-$ID-1S26.mp4 $CS/video.mp4; cp $B/meta-short.json $CS/meta.json
git add $C $CS; git commit -qm "Cola España: $ID 1S26 (vídeo, Short, posts LinkedIn y X)

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015cVN5AA7UoW9HnZg8n5edQ"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/buffer.json ] && [ -f $C/buffer-linkedin.json ] && [ -f $CS/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
sed -i "s/\"VIDEO_ID\"/\"$V\"/; s/\"SHORT_ID\"/\"$SH\"/" $B/ficha-web.py
X=$(python3 -c "import json;print(json.load(open('$C/buffer.json'))['id'])"); L=$(python3 -c "import json;print(json.load(open('$C/buffer-linkedin.json'))['id'])")
P=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['privacy'])")
echo "$ID: YouTube $V ($P), Short $SH, X $X, LinkedIn $L" | tee -a $S/bancos-ids.txt
