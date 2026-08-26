import pytest 


def test_show_portfolios(authorized_client,test_portfolio_create):
    res = authorized_client.get("/portfolios")
    
    portfolios = res.json()
    print(portfolios)
    assert res.status_code == 200

def test_show_portfolio(authorized_client,test_portfolio_create):
    res = authorized_client.get("/portfolios/1")
    portfolio = res.json()
    print(portfolio)
    assert res.status_code == 200

def test_edit_portfolio(authorized_client,test_portfolio_create):
    res = authorized_client.put("portfolios/1",json={"name":"dummy2.0","description":"Long term but more accurate"})
    portfolio = res.json()
    print(portfolio)
    assert res.status_code == 200
def test_delete_portfolio(authorized_client,test_portfolio_create,test_user):
    id = test_portfolio_create["id"]
    res = authorized_client.request('DELETE',f"/portfolios/{id}",json={"current_password":test_user["password"]})
    assert res.status_code == 204
def test_get_summary_portfolio(authorized_client,test_portfolio_create):
    id = test_portfolio_create["id"]
    res = authorized_client.get(f"/portfolios/{id}")
    print(res.json())
    assert res.status_code == 200