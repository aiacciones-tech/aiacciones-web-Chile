"""Daily candles of a Bahrain Bourse stock for a lesson of «التحليل الفني ببساطة» (@BahrainAIStocks, bahrain/educativo/).
TradingView charts of Bahrain are paid ("permission denied, group bahrain_dly"), so the candles come from Mubasher's public chart file
(the one its classic stock page draws: static.mubasher.info/.../File.Historical_Stock_Charts_Dir/<id>.csv, prices in BHD, since listing).
The file id is read from https://english-old.mubasher.info/markets/BB/stocks/<TICKER> (or taken from IDS). Runs in GitHub Actions
(educativo-bahrain.yml): Mubasher is blocked from Claude's container. Candles are frozen: if <out>/velas-bahrain.json exists they are not
fetched again (the figures said in the video must not change), unless REFRESCAR=1.
Usage: python3 lesson-data-bahrain.py <video-bahrain.json> <output folder>   ("simbolo": "BAHRAIN:ALBH"; "velas_n" optional, 520)"""
import json, os, re, sys, datetime as dt, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
TZH = 3 * 3600  # Manama
CSV = "https://static.mubasher.info/File.MubasherCharts/File.Historical_Stock_Charts_Dir/{}.csv"
IDS = {"NBB": "220ec8ce6abb3e952a85b8551ba726a1227", "ALBH": "591815ae3b9d6286f1b2a489ea4f3f4abaed"}  # found 20-nov-2026
txt = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")


def file_id(tk):
    try:
        m = re.search(r"Historical_Stock_Charts_Dir/([0-9a-f]{30,40})\.csv", txt(f"https://english-old.mubasher.info/markets/BB/stocks/{tk}"))
        if m: return m.group(1)
    except Exception as e:
        print("Mubasher page:", e)
    if tk in IDS: return IDS[tk]
    raise SystemExit(f"no Mubasher chart file for {tk}")


def velas(tk, n):
    fid = file_id(tk); out = []
    for l in txt(CSV.format(fid)).splitlines():
        p = l.strip().split(",")
        if len(p) < 6: continue
        o, h, lo, c, v = (float(x) for x in p[1:6])
        if min(o, h, lo, c) <= 0: continue  # Mubasher writes 0.0 on days without trades
        d = dt.datetime.strptime(p[0], "%Y-%m-%d/%H:%M:%S").replace(tzinfo=dt.timezone.utc)
        out.append({"t": int(d.timestamp()) - TZH + 12 * 3600, "o": o, "h": h, "l": lo, "c": c, "v": v})  # noon Manama: the UTC date is the session date
    return {"simbolo": "BAHRAIN:" + tk, "fuente": "Mubasher", "archivo": CSV.format(fid), "velas": out[-n:]}


if __name__ == "__main__":
    VJ = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); p = os.path.join(out, "velas-bahrain.json")
    if os.path.exists(p) and not os.environ.get("REFRESCAR"):
        print("candles already frozen:", p); sys.exit()
    D = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "series": {}}
    for s in [VJ["simbolo"]] + VJ.get("simbolos_extra", []):
        S = velas(s.split(":")[-1], VJ.get("velas_n", 520)); S["simbolo"] = s; D["series"][s] = S
        v = S["velas"]; ult = dt.datetime.fromtimestamp(v[-1]["t"], dt.timezone.utc).date()
        print(s, len(v), "candles", dt.datetime.fromtimestamp(v[0]["t"], dt.timezone.utc).date(), "->", ult, v[-1]["c"])
        if (dt.date.today() - ult).days > 10: print(f"WARNING: {s} last candle {ult}: Mubasher's file is stale, pick another stock")
    json.dump(D, open(p, "w"))
