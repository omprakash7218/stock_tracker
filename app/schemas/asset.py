from pydantic import BaseModel
from pydantic import ConfigDict
class AssetBase(BaseModel):
	symbol : str
	name : str
	asset_type : str

class AssetCreate(AssetBase):
	pass

class AssetOut(AssetCreate):
	id : int
	model_config = ConfigDict(from_attributes = True)
