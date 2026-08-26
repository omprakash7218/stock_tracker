import pytest
def test_show_holdings(client,test_portfolio_create):
    portfolio_id = test_portfolio_create["id"]
    res = client.get(f"/holdings/{portfolio_id}")
    print(res.json())
    assert res.status_code == 200