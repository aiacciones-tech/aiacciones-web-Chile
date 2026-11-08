# Video diario en árabe de la bolsa de EAU (FTSE ADX General y DFM General): 1080p, voz Piper ar_JO-kareem, logo AI Stocks UAE.
# Uso: AUD=<scratch> python3 make_video.py <carpeta del día> [preview]
#   La carpeta del día tiene mercado.json (de datos/mercado-<fecha>.json de la rama datos-diario-eau) y video.json (textos y locución;
#   ver ejemplo-2026-11-06/). Escribe <carpeta>/video-bolsa-<fecha>-UAE.mp4 y <carpeta>/times.json (capítulos).
import os, sys, json, numpy as np, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
from tecnico import calc, INDICE, MESES, TZ, fecha_ar
DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
W, H, FPS = 1920, 1080, 30
AUD = os.environ.get("AUD", "aud")
M = json.load(open(f"{DIR}/mercado.json")); VJ = json.load(open(f"{DIR}/video.json"))
R, A = calc(M, VJ.get("nombres")); FECHA = dt.date.fromisoformat(R["fecha"]); FECHA_TXT = fecha_ar(FECHA)
OUT = f"{DIR}/video-bolsa-{R['fecha']}-UAE.mp4"
CTA = cta_activa(R["fecha"])
if CTA: VJ["voz"]["s_fin"] = VJ["voz"]["s_fin"].rstrip() + " " + CTA_VOZ
SECS = ["الأخبار", "التحليل الأساسي", "الأسهم", "التحليل الفني", "الأجندة"]; NS = len(SECS)
LG = load_logo(130); LGS = load_logo(95); LGB = load_logo(230)
NB = 126  # unas 6 meses de sesiones


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)


def base_fig(n, kicker, title, sub):
    f = fig(W, H)
    T(f, 0.94, 0.90, kicker, GOLD, 24, "bold")
    T(f, 0.94, 0.80, title, FG, 44 if len(title) <= 50 else 38, "bold")
    T(f, 0.105, 0.92, f"{n}/{NS} · {SECS[n - 1]}", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.885, "أسهم الإمارات · " + FECHA_TXT, DIM, 16, "bold", ha="left")
    w = 0.88 / NS
    for i in range(NS):  # barra de progreso de derecha a izquierda
        f.patches.append(plt.Rectangle((0.94 - (i + 1) * w + 0.008, 0.975), w - 0.008, 0.008, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))
    T(f, 0.94, 0.04, "\n".join(textwrap.wrap(sub, 150)), MUTED, 16, linespacing=1.4)
    return f


def s_title(t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, 0.94, 0.89, "أسهم الإمارات · ملخص جلسة التداول", GOLD, 28, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.14, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, 0.94, 0.77, "جلسة " + FECHA_TXT, BG, 66, "bold", va="center", alpha=a)
    for k, x0 in (("adx", 0.53), ("dfm", 0.06)):
        r = R[k]; up = r["var_pct"] >= 0; cc = TEAL if up else NEG; xr = x0 + 0.41
        T(f, xr, 0.615, INDICE[k], MUTED, 28, "bold", alpha=a)
        f.text(xr, 0.52, num(r["cierre"]), color=FG, fontsize=64, weight="bold", ha="right", alpha=a)
        f.text(xr, 0.46, f"{pct(r['var_pct'])}   ({r['var_pts']:+,.2f})", color=cc, fontsize=34, weight="bold", ha="right", alpha=a)
        I = [v for v in M[f"{k}_intradia"]["velas"] if dt.datetime.fromtimestamp(v["t"], TZ).date() == FECHA]
        IC = np.array([v["c"] for v in I]); prev = r["anterior"]
        if len(IC) > 2:
            ax = f.add_axes([x0, 0.17, 0.41, 0.24]); clean(ax)
            n = max(2, int(len(IC) * ease(t))); x = np.arange(len(IC))
            ax.plot(x[:n], IC[:n], color=cc, lw=3); ax.axhline(prev, color=DIM, lw=1.5, ls="--")
            ax.fill_between(x[:n], IC[:n], prev, color=cc, alpha=0.12)
            pad = (max(IC.max(), prev) - min(IC.min(), prev)) * 0.15
            ax.set_xlim(0, len(IC) - 1); ax.set_ylim(min(IC.min(), prev) - pad, max(IC.max(), prev) + pad); ax.set_xticks([]); ax.set_yticks([])
            T(f, xr, 0.415, "حركة المؤشر خلال الجلسة (كل 5 دقائق)", MUTED, 17)
            T(f, x0, 0.415, "الإغلاق السابق " + num(prev), MUTED, 15, ha="left")
    if VJ.get("titular"): T(f, 0.94, 0.095, VJ["titular"], BLUE, 30, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, 0.94, 0.04, VJ.get("title_fuente", "البيانات: TradingView (إغلاق " + R["fecha"] + ")"), MUTED, 16)
    return with_logo(to_arr(f), LG, x=60, y=40)


