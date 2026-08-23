from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums import TradeType, TransactionType
from app.models.portfolio import Portfolio
from app.models.trade import Trade
from app.models.transaction import Transaction
from app.oauth2 import get_current_user
from app.schemas.transaction import TransactionCreate
from app.schemas.user import UserOut

router = APIRouter(tags=["TRANSACTIONS"], prefix="/transactions")


@router.get("/{id}")
def show_transaction(
    id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    transaction = (
        db.query(Transaction)
        .join(Trade)
        .join(Portfolio)
        .filter(Transaction.id == id, Portfolio.user_id == current_user.id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return transaction


# ? JOINS In Action


@router.get("/")
def show_transactions(
    current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)
):
    transactions = (
        db.query(Transaction)
        .join(Trade)
        .join(Portfolio)
        .filter(Portfolio.user_id == current_user.id)
        .all()
    )
    return transactions


@router.post("/{trade_id}")
def create_transaction(
    trade_id: int,
    transaction: TransactionCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    trade = (
        db.query(Trade)
        .join(Portfolio)
        .filter(Portfolio.user_id == current_user.id, Trade.id == trade_id)
        .first()
    )
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if (
        trade.trade_type == TradeType.BUY
    ):  # ? trade.trade_type  --- it is not just a string any more , it is a TradeType enum value
        calculated_type = TransactionType.DEBIT
    else:
        calculated_type = TransactionType.CREDIT
    transaction = Transaction(
        trade_id=trade.id,
        type=calculated_type,
        amount=trade.price * trade.quantity,
        fee=transaction.fee,
        notes=transaction.notes,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.put("/{transaction_id}")
def edit_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    transaction_obj = (
        db.query(Transaction)
        .join(Trade)
        .join(Portfolio)
        .filter(Transaction.id == transaction_id, Portfolio.user_id == current_user.id)
        .first()
    )
    if not transaction_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    transaction_obj.fee = transaction.fee

    transaction_obj.notes = transaction.notes

    db.commit()
    db.refresh(transaction_obj)

    return transaction_obj
