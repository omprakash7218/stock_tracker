from pydantic import BaseModel,ConfigDict
from typing import Optional
from app.enums import TransactionType
from datetime import datetime
from app.schemas.trade import TradeOut
class TransactionCreate(BaseModel):
    # trade_id: int
    # type: TransactionType
    # amount: float
    fee: float
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    # trade_id: int
    type: TransactionType
    amount: float
    fee: float
    timestamp: datetime
    notes: Optional[str] = None
    trade: TradeOut
    model_config= ConfigDict(from_attributes = True)
