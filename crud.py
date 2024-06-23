from sqlalchemy.orm import Session

from . import models, schemas

#Implements the method for getting a specific country
def get_country(db: Session, country_id: int):
    return db.query(models.Country).filter(models.Country.id == country_id).first()

def get_country_by_name(db: Session, name: str):
    return db.query(models.Country).filter(models.Country.name == name).first()

#Implements for creating a country
def create_country(db: Session, country: schemas.ItemCreate):
    db_country = models.Country(name=country.name)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

#Implements the method for getting all countries
def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Country).offset(skip).limit(limit).all()

#Implements the method for updating a country
def update_country(db: Session, db_country: schemas.ItemCreate ,name: str):
    db_country.name = name
    db.commit()
    db.refresh(db_country)
    return db_country

#Implements the method for deleting a country
def delete_country(db: Session, db_country: schemas.ItemCreate ,name: str):
    db.delete(db_country)
    db.commit()
    return db_country

