#!/usr/bin/env python3
"""Bahrain AI Stocks: weekly results-calendar Short (تقويم النتائج الأسبوعي), 1080x1920, from a JSON spec.

  python3 make-calendar-bahrain.py <week>/short-<week>.json --preview [--outdir D]   # PNG of every slide
  VOZ_DIR=<wavs> python3 make-calendar-bahrain.py <week>/short-<week>.json [--outdir D]  # MP4 with the Azure voice
  python3 make-calendar-bahrain.py ... --piper    # Piper fallback (bahrain-pipeline/voice/ar_JO-kareem), never mixed with Azure
  python3 make-calendar-bahrain.py ... --silent   # timing check without voice

Slide types: hook (title, subtitle, days [[day, [tickers]]]), note (kicker, title, subtitle), company (n, day, when, name, ticker,
eps, rev; eps/rev optional: a missing estimate is simply left out), outro (title, items). Every slide needs "voice".
Outputs go to --outdir (default: the spec's folder); also writes cover.png (first slide) for Telegram/Threads.
"""
import html, json, os, re, shutil, subprocess, sys, tempfile, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from voz_calendar_bahrain import clave  # noqa: E402

PIPE = "/mnt/project-files/bahrain-pipeline"
FONTS = os.environ.get("FONTS_BH", os.path.join(PIPE, "fonts"))
PIPER_VOICE = os.path.join(PIPE, "voice", "ar_JO-kareem-medium.onnx")
DISCLAIMER = "محتوى إعلامي، وليس توصية استثمارية"
PAUSE, FPS, W, H = 0.35, 30, 1080, 1920

CSS = """
@font-face { font-family: T; src: url('file://@FONTS@/Tajawal-Regular.ttf'); font-weight: 400; }
@font-face { font-family: T; src: url('file://@FONTS@/Tajawal-Bold.ttf'); font-weight: 700; }
@font-face { font-family: T; src: url('file://@FONTS@/Tajawal-ExtraBold.ttf'); font-weight: 800; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; }
body { font-family: T, sans-serif; direction: rtl; color: #fff;
  background: radial-gradient(ellipse at 50% -10%, #b3122e 0%, #7a0b1f 38%, #3d0610 100%); position: relative; }
.serr { position: absolute; top: 0; bottom: 0; left: 0; width: 90px; background: #fff; opacity: .06;
  clip-path: polygon(0 0, 60% 0, 100% 10%, 60% 20%, 100% 30%, 60% 40%, 100% 50%, 60% 60%, 100% 70%, 60% 80%, 100% 90%, 60% 100%, 0 100%); }
.head { position: absolute; top: 150px; right: 70px; left: 130px; display: flex; justify-content: space-between; align-items: center; }
.head .co { font-size: 36px; color: #f3d6db; font-weight: 700; }
.logo { width: 96px; height: 96px; border-radius: 50%; background: #fff; color: #a8102a; display: flex; flex-direction: column;
  align-items: center; justify-content: center; font-weight: 800; line-height: .9; box-shadow: 0 0 0 4px rgba(255,255,255,.25); }
.logo b { font-size: 38px; font-family: Arial, sans-serif; } .logo span { font-size: 22px; }
.foot { position: absolute; bottom: 260px; left: 120px; right: 70px; text-align: center; font-size: 25px; color: #e7bcc4; line-height: 1.6; }
.main { position: absolute; top: 300px; bottom: 420px; left: 120px; right: 70px; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center; }
h1 { font-size: 92px; font-weight: 800; line-height: 1.2; }
.kicker { font-size: 44px; font-weight: 700; color: #ffd0d7; margin-bottom: 26px; }
.sub { font-size: 46px; color: #f3d6db; margin-top: 30px; line-height: 1.4; }
.rule { width: 220px; height: 6px; background: #fff; margin: 34px auto 0; border-radius: 3px; opacity: .85; }
.days { width: 100%; margin-top: 50px; }
.dayrow { display: flex; align-items: center; gap: 20px; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,.2); }
.dayrow .d { width: 270px; text-align: right; font-size: 40px; font-weight: 700; color: #ffe1e6; flex: none; }
.chips { display: flex; flex-wrap: wrap; gap: 14px; }
.chip { background: #fff; color: #a8102a; font-family: Arial, sans-serif; font-weight: 800; font-size: 38px; padding: 8px 22px; border-radius: 12px; }
.chip.ar { font-family: T, sans-serif; background: rgba(255,255,255,.16); color: #fff; font-weight: 700; }
.pill { display: inline-flex; gap: 18px; align-items: center; background: rgba(255,255,255,.14); border: 2px solid rgba(255,255,255,.35);
  border-radius: 60px; padding: 14px 34px; font-size: 42px; font-weight: 700; }
.pill .w { color: #ffd0d7; font-weight: 400; }
.name { font-size: 100px; font-weight: 800; line-height: 1.15; margin-top: 50px; }
.tk { margin-top: 22px; display: inline-block; background: #fff; color: #a8102a; font-family: Arial, sans-serif; font-weight: 800;
  font-size: 50px; padding: 8px 30px; border-radius: 14px; direction: ltr; }
.cards { width: 100%; margin-top: 60px; display: flex; flex-direction: column; gap: 28px; }
.card { background: rgba(0,0,0,.22); border: 2px solid rgba(255,255,255,.18); border-radius: 26px; padding: 26px 34px; text-align: right; }
.card .l { font-size: 36px; color: #f3d6db; }
.card .v { font-size: 64px; font-weight: 800; margin-top: 6px; }
.est { font-size: 30px; color: #e7bcc4; margin-top: 22px; }
.num { position: absolute; top: 270px; left: 130px; font-size: 32px; color: #e7bcc4; font-family: Arial, sans-serif; direction: ltr; }
ul { list-style: none; font-size: 54px; line-height: 1.5; margin-top: 40px; }
li { margin: 18px 0; } li.t { font-size: 44px; color: #f3d6db; margin-bottom: 0; }
li.h { font-family: Arial, sans-serif; font-weight: 800; direction: ltr; }
"""


