from app.db.database import Base, SessionLocal, engine
from app.models.job import Job
from app.models.source import Source
from app.services.scraper import build_search_url


SEEDS = [
    ("Vagas Python Backend", "python backend"),
    ("Vagas Node.js", "node typescript"),
    ("Vagas Java Spring", "java spring"),
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for name, term in SEEDS:
            exists = db.query(Source).filter(Source.name == name).first()
            if exists:
                continue

            db.add(
                Source(
                    name=name,
                    search_term=term,
                    url=build_search_url(term),
                    interval_minutes=30,
                    is_active=True,
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
