from fastapi import APIRouter, Depends,  status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import token_key
from database.db import get_db
from model.users_model import User
from schema import users_shema

from sqlalchemy.orm import Session
from hashing import hash

app = APIRouter(tags=['User'])

@app.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user=db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hate to say but {user} does not exist")

    if not hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hate to say but your password is incorrect")


    token = token_key.create_access_token(data={"sub": user.email})
    
    return {'access_token': token, 'token_type': 'bearer'}
