from fastapi import status,APIRouter,Depends,HTTPException,Response
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user
from app.database import get_db
from app.models.portfolio import Portfolio
from app.models.trade import Trade
from app.models.asset import Asset
from app.schemas.portfolio import PortfolioCreate,PortfolioOut
from app.schemas.user import UserOut
from app.verification import verify_portfolio,verify_asset
from app.services.price_service import PriceService

router = APIRouter(tags = ["PORTFOLIOS"],prefix="/portfolios")
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

@router.get("/{portfolio_id}",response_model = PortfolioOut)
def show_portfolio(portfolio_id:int,current_user : UserOut = Depends(get_current_user),db:Session=Depends(get_db)):
	portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id and Portfolio.user_id == current_user.id).first()
	if not portfolio: 
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN)
	return portfolio

@router.delete("/{portfolio_id}")
def delete_portfolio(portfolio_id:int,current_user:UserOut=Depends(get_current_user),db:Session=Depends(get_db)):
	query_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id and Portfolio.user_id == current_user.id)
	old_portfolio = query_portfolio.first()
	if not old_portfolio :
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
	db.delete(old_portfolio)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)


from app.services.portfolio_service import portfolio_service
@router.get("/{portfolio_id}/summary")
def portfolio_sumamry(portfolio_id : int,current_user : UserOut = Depends(get_current_user), db : Session = Depends(get_db)):
	results = portfolio_service(portfolio_id,current_user,db)
	if results is None :
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
	return results