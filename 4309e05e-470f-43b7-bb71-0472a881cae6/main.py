from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self, tickers=["AAPL", "AMD", "NVDA"], low_price_threshold=50):
        """
        Initializes the trading strategy with a list of tickers and a price threshold.
        Only considers stocks with closing prices below this threshold for trading signals.
        """
        self.tickers = tickers
        self.low_price_threshold = low_price_threshold
    
    @property
    def interval(self):
        """
        Defines the data interval to be used for indicators calculation.
        """
        return "1day"
    
    @property
    def assets(self):
        """
        Lists the assets (tickers) this strategy will analyze.
        """
        return self.tickers
    
    def run(self, data):
        """
        Executes the trading strategy using provided market data. 
        Utilizes RSI and MACD to identify buy/sell opportunities for low-cost, fast-moving stocks.
        """
        allocation_dict = {}
        
        # Loop through each ticker to analyze its data
        for ticker in self.tickers:
            d = data["ohlcv"][ticker]
            
            if len(d) == 0:
                continue  # Skip if no data is available
            
            current_price = d[-1]["close"]
            
            # Only consider stocks below the specified price threshold
            if current_price <= self.low_price_threshold:
                rsi = RSI(ticker, d, length=14)[-1]  # Calculate the latest RSI value
                macd_signal = MACD(ticker, d, fast=12, slow=26)["signal"][-1]  # Get the latest MACD signal line value
                
                # Simple buy/sell strategy based on RSI and MACD signal line
                if rsi < 30 and macd_signal > 0:
                    # Considered a buy signal
                    allocation_dict[ticker] = 0.1  # 10% allocation for simplicity
                elif rsi > 70:
                    # Considered a sell/avoid signal, allocate 0 for this ticker
                    allocation_dict[ticker] = 0
                else:
                    # Hold strategy, do not adjust allocation
                    allocation_dict[ticker] = allocation_dict.get(ticker, 0)
            else:
                # If the stock is above the threshold, do not allocate
                allocation_dict[ticker] = 0
        
        return TargetAllocation(allocation_dict)