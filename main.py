from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_countries(db, skip=skip, limit=limit)
    return items

@app.get("/{country_id}", response_model=schemas.Item)
def read_country(country_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_country(db, country_id=country_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_user

@app.post("/", response_model=schemas.Item)
def create_user(country: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_country_by_name(db, name=country.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Country already exists")
    return crud.create_country(db=db, country=country)