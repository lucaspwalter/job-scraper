from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.source import Source


def persist_new_jobs(db: Session, source: Source, scraped_jobs: list[dict]) -> list[Job]:
    new_jobs = []

    for scraped_job in scraped_jobs:
        url = scraped_job.get("url")
        title = scraped_job.get("title")
        if not url or not title:
            continue

        exists = db.query(Job).filter(Job.url == url).first()
        if exists:
            continue

        job = Job(
            source_id=source.id,
            title=title,
            company=scraped_job.get("company"),
            url=url,
        )
        db.add(job)
        new_jobs.append(job)

    db.commit()

    for job in new_jobs:
        db.refresh(job)

    return new_jobs
