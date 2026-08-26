from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from app.database import Base


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, nullable=False)
    asset_id = Column(
        Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )
    symbol = Column(String, nullable=False)
    portfolio_id = Column(
        Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )
    trade_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    trade_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    portfolios = relationship("Portfolio")
    asset = relationship("Asset")
