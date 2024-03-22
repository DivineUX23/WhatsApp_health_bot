# 24/7 Medical Support AI on WhatsApp -----Documentation update coming soon: WhatsApp chat fully functional.

It's 2 am, and a sudden wave of unfamiliar symptoms disrupts your sleep.  With no recourse to a medical professional, you turn to your phone.  A sophisticated AI chatbot, readily available through your WhatsApp, analyzes your condition, offering potential diagnoses and suggesting over-the-counter remedies or home treatments.

This project is a conversational AI assistant in WhatsApp to help users diagnose their medical issues. It allows users to describe their symptoms and receive diagnostic suggestions and treatment recommendations. It acts like a medical support companion available 24/7 at the reach of your phone, powered by Cohere and Google Gemini AI.



## Problem statement
Millions in regions with limited healthcare suffer from undiagnosed illnesses. Lack of understanding leads to untreated conditions, escalating costs when early intervention could prevent complications. 

This project proposes a WhatsApp-based Conversational Health Chatbot to empower users with basic health tools for self-monitoring and informed decisions, preventing future complications.  

Focusing on WhatsApp as the frontend leverages existing familiarity, especially in developing countries, and eliminates the need for app downloads or website navigation for cost-effective access.


## Overview

The assistant uses two AI models - Cohere and Google Gemini, to provide robust diagnosis capabilities. Users can have natural conversations with the assistant, describing any symptoms they are experiencing. If needed, the assistant will ask clarifying questions and provide possible diagnoses based on the symptoms. 

### Key features

- WhatsApp Integration: Users can interact with the medical AI assistant directly through WhatsApp, leveraging the popular messaging platform's familiarity and accessibility.
  
- Cohere AI and Google Gemini AI: The assistant utilizes two powerful AI models, Cohere and Google Gemini, to provide robust diagnosis capabilities.
  
- Natural Conversation: Users can have natural conversations with the assistant, describing any symptoms they are experiencing. The assistant will ask clarifying questions as needed.

- Diagnosis Suggestions: Based on the user's symptoms, the assistant provides possible diagnoses and suggests potential treatments or next steps.
  
- Web Search Integration: The assistant incorporates web search results from Google Search and Tavily Search to enhance its knowledge base and provide more accurate recommendations.

- Citation Tracking: Any external sources used by the assistant for diagnosis or treatment recommendations are included as citations in the response.

## Table of Contents
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Cohere Integration](#cohere-integration)
- [Google Gemini Integration](#google-gemini-integration)

## Technologies

- FastAPI - REST API framework for building the backend server.
- SQLAlchemy - Database ORM for user management and data storage.
- Cohere - Conversational AI model for natural language processing.
- Google Gemini - Generative AI model for diagnosis and treatment suggestions.
- Google Search - Web search integration for gathering relevant health information.
- Tavily Search - Alternative web search integration option.
- OAuth - Authentication system for user accounts.
- Twilio - Communication platform for integrating with WhatsApp.
  

## Installation
1. Clone the repository:
```
git clone https://github.com/DivineUX23/Health_cohere.git
```
2. (Optional) Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the dependencies:
```bash
pip install -r requirements.txt  
```
4. Set up environment variables:
Create a `.env` file in your root directory and add your Cohere, Tavily, Google, and Twilio API keys.
```plaintext
CohereAPI=your_cohere_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_CSE_ID=your_google_cse_id
GOOGLE_API_KEY=your_google_api_key
account_sid=your_twilio_account_sid
auth_token=your_twilio_auth_token
FROM=your_twilio_number
```

Run the main file:
```
uvicorn main:app
```
The application will start, and you can interact with it via WhatsApp by sending messages to the configured Twilio number.

The assistant will also be available at http://localhost:8000/docs



## Usage

Once the application is running, you can interact with the medical AI assistant through WhatsApp. Simply send a message to the configured Twilio number, and the assistant will respond with prompts or questions to gather information about your symptoms.

Follow the assistant's instructions, and provide detailed descriptions of your symptoms. The assistant will use the information you provide to suggest possible diagnoses and recommend treatments or next steps.

The assistant may ask clarifying questions to better understand your condition. Respond accordingly, and the assistant will continue refining its diagnosis and recommendations.

At the end of the conversation, the assistant will provide citations or links to the sources it used for its recommendations. Remember that the assistant's suggestions should not replace professional medical advice, diagnosis, or treatment.


## Usage (API Endpoint for testing)

Interact with the assistant through the `/conversation` endpoint. 

Send a POST request with your message as the `input` body parameter. The API will call the assistant and return the response.

Example request:

```
POST /conversation
{
    "input": "I have a bad headache and fever" 
}
```

Example response:

```json
{
    "AI": "Based on your symptoms of headache and fever, it sounds like you may have a viral infection like the flu or a cold. Some things you can try....",
    "citations": ["https://www.webmd.com/cold-and-flu/default.htm", "https://www.cdc.gov/flu/index.htm"] 
}
```

The `AI` field contains the assistant's response. `citations` includes any pages the assistant used for reference.


## Code Structure

The code is structured into the following folders:

- `database`: Contains DB setup and access logic.

- `model`: Defines the User model.

- `schema`: Validation schemas for Users. 

- `services`: Individual bot logic - `cohere.py` and `gemini.py`.

- `main.py`: Main app startup and endpoints.

- `.env`: Stores credentials and API keys.

Other files:

- `user_service.py`: Shared user logic.

- `oauth.py`: Auth routes. 

- Etc.



## File Structure
The project has the following file structure:
```HEALTH
Health
├── database
│   └── db.py
├── model
│   └── users_model.py
├── schema
│   └── users_schema.py
│   └── llm_schema.py
├── services
│   ├── cohere.py
│   ├── gemini.py
│   └── twilio.py
├── venv
├── .env
├── hashing.py
├── llama.py
├── main.py
├── oauth.py
├── requirements.txt
├── token_key.py
├── user_login.py
└── user.py   

```

## Cohere Integration
The `cohere.py` file contains code for integrating the Cohere API into the application. It uses FastAPI and SQLAlchemy to create an interactive endpoint where users can communicate with the AI for medical advice. Some key points:

- Cohere API key is stored in `.env` and loaded at runtime.

- Unique conversation ID generated for each chat session.

- Overridable preamble provides bot instructions/persona.

- Bot responses streamed back line-by-line.

- Citations extracted and returned.


## Google Gemini Integration
The `gemini.py` file includes code that integrates Google’s Gemini AI. This AI can be used to provide medical advice, serving as an alternative to the Cohere API. 

The code is constructed using the Langchain framework, which equips Google Gemini with the capability to search the web and deliver suitable health diagnoses. 

Furthermore, it employs FastAPI and SQLAlchemy to establish an interactive endpoint, enabling users to seek medical advice from the AI. Some key points:

- API keys loaded from `.env`. 

- Built on LangChain library.

- Tools include Tavily search and Google search.

- Prompt formats bot responses.

- Results post-processed to extract citations.


## Further Work

- Connect endpoints to UI.

- Add user account features. 

- Expand bot knowledge base for more robust conversations.

- Improve diagnosis accuracy with medical datasets.

- Add more search tools.


## Contributing
Pull requests are welcome! Feel free to open issues for any bugs or ideas for new features.

Some areas that could use improvement:

- Expanding the vocabulary and training data for medical symptom understanding
- Integrating additional healthcare APIs for diagnosis suggestions
- Building a user account system to track diagnosis history
- Improving the natural language processing and conversation flow.
- Enhancing the search capabilities and knowledge base for more accurate recommendations.
