from pydantic import BaseModel,Field
from datetime import datetime,timezone


class TradeCreate(BaseModel):
	asset_id : int
	trade_type : str
	quantity : float
	price : float
	trade_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
