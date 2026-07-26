
def calculate_pnl(buy_price ,sell_price , quantity):
    pnl = (sell_price-buy_price)*quantity
    return pnl


def apply_brokerage(amount:int,brokerage_percentage=0.1):
    amount -= amount*brokerage_percentage
    return amount

class InvalidTradeError(Exception):
    pass

class Portfolio():
    def __init__(self,starting_cash=0):
        self.cash= starting_cash
        self.holdings = {}
    
    def buy_stock(self,symbol,price,quantity):
        cost = price*quantity
        if cost > self.cash :
            raise InvalidTradeError("Not enough money in the wallet!")
        self.cash -= cost
        self.holdings[symbol] = self.holdings.get(symbol,0) + quantity
    def sell_stock(self,symbol,price,quantity):
        if self.holdings.get(symbol,0) < quantity:
            raise InvalidTradeError("Not enough quantity!")
        self.holdings[symbol]-=quantity
        self.cash += price *quantity
