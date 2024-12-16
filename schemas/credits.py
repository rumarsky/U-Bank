from pydantic import BaseModel, Field
from uuid import UUID

class CreditBase(BaseModel):
    name: str = Field(..., max_length=100)
    interest_rate: float = Field(..., ge=0)
    amount: float = Field(..., ge=0)
    repayment_term: int = Field(..., ge=1)

class CreditCreate(CreditBase):
    pass

class CreditUpdate(CreditBase):
    pass

class CreditResponse(CreditBase):
    id: UUID

    class Config:
        from_attributes = True
