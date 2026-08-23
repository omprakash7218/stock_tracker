from app.oauth2 import create_access_token
import pytest
def test_show_all_assets(client,test_asset):
    res = client.get("/assets")
    print(res.json())
    res.status_code == 200
    assert res.status_code == 200
    assert res.json()["message"][0].get("symbol") == "dummy"
# symbol : str
# 	name : str
# 	asset_type : str


def test_show_asset(test_asset,client):
    res = client.get("/assets/dummy")
    assert res.status_code == 200
    assert res.json()["name"] == "dummy-asset"
    

def test_asset_edit(authorized_client,test_asset,test_user):
    res = authorized_client.put("/assets/dummy",json={"symbol":"dummy2.0","name":"dummy-asset","asset_type":"dummy-type"})
    print(res.json())
    assert res.status_code == 200

def test_asset_delete(authorized_client,test_asset,test_user):
    res = authorized_client.delete("/assets/dummy")
    assert res.status_code == 204
    # print(res.json())

def test_asset_price(client,test_asset):
    res = client.get("/assets/AAPL/fetch_current_price/?asset_type=stock")
    print(res.json())

def test_asset_create(client):
    res = client.post("/assets",json = {"symbol":"AAPL","name":"Apple Incorporation","asset_type":"dummy-type"})
    assert res.status_code == 200