def esc(t):
    return html.escape(str(t))


def num(t):
    """Numbers and Latin text keep left-to-right order inside the Arabic line."""
    return re.sub(r"([0-9][0-9.,]*)", r'<bdi dir="ltr">\1</bdi>', esc(t))


def body(sl):
    t = sl["type"]
    if t == "hook":
        rows = "".join(
            f'<div class="dayrow"><div class="d">{esc(d)}</div><div class="chips">'
            + "".join(f'<span class="chip{" ar" if re.search(r"[؀-ۿ]", x) else ""}">{esc(x)}</span>' for x in tk)
            + "</div></div>" for d, tk in sl.get("days", []))
        return (f'<h1>{esc(sl["title"])}</h1><div class="sub">{num(sl.get("subtitle", ""))}</div><div class="rule"></div>'
                f'<div class="days">{rows}</div>')
    if t == "note":
        return (f'<div class="kicker">{esc(sl.get("kicker", ""))}</div><h1>{esc(sl["title"])}</h1>'
                f'<div class="sub">{num(sl.get("subtitle", ""))}</div><div class="rule"></div>')
    if t == "company":
        cards = ""
        for k, lbl in (("eps", "ربحية السهم المتوقعة"), ("rev", "الإيرادات المتوقعة")):
            if sl.get(k):
                cards += f'<div class="card"><div class="l">{lbl}</div><div class="v">{num(sl[k])}</div></div>'
        return (f'<div class="pill">{num(sl["day"])}<span class="w">· {esc(sl.get("when", ""))}</span></div>'
                f'<div class="name">{esc(sl["name"])}</div><div class="tk">{esc(sl["ticker"])}</div>'
                + (f'<div class="cards">{cards}</div><div class="est">متوسط تقديرات المحللين للربع</div>' if cards else ""))
    if t == "outro":
        items = "".join(f'<li class="h">{esc(i)}</li>' if i.startswith("@") or not re.search(r"[؀-ۿ]", i)
                        else f'<li class="t">{esc(i)}</li>' for i in sl.get("items", []))
        return f'<h1>{esc(sl["title"])}</h1><div class="rule"></div><ul>{items}</ul>'
    sys.exit(f"Unknown slide type {t!r}")


