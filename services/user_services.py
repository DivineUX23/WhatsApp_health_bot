from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends
from hashing import hash
from database.db import get_db
from model.users_model import User
from schema.users_shema import user
from hashing import hash

from schema.users_shema import user
import oauth


def sign_up(user: str, db: Session = Depends(get_db)):

    new_users = User(name = user.name, 
                            email = user.email,
                            password = hash.bcrypt(user.password))
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    return new_users