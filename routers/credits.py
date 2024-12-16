from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.credits import CreditCreate, CreditUpdate, CreditResponse
from models import Credit
from database import get_db
from uuid import UUID

router = APIRouter(prefix="/credits", tags=["Credits"])

@router.post("/", response_model=CreditResponse)
async def create_credit(credit_data: CreditCreate, db: AsyncSession = Depends(get_db)):
    credit = Credit(**credit_data.dict())
    db.add(credit)
    await db.commit()
    await db.refresh(credit)
    return credit

@router.get("/", response_model=list[CreditResponse])
async def get_credits(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Credit))
    return result.scalars().all()

@router.put("/{credit_id}", response_model=CreditResponse)
async def update_credit(credit_id: UUID, credit_data: CreditUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Credit).filter(Credit.id == credit_id))
    credit = result.scalars().first()
    if not credit:
        raise HTTPException(status_code=404, detail="Credit not found")
    for field, value in credit_data.dict().items():
        setattr(credit, field, value)
    await db.commit()
    await db.refresh(credit)
    return credit

@router.delete("/{credit_id}")
async def delete_credit(credit_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Credit).filter(Credit.id == credit_id))
    credit = result.scalars().first()
    if not credit:
        raise HTTPException(status_code=404, detail="Credit not found")
    await db.delete(credit)
    await db.commit()
    return {"message": "Credit deleted"}
