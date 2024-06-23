from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

#Tries to get the DB from it's configuration location
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Route for getting all countries
@app.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_countries(db, skip=skip, limit=limit)
    return items

#Route for getting a specific country
@app.get("/{country_id}", response_model=schemas.Item)
def read_country(country_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_country(db, country_id=country_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_user

#Route for creating a country
@app.post("/", response_model=schemas.Item)
def create_user(country: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_country_by_name(db, name=country.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Country already exists")
    return crud.create_country(db=db, country=country)

#Route for updating a country
@app.put("/{country_id}", response_model=schemas.Item)
def update_country(country_id: int, country: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return crud.update_country(db=db, db_country=db_country, name = country.name)

#Route for deleting a country
@app.delete("/{country_id}", response_model=schemas.Item)
def delete_country(country_id: int, country: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return crud.delete_country(db=db, db_country=db_country, name = country.name)