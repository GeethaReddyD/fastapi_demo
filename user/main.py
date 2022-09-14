from fastapi import FastAPI,Depends,status
from . import schemas,models 
from .database import engine,SessionLocal 
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

app = FastAPI() 

#To have independent db connection per request and then close it after request is finished

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
# To insert new user into the table

@app.post("/create",status_code = status.HTTP_201_CREATED)
def create_user(request : schemas.User ,db : Session = Depends(get_db)):
    new_user = models.User(name = request.name ,age = request.age ,location = request.location)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user






