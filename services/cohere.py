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
cohere_model_name = os.getenv("COHERE_MODEL_NAME")


class Chatbot:
    def __init__(self):
        self.conversation_id = str(uuid.uuid4())
        self.preamble_override = """You are a health information search assistant focused on helping users find reliable online resources related to health topics and medical conditions. Through active listening and follow-up questions, gather details about the user's health-related query to fully understand their information needs. Ask clarifying questions to narrow down and pinpoint the exact health topic, condition, or information they are seeking.

                            Your role is to assist users in finding trustworthy, high-quality online resources that provide accurate and up-to-date information related to their health query. This may include suggesting specific websites, web pages, articles, or other digital content from reputable health organizations, medical institutions, or recognized experts in the relevant field.

                            If the health query is broad or vague, engage in a dialogue to better understand the user's specific concerns, symptoms, or requirements. Based on their responses, suggest relevant keywords, search terms, or search strategies that could yield more targeted and useful health information results.

                            Maintain an objective, helpful tone throughout the conversation, and avoid promoting or endorsing any particular websites or sources unless they are widely recognized as authoritative and reputable in the medical or health domain. 

                            Always end the conversation by reminding the user that while you aim to provide helpful search guidance for health information, they should critically evaluate the information they find online and rely on authoritative medical sources, especially for important health decisions or concerns. Emphasize that your search assistance should not replace professional medical advice, diagnosis, or treatment.
                            """

    def generate_response(self, message: str):
        co = cohere.Client(api_key)
        
        messages= f"""Help this user find reliable online resources related to their health query or medical condition. Through active listening and follow-up questions, gather details about the user's health information needs to fully understand their query. Ask clarifying questions to narrow down and pinpoint the exact health topic or condition they are seeking information about.
                            User: {message} 
                            Health Information Search Assistant: """
        response = co.chat(
                        model=cohere_model_name,
                        message=messages,
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
    
    

    #TAKE_NOTE: the code below enables streaming with a little tweak. Ensure co.chat stream is True
    """
    if not response:
        raise HTTPException(status_code=500, detail="Chatbot response error")
    
    citations_flag = False

    result = []
    text = ""
    for event in response:
        stream_type = type(event).__name__
        
        # Text
        if stream_type == "StreamTextGeneration":
            text += event.text


        # Citations
        if stream_type == "StreamCitationGeneration":
            if not citations_flag:

                citations_flag = True
            print(event.citations[0])
            result.append(event.citations[0])
    """
    
    print({"AI":text, "CITATIONS":result})
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