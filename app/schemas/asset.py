from pydantic import BaseModel
class AssetBase(BaseModel):
	symbol : str	
	name : str
	asset_type : str

class AssetCreate(AssetBase):
	pass

class AssetOut(AssetCreate):
	id : int
	class Config:
		from_attributes = True

