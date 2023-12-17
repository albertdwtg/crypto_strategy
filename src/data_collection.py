import requests
import pandas as pd
from binance import Client
from binance.enums import HistoricalKlinesType
import datetime
from typing import List
import os

from src import logging_config
import logging

logger = logging.getLogger(__name__)


def get_futures_symbols(status: str, coin_pair: str, required_list: List[str]) -> List[str]:
    """Function that returns a list of coins names

    Args:
        status (str): status of the coin on api binance. ex: TRADING
        coin_pair (str): pair of the coin we want to collect. ex: USDT
        required_list (List[str]): list of coin to retrieve

    Returns:
        List[str]: list of coins names
    """
    base = 'https://fapi.binance.com'
    endpoint = f'{base}/fapi/v1/exchangeInfo'

    params = {}
    result = requests.get(endpoint, params=params).json()

    usdt = []
    logger.info(f"Loading crypto symbols for status {status} and pair {coin_pair}")

    for symb in result['symbols']:
        if symb['status'] == status:
            if symb['symbol'].endswith(coin_pair) and symb["baseAsset"] in required_list:
                usdt.append(symb['symbol'])

    # -- we put BTC in the first place
    btc_pair = "BTC" + coin_pair
    usdt.remove(btc_pair)
    usdt.insert(0, btc_pair)
    return usdt


def collect_historic_data(coins: List[str], start_date: str) -> dict:
    """Function that collects historical data of a list of coins

    Args:
        coins (List[str]): List of coins names. ex: BTCUSDT
        start_date(str): date where to start the historic
        
    Returns:
        dict: dict of dataframes containing data
    """
    logger.info(f"Staring loading since {start_date}")
    historic = {}
    historic["High"] = pd.DataFrame()
    historic["Volume"] = pd.DataFrame()
    historic["Low"] = pd.DataFrame()
    historic["Open"] = pd.DataFrame()
    historic["Close"] = pd.DataFrame()
    for i in coins:
        try:
            klinesT = Client().get_historical_klines(i, Client.KLINE_INTERVAL_1DAY, start_date,
                                                     klines_type=HistoricalKlinesType.FUTURES)
            df = pd.DataFrame(klinesT, columns=[
                'timestamp', 'Open', 'High', 'Low', 'Close',
                'Volume', 'close_time', 'quote_av', 'trades',
                'tb_base_av', 'tb_quote_av', 'ignore'])
            df.index = df['timestamp'].apply(
                lambda x: datetime.datetime.fromtimestamp(x / 1000))
            df = df[["Open", "Low", "Close", "High", "Volume"]]
            cols = df.columns
            name = i[:-4]
            df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
            historic["Open"][name] = df["Open"]
            historic["Close"][name] = df["Close"]
            historic["Volume"][name] = df["Volume"]
            historic["High"][name] = df["High"]
            historic["Low"][name] = df["Low"]
        except:
            continue
    return historic


def save_df_to_parquet(df: pd.DataFrame, path: str, filename: str) -> str:
    """
    Function that saves a dataframe to a parquet file

    Args:
        df (pd.DataFrame): dataframe to save in parquet file
        path (string): location of the parquet file
    Returns:
        str: name of the file
    """
    if not os.path.exists(path):
        os.makedirs(path)
    name = filename + ".parquet"
    target_path = os.path.join(path, name)
    df.to_parquet(target_path)
    logger.info(f"Save data to parquet file in {target_path}")
    return name


def collect_coins_data(start_date: str, coin_pair: str, coin_status: str, data_folder_name: str,
                       required_list: List[str]) -> dict:
    """Function that collects historical data of coins and save it to parquet

    Args:
        start_date (str): date where to start the historic
        coin_pair (str): pair of the coin we want to collect. ex: USDT
        coin_status (str): status of the coin on api binance. ex: TRADING
        data_folder_name (str): name of the folder where we will save data
        required_list (List[str]): list of coin to retrieve
    Returns:
        dict: dict of dataframes containing data
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder_path = os.path.join(root_dir, data_folder_name)
    coins_names = get_futures_symbols(coin_status, coin_pair, required_list)

    historic = collect_historic_data(coins_names, start_date)
    for key, value in historic.items():
        value.index = value.index.date
        save_df_to_parquet(value, data_folder_path, key)
    return historic


def remove_columns_with_null_values(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Removes columns from a DataFrame that contain more than the threshold percentage of null values.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.
        threshold (float, optional): The threshold percentage of null values. Default is 0.5 (50%).

    Returns:
        pd.DataFrame: The modified DataFrame with removed columns.
    """
    # Calculate the number of rows in the DataFrame
    num_rows = len(df)

    # Calculate the maximum allowed null values per column
    threshold_null_values = num_rows * threshold

    # Remove columns with more than threshold_null_values null values
    columns_to_remove = []
    for column in df.columns:
        num_null_values = df[column].isnull().sum()
        if num_null_values > threshold_null_values:
            columns_to_remove.append(column)

    df = df.drop(columns_to_remove, axis=1)
    return df


def load_data(reload: bool, start_date: str, coin_pair: str, coin_status: str,
              data_folder_name: str, required_list: List[str], threshold: float = 0.5) -> dict:
    """Function that reload files or just import existing files

    Args:
        reload (bool): tells if we reload or just import
        start_date (str): date where to start the historic
        coin_pair (str): pair of the coin we want to collect. ex: USDT
        coin_status (str): status of the coin on api binance. ex: TRADING
        data_folder_name (str): name of the folder wher we will save data
        required_list (List[str]): list of coin to retrieve
        threshold (float, optional): The threshold percentage of null values. Default is 0.5 (50%).
    Returns:
        dict: dict of dataframes containing data
    """
    historic_data = {}
    if reload:
        logger.info("Reloading is starting")
        historic_data = collect_coins_data(start_date, coin_pair, coin_status, data_folder_name, required_list)
        logger.info("Realoading is done")
    else:
        logger.info("Realoading data is not required")
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_folder_path = os.path.join(root_dir, data_folder_name)
        files_dir = [f for f in os.listdir(data_folder_path) if f.endswith(".parquet")]
        for file in files_dir:
            complete_file_path = os.path.join(data_folder_path, file)
            file_name = file.split('.')[0]
            df = pd.read_parquet(complete_file_path)
            historic_data[file_name] = df
    for key in historic_data:
        historic_data[key] = remove_columns_with_null_values(historic_data[key], threshold)
    return historic_data
