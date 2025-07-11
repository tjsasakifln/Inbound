from pydantic import BaseModel
from typing import Optional, Any

class LeadIn(BaseModel):
    email_id: str
    sender: str
    subject: str
    body: str

class LeadOut(LeadIn):
    id: int
    score: float
    stage: str
    source: str
    intent: Optional[str] = None
    entities: Optional[dict[str, Any]] = None

    class Config:
        from_attributes = True
