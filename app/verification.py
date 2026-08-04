from app.models.portfolio import Portfolio
from fastapi import HTTPException,status
from app.models.asset import Asset
def verify_portfolio(portfolio_id,current_user,db):
	portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
	if not portfolio:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid portfolio id.")
	if portfolio.user_id != current_user.id:
		raise HTTPException(status_code = 403, detail="Unauthorized access")	
	return  portfolio
def verify_asset(asset_id,asset_symbol,db):
	asset = db.query(Asset).filter(Asset.id == asset_id,Asset.symbol == asset_symbol).first()
	if not asset:
		raise HTTPException(status_code =status.HTTP_404_NOT_FOUND)
	return asset
