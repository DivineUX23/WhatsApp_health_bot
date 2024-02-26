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


import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
tavily_api_key = os.getenv("TAVILY_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")
google_api_key = os.getenv("GOOGLE_API_KEY")


description = """
                You are a highly skilled and empathetic doctor.
                Your primary role is to diagnose ailments based on the symptoms described by the patient.
                Ask relevant questions to gather enough information about the patient's condition.
                Once you have enough information, use the tool to provide a possible diagnosis and suggest appropriate treatments or medications.
                Remember to maintain a professional and caring tone throughout the conversation.
            """



search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)


google_tool = Tool(
    name = "google_search",
    description = description,
    func = search.run,
)
#-------------------------------------------


# Create the tool
search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
description = description
tavily_tool = TavilySearchResults(api_wrapper=search, description=description)

tools = [tavily_tool]

#tools = [google_tool]

#llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro", convert_system_message_to_human=True, google_api_key="AIzaSyBwVvXkHRbgcp9Z2qLnDMV5lS7YfJKvIQk")



#______________________

llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro", google_api_key=gemini_api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

#_________________________

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

def run(input1):
    result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=input1),
            AIMessage(content=result["output"]),
        ]
    )

    lst=result["intermediate_steps"]
    #print(lst)

    citation = []
    
    if lst != []:
        #print(lst[0][1])

        #if search works:
        if lst[0][1] != "tavilly_search_results_json is not a valid tool, try one of [tavily_search_results_json]":
            
            obj = json.dumps(lst[0][1])

            urls = [item['url'] for item in json.loads(obj)]

            for url in urls:
                citation.append(url)

            #print(citation)

    return result['output'], citation


while True:
    input1 = input("User: ")

    result, citation  = run(input1)
    print({"AI":result, "\n\nCITATIONS":citation})