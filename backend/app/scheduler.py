import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.source import Source
from app.services.detector import persist_new_jobs
from app.services.notifier import notify_job
from app.services.scraper import scrape_gupy


scheduler = BackgroundScheduler()


def run_source(source_id: str) -> int:
    db: Session = SessionLocal()
    try:
        source_uuid = uuid.UUID(str(source_id))
        source = db.query(Source).filter(Source.id == source_uuid, Source.is_active.is_(True)).first()
        if not source:
            return 0

        scraped_jobs = scrape_gupy(source.search_term, source.url)
        new_jobs = persist_new_jobs(db, source, scraped_jobs)

        notified_count = 0
        for job in new_jobs:
            if notify_job(job):
                job.notified = True
                notified_count += 1

        db.commit()
        return notified_count
    finally:
        db.close()


def run_all_sources() -> dict:
    db: Session = SessionLocal()
    try:
        sources = db.query(Source).filter(Source.is_active.is_(True)).all()
    finally:
        db.close()

    results = []
    for source in sources:
        results.append({"source_id": str(source.id), "notified": run_source(str(source.id))})

    return {"sources_processed": len(results), "results": results}


def reload_schedules() -> None:
    scheduler.remove_all_jobs()

    db: Session = SessionLocal()
    try:
        sources = db.query(Source).filter(Source.is_active.is_(True)).all()
        for source in sources:
            scheduler.add_job(
                run_source,
                "interval",
                minutes=source.interval_minutes,
                args=[str(source.id)],
                id=str(source.id),
                replace_existing=True,
            )
    finally:
        db.close()


def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.start()
    reload_schedules()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)


def scheduler_status() -> dict:
    return {
        "running": scheduler.running,
        "jobs": [
            {
                "id": job.id,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            }
            for job in scheduler.get_jobs()
        ],
    }
