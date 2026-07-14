from app.database import Base
from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, Float,text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from app.enums import TransactionType
from sqlalchemy.orm import relationship
class Transaction(Base):
    __tablename__="transactions"
    id = Column(Integer,primary_key = True)
    trade_id = Column(Integer,ForeignKey("trades.id",ondelete="CASCADE"),nullable = False)
    type= Column(SQLEnum(TransactionType),nullable = False)    # ! Restricted
    amount = Column(Float,nullable = False)
    fee = Column(Float, nullable = False)
    timestamp = Column(DateTime(timezone = True), server_default=func.now(),nullable = False)
    notes = Column(String,nullable = True)
    trade = relationship("Trade")