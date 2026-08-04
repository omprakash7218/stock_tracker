from pydantic import BaseModel, ConfigDict
from app.schemas.portfolio import PortfolioOut
from datetime import datetime
 # __tablename__ = "cash_transactions"
    # id = Column(Integer, primary_key=True)
    # portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    # transaction_type = Column(String, nullable=False)
    # amount = Column(Float, nullable=False)
    # timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # portfolio = relationship("Portfolio", back_populates="cash_transactions")

class CashTransactionCreate(BaseModel):
    # portfolio_id: int
    # transaction_type : str
    amount : float

class CashTransactionOut(CashTransactionCreate):
    id : int
    portfolio_id : int
    portfolio : PortfolioOut
    timestamp : datetime
    