from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from .database import Base
from datetime import datetime

class Lead(Base):
    __tablename__ = "leads"
    id          = Column(Integer, primary_key=True, index=True)
    email_id    = Column(String, unique=True, index=True)
    sender      = Column(String, index=True)
    subject     = Column(String)
    body        = Column(Text)
    score       = Column(Float, default=0.0)
    stage       = Column(String, default="NEW", index=True)   # NEW → QUALIFIED → WON
    source      = Column(String, default="EMAIL") # EMAIL, WEBFORM, etc.
    intent      = Column(String, nullable=True)
    entities    = Column(JSON, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

class PromptHistory(Base):
    __tablename__ = "prompt_history"
    id          = Column(Integer, primary_key=True, index=True)
    prompt      = Column(Text, nullable=False)
    response    = Column(Text, nullable=False)
    model_used  = Column(String, nullable=False)
    timestamp   = Column(DateTime, default=datetime.utcnow)
