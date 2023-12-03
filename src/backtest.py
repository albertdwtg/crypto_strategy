from enum import Enum
import pandas as pd

class Operation(Enum):
    BUY = "BUY"
    SELL = "SELL"

def make_operation_rsi(current_value, previous_value):
    if current_value > 70:
        return Operation.SELL
    elif current_value < 30:
        return Operation.BUY
    else:
        return None

def run_backtest(historical_data : dict, coin_name: str, usdt: float, 
                 stop_loss_pct: float, take_profit_pct: float,
                 taker_fee: float, maker_fee: float,
                 *signal):

    previous_value = signal[0].iloc[0][coin_name]
    wallet = usdt
    stop_loss = 0
    take_profit = 100000000
    last_ath = 0
    coin = 0
    buy_ready = True
    all_operations = []
    
    for index, row in signal[0][1:].iterrows():
        current_value = row[coin_name]
        current_price = historical_data["Close"].loc[index, coin_name]

        myrow = {}
        
        if make_operation_rsi(current_value, previous_value) == Operation.BUY and buy_ready == True and usdt > 0:
            take_profit = current_price + take_profit_pct * current_price
            stop_loss = current_price - stop_loss_pct * current_price
            coin = usdt / current_price
            fee = taker_fee * coin 
            coin = coin - fee
            usdt = 0
            wallet = coin * current_price
            last_ath = update_ath(wallet, last_ath)
            
            myrow = {'date': index,'position': Operation.BUY.value, 'reason': 'Buy Market','price': current_price,
                     'fee': fee * current_price, 'fiat': usdt, 'coins': coin, 'wallet': wallet, 'drawBack':(wallet-last_ath)/last_ath}
            myrow = write_operation(index, Operation.BUY.value, "Buy Market", current_price, fee * current_price, usdt, coin, wallet, last_ath)
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

                
            myrow = {'date': index,'position': Operation.SELL.value, 'reason': 'Sell Stop Loss','price': current_price,
                     'fee': fee * current_price, 'fiat': usdt, 'coins': coin, 'wallet': wallet, 'drawBack':(wallet-last_ath)/last_ath}
            myrow = write_operation(index, Operation.SELL.value, "Sell Stop Loss", current_price, fee * current_price, usdt, coin, wallet, last_ath)
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
            
            myrow = {'date': index,'position': Operation.SELL.value, 'reason': 'Sell Take Profit','price': current_price,
                     'fee': fee * current_price, 'fiat': usdt, 'coins': coin, 'wallet': wallet, 'drawBack':(wallet-last_ath)/last_ath}
            myrow = write_operation(index, Operation.SELL.value, "Sell Take Profit", current_price, fee * current_price, usdt, coin, wallet, last_ath)
            all_operations.append(myrow)
        
        elif make_operation_rsi(current_value, previous_value) == Operation.SELL:
            buy_ready = True
            if coin > 0:
                sell_price = current_price 
                usdt = coin * sell_price
                fee = taker_fee * usdt
                usdt = usdt - fee
                coin = 0
                wallet = usdt
                last_ath = update_ath(wallet, last_ath)
                myrow = {'date': index,'position': Operation.SELL.value, 'reason': 'Sell Market', 'price': current_price, 
                         'fee': fee, 'fiat': usdt, 'coins': coin, 'wallet': wallet, 'drawBack':(wallet-last_ath)/last_ath}
                myrow = write_operation(index, Operation.SELL.value, "Sell Market", current_price, fee, usdt, coin, wallet, last_ath)
                all_operations.append(myrow)
        previous_value = current_value

    
    dt = pd.DataFrame(all_operations)
    
    print(dt)

def update_ath(wallet, last_ath):
    if wallet > last_ath:
        last_ath = wallet
    return last_ath

def compute_drawback(wallet, last_ath):
    return (wallet-last_ath)/last_ath

def write_operation(date, position, reason, price, fee, fiat, coins, wallet, last_ath):
    row = {
        'date': date,
        'position': position, 
        'reason': reason, 
        'price': price, 
        'fee': fee, 
        'fiat': fiat, 
        'coins': coins, 
        'wallet': wallet, 
        'drawBack':compute_drawback(wallet, last_ath)
    }
    return row