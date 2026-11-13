"""Diagnóstico temporal: qué columnas fundamentales da el escáner de TradingView (AAPL y JPM)."""
import json, urllib.request
C = """total_revenue_fq total_revenue_ttm total_revenue_fy net_income_fq net_income_ttm earnings_per_share_diluted_fq earnings_per_share_fq
earnings_per_share_forecast_fq earnings_per_share_forecast_next_fq revenue_forecast_fq revenue_forecast_next_fq eps_surprise_fq eps_surprise_percent_fq
revenue_surprise_fq revenue_surprise_percent_fq gross_margin_fq gross_margin operating_margin_fq operating_margin net_margin_fq net_margin
free_cash_flow_ttm free_cash_flow_fq cash_n_short_term_invest_fq total_debt_fq total_assets_fq total_liabilities_fq total_equity_fq
debt_to_equity_fq dividends_yield total_revenue_yoy_growth_fq net_income_yoy_growth_fq earnings_per_share_diluted_yoy_growth_fq
capital_expenditures_ttm capital_expenditures_fq cash_f_operating_activities_ttm cash_f_operating_activities_fq gross_profit_fq oper_income_fq
total_revenue_fq_h net_income_fq_h earnings_per_share_diluted_fq_h total_revenue_fy_h free_cash_flow_fq_h fiscal_period_end_fq fiscal_period_current
earnings_release_date earnings_release_next_date dps_common_stock_prim_issue_fy""".split()
for col in C:
    body = json.dumps({"symbols": {"tickers": ["NASDAQ:AAPL", "NYSE:JPM"]}, "columns": [col]}).encode()
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request("https://scanner.tradingview.com/america/scan", body, {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}), timeout=30).read())
        print("OK ", col, [str(x["d"][0])[:160] for x in r["data"]])
    except Exception as e:
        print("NO ", col, e)
