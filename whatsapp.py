from sqlalchemy.orm import Session
from fastapi import FastAPI, WebSocket, status, Depends, APIRouter, HTTPException, Request
from services.twilio import send_message
import llama
from schema.llm_schema import choose, search
from database.db import get_db

from services.twilio import send_message
from twilio.rest import Client


app = APIRouter(tags = ["WhatsApp"])


@app.get('/testing/')
async def home():
    return {"Message": "Debugger TESTING----"}


#ENDPOINT

chosen = None
choice = None
@app.post("/twilio/")
async def twilio(request: Request, manager: llama.Choose = Depends(llama.model_choice), db: Session = Depends(get_db)):
    global chosen
    global choice
    sending_message = None

    provide = await request.form()
    input = provide.get('Body')
    sender_id = provide.get('From')
    print(sender_id, input)
 
    send_message(sender_id, "Thinking...")
    current_user = sender_id   

    if chosen not in ["Cohere large AI", "Google Gemini AI"]:
        chosen = await whatsapp_choose(choice = input, current_user=current_user, manager=manager)
        try:
            if chosen == "Cohere large AI":
                sending_message = "I'm happy to assist you. Could you describe any health concerns you're experiencing?"
            elif chosen == "Google Gemini AI":
                sending_message = "Would you like me to be detailed or concise? \nPlease reply with one of these options."
            else:
                sending_message = chosen
        except Exception as e:
            print(f"Failed to send message: {e}")

    elif chosen == "Google Gemini AI" and choice == None:

        if input.lower() == "detailed":
            input = "Tavily search"
        elif input.lower() == "concise":
            input = "Google search"

        if input in ["Tavily search", "Google search"]:
            choice = input
            res = f"Ready to assist! What questions do you have for me?"
        else:
            #res = "Hi would you like to chat with Tavily search or Google search?"
            res = "Would you like me to be detailed or concise? \n\nPlease reply with one of these options."

        try:
            #send_message(sender_id, res)
            sending_message = res
        except Exception as e:
            print(f"Failed to send message: {e}")            
        print(res)

    elif chosen in ["Cohere large AI", "Google Gemini AI"]:
        response = await llama.conversationing(input = input, choice = choice, manager = manager, db = db, current_user = current_user)        
        sending_message = response['Detail']["AI"]
        print(sending_message)

        sending_citaion = f"Source: \n\n{response['Detail']['CITATIONS']}"
        print(sending_citaion)

    try:
        send_message(sender_id, sending_message)
        if response['Detail']["CITATIONS"] != "":
            send_message(sender_id, sending_citaion)
    except Exception as e:
        print(f"Failed to send message: {e}")

    return {'message': status.HTTP_200_OK, "Detail": sending_message}




async def whatsapp_choose(choice, current_user, manager: llama.Choose = Depends(llama.model_choice)):
    
    if choice.lower() in ("detailed", "diagnosis") or "detail" in choice.lower():
        choice = "Cohere large AI"
    elif choice.lower() in ("quick", "check-in") or "quick" in choice.lower():
        choice = "Google Gemini AI"

    if choice not in ["Cohere large AI", "Google Gemini AI"]:
        user_choose = "Hi! How about a detailed diagnosis or a quick check-in? \n\nPlease reply with one of these options."
    else:
        choosen = await llama.choose(choice = choice, manager = manager, current_user = current_user)
        user_choose = choice 
    print(f"--------------------------------{user_choose}")

    return user_choose
