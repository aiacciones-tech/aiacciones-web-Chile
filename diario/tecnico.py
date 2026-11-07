"""Indicadores del MSCI IPSA a partir de datos/mercado-<fecha>.json (lo usan make_video.py y el guion).
uso: python3 tecnico.py <mercado.json>  -> imprime JSON con cierre, medias, RSI, estocástico, niveles y acciones."""
import json, sys, datetime as dt, numpy as np

NOMBRES = {"AGUAS-A": "Aguas Andinas", "CHILE": "Banco de Chile", "BCI": "Bci", "ITAUCL": "Itaú Chile", "BSANTANDER": "Santander Chile",
           "CAP": "CAP", "CENCOSUD": "Cencosud", "CENCOMALLS": "Cencosud Shopping", "CCU": "CCU", "VAPORES": "CSAV (Vapores)",
           "COLBUN": "Colbún", "CONCHATORO": "Concha y Toro", "ANDINA-B": "Andina-B", "CMPC": "CMPC", "COPEC": "Copec",
           "ENELAM": "Enel Américas", "ENELCHILE": "Enel Chile", "ECL": "Engie Energía", "ENTEL": "Entel", "FALABELLA": "Falabella",
           "IAM": "IAM", "ILC": "ILC", "LTM": "LATAM Airlines", "PAMPA": "Pampa Investments", "PARAUCO": "Parque Arauco",
           "MALLPLAZA": "Mallplaza", "QUINENCO": "Quiñenco", "RIPLEY": "Ripley", "SALFACORP": "Salfacorp", "SMU": "SMU", "SQM-B": "SQM-B"}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
NO_CLP = {"PAMPA"}   # cotiza en dólares: fuera del cálculo de monto en pesos


def calc(D):
    V = D["ipsa_diario"]["velas"]
    dates = [dt.datetime.fromtimestamp(v["t"], dt.timezone.utc).date() for v in V]
    o, hi, lo, c = (np.array([v[k] for v in V], float) for k in "ohlc")
    sma = lambda n: np.array([c[max(0, i - n + 1):i + 1].mean() if i >= n - 1 else np.nan for i in range(len(c))])
    S50, S200 = sma(50), sma(200)
    dd = np.diff(c); g = np.where(dd > 0, dd, 0); ls = np.where(dd < 0, -dd, 0); RSI = [np.nan] * 15
    ag, al = g[:14].mean(), ls[:14].mean()
    for i in range(14, len(dd)):
        ag = (ag * 13 + g[i]) / 14; al = (al * 13 + ls[i]) / 14; RSI.append(100 - 100 / (1 + ag / al))
    RSI = np.array(RSI[:len(c)])
    fk = np.array([np.nan] * 13 + [(c[i] - lo[i - 13:i + 1].min()) / (hi[i - 13:i + 1].max() - lo[i - 13:i + 1].min()) * 100 for i in range(13, len(c))])
    roll = lambda a, n: np.array([np.mean(a[i - n + 1:i + 1]) if i >= n - 1 and not np.isnan(a[i - n + 1:i + 1]).any() else np.nan for i in range(len(a))])
    K = roll(fk, 3); Dl = roll(K, 3)
    y1 = [i for i, d in enumerate(dates) if d > dates[-1] - dt.timedelta(days=365)]
    i_hi = y1[0] + int(np.argmax(hi[y1])); i_lo = y1[0] + int(np.argmin(lo[y1]))
    lv = []
    for n in (5, 30):
        j = len(c) - n + int(np.argmax(hi[-n:])); lv.append(("res", float(hi[j]), dates[j]))
        j = len(c) - n + int(np.argmin(lo[-n:])); lv.append(("sop", float(lo[j]), dates[j]))
    lv.append(("res", float(hi[i_hi]), dates[i_hi]))
    seen, niveles = set(), []
    for t, v, d in lv:
        if round(v) in seen or (t == "res" and v <= c[-1]) or (t == "sop" and v >= c[-1]): continue
        seen.add(round(v)); niveles.append({"tipo": t, "valor": round(v, 1), "fecha": d.isoformat()})
    tv = D.get("tv", {}); tk = D.get("ipsa_tickers", {})
    acc = {t: tv[s] for t, s in tk.items() if s and tv.get(s, {}).get("change") is not None}
    vals = sorted([(v["change"], t) for t, v in acc.items()])
    # Volumen: monto transado hoy por las acciones del IPSA (precio x acciones) frente a su media de 10 sesiones (TradingView). Calculado.
    hoy = sum(v["close"] * v["volume"] for t, v in acc.items() if t not in NO_CLP and v.get("volume") and v.get("close"))
    med = sum(v["close"] * v["average_volume_10d_calc"] for t, v in acc.items() if t not in NO_CLP and v.get("average_volume_10d_calc") and v.get("close"))
    sem = [i for i, d in enumerate(dates) if d <= dates[-1] - dt.timedelta(days=dates[-1].weekday() + 1)]
    return dict(fecha=dates[-1].isoformat(), cierre=round(float(c[-1]), 2), anterior=round(float(c[-2]), 2),
                var_pct=round(float(c[-1] / c[-2] * 100 - 100), 2), var_pts=round(float(c[-1] - c[-2]), 2),
                semana_pct=round(float(c[-1] / c[sem[-1]] * 100 - 100), 2) if sem else None,
                cierre_semana_anterior=round(float(c[sem[-1]]), 2) if sem else None,
                max_dia=round(float(hi[-1]), 1), min_dia=round(float(lo[-1]), 1),
                sma50=round(float(S50[-1]), 1), sma200=round(float(S200[-1]), 1),
                dist_sma50_pct=round(float(c[-1] / S50[-1] * 100 - 100), 2), dist_sma200_pct=round(float(c[-1] / S200[-1] * 100 - 100), 2),
                rsi14=round(float(RSI[-1]), 1), estoc_k=round(float(K[-1]), 1), estoc_d=round(float(Dl[-1]), 1),
                estoc_k_prev=round(float(K[-2]), 1), estoc_d_prev=round(float(Dl[-2]), 1),
                max_52s=round(float(hi[i_hi]), 1), max_52s_fecha=dates[i_hi].isoformat(), min_52s=round(float(lo[i_lo]), 1), min_52s_fecha=dates[i_lo].isoformat(),
                monto_mm=round(hoy / 1e9, 1) if hoy else None, volumen_vs_media10_pct=round(hoy / med * 100 - 100, 1) if hoy and med else None,
                niveles=niveles, suben=sum(1 for x, _ in vals if x > 0), bajan=sum(1 for x, _ in vals if x < 0), sin_cambio=sum(1 for x, _ in vals if x == 0),
                mejores=[(NOMBRES.get(k, k), k, round(x, 2)) for x, k in vals[::-1][:5]], peores=[(NOMBRES.get(k, k), k, round(x, 2)) for x, k in vals[:5]],
                todos={k: round(x, 2) for x, k in vals},
                contexto={k: {"close": v.get("close"), "change": None if v.get("change") is None else round(v["change"], 2)} for k, v in tv.items() if k not in tk.values()}), \
        dict(dates=dates, o=o, hi=hi, lo=lo, c=c, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
