from src.conf import Config
from src.backtest import run_backtest, multiple_coin_strategy
from src.signals_creation import compute_signal, train_test_split
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

config = Config()

if config.EXECUTE_DASHBOARD:
    with open("./dashboard.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='venv-crypto-strategy-v2')
    ep.preprocess(nb, {'metadata': {'path': './'}})
    with open(config.DASHBOARD_OUTPUT, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

# historical_data = config.historical_data
# rsi_params = {"window": 7}
# signals = {}
# signals["rsi"] = compute_signal("rsi", historical_data, **rsi_params)

# historical_data, signals = train_test_split(historical_data, config.TRAIN_TEST_SPLIT, signals)
# run_backtest(historical_data,
#              "BNB",
#              config.INITIAL_USDT,
#              config.STOP_LOSS_PCT,
#              config.TAKE_PROFIT_PCT,
#              config.TAKER_FEE,
#              config.MAKER_FEE,
#              signals)

# multiple_coin_strategy(
#     historical_data,
#     config.REQUIRED_LIST,
#     config.INITIAL_USDT,
#     config.STOP_LOSS_PCT,
#     config.TAKE_PROFIT_PCT,
#     config.TAKER_FEE,
#     config.MAKER_FEE,
#     signals
# )






