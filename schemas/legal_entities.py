from pydantic import BaseModel, Field
from uuid import UUID

class LegalEntityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., max_length=200)
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')

class LegalEntityCreate(LegalEntityBase):
    pass

class LegalEntityUpdate(LegalEntityBase):
    pass

class LegalEntityResponse(LegalEntityBase):
    id: UUID

    class Config:
        from_attributes = True
