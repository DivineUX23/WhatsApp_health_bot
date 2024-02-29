from sqlalchemy.orm import Session
from fastapi import FastAPI, WebSocket, status, Depends, APIRouter
from typing import Optional
import cohere


from database.db import get_db

from decouple import config

from services.cohere import conversation
from services.gemini import run

from schema.users_shema import user
from schema.llm_schema import choose, search
import oauth


fastapp = FastAPI()
app = APIRouter(tags = ["Llama"])
fastapp.include_router(app)


cohere_api = config('CohereAPI')


class Choose:
    def __init__(self, user_choice) -> None:
        self.user_choice = user_choice
        self.running_model = None

        if user_choice == "Cohere large AI":
            self.running_model = conversation

        elif user_choice == "Google Gemini AI":
            self.running_model = run

    def current_model(self):
        return self.running_model

        
#Choose model Endpoint:

@app.post("/choose_model/")
async def choose(choice: choose, current_user: user = Depends(oauth.get_current_user)):

    chose_llm = Choose(choice)

    fastapp.llm_instance = chose_llm

    return {'message': status.HTTP_200_OK, "Detail": ""}


#Conversation Endpoint:

@app.post("/response/")
async def conversationing(input: str, choice: search, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):

    chose_llm = fastapp.llm_instance

    model=chose_llm.current_model()

    if model == conversation:
        result = model(input=input, db=db, current_user=current_user)
    elif model == run:
        result = model(input=input, choice=choice, db=db, current_user=current_user)


    return {'message': status.HTTP_200_OK, "Detail": result}

"""
@app.websocket("/response/")
async def conversationing(websocket: WebSocket, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):
    await websocket.accept()
    while True:
        input = await websocket.receive_text()
        result = conversation(input=input, db=db, current_user=current_user)
        await websocket.send_text(result)"""