def s_news(t):
    N_ = VJ["noticias"]; f = base_fig(1, "أخبار اليوم", N_["titulo"], N_["fuente"]); pal = [GOLD, TEAL, BLUE, NEG, FG]
    for i, (tag, txt) in enumerate(N_["items"]):
        b = ease((t - i * 0.15) / 0.4)
        if b <= 0: continue
        y = 0.66 - i * 0.14; cc = pal[i % 5]
        f.patches.append(plt.Rectangle((0.945, y - 0.035), 0.006, 0.09, transform=f.transFigure, color=cc, alpha=b, figure=f))
        T(f, 0.93, y + 0.02, tag, cc, 28, "bold", alpha=b)
        T(f, 0.93, y - 0.03, txt, FG, 25 if len(txt) <= 95 else 22, alpha=b)
    return to_arr(f)


def s_fact(t):
    F = VJ["factores"]; f = base_fig(2, "التحليل الأساسي: لماذا تحركت السوق؟", F["titulo"], F["fuente"])
    TV = M.get("tv", {})
    L = [(n, (TV[v]["change"] if isinstance(v, str) else v)) for n, v in F["bolsas"] if not isinstance(v, str) or (v in TV and TV[v].get("change") is not None)]
    ax = f.add_axes([0.20, 0.13, 0.25, 0.58]); clean(ax); e = ease(t)
    y = np.arange(len(L))[::-1]; v = [x[1] for x in L]; lim = max(abs(min(v)), abs(max(v))) * 1.5
    ax.barh(y, [x * e for x in v], color=[(GOLD if "الإمارات" in n or "أبوظبي" in n or "دبي" in n else (TEAL if x > 0 else NEG)) for n, x in L], height=0.6)
    ax.set_yticks(y, [ar(n) for n, _ in L]); ax.tick_params(colors=FG, labelsize=19); ax.set_xticks([])
    ax.set_xlim(-lim if min(v) < 0 else -lim * 0.35, lim * 0.7 if max(v) > 0 else lim * 0.35); ax.axvline(0, color=DIM, lw=1.5)
    if t >= 0.6:
        for yy, x in zip(y, v): ax.text(x * e + (lim * 0.03 if x > 0 else -lim * 0.03), yy, pct(x), va="center", ha="left" if x > 0 else "right", color=FG, fontsize=18, weight="bold")
    T(f, 0.45, 0.735, F.get("bolsas_titulo", "الأسواق في الجلسة"), MUTED, 20)
    for i, (a_, b_, cc) in enumerate(F["items"]):
        b = ease((t - 0.2 - i * 0.12) / 0.4)
        if b <= 0: continue
        yy = 0.67 - i * 0.135
        T(f, 0.94, yy, a_, col(cc), 29 if len(a_) <= 36 else 25, "bold", alpha=b)
        T(f, 0.94, yy - 0.048, b_, MUTED, 22 if len(b_) <= 50 else 19, alpha=b)
    return to_arr(f)


def s_movers(t):
    V_ = VJ["valores"]; MOT = V_.get("motivos", {}); sub = R["adx"]["suben"] + R["dfm"]["suben"]; baj = R["adx"]["bajan"] + R["dfm"]["bajan"]
    f = base_fig(3, "الأسهم الأكثر ارتفاعًا وانخفاضًا", f"انخفض {baj} سهمًا وارتفع {sub} في السوقين", V_["fuente"])
    mx = max(abs(x["cambio"]) for x in R["mejores"] + R["peores"])
    for xr, lst, cc, title in [(0.94, R["mejores"], TEAL, "الأكثر ارتفاعًا"), (0.48, R["peores"], NEG, "الأكثر انخفاضًا")]:
        T(f, xr, 0.715, title, cc, 26, "bold")
        for i, m in enumerate(lst):
            b = ease((t - i * 0.08) / 0.4)
            if b <= 0: continue
            y = 0.635 - i * 0.098; bw = 0.10 * abs(m["cambio"]) / mx * b; x0 = xr - 0.265
            T(f, xr, y, m["nombre"], FG, 24, "bold", alpha=b)
            f.patches.append(plt.Rectangle((x0 - bw, y - 0.002), bw, 0.032, transform=f.transFigure, color=cc, figure=f))
            f.text(x0 - bw - 0.006, y, pct(m["cambio"]), color=FG, fontsize=21, weight="bold", ha="right", alpha=b)
            T(f, xr, y - 0.036, m["ticker"] + " · " + m["mercado"] + " · " + MOT.get(m["ticker"], "لا يوجد خبر محدد في الصحافة"), MUTED, 16, alpha=b)
    if V_.get("extra"): T(f, 0.94, 0.135, V_["extra"], BLUE, 24, "bold", alpha=ease((t - 0.5) / 0.4))
    return to_arr(f)


