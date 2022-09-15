from fastapi import FastAPI,Depends,status
from . import schemas,models 
from .database import engine,SessionLocal 
from sqlalchemy.orm import Session 
from passlib.context import CryptContext

models.Base.metadata.create_all(engine)

app = FastAPI() 

#To have independent db connection per request and then close it after request is finished

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
# To insert new user into the table

@app.post("/create",status_code = status.HTTP_201_CREATED)

def create_user(request : schemas.Userdetail ,db : Session = Depends(get_db)):

    hashed_password = pwd_context.hash(request.password)
    new_user = models.Userdetail(name = request.name ,email = request.email ,password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user
    






