"""Datos de TradingView para un capítulo de la serie semanal de análisis fundamental en árabe de Nabd Wall Street (nabd/fundamental/).
Corre en GitHub Actions (datos-fundamental-Nabd.yml), porque el contenedor de Claude no llega a TradingView.
Pide al escáner de TradingView las cifras fundamentales de la empresa (ingresos, beneficio, márgenes, PER, deuda, flujo de caja,
dividendos, ROE… y, cuando existen, sus series históricas «_h»), más velas semanales de 5 años. Cada campo se prueba por separado:
los que TradingView no conoce se anotan en "sin_campo" y no rompen nada.
Las cifras se congelan: si <salida>/datos.json ya existe, no se vuelve a pedir (salvo REFRESCAR=1), para que la locución no cambie.
uso: python3 datos_fundamental.py <video.json> <carpeta de salida>   (video.json → "simbolo", p. ej. "NASDAQ:AAPL"; "simbolos_extra" opcional)"""
import json, os, sys, time, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diario"))
from datos_mercado import get, TVH, tv_velas

BASES = ["total_revenue", "net_income", "gross_profit", "oper_income", "ebitda", "ebit", "pre_tax_income", "cost_of_goods",
         "gross_margin", "operating_margin", "net_margin", "pre_tax_margin", "ebitda_margin",
         "earnings_per_share_basic", "earnings_per_share_diluted", "earnings_per_share", "revenue_per_share",
         "total_assets", "total_liabilities", "total_equity", "total_debt", "net_debt", "long_term_debt", "short_term_debt",
         "cash_n_short_term_invest", "cash_n_equivalents", "debt_to_equity", "debt_to_assets", "current_ratio", "quick_ratio",
         "free_cash_flow", "cash_f_operating_activities", "cash_f_investing_activities", "cash_f_financing_activities", "capital_expenditures",
         "return_on_equity", "return_on_assets", "return_on_invested_capital", "dividends_paid", "dps_common_stock_prim_issue",
         "dividend_payout_ratio", "book_value_per_share", "total_shares_outstanding", "price_earnings", "price_book", "price_sales",
         "enterprise_value_ebitda", "price_free_cash_flow"]
SUF = ["_fy", "_fq", "_ttm", "_fy_h", "_fq_h", "_current"]
SUELTOS = ["name", "description", "close", "currency", "fundamental_currency_code", "market_cap_basic", "price_earnings_ttm", "price_book_fq",
           "price_sales_current", "enterprise_value_current", "enterprise_value_ebitda_ttm", "dividends_yield", "dividends_yield_current",
           "dividend_yield_recent", "earnings_release_date", "earnings_release_next_date", "fiscal_period_end", "fy_end", "sector", "industry",
           "number_of_employees", "float_shares_outstanding", "total_shares_outstanding", "Perf.Y", "Perf.5Y", "Perf.YTD", "price_52_week_high",
           "price_52_week_low", "beta_1_year", "fiscal_period_fq_h", "fiscal_period_fy_h", "fiscal_period_end_fq_h", "fiscal_period_end_fy_h"]


def scan(sym, cols):
    r = get("https://scanner.tradingview.com/global/scan", json.dumps({"symbols": {"tickers": [sym]}, "columns": cols}).encode(), TVH)
    d = r.get("data") or []
    return dict(zip(cols, d[0]["d"])) if d else {}


def fundamentales(sym):
    out, sin = {}, []
    for c in SUELTOS + [b + s for b in BASES for s in SUF]:
        try:
            v = scan(sym, [c])
            if v.get(c) is not None: out[c] = v[c]
        except Exception:
            sin.append(c)
        time.sleep(0.15)
    return out, sin


def main():
    VJ = json.load(open(sys.argv[1])); outd = sys.argv[2]; os.makedirs(outd, exist_ok=True); p = os.path.join(outd, "datos.json")
    if os.path.exists(p) and not os.environ.get("REFRESCAR"):
        print("datos ya congelados:", p); return
    D = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "fuente": "TradingView", "empresas": {}}
    for s in [VJ["simbolo"]] + VJ.get("simbolos_extra", []):
        f, sin = fundamentales(s); e = {"campos": f, "sin_campo": sin}
        try:
            e["velas_semanales"] = tv_velas(s, "1W", 270)["velas"]
        except Exception as ex:
            e["error_velas"] = str(ex)
        D["empresas"][s] = e
        print(s, len(f), "campos;", len(sin), "rechazados;", len(e.get("velas_semanales", [])), "velas semanales")
    json.dump(D, open(p, "w"), ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main()
