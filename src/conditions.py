from enum import Enum


class Operation(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Condition(Enum):
    RSI = "RSI"


def condition_rsi(current_rsi_value, previous_rsi_value):
    if current_rsi_value > 70:
        return Operation.SELL
    elif current_rsi_value < 30:
        return Operation.BUY
    else:
        return None


def match_condition(**values):
    if condition_rsi(values["current_rsi"], values["previous_rsi"]) is not None:
        return condition_rsi(values["current_rsi"], values["previous_rsi"]), Condition.RSI
    else:
        return None, None
