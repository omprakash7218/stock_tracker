import pytest
from app.schemas import user
from jose import jwt , JWTError
from .database import session,client
from app.config import settings



def test_root(client): 
	res = client.get("/")
	# print(res.json()["message"])      # Bad practice = if message is not there , it will crash the entire api
	assert res.json().get("message") == "Stock Tracker API is running."




def test_hello_name(client):
	res = client.get("/users/hello/omprakash%20chaudhary")
	assert res.status_code == 200
	assert res.json()['message'] == 'Hello! OMPRAKASH CHAUDHARY'




def test_create_user(client):
	res = client.post("/users/",json={"username":"omprakashcn311","email":"omprakashcn311@gmail.com","password":"password"})
	new_user = user.UserOut(**res.json())
	assert res.status_code == 200
	assert new_user.email == "omprakashcn311@gmail.com"




def test_show_all_users(authorized_client,client):
	client.post("/users/",json={"username":"test1","email":"test1@gmail.com","password":"password"})
	client.post("/users/",json={"username":"test3","email":"test2@gmail.com","password":"password"})
	client.post("/users/",json={"username":"test","email":"test@gmail.com","password":"password"})
	res = authorized_client.get("/users/")
	data = res.json()
	print("--------------------------------------------------------------------------------")
	print(data)
	print("--------------------------------------------------------------------------------")
	assert len(data) == 4
	
	print(data[0])
	assert data[0]["email"] == "admin@gmail.com"
	assert res.status_code == 200




def test_login_user(test_user,client):
	res = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
	login_res = user.Token(**res.json())
	payload = jwt.decode(login_res.access_token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
	email = payload.get("user_email")
	assert email == test_user["email"]
	assert res.status_code == 200
	assert login_res.token_type == 'bearer'


@pytest.mark.parametrize("email,password,status_code",[
	("hello123@gamil.com","WrongPassword",403),
	("Wrong@gmail.com","password",403),
	("Wrong@gmail.com","WrongPassword",403),
	(None,"WrongPassword",422),
	("Wrong@gmail.com",None,422),
	(None,None,422)
])


def test_incorrect_login(test_user,client,email,password,status_code):
	res = client.post("/login",data={"username":email,"password":password})
	
	assert res.status_code == status_code
	# assert res.json().get("detail") == "Invalid Credentials"


def test_user_edit(authorized_client,test_user):
	res = authorized_client.put(f"/users/{test_user.get("username")}",
	json={
		"password": {"current_password":test_user.get("password")},
  		"edit_user": {"username": "admin2.0","email": "admin2@gmail.com","password": "password123"}
	}
	)
	print(res.json())
	assert res.status_code == 200

def test_user_delete(authorized_client,test_user):
	res = authorized_client.request("DELETE",f"/users/{test_user.get("username")}",
	json={
		"current_password":test_user.get("password")})
	assert res.status_code == 204

