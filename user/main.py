
from multiprocessing.sharedctypes import synchronized
from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# To have independent db connection per request and then close it after request is finished.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# To insert new user into the table.
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# To get all the user details.
@app.get("/users", status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Update the details of users in the table.
@app.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_details(user_id: str, request: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_update = db.query(models.User).filter(models.User.id == user_id)
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_update.update(request.dict())
    db.commit()
    return "Updated successfully"

# To delete the user from the table.
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_delete = db.query(models.User).filter(models.User.id == user_id)
    if not user_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_delete.delete(synchronize_session=False)
    db.commit()

# To get the required number of user details.
@app.get("/user", status_code=status.HTTP_200_OK)
def limited_users(limit: int, skip: int = 0, db: Session = Depends(get_db)):
    user_list = db.query(models.User).offset(skip).limit(limit).all()
    return user_list
    





    
