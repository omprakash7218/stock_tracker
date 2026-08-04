from app.services.price_service import PriceService
from app.models.asset import Asset
from app.models.portfolio import Portfolio
from app.models.trade import Trade
from fastapi import HTTPException,status

def portfolio_service(portfolio_id , current_user,db):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id , Portfolio.user_id == current_user.id).first()
    if not portfolio:
        return None
    trades = db.query(Trade).join(Asset).filter(Trade.portfolio_id==portfolio_id).all()
    if not trades :
        return {
            "Portfolio id":portfolio_id,
            "Portfolio name": portfolio.name,
            "message": "No trades taken in this portfolio."
        }
    total_current_value = 0
    total_amount_invested = 0
    holdings = []
    
    for trade in trades:
        current_price = PriceService.get_price(trade.asset.symbol,trade.asset.asset_type)
        if current_price is None:
            current_price = trade.price
        invested_amount = trade.price * trade.quantity
        current_amount = current_price * trade.quantity
        profit_loss = current_amount - invested_amount
        profit_loss_percentage = (profit_loss/invested_amount) * 100 if invested_amount > 0 else 0
        holdings.append(
            {   
                "":"-------------------------------",
                "Asset Symbol":trade.asset.symbol,
                "Asset Name": trade.asset.name,
                "Current Price": round(current_price,2),
                "Quantity":trade.quantity,
                "Current Amount": round(current_amount,2),
                "Avg buy price": round(trade.price,2),
                "Invested Amount":invested_amount,
                "Profit/Loss": round(profit_loss,2),
                "Profit/Loss%": round(profit_loss_percentage,2)
            }
        )
        total_current_value += current_amount
        total_amount_invested += invested_amount
    portfolio_profit_loss = total_current_value - total_amount_invested
    portfolio_profit_loss_percentage = (portfolio_profit_loss/total_amount_invested)*100 if total_amount_invested > 0 else 0
    return {
        "Portfolio id":portfolio_id,
        "Portfolio name": portfolio.name,
        "Total current value":round(total_current_value,2),
        "Total amount invested":total_amount_invested,
        "Overall profit or loss":round(portfolio_profit_loss,2),
        "Profit or loss percentage":round(portfolio_profit_loss_percentage,2),
        "Holdings":holdings
    }
   