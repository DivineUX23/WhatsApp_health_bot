from sqlalchemy.orm import Session
from fastapi import FastAPI, WebSocket, status, Depends, APIRouter, HTTPException
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

    def __init__(self):
        self.running_model = None

    def model(self, user_choice) -> None:
        self.user_choice = user_choice

        if user_choice == "Cohere large AI":
            self.running_model = conversation

        elif user_choice == "Google Gemini AI":
            self.running_model = run

        return self.running_model


    def current_model(self):
        if self.running_model is None:
            raise HTTPException(status_code=400, detail="Model not set")
        return self.running_model


model_manager = Choose()

def model_choice():
    return model_manager


#Choose model Endpoint:

@app.post("/choose_model/")
async def choose(choice: choose, manager: Choose = Depends(model_choice), current_user: user = Depends(oauth.get_current_user)):

    user_choose = manager.model(choice)
    return {'message': status.HTTP_200_OK, "Detail": f"{user_choose} is now live"}


#Conversation Endpoint:
@app.post("/response/")
async def conversationing(input: str, choice: search, manager: Choose = Depends(model_choice), db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):

    model=manager.current_model()

    if model == conversation:
        result = model(input=input, db=db, current_user=current_user)
    elif model == run:

        if not choice:
            raise HTTPException(status_code=400, detail="Choice parameter is required for the Google Gemini AI model")
        
        result = model(input=input, choice=choice, db=db, current_user=current_user)

    return {'message': status.HTTP_200_OK, "Detail": result}
