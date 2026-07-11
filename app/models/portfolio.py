from sqlalchemy import Column, String, Integer, Boolean,DateTime
from app.database import Base
from app.models.user import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class Portfolio(Base):
	__tablename__="portfolios"
	id = Column(Integer,primary_key = True, nullable = False)
	user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
	name = Column(String,nullable = False)
	description = Column(String,nullable = False)
	created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable = False)
	updated_at = Column(DateTime(timezone=True),server_default = func.now(),onupdate=func.now(),nullable = False)
	owner = relationship("User",back_populates = "portfolios")
