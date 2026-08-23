from sqlalchemy import Column, Integer, String

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    symbol = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, unique=True)
    asset_type = Column(String, nullable=False)