def tech(k, n_sec, t):
    TJ = VJ["tecnico"][k]; r = R[k]; a_ = A[k]
    f = base_fig(4, "التحليل الفني · " + INDICE[k], TJ["titulo"],
                 "شموع يومية لآخر 6 أشهر من TradingView. المتوسطات والدعوم والمقاومات (قمم وقيعان حديثة) و RSI والعشوائي: محسوبة. حجم التداول مقابل متوسط 10 جلسات: محسوب. هذه بيانات وليست إشارات شراء أو بيع.")
    dates, o, hi, lo, c, S50, S200 = (a_[x] for x in ("dates", "o", "hi", "lo", "c", "S50", "S200"))
    n = len(c); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.36, 0.56, 0.38]); clean(ax)
    span = hi[idx].max() - lo[idx].min()
    for j in range(m):
        i = idx[j]; cc = TEAL if c[i] >= o[i] else NEG
        ax.vlines(j, lo[i], hi[i], color=cc, lw=1.2); ax.add_patch(plt.Rectangle((j - 0.35, min(o[i], c[i])), 0.7, max(abs(c[i] - o[i]), span * 0.002), color=cc))
    ax.plot(x[:m], S50[idx][:m], color=BLUE, lw=2.5, label=ar("متوسط 50 جلسة"))
    ax.plot(x[:m], S200[idx][:m], color=GOLD, lw=2.5, label=ar("متوسط 200 جلسة"))
    al = ease((t - 0.6) / 0.4); LEV = [l for l in r["niveles"] if lo[idx].min() - span * 0.25 <= l["valor"] <= hi[idx].max() + span * 0.25]
    for l in LEV:
        cc = NEG if l["tipo"] == "res" else TEAL
        ax.axhline(l["valor"], color=cc, lw=1.1, ls="--", alpha=al)
    vals = [l["valor"] for l in LEV]
    ax.set_xlim(-1, NB); ax.set_ylim(min(lo[idx].min(), np.nanmin(S200[idx]), *vals) - span * 0.05, max(hi[idx].max(), np.nanmax(S200[idx]), *vals) + span * 0.05)
    tk = [j for j in range(NB) if j == 0 or dates[idx[j]].month != dates[idx[j - 1]].month]
    ax.set_xticks(tk, [ar(MESES[dates[idx[j]].month - 1]) for j in tk]); ax.tick_params(labelsize=16)
    ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
    ax.legend(frameon=False, labelcolor=FG, fontsize=17, loc=TJ.get("leyenda", "upper left"), ncol=2)
    ax2 = f.add_axes([0.05, 0.13, 0.56, 0.17]); clean(ax2)
    ax2.axhspan(70, 100, color=NEG, alpha=0.07); ax2.axhspan(0, 30, color=TEAL, alpha=0.07)
    for lv in (20, 30, 70, 80): ax2.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax2.plot(x[:m], a_["RSI"][idx][:m], color=BLUE, lw=2.2, label="RSI 14")
    ax2.plot(x[:m], a_["K"][idx][:m], color=TEAL, lw=1.6, label="%K"); ax2.plot(x[:m], a_["D"][idx][:m], color=NEG, lw=1.6, label="%D")
    ax2.set_xlim(-1, NB); ax2.set_ylim(0, 100); ax2.set_xticks([]); ax2.yaxis.tick_right(); ax2.set_yticks([20, 50, 80])
    ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left", ncol=3)
    vr = r["volumen_vs_media10_pct"]
    filas = [("الإغلاق", num(r["cierre"]), FG),
             ("متوسط 50 جلسة", f"{num(r['sma50'])}  ({pct(r['dist_sma50_pct'], 1)})", BLUE),
             ("متوسط 200 جلسة", f"{num(r['sma200'])}  ({pct(r['dist_sma200_pct'], 1)})", GOLD)]
    filas += [(("مقاومة" if l["tipo"] == "res" else "دعم") + " · " + l["et"], num(l["valor"]), NEG if l["tipo"] == "res" else TEAL) for l in TJ["niveles"]]
    filas += [("RSI 14", num(r["rsi14"], 1) + "  · " + TJ["rsi_txt"], BLUE),
              ("العشوائي (14، 3، 3)", f"%K {num(r['estoc_k'], 0)} · %D {num(r['estoc_d'], 0)}", TEAL),
              ("حجم التداول", ("—" if vr is None else f"{pct(vr, 0)}") + " عن متوسط 10 جلسات", MUTED)]
    for i, (lab, val, cc) in enumerate(filas):
        b = ease((t - 0.3 - i * 0.05) / 0.4)
        if b <= 0: continue
        y = 0.715 - i * 0.063
        T(f, 0.94, y, lab, MUTED, 19, alpha=b)
        T(f, 0.67, y, val, cc, 21, "bold", ha="left", alpha=b)
    return to_arr(f)


