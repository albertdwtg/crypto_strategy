from src.conf import Config
from src.backtest import run_backtest, multiple_coin_strategy
from src.signals_creation import compute_signal, train_test_split

config = Config()


historical_data = config.historical_data
rsi_params = {"window": 7}
signals = {}
signals["rsi"] = compute_signal("rsi", historical_data, **rsi_params)

print(signals["rsi"].shape, historical_data["Close"].shape)
historical_data, signals = train_test_split(historical_data, config.TRAIN_TEST_SPLIT, signals)
print(signals["rsi"].shape, historical_data["Close"].shape)
# run_backtest(historical_data,
#              "BNB",
#              config.INITIAL_USDT,
#              config.STOP_LOSS_PCT,
#              config.TAKE_PROFIT_PCT,
#              config.TAKER_FEE,
#              config.MAKER_FEE,
#              signals)

multiple_coin_strategy(
    historical_data,
    config.REQUIRED_LIST,
    config.INITIAL_USDT,
    config.STOP_LOSS_PCT,
    config.TAKE_PROFIT_PCT,
    config.TAKER_FEE,
    config.MAKER_FEE,
    signals
)




