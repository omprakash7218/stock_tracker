import requests
import yfinance as yf



class PriceService:

	@staticmethod
	def get_price(symbol:str,asset_type:str):
		if asset_type.lower() == "crypto":
			return PriceService._get_crypto_price(symbol)
		elif asset_type.lower() == "stock":
			return PriceService._get_stock_price(symbol)
		else:
			raise ValueError("Asset Type must be Crypto or Sock")

	@staticmethod
	def _get_crypto_price(symbol:str):
		try:
			url = "https://api.coingecko.com/api/v3/simple/price"
			parameters = {
				"ids":symbol.lower(),"vs_currencies":"inr"
			}
			response = requests.get(url,parameters)
			price = response.json()[symbol.lower()]["inr"]

			return price 
		except Exception as e:
			print(f"Error fetching crypto price: {e}")
			return None
	@staticmethod
	def _stock_price(symbol):
		stock = yf.Ticker(symbol)
		stock_price = stock.history(period="1d")["Close"].iloc[-1]
		return stock_price
	@staticmethod
	def _get_stock_price(symbol:str):
		try:
			symbol = symbol.upper()
			if symbol.endswith(".NS"):
				price = PriceService._stock_price(symbol)
				return price
			else:
				usd_inr = yf.Ticker("INR=X")
				ex_rate = usd_inr.history(period="1d")["Close"].iloc[-1]
				price = PriceService._stock_price(symbol) * ex_rate
				return price
		except Exception as e:
			print(f"Error fetching stock price: {e}")
			return None