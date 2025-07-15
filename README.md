# MediChat AI: 24/7 Health Support on WhatsApp

Empowering personal healthcare, this project delivers a conversational AI assistant directly to users' WhatsApp, providing round-the-clock access to medical guidance. 

Through intuitive conversations, individuals can describe their symptoms and receive potential diagnoses, treatment recommendations, and reliable online resources - all powered by the cutting-edge Cohere and Google Gemini AI models. 

This innovative solution serves as a trusted 24/7 medical companion, offering expert insights at users' fingertips, anytime, anywhere.


## Video Demo


https://github.com/DivineUX23/WhatsApp_health_bot/assets/96517814/606e2a40-c259-4070-97ab-b077c8ed833f

"Google Gemini AI performing Diagnosis"


https://github.com/DivineUX23/WhatsApp_health_bot/assets/96517814/d92eb43e-3892-4e8d-b5c1-6a183f159f00

"Cohere AI Delivering In-depth Insights from Authoritative Health Resources, Complete with Direct Source Attributions"


## Problem statement

Millions in underserved regions lack access to healthcare, leading to undiagnosed illnesses and escalating costs due to delayed treatment. 

This project proposes a WhatsApp-based Conversational Health Chatbot to provide accessible self-monitoring tools and informed decision-making. 

Leveraging WhatsApp's familiarity, especially in developing countries, enables cost-effective access without dedicated app downloads or website navigation, empowering users to prevent complications through early intervention.


## Overview

The assistant uses two AI models - Cohere and Google Gemini, to provide robust diagnosis capabilities. Users can have natural conversations with the assistant, describing any symptoms they are experiencing. If needed, the assistant will ask clarifying questions and provide possible diagnoses based on the symptoms. 


### Key features

- WhatsApp Integration: Users can interact with the medical AI assistant through WhatsApp, leveraging the popular messaging platform's familiarity and accessibility.
  
- Cohere AI and Google Gemini AI: The assistant utilizes two powerful AI models, Cohere and Google Gemini, to provide robust diagnosis capabilities.
  
- Natural Conversation: Users can have natural conversations with the assistant, describing any symptoms they are experiencing. The assistant will ask clarifying questions as needed.

- Diagnosis Suggestions: Based on the user's symptoms, the assistant provides possible diagnoses and suggests potential treatments or next steps.
  
- Web Search Integration: The assistant incorporates web search results from Google Search and Tavily Search to enhance its knowledge base and provide more accurate recommendations.

- Citation Tracking: External sources used by the assistant for diagnosis or treatment recommendations are included as citations in the response.


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

- Twilio - A communication platform for integrating with WhatsApp.
  

## Installation
1. Clone the repository:
```
git clone https://github.com/DivineUX23/WhatsApp_health_bot.git
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

5. Access the API documentation at http://localhost:8000/docs to interact with the endpoints and test the functionality.

6. Users can initiate a conversation with the medical AI assistant by sending a message to the designated WhatsApp number, and the AI will engage in a dialogue to provide relevant health-related assistance.


## 🚀 Docker Quickstart

You can run this project instantly using Docker!
The latest image is available on [Docker Hub](https://hub.docker.com/r/divineux23/whatsapp-health-bot).

### Run the app with Docker

```sh
docker pull divineux23/whatsapp-health-bot:latest
docker run -p 8000:8000 --env-file .env divineux23/whatsapp-health-bot:latest
```

- Make sure to create a `.env` file in your current directory with all required environment variables (see the [Installation](#installation) section for details).
- The app will be available at [http://localhost:8000](http://localhost:8000).

### Deploy via Docker Image

You can deploy this image to any cloud provider that supports Docker images (e.g., Render, AWS, Azure, GCP, etc.).
Just use the image:
```
divineux23/whatsapp-health-bot:latest
```
and set the required environment variables.


## Usage

Once the application is running, you can interact with the medical AI assistant through WhatsApp. Simply send a message to the configured Twilio number, and the assistant will respond with prompts or questions to gather information about your symptoms.

Follow the assistant's instructions, and provide detailed descriptions of your symptoms. The assistant will use the information you provide to suggest possible diagnoses and recommend treatments or next steps.

The assistant may ask clarifying questions to understand your condition. Respond accordingly, and the assistant will continue refining its diagnosis and recommendations.

At the end of the conversation, the assistant will provide citations or links to the sources it used for its recommendations. Remember that the assistant's suggestions should not replace professional medical advice, diagnosis, or treatment.


## API Endpoint for testing

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

The project is organized into the following main components:

- `database`: Contains the database setup and utility functions for interacting with the SQLAlchemy database.
  
- `model`: Defines the User model for storing user data.
  
- `schema`: Defines the Pydantic schemas for data validation and serialization, including the User schema.
  
- `services`: Includes the core logic for the AI models and assistants.
  - `cohere.py`: Implements the Cohere AI model for conversational interactions.
  - `gemini.py`: Integrates the Google Gemini AI model for medical diagnosis and information retrieval.
    
- `main.py`: The main entry point for the FastAPI application, defining the API endpoints and routes.
  
- `.env`: Stores environment variables, including API keys and credentials.


Additional files:

- `user_service.py`: Contains shared utility functions for user-related operations.
  
- `oauth.py`: Implements OAuth2 authentication and authorization flows.
  
- `llama.py`: Manages the selection and instantiation of the AI models (Cohere or Gemini).
  
- `twilio.py`: Handles the integration with Twilio for WhatsApp messaging.
  
- `hashing.py`: Provides utility functions for password hashing and verification.
  
- `token_key.py`: Generates and manages the JWT token key.



## File Structure
The project has the following file structure:
``` HEALTH
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


## Google Gemini Integration
The `gemini.py` file integrates Google’s Gemini AI, Which provides diagnoses and recommends treatments. 

The code is constructed using the Langchain framework, which equips Google Gemini with the capability to search the web and deliver suitable health diagnoses:

- Interpret symptoms and provide relevant medical guidance.
  
- Engages users in a dialogue to gather comprehensive information about their health conditions.

- Suggests potential treatments, backed by data and research.
  
- API keys loaded from `.env`. 

- Built on LangChain library.

- Tools include Tavily search and Google search.



## Cohere Integration
The `cohere.py` file integrates the Cohere API into the application. It uses FastAPI and SQLAlchemy to create an interactive endpoint where users can communicate with the AI for medical advice. Some key points:

- Delivers in-depth insights from Authoritative health resources.

- Provides direct citation of reputable online sources utilized.

- The Cohere API key is stored in `.env` and loaded at runtime.

- Unique conversation ID generated for each chat session.

- Overridable preamble provides bot instructions/persona.

- Citations extracted and returned.



## Contributing
Pull requests are welcome! Feel free to open issues for any bugs or ideas for new features.

Some areas that could use improvement:

- Enhancing the system prompt for better performance.

- Building a user account system to track diagnosis history

- Enhancing the search capabilities and knowledge base for more accurate recommendations.
