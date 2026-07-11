# pydantic model
from pydantic import BaseModel
from app.schemas.user import UserOut

class PortfolioCreate(BaseModel):
	name : str
	description : str

class PortfolioOut(PortfolioCreate):
	id : int
	owner : UserOut
	class Config:
		from_attributes = True