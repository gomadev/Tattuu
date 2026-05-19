"""Admin routes for lakehouse pipeline management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.lakehouse import LakehousePipeline
from app.jobs import get_job_manager
from app.core.config import get_settings

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
settings = get_settings()


@router.post("/lakehouse/batch")
def trigger_batch_pipeline(db: Session = Depends(get_db)):
    try:
        pipeline = LakehousePipeline(settings.DATA_LAKE_PATH)
        result = pipeline.run_daily_batch(db)
        return {"status": "triggered", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/jobs/status")
def get_jobs_status():
    manager = get_job_manager()
    return manager.get_all_jobs_status()


@router.get("/jobs/{job_name}/status")
def get_job_status(job_name: str):
    manager = get_job_manager()
    status_info = manager.get_job_status(job_name)
    if status_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_name}' not found"
        )
    return status_info


@router.post("/jobs/{job_name}/run")
async def trigger_job(job_name: str):
    manager = get_job_manager()
    try:
        result = await manager.run_job_now(job_name)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