def page(spec, sl):
    head = (f'<div class="head"><div class="co">تقويم النتائج الأسبوعي · {esc(spec.get("range", ""))}</div>'
            f'<div class="logo"><b>AI</b><span>أسهم</span></div></div>')
    n = f'<div class="num">{esc(sl["n"])}</div>' if sl.get("n") else ""
    foot = f'<div class="foot">{esc(spec.get("source", ""))}<br>BAHRAIN AI STOCKS · {DISCLAIMER}</div>'
    return (f'<!doctype html><html lang="ar"><head><meta charset="utf-8"><style>{CSS.replace('@FONTS@', FONTS)}</style></head>'
            f'<body><div class="serr"></div>{head}{n}<div class="main">{body(sl)}</div>{foot}</body></html>')


def dur(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate()


def main():
    a = sys.argv[1:]
    args = [x for x in a if not x.startswith("--")]
    if not args:
        sys.exit(__doc__)
    preview, silent, piper = "--preview" in a, "--silent" in a, "--piper" in a
    spec_path = os.path.abspath(args[0])
    outdir = os.path.abspath(a[a.index("--outdir") + 1]) if "--outdir" in a else os.path.dirname(spec_path)
    if "--outdir" in a:
        args = [x for x in args if os.path.abspath(x) != outdir]
    os.makedirs(outdir, exist_ok=True)
    spec = json.load(open(spec_path, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="cal-")
    jobs = []
    for i, sl in enumerate(spec["slides"]):
        h = os.path.join(tmp, f"s{i:02d}.html")
        open(h, "w", encoding="utf-8").write(page(spec, sl))
        jobs.append({"html": h, "out": os.path.join(tmp, f"s{i:02d}.png"), "w": W, "h": H})
    jp = os.path.join(tmp, "jobs.json"); json.dump(jobs, open(jp, "w"))
    subprocess.run(["node", os.path.join(PIPE, "shoot-bahrain.js"), jp], check=True)
    shutil.copy(jobs[0]["out"], os.path.join(outdir, "cover.png"))
    if preview:
        pd = os.path.join(outdir, "preview"); os.makedirs(pd, exist_ok=True)
        for j in jobs:
            shutil.copy(j["out"], pd)
        print("Preview:", pd); return
    vd = os.environ.get("VOZ_DIR", "")
    if not (silent or piper):
        miss = [sl["voice"] for sl in spec["slides"] if not os.path.isfile(os.path.join(vd, clave(sl["voice"]) + ".wav"))]
        if not vd or miss:
            sys.exit(f"VOZ_DIR has no Azure wav for {len(miss)} line(s): run the voice workflow again, or render all with --piper.")
    parts, total = [], 0.0
    for i, sl in enumerate(spec["slides"]):
        wav = os.path.join(tmp, f"s{i:02d}.wav")
        if silent:
            d = max(3.0, len(sl["voice"]) / 14.0)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{d:.2f}", wav], check=True)
        elif piper:
            subprocess.run([sys.executable, "-m", "piper", "-m", PIPER_VOICE, "-f", wav, "--length-scale", "0.95"],
                           input=sl["voice"].encode(), check=True, capture_output=True)
        else:
            shutil.copy(os.path.join(vd, clave(sl["voice"]) + ".wav"), wav)
        d = dur(wav) + PAUSE; total += d
        seg = os.path.join(tmp, f"s{i:02d}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", jobs[i]["out"], "-i", wav,
                        "-af", f"apad=whole_dur={d:.2f}", "-t", f"{d:.2f}",
                        "-vf", f"fade=t=in:st=0:d=0.25,fade=t=out:st={max(0, d - 0.25):.2f}:d=0.25,format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2",
                        seg], check=True)
        parts.append(seg)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    out = os.path.join(outdir, spec.get("out", "short-calendar-bahrain.mp4"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out], check=True)
    print(f"{out}: {total:.1f} s" + (" (SILENT)" if silent else " (Piper)" if piper else " (Azure)"))
    if not 45 <= total <= 60:
        print("WARNING: the Short must last 45-60 s; adjust the voice lines.")
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
