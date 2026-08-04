from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user,get_db
from app.schemas.user import UserOut
from app.models.holding import Holding
router = APIRouter(tags = ["HOLDINGS"],prefix="/holdings")

@router.get("/{portfolio_id}")
def show_holdings(portfolio_id : int ,db:Session=Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.portfolio_id==portfolio_id).all()

    return holdings