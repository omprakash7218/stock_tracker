import pytest


def test_cash_transaction_deposit(authorized_client,test_portfolio_create,test_trade_create,):
	portfolio_id = test_portfolio_create["id"]
	res = authorized_client.post(f"/cashtransaction/{portfolio_id}/add_money",json={"amount":50000})
	assert res.json()["amount"] == 50000

def test_cash_transaction_wihtdraw(authorized_client,test_portfolio_create):
	portfolio_id = test_portfolio_create["id"]
	res = authorized_client.post(f"/cashtransaction/{portfolio_id}/withdraw",json={"amount":100})

	assert res.json()["amount"] == 100
