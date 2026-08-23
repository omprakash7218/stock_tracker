# pydantic model
from pydantic import BaseModel,ConfigDict
from app.schemas.user import UserOut
class PortfolioCreate(BaseModel):
	name : str
	description : str
	cash_balance : float = 0.0

class PortfolioOut(PortfolioCreate):
	id : int
	owner : UserOut
	cash_balance : float
	model_config = ConfigDict(from_attributes = True)
class PortfolioUpdate(BaseModel):
	name : str
	description : str
