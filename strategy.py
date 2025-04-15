import yfinance as yf
import datetime

def backtest_strategy(ticker, strategy_type, monthly_investment, start_year):
    end_date = datetime.datetime.today()
    start_date = datetime.datetime(start_year, 1, 1)
    data = yf.download(ticker, start=start_date, end=end_date, interval="1mo")

    total_invested = 0
    total_value = 0
    num_shares = 0

    for date, row in data.iterrows():
        price = row["Close"]
        if strategy_type == "momentum" and row["Close"] > row["Open"]:
            shares = monthly_investment / price
        else:
            shares = monthly_investment / price

        total_invested += monthly_investment
        num_shares += shares
        total_value = num_shares * price

    return {
        "ticker": ticker,
        "start_year": start_year,
        "strategy": strategy_type,
        "total_invested": round(total_invested, 2),
        "portfolio_value": round(total_value, 2),
        "gain": round(total_value - total_invested, 2)
    }
