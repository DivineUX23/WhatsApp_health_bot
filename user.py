from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from hashing import hash
from database.db import get_db
from model.users_model import User
from schema.users_shema import user
from schema.users_shema import show_user
from hashing import hash
import services.user_services
from uuid import uuid4



from schema.users_shema import user
import oauth

from model.users_model import User
from hashing import hash


app = APIRouter(tags= ["User"])


@app.post("/sign_up")
async def sign_up(user: user, db: Session = Depends(get_db)):

    new_users = services.user_services.sign_up(user=user, db=db)

    verification_token = str(uuid4())
    
    new_users.verification_token = verification_token
    db.commit()

    return {'message': "User created successfully.", 'detail': show_user.from_orm(new_users)}

