
from fastapi import FastAPI,Depends,status,HTTPException
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

def create_user(request : schemas.User ,db : Session = Depends(get_db)):

    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name = request.name ,email = request.email ,password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user
    
# To get all the user details
@app.get("/read", status_code = status.HTTP_200_OK)

def read_users(db : Session = Depends(get_db)):
    
    user_list = db.query(models.User).all()
    return user_list

# To delete the user from the table 
@app.delete('/delete/{id}',status_code = status.HTTP_204_NO_CONTENT) 

def delete_user(id ,db : Session = Depends(get_db)):
    user_delete = db.query(models.User).filter(models.User.id == id)
    if not user_delete.first():

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User is not found")

    user_delete.delete(synchronize_session=False)
    db.commit()
    return "User has been deleted successfully" 

