from fastapi import status,APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate
from app.oauth2 import get_current_user
router = APIRouter(tags = ["PORTFOLIOS"],prefix="/portfolio")
@router.get("/")
def show_portfolios(db:Session=Depends(get_db)):
	portfolios = db.query(Portfolio).all()
	return portfolios
@router.post("/")
def create_portfolio(portfolio:PortfolioCreate,current_user = Depends(get_current_user),db:Session=Depends(get_db)):
	new_portfolio = Portfolio(**portfolio.dict(),user_id = current_user.id)
	if db.query(Portfolio).filter(Portfolio.name == portfolio.name and Portfolio.user_id == current_user.id).first() == True:
		raise HTTPException(status_code = 400 , detail="Portfolio already exists.")
	db.add(new_portfolio)
	db.commit()
	db.refresh(new_portfolio)
	return new_portfolio


@router.put("/{portfolio_id}")
def edit_portfolio(portfolio_id : int, portfolio:PortfolioCreate,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
	portfolio_query = db.query(Portfolio).filter(Portfolio.id == portfolio_id and Portfolio.user_id == current_user.id)
	old_portfolio = portfolio_query.first()
	if not old_portfolio:
		raise HTTPException(status_code = 404,detail="Portfolio does not exist")
	portfolio_query.update(portfolio.dict(),synchronize_session=False)
	db.commit()
	db.refresh(portfolio_query.first())
	return portfolio_query.first()
