import strawberry
from fastapi import Depends
from .schemas import LeadOut
from .database import SessionLocal
from .models import Lead
from .auth import get_current_user
from aiocache import cached, Cache
from typing import Optional, Any
from strawberry.scalars import JSON

@strawberry.input
class UserType:
    username: str

@strawberry.type
class LeadType:
    id: int
    email_id: str
    sender: str
    subject: str
    body: str
    score: float
    stage: str
    source: str
    intent: Optional[str] = None
    entities: Optional[JSON] = None

@strawberry.type
class Query:
    @strawberry.field
    @cached(ttl=60, cache=Cache.REDIS, key_builder=lambda f, *args, **kwargs: f"leads:{kwargs.get('stage', 'all')}") # Cache for 60 seconds
    async def leads(self, stage: str | None = None, current_user: UserType = Depends(get_current_user)) -> list[LeadType]:
        db = SessionLocal()
        q = db.query(Lead)
        if stage:
            q = q.filter(Lead.stage == stage)
        leads = q.all()
        return [LeadType(**lead_item.__dict__) for lead_item in leads]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_lead_stage(self, lead_id: int, new_stage: str, current_user: UserType = Depends(get_current_user)) -> LeadType:
        db = SessionLocal()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if lead:
            old_stage = lead.stage # Capture old stage before update
            lead.stage = new_stage
            db.commit()
            db.refresh(lead)
            updated_lead = LeadType(**lead.__dict__)
            # Invalidate cache for leads query
            await Cache.get_by_name("default").delete_many([f"leads:{old_stage}", f"leads:{new_stage}", "leads:all"])
            db.close()
            return updated_lead
        db.close()
        raise Exception(f"Lead with id {lead_id} not found")

schema = strawberry.Schema(query=Query, mutation=Mutation)
