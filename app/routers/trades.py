from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.models.trade import Trade
from app.oauth2 import get_current_user
from app.schemas.trade import TradeCreate, TradeOut
from app.schemas.user import UserOut
from app.verification import verify_asset, verify_portfolio

router = APIRouter(tags=["TRADES"], prefix="/trades")


@router.get("/", response_model=list[TradeOut])
def show_trades(
    current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)
):
    # portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    # portfolio_ids = [portfolio.id for portfolio in portfolios]
    # #print(portfolios)
    # trades = db.query(Trade).filter(Trade.portfolio_id.in_(portfolio_ids)).all()
    # print(type(portfolios[0]))
    # return trades
    trades = (
        db.query(Trade)
        .join(Portfolio)
        .filter(Portfolio.user_id == current_user.id)
        .all()
    )
    if not trades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return trades


@router.post("/{portfolio_id}", response_model=TradeOut)
def create_trade(
    portfolio_id: int,
    asset: TradeCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_portfolio(portfolio_id, current_user, db)
    verify_asset(asset.asset_id, asset.symbol, db)
    holding_query = db.query(Holding).filter(
        Holding.portfolio_id == portfolio_id, Holding.symbol == asset.symbol
    )
    holding = holding_query.first()
    if not holding:
        if asset.trade_type == "sell":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough quantity"
            )
        elif asset.trade_type == "buy":
            trade = Trade(**asset.dict(), portfolio_id=portfolio_id)
            db.add(trade)
            db.commit()
            db.refresh(trade)
            create_holding = Holding(
                portfolio_id=portfolio_id,
                symbol=asset.symbol,
                quantity=asset.quantity,
                average_buy_price=asset.price,
            )
            db.add(create_holding)
            db.commit()
            db.refresh(create_holding)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can either do buy or sell trade only.",
            )
    elif asset.trade_type == "sell":
        if holding.quantity < asset.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough quantity"
            )
        trade = Trade(**asset.dict(), portfolio_id=portfolio_id)
        db.add(trade)
        db.commit()
        db.refresh(trade)
        if holding.quantity == asset.quantity:
            db.delete(holding)
        else:
            remaining_holding = {
                "portfolio_id": portfolio_id,
                "symbol": asset.symbol,
                "quantity": holding.quantity - asset.quantity,
                "average_buy_price": holding.average_buy_price,
            }
            holding_query.update(remaining_holding, synchronize_session=False)  # type: ignore[arg-type]
        db.commit()
    elif asset.trade_type == "buy":
        trade = Trade(**asset.dict(), portfolio_id=portfolio_id)
        db.add(trade)
        db.commit()
        db.refresh(trade)
        new_holding = {
            "portfolio_id": portfolio_id,
            "symbol": asset.symbol,
            "quantity": holding.quantity + asset.quantity,
            "average_buy_price": (
                asset.price * asset.quantity
                + holding.average_buy_price * holding.quantity
            )
            / (asset.quantity + holding.quantity),
        }
        holding_query.update(new_holding, synchronize_session=False)  # type: ignore[arg-type]
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can either do buy or sell trade only.",
        )
    return trade
    # id = int
    # portfolio_id = int
    # symbol = str
    # quantity = int
    # average_buy_price = float


@router.get("/{id}", response_model=TradeOut)
def show_trade(
    id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    trade = db.query(Trade).filter(Trade.id == id).first()
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    verify_portfolio(trade.portfolio_id, current_user, db)

    return trade


@router.delete("/{id}")
def delete_trade(
    id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    trade = db.query(Trade).filter(Trade.id == id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Not found")
    verify_portfolio(trade.portfolio_id, current_user, db)

    db.delete(trade)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def edit_trade(
    id: int,
    edited_trade: TradeCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    trade_query = db.query(Trade).filter(Trade.id == id)
    trade = db.query(Trade).filter(Trade.id == id).first()
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    verify_portfolio(trade.portfolio_id, current_user, db)
    updated_data = edited_trade.model_dump()
    trade_query.update(updated_data, synchronize_session=False)  # type: ignore[arg-type]
    db.commit()
    db.refresh(trade)
    return trade
