from src.conf import Config
from src.backtest import run_backtest, multiple_coin_strategy
from src.signals_creation import compute_signal

config = Config()


historical_data = config.historical_data
rsi_params = {"window":7}
rsi_signal = compute_signal("rsi", historical_data, **rsi_params)
run_backtest(historical_data,
             "BNB", 
             config.INITIAL_USDT,
             config.STOP_LOSS_PCT,
             config.TAKE_PROFIT_PCT,
             config.TAKER_FEE,
             config.MAKER_FEE,
             rsi_signal)

# multiple_coin_strategy(
#     historical_data,
#     config.REQUIRED_LIST, 
#     config.INITIAL_USDT,
#     config.STOP_LOSS_PCT,
#     config.TAKE_PROFIT_PCT,
#     config.TAKER_FEE,
#     config.MAKER_FEE,
#     rsi_signal
# )



