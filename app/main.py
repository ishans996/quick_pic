from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/images/custom")
async def get_custom_image_url(placeid:str = '', photoref:str = '', db: Session = Depends(get_db)):
    if placeid == '' and photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the fields placeid and photoref are both empty or you may have misspelled the names of query parameters in your request' 
        }
    elif placeid == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field placeid  is empty or you may have misspelled the name of this field in your request' 
        }
    elif photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field photoref field is empty or you may have misspelled the name of this field in your request' 
        }

    db_user = crud.get_image_url(db,placeid=placeid)
    print(db_user)
    if db_user:
        return {
        'status' : 'FOUND', 
        'placeid' : db_user.placeid,
        'image_url' : db_user.photo_url
    }
    else:
        image_url = f'https://domainname.com/{placeid}.jpg'
        place = crud.create_place(db=db, placeid=placeid,photoref=photoref,photo_url=image_url)   
        if place:
            return {
                'status' : 'CREATED', 
                'placeid' : place.placeid,
                'image_url' : place.photo_url
            }
    