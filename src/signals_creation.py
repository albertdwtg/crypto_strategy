import ta
import pandas as pd
from typing import Tuple


def get_returns_data(historic_data: dict) -> pd.DataFrame:
    """Function that creates a returns matrix from historic data

    Args:
        historic_data (dict): dict of dataframes

    Returns:
        pd.DataFrame: returns dataframes
    """
    returns = historic_data["Close"].pct_change()
    return returns


def train_test_split(
    historic_data: dict, train_ratio: float, signals: dict
) -> Tuple[dict, dict]:
    """Function that applies a train test split on all dataframes of two dicts of dataframes

    Args:
        historic_data (dict): dict of dataframes
        train_ratio (float): ratio of the training sample (between 0 and 1)
        signals (dict): dict of signals dataframes

    Returns:
        Tuple[dict,dict]: two dict of dataframes, one for historic data and an another for signals
    """
    train_data = {}
    signals_train = {}
    nb_rows = int(train_ratio * len(historic_data["Close"]))
    index_limit = historic_data["Close"].index[nb_rows]
    for key in historic_data:
        train_data[key] = historic_data[key].loc[:index_limit]
    for key in signals:
        signals_train[key] = signals[key].loc[:index_limit]
    return train_data, signals_train


# -- Momentum Indicators
def get_rsi(df_records: dict, **params):
    """
    Function that creates the rsi dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.rsi(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_stoch_rsi(df_records: dict, **params):
    """
    Function that creates the stochastic rsi dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.stochrsi(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_stoch_rsi_d(df_records: dict, **params):
    """
    Function that creates the stochastic rsi d dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.stochrsi_d(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_stoch_rsi_k(df_records: dict, **params):
    """
    Function that creates the stochastic rsi k dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.stochrsi_k(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_tsi(df_records: dict, **params):
    """
    Function that creates the tsi dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.tsi(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_aws_oscillator(df_records: dict, **params):
    """
    Function that creates the awesome oscillator dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.awesome_oscillator(
            high=df_records["High"][coin_name],
            low=df_records["Low"][coin_name],
            **params
        )

    return signal_df


def get_kama(df_records: dict, **params):
    """
    Function that creates the kama dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.kama(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_stoch(df_records: dict, **params):
    """
    Function that creates the stoch oscillator dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.stoch(
            close=df_records["Close"][coin_name],
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            **params
        )

    return signal_df


def get_stoch_signal(df_records: dict, **params):
    """
    Function that creates the stoch oscillator signal dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.stoch_signal(
            close=df_records["Close"][coin_name],
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            **params
        )

    return signal_df


def get_williams_r(df_records: dict, **params):
    """
    Function that creates the williams r dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.williams_r(
            close=df_records["Close"][coin_name],
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            **params
        )

    return signal_df


def get_ppo(df_records: dict, **params):
    """
    Function that creates the ppo dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.ppo(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_ppo_signal(df_records: dict, **params):
    """
    Function that creates the ppo signal dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.ppo_signal(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_pvo(df_records: dict, **params):
    """
    Function that creates the pvo dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.pvo(
            volume=df_records["Volume"][coin_name], **params
        )

    return signal_df


def get_pvo_signal(df_records: dict, **params):
    """
    Function that creates the pvo signal dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.pvo_signal(
            volume=df_records["Volume"][coin_name], **params
        )

    return signal_df


def get_pvo_hist(df_records: dict, **params):
    """
    Function that creates the pvo hist dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.pvo_hist(
            volume=df_records["Volume"][coin_name], **params
        )

    return signal_df


def get_roc(df_records: dict, **params):
    """
    Function that creates the roc dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.momentum.roc(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


# -- Trend Indicators


def get_macd_diff(df_records: dict, **params):
    """
    Function that creates the macd diff dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        MACD = ta.trend.MACD(close=df_records["Close"][coin_name], **params)
        signal_df[coin_name] = MACD.macd_diff()

    return signal_df


def get_macd_signal(df_records: dict, **params):
    """
    Function that creates the macd signal dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        MACD = ta.trend.MACD(close=df_records["Close"][coin_name], **params)
        signal_df[coin_name] = MACD.macd_signal()

    return signal_df


def get_ema(df_records: dict, **params):
    """
    Function that creates the EMA dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.ema_indicator(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_aroon_up(df_records: dict, **params):
    """
    Function that creates the aroon up dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.aroon_up(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_aroon_down(df_records: dict, **params):
    """
    Function that creates the aroon down dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.aroon_down(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_cci(df_records: dict, **params):
    """
    Function that creates the cci dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.cci(
            close=df_records["Close"][coin_name],
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            **params
        )

    return signal_df


def get_dpo(df_records: dict, **params):
    """
    Function that creates the dpo dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.dpo(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_trix(df_records: dict, **params):
    """
    Function that creates the trix dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.trix(
            close=df_records["Close"][coin_name], **params
        )

    return signal_df


def get_mass_index(df_records: dict, **params):
    """
    Function that creates the mass_index dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.trend.mass_index(
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            **params
        )

    return signal_df


# -- Volatility Indicators


def get_bol_wband(df_records: dict, **params):
    """
    Function that creates the bol wband dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        BOL_BAND = ta.volatility.BollingerBands(
            close=df_records["Close"][coin_name], **params
        )
        signal_df[coin_name] = BOL_BAND.bollinger_wband()

    return signal_df


# -- Volume Indicators


def get_chaikin_money_flow(df_records: dict, **params):
    """
    Function that creates the chaikin_money_flow dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.volume.chaikin_money_flow(
            close=df_records["Close"][coin_name],
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            volume=df_records["Volume"][coin_name],
            **params
        )

    return signal_df


def get_ease_of_movement(df_records: dict, **params):
    """
    Function that creates the ease of movement dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.volume.ease_of_movement(
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            volume=df_records["Volume"][coin_name],
            **params
        )

    return signal_df


def get_force_index(df_records: dict, **params):
    """
    Function that creates the force index dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.volume.force_index(
            close=df_records["Close"][coin_name],
            volume=df_records["Volume"][coin_name],
            **params
        )

    return signal_df


def get_money_flow_index(df_records: dict, **params):
    """
    Function that creates the money_flow_index dataframe
    :param df_records: all dataframes containing historical_data

    :param params: dict of parameters to create the signal
    :return: dataframe containing the signal
    """
    signal_df = pd.DataFrame()
    for coin_name in df_records["Open"].columns:
        signal_df[coin_name] = ta.volume.money_flow_index(
            close=df_records["Close"][coin_name],
            low=df_records["Low"][coin_name],
            high=df_records["High"][coin_name],
            volume=df_records["Volume"][coin_name],
            **params
        )

    return signal_df


def compute_signal(signal_name: str, historic_data: dict, **params) -> pd.DataFrame:
    """
    Function that create a signal, based on its name
    :param signal_name: name of the signal we want to create
    :param historic_data: all dataframes containing historical data
    :param params: dict of parameters to create the signal
    :return: dataframe of the signal
    """

    signal = pd.DataFrame()
    if signal_name.lower() == "rsi":
        signal = get_rsi(historic_data, **params)
    if signal_name.lower() == "stoch_rsi":
        signal = get_stoch_rsi(historic_data, **params)
    if signal_name.lower() == "stoch_rsi_d":
        signal = get_stoch_rsi_d(historic_data, **params)
    if signal_name.lower() == "stoch_rsi_k":
        signal = get_stoch_rsi_k(historic_data, **params)
    if signal_name.lower() == "tsi":
        signal = get_tsi(historic_data, **params)
    if signal_name.lower() == "awesome_oscillator":
        signal = get_aws_oscillator(historic_data, **params)
    if signal_name.lower() == "kama":
        signal = get_kama(historic_data, **params)
    if signal_name.lower() == "stoch_oscillator":
        signal = get_stoch(historic_data, **params)
    if signal_name.lower() == "stoch_oscillator_signal":
        signal = get_stoch_signal(historic_data, **params)
    if signal_name.lower() == "williams_r":
        signal = get_williams_r(historic_data, **params)
    if signal_name.lower() == "ppo":
        signal = get_ppo(historic_data, **params)
    if signal_name.lower() == "ppo_signal":
        signal = get_ppo_signal(historic_data, **params)
    if signal_name.lower() == "pvo":
        signal = get_pvo(historic_data, **params)
    if signal_name.lower() == "pvo_signal":
        signal = get_pvo_signal(historic_data, **params)
    if signal_name.lower() == "pvo_hist":
        signal = get_pvo_hist(historic_data, **params)
    if signal_name.lower() == "roc":
        signal = get_roc(historic_data, **params)
    if signal_name.lower() == "macd_diff":
        signal = get_macd_diff(historic_data, **params)
    if signal_name.lower() == "macd_signal":
        signal = get_macd_signal(historic_data, **params)
    if signal_name.lower() == "ema":
        signal = get_ema(historic_data, **params)
    if signal_name.lower() == "aroon_up":
        signal = get_aroon_up(historic_data, **params)
    if signal_name.lower() == "aroon_down":
        signal = get_aroon_down(historic_data, **params)
    if signal_name.lower() == "cci":
        signal = get_cci(historic_data, **params)
    if signal_name.lower() == "dpo":
        signal = get_dpo(historic_data, **params)
    if signal_name.lower() == "trix":
        signal = get_trix(historic_data, **params)
    if signal_name.lower() == "mass_index":
        signal = get_mass_index(historic_data, **params)
    if signal_name.lower() == "bol_wband":
        signal = get_bol_wband(historic_data, **params)
    if signal_name.lower() == "chaikin_money_flow":
        signal = get_chaikin_money_flow(historic_data, **params)
    if signal_name.lower() == "ease_of_movement":
        signal = get_ease_of_movement(historic_data, **params)
    if signal_name.lower() == "force_index":
        signal = get_force_index(historic_data, **params)
    if signal_name.lower() == "money_flow_index":
        signal = get_money_flow_index(historic_data, **params)
    return signal.shift(1)
