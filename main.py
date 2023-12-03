from src.conf import Config
from src.backtest import run_backtest
from src.signals_creation import compute_signal

config = Config()


historical_data = config.historical_data
print(historical_data)
params1 = {"window":7}
signal1 = compute_signal("rsi",historical_data,**params1)
# signal1.index = (signal1.index.date)
run_backtest(historical_data,
             "BTC", 
             config.INITIAL_USDT,
             config.STOP_LOSS_PCT,
             config.TAKE_PROFIT_PCT,
             config.TAKER_FEE,
             config.MAKER_FEE,
             signal1)



