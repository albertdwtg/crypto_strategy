from src.conf import Config
from src.backtest import run_backtest, multiple_coin_strategy
from src.signals_creation import compute_signal, train_test_split
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

config = Config()


def main_function():
    historical_data = config.historical_data
    signals = config.SIGNALS
    #print(signals["stoch_rsi_k"])

    if config.APPLY_TRAIN_TEST_SPLIT:
        historical_data, signals = train_test_split(
            historic_data = historical_data, 
            signals = signals,
            train_ratio = config.TRAIN_TEST_SPLIT
            )

    df_results, summary = multiple_coin_strategy(
        historical_data = historical_data,
        list_of_coin = config.REQUIRED_LIST,
        usdt = config.INITIAL_USDT,
        stop_loss_pct = config.STOP_LOSS_PCT,
        take_profit_pct = config.TAKE_PROFIT_PCT,
        taker_fee = config.TAKER_FEE,
        maker_fee = config.MAKER_FEE,
        signals = signals
        )
    return df_results, summary


if config.EXECUTE_DASHBOARD:
    with open("./dashboard.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='venv-crypto-strategy-v2')
    ep.preprocess(nb, {'metadata': {'path': './'}})
    with open(config.DASHBOARD_OUTPUT, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
else:
    df_results, summary = main_function()
    print(summary)






