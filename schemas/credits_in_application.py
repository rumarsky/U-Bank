from pydantic import BaseModel
from uuid import UUID

class CreditsInApplicationBase(BaseModel):
    application_id: UUID
    credit_id: UUID
    quantity: int

class CreditsInApplicationCreate(CreditsInApplicationBase):
    pass

class CreditsInApplicationUpdate(BaseModel):
    quantity: int

class CreditsInApplicationResponse(CreditsInApplicationBase):
    pass

    class Config:
        from_attributes = True
