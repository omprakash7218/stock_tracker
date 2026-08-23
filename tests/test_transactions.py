import pytest

def test_show_transaction(authorized_client,test_transaction_create):
    transaction_id = test_transaction_create["id"]
    res = authorized_client.get(f"/transactions/{transaction_id}")
    print(res.json())
    assert res.status_code == 200

def test_show_transactions(authorized_client,test_transaction_create):
    res = authorized_client.get("/transactions")
    print(res.json())
    assert res.status_code == 200

def test_edit_transaction(authorized_client,test_transaction_create):
    transaction_id = test_transaction_create["id"]
    res = authorized_client.put(f"/transactions/{transaction_id}",json={"fee":45,"notes":"yes Notes"})
    print(res.json())
    assert res.status_code == 200