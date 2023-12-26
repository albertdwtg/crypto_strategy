from dataclasses import dataclass, field
from src.data_collection import load_data
from typing import List
from src.signals_creation import compute_signal

@dataclass
class Config:
    #-- Data Collection
    COIN_PAIR: str = 'USDT'
    COIN_STATUS: str = 'TRADING'
    DATA_FOLDER: str = 'data'
    RELOAD: bool = False
    START_DATE: str = "01 january 2019"
    REQUIRED_LIST: list[str] = field(default_factory=lambda: ["BTC", "ETH", "BNB", "XRP", "SOL", "ADA", 
                                                              "LINK", "AVAX", "DOT", "LTC"])
    THRESHOLD_NULL_COLUMNS: float = 0.5
    APPLY_TRAIN_TEST_SPLIT: bool = True
    TRAIN_TEST_SPLIT: float = 0.8
    
    #-- Backtest params
    INITIAL_USDT: float = 1000.0
    MAKER_FEE: float = 0.0005
    TAKER_FEE: float = 0.0007
    STOP_LOSS_PCT: float = 0.02
    TAKE_PROFIT_PCT: float = 0.1
    
    #-- Dashboard
    EXECUTE_DASHBOARD: bool = False
    DASHBOARD_OUTPUT: str = "executed_dashboard.ipynb"
    
    def __post_init__(self):
        self.historical_data = load_data(self.RELOAD,
                                         self.START_DATE,
                                         self.COIN_PAIR,
                                         self.COIN_STATUS,
                                         self.DATA_FOLDER,
                                         self.REQUIRED_LIST, 
                                         self.THRESHOLD_NULL_COLUMNS)
        
        signals_values = {
            "rsi" : {"signal_name": "rsi", "params": {"window": 7}},
            "ema" : {"signal_name": "ema", "params": {"window": 100}},
            "ema_slow" : {"signal_name": "ema", "params": {"window": 100}},
            "ema_fast" : {"signal_name": "ema", "params": {"window": 15}},
            "macd_diff": {"signal_name": "macd_diff", "params": {"window_slow": 60,
                                                                 "window_fast": 20,
                                                                 "window_sign": 9}},
            "stoch_rsi_k": {"signal_name": "stoch_rsi_k", "params": {"window": 50}},
            "stoch_rsi_d": {"signal_name": "stoch_rsi_d", "params": {"window": 50}},
            "williams_r" : {"signal_name" : "williams_r", "params": {"lbp": 7}}
        }
        signals_computed = {}
        for key, value in signals_values.items():
            signals_computed[key] = compute_signal(value["signal_name"],
                                                   self.historical_data,
                                                   **value["params"])
        self.SIGNALS = signals_computed
        