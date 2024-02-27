from pydantic import BaseModel, root_validator
from model.users_model import User
from database.db import SessionLocal
from fastapi import HTTPException, status
from enum import Enum



class choose(str, Enum):
    COHERE = "Cohere large AI"
    GEMINI = "Google Gemini AI"

