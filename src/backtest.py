from enum import Enum
import pandas as pd
from typing import List
from src.conditions import *


class Reason(Enum):
    BUY_MARKET = "BUY_MARKET"
    SELL_STOP_LOSS = "SELL_STOP_LOSS"
    SELL_TAKE_PROFIT = "SELL_TAKE_PROFIT"
    SELL_MARKET = "SELL_MARKET"


def init_signals_values(signals: dict, coin_name: str):
    signals_values = {}
    for key, value in signals.items():
        signals_values["current_" + key.lower()] = value.iloc[0][coin_name]
        signals_values["previous_" + key.lower()] = value.iloc[0][coin_name]
    return signals_values


def run_backtest(historical_data: dict, coin_name: str, usdt: float,
                 stop_loss_pct: float, take_profit_pct: float,
                 taker_fee: float, maker_fee: float,
                 signals: dict):
    rsi_signal = signals["rsi"]
    close_data = historical_data["Close"]
    close_data = close_data[close_data[coin_name].notnull()]
    wallet = usdt
    stop_loss = 0
    take_profit = 100000000
    last_ath = 0
    coin = 0
    buy_ready = True
    all_operations = []
    signals_value = init_signals_values(signals, coin_name)

    for index, row in close_data.iterrows():
        signals_value["current_rsi"] = rsi_signal.loc[index, coin_name]
        current_price = row[coin_name]
        myrow = {}

        operation, condition = match_condition(**signals_value)
        if operation == Operation.BUY and buy_ready == True and usdt > 0:
            take_profit = current_price + take_profit_pct * current_price
            stop_loss = current_price - stop_loss_pct * current_price
            coin = usdt / current_price
            fee = taker_fee * coin
            coin = coin - fee
            usdt = 0
            wallet = coin * current_price
            last_ath = update_ath(wallet, last_ath)
            myrow = write_operation(index, coin_name, Operation.BUY.value, Reason.BUY_MARKET.value, current_price,
                                    fee * current_price, usdt, coin, wallet, last_ath, condition.value)
            all_operations.append(myrow)

        elif current_price <= stop_loss and coin > 0:
            sell_price = current_price
            usdt = coin * sell_price
            fee = maker_fee * usdt
            usdt = usdt - fee
            coin = 0
            buy_ready = False
            wallet = usdt
            last_ath = update_ath(wallet, last_ath)
            myrow = write_operation(index, coin_name, Operation.SELL.value, Reason.SELL_STOP_LOSS.value, current_price,
                                    fee, usdt, coin, wallet, last_ath)
            all_operations.append(myrow)

        elif current_price > take_profit and coin > 0:
            sell_price = current_price
            usdt = coin * sell_price
            fee = maker_fee * usdt
            usdt = usdt - fee
            coin = 0
            buy_ready = False
            wallet = usdt
            last_ath = update_ath(wallet, last_ath)
            myrow = write_operation(index, coin_name, Operation.SELL.value, Reason.SELL_TAKE_PROFIT.value,
                                    current_price, fee, usdt, coin, wallet, last_ath)
            all_operations.append(myrow)

        elif operation == Operation.SELL:
            buy_ready = True
            if coin > 0:
                sell_price = current_price
                usdt = coin * sell_price
                fee = taker_fee * usdt
                usdt = usdt - fee
                coin = 0
                wallet = usdt
                last_ath = update_ath(wallet, last_ath)
                myrow = write_operation(index, coin_name, Operation.SELL.value, Reason.SELL_MARKET.value, current_price,
                                        fee, usdt, coin, wallet, last_ath, condition.value)
                all_operations.append(myrow)
        signals_value["previous_rsi"] = signals_value["current_rsi"]

    dt = pd.DataFrame(all_operations)
    return backtest_evaluation(dt, close_data[coin_name])


