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