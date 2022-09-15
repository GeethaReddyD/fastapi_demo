from pydantic import BaseModel


class Userdetail(BaseModel):
    name : str 
    email: str
    password : str

    