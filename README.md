# 24/7 Medical Support AI

This project is a software application designed to assist users in diagnosing their illnesses. It acts like a medical support companion available 24/7 at the reach of your phone, powered by Cohere and Google Gemini AI.

## Overview

The code implements a conversational chatbot using two different AI models - Cohere and Google's Gemini. Users can have a natural conversation with the bot to describe their symptoms, and the bot will try to determine a possible diagnosis and suggest treatments. 

### Note
The application is designed to interact with users, collecting information about their symptoms and providing possible diagnoses and treatments.


Key features:

- Cohere AI powers the chatbot conversation. It is set up to to provide diagnosis based on user info and search results.

- Google Gemini AI also powers the chatbot conversation fully capable of replacing Cohere AI but is not yet set up to an endpoint.

- User input is analyzed to extract symptoms and gather information. The bot asks clarifying questions as needed. 

- Once the bot has enough information, it provides a tentative diagnosis and suggests potential treatments or next steps based on information from the web.

- Bot responses include citations/links to any external sources used.


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Cohere Integration](#cohere-integration)
- [Google Gemini Integration](#google-gemini-integration)

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

## Usage
Run the main file:
```
uvicorn main:app
```
The application will start and you can interact with it via the command line.



## Code Structure

The code is structured into the following folders:

- `database`: Contains DB setup and access logic.

- `model`: Defines the User model.

- `schema`: Validation schemas for User. 

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
The `gemini.py` file contains code for integrating Google's Gemini AI which can be used for medical advice in place of Cohere API but is not yet set up to an endpoint. It will be functional after connecting it to an appropriate API endpoint.

- API keys loaded from `.env`. 

- Built on LangChain library.

- Tools include Tavily search and Google search.

- Prompt formats bot responses.

- Results post-processed to extract citations.


## Further Work

- Connect Google Gemini AI to the endpoint

- Option to choose between Cohere AI and Google Gemini AI

- Connect endpoints to UI.

- Add user account features. 

- Expand bot knowledge base for more robust conversations.

- Improve diagnosis accuracy with medical datasets.

- Add more search tools.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
