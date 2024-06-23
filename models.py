from sqlalchemy import Column, Integer, String
from .database import Base

#Generates a database model
class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)