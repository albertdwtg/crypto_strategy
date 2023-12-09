from dataclasses import dataclass, field
from src.data_collection import load_data
from typing import List

@dataclass
class Config:
    COIN_PAIR: str = 'USDT'
    COIN_STATUS: str = 'TRADING'
    DATA_FOLDER: str = 'data'
    RELOAD: bool = False
    START_DATE: str = "01 january 2019"
    REQUIRED_LIST: list[str] = field(default_factory=lambda: ["BTC", "ETH", "BNB", "XRP", "SOL", "ADA", 
                                                              "LINK", "AVAX", "DOT", "LTC"])
    THRESHOLD_NULL_COLUMNS: float = 0.5
    TRAIN_TEST_SPLIT: float = 0.8
    
    #-- Backtest params
    INITIAL_USDT: float = 1000.0
    MAKER_FEE: float = 0.0005
    TAKER_FEE: float = 0.0007
    STOP_LOSS_PCT: float = 0.02
    TAKE_PROFIT_PCT: float = 0.1
    
    def __post_init__(self):
        self.historical_data = load_data(self.RELOAD,
                                         self.START_DATE,
                                         self.COIN_PAIR,
                                         self.COIN_STATUS,
                                         self.DATA_FOLDER,
                                         self.REQUIRED_LIST, 
                                         self.THRESHOLD_NULL_COLUMNS)
        