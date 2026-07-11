from app.database import Base
from sqlalchemy import Integer,Boolean,String,Column,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
class User(Base):
	__tablename__= "users"
	username = Column(String,unique=True,nullable = False)
	id = Column(Integer,primary_key=True, nullable = False)
	email = Column(String, unique = True, nullable = False)
	password = Column(String, nullable = False)
	created_at = Column(DateTime(timezone=True),nullable = False , server_default = func.now())
	portfolios = relationship("Portfolio" , back_populates="owner")
