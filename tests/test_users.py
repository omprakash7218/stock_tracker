from fastapi.testclient import TestClient
from app.main import app 
from app.schemas import user
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.config import settings
from app.database import Base,get_db
from app.oauth2 import get_current_user
import pytest
from sqlalchemy.pool import StaticPool


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




def override_get_current_user():
	return {"username":"test@gmail.com", "password":"passowrd"}


app.dependency_overrides[get_current_user] = override_get_current_user






def test_root(client): 
	res = client.get("/")
	# print(res.json()["message"])      # Bad practice = if message is not there , it will crash the entire api
	assert res.json().get("message") == "Stock Tracker API is running."

def test_hello_name(client):
	res = client.get("/users/hello/omprakash%20chaudhary")
	print(res.json)
	assert res.status_code == 200

def test_create_user(client):
	res = client.post("/users/",json={"username":"omprakashcn311","email":"omprakashcn311@gmail.com","password":"password"})
	new_user = user.UserOut(**res.json())
	assert res.status_code == 200
	assert new_user.email == "omprakashcn311@gmail.com"

def test_show_all_users(client):
	client.post("/users/",json={"username":"test1","email":"test1@gmail.com","password":"password"})
	client.post("/users/",json={"username":"test3","email":"test2@gmail.com","password":"password"})
	client.post("/users",json={"username":"test","email":"test@gmail.com","password":"password"})
	res = client.get("/users")
	assert res.status_code==200
	data = res.json()
	assert len(data) == 3
	assert data[0].get("username") == "test1"
	assert data[1].get("email") == "test2@gmail.com"
