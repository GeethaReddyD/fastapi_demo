from fastapi import FastAPI,Depends,status
from . import schemas,models 
from .database import engine,SessionLocal 


models.Base.metadata.create_all(engine)

app = FastAPI() 

#To have independent db connection per request and then close it after request is finished

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





