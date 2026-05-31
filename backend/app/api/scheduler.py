from fastapi import APIRouter

from app.scheduler import run_all_sources, scheduler_status


router = APIRouter(prefix="/scheduler", tags=["scheduler"])


@router.post("/run")
def run_scheduler_now():
    return run_all_sources()


@router.get("/status")
def get_scheduler_status():
    return scheduler_status()
