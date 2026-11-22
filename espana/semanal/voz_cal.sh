#!/bin/bash
# Voz neuronal es-ES-AlvaroNeural (la del canal) para el Short «Calendario semanal de resultados».
# Uso (desde la raíz del repo): SCRATCH=/tmp/x bash espana/semanal/voz_cal.sh <carpeta de la semana> [rate, p. ej. +5%]
# Sube los textos a la rama datos-diario-es (voz/cal-<semana>-<hora>/textos.json), lanza voz-espana.yml, espera
# y deja los mp3 en <carpeta>/voz/short_<i>.mp3 (make_short_cal.py los usa solos; si falta alguno, usa Piper).
set -euo pipefail
D=$(cd "$1" && pwd); RATE=${2:-+0%}; REPO=$(pwd); S=${SCRATCH:-/tmp/es-scratch}; GH=aiacciones-tech/aiacciones-web-Chile
F=$(python3 -c "import json;print(json.load(open('$D/calendario.json'))['semana'])")
ID="cal-$F-$(date -u +%H%M%S)"; W="$S/voz-rama"; mkdir -p "$S"
rm -rf "$W"; git clone -q --depth 1 -b datos-diario-es "https://github.com/$GH.git" "$W" 2>&1 | grep -v -i moved || true
mkdir -p "$W/voz/$ID"
python3 - "$D/calendario.json" "$W/voz/$ID/textos.json" "$RATE" <<'PY'
import json,sys,os
sys.path.insert(0,os.path.join(os.getcwd(),"espana/semanal"))
S=json.load(open(sys.argv[1]))
E=[S["gancho"]]+S["empresas"]+[S["cierre"]]
T={f"short_{i}":e["voz"] for i,e in enumerate(E)}; T["_voz"]="es-ES-AlvaroNeural"; T["_rate"]=sys.argv[3]
json.dump(T,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
PY
cd "$W"; git add voz; git -c user.name=aiacciones-bot -c user.email=aiacciones-bot@users.noreply.github.com commit -qm "Textos de voz $ID"
for i in 1 2 3 4; do git push -q origin datos-diario-es 2>&1 | grep -v -i moved && break || true; git pull -q --rebase origin datos-diario-es; done
git ls-remote origin datos-diario-es | grep -q "$(git rev-parse HEAD)" || { git pull -q --rebase origin datos-diario-es; git push -q origin datos-diario-es; }
cd "$REPO"
gh workflow run voz-espana.yml --ref main -R $GH -f id="$ID" >/dev/null; sleep 8
RUN=$(gh run list -w voz-espana.yml -R $GH -L 1 --json databaseId -q '.[0].databaseId')
until [ "$(gh run view "$RUN" -R $GH --json status -q .status)" = completed ]; do sleep 10; done
[ "$(gh run view "$RUN" -R $GH --json conclusion -q .conclusion)" = success ] || { echo "voz-espana falló (run $RUN): se usará Piper"; exit 1; }
cd "$W"; git pull -q origin datos-diario-es 2>&1 | grep -v -i moved || true
mkdir -p "$D/voz"; rm -f "$D/voz/"*.mp3; cp voz/$ID/*.mp3 "$D/voz/"
echo "voz neuronal: $(ls "$D/voz" | wc -l) mp3 en $D/voz"
