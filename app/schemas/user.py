from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr,constr,ConfigDict
class UserCreate(BaseModel):
	username : str
	email : EmailStr
	password : constr(min_length=8,max_length=72)
class UserOut(BaseModel):
	username : str
	email : EmailStr
	id : int
	model_config = ConfigDict(from_attributes = True)
class UserLogin(BaseModel):
	email : EmailStr
	password : str

class TokenData(BaseModel):
	email : EmailStr

class UserPassword(BaseModel):
	current_password: str