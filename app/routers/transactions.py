from fastapi import APIRouter,HTTPException,status,Response,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.oauth2 import get_current_user
from app.schemas.user import userOut
from app.models.trade import Trade
from app.models.portfolio import Portfolio
router = APIRouter(tags = ["TRANSACTIONS"],prefix = "/transactions")

@router.get("/{id}")
def show_transaction(id : int, current_user: UserOut = Depends(get_current_user), db:Session=Depends(get_db)):

	transaction = db.query(Transaction).filter(Transaction.id == id).first()
	if not transaction:
		raise HTTPException(satatus_code = status.HTTP_404_NOT_FOUND)
	trade = db.query(Trade).filter(Trade.id == transaction.trade_id ).first()
	if not trade :
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
	verify_portfolio(trade.portfolio_id ,current_user,db)
	return transaction


# ? JOINS In Action

@router.get("/")
def show_transactions(current_user : UserOut = Depends(get_current_user), db:Session=Depends(get_db)):
	transactions = db.query(Transaciton).join(Trade).join(Portfolio).filter(Portfolio.user_id == current_user.id).all()
	return transactions