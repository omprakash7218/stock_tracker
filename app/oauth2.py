from jose import jwt , JWTError
from datetime import datetime , timedelta
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.schemas.user import TokenData,UserOut
from app.models.user import User
from app.database import get_db
from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
# end point for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRATION_TIME   = settings.EXPIRATION_TIME

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp":expire})
    access_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return access_token
def verify_access_token(token:str,credentials_exception):
	payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
	email = payload.get("user_email")
	if not email:
		raise credentials_exception
	token_data = TokenData(email=email)

	return token_data



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
	credentials_exception = HTTPException(status_code = 401 , detail = "Invalid Credentials")
	token_data = verify_access_token(token,credentials_exception)
	user = db.query(User).filter(User.email == token_data.email).first()
	if not user:
		raise  credentials_exception
	return UserOut.model_validate(user)
