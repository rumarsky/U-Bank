from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.applications import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from models import Application
from database import get_db
from uuid import UUID

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse)
async def create_application(application_data: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    application = Application(**application_data.dict())
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application

@router.get("/", response_model=list[ApplicationResponse])
async def get_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application))
    return result.scalars().all()

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(application_id: UUID, application_data: ApplicationUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).filter(Application.id == application_id))
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    for field, value in application_data.dict().items():
        setattr(application, field, value)
    await db.commit()
    await db.refresh(application)
    return application

@router.delete("/{application_id}")
async def delete_application(application_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).filter(Application.id == application_id))
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    await db.delete(application)
    await db.commit()
    return {"message": "Application deleted"}
