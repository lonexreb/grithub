# models/user_model.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    email: EmailStr
    hashed_password: str

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
