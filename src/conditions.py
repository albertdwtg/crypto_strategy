from enum import Enum
import numpy as np
import pandas as pd


class Operation(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Condition(Enum):
    RSI = "RSI"
    MACD = "MACD"
    STOCH_RSI = "STOCH_RSI"
    CROSS_EMA = "CROSS_EMA"
    WILLIAMS_R = "WILLIAMS_R"


def condition_rsi(signals: dict, index, coin_name: str, current_price: float):
    signal_rsi = signals["rsi"]
    signal_ema = signals["ema"]
    previous_index = get_previous_index(signal_rsi, index)
    current_rsi_value = signal_rsi.loc[index, coin_name]
    previous_rsi_value = signal_rsi.loc[previous_index, coin_name]
    current_ema_value = signal_ema.loc[index, coin_name]

    if current_rsi_value > 70:
        return Operation.SELL
    elif current_rsi_value < 30 and current_ema_value > current_price:
        return Operation.BUY
    else:
        return None


def condition_cross_ema(signals: dict, index, coin_name: str, current_price: float):
    ema_slow = signals["ema_slow"]
    ema_fast = signals["ema_fast"]
    current_ema_slow = ema_slow.loc[index, coin_name]
    current_ema_fast = ema_fast.loc[index, coin_name]

    # if current_ema_fast < current_ema_slow:
    #     return Operation.SELL
    if current_ema_fast > current_ema_slow:
        return Operation.BUY
    else:
        return None


def condition_stoch_rsi(signals: dict, index, coin_name: str, current_price: float):
    stoch_rsi_k = signals["stoch_rsi_k"]
    stoch_rsi_d = signals["stoch_rsi_d"]
    signal_ema = signals["ema"]
    current_stoch_k = stoch_rsi_k.loc[index, coin_name]
    current_stoch_d = stoch_rsi_d.loc[index, coin_name]
    current_ema_value = signal_ema.loc[index, coin_name]

    if current_stoch_k > 0.7 and current_stoch_d > current_stoch_k:
        return Operation.SELL
    elif (
        current_stoch_k < 0.3
        and current_stoch_k > current_stoch_d
        and current_price < current_ema_value
    ):
        return Operation.BUY
    else:
        return None


def condition_williams_r(signals: dict, index, coin_name: str, current_price: float):
    signal_williams_r = signals["williams_r"]
    current_williams_r = signal_williams_r.loc[index, coin_name]
    signal_ema = signals["ema"]
    current_ema_value = signal_ema.loc[index, coin_name]
    previous_index = get_previous_index(signal_williams_r, index)
    previous_williams_r = signal_williams_r.loc[previous_index, coin_name]

    if current_williams_r < -20 and previous_williams_r > -20:
        return Operation.SELL
    # if current_williams_r > -80 \
    #     and previous_williams_r < -80:
    #         return Operation.BUY
    else:
        return None


def condition_macd(signals: dict, index, coin_name: str, current_price: float):
    signal_macd = signals["macd_diff"]
    signal_ema = signals["ema"]
    signal_rsi = signals["rsi"]
    previous_index = get_previous_index(signal_macd, index)
    current_macd_value = signal_macd.loc[index, coin_name]
    previous_macd_value = signal_macd.loc[previous_index, coin_name]
    current_ema_value = signal_ema.loc[index, coin_name]
    current_rsi_value = signal_rsi.loc[index, coin_name]

    if (
        current_macd_value > previous_macd_value
        and current_macd_value < 0
        and current_ema_value > current_price
        and current_rsi_value < 30
    ):
        return Operation.BUY
    # elif current_macd_value < previous_macd_value and current_macd_value > 10:
    #     return Operation.SELL
    else:
        return None


def match_condition(signals: dict, index, coin_name: str, current_price: float):
    # print(locals())

    if condition_stoch_rsi(**locals()) is not None:
        return condition_stoch_rsi(**locals()), Condition.STOCH_RSI

    if condition_rsi(**locals()) is not None:
        return condition_rsi(**locals()), Condition.RSI

    if condition_macd(**locals()) is not None:
        return condition_macd(**locals()), Condition.MACD

    if condition_cross_ema(**locals()) is not None:
        return condition_cross_ema(**locals()), Condition.CROSS_EMA

    if condition_williams_r(**locals()) is not None:
        return condition_williams_r(**locals()), Condition.WILLIAMS_R
    else:
        return None, None


def get_previous_index(df: pd.DataFrame, cur_index, n_previous=1):
    idx = np.searchsorted(df.index, cur_index)
    return df.index[max(0, idx - n_previous)]
