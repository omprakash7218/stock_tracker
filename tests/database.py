from fastapi.testclient import TestClient
from app.main import app 
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


# def override_get_current_user():
# 	return {"username":"test@gmail.com", "password":"passowrd"}


# app.dependency_overrides[get_current_user] = override_get_current_user

