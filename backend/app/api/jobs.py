import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.job import Job


router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_id: uuid.UUID
    title: str
    company: str | None
    url: str
    found_at: datetime
    notified: bool


@router.get("", response_model=list[JobOut])
def list_jobs(source_id: uuid.UUID | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Job)
    if source_id:
        query = query.filter(Job.source_id == source_id)
    return query.order_by(Job.found_at.desc()).all()


@router.delete("/{job_id}")
def delete_job(job_id: uuid.UUID, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"deleted": True}
