#!/bin/bash
# bash enqueue-calendar-bahrain.sh <week>   e.g. 2026-11-22
# Queues the weekly results-calendar Short in cola-bahrain/calendar-<week>-short/ of branch youtube-cola. Then youtube-bahrain.yml
# uploads it to YouTube (@BahrainAIStocks), buffer.yml posts it to X, Threads, TikTok, Instagram and LinkedIn (Short as video)
# and telegram-bahrain.yml to Telegram. Texts from bahrain/calendar/<week>-bahrain/, video and cover from
# /mnt/project-files/bahrain-pipeline/calendar-bahrain/<week>/. PRIVACY=public by default.
set -e
WK=${1:?week}; HERE=$(cd "$(dirname "$0")" && pwd); T=$HERE/$WK-bahrain; M=/mnt/project-files/bahrain-pipeline/calendar-bahrain/$WK
S=${SCRATCH:-/tmp/bahrain-cal-scratch}; mkdir -p $S
for f in $T/meta-short-$WK-bahrain.json $M/short-calendar-$WK-bahrain.mp4 $M/cover.png; do test -s $f || { echo "missing $f"; exit 1; }; done
for p in x threads tiktok instagram telegram linkedin; do
  f=$T/post-$p-$WK-bahrain.txt; test -s $f || { echo "missing $f"; exit 1; }
  grep -q "BahrainAIStocks\|{youtube}" $f || { echo "channel/video link missing in post-$p"; exit 1; }
done
python3 - "$T" "$WK" "$M" <<'EOF'
import json, sys, os, re, subprocess
t, wk, m = sys.argv[1:4]
d = json.load(open(f"{t}/meta-short-{wk}-bahrain.json", encoding="utf-8"))
assert len(d["title"]) <= 100 and "youtube.com/@BahrainAIStocks" in d["description"]
assert "ليس توصية استثمارية" in d["description"]
li = open(f"{t}/post-linkedin-{wk}-bahrain.txt", encoding="utf-8").read().strip()
assert li.endswith("https://www.youtube.com/@BahrainAIStocks") and "فيديو من إعداد قناة" in li, "LinkedIn rule"
spec = json.load(open(f"{t}/short-{wk}-bahrain.json", encoding="utf-8"))
if re.search(r"[A-Z]{1,5}", " ".join(s.get("ticker", "") for s in spec["slides"])):  # US companies -> recommend Nabd (Daniel, 22-nov-2026)
    for n in ("x", "threads", "tiktok", "instagram", "telegram", "linkedin"):
        assert "NabdWallStreet" in open(f"{t}/post-{n}-{wk}-bahrain.txt", encoding="utf-8").read(), f"post-{n}: recommend @NabdWallStreet"
    assert "NabdWallStreet" in d["description"]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            f"{m}/short-calendar-{wk}-bahrain.mp4"], capture_output=True, text=True).stdout)
assert 45 <= dur <= 60, f"Short lasts {dur:.1f} s (45-60)"
print("checks ok, Short", round(dur, 1), "s")
EOF
# Daniel: it goes out on Saturday between 20:00 and 21:00 Manama. If it is earlier than 20:00 Manama, wait (at most 2 h).
W=$(python3 -c "import datetime as d,zoneinfo as z;n=d.datetime.now(z.ZoneInfo('Asia/Bahrain'));print(max(0,min(7200,int((n.replace(hour=20,minute=2,second=0)-n).total_seconds()))))")
[ "${NOW:-0}" = 1 ] || { [ "$W" -gt 0 ] && echo "waiting $W s for 20:02 Manama" && sleep $W; }
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola --filter=blob:none --sparse https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
cd $S/cola; git sparse-checkout set cola-bahrain >/dev/null 2>&1 || true; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
C=cola-bahrain/calendar-$WK-short
[ -f $C/resultado.json ] && { echo "already uploaded: $C"; cat $C/resultado.json; exit 0; }
mkdir -p $C
cp $M/short-calendar-$WK-bahrain.mp4 $C/video.mp4; cp $M/cover.png $C/miniatura.png
python3 - $T/meta-short-$WK-bahrain.json $C/meta.json "${PRIVACY:-public}" <<'EOF'
import json, sys; d = json.load(open(sys.argv[1], encoding="utf-8")); d["privacy"] = sys.argv[3]
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
EOF
git add cola-bahrain; git commit -qm "Cola Baréin: calendario semanal de resultados $WK"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# posts in a second push, once the video is on the branch (Buffer takes the Short's video from GitHub)
for p in x threads tiktok instagram telegram linkedin; do cp $T/post-$p-$WK-bahrain.txt $C/post-$p.txt; done
git add cola-bahrain; git commit -qm "Cola Baréin: posts del calendario semanal $WK"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
echo "Queued $C. Waiting for YouTube..."
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
[ -f $C/resultado.json ] || { echo "No resultado.json after 20 min: check 'Subir videos a YouTube (Baréin)'"; exit 2; }
cat $C/resultado.json; echo
sleep 240; git pull -q origin youtube-cola 2>/dev/null
for f in buffer.json buffer-threads.json buffer-tiktok.json buffer-instagram.json buffer-linkedin.json telegram.json; do [ -f $C/$f ] && { echo "-- $f"; cat $C/$f; echo; }; done
