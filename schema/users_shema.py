from pydantic import BaseModel, root_validator
from model.users_model import User
from database.db import SessionLocal
from fastapi import HTTPException, status



#Usually for testing API endpoint.
#Use when connected to a frontend (not whatsapp).


class user(BaseModel):

    name: str
    email: str
    password: str

    class Config:
        from_attributes = True

class show_user(BaseModel):
    name: str
    email: str
    
    class Config:
        from_attributes = True

class login(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class CreateUser(user):
    password: str

    class Config:

        from_attributes = True

    @root_validator(pre=True)
    @classmethod
    def validate_email(cls, values):
        email = values.get("email")

        with SessionLocal() as db:
            user_email = db.query(User).filter(User.email == email).first()
            if user_email:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Email already exists.")
        
        return values