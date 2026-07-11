from fastapi import APIRouter,HTTPException,Depends,status,Response
from sqlalchemy.orm import Session
from app.schemas.asset import AssetCreate
from app.database import get_db
from app.models.asset import Asset


router = APIRouter(prefix="/assets",tags=["ASSETS"])

@router.post("/")
def create_asset(asset:AssetCreate,db:Session=Depends(get_db)):
	
	if db.query(Asset).filter(Asset.symbol == asset.symbol or Asset.name == asset.name)==True:
		raise HTTPException(status_code = 406, detail="Asset already exist.")
	new_asset = Asset(**asset.dict())
	db.add(new_asset)
	db.commit()
	db.refresh(new_asset)
	return new_asset 
@router.get("/")
def show_assets(db:Session=Depends(get_db)):
	assets = db.query(Asset).all()
	return {"message":assets}

@router.put("/{symbol}")
def edit_asset(symbol:str , asset1:AssetCreate , db:Session=Depends(get_db)):
	asset_query =db.query(Asset).filter(Asset.symbol == symbol) # This won't be helpful for next operation. 
	asset = asset_query.first()
	if not asset:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"I don't see the asset in our database.")	
	if db.query(Asset).filter(Asset.symbol == asset.symbol or Asset.name == asset.name):
		raise HTTPException(status_code = 406 , detail="Asset already exists.")
	asset_query.update(asset1.dict(),synchronize_session= False)
	db.commit()
	print(asset)
	return {"message":asset}
@router.delete("/{symbol}")
def delete_asset(symbol:str,db:Session=Depends(get_db)):
	asset = db.query(Asset).filter(Asset.symbol == symbol)
	if asset.first() == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
	asset.delete(synchronize_session = False)
	db.commit()
	return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.get("/{symbol}")
def show_asset(symbol:str,db:Session=Depends(get_db)):
	asset = db.query(Asset).filter(Asset.symbol == symbol).first()
	if not asset:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
	return asset



