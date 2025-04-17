import alpaca_trade_api as tradeapi
import random
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Alpaca credentials
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
symbol = 'SPY'

def get_current_price(symbol):
    trade = api.get_latest_trade(symbol)
    return float(trade.price)

def buy_spy():
    account = api.get_account()
    cash = float(account.cash)
    price = get_current_price(symbol)

    # Calculate how many shares can be bought with available cash, but limit to a max of 10 shares
    max_shares_to_buy = min(10, int(cash // price))
    
    if max_shares_to_buy > 0:
        print(f"Buying {max_shares_to_buy} shares of {symbol}")
        api.submit_order(
            symbol=symbol,
            qty=max_shares_to_buy,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    else:
        print("Not enough cash to buy even one share of SPY.")

def sell_spy():
    positions = api.list_positions()
    spy_position = next((pos for pos in positions if pos.symbol == symbol), None)
    
    if spy_position:
        qty_to_sell = min(10, abs(int(float(spy_position.qty))))  # Limit to max 10 shares to sell
        if qty_to_sell > 0:
            print(f"Selling {qty_to_sell} shares of {symbol}")
            api.submit_order(
                symbol=symbol,
                qty=qty_to_sell,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
        else:
            print(f"No {symbol} shares to sell.")
    else:
        print(f"No {symbol} positions to sell.")

def flip_coin_and_trade():
    coin = random.randint(0, 1)
    action = 'BUY SPY' if coin == 1 else 'SELL SPY'
    print(f"\nFlipped coin: {coin} — {action}")

    if coin == 1:
        buy_spy()
    else:
        sell_spy()

# Main loop
try:
    while True:
        flip_coin_and_trade()
        time.sleep(1)  # Adjusted to run every 1 second
except KeyboardInterrupt:
    print("Trading bot stopped.")
