import pytest
from tests.trade_utils import calculate_pnl,apply_brokerage,Portfolio,InvalidTradeError
@pytest.mark.parametrize("amount,brokerage_percentage,actual_amount",[(500,0.01,495),(200,0.02,196),(1000,0.02,980),])
def test_apply_brokerage(amount,brokerage_percentage,actual_amount):
    assert apply_brokerage(amount,brokerage_percentage)==actual_amount

def test_calculate_pnl():
    assert calculate_pnl(12,13,12)==12


@pytest.fixture
def min_balance_portfolio():
    return Portfolio(10000)
def test_portfolio_balance(min_balance_portfolio):
    assert min_balance_portfolio.cash==10000
    
def test_buy_stock():
    portfolio = Portfolio(12000)
    portfolio.buy_stock("RELIANCE.NS",1000,10)
    assert portfolio.cash == 2000
    assert portfolio.holdings["RELIANCE.NS"]==10
def test_buy_stock_insufficient_funds(min_balance_portfolio):
    with pytest.raises(InvalidTradeError):
        min_balance_portfolio.buy_stock("RELIANCE.NS",1000,12)
    
def test_sell_stock():
    portfolio = Portfolio(12000)
    portfolio.buy_stock("RELIANCE.NS",1000,11)
    portfolio.sell_stock("RELIANCE.NS",1289,10)
    assert portfolio.holdings["RELIANCE.NS"]==1
    
def test_sell_not_enough_quantity(min_balance_portfolio):
    with pytest.raises(InvalidTradeError):
        min_balance_portfolio.sell_stock("RELIANCE.NS",1999,49)