def update_ath(wallet: float, last_ath: float) -> float:
    """
    Function that updates the last ath value
    Args:
        wallet (float): current wallet value
        last_ath (float): previous ath

    Returns:
        float: value of the current ath
    """
    if wallet > last_ath:
        last_ath = wallet
    return last_ath


def compute_drawback(wallet: float, last_ath: float) -> float:
    """
    Function that computes the drawback between ath and current wallet value
    Args:
        wallet (float): current wallet value
        last_ath (float): previous ath

    Returns:
        float: drawback computed
    """
    return (wallet - last_ath) / last_ath


def write_operation(date, coin_name, position, reason, price, fee, fiat, coins, wallet, last_ath, condition = None):
    row = {
        'date': date,
        'coin_name': coin_name,
        'position': position,
        'reason': reason,
        'condition': condition,
        'price': price,
        'fee': fee,
        'fiat': fiat,
        'coins': coins,
        'wallet': wallet,
        'drawBack': compute_drawback(wallet, last_ath)
    }
    return row


def backtest_evaluation(results: pd.DataFrame, close_dataframe: pd.Series):
    dt = results.copy()
    dt = dt.set_index(dt['date'])
    dt.index = pd.to_datetime(dt.index)
    dt['resultat'] = dt['wallet'].diff()
    dt['resultat%'] = dt['wallet'].pct_change() * 100
    dt.loc[dt['position'] == 'Buy', 'resultat'] = None
    dt.loc[dt['position'] == 'Buy', 'resultat%'] = None

    dt['tradeIs'] = ''
    dt.loc[dt['resultat'] > 0, 'tradeIs'] = 'Good'
    dt.loc[dt['resultat'] <= 0, 'tradeIs'] = 'Bad'
    initial_wallet = round(dt.wallet.iloc[0], 2)
    final_wallet = round(dt.wallet.iloc[-1], 2)
    ini_close = close_dataframe.iloc[0]
    last_close = close_dataframe.iloc[-1]
    hold_pct = ((last_close - ini_close) / ini_close) * 100
    algo_pct = ((final_wallet - initial_wallet) / initial_wallet) * 100
    algo_vs_hold_pct = ((algo_pct - hold_pct) / hold_pct) * 100

    data = {
        "starting_balance": initial_wallet,
        "final_balance": final_wallet,
        "performance_algo": round(algo_pct, 2),
        "performance_buy_hold": round(hold_pct, 2),
        "algo_vs_hold": round(algo_vs_hold_pct, 2),
        "nb_negative_trades": dt.groupby('tradeIs')['date'].nunique()['Bad'],
        "nb_positive_trades": dt.groupby('tradeIs')['date'].nunique()['Good'],
        "avg_pct_negative_trades": round(
            dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].sum() / dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].count(), 2),
        "avg_pct_positive_trades": round(
            dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].sum() / dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].count(),
            2),
        "total_fee": round(dt['fee'].sum(), 2),
        "worst_drawback": 100 * round(dt['drawBack'].min(), 2),
        "detail": results
    }
    data["win_rate"] = data["nb_positive_trades"]/(data["nb_negative_trades"] + data["nb_positive_trades"])*100
    data["total_trades"] = data["nb_negative_trades"] + data["nb_positive_trades"]
    return data


def multiple_coin_strategy(historical_data: dict, list_of_coin: List[str], usdt: float,
                           stop_loss_pct: float, take_profit_pct: float,
                           taker_fee: float, maker_fee: float,
                           signals: dict):
    all_evaluations = {}
    share_usdt = usdt / len(list_of_coin)
    for coin in list_of_coin:
        evaluation = run_backtest(
            historical_data,
            coin,
            share_usdt,
            stop_loss_pct,
            take_profit_pct,
            taker_fee,
            maker_fee,
            signals
        )
        all_evaluations[coin] = evaluation

    df_evaluations = pd.DataFrame.from_dict(all_evaluations, orient='index')
    print("final wallet : ", df_evaluations["final_balance"].sum())
    return df_evaluations
