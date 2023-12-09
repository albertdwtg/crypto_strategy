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

historical_data = config.historical_data
rsi_params = {"window": 7}
signals = {}
signals["rsi"] = compute_signal("rsi", historical_data, **rsi_params)

if config.APPLY_TRAIN_TEST_SPLIT:
    historical_data, signals = train_test_split(
        historic_data = historical_data, 
        signals = signals,
        train_ratio = config.TRAIN_TEST_SPLIT
        )

run_backtest(
    historical_data = historical_data,
    coin_name = "BNB",
    usdt = config.INITIAL_USDT,
    stop_loss_pct = config.STOP_LOSS_PCT,
    take_profit_pct = config.TAKE_PROFIT_PCT,
    taker_fee = config.TAKER_FEE,
    maker_fee = config.MAKER_FEE,
    signals = signals
    )

multiple_coin_strategy(
    historical_data = historical_data,
    list_of_coin = config.REQUIRED_LIST,
    usdt = config.INITIAL_USDT,
    stop_loss_pct = config.STOP_LOSS_PCT,
    take_profit_pct = config.TAKE_PROFIT_PCT,
    taker_fee = config.TAKER_FEE,
    maker_fee = config.MAKER_FEE,
    signals = signals
    )






