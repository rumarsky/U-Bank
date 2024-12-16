from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

class ApplicationBase(BaseModel):
    legal_entity_id: UUID
    submission_date: date
    status: str = Field(..., max_length=50)

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id: UUID

    class Config:
        from_attributes = True
