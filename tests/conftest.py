from fastapi.testclient import TestClient
from app.main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.config import settings
from app.database import Base,get_db
from app.oauth2 import get_current_user
import pytest
from sqlalchemy.pool import StaticPool
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test'



engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit= False, autoflush=False,bind=engine)


# dependency
	
@pytest.fixture
def session():
	Base.metadata.drop_all(bind = engine)
	Base.metadata.create_all(bind=engine)
	db = TestingSessionLocal()
	try:
		yield db
	finally:
		db.close()
@pytest.fixture
def client(session):
	def override_get_db():
		try:
			yield session
		finally:
			session.close()
	app.dependency_overrides[get_db] = override_get_db
			
	yield TestClient(app)


# def override_get_current_user():
# 	return {"username":"test@gmail.com", "password":"passowrd"}


# app.dependency_overrides[get_current_user] = override_get_current_user



@pytest.fixture
def test_user(client):
	user_data = {
		"username":"admin",
		"email":"admin@gmail.com",
		"password":"password"
	}
	res = client.post("/users/",json=user_data)
	assert res.status_code == 200
	new_user = res.json()
	new_user['password'] = user_data['password']
	return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_email":test_user["email"]})


@pytest.fixture
def authorized_client(client,token):
	client.headers = {
		**client.headers,
		"Authorization": f"Bearer {token}"
	}
	return client

	
@pytest.fixture
def test_asset(client):
    res = client.post("/assets",json={"symbol":"dummy","name":"dummy-asset","asset_type":"dummy-type"})
    dummy_asset = res.json()
    return dummy_asset

@pytest.fixture
def test_portfolio_create(test_user,authorized_client):
	res = authorized_client.post("/portfolios",json={"name":"dummy","description":"dummy-description","cash_balance":50000})
	dummy_portfolio= res.json()
	return dummy_portfolio

@pytest.fixture
def test_trade_create(authorized_client,test_portfolio_create,test_asset):
	portfolio_id = test_portfolio_create["id"]
	res = authorized_client.post(
		f"/trades/{portfolio_id}",
		json={
		"asset_id": test_asset["id"],
		"symbol":test_asset["symbol"],
		"quantity":12,
		"price":1200,
		"trade_type":"buy"
		})
	dummy_trade = res.json()
	return dummy_trade

@pytest.fixture
def test_transaction_create(authorized_client,test_trade_create):
	trade_id = test_trade_create["id"]
	res = authorized_client.post(f"/transactions/{trade_id}",json={"fee":20,"notes":"No notes"})
	dummy_transaction = res.json()
	return dummy_transaction
