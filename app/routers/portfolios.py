from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.portfolio import Portfolio
from app.models.user import User
from app.oauth2 import get_current_user
from app.schemas.portfolio import PortfolioCreate, PortfolioOut, PortfolioUpdate
from app.schemas.user import UserOut, UserPassword
from app.services.portfolio_services import portfolio_service
from app.utils import verify

router = APIRouter(tags=["PORTFOLIOS"], prefix="/portfolios")


@router.get("/")
def show_portfolios(
    current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)
):
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    return portfolios


@router.post("/")
def create_portfolio(
    portfolio: PortfolioCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    portfolio_check = (
        db.query(Portfolio)
        .filter(Portfolio.name == portfolio.name, Portfolio.user_id == current_user.id)
        .first()
    )
    if portfolio_check:
        raise HTTPException(status_code=400, detail="Portfolio already exists.")
    new_portfolio = Portfolio(**portfolio.dict(), user_id=current_user.id)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioOut)
def show_portfolio(
    portfolio_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id)
        .first()
    )
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return portfolio


@router.put("/{portfolio_id}")
def edit_portfolio(
    portfolio_id: int,
    portfolio: PortfolioUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    portfolio_query = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id
    )
    old_portfolio = portfolio_query.first()
    if not old_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio does not exist")
    update_data: dict = portfolio.model_dump()
    portfolio_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(old_portfolio)
    return old_portfolio


@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    password: UserPassword,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query_portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id
    )
    old_portfolio = query_portfolio.first()
    if not old_portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not verify(password.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Mismatched!"
        )
    db.delete(old_portfolio)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{portfolio_id}/summary")
def portfolio_sumamry(
    portfolio_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = portfolio_service(portfolio_id, current_user, db)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return results
