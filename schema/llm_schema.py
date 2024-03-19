from pydantic import BaseModel, root_validator
from model.users_model import User
from database.db import SessionLocal
from fastapi import HTTPException, status
from enum import Enum


class choose(str, Enum):
    GEMINI = "Google Gemini AI"
    COHERE = "Cohere large AI"
    

class search(str, Enum):
    GOOGLE = "Google search"
    TAVILY = "Tavily search"


"""

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

import os
from dotenv import load_dotenv

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")
google_api_key = os.getenv("GOOGLE_API_KEY")


# REFACTORING OF GEMINI_____ to be removed from here to replace gemini current code


class Gemini:
    def __init__(self):
        self.description =  ""
                                You are a highly skilled and empathetic doctor.
                                Your primary role is to diagnose ailments based on the symptoms described by the patient.
                                Ask relevant questions to gather enough information about the patient's condition.
                                Once you have enough information, use the tool to provide a possible diagnosis and suggest appropriate treatments or medications.
                                Remember to maintain a professional and caring tone throughout the conversation.
                            ""
        self.tool = None

        self.tavily = None

        self.input = None

        self.agent_executor = None


    def tools(self, choose_tool):

        search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)

        google_tool = Tool(
            name = "google_search",
            description = self.description,
            func = search.run,
        )

        search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)

        tavily_tool = TavilySearchResults(api_wrapper=search, description=self.description)

        #testo:
        self.tavily = [tavily_tool]

        if choose_tool.lower() == "y":
            print("\nGoogle search activated\n")
            self.tool = [google_tool]

        elif choose_tool.lower() == "n":
            print("\nTavily search activated\n")
            self.tool = [tavily_tool]

        else:
            return "\nProvide a valid input (Y or N)\n"
        

    def gemini(self, input):
                
        self.input = input
        #--class.gemini:
        llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro", google_api_key=gemini_api_key)

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


        self.agent_executor = AgentExecutor(agent=agent, tools=self.tool, verbose=True, return_intermediate_steps=True, handle_parsing_errors=True)


    #def run(self):

        chat_history = []

        
        result = self.agent_executor.invoke({"input": input, "chat_history": chat_history})
        chat_history.extend(
            [
                HumanMessage(content=input),
                AIMessage(content=result["output"]),
            ]
        )

        #--def
        lst=result["intermediate_steps"]
        #print(lst)

        citation = []
        
        if lst != []:
            #print(lst[0][1])

            #for tavily search only:
            if self.tool == self.tavily:

                if lst[0][1] != "tavilly_search_results_json is not a valid tool, try one of [tavily_search_results_json]":
                    
                    obj = json.dumps(lst[0][1])

                    urls = [item['url'] for item in json.loads(obj)]

                    for url in urls:
                        citation.append(url)

                    #print(citation)

        return result['output'], citation



#def run(input: str, choice: search, db: Session = Depends(get_db), current_user: user = Depends(oauth.get_current_user)):
def main():
    
    gemini = Gemini()

    #gemini.tools(input(choice))

    gemini.tools(input("User: "))

    while True:

        input = input("User: ")

        result, citation  = gemini.gemini(input)
        print({"AI":result, "\n\nCITATIONS":citation})

        return {"AI":result, "CITATIONS":citation}

if __name__ == "__main__":
    main()

"""


"""#--class
description = ""
                You are a highly skilled and empathetic doctor.
                Your primary role is to diagnose ailments based on the symptoms described by the patient.
                Ask relevant questions to gather enough information about the patient's condition.
                Once you have enough information, use the tool to provide a possible diagnosis and suggest appropriate treatments or medications.
                Remember to maintain a professional and caring tone throughout the conversation.
            ""


#--class
search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)

#--class.tools:
google_tool = Tool(
    name = "google_search",
    description = description,
    func = search.run,
)
#--class.tools:
# Create the tool
search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
description = description
tavily_tool = TavilySearchResults(api_wrapper=search, description=description)

#--class.tools:
#NOTice: Choose search tool, between Tavily searchn and google search:
while True:
    choose_tool = input("Quick Result? (reply (y/n)): ")

    if choose_tool.lower() == "y":
        print("\nGoogle search activated\n")
        tools = [google_tool]
        break

    elif choose_tool.lower() == "n":
        print("\nTavily search activated\n")
        tools = [tavily_tool]
        break

    else:
        print("\nProvide a valid input (Y or N)\n")



#--class.gemini:
llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro", google_api_key=gemini_api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)



llm_with_tools = llm.bind(functions=tools)


from langchain_core.messages import AIMessage, HumanMessage

chat_history = []

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


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True, handle_parsing_errors=True)

#----------------I bruised my knee cap after falling off a tree

import json

#--class.run:
def run(input1):
    result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=input1),
            AIMessage(content=result["output"]),
        ]
    )

    #--def
    lst=result["intermediate_steps"]
    #print(lst)

    citation = []
    
    if lst != []:
        #print(lst[0][1])

        #for tavily search only:
        if tools == [tavily_tool]:

            if lst[0][1] != "tavilly_search_results_json is not a valid tool, try one of [tavily_search_results_json]":
                
                obj = json.dumps(lst[0][1])

                urls = [item['url'] for item in json.loads(obj)]

                for url in urls:
                    citation.append(url)

                #print(citation)

    return result['output'], citation

#--def
while True:
    input1 = input("User: ")

    result, citation  = run(input1)
    print({"AI":result, "\n\nCITATIONS":citation})


"""