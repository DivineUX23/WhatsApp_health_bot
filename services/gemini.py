from typing import List, Tuple

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper
import json

from schema.llm_schema import search
from sqlalchemy.orm import Session
from fastapi import FastAPI,HTTPException,status, Depends
from database.db import get_db

from schema.users_shema import user
import oauth

import os
from dotenv import load_dotenv

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_model_name = os.getenv("GOOGLE_MODEL_NAME")


class Gemini:
    def __init__(self):
        self.description =  """You are a medical chatbot focused on diagnosing and suggesting remedies for common, non-emergency conditions when professional care is unavailable. Through active listening and follow-up questions, gather detailed information about the user's symptoms to determine the specific condition. Ask probing questions, just like a doctor would, to pinpoint the exact ailment before providing potential diagnoses.

                                    Your scope covers minor illnesses, injuries, and general health concerns like colds, flu, headaches, muscle aches, minor cuts/burns, allergic reactions, digestive issues, and sleep disturbances. For these conditions, suggest appropriate over-the-counter medications, home remedies, or lifestyle changes.

                                    However, if symptoms indicate a potentially serious or complex condition requiring immediate attention, advise the user to seek emergency medical care or consult a healthcare professional promptly. Maintain an objective, caring tone throughout, avoiding subjective recommendations. And keep your response consice and well structured.

                                    Always end the conversation with a disclaimer that your recommendations are not a substitute for professional medical advice, diagnosis, or treatment.
                                    """

        self.tool = None

        self.tavily = None

        self.input = None

        self.agent_executor = None

        self.chat_history = []


    def tools(self, choose_tool):

        search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)

        google_tool = Tool(
            name = "google_search",
            description = self.description,
            func = search.run,
        )

        search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
        tavily_tool = TavilySearchResults(api_wrapper=search, description=self.description)
        self.tavily = [tavily_tool]

        if choose_tool.lower() == "tavily search":
            print("\nTavily search activated\n")
            self.tool = [tavily_tool]

        elif choose_tool.lower() == "google search":
            print("\nGoogle search activated\n")
            self.tool = [google_tool]

        else:
            raise HTTPException(status_code=500, detail="Provide a valid input (Y or N)")    




    def gemini(self, message):
                
        input = f"""Diagnose and suggest remedies for this user's codition. Through active listening and follow-up questions, gather detailed information about the user's symptoms to determine the specific condition. Ask probing questions, just like a doctor would, to pinpoint the exact ailment before providing potential diagnoses. keep your response consice and well structured.
                                            User: {message} 
                                            Medical chatbot: """


        self.input = input
        #--class.gemini:
        llm = ChatGoogleGenerativeAI(temperature=0.1, model=google_model_name, google_api_key=gemini_api_key)

        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )


        llm_with_tools = llm.bind(functions=self.tool)


        from langchain_core.messages import AIMessage, HumanMessage

        agent = (
            {
                "input":lambda x: x["input"],
                "chat_history":lambda x: x["chat_history"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )


        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tool, 
            verbose=True, 
            return_intermediate_steps=True, 
            handle_parsing_errors=True,
        )


        result = self.agent_executor.invoke({"input": input, "chat_history": self.chat_history})
        self.chat_history.extend(
            [
                HumanMessage(content=input),
                AIMessage(content=result["output"]),
            ]
        )

        lst=result["intermediate_steps"]
        citation = ""
        
        if lst != []:
            print(lst[0][1])

            #for tavily search only:
            if self.tool == self.tavily:
                try:
                    obj = json.dumps(lst[0][1])
                    urls = [item['url'] for item in json.loads(obj)]
                    for url in urls:
                        citation += f"\n\n{url}"
                except TypeError:
                    pass
        #print(f"this is it------------\n\n\n{result}\n\n\n")
        print(f"this------------\n\n\n{result['output']}\n\n\n")

        return result['output'], citation
    


gemini = Gemini()

def run(input: str, choice: search, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):
    print({"AI":choice})

    gemini.tools(choice)

    result, citation  = gemini.gemini(input)
    #print({"AI":result, "\n\nCITATIONS":citation})

    return {"AI":result, "CITATIONS":citation}
