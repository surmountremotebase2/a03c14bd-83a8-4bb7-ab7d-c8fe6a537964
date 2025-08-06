from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, ATR
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):

    def __init__(self):
        # Assuming 'assets' represents a predetermined list of low price high volatility stocks
        self.assets_list = ["PENNY1", "PENNY2", "PENNY3"] 

    @property
    def assets(self):
        return self.assets_list

    @property
    def interval(self):
        return "1day"  # 1-day interval to capture daily movements

    @property
    def data(self):
        # No additional data sources needed for this strategy
        return []

    def run(self, data):
        allocation_dict = {}
        
        # Minimum ATR and MACD threshold as volatility and momentum indicators, respectively
        min_atr_threshold = 0.05
        macd_signal_buy_threshold = 0
        
        for asset in self.assets:
            ohlcv = data["ohlcv"][asset]
            df = pd.DataFrame(ohlcv)
            if len(df) < 30:  # Ensure enough data for indicators
                log(f"Not enough data for {asset}")
                continue
            
            # Calculate ATR and MACD for each asset
            atr = ATR(asset, ohlcv, length=14)
            macd_info = MACD(asset, ohlcv, fast=12, slow=26)
            macd, signal, histogram = macd_info["MACD"], macd_info["signal"], macd_info["histogram"]
            
            # Check for recent volatility and positive momentum
            if atr[-1] > min_atr_threshold and histogram[-1] > macd_signal_buy_threshold:
                # Simple allocation strategy: equally distribute among selected stocks
                allocation_dict[asset] = 1 / len(self.assets)
            else:
                allocation_dict[asset] = 0  # No allocation if criteria not met
            
        # Log allocation for review
        log(f"Allocations: {allocation_dict}")
        
        return TargetAllocation(allocation_dict)