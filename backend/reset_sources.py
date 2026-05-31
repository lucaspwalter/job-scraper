from app.db.database import Base, SessionLocal, engine
from app.models.job import Job
from app.models.source import Source
from app.services.scraper import build_search_url


SOURCES = [
    {"name": "Vagas Python Backend", "search_term": "python backend"},
    {"name": "Vagas Node.js TypeScript", "search_term": "node typescript"},
    {"name": "Vagas Java Spring", "search_term": "java spring"},
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Job).delete()
        db.query(Source).delete()

        for source_data in SOURCES:
            db.add(
                Source(
                    name=source_data["name"],
                    search_term=source_data["search_term"],
                    url=build_search_url(source_data["search_term"]),
                    interval_minutes=30,
                    is_active=True,
                )
            )

        db.commit()
        print("Sources e jobs resetados.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
