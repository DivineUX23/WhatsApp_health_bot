from sqlalchemy.orm import Session
from fastapi import FastAPI, WebSocket, status, Depends, APIRouter, HTTPException, Request
from services.twilio import send_message
import llama
from schema.llm_schema import choose, search
from database.db import get_db

from services.twilio import send_message


qa = llama.choose


app = APIRouter(tags = ["Llama"])


option = None

@app.post('/')
def home():
    return 'OK', 200


chosen_model = None

@app.post("/whatsapp_choose/")
def whatsapp_choose(current_user: str, request: Request, manager: llama.Choose = Depends(llama.model_choice)):

    #choice = chosen_model

    while chosen_model not in ["Cohere large AI", "Google Gemini AI"]:

        query = request.form['Body']
        sender_id = request.form['From']
        print(sender_id, query)

        chosen_model = query

        if chosen_model in ["Cohere large AI", "Google Gemini AI"]:
            break
        else:
            res = "Hi chat with Cohere large AI or Google Gemini AI"
            try:
                send_message(sender_id, res)
            except Exception as e:
                print(f"Failed to send message: {e}")
            
    choosen = choose(choice = chosen_model, manager = manager, current_user = current_user)     
    print(choosen)
    
    try:
        send_message(sender_id, choosen['Detail'])
    except Exception as e:
        print(f"Failed to send message: {e}")

    return {'message': status.HTTP_200_OK, "Detail": choosen['Detail']}



@app.post("/whatsapp_chat/")
def twilio(request: Request, current_user: str, manager: llama.Choose = Depends(llama.model_choice), db: Session = Depends(get_db)):

    global chosen_model
    choice = None

    #if chosen_model == "Google Gemini AI" and choice not in ["Cohere large AI", "Google Gemini AI"]:

    while chosen_model == "Google Gemini AI" and choice not in ["Cohere large AI", "Google Gemini AI"]:
        choice = request.form['Body']
        sender_id = request.form['From']
        print(sender_id, choice)

        if choice in ["Cohere large AI", "Google Gemini AI"]:
            break
        else:
            res = "Hi chat with Tavily search or Google search"
            
        try:
            send_message(sender_id, res)
        except:
            pass

        print(res)


    else:

        input = request.form['Body']
        sender_id = request.form['From']
        print(sender_id, input)
            
        res = llama.conversationing(input = input, choice = choice, manager = manager, db = db, current_user = current_user)
        print(res)

        try:
            send_message(sender_id, res['Detail'])
        except Exception as e:
            print(f"Failed to send message: {e}")

        return {'message': status.HTTP_200_OK, "Detail": res['Detail']}
