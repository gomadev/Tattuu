"""Batch job orchestration and scheduling."""
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal

logger = logging.getLogger("jobs")


class Job:
    def __init__(
        self,
        name: str,
        func: Callable,
        schedule_hour: int = 2,
        description: str = ""
    ):
        self.name = name
        self.func = func
        self.schedule_hour = schedule_hour
        self.description = description
        self.last_run: Optional[datetime] = None
        self.last_status: str = "pending"

    async def run(self, db: Session) -> dict:
        self.last_run = datetime.utcnow()
        try:
            logger.info(f"Running job: {self.name}")
            result = await self.func(db)
            self.last_status = "success"
            logger.info(f"Job completed: {self.name}")
            return {"job": self.name, "status": "success", "result": result}
        except Exception as e:
            self.last_status = "failed"
            logger.error(f"Job failed: {self.name} - {str(e)}", exc_info=True)
            return {"job": self.name, "status": "failed", "error": str(e)}

    def should_run(self) -> bool:
        now = datetime.utcnow()
        
        if self.last_run is None:
            return now.hour == self.schedule_hour
        
        last_run_date = self.last_run.date()
        now_date = now.date()
        
        return (
            now.hour == self.schedule_hour
            and last_run_date < now_date
        )


class JobManager:
    def __init__(self):
        self.jobs: dict[str, Job] = {}

    def register_job(
        self,
        name: str,
        func: Callable,
        schedule_hour: int = 2,
        description: str = ""
    ) -> Job:
        job = Job(name, func, schedule_hour, description)
        self.jobs[name] = job
        logger.info(f"Job registered: {name} - {description}")
        return job

    async def run_scheduled_jobs(self) -> list[dict]:
        db = SessionLocal()
        results = []
        
        try:
            for job_name, job in self.jobs.items():
                if job.should_run():
                    result = await job.run(db)
                    results.append(result)
        finally:
            db.close()
        
        return results

    async def run_job_now(self, job_name: str) -> dict:
        if job_name not in self.jobs:
            return {"job": job_name, "status": "not_found"}
        
        db = SessionLocal()
        try:
            return await self.jobs[job_name].run(db)
        finally:
            db.close()

    def get_job_status(self, job_name: str) -> Optional[dict]:
        if job_name not in self.jobs:
            return None
        
        job = self.jobs[job_name]
        return {
            "name": job.name,
            "description": job.description,
            "last_run": job.last_run.isoformat() if job.last_run else None,
            "last_status": job.last_status,
            "schedule_hour": job.schedule_hour,
        }

    def get_all_jobs_status(self) -> list[dict]:
        return [self.get_job_status(name) for name in self.jobs.keys()]


_job_manager: Optional[JobManager] = None


def get_job_manager() -> JobManager:
    global _job_manager
    if _job_manager is None:
        _job_manager = JobManager()
    return _job_manager
