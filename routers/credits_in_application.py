from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.credits_in_application import (
    CreditsInApplicationCreate,
    CreditsInApplicationUpdate,
    CreditsInApplicationResponse,
)
from models import CreditsInApplication
from database import get_db
from uuid import UUID

router = APIRouter(prefix="/credits-in-application", tags=["Credits in application"])

@router.post("/", response_model=CreditsInApplicationResponse)
async def create_credit_in_application(data: CreditsInApplicationCreate, db: AsyncSession = Depends(get_db)):
    credit_in_application = CreditsInApplication(**data.dict())
    db.add(credit_in_application)
    await db.commit()
    return credit_in_application

@router.get("/", response_model=list[CreditsInApplicationResponse])
async def get_credits_in_application(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CreditsInApplication))
    return result.scalars().all()

@router.put("/{application_id}/{credit_id}", response_model=CreditsInApplicationResponse)
async def update_credit_in_application(
    application_id: UUID,
        credit_id: UUID,
        data: CreditsInApplicationUpdate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CreditsInApplication)
        .filter(CreditsInApplication.application_id == application_id)
        .filter(CreditsInApplication.credit_id == credit_id)
    )
    credit_in_application = result.scalars().first()
    if not credit_in_application:
        raise HTTPException(status_code=404, detail="Credit in application not found")
    credit_in_application.quantity = data.quantity
    await db.commit()
    return credit_in_application

@router.delete("/{application_id}/{credit_id}")
async def delete_credit_in_application(
        application_id: UUID,
        credit_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CreditsInApplication)
        .filter(CreditsInApplication.application_id == application_id)
        .filter(CreditsInApplication.credit_id == credit_id)
    )
    credit_in_application = result.scalars().first()
    if not credit_in_application:
        raise HTTPException(status_code=404, detail="Credit in application not found")
    await db.delete(credit_in_application)
    await db.commit()
    return {"message": "Credit in application deleted"}
