from pydantic import BaseModel,Field
from datetime import datetime,timezone
from app.schemas.asset import AssetCreate,AssetOut
from app.schemas.portfolio import PortfolioOut

class TradeCreate(BaseModel):
	asset_id : int
	trade_type : str
	quantity : float
	price : float
	trade_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TradeOut(TradeCreate):
	id : int
	asset : AssetOut
	portfolios : PortfolioOut
	class Config: from_attributes = True
