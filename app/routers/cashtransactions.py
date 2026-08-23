from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cash_transaction import CashTransaction
from app.oauth2 import get_current_user
from app.schemas.cash_transaction import CashTransactionCreate, CashTransactionOut
from app.schemas.user import UserOut
from app.verification import verify_portfolio

router = APIRouter(tags=["CASH TRANSACTIONS"], prefix="/cashtransaction")


@router.post("/{portfolio_id}/add_money", response_model=CashTransactionOut)
def deposit(
    portfolio_id: int,
    transaction: CashTransactionCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if transaction.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sorry , Deposit amount should be greater than 0.",
        )
    portfolio = verify_portfolio(portfolio_id, current_user, db)
    new_cash_transaction = CashTransaction(
        **transaction.dict(), portfolio_id=portfolio_id, transaction_type="deposit"
    )
    db.add(new_cash_transaction)
    db.commit()
    db.refresh(new_cash_transaction)
    portfolio.cash_balance += transaction.amount
    db.commit()
    return new_cash_transaction


@router.post("/{portfolio_id}/withdraw", response_model=CashTransactionOut)
def withdraw(
    portfolio_id: int,
    transaction: CashTransactionCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if transaction.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sorry , Withdrawal amount should be greater than 0.",
        )
    portfolio = verify_portfolio(portfolio_id, current_user, db)
    if portfolio.cash_balance < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Not enough funds to withdraw!",
        )
    else:
        new_cash_transaction = CashTransaction(
            **transaction.dict(), portfolio_id=portfolio_id, transaction_type="withdraw"
        )
        db.add(new_cash_transaction)
        db.commit()
        db.refresh(new_cash_transaction)
        portfolio.cash_balance -= transaction.amount
        db.commit()
    return new_cash_transaction