def s_tech_adx(t): return tech("adx", 4, t)
def s_tech_dfm(t): return tech("dfm", 4, t)


def s_agenda(t):
    G = VJ["agenda"]; f = base_fig(5, "الأجندة", G["titulo"], G["fuente"])
    for i, (d_, e_, s_) in enumerate(G["filas"]):
        b = ease((t - i * 0.12) / 0.4); y = 0.64 - i * 0.095
        T(f, 0.94, y, d_, GOLD, 27, "bold", alpha=b)
        T(f, 0.76, y, e_, FG, 26 if len(e_) <= 55 else 22, alpha=b)
        T(f, 0.06, y, s_, MUTED, 19, ha="left", alpha=b)
    return to_arr(f)


def s_fin(t):
    Fn = VJ["fin"]; f = fig(W, H); a = ease(t / 0.5)
    T(f, 0.94, 0.80, "أسهم الإمارات · " + FECHA_TXT, FG, 50, "bold", alpha=a)
    T(f, 0.94, 0.715, "\n".join(textwrap.wrap(Fn["titular"], 52)), GOLD, 32, "bold", alpha=a, linespacing=1.05, va="top")
    T(f, 0.94, 0.535, "ملخص يومي بعد إغلاق كل جلسة في سوقي أبوظبي ودبي", BLUE, 27, alpha=a)
    if CTA: T(f, 0.94, 0.405, CTA_TXT, FG, 28, "bold", alpha=ease((t - 0.3) / 0.5))
    f.text(0.94, 0.475, CANAL.replace("https://www.", ""), color=BLUE, fontsize=27, ha="right", weight="bold", alpha=a)
    aviso = ("إخلاء مسؤولية: هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية أو دعوة لشراء أو بيع أي ورقة مالية أو استشارة مالية شخصية، "
             "ولا يراعي وضعك أو أهدافك أو مدى تحملك للمخاطر. استشر جهة مرخصة من هيئة الأوراق المالية والسلع قبل أي قرار استثماري. "
             "الأرقام من مصادر عامة مذكورة (" + Fn["fuentes"] + ")، والحسابات الخاصة موضحة بعبارة «محسوب». "
             "التحليل الفني يصف حركة الأسعار في الماضي وليس إشارات شراء أو بيع ولا يتنبأ بالمستقبل. "
             "لا نملك مراكز في الأسهم المذكورة ولا نتلقى أي مقابل من الشركات. الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال، والأداء السابق لا يضمن النتائج المستقبلية. "
             "النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي ومراجعة مع المصادر.")
    T(f, 0.94, 0.07, "\n".join(textwrap.wrap(aviso, 125)), MUTED, 17, linespacing=1.3, alpha=a)
    return with_logo(to_arr(f), LGB, x=110, y=90)


SEQ = [s_title, s_news, s_fact, s_movers, s_tech_adx, s_tech_dfm, s_agenda, s_fin]; BIG = {s_title, s_fin}
def frame(fn, t):
    arr = fn(t); return arr if fn in BIG else with_logo(arr, LGS, x=60, y=48)


if __name__ == "__main__":
    os.makedirs(AUD, exist_ok=True)
    if PREVIEW:
        for fn in SEQ: Image.fromarray(frame(fn, 1.0)).save(os.path.join(AUD, "prev_" + fn.__name__ + ".png"))
        sys.exit()
    clips = [voz(VJ["voz"][fn.__name__], os.path.join(AUD, fn.__name__ + ".wav")) for fn in SEQ]; sr = clips[0][1]
    LEAD, TAIL = 0.12, 0.45
    durs = [LEAD + len(a) / sr + TAIL for a, _ in clips]; durs[0] += 0.4; durs[-1] += 1.5
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if sum(durs) > 180: sys.exit(f"Video demasiado largo: {sum(durs):.1f} s (máx. 180). Acorta la locución.")
    leads = [LEAD + (0.4 if j == 0 else 0) for j in range(len(SEQ))]
    times, t0 = render([lambda t, fn=fn: frame(fn, t) for fn in SEQ], durs, ([a for a, _ in clips], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "video-silent.mp4"), os.path.join(AUD, "full.wav"))
    json.dump([(fn.__name__, tt) for fn, tt in zip(SEQ, times)], open(os.path.join(DIR, "times.json"), "w")); print("listo", round(t0, 1), "s", OUT)
