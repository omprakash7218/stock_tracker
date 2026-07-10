from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationships
from app.database import Base
class Trade(Base):
	__tablename__= "trades"
	id = Column(Integer,primary_key = True, nullable = False)
	asset_id = Column(Integer, ForeignKey("assets.id",ondelete="CASCADE"),nullable = False)
	portfolio_id = Column(Integer,ForeignKey("portfolios.id",ondelete="CASCADE"),nullable = False)
	trade_type = Column(String,nullable = False)
	quantity = Column(Float,nullable=False)
	price = Column(Float,nullable=False)
	trade_date=Column(DateTime(timezone=True),nullable = False)
	created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable= False)
# portfolio = relationships("Portfolio",back_populates="trades")
# asset = relationships("Asset")
