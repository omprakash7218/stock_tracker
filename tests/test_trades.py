import pytest


def test_get_trades(authorized_client,test_portfolio_create,test_trade_create):
    portfolio_id = test_portfolio_create["id"]
    res = authorized_client.get(f"trades/{portfolio_id}")
    print(res.json())
    assert res.status_code == 200


def test_get_trade(authorized_client,test_portfolio_create,test_trade_create):
    trade_id = test_trade_create["id"]
    res = authorized_client.get(f"/trades/{trade_id}")
    print(res.json())
    assert res.status_code == 200

def test_delete_trade(authorized_client,test_portfolio_create,test_trade_create):
    trade_id = test_trade_create["id"]
    res = authorized_client.delete(f"/trades/{trade_id}")
    assert res.status_code == 204

def test_edit_trade(authorized_client,test_portfolio_create,test_trade_create,test_asset):
    trade_id = test_trade_create["id"]
    res = authorized_client.put(
        f"/trades/{trade_id}",
        json={"asset_id":test_trade_create["asset"]["id"],
        "symbol":test_trade_create["asset"]["symbol"],
        "quantity":1100,
        "price":1212,
        "trade_type":"buy"},)
    print(res.json())
    assert res.status_code == 200




# class TradeCreate(BaseModel):
# 	asset_id : int
# 	symbol : str
# 	quantity : float
# 	price : float
# 	trade_type : str
