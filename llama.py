from sqlalchemy.orm import Session
from fastapi import WebSocket, status, Depends, APIRouter

import cohere


from database.db import get_db

from decouple import config

from services.cohere import conversation


from schema.users_shema import user
import oauth

app = APIRouter(tags = ["Llama"])


cohere_api = config('CohereAPI')



#Conversation Endpoint:
"""
@app.post("/response/")
async def conversationing(input: str, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):

    result = conversation(input=input, db=db, current_user=current_user)


    return {'message': status.HTTP_200_OK, "Detail": result}

"""
@app.websocket("/response/")
async def conversationing(websocket: WebSocket, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):
    await websocket.accept()
    while True:
        input = await websocket.receive_text()
        result = conversation(input=input, db=db, current_user=current_user)
        await websocket.send_text(result)