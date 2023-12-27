import pytest
import pandas as pd
import sys

sys.path.append("./")
from src.data_collection import get_futures_symbols, collect_historic_data
from src.conf import Config

config = Config()


def test_get_symbols():
    nb_coins = 3
    list_returned = get_futures_symbols(
        status="TRADING",
        coin_pair="USDT",
        required_list=config.REQUIRED_LIST[:nb_coins],
    )
    assert isinstance(list_returned, list)
    assert len(list_returned) == nb_coins


def test_collect_historic_data():
    nb_coins = 3
    start_date = "01 january 2023"
    list_returned = get_futures_symbols(
        status="TRADING",
        coin_pair="USDT",
        required_list=config.REQUIRED_LIST[:nb_coins],
    )
    obj_returned = collect_historic_data(list_returned, start_date)
    assert len(obj_returned) == 5
    assert isinstance(obj_returned, dict)
    assert "Close" in obj_returned
    assert isinstance(obj_returned["Close"], pd.DataFrame)
    assert obj_returned["Close"].shape[0] > 100
    assert obj_returned["Close"].shape[1] == nb_coins
