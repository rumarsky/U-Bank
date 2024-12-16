from fastapi import FastAPI
from routers import legal_entities_router, credits_router, applications_router, credits_in_application_router
from utils.logger import setup_logger
from contextlib import asynccontextmanager

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    logger.info("Application starting up...")
    yield
    # Действия при завершении работы приложения
    logger.info("Application shutting down...")

# Инициализация приложения с использованием lifespan
app = FastAPI(lifespan=lifespan)

# Подключение маршрутов
app.include_router(legal_entities_router)
app.include_router(credits_router)
app.include_router(applications_router)
app.include_router(credits_in_application_router)
