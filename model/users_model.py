from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database.db import Base
from datetime import datetime, timedelta


#Usually for testing API endpoint.
#Use when connected to a frontend (not whatsapp).

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    verification_token = Column(String(255))
    is_verified = Column(Boolean, default=False)

    paid_start = Column(DateTime)
    paid_duration = Column(Integer)

    def is_paid(self):
        if self.paid_start and self.paid_duration:
            return self.paid_start + timedelta(days=self.paid_duration) > datetime.utcnow()
        else:
            return False