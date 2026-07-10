from pydantic import BaseModel

class AssetCreate(BaseModel):
	symbol:str
	name:str
	asset_type:str
