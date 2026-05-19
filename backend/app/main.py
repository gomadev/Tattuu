"""Aplicação FastAPI - Tattuu Backend API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routes import users, artists, portfolios, ratings, favorites, search, admin
from app.database import Base, engine
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware, setup_logging
from app.jobs import get_job_manager
from app.events import producer
from app.lakehouse import LakehousePipeline

Base.metadata.create_all(bind=engine)

settings = get_settings()
setup_logging()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    debug=settings.DEBUG
)

app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
)
app.include_router(
    artists.router,
    prefix=settings.API_V1_STR,
)
app.include_router(
    portfolios.router,
    prefix=settings.API_V1_STR,
)
app.include_router(
    ratings.router,
    prefix=settings.API_V1_STR,
)
app.include_router(
    favorites.router,
    prefix=settings.API_V1_STR,
)
app.include_router(
    search.router,
    prefix=settings.API_V1_STR,
)
app.include_router(
    admin.router,
)


@app.get("/")
def read_root():
    return {
        "message": "Tattuu API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "tattuu-api",
        "lakehouse": "enabled",
        "kafka": producer.KAFKA_AVAILABLE
    }


@app.on_event("startup")
def startup_event():
    job_manager = get_job_manager()
    
    async def daily_batch_job(db):
        pipeline = LakehousePipeline(settings.DATA_LAKE_PATH)
        return pipeline.run_daily_batch(db)
    
    job_manager.register_job(
        "daily_lakehouse_batch",
        daily_batch_job,
        schedule_hour=2,
        description="Daily Lakehouse pipeline (Bronze → Silver → Gold)"
    )


@app.on_event("shutdown")
def shutdown_event():
    producer.get_event_producer().close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
