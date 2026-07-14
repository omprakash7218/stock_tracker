# app/services/price_service.py

import requests
import yfinance as yf
from datetime import datetime, timedelta

class PriceService:
    
    # Cache variables
    _exchange_rate = None
    _exchange_rate_timestamp = None
    _CACHE_DURATION = 3600  # Refresh every 1 hour (3600 seconds)
    
    @staticmethod
    def get_price(symbol: str, asset_type: str):
        """Get live price for any asset in INR"""
        if asset_type.lower() == "crypto":
            return PriceService._get_crypto_price(symbol)
        elif asset_type.lower() == "stock":
            return PriceService._get_stock_price(symbol)
        else:
            raise ValueError("asset_type must be 'crypto' or 'stock'")

    @staticmethod
    def _get_crypto_price(symbol: str):
        """Get crypto price from CoinGecko (already in INR)"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            parameters = {"ids": symbol.lower(), "vs_currencies": "inr"}
            response = requests.get(url, parameters)
            price = response.json()[symbol.lower()]["inr"]
            return price
        except Exception as e:
            print(f"Error fetching crypto price: {e}")
            return None

    @staticmethod
    def _get_exchange_rate():
        """Get USD to INR exchange rate (cached)"""
        now = datetime.now()
        
        # Check if cache is still valid
        if PriceService._exchange_rate is not None and PriceService._exchange_rate_timestamp is not None:
            time_diff = (now - PriceService._exchange_rate_timestamp).total_seconds()
            
            # If less than 1 hour old, use cached rate
            if time_diff < PriceService._CACHE_DURATION:
                return PriceService._exchange_rate
        
        # Cache expired or doesn't exist, fetch new rate
        try:
            usd_inr = yf.Ticker("INR=X")
            rate = usd_inr.history(period="1d")["Close"].iloc[-1]
            
            # Store in cache
            PriceService._exchange_rate = rate
            PriceService._exchange_rate_timestamp = now
            
            return rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return 83  # Fallback rate (approx ₹83 per $1)

    @staticmethod
    def _get_stock_price(symbol: str):
        """Get stock price from yfinance and convert to INR if needed"""
        try:
            symbol_upper = symbol.upper()
            stock = yf.Ticker(symbol_upper)
            price = stock.info.get("regularMarketPrice")
            
            if price is None:
                return None
            
            # Check if it's an NSE stock (ends with .NS) or US stock
            if symbol_upper.endswith(".NS"):
                # Already in INR
                return price
            else:
                # US stock, need to convert to INR
                exchange_rate = PriceService._get_exchange_rate()
                price_in_inr = price * exchange_rate
                return price_in_inr
        
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None