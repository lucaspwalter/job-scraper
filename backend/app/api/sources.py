import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.source import Source
from app.scheduler import reload_schedules
from app.services.scraper import build_search_url


router = APIRouter(prefix="/sources", tags=["sources"])


class SourceBase(BaseModel):
    name: str
    search_term: str
    url: str | None = None
    interval_minutes: int = 30
    is_active: bool = True


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: str | None = None
    search_term: str | None = None
    url: str | None = None
    interval_minutes: int | None = None
    is_active: bool | None = None


class SourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    url: str
    search_term: str
    interval_minutes: int
    is_active: bool
    created_at: datetime


@router.post("", response_model=SourceOut)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    source = Source(
        name=payload.name,
        search_term=payload.search_term,
        url=payload.url or build_search_url(payload.search_term),
        interval_minutes=payload.interval_minutes,
        is_active=payload.is_active,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    reload_schedules()
    return source


@router.get("", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).order_by(Source.created_at.desc()).all()


@router.put("/{source_id}", response_model=SourceOut)
def update_source(source_id: uuid.UUID, payload: SourceUpdate, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        if field == "url" and value is None:
            continue
        setattr(source, field, value)

    if "search_term" in updates and "url" not in updates:
        source.url = build_search_url(source.search_term)

    db.commit()
    db.refresh(source)
    reload_schedules()
    return source


@router.delete("/{source_id}")
def delete_source(source_id: uuid.UUID, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    db.delete(source)
    db.commit()
    reload_schedules()
    return {"deleted": True}
