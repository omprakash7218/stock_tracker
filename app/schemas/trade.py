from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime,timezone
from app.schemas.asset import AssetCreate,AssetOut
from app.schemas.portfolio import PortfolioOut

class TradeCreate(BaseModel):
	asset_id : int
	symbol : str
	quantity : float
	price : float
	trade_type : str
	trade_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TradeOut(TradeCreate):
	id : int
	symbol : str
	asset : AssetOut
	portfolios : PortfolioOut
	
	model_config = ConfigDict(from_attributes = True)
