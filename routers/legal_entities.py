from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import LegalEntity
from schemas import LegalEntityCreate, LegalEntityResponse, LegalEntityUpdate
from database import get_db
from uuid import UUID

router = APIRouter(prefix="/legal-entities", tags=["Legal entities"])

@router.post("/", response_model=LegalEntityResponse)
async def create_legal_entity(entity: LegalEntityCreate, db: AsyncSession = Depends(get_db)):
    legal_entity = LegalEntity(**entity.dict())
    db.add(legal_entity)
    await db.commit()
    await db.refresh(legal_entity)
    return legal_entity

@router.get("/", response_model=list[LegalEntityResponse])
async def get_legal_entities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LegalEntity))
    return result.scalars().all()

@router.put("/{entity_id}", response_model=LegalEntityResponse)
async def update_legal_entity(entity_id: UUID, entity_data: LegalEntityUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LegalEntity).where(LegalEntity.id == entity_id))
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    for field, value in entity_data.dict().items():
        setattr(entity, field, value)
    await db.commit()
    await db.refresh(entity)
    return entity

@router.delete("/{entity_id}", response_model=dict)
async def delete_legal_entity(entity_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LegalEntity).where(LegalEntity.id == entity_id))
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    await db.delete(entity)  # Удаляем сущность
    await db.commit()  # Подтверждаем изменения
    return {"message": "Entity deleted successfully"}
