# pydantic model
from pydantic import BaseModel

class PortfolioCreate(BaseModel):
	name : str
	description : str
