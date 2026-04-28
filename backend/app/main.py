"""Aplicação FastAPI - Tattuu Backend API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routes import users, artists
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

settings = get_settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    debug=settings.DEBUG
)

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


@app.get("/")
def read_root():
    """Endpoint raiz."""
    return {
        "message": "Tattuu API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check da API."""
    return {
        "status": "healthy",
        "service": "tattuu-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
