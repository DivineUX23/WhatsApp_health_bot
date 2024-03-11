from sqlalchemy.orm import Session
from fastapi import FastAPI,HTTPException,status, Depends

import cohere

from database.db import get_db
import json
from decouple import config


from schema.users_shema import user
import oauth
import uuid

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
api_key = os.getenv("CohereAPI")


cohere_api = config("CohereAPI")


class Chatbot:
    def __init__(self):
        self.conversation_id = str(uuid.uuid4())
        self.preamble_override ="""You are a highly skilled and empathetic doctor. 
                                    Your primary role is to diagnose ailments based on the symptoms described by the patient. 
                                    You should ask relevant questions to gather enough information about the patient's condition. 
                                    Once you have enough information, you should provide a possible diagnosis and suggest appropriate and actionable treatments or medications. 
                                    After providing a detailed diagnosis and suggesting appropriate and actionable treatment, remind the patient that while you can provide advice based on their symptoms, they should seek professional medical help for a definitive diagnosis and treatment. 
                                    Remember to maintain a professional and caring tone throughout the conversation.  
                                """

    def generate_response(self, message: str):
        co = cohere.Client(api_key)
        response = co.chat(
                        message=message,
                        preamble_override=self.preamble_override,
                        conversation_id=self.conversation_id,
                        stream=False,
                        temperature=0.3,
                        return_chat_history=True,
                        prompt_truncation='AUTO',
                        citation_quality='fast',
                        connectors=[{"id":"web-search"}],
                        )

        #for event in response:
            #yield event

        return response

#conversation with AI:
chatbot = Chatbot()

def conversation(input: str, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):
    message = input
    print(f"User: {message}")
    response = chatbot.generate_response(message)

    text = response.text
    documents = response.documents
    result = ""
    seen = set()

    for doc in documents:
        url = doc['url']

        if url not in seen:
            seen.add(url)
            result += f"\n\n{url}"

    print(f"The text is: {text}")
    print(f"The url of the first document is: {result}")
    
    #the code below enables streaming with a little tweak. Ensure co.chat stream is True
    """
    if not response:
        raise HTTPException(status_code=500, detail="Chatbot response error")
    
    citations_flag = False

    resultant = []
    result = ""
    for event in response:
        stream_type = type(event).__name__
        
        # Text
        if stream_type == "StreamTextGeneration":
            result += event.text


        # Citations
        if stream_type == "StreamCitationGeneration":
            if not citations_flag:

                citations_flag = True
            print(event.citations[0])
            resultant.append(event.citations[0])
    """
    #print({"AI":text, "CITATIONS":result})
    return {"AI":text, "CITATIONS":result}


"""
Sending the Ai response as a dictionary which has a string (AI response) and a list showing the citaions something like this:

 {
    'AI': "It's best to begin by first establishing what you are experiencing. Do you have physical or mental symptoms you are concerned about? 
    Try to describe your symptoms in as much detail as possible so we can explore potential causes and solutions. ", 
    
    'CITATIONS':   link 1
                    link 2
                    link 3...}

"""



#if __name__ == "__main__":
#    conversation()