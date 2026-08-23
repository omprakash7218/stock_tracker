from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.oauth2 import get_current_user
from app.schemas.user import UserCreate, UserOut, UserPassword
from app.utils import hash_pwd, verify

router = APIRouter(tags=["USERS"], prefix="/users")


@router.get("/hello/{name}")
def hello_name(name):
    print("Hello ", name)
    return {"message": f"Hello! {name.upper()}"}


@router.get("/", response_model=list[UserOut])
def show_users(
    db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)
):
    users = db.query(User).all()
    return users


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    pwd = hash_pwd(user.password)
    user.password = pwd
    existing_user = (
        db.query(User)
        .filter(or_(User.email == user.email, User.username == user.username))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{username}")
def delete_user(
    username: str,
    password: UserPassword,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not authorized"
        )
    user_query = db.query(User).filter(
        User.username == username,
    )
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if not verify(password.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password entered!"
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{username}", response_model=UserOut)
def update_user(
    username: str,
    password: UserPassword,
    edit_user: UserCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    user_query = db.query(User).filter(
        User.username == username,
    )
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=404, detail="Not Found")
    if not verify(password.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Icorrect current password"
        )
    if (
        db.query(User)
        .filter(
            (User.email == user.email) | (User.username == user.username),
            User.id != user.id,
        )
        .first()
    ):
        raise HTTPException(
            status_code=406,
            detail="A user with same credentials already exist. Try different credentials.",
        )
    user_query.update(edit_user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user
