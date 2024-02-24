# 24/7 Medical Support AI

This project is a software application designed to assist users in diagnosing their illnesses. It acts like a medical support companion available 24/7 at the reach of your phone, powered by Cohere and Google Gemini AI.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Cohere Integration](#cohere-integration)
- [Google Gemini Integration](#google-gemini-integration)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/247-medical-support-ai.git
cd 247-medical-support-ai
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
```bash
python main.py
```
The application will start and you can interact with it via the command line.

## File Structure
The project has the following file structure:
```
HEALTH/
│
├── database/
│   ├── __pycache__/
│   └── db.py
│
├── model/
│   ├── __pycache__/
│   └── users_model.py
│
├── schema/
│   ├── __pycache__/
│   └── users_schema.py
|
├── services/
|    ├── __pycache__/
|    ├── cohere.py 
|    └── gemini.py 
|
├─ user_services.py 
|
├─ venv/ 
|
├─ .gitignore 
|
├─ hashing.py 
|
├─ llama.py 
|
├─ main.py 
|
└─ requirements.txt  
```

## Cohere Integration
The `cohere.py` file contains code for integrating the Cohere API into the application. It uses FastAPI and SQLAlchemy to create an interactive endpoint where users can communicate with the AI for medical advice.

## Google Gemini Integration
The `gemini.py` file contains code for integrating Google's Gemini AI but is not yet set up to an endpoint. It will be functional after connecting it to an appropriate API endpoint.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
