from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.asset import Asset
from app.oauth2 import get_current_user
from app.schemas.asset import AssetCreate
from app.schemas.user import UserOut
from app.services.price_service import PriceService

router = APIRouter(prefix="/assets", tags=["ASSETS"])


@router.post("/")
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    asset_check = (
        db.query(Asset)
        .filter(Asset.symbol == asset.symbol or Asset.name == asset.name)
        .first()
    )
    if asset_check:
        raise HTTPException(status_code=406, detail="Asset already exist.")
    new_asset = Asset(**asset.dict())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


@router.get("/")
def show_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return {"message": assets}


@router.put("/{symbol}")
def edit_asset(
    symbol: str,
    asset1: AssetCreate,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is allowed here!"
        )
    asset_query = db.query(Asset).filter(
        Asset.symbol == symbol
    )  # This won't be helpful for next operation.
    asset = asset_query.first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="I don't see the asset in our database.",
        )
    update_data: dict = asset1.model_dump()
    asset_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(asset)
    print(asset)
    return {"message": asset}


@router.delete("/{symbol}")
def delete_asset(
    symbol: str,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is allowed here!"
        )
    asset = db.query(Asset).filter(Asset.symbol == symbol)
    if not asset.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    asset.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{symbol}")
def show_asset(symbol: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.symbol == symbol).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return asset


@router.get("/{symbol}/fetch_current_price")
def get_asset_price(symbol: str, asset_type: str):
    price = PriceService.get_price(symbol, asset_type)
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not fetch price."
        )
    return {"symbol": symbol, "price-inr": round(price, 3)}
