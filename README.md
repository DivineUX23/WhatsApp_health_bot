# 24/7 Medical Support AI on WhatsApp -----Documentation update coming soon: WhatsApp chat fully functional.

It's 2 am, and a sudden wave of unfamiliar symptoms disrupts your sleep.  With no recourse to a medical professional, you turn to your phone.  A sophisticated AI chatbot, readily available through your WhatsApp, analyzes your condition, offering potential diagnoses and suggesting over-the-counter remedies or home treatments.

This project is a conversational AI assistant in WhatsApp to help users diagnose their medical issues. It allows users to describe their symptoms and receive diagnostic suggestions and treatment recommendations. It acts like a medical support companion available 24/7 at the reach of your phone, powered by Cohere and Google Gemini AI.



## Problem statement
Millions in regions with limited healthcare suffer from undiagnosed illnesses. Lack of understanding leads to untreated conditions, escalating costs when early intervention could prevent complications. 

This project proposes a WhatsApp-based Conversational Health Chatbot to empower users with basic health tools for self-monitoring and informed decisions, preventing future complications.  

Focusing on WhatsApp leverages existing familiarity, especially in developing countries, and eliminates the need for app downloads or website navigation for cost-effective access.


## Overview

The assistant uses two AI models - Cohere and Google Gemini, to provide robust diagnosis capabilities. Users can have natural conversations with the assistant, describing any symptoms they are experiencing. If needed, the assistant will ask clarifying questions and provide possible diagnoses based on the symptoms. 

### Key features
The application is designed to interact with users, collecting information about their symptoms and providing possible diagnoses and treatments. Key features include:

- Users can choose between Cohere AI and Google Gemini AI to provide diagnosis based on user info and search results.

- Cohere AI powers the chatbot conversation. It is set up to provide diagnosis based on user info and search results.

- Google Gemini AI also powers the chatbot conversation fully capable of replacing Cohere AI. Users can choose to activate Google Gemini instead of Cohere AI.

- User input is analyzed to extract symptoms and gather information. The bot asks clarifying questions as needed. 

- Once the bot has enough information, it provides a tentative diagnosis and suggests potential treatments or next steps based on information from the web.

- Bot responses include citations/links to any external sources used.


## Table of Contents
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Cohere Integration](#cohere-integration)
- [Google Gemini Integration](#google-gemini-integration)

## Technologies

- FastAPI - REST API framework 
- SQLAlchemy - Database ORM
- Cohere - Conversational AI
- Google Gemini - Generative AI
- Google Search - Search API
- Tavily Search - Search API
- OAuth - Authentication


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
Create a `.env` file in your root directory and add your Cohere, Tavily, and Google API keys.
```plaintext
CohereAPI=your_cohere_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Run the main file:
```
uvicorn main:app
```
The application will start and you can interact with it via the command line.

The assistant will be available at http://localhost:8000/docs


## Usage

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
├── datab
│   └── Health
│       ├── __pycache__
│       └── db.py
├── model
│   ├── __pycache__
│   └── users_model.py
├── schema
│   ├── __pycache__
│   └── users_schema.py 
├── services 
│   ├── __pycache__ 
│   ├── cohere.py 
│   └── gemini.py 
├── user_services.py 
├── venv 
├── .env 
├── .gitignore 
├── hashing.py 
├── llama.py  
├── main.py  
├── oauth.py  
├── requirements.txt  
├── token_key.py  
├── user_login.py  
╰─ user.py   

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
