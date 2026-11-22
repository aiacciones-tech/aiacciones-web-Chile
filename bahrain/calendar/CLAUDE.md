# Bahrain AI Stocks · «تقويم النتائج الأسبوعي» (weekly results-calendar Short)

Daniel's format (22-nov-2026). Every Saturday, out between 20:00 and 21:00 Manama, before Bahrain Bourse opens on Sunday.
Reply to Daniel in Spanish; everything the viewer sees or hears is in Arabic. These instructions prevail over the scheduled task text.

## Content
- Short 9:16, **45–60 s** (the renderer warns outside that range), voice Azure **ar-BH-AliNeural** at +15% (Ali is slow: ~1.8 words/s,
  so ~90 voice words in total). Numbers in words in the voice lines, rounded ("نحو دولار ونصف"); exact figures on screen.
- 5–7 most relevant companies reporting that week: first Bahrain Bourse (Sun–Thu; if few, large Gulf banks), then large US companies
  (Mon–Fri), in chronological order. Per company: name + ticker, day and timing (before open / after close), consensus EPS and revenue.
  ~6–7 s per company.
- Script: 1) hook (3 s): «هذا الأسبوع تعلن [the most important], و[N] شركات أخرى.» 2) companies 3) close: «تابع القناة لتحليل النتائج…»
  and the disclaimer «محتوى إعلامي، وليس توصية استثمارية.»
- If no Bahraini/Gulf company reports (between results seasons), say so in one short "note" slide (as on 22-nov-2026).
- **US companies → recommend @NabdWallStreet** (Daniel, 22-nov-2026): in the closing voice line, the outro slide and every text
  (YouTube description, X, Threads, TikTok/Instagram, Telegram, LinkedIn). `enqueue-calendar-bahrain.sh` checks it.
- US holidays that week (market closed / half day): one short clause.

## Verify the data (never invent)
- Dates: the company's own notice (IR page, PR Newswire/GlobeNewswire/Business Wire). Calendar sites (TheStreet "est.", Digrin,
  nextearningsdate) are often stale or estimated: a date marked estimated, or only on one calendar site, is dropped.
  On 22-nov-2026 TheStreet still listed NVIDIA for 25-nov although it had reported the week before.
- Consensus: Earnings Whispers previews (finviz.com/news/… and earningswhispers.com/article/<TICKER>/…) dated in the days before,
  cross-checked with another source when available (TheStreet week page, Digrin, Zacks, Barchart). Show one source's figures,
  consistently, and name it and its date in the footer `source`. A company without any consensus keeps its date, without eps/rev.
- Bahrain/Gulf: Bahrain Bourse disclosures, Argaam, Zawya, Mubasher, GDN, Daily Tribune. Quarterly deadline: 45 days after quarter end
  (3T: 14-nov; annual results Feb–March; 1T: mid-May; 2T: mid-August).
- Write `script-<week>-bahrain.md` with the voice lines and a table of sources (date source, consensus source, cross-check).

## Steps (week = the Sunday that starts the Bahrain week, e.g. 2026-11-22)
1. Folder `bahrain/calendar/<week>-bahrain/`: `short-<week>-bahrain.json` (copy the 2026-11-22 one; slide types in
   `make-calendar-bahrain.py`), `meta-short-…json`, `post-{x,threads,tiktok,instagram,telegram,linkedin}-<week>-bahrain.txt`,
   `script-…md`. Telegram is plain text (no HTML). LinkedIn follows the permanent rule (3–4 facts with figures, conclusion,
   «🎥 فيديو من إعداد قناة أسهم البحرين بالذكاء الاصطناعي (Bahrain AI Stocks)», disclaimer, last line the channel link).
2. Preview: `python3 make-calendar-bahrain.py <week>-bahrain/short-<week>-bahrain.json --preview --outdir /mnt/project-files/bahrain-pipeline/calendar-bahrain/<week>`; look at the PNGs.
3. Commit and push to the claude/** branch: `voz-calendar-bahrain.yml` makes the Azure wavs (key: Saudi's or Nabd's, shared F0 quota).
   `bash get-voice-calendar-bahrain.sh <week> <scratch>/voz` waits and copies them.
4. Render: `VOZ_DIR=<scratch>/voz/<week>-bahrain python3 make-calendar-bahrain.py … --outdir /mnt/project-files/bahrain-pipeline/calendar-bahrain/<week>`.
   Over 60 s: shorten voice lines and repeat 3–4. No Azure voice: render all with `--piper` (never mix) and say so.
5. Publish: `bash enqueue-calendar-bahrain.sh <week>` (waits until 20:02 Manama; `NOW=1` skips the wait). Copy the texts to the
   project-files folder too. Then open a PR with the week folder, and tell Daniel in the thread (Spanish): companies, length, links.
