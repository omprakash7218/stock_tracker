from fastapi import APIRouter,HTTPException,Response,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trade import Trade
from app.oauth2 import get_current_user
from app.schemas.user import UserOut
from app.schemas.trade import TradeCreate
from app.verification import verify_portfolio,verify_asset
from app.models.portfolio import Portfolio
from typing import List
router = APIRouter(tags=["TRADES"],prefix="/trades")

@router.get("/")
def show_trades(current_user:UserOut = Depends(get_current_user),db:Session=Depends(get_db)):
	portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
	portfolio_ids = [portfolio.id for portfolio in portfolios]
	#print(portfolios)
	trades = db.query(Trade).filter(Trade.portfolio_id.in_(portfolio_ids)).all()
	print(type(portfolios[0]))
	return trades

@router.post("/{portfolio_id}")
def create_trade(portfolio_id : int,asset : TradeCreate, current_user:UserOut=Depends(get_current_user),db:Session=Depends(get_db)):
	portfolio = verify_portfolio(portfolio_id,current_user,db)
	asset_object = verify_asset(asset.asset_id,db)
	trade = Trade(**asset.dict(),portfolio_id = portfolio_id)
	db.add(trade)
	db.commit()
	db.refresh(trade)
	return trade

@router.get("/{id}")
def show_trade(id:int , db:Session=Depends(get_db)):
	trade = db.query(Trade).filter(Trade.id == id).first()
	return trade

@router.delete("{id}")
def delete_trade(id:int, db:Session=Depends(get_db)):
	trade = db.query(Trade).filter(Trade.id == id)
	db.delete(trade)
	db.commit()
	return Response(status_code = 203, detail="No content")

