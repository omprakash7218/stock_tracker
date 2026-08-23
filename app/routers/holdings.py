from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.holding import Holding
from app.oauth2 import get_db

router = APIRouter(tags=["HOLDINGS"], prefix="/holdings")


@router.get("/{portfolio_id}")
def show_holdings(portfolio_id: int, db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()

    return holdings
