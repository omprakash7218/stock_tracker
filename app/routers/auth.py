from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.oauth2 import create_access_token
from app.schemas.user import Token
from app.utils import verify

router = APIRouter(tags=["AUTHENTICATION"])


@router.post("/login", response_model=Token)
def authenticate_user(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if verify(credentials.password, user.password) == False:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    token = create_access_token({"user_email": user.email})
    print("Logged in by : ", user.username)
    return {"access_token": token, "token_type": "bearer"}
