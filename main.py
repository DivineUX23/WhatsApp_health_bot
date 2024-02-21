from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from database.db import get_db

#for testing
from sqlalchemy import func
#===========================

from user import app as user
from user_login import app as user_login
from llama import app as llama


app = FastAPI()



origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




app.include_router(user, tags=["User"])
app.include_router(user_login, tags=["User"])
app.include_router(llama, tags=["Llama"])


"""
#Testing:
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    
    
    Audio_no = db.query(func.max(Audio.id)).scalar()
    TEST = db.query(Audio).filter(Audio.id == 41).first()
    print(TEST.transcript)

    Audio_no = db.query(func.max(Audio.id)).scalar()
    TEST = db.query(Audio).filter(Audio.id == 41).first()
    print(TEST.transcript)

    return {"Message": "Debugger page"}
"""