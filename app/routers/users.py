from fastapi import APIRouter, HTTPException,Depends,Response,status
from app.schemas.user import UserCreate,UserOut,UserPassword
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import hash_pwd
from app.models.user import User
from app.oauth2 import get_current_user
from app.schemas.user import UserCreate,UserOut
from typing import List
router = APIRouter(tags= ["USERS"],prefix = "/users")

@router.get("/hello/{name}")
def hello_name(name):
	print("Hello ",name)
	return {"message":f"Hello! {name.upper()}"}

@router.get("/",response_model=List[UserOut])
def show_users(db:Session=Depends(get_db),current_user:UserOut=Depends(get_current_user)):
	users = db.query(User).all()
	return users

@router.post("/",response_model = UserOut)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
	pwd = hash_pwd(user.password)
	user.password = pwd
	existing_user = db.query(User).filter(User.email == user.email).first()
	if existing_user:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Forbidden")
	new_user = User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user
@router.delete("/{username}")
def delete_user(username:str,password:UserPassword,current_user:UserOut=Depends(get_current_user),db:Session=Depends(get_db)):
	user_query = db.query(User).filter(User.username==username,current_user.username == username,User.password == password.current_password)
	user = user_query.first()
	if not user:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Not found")
	db.delete(user)
	db.commit()
	return Response(status_code = status.HTTP_204_NO_CONTENT)
@router.put("/{username}",response_model = UserOut)
def update_user(username : str , password:UserPassword, edit_user:UserCreate ,current_user:UserOut=Depends(get_current_user) , db : Session = Depends(get_db)):
	user_query = db.query(User).filter(User.username == username,current_user.username == username,User.password==password.current_password)
	user = user_query.first()
	if not user:
		raise HTTPException(status_code = 404, detail = "Not Found")
	if db.query(User).filter(User.email == user.email,User.username == user.username).first() == True:
		raise HTTPException(status_code = 406 , detail = "A user with same credentials already exist. Try different credentials.")
	
	user_query.update(edit_user.dict(),synchronize_session=False)
	db.commit()
	db.refresh(user)
	return